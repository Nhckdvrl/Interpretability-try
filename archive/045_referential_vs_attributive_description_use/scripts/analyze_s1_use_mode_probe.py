"""Is there a use-mode state at the description token that survives held-out frame paraphrases?

Unlike 041's modifier probe, layer 0 is *not* expected to be at chance here: referential and
attributive frames differ lexically, so a shallow probe can read the frame's words. The control
that matters is therefore paraphrase transfer — train on two wordings of each mode and test on the
third — together with item-held-out folds.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


def auc(labels: np.ndarray, scores: np.ndarray) -> float:
    positive, negative = scores[labels == 1], scores[labels == 0]
    if not len(positive) or not len(negative):
        return float("nan")
    comparisons = (positive[:, None] > negative[None, :]).astype(float)
    comparisons += 0.5 * (positive[:, None] == negative[None, :])
    return float(comparisons.mean())


def mass_mean(train_x, train_y):
    positive, negative = train_x[train_y == 1].mean(0), train_x[train_y == 0].mean(0)
    direction = positive - negative
    return direction / max(float(np.linalg.norm(direction)), 1e-9)


def held_out(features, labels, folds, train_mask=None):
    scores = np.zeros(len(labels))
    source = np.ones(len(labels), dtype=bool) if train_mask is None else train_mask
    for fold in np.unique(folds):
        test = folds == fold
        train = (~test) & source
        if len(np.unique(labels[train])) < 2:
            continue
        centre, scale = features[train].mean(0), features[train].std(0) + 1e-6
        direction = mass_mean((features[train] - centre) / scale, labels[train])
        scores[test] = ((features[test] - centre) / scale) @ direction
    return scores


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    models = []
    for path in args.inputs:
        lines = [json.loads(line) for line in path.read_text().splitlines() if line]
        metadata = next(row for row in lines if row["record_type"] == "metadata")
        rows = [row for row in lines if row["record_type"] == "example"]
        bundle = np.load(path.with_name(metadata["states_file"]))
        states = bundle["states"]
        keys = {str(value): index for index, value in enumerate(bundle["state_keys"])}
        seen = {}
        for row in rows:
            if row["context"] == "attributive_bare":
                continue
            seen.setdefault(row["state_key"], row)
        entries = [seen[key] for key in sorted(seen)]
        indices = np.array([keys[row["state_key"]] for row in entries])
        labels = np.array([int(row["context"] == "referential") for row in entries])
        items = np.array([row["item"] for row in entries])
        # r1/a1 -> 0, r2/a2 -> 1, r3/a3 -> 2, so a fold holds out one wording of *each* mode
        paraphrase = np.array([int(row["frame"][1]) - 1 for row in entries])
        probes = {}
        for position, fraction in enumerate(config["depth_fractions"]):
            features = states[indices, position, :].astype(np.float32)
            probes[f"{fraction:g}"] = {
                "residual_layer": int(bundle["residual_layers"][position]),
                "item_held_out_auc": auc(labels, held_out(features, labels, items)),
                "paraphrase_held_out_auc": auc(labels, held_out(features, labels, paraphrase)),
            }
        gate = [f"{value:g}" for value in config["gate_depth_fractions"]]
        models.append({
            "model": metadata["model_checkpoint"], "n_states": len(entries), "probes": probes,
            "best_paraphrase_held_out_auc": max(probes[f]["paraphrase_held_out_auc"] for f in gate),
            "best_item_held_out_auc": max(probes[f]["item_held_out_auc"] for f in gate),
        })
    result = {"contract": "a use-mode state at the description token that survives held-out frame wordings",
              "models": models}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    for model in models:
        print(f"{model['model'][:40]:40s} paraphrase-held-out {model['best_paraphrase_held_out_auc']:.3f} "
              f"| item-held-out {model['best_item_held_out_auc']:.3f}")


if __name__ == "__main__":
    main()
