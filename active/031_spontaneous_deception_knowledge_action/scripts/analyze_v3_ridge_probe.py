#!/usr/bin/env python3
"""Run the final stronger linear-probe check for the V3 reachability gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from analyze_v3_reachability import auroc, normalized


ALPHAS = (1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0)


def fit_ridge_direction(
    fit_states: Any, fit_labels: Any, validation_states: Any, validation_labels: Any
) -> tuple[Any, float, float]:
    """Fit a dual ridge direction and choose alpha only on validation AUROC."""
    import numpy as np

    center = fit_states.mean(axis=0, keepdims=True)
    scale = float(np.sqrt(np.mean((fit_states - center) ** 2)))
    x = (fit_states - center) / scale
    validation_x = (validation_states - center) / scale
    y = np.where(fit_labels, 1.0, -1.0)
    y -= y.mean()
    gram = x @ x.T / x.shape[1]
    eigenvalues, eigenvectors = np.linalg.eigh(gram)
    projected_y = eigenvectors.T @ y
    best = None
    for alpha in ALPHAS:
        dual = eigenvectors @ (projected_y / (eigenvalues + alpha))
        direction = normalized(x.T @ dual / x.shape[1])
        score = validation_x @ direction
        auc = auroc(validation_labels, score)
        candidate = (auc, -alpha, direction)
        if best is None or candidate[:2] > best[:2]:
            best = candidate
    return best[2], -best[1], best[0]


def analyze(states_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    import numpy as np

    data = np.load(states_path)
    hidden = data["hidden_states"]
    graph_ids = data["graph_ids"].astype(str)
    splits = data["splits"].astype(str)
    polarity = data["polarities"].astype(str)
    reachable = data["reachable"].astype(bool)
    expected_yes = data["expected_answers"].astype(str) == "Yes"
    train_graphs = sorted(set(graph_ids[splits == "train"]))
    validation_graphs = set(train_graphs[::4])
    fit = (splits == "train") & ~np.isin(graph_ids, list(validation_graphs))
    validation = (splits == "train") & np.isin(graph_ids, list(validation_graphs))
    test = splits == "test"
    recipient = splits == "recipient"
    zero = np.zeros(hidden.shape[2], dtype=np.float32)
    positive_directions, reverse_directions, invariant_directions = [zero], [zero], [zero]
    layers = []
    for layer in range(1, hidden.shape[1]):
        states = hidden[:, layer].astype(np.float32)
        fit_positive = fit & (polarity == "positive")
        fit_reverse = fit & (polarity == "reverse")
        val_positive = validation & (polarity == "positive")
        val_reverse = validation & (polarity == "reverse")
        d_positive, alpha_positive, val_auc_positive = fit_ridge_direction(
            states[fit_positive], reachable[fit_positive], states[val_positive], reachable[val_positive]
        )
        d_reverse, alpha_reverse, val_auc_reverse = fit_ridge_direction(
            states[fit_reverse], reachable[fit_reverse], states[val_reverse], reachable[val_reverse]
        )
        d_invariant = normalized(d_positive + d_reverse)
        positive_directions.append(d_positive.astype(np.float32))
        reverse_directions.append(d_reverse.astype(np.float32))
        invariant_directions.append(d_invariant.astype(np.float32))
        score_positive = states @ d_positive
        score_reverse = states @ d_reverse
        score_invariant = states @ d_invariant
        test_positive = test & (polarity == "positive")
        test_reverse = test & (polarity == "reverse")
        layers.append(
            {
                "layer": layer,
                "alpha_positive": alpha_positive,
                "alpha_reverse": alpha_reverse,
                "validation_auc_positive": val_auc_positive,
                "validation_auc_reverse": val_auc_reverse,
                "direction_cosine_positive_reverse": float(d_positive @ d_reverse),
                "same_polarity_auc_positive": auroc(reachable[test_positive], score_positive[test_positive]),
                "same_polarity_auc_reverse": auroc(reachable[test_reverse], score_reverse[test_reverse]),
                "cross_polarity_auc_positive_to_reverse": auroc(reachable[test_reverse], score_positive[test_reverse]),
                "cross_polarity_auc_reverse_to_positive": auroc(reachable[test_positive], score_reverse[test_positive]),
                "invariant_reachability_auc": auroc(reachable[test], score_invariant[test]),
                "invariant_answer_yes_auc": auroc(expected_yes[test], score_invariant[test]),
                "recipient_invariant_reachability_auc": auroc(
                    reachable[recipient], score_invariant[recipient]
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
        "measurement": "dual ridge linear reachability probe with graph-group fit/validation/test",
        "alphas": list(ALPHAS),
        "n_fit_graphs": len(set(graph_ids[fit])),
        "n_validation_graphs": len(validation_graphs),
        "n_test_graphs": len(set(graph_ids[test])),
        "gate_passed": bool(passing),
        "passing_layers": [row["layer"] for row in passing],
        "best_invariant_layer": best,
        "layers": layers,
    }
    directions = {
        "positive": np.asarray(positive_directions),
        "reverse": np.asarray(reverse_directions),
        "invariant": np.asarray(invariant_directions),
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
