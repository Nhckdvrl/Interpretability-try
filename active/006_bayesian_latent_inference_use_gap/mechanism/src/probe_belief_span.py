#!/usr/bin/env python3
"""Grouped linear probes over the joint eight-token posterior span."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from mechanism_data import dump_jsonl, load_jsonl
from probe_timeline import grouped_probe, target_value


def run(args: argparse.Namespace) -> dict:
    import numpy as np
    import torch

    cache = torch.load(args.cache, map_location="cpu", weights_only=True)
    activations = cache["activations"]
    metadata = load_jsonl(Path(args.metadata))
    if activations.shape[0] != len(metadata):
        raise ValueError("metadata/cache row mismatch")
    results = []
    for condition in args.conditions:
        indices = [i for i, row in enumerate(metadata) if row["condition"] == condition]
        groups = np.array([metadata[i]["evidence_id"] for i in indices])
        layer_indices = args.layers or list(range(activations.shape[1]))
        for layer_i in layer_indices:
            states = activations[indices, layer_i].float().numpy()
            all_features = {
                "mean": states.mean(axis=1),
                "concat": states.reshape(len(indices), -1),
            }
            features = {name: all_features[name] for name in args.poolings}
            for pooling, X in features.items():
                for target in args.targets:
                    y = np.array([target_value(metadata[i], target) for i in indices])
                    binary = target == "condition_action"
                    results.append(
                        {
                            "condition": condition,
                            "pooling": pooling,
                            "layer": layer_i - 1,
                            "hidden_state_index": layer_i,
                            "target": target,
                            "n": len(indices),
                            **grouped_probe(X, y, groups, args.alpha, binary),
                        }
                    )
    dump_jsonl(results, Path(args.out))
    top = []
    for condition in args.conditions:
        for pooling in args.poolings:
            for target in args.targets:
                candidates = [
                    row
                    for row in results
                    if row["condition"] == condition
                    and row["pooling"] == pooling
                    and row["target"] == target
                ]
                metric = "balanced_accuracy" if target == "condition_action" else "pearson"
                top.append(max(candidates, key=lambda row: row.get(metric) or -float("inf")))
    summary = {"n_results": len(results), "top": top}
    Path(args.summary).write_text(json.dumps(summary, indent=2) + "\n")
    return {"n_results": len(results), "out": args.out, "summary": args.summary}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--alpha", type=float, default=100.0)
    parser.add_argument("--layers", nargs="+", type=int)
    parser.add_argument("--poolings", nargs="+", choices=("mean", "concat"), default=["mean", "concat"])
    parser.add_argument(
        "--conditions", nargs="+", default=["gold_bridge", "self_mean_bridge"]
    )
    parser.add_argument(
        "--targets",
        nargs="+",
        default=[
            "serialized_posterior_logit",
            "serialized_decision_margin",
            "condition_action",
        ],
    )
    args = parser.parse_args()
    print(json.dumps(run(args), indent=2))


if __name__ == "__main__":
    main()
