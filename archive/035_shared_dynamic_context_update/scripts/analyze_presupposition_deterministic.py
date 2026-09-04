"""Aggregate counterbalanced predictions at the source-item level."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from sklearn.metrics import balanced_accuracy_score, confusion_matrix


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--inputs", type=Path, nargs="+", required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    summaries = []
    for path in args.inputs:
        lines = [json.loads(x) for x in path.read_text().splitlines() if x]
        meta = next(x for x in lines if x["record_type"] == "metadata")
        rows = [x for x in lines if x["record_type"] == "example"]
        grouped = defaultdict(list)
        for row in rows:
            grouped[row["id"]].append(row)
        gold, pred = [], []
        forced_binary_gold, forced_binary_pred = [], []
        label_stability = []
        by_band_margin = defaultdict(list)
        for item_rows in grouped.values():
            semantic_scores = {
                semantic: float(np.mean([row["semantic_scores"][semantic] for row in item_rows]))
                for semantic in ["low", "mid", "high"]
            }
            item_gold = item_rows[0]["probability"]
            item_pred = max(semantic_scores, key=semantic_scores.get)
            gold.append(item_gold)
            pred.append(item_pred)
            if item_gold in {"high", "low"}:
                forced_binary_gold.append(item_gold)
                forced_binary_pred.append(max(["high", "low"], key=semantic_scores.get))
            margin = semantic_scores[item_gold] - max(value for key, value in semantic_scores.items() if key != item_gold)
            by_band_margin[item_gold].append(margin)
            label_stability.append(len({row["prediction_semantic"] for row in item_rows}) == 1)
        order = ["low", "mid", "high"]
        balanced = float(balanced_accuracy_score(gold, pred))
        high_low = [i for i, value in enumerate(gold) if value in {"high", "low"}]
        three_way_high_low_accuracy = float(np.mean([pred[i] == gold[i] for i in high_low]))
        forced_binary_high_low_accuracy = float(np.mean([
            observed == expected for observed, expected in zip(forced_binary_pred, forced_binary_gold)
        ]))
        summaries.append({
            "model": meta["model_checkpoint"], "model_revision": meta["model_revision"],
            "n_source_items": len(grouped), "n_counterbalanced_prompts": len(rows),
            "balanced_accuracy": balanced,
            "three_way_high_low_item_accuracy": three_way_high_low_accuracy,
            "forced_binary_high_low_accuracy": forced_binary_high_low_accuracy,
            "confusion_matrix_labels": order,
            "confusion_matrix": confusion_matrix(gold, pred, labels=order).tolist(),
            "prediction_counts": dict(Counter(pred)),
            "label_order_stability_rate": float(np.mean(label_stability)),
            "mean_gold_margin_by_band": {key: float(np.mean(values)) for key, values in by_band_margin.items()},
            "gate_pass": bool(balanced >= config["gate"]["min_balanced_accuracy"]
                              and forced_binary_high_low_accuracy >= config["gate"]["min_high_vs_low_pair_accuracy"]),
        })
    result = {
        "contract": "label-counterbalanced deterministic presupposition probability classification",
        "models": summaries,
        "panel_gate_pass": bool(len(summaries) >= 2 and all(x["gate_pass"] for x in summaries)),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
