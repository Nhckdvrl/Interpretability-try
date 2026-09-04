"""Behavioural and decoding analysis separating modifier restriction from description uniqueness."""

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
            "n_clusters": len(keys)}


def omission_units(rows: list[dict], uniqueness: str, restricting: bool) -> dict[str, float]:
    margins = defaultdict(list)
    for row in rows:
        if row["uniqueness"] != uniqueness:
            continue
        margins[(row["world_id"], row["description_condition"])].append(row["referent_margin"])
    means = {key: float(np.mean(values)) for key, values in margins.items()}
    units = {}
    for world in sorted({row["world_id"] for row in rows if row["uniqueness"] == uniqueness}):
        restricting_dimension = next(row["restricting_dimension"] for row in rows
                                     if row["world_id"] == world)
        dropped = restricting_dimension if restricting else (
            "dim2" if restricting_dimension == "dim1" else "dim1")
        key_full, key_drop = (world, "full"), (world, f"drop_{dropped}")
        if key_full in means and key_drop in means:
            units[world] = means[key_full] - means[key_drop]
    return units


def auc(labels: np.ndarray, scores: np.ndarray) -> float:
    """Threshold-free, so a mean shift between world types cannot masquerade as a transfer failure."""
    positive, negative = scores[labels == 1], scores[labels == 0]
    if not len(positive) or not len(negative):
        return float("nan")
    comparisons = (positive[:, None] > negative[None, :]).astype(float)
    comparisons += 0.5 * (positive[:, None] == negative[None, :])
    return float(comparisons.mean())


def balanced_accuracy(labels: np.ndarray, scores: np.ndarray) -> float:
    predicted = (scores > 0).astype(int)
    return float(np.mean([float((predicted[labels == value] == value).mean())
                          for value in [0, 1] if (labels == value).sum()]))


def mass_mean_direction(features: np.ndarray, labels: np.ndarray) -> tuple[np.ndarray, float]:
    positive, negative = features[labels == 1].mean(0), features[labels == 0].mean(0)
    direction = positive - negative
    norm = np.linalg.norm(direction)
    if norm < 1e-9:
        return np.zeros_like(direction), 0.0
    direction = direction / norm
    return direction, float((positive + negative) @ direction / 2)


