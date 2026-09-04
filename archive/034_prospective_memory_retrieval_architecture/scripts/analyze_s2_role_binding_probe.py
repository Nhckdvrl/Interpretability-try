"""Analyze the cue-role binding probe: behavioral crossover plus cue-token decodability."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

CONDITIONS = ["nonfocal", "focal_target", "focal_other"]
CUE_TYPES = ["target", "other", "none"]
SEMANTICS = ["TARGET_ACTION", "OTHER_ACTION", "YES", "NO"]
MATCHED = {"target": "focal_target", "other": "focal_other"}
MISMATCHED = {"target": "focal_other", "other": "focal_target"}


def cluster_bootstrap(units: dict[int, list[float]], seed: int, n_boot: int) -> dict:
    keys = sorted(units)
    observed = float(np.mean([value for key in keys for value in units[key]]))
    rng = np.random.default_rng(seed)
    draws = []
    for _ in range(n_boot):
        sample = rng.choice(keys, size=len(keys), replace=True)
        draws.append(float(np.mean([value for key in sample for value in units[key]])))
    return {"estimate": observed, "ci95": [float(value) for value in np.quantile(draws, [0.025, 0.975])]}


def behavior(rows: list[dict], seed: int, n_boot: int) -> dict:
    cells = {}
    for condition in CONDITIONS:
        for cue_type in CUE_TYPES:
            subset = [row for row in rows if row["focality"] == condition and row["cue_type"] == cue_type]
            counts = defaultdict(int)
            for row in subset:
                counts[row["predicted_semantic"]] += 1
            cells[f"{condition}/{cue_type}"] = {
                "n": len(subset),
                "accuracy": float(np.mean([row["predicted_semantic"] == row["correct_semantic"] for row in subset])),
                "misroute_to_other_intention": float(np.mean([
                    row["predicted_semantic"] == ("OTHER_ACTION" if cue_type == "target" else "TARGET_ACTION")
                    for row in subset])) if cue_type != "none" else None,
                "prediction_counts": dict(sorted(counts.items())),
            }

    def per_pair(condition: str, cue_type: str) -> dict[int, list[float]]:
        units = defaultdict(list)
        for row in rows:
            if row["focality"] == condition and row["cue_type"] == cue_type:
                units[row["pair_index"]].append(float(row["predicted_semantic"] == row["correct_semantic"]))
        return units

    def contrast(left: dict[int, list[float]], right: dict[int, list[float]], seed_offset: int) -> dict:
        units = {key: [np.mean(left[key]) - np.mean(right[key])] for key in sorted(left)}
        return cluster_bootstrap(units, seed + seed_offset, n_boot)

    matched_gain = {
        cue_type: contrast(per_pair(MATCHED[cue_type], cue_type), per_pair("nonfocal", cue_type), index)
        for index, cue_type in enumerate(["target", "other"])
    }
    mismatched_gain = {
        cue_type: contrast(per_pair(MISMATCHED[cue_type], cue_type), per_pair("nonfocal", cue_type), 10 + index)
        for index, cue_type in enumerate(["target", "other"])
    }
    crossover_units = {}
    for key in sorted(per_pair("focal_target", "target")):
        target_effect = (np.mean(per_pair("focal_target", "target")[key])
                         - np.mean(per_pair("focal_other", "target")[key]))
        other_effect = (np.mean(per_pair("focal_target", "other")[key])
                        - np.mean(per_pair("focal_other", "other")[key]))
        crossover_units[key] = [float(target_effect - other_effect)]
    return {
        "cells": cells,
        "matched_focal_minus_nonfocal": matched_gain,
        "mismatched_focal_minus_nonfocal": mismatched_gain,
        "monitoring_crossover": cluster_bootstrap(crossover_units, seed + 20, n_boot),
    }


def mass_mean_scores(train_x: np.ndarray, train_y: np.ndarray, test_x: np.ndarray) -> np.ndarray:
    positive = train_x[train_y == 1].mean(0)
    negative = train_x[train_y == 0].mean(0)
    direction = positive - negative
    norm = np.linalg.norm(direction)
    if norm < 1e-9:
        return np.zeros(len(test_x))
    direction = direction / norm
    midpoint = float((positive + negative) @ direction / 2)
    return test_x @ direction - midpoint


def logistic_scores(train_x: np.ndarray, train_y: np.ndarray, test_x: np.ndarray, seed: int) -> np.ndarray:
    """Ridge-regularised readout on a randomised PCA basis; a secondary check on the mass-mean probe."""
    components = min(32, train_x.shape[0] - 1, train_x.shape[1])
    reducer = PCA(n_components=components, svd_solver="randomized", random_state=seed).fit(train_x)
    model = LogisticRegression(max_iter=200, C=1.0, class_weight="balanced", random_state=seed)
    model.fit(reducer.transform(train_x), train_y)
    return model.decision_function(reducer.transform(test_x))


def balanced_accuracy(labels: np.ndarray, scores: np.ndarray) -> float:
    predicted = (scores > 0).astype(int)
    values = []
    for value in [0, 1]:
        mask = labels == value
        if mask.sum():
            values.append(float((predicted[mask] == value).mean()))
    return float(np.mean(values))


def auc(labels: np.ndarray, scores: np.ndarray) -> float:
    positive, negative = scores[labels == 1], scores[labels == 0]
    if not len(positive) or not len(negative):
        return float("nan")
    comparisons = (positive[:, None] > negative[None, :]).astype(float)
    comparisons += 0.5 * (positive[:, None] == negative[None, :])
    return float(comparisons.mean())


def held_out_probe(features: np.ndarray, labels: np.ndarray, pairs: np.ndarray, seed: int,
                   train_mask: np.ndarray | None = None, with_logistic: bool = True) -> dict:
    scores_mm = np.zeros(len(labels))
    scores_lr = np.zeros(len(labels))
    source = np.ones(len(labels), dtype=bool) if train_mask is None else train_mask
    for pair in np.unique(pairs):
        test = pairs == pair
        train = (~test) & source
        if len(np.unique(labels[train])) < 2:
            continue
        centre = features[train].mean(0)
        scale = features[train].std(0) + 1e-6
        train_x = (features[train] - centre) / scale
        test_x = (features[test] - centre) / scale
        scores_mm[test] = mass_mean_scores(train_x, labels[train], test_x)
        if with_logistic:
            scores_lr[test] = logistic_scores(train_x, labels[train], test_x, seed)
    return {
        "mass_mean": {"balanced_accuracy": balanced_accuracy(labels, scores_mm), "auc": auc(labels, scores_mm)},
        "logistic_pca": ({"balanced_accuracy": balanced_accuracy(labels, scores_lr), "auc": auc(labels, scores_lr)}
                         if with_logistic else None),
        "mass_mean_scores": scores_mm.tolist(),
    }


def probes(states: np.ndarray, state_rows: list[dict], layers: list[int], fractions: list[float],
           seed: int, gate_fractions: list[float]) -> dict:
    pairs = np.array([row["pair_index"] for row in state_rows])
    result = {}
    for layer_index, (layer, fraction) in enumerate(zip(layers, fractions)):
        features_all = states[:, layer_index, :].astype(np.float32)
        entry = {"residual_layer": layer, "depth_fraction": fraction, "conditions": {}}
        for condition in CONDITIONS:
            in_condition = np.array([row["focality"] == condition for row in state_rows])
            cue_mask = in_condition & np.array([row["cue_type"] != "none" for row in state_rows])
            role_labels = np.array([1 if row["cue_type"] == "target" else 0 for row in state_rows])
            secondary = fraction in gate_fractions
            role = held_out_probe(features_all[cue_mask], role_labels[cue_mask], pairs[cue_mask], seed,
                                  with_logistic=secondary)
            detect_labels = np.array([0 if row["cue_type"] == "none" else 1 for row in state_rows])
            detect = held_out_probe(features_all[in_condition], detect_labels[in_condition],
                                    pairs[in_condition], seed, with_logistic=secondary)
            entry["conditions"][condition] = {
                "n_role": int(cue_mask.sum()), "n_detect": int(in_condition.sum()),
                "role": {key: value for key, value in role.items() if key != "mass_mean_scores"},
                "detect": {key: value for key, value in detect.items() if key != "mass_mean_scores"},
                "role_scores": role["mass_mean_scores"],
                "role_index": np.where(cue_mask)[0].tolist(),
            }
        result[f"{fraction:g}"] = entry
    return result


def transfer(states: np.ndarray, state_rows: list[dict], layers: list[int], fractions: list[float],
             seed: int) -> dict:
    pairs = np.array([row["pair_index"] for row in state_rows])
    role_labels = np.array([1 if row["cue_type"] == "target" else 0 for row in state_rows])
    cue_mask = np.array([row["cue_type"] != "none" for row in state_rows])
    result = {}
    for layer_index, (layer, fraction) in enumerate(zip(layers, fractions)):
        features = states[:, layer_index, :].astype(np.float32)
        entry = {}
        for train_condition in ["focal_target", "focal_other"]:
            select = cue_mask
            source = np.array([row["focality"] == train_condition for row in state_rows])[select]
            probe = held_out_probe(features[select], role_labels[select], pairs[select], seed,
                                   train_mask=source, with_logistic=False)
            scores = np.array(probe["mass_mean_scores"])
            target_mask = np.array([row["focality"] == "nonfocal" for row in state_rows])[select]
            entry[f"train_{train_condition}_test_nonfocal"] = {
                "balanced_accuracy": balanced_accuracy(role_labels[select][target_mask], scores[target_mask]),
                "auc": auc(role_labels[select][target_mask], scores[target_mask]),
            }
        result[f"{fraction:g}"] = entry
    return result


def behavior_linked(states: np.ndarray, state_rows: list[dict], rows: list[dict], layers: list[int],
                    fractions: list[float], seed: int) -> dict:
    """Is the role still decodable on the very trials whose action is misrouted?"""
    outcome = defaultdict(list)
    for row in rows:
        if row["focality"] == "nonfocal" and row["cue_type"] == "other":
            outcome[row["state_row"]].append(row["predicted_semantic"] == "TARGET_ACTION")
    misrouted = {key for key, values in outcome.items() if all(values)}
    correct = {key for key, values in outcome.items() if not any(values)}
    pairs = np.array([row["pair_index"] for row in state_rows])
    role_labels = np.array([1 if row["cue_type"] == "target" else 0 for row in state_rows])
    cue_mask = np.array([row["cue_type"] != "none" for row in state_rows])
    result = {}
    for layer_index, (layer, fraction) in enumerate(zip(layers, fractions)):
        features = states[:, layer_index, :].astype(np.float32)
        select = cue_mask & np.array([row["focality"] == "nonfocal" for row in state_rows])
        probe = held_out_probe(features[select], role_labels[select], pairs[select], seed,
                               with_logistic=False)
        scores = np.array(probe["mass_mean_scores"])
        indices = np.where(select)[0]
        labels = role_labels[select]
        groups = {}
        for name, keys in [("misrouted", misrouted), ("correctly_routed", correct)]:
            mask = np.array([index in keys for index in indices]) & (labels == 0)
            groups[name] = {
                "n": int(mask.sum()),
                "role_correct_rate": float(((scores[mask] < 0)).mean()) if mask.sum() else None,
                "mean_score": float(scores[mask].mean()) if mask.sum() else None,
            }
        result[f"{fraction:g}"] = {"residual_layer": layer, "groups": groups,
                                   "overall_balanced_accuracy": probe["mass_mean"]["balanced_accuracy"]}
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    models = []
    for model_index, path in enumerate(args.inputs):
        lines = [json.loads(line) for line in path.read_text().splitlines() if line]
        metadata = next(row for row in lines if row["record_type"] == "metadata")
        rows = [row for row in lines if row["record_type"] == "example"]
        bundle = np.load(path.with_name(metadata["states_file"]))
        states = bundle["states"]
        by_state_row = {}
        for row in rows:
            by_state_row.setdefault(row["state_row"], row)
        state_rows = [by_state_row[index] for index in range(states.shape[0])]
        keys = list(bundle["state_keys"])
        if [row["state_key"] for row in state_rows] != [str(value) for value in keys]:
            raise ValueError("State ordering does not match the behavioral records")
        layers = [int(value) for value in bundle["residual_layers"]]
        fractions = list(config["depth_fractions"])
        seed = int(config["seed"]) + 100 * model_index
        probe_result = probes(states, state_rows, layers, fractions, seed,
                              [float(value) for value in config["gate_depth_fractions"]])
        gate_fractions = [f"{value:g}" for value in config["gate_depth_fractions"]]
        role_gap = {
            fraction: {
                "focal_target_minus_nonfocal":
                    probe_result[fraction]["conditions"]["focal_target"]["role"]["mass_mean"]["balanced_accuracy"]
                    - probe_result[fraction]["conditions"]["nonfocal"]["role"]["mass_mean"]["balanced_accuracy"],
                "focal_other_minus_nonfocal":
                    probe_result[fraction]["conditions"]["focal_other"]["role"]["mass_mean"]["balanced_accuracy"]
                    - probe_result[fraction]["conditions"]["nonfocal"]["role"]["mass_mean"]["balanced_accuracy"],
            } for fraction in gate_fractions
        }
        behavior_result = behavior(rows, seed, int(config["bootstrap_samples"]))
        models.append({
            "model": metadata["model_checkpoint"], "model_revision": metadata["model_revision"],
            "residual_layers": layers, "depth_fractions": fractions,
            "behavior": behavior_result,
            "probes": {fraction: {
                "residual_layer": value["residual_layer"],
                "conditions": {condition: {key: entry[key] for key in ["n_role", "n_detect", "role", "detect"]}
                               for condition, entry in value["conditions"].items()},
            } for fraction, value in probe_result.items()},
            "role_gap_at_gate_depths": role_gap,
            "role_transfer_to_nonfocal": transfer(states, state_rows, layers, fractions, seed),
            "role_decodability_by_routing_outcome": behavior_linked(states, state_rows, rows, layers,
                                                                    fractions, seed),
            "crossover_pass": bool(behavior_result["monitoring_crossover"]["ci95"][0]
                                   > config["gate"]["min_crossover_gap"]),
        })
    result = {
        "contract": "cue-to-intention routing follows the ongoing task's own category check",
        "models": models,
        "panel_gate_pass": bool(len(models) >= int(config["gate"]["min_crossover_models"])
                                and all(model["crossover_pass"] for model in models)),
        "interpretation_guard": (
            "A crossover pass means routing is controlled by the ongoing task's category check rather than by "
            "generic semantic depth. Probe results say whether the intention-role binding is absent at the cue "
            "token or present but unused downstream."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(args.output),
                      "panel_gate_pass": result["panel_gate_pass"]}, indent=2))


if __name__ == "__main__":
    main()
