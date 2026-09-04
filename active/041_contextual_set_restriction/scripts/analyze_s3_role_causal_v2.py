"""Analyze causal test v2: scaled counterfactual replacement with shuffled and random controls."""

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


def margin(scores: dict[str, float], row: dict) -> float:
    return scores[row["gold_option"]] - scores[row["other_option"]]


def units(rows, depth, name_for, on_restricting, probe, select=lambda row: True):
    grouped = defaultdict(list)
    for row in rows:
        if row["probe"] != probe or not select(row):
            continue
        for slot in ["dim1", "dim2"]:
            if (slot == row["restricting_dimension"]) != on_restricting:
                continue
            edited = row["edited_by_depth"][depth][name_for(slot)]
            grouped[f"{row['world_id']}|{row['surface_form']}"].append(
                margin(edited, row) - margin(row["clean_scores"], row))
    return {key: float(np.mean(values)) for key, values in grouped.items()}


def interaction(rows, depth, kind, target_role, alpha, probe, seed, n_boot, select=lambda row: True):
    def name_for(slot):
        return f"{kind}|{target_role}|{slot}|a{alpha:g}"
    on = units(rows, depth, name_for, True, probe, select)
    off = units(rows, depth, name_for, False, probe, select)
    shared = sorted(set(on) & set(off))
    return {
        "on_restricting": cluster_bootstrap(on, seed, n_boot),
        "on_non_restricting": cluster_bootstrap(off, seed + 1, n_boot),
        "interaction": cluster_bootstrap({key: on[key] - off[key] for key in shared}, seed + 2, n_boot),
    }


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
        alphas = list(metadata["alphas"])
        depths = {}
        positive = 0
        for depth in metadata["depths"]:
            entry = {"alphas": {}}
            for alpha in alphas:
                per_alpha = {}
                for kind in ["role", "shuffled", "random"]:
                    per_alpha[kind] = interaction(rows, depth, kind, "to_non_restricting", alpha,
                                                  "reference", seed, n_boot)
                role = per_alpha["role"]["interaction"]
                best_control = max(per_alpha["shuffled"]["interaction"]["estimate"],
                                   per_alpha["random"]["interaction"]["estimate"])
                worst_control = min(per_alpha["shuffled"]["interaction"]["estimate"],
                                    per_alpha["random"]["interaction"]["estimate"])
                reference_rows = [row for row in rows if row["probe"] == "reference"]
                property_rows = [row for row in rows if row["probe"] == "property_truth"]

                def accuracy(subset, edited=True):
                    if not edited:
                        return float(np.mean([margin(row["clean_scores"], row) > 0 for row in subset]))
                    return float(np.mean([
                        margin(row["edited_by_depth"][depth][
                            f"role|to_non_restricting|{row['restricting_dimension']}|a{alpha:g}"], row) > 0
                        for row in subset]))
                per_alpha["reference_accuracy"] = {"clean": accuracy(reference_rows, False),
                                                   "edited": accuracy(reference_rows)}
                per_alpha["property_truth_accuracy"] = {"clean": accuracy(property_rows, False),
                                                        "edited": accuracy(property_rows)}
                per_alpha["property_truth_drop"] = (per_alpha["property_truth_accuracy"]["clean"]
                                                    - per_alpha["property_truth_accuracy"]["edited"])
                per_alpha["reference_accuracy_drop"] = (per_alpha["reference_accuracy"]["clean"]
                                                        - per_alpha["reference_accuracy"]["edited"])
                per_alpha["by_surface_form"] = {
                    surface: interaction(rows, depth, "role", "to_non_restricting", alpha, "reference",
                                         seed + 10, n_boot,
                                         select=lambda row, s=surface: row["surface_form"] == s)["interaction"]
                    for surface in sorted({row["surface_form"] for row in rows})}
                per_alpha["reverse_direction"] = interaction(rows, depth, "role", "to_restricting", alpha,
                                                             "reference", seed + 20, n_boot)["interaction"]
                per_alpha["role_beats_controls"] = bool(role["ci95"][1] < 0 and role["estimate"] < worst_control
                                                        and abs(role["estimate"] - best_control)
                                                        >= config["gate"]["min_role_minus_control_effect"])
                per_alpha["property_preserved"] = bool(
                    per_alpha["property_truth_drop"] <= config["gate"]["max_property_truth_drop"])
                per_alpha["cross_surface_consistent"] = bool(
                    all(value["ci95"][1] < 0 for value in per_alpha["by_surface_form"].values()))
                entry["alphas"][f"{alpha:g}"] = per_alpha
            entry["depth_pass"] = bool(any(
                value["role_beats_controls"] and value["property_preserved"]
                and value["cross_surface_consistent"] for value in entry["alphas"].values()))
            positive += int(entry["depth_pass"])
            depths[depth] = entry
        models.append({
            "model": metadata["model_checkpoint"], "model_revision": metadata["model_revision"],
            "train_families": metadata["train_families"], "test_families": metadata["test_families"],
            "depths": depths, "positive_depths": positive, "causal_pass": bool(positive >= 1),
        })
    result = {
        "contract": ("replacing the restriction-role component at a modifier token with its non-restricting "
                     "counterfactual value costs referent margin specifically for the restricting modifier, "
                     "beyond shuffled-label and random directions, on a held-out surface form, while raw "
                     "property truth survives"),
        "models": models,
        "panel_pass": bool(sum(model["causal_pass"] for model in models) >= config["gate"]["min_models_passing"]),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "panel_pass": result["panel_pass"]}))


if __name__ == "__main__":
    main()