def held_out_scores(features: np.ndarray, labels: np.ndarray, folds: np.ndarray,
                    train_mask: np.ndarray | None = None) -> np.ndarray:
    scores = np.zeros(len(labels))
    source = np.ones(len(labels), dtype=bool) if train_mask is None else train_mask
    for fold in np.unique(folds):
        test = folds == fold
        train = (~test) & source
        if len(np.unique(labels[train])) < 2:
            continue
        centre, scale = features[train].mean(0), features[train].std(0) + 1e-6
        direction, midpoint = mass_mean_direction((features[train] - centre) / scale, labels[train])
        scores[test] = ((features[test] - centre) / scale) @ direction - midpoint
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

        behaviour = {"cells": {}, "contrasts": {}}
        for uniqueness in ["unique", "duplicate"]:
            for condition in ["full", "drop_dim1", "drop_dim2"]:
                subset = [row for row in rows if row["uniqueness"] == uniqueness
                          and row["description_condition"] == condition]
                behaviour["cells"][f"{uniqueness}/{condition}"] = {
                    "n": len(subset),
                    "accuracy": float(np.mean([row["correct"] for row in subset])),
                    "mean_margin": float(np.mean([row["referent_margin"] for row in subset])),
                }
            for restricting in [True, False]:
                subset = [row for row in rows if row["uniqueness"] == uniqueness
                          and row["dropped_modifier_is_restricting"] is restricting]
                behaviour["cells"][f"{uniqueness}/dropped_{'restricting' if restricting else 'other'}"] = {
                    "n": len(subset),
                    "accuracy": float(np.mean([row["correct"] for row in subset])),
                    "mean_margin": float(np.mean([row["referent_margin"] for row in subset])),
                }
        for uniqueness in ["unique", "duplicate"]:
            restrict_units = omission_units(rows, uniqueness, True)
            other_units = omission_units(rows, uniqueness, False)
            shared = sorted(set(restrict_units) & set(other_units))
            behaviour["contrasts"][f"{uniqueness}/restricting_minus_other_omission_cost"] = cluster_bootstrap(
                {key: restrict_units[key] - other_units[key] for key in shared}, seed, n_boot)

        bundle = np.load(path.with_name(metadata["states_file"]))
        states = bundle["states"]
        keys = {str(value): index for index, value in enumerate(bundle["state_keys"])}
        entries = []
        for row in rows:
            if row["description_condition"] != "full" or row["mapping_index"] != 0:
                continue
            for slot in ["dim1", "dim2"]:
                key = f"{row['state_key']}|{slot}"
                if key in keys:
                    entries.append({"index": keys[key], "family": row["family"],
                                    "surface_form": row["surface_form"],
                                    "restricting": int(slot == row["restricting_dimension"]),
                                    "duplicate": int(row["uniqueness"] == "duplicate")})
        indices = np.array([entry["index"] for entry in entries])
        families = np.array([entry["family"] for entry in entries])
        restricting = np.array([entry["restricting"] for entry in entries])
        duplicate = np.array([entry["duplicate"] for entry in entries])
        probes = {}
        for layer_position, (layer, fraction) in enumerate(zip([int(v) for v in bundle["residual_layers"]],
                                                               config["depth_fractions"])):
            features = states[indices, layer_position, :].astype(np.float32)
            restriction_scores = held_out_scores(features, restricting, families)
            uniqueness_scores = held_out_scores(features, duplicate, families)
            train_unique = duplicate == 0
            train_duplicate = duplicate == 1
            cross = held_out_scores(features, restricting, families, train_mask=train_unique)
            cross_back = held_out_scores(features, restricting, families, train_mask=train_duplicate)
            centre, scale = features.mean(0), features.std(0) + 1e-6
            normalised = (features - centre) / scale
            restriction_direction, _ = mass_mean_direction(normalised, restricting)
            uniqueness_direction, _ = mass_mean_direction(normalised, duplicate)
            probes[f"{fraction:g}"] = {
                "residual_layer": layer,
                "restriction_balanced_accuracy": balanced_accuracy(restricting, restriction_scores),
                "restriction_auc": auc(restricting, restriction_scores),
                "uniqueness_balanced_accuracy": balanced_accuracy(duplicate, uniqueness_scores),
                "restriction_auc_within_unique": auc(restricting[train_unique], restriction_scores[train_unique]),
                "restriction_auc_within_duplicate": auc(restricting[train_duplicate], restriction_scores[train_duplicate]),
                "restriction_from_unique_worlds_tested_on_duplicate": balanced_accuracy(
                    restricting[train_duplicate], cross[train_duplicate]),
                "restriction_from_unique_worlds_tested_on_duplicate_auc": auc(
                    restricting[train_duplicate], cross[train_duplicate]),
                "restriction_from_duplicate_worlds_tested_on_unique": balanced_accuracy(
                    restricting[train_unique], cross_back[train_unique]),
                "restriction_from_duplicate_worlds_tested_on_unique_auc": auc(
                    restricting[train_unique], cross_back[train_unique]),
                "restriction_accuracy_using_uniqueness_direction": balanced_accuracy(
                    restricting, normalised @ uniqueness_direction - float(np.median(normalised @ uniqueness_direction))),
                "direction_cosine": float(restriction_direction @ uniqueness_direction),
            }
        gate_fractions = [f"{value:g}" for value in config["gate_depth_fractions"]]
        best = max(probes[fraction]["restriction_balanced_accuracy"] for fraction in gate_fractions)
        cross_best = max(min(probes[fraction]["restriction_from_unique_worlds_tested_on_duplicate_auc"],
                             probes[fraction]["restriction_from_duplicate_worlds_tested_on_unique_auc"])
                         for fraction in gate_fractions)
        confound = max(probes[fraction]["restriction_accuracy_using_uniqueness_direction"]
                       for fraction in gate_fractions)
        models.append({
            "model": metadata["model_checkpoint"], "model_revision": metadata["model_revision"],
            "n_probe_examples": len(entries), "behaviour": behaviour, "probes": probes,
            "gate_summary": {"best_restriction_accuracy": best,
                             "worst_cross_uniqueness_transfer_auc": cross_best,
                             "restriction_accuracy_from_uniqueness_direction": confound},
            "probe_pass": bool(best >= config["gate"]["min_restriction_probe_accuracy"]
                               and cross_best >= config["gate"]["min_restriction_probe_accuracy"]
                               and confound <= config["gate"]["max_uniqueness_confound_share"]),
        })
    result = {
        "contract": ("modifier restriction is represented at the modifier token independently of whether the "
                     "description still picks out a unique referent"),
        "models": models,
        "panel_pass": bool(sum(model["probe_pass"] for model in models) >= config["gate"]["min_models_passing"]),
        "interpretation_guard": (
            "Restriction and uniqueness are orthogonal by construction here. A restriction direction that "
            "transfers across uniqueness levels, while the uniqueness direction fails to classify restriction, "
            "is what separates a modifier-role state from a generic ambiguity signal."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "panel_pass": result["panel_pass"]}))


if __name__ == "__main__":
    main()
