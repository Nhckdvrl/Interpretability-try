from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable

from .io import read_jsonl, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze paired clarification-lag results.")
    parser.add_argument("--inputs", nargs="+", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bootstrap-replicates", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=15002)
    return parser.parse_args()


def aggregate_orders(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["pair_id"], row["condition"])].append(row)
    aggregated: dict[tuple[str, str], dict[str, Any]] = {}
    for key, local in grouped.items():
        orders = {row["answer_order"] for row in local}
        if orders != {"target_first", "target_second"}:
            raise ValueError(f"Missing counterbalance for {key}: {orders}")
        aggregated[key] = {
            "pair_id": key[0],
            "condition": key[1],
            "question_id": local[0]["question_id"],
            "property_count": local[0]["property_count"],
            "probability": sum(float(row["gold_probability"]) for row in local) / 2,
            "accuracy": sum(bool(row["correct"]) for row in local) / 2,
            "both_correct": all(bool(row["correct"]) for row in local),
        }
    return aggregated


def cluster_values(
    pair_rows: list[dict[str, Any]], value: Callable[[dict[str, Any]], float]
) -> list[float]:
    clusters: dict[str, list[float]] = defaultdict(list)
    for row in pair_rows:
        clusters[row["question_id"]].append(value(row))
    return [sum(values) / len(values) for values in clusters.values()]


def bootstrap_mean(values: list[float], replicates: int, seed: int) -> dict[str, float]:
    import numpy as np

    if not values:
        return {"estimate": float("nan"), "ci_low": float("nan"), "ci_high": float("nan")}
    array = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    draws = rng.choice(array, size=(replicates, len(array)), replace=True).mean(axis=1)
    low, high = np.quantile(draws, [0.025, 0.975])
    return {"estimate": float(array.mean()), "ci_low": float(low), "ci_high": float(high)}


def analyze_model(
    rows: list[dict[str, Any]], replicates: int, seed: int
) -> dict[str, Any]:
    aggregated = aggregate_orders(rows)
    pair_ids = sorted({row["pair_id"] for row in rows})
    complete = []
    for pair_id in pair_ids:
        local = {condition: aggregated[(pair_id, condition)] for condition in (
            "direct", "ambiguity_history", "matched_history", "wrong_condition"
        )}
        direct, wrong = local["direct"], local["wrong_condition"]
        if direct["both_correct"] and wrong["both_correct"]:
            complete.append(local)

    def contrast(left: str, right: str, metric: str) -> list[float]:
        pair_rows = [
            {
                "question_id": local[left]["question_id"],
                "value": float(local[left][metric]) - float(local[right][metric]),
            }
            for local in complete
        ]
        return cluster_values(pair_rows, lambda row: row["value"])

    all_direct = [aggregated[(pair_id, "direct")] for pair_id in pair_ids]
    all_wrong = [aggregated[(pair_id, "wrong_condition")] for pair_id in pair_ids]
    ungated_condition_metrics = {}
    for condition in ("direct", "ambiguity_history", "matched_history", "wrong_condition"):
        local = [aggregated[(pair_id, condition)] for pair_id in pair_ids]
        ungated_condition_metrics[condition] = {
            "mean_order_accuracy": sum(float(row["accuracy"]) for row in local) / len(local),
            "both_order_accuracy": sum(bool(row["both_correct"]) for row in local) / len(local),
            "mean_gold_probability": sum(float(row["probability"]) for row in local) / len(local),
        }
    gated_condition_metrics = {}
    for condition in ("direct", "ambiguity_history", "matched_history", "wrong_condition"):
        local = [item[condition] for item in complete]
        gated_condition_metrics[condition] = {
            "mean_order_accuracy": (
                sum(float(row["accuracy"]) for row in local) / len(local) if local else float("nan")
            ),
            "both_order_accuracy": (
                sum(bool(row["both_correct"]) for row in local) / len(local)
                if local
                else float("nan")
            ),
            "mean_gold_probability": (
                sum(float(row["probability"]) for row in local) / len(local)
                if local
                else float("nan")
            ),
        }
    results = {
        "model_label": rows[0]["model_label"],
        "n_pairs": len(pair_ids),
        "n_questions": len({row["question_id"] for row in rows}),
        "recognition_gated_pairs": len(complete),
        "recognition_gated_questions": len(
            {local["direct"]["question_id"] for local in complete}
        ),
        "recognition_gated_pair_rate": len(complete) / len(pair_ids),
        "ungated_direct_both_order_accuracy": sum(row["both_correct"] for row in all_direct)
        / len(all_direct),
        "ungated_wrong_condition_both_order_accuracy": sum(
            row["both_correct"] for row in all_wrong
        )
        / len(all_wrong),
        "ungated_condition_metrics": ungated_condition_metrics,
        "gated_condition_metrics": gated_condition_metrics,
        "gated_contrasts": {
            "direct_minus_ambiguity_accuracy": bootstrap_mean(
                contrast("direct", "ambiguity_history", "accuracy"), replicates, seed + 1
            ),
            "direct_minus_ambiguity_probability": bootstrap_mean(
                contrast("direct", "ambiguity_history", "probability"), replicates, seed + 2
            ),
            "direct_minus_matched_accuracy": bootstrap_mean(
                contrast("direct", "matched_history", "accuracy"), replicates, seed + 3
            ),
            "direct_minus_matched_probability": bootstrap_mean(
                contrast("direct", "matched_history", "probability"), replicates, seed + 4
            ),
            "matched_minus_ambiguity_accuracy": bootstrap_mean(
                contrast("matched_history", "ambiguity_history", "accuracy"), replicates, seed + 5
            ),
            "matched_minus_ambiguity_probability": bootstrap_mean(
                contrast("matched_history", "ambiguity_history", "probability"), replicates, seed + 6
            ),
        },
        "label_accuracy": {},
    }
    for label in ("A", "B"):
        label_rows = [row for row in rows if row["gold_label"] == label]
        results["label_accuracy"][label] = sum(bool(row["correct"]) for row in label_rows) / len(
            label_rows
        )
    return results


def main() -> None:
    args = parse_args()
    reports = []
    for index, path in enumerate(args.inputs):
        rows = list(read_jsonl(path))
        if not rows:
            raise ValueError(f"No rows in {path}")
        reports.append(analyze_model(rows, args.bootstrap_replicates, args.seed + index * 100))
    report = {
        "analysis": "D0 paired A/B next-token scoring; answer orders averaged; question-cluster bootstrap",
        "bootstrap_replicates": args.bootstrap_replicates,
        "models": reports,
    }
    write_json(args.output, report)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
