"""Under rising task load, does the model's *use* of the restriction role fall faster than its representation?"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


def cluster_bootstrap(units: dict[str, float], seed: int, n_boot: int) -> dict:
    keys = sorted(units)
    values = np.array([units[key] for key in keys])
    rng = np.random.default_rng(seed)
    draws = [float(values[rng.integers(0, len(keys), len(keys))].mean()) for _ in range(n_boot)]
    return {"estimate": float(values.mean()), "ci95": [float(v) for v in np.quantile(draws, [0.025, 0.975])],
            "n_worlds": len(keys)}


def auc(labels: np.ndarray, scores: np.ndarray) -> float:
    positive, negative = scores[labels == 1], scores[labels == 0]
    if not len(positive) or not len(negative):
        return float("nan")
    wins = (positive[:, None] > negative[None, :]).astype(float)
    wins += 0.5 * (positive[:, None] == negative[None, :])
    return float(wins.mean())


def held_out_scores(features: np.ndarray, labels: np.ndarray, folds: np.ndarray) -> np.ndarray:
    scores = np.zeros(len(labels))
    for fold in np.unique(folds):
        test = folds == fold
        train = ~test
        if len(np.unique(labels[train])) < 2:
            continue
        centre, scale = features[train].mean(0), features[train].std(0) + 1e-6
        normalised = (features[train] - centre) / scale
        direction = normalised[labels[train] == 1].mean(0) - normalised[labels[train] == 0].mean(0)
        direction = direction / max(float(np.linalg.norm(direction)), 1e-9)
        scores[test] = ((features[test] - centre) / scale) @ direction
    return scores


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    n_boot = int(config["bootstrap_samples"])
    models = []
    for model_index, path in enumerate(args.inputs):
        lines = [json.loads(line) for line in path.read_text().splitlines() if line]
        metadata = next(row for row in lines if row["record_type"] == "metadata")
        rows = [row for row in lines if row["record_type"] == "example"]
        seed = int(config["seed"]) + 100 * model_index

        margins = defaultdict(list)
        for row in rows:
            margins[(row["world_id"], row["description_condition"])].append(row["referent_margin"])
        means = {key: float(np.mean(values)) for key, values in margins.items()}
        meta = {row["world_id"]: row for row in rows if row["dropped_slot"] is None}

        bundle = np.load(path.with_name(metadata["states_file"]))
        states = bundle["states"]
        keys = {str(value): index for index, value in enumerate(bundle["state_keys"])}
        fractions = list(metadata["depth_fractions"])

        cells = {}
        for world in meta.values():
            cells.setdefault((world["load_axis"], world["n_modifiers"], world["n_candidates"]), [])
        for world_id, world in meta.items():
            cells[(world["load_axis"], world["n_modifiers"], world["n_candidates"])].append(world_id)

        cell_results = {}
        for (axis, n_mod, n_cand), world_ids in sorted(cells.items()):
            use_units, accuracy = {}, []
            for world_id in world_ids:
                world = meta[world_id]
                full = means.get((world_id, "full"))
                restricting = means.get((world_id, f"drop_{world['restricting_slot']}"))
                others = [means[(world_id, f"drop_{slot}")] for slot in range(n_mod)
                          if slot != world["restricting_slot"] and (world_id, f"drop_{slot}") in means]
                if full is None or restricting is None or not others:
                    continue
                use_units[world_id] = (full - restricting) - (full - float(np.mean(others)))
            accuracy = [row["correct"] for row in rows
                        if row["world_id"] in set(world_ids) and row["dropped_slot"] is None]
            entry = {"n_modifiers": n_mod, "n_candidates": n_cand,
                     "full_description_accuracy": float(np.mean(accuracy)) if accuracy else float("nan"),
                     "role_use": cluster_bootstrap(use_units, seed, n_boot)}
            index_list, labels, folds = [], [], []
            for world_id in world_ids:
                world = meta[world_id]
                for slot in range(n_mod):
                    key = f"{world_id}|None|{slot}" if f"{world_id}|None|{slot}" in keys else f"{world_id}|None"
                    key = f"{world_id}|None|{slot}"
                    if key not in keys:
                        continue
                    index_list.append(keys[key]); labels.append(int(slot == world["restricting_slot"]))
                    folds.append(world["noun"])
            if index_list:
                indices = np.array(index_list); label_array = np.array(labels); fold_array = np.array(folds)
                probe = {}
                for position, fraction in enumerate(fractions):
                    features = states[indices, position, :].astype(np.float32)
                    probe[f"{fraction:g}"] = auc(label_array, held_out_scores(features, label_array, fold_array))
                entry["probe_auc_by_depth"] = probe
                gate = [f"{value:g}" for value in config["gate_depth_fractions"]]
                entry["probe_auc"] = max(probe[f] for f in gate)
            cell_results[f"{axis}|m{n_mod}|c{n_cand}"] = entry
        models.append({"model": metadata["model_checkpoint"], "cells": cell_results})
    result = {"contract": "under task load, use of the restriction role degrades faster than its representation",
              "models": models}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(args.output)}))


if __name__ == "__main__":
    main()
