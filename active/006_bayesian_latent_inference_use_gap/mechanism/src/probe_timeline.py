#!/usr/bin/env python3
"""Cross-family ridge probes over cached residual states.

These probes are diagnostic maps only.  Causal claims require the interchange
experiments in residual_interchange.py.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from mechanism_data import dump_jsonl, load_jsonl


def target_value(row: dict, target: str) -> float:
    if target == "posterior_logit":
        return float(row["posterior_logit"])
    if target == "raw_posterior":
        return float(row["gold_p_a"])
    if target == "decision_margin":
        return float(row["decision_margin"])
    if target == "raw_margin":
        return float(row["raw_margin"])
    if target == "semantic_action":
        return 1.0 if row["gold_action"] == "ACT" else -1.0
    if target == "serialized_posterior_logit":
        value = (
            row["posterior_mean"]
            if row["condition"] == "self_mean_bridge"
            else row["gold_p_a"]
        )
        value = min(max(float(value), 1e-6), 1 - 1e-6)
        return math.log(value / (1 - value))
    if target == "serialized_decision_margin":
        value = (
            row["posterior_mean"]
            if row["condition"] == "self_mean_bridge"
            else row["gold_p_a"]
        )
        value = min(max(float(value), 1e-6), 1 - 1e-6)
        threshold = min(max(float(row["threshold"]), 1e-6), 1 - 1e-6)
        return math.log(value / (1 - value)) - math.log(threshold / (1 - threshold))
    if target == "condition_action":
        return 1.0 if row["condition_action"] == "ACT" else -1.0
    if target == "mapping":
        return 1.0 if row["option_mapping"][0] == "ACT" else -1.0
    raise ValueError(target)


def pearson(x, y) -> float | None:
    import numpy as np

    if len(x) < 2 or np.std(x) == 0 or np.std(y) == 0:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def grouped_probe(X, y, groups, alpha: float, binary: bool) -> dict:
    import numpy as np
    from sklearn.linear_model import Ridge
    from sklearn.metrics import balanced_accuracy_score, r2_score
    from sklearn.model_selection import GroupKFold

    unique_groups = np.unique(groups)
    n_splits = min(5, len(unique_groups))
    predictions = np.zeros_like(y, dtype=float)
    splitter = GroupKFold(n_splits=n_splits)
    for train, test in splitter.split(X, y, groups):
        model = Ridge(alpha=alpha)
        model.fit(X[train], y[train])
        predictions[test] = model.predict(X[test])
    result = {
        "pearson": pearson(predictions, y),
        "prediction_std": float(np.std(predictions)),
    }
    if binary:
        result["balanced_accuracy"] = float(
            balanced_accuracy_score(y > 0, predictions > 0)
        )
    else:
        result["r2"] = float(r2_score(y, predictions))
        result["mae"] = float(np.mean(np.abs(predictions - y)))
    return result


def cross_format_probe(X_train, y_train, X_test, y_test, alpha: float, binary: bool) -> dict:
    import numpy as np
    from sklearn.linear_model import Ridge
    from sklearn.metrics import balanced_accuracy_score, r2_score

    model = Ridge(alpha=alpha)
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    result = {"pearson": pearson(prediction, y_test)}
    if binary:
        result["balanced_accuracy"] = float(
            balanced_accuracy_score(y_test > 0, prediction > 0)
        )
    else:
        result["r2"] = float(r2_score(y_test, prediction))
        result["mae"] = float(np.mean(np.abs(prediction - y_test)))
    return result


def run(args: argparse.Namespace) -> dict:
    import numpy as np
    import torch

    cache = torch.load(args.cache, map_location="cpu", weights_only=True)
    activations = cache["activations"]
    all_anchors = cache["anchors"]
    metadata = load_jsonl(Path(args.metadata))
    if len(metadata) != activations.shape[0]:
        raise ValueError("metadata/cache row mismatch")
    anchors = args.anchors or all_anchors
    conditions = args.conditions or sorted({row["condition"] for row in metadata})
    results = []

    for condition in conditions:
        indices = [i for i, row in enumerate(metadata) if row["condition"] == condition]
        if not indices:
            continue
        groups = np.array([metadata[i]["evidence_id"] for i in indices])
        for anchor in anchors:
            anchor_i = all_anchors.index(anchor)
            for layer in range(activations.shape[1]):
                X = activations[indices, layer, anchor_i].float().numpy()
                for target in args.targets:
                    y = np.array([target_value(metadata[i], target) for i in indices])
                    binary = target in ("semantic_action", "condition_action", "mapping")
                    metric = grouped_probe(X, y, groups, args.alpha, binary)
                    results.append(
                        {
                            "kind": "within_format_group_cv",
                            "condition": condition,
                            "anchor": anchor,
                            "layer": layer - 1,
                            "hidden_state_index": layer,
                            "target": target,
                            "n": len(indices),
                            **metric,
                        }
                    )

    # Train on an explicit-belief context and test the matched direct rows.
    if "direct" in conditions:
        for train_condition in ("gold_bridge", "self_mean_bridge"):
            if train_condition not in conditions:
                continue
            train_by_key = {
                (row["case_id"], row["surface_id"]): i
                for i, row in enumerate(metadata)
                if row["condition"] == train_condition
            }
            test_by_key = {
                (row["case_id"], row["surface_id"]): i
                for i, row in enumerate(metadata)
                if row["condition"] == "direct"
            }
            keys = sorted(set(train_by_key) & set(test_by_key))
            train_indices = [train_by_key[key] for key in keys]
            test_indices = [test_by_key[key] for key in keys]
            for anchor in anchors:
                anchor_i = all_anchors.index(anchor)
                for layer in range(activations.shape[1]):
                    X_train = activations[train_indices, layer, anchor_i].float().numpy()
                    X_test = activations[test_indices, layer, anchor_i].float().numpy()
                    for target in args.targets:
                        y_train = np.array(
                            [target_value(metadata[i], target) for i in train_indices]
                        )
                        y_test = np.array(
                            [target_value(metadata[i], target) for i in test_indices]
                        )
                        binary = target in ("semantic_action", "condition_action", "mapping")
                        metric = cross_format_probe(
                            X_train, y_train, X_test, y_test, args.alpha, binary
                        )
                        results.append(
                            {
                                "kind": "cross_format",
                                "train_condition": train_condition,
                                "test_condition": "direct",
                                "anchor": anchor,
                                "layer": layer - 1,
                                "hidden_state_index": layer,
                                "target": target,
                                "n": len(keys),
                                **metric,
                            }
                        )

    dump_jsonl(results, Path(args.out))
    top = {}
    for row in results:
        key = (
            row["kind"],
            row.get("condition", row.get("train_condition")),
            row["anchor"],
            row["target"],
        )
        score = row.get("balanced_accuracy", row.get("pearson"))
        score = -math.inf if score is None else score
        if key not in top or score > top[key][0]:
            top[key] = (score, row)
    summary = {"n_results": len(results), "top": [value[1] for value in top.values()]}
    Path(args.summary).write_text(json.dumps(summary, indent=2) + "\n")
    return {"n_results": len(results), "out": args.out, "summary": args.summary}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--alpha", type=float, default=100.0)
    parser.add_argument("--conditions", nargs="+")
    parser.add_argument("--anchors", nargs="+")
    parser.add_argument(
        "--targets",
        nargs="+",
        default=["posterior_logit", "decision_margin", "semantic_action", "mapping"],
    )
    args = parser.parse_args()
    print(json.dumps(run(args), indent=2))


if __name__ == "__main__":
    main()
