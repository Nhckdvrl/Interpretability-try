from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable

from .io import read_jsonl, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bootstrap-replicates", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=16002)
    return parser.parse_args()


def aggregate_orders(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["pair_id"], row["condition"])].append(row)
    output = {}
    for key, local in grouped.items():
        if {row["option_order"] for row in local} != {"canonical", "reversed"}:
            raise ValueError(f"Missing option counterbalance for {key}")
        first = local[0]
        output[key] = {
            "pair_id": key[0],
            "condition": key[1],
            "doc_id": first["doc_id"],
            "direction": first["direction"],
            "target_label": first["target_label"],
            "neighbor_label": first["neighbor_label"],
            "has_explicit_relation": first["has_explicit_relation"],
            "same_sentence": first["same_sentence"],
            "target_event_type": first["target_event_type"],
            "neighbor_event_type": first["neighbor_event_type"],
            "target_probability": sum(row["label_probabilities"][first["target_label"]] for row in local) / 2,
            "neighbor_probability": sum(row["label_probabilities"][first["neighbor_label"]] for row in local) / 2,
            "mean_accuracy": sum(bool(row["correct"]) for row in local) / 2,
            "both_correct": all(bool(row["correct"]) for row in local),
            "both_toward_neighbor": all(bool(row["toward_neighbor"]) for row in local),
        }
    return output


def cluster_means(rows: list[dict[str, Any]], value: Callable[[dict[str, Any]], float]) -> list[float]:
    clusters: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        clusters[row["doc_id"]].append(float(value(row)))
    return [sum(values) / len(values) for values in clusters.values()]


def bootstrap(values: list[float], replicates: int, seed: int) -> dict[str, float]:
    import numpy as np

    if not values:
        return {"estimate": float("nan"), "ci_low": float("nan"), "ci_high": float("nan")}
    array = np.asarray(values)
    rng = np.random.default_rng(seed)
    samples = rng.choice(array, size=(replicates, len(array)), replace=True).mean(1)
    low, high = np.quantile(samples, [0.025, 0.975])
    return {"estimate": float(array.mean()), "ci_low": float(low), "ci_high": float(high)}


def contrasts(
    items: list[dict[str, dict[str, Any]]], replicates: int, seed: int
) -> dict[str, Any]:
    def values(left: str, right: str, metric: str) -> list[float]:
        rows = [
            {
                "doc_id": item[left]["doc_id"],
                "value": item[left][metric] - item[right][metric],
            }
            for item in items
        ]
        return cluster_means(rows, lambda row: row["value"])

    def binary(left: str, right: str, metric: str) -> list[float]:
        rows = [
            {
                "doc_id": item[left]["doc_id"],
                "value": float(item[left][metric]) - float(item[right][metric]),
            }
            for item in items
        ]
        return cluster_means(rows, lambda row: row["value"])

    specs = {
        "mixed_minus_local_neighbor_probability": ("mixed_status_natural", "target_local", "neighbor_probability"),
        "same_minus_local_pseudo_neighbor_probability": ("same_status_natural", "target_local", "neighbor_probability"),
        "mixed_minus_same_neighbor_probability": ("mixed_status_natural", "same_status_natural", "neighbor_probability"),
        "mixed_reversed_minus_same_reversed_neighbor_probability": ("mixed_status_reversed", "same_status_reversed", "neighbor_probability"),
        "full_minus_local_neighbor_probability": ("full_local_discourse", "target_local", "neighbor_probability"),
        "local_minus_mixed_target_accuracy": ("target_local", "mixed_status_natural", "mean_accuracy"),
        "local_minus_same_target_accuracy": ("target_local", "same_status_natural", "mean_accuracy"),
    }
    report = {}
    for index, (name, (left, right, metric)) in enumerate(specs.items()):
        report[name] = bootstrap(values(left, right, metric), replicates, seed + index)
    report["mixed_minus_same_toward_neighbor_transition"] = bootstrap(
        binary("mixed_status_natural", "same_status_natural", "both_toward_neighbor"),
        replicates,
        seed + 20,
    )
    report["full_minus_same_toward_neighbor_transition"] = bootstrap(
        binary("full_local_discourse", "same_status_natural", "both_toward_neighbor"),
        replicates,
        seed + 21,
    )
    return report


def analyze_model(rows: list[dict[str, Any]], replicates: int, seed: int) -> dict[str, Any]:
    aggregated = aggregate_orders(rows)
    pair_ids = sorted({row["pair_id"] for row in rows})
    conditions = sorted({row["condition"] for row in rows})
    complete = [{condition: aggregated[(pair_id, condition)] for condition in conditions} for pair_id in pair_ids]
    gated = [item for item in complete if item["target_local"]["both_correct"]]
    primary = [
        item for item in gated
        if item["target_local"]["target_label"] != "Uu"
        and item["target_local"]["neighbor_label"] != "Uu"
    ]

    condition_metrics = {}
    for condition in conditions:
        local = [item[condition] for item in gated]
        condition_metrics[condition] = {
            "mean_order_accuracy": sum(row["mean_accuracy"] for row in local) / len(local) if local else float("nan"),
            "both_order_accuracy": sum(row["both_correct"] for row in local) / len(local) if local else float("nan"),
            "toward_neighbor_both_order_rate": sum(row["both_toward_neighbor"] for row in local) / len(local) if local else float("nan"),
            "mean_target_probability": sum(row["target_probability"] for row in local) / len(local) if local else float("nan"),
            "mean_neighbor_probability": sum(row["neighbor_probability"] for row in local) / len(local) if local else float("nan"),
        }

    directions = {}
    for direction in sorted({item["target_local"]["direction"] for item in primary}):
        local = [item for item in primary if item["target_local"]["direction"] == direction]
        directions[direction] = {
            "n_pairs": len(local),
            "n_documents": len({item["target_local"]["doc_id"] for item in local}),
            "contrasts": contrasts(local, replicates, seed + sum(map(ord, direction))),
        }
    strata = {}
    for name, predicate in {
        "no_explicit_relation": lambda item: not item["target_local"]["has_explicit_relation"],
        "explicit_relation": lambda item: item["target_local"]["has_explicit_relation"],
        "different_sentence": lambda item: not item["target_local"]["same_sentence"],
        "same_sentence": lambda item: item["target_local"]["same_sentence"],
    }.items():
        local = [item for item in primary if predicate(item)]
        strata[name] = {
            "n_pairs": len(local),
            "n_documents": len({item["target_local"]["doc_id"] for item in local}),
            "contrasts": contrasts(local, replicates, seed + sum(map(ord, name))),
        }

    return {
        "model_label": rows[0]["model_label"],
        "n_pairs": len(complete),
        "n_documents": len({item["target_local"]["doc_id"] for item in complete}),
        "recognition_gated_pairs": len(gated),
        "recognition_gated_documents": len({item["target_local"]["doc_id"] for item in gated}),
        "recognition_gate_rate": len(gated) / len(complete),
        "primary_gated_pairs": len(primary),
        "condition_metrics_gated": condition_metrics,
        "primary_contrasts": contrasts(primary, replicates, seed),
        "direction_results": directions,
        "validity_strata": strata,
    }


def main() -> None:
    args = parse_args()
    models = []
    for index, path in enumerate(args.inputs):
        rows = list(read_jsonl(path))
        models.append(analyze_model(rows, args.bootstrap_replicates, args.seed + index * 1000))
    report = {
        "analysis": "Option-order averaged; recognition-gated; document-cluster bootstrap",
        "bootstrap_replicates": args.bootstrap_replicates,
        "models": models,
    }
    write_json(args.output, report)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
