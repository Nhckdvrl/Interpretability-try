#!/usr/bin/env python3
"""Evaluate held-out and cross-polarity reachability directions for V3."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def average_ranks(values: Any) -> Any:
    import numpy as np

    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=float)
    start = 0
    while start < len(values):
        end = start + 1
        while end < len(values) and values[order[end]] == values[order[start]]:
            end += 1
        ranks[order[start:end]] = (start + 1 + end) / 2
        start = end
    return ranks


def auroc(labels: Any, scores: Any) -> float:
    import numpy as np

    labels = np.asarray(labels, dtype=bool)
    scores = np.asarray(scores, dtype=float)
    n_pos, n_neg = int(labels.sum()), int((~labels).sum())
    if not n_pos or not n_neg:
        raise ValueError("AUROC needs both classes")
    rank_sum = average_ranks(scores)[labels].sum()
    return float((rank_sum - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def normalized(vector: Any) -> Any:
    import numpy as np

    norm = np.linalg.norm(vector)
    if norm == 0:
        raise ValueError("Zero direction")
    return vector / norm


def semantic_direction(states: Any, reachable: Any, mask: Any) -> Any:
    return normalized(states[mask & reachable].mean(axis=0) - states[mask & ~reachable].mean(axis=0))


def analyze(arrays_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    import numpy as np

    data = np.load(arrays_path)
    hidden = data["hidden_states"].astype(np.float32)
    split = data["splits"].astype(str)
    polarity = data["polarities"].astype(str)
    reachable = data["reachable"].astype(bool)
    expected_yes = data["expected_answers"].astype(str) == "Yes"
    train = split == "train"
    test = split == "test"
    recipient = split == "recipient"
    layers = []
    invariant_directions = [np.zeros(hidden.shape[2], dtype=np.float32)]
    positive_directions = [np.zeros(hidden.shape[2], dtype=np.float32)]
    reverse_directions = [np.zeros(hidden.shape[2], dtype=np.float32)]
    for layer in range(1, hidden.shape[1]):
        states = hidden[:, layer]
        d_positive = semantic_direction(states, reachable, train & (polarity == "positive"))
        d_reverse = semantic_direction(states, reachable, train & (polarity == "reverse"))
        d_invariant = normalized(d_positive + d_reverse)
        positive_directions.append(d_positive)
        reverse_directions.append(d_reverse)
        invariant_directions.append(d_invariant)
        scores_positive = states @ d_positive
        scores_reverse = states @ d_reverse
        scores_invariant = states @ d_invariant
        test_positive = test & (polarity == "positive")
        test_reverse = test & (polarity == "reverse")
        pooled_test = test
        layers.append(
            {
                "layer": layer,
                "direction_cosine_positive_reverse": float(d_positive @ d_reverse),
                "same_polarity_auc_positive": auroc(reachable[test_positive], scores_positive[test_positive]),
                "same_polarity_auc_reverse": auroc(reachable[test_reverse], scores_reverse[test_reverse]),
                "cross_polarity_auc_positive_to_reverse": auroc(reachable[test_reverse], scores_positive[test_reverse]),
                "cross_polarity_auc_reverse_to_positive": auroc(reachable[test_positive], scores_reverse[test_positive]),
                "invariant_reachability_auc": auroc(reachable[pooled_test], scores_invariant[pooled_test]),
                "invariant_answer_yes_auc": auroc(expected_yes[pooled_test], scores_invariant[pooled_test]),
                "recipient_invariant_reachability_auc": auroc(
                    reachable[recipient], scores_invariant[recipient]
                ),
            }
        )
    passing = [
        row for row in layers
        if row["invariant_reachability_auc"] >= 0.8
        and row["cross_polarity_auc_positive_to_reverse"] >= 0.7
        and row["cross_polarity_auc_reverse_to_positive"] >= 0.7
        and row["direction_cosine_positive_reverse"] > 0
        and 0.4 <= row["invariant_answer_yes_auc"] <= 0.6
    ]
    best = max(layers, key=lambda row: row["invariant_reachability_auc"])
    summary = {
        "schema_version": 1,
        "measurement": "mean-difference reachability direction trained on graph-group train split",
        "gate_a": "held-out invariant reachability AUROC >= 0.8",
        "gate_b": "both cross-polarity AUROCs >= 0.7, direction cosine > 0, answer AUROC in [0.4, 0.6]",
        "n_layers": len(layers),
        "passing_layers": [row["layer"] for row in passing],
        "gate_passed": bool(passing),
        "best_invariant_layer": best,
        "layers": layers,
    }
    directions = {
        "positive": np.asarray(positive_directions, dtype=np.float32),
        "reverse": np.asarray(reverse_directions, dtype=np.float32),
        "invariant": np.asarray(invariant_directions, dtype=np.float32),
    }
    return summary, directions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--states", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    parser.add_argument("--directions-out", type=Path, required=True)
    args = parser.parse_args()
    import numpy as np

    summary, directions = analyze(args.states)
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.directions_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    np.savez(args.directions_out, **directions)
    print(json.dumps({key: summary[key] for key in ("gate_passed", "passing_layers", "best_invariant_layer")}, indent=2))


if __name__ == "__main__":
    main()
