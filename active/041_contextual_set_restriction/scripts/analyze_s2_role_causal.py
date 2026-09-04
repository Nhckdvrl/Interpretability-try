"""Analyze the causal specificity of the restriction-role direction."""

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


def effect_units(rows: list[dict], depth: str, kind: str, probe: str,
                 on_restricting: bool) -> dict[str, float]:
    grouped = defaultdict(list)
    for row in rows:
        if row["probe"] != probe:
            continue
        for slot in ["dim1", "dim2"]:
            if (slot == row["restricting_dimension"]) != on_restricting:
                continue
            edited = row["edited_by_depth"][depth][f"{kind}_{slot}"]
            grouped[row["world_id"]].append(margin(edited, row) - margin(row["clean_scores"], row))
    return {key: float(np.mean(values)) for key, values in grouped.items()}


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
        depths = {}
        positive = 0
        for depth in metadata["depths"]:
            entry = {}
            for kind in ["role", "random"]:
                on = effect_units(rows, depth, kind, "reference", True)
                off = effect_units(rows, depth, kind, "reference", False)
                shared = sorted(set(on) & set(off))
                entry[f"{kind}_effect_on_restricting"] = cluster_bootstrap(on, seed, n_boot)
                entry[f"{kind}_effect_on_non_restricting"] = cluster_bootstrap(off, seed + 1, n_boot)
                entry[f"{kind}_interaction"] = cluster_bootstrap(
                    {key: on[key] - off[key] for key in shared}, seed + 2, n_boot)
            role_on = effect_units(rows, depth, "role", "reference", True)
            random_on = effect_units(rows, depth, "role", "reference", False)
            role_random_on = effect_units(rows, depth, "random", "reference", True)
            random_random_on = effect_units(rows, depth, "random", "reference", False)
            shared = sorted(set(role_on) & set(random_on) & set(role_random_on) & set(random_random_on))
            entry["role_minus_random_interaction"] = cluster_bootstrap(
                {key: (role_on[key] - random_on[key]) - (role_random_on[key] - random_random_on[key])
                 for key in shared}, seed + 3, n_boot)
            property_rows = [row for row in rows if row["probe"] == "property_truth"]
            clean_accuracy = float(np.mean([margin(row["clean_scores"], row) > 0 for row in property_rows]))
            edited_accuracy = float(np.mean([
                margin(row["edited_by_depth"][depth][f"role_{row['restricting_dimension']}"], row) > 0
                for row in property_rows]))
            reference_rows = [row for row in rows if row["probe"] == "reference"]
            reference_clean = float(np.mean([margin(row["clean_scores"], row) > 0 for row in reference_rows]))
            reference_edited = float(np.mean([
                margin(row["edited_by_depth"][depth][f"role_{row['restricting_dimension']}"], row) > 0
                for row in reference_rows]))
            entry["property_truth_accuracy"] = {"clean": clean_accuracy, "edited": edited_accuracy,
                                                "drop": clean_accuracy - edited_accuracy}
            entry["reference_accuracy"] = {"clean": reference_clean, "edited": reference_edited,
                                           "drop": reference_clean - reference_edited}
            depth_pass = bool(
                entry["role_minus_random_interaction"]["ci95"][1] < 0
                and abs(entry["role_minus_random_interaction"]["estimate"])
                >= config["gate"]["min_role_minus_control_effect"]
                and entry["property_truth_accuracy"]["drop"] <= config["gate"]["max_property_truth_drop"])
            entry["depth_pass"] = depth_pass
            positive += int(depth_pass)
            depths[depth] = entry
        models.append({
            "model": metadata["model_checkpoint"], "model_revision": metadata["model_revision"],
            "train_families": metadata["train_families"], "test_families": metadata["test_families"],
            "depths": depths, "positive_depths": positive,
            "causal_pass": bool(positive >= 2),
        })
    result = {
        "contract": ("attenuating the restriction-role component costs referent margin specifically when that "
                     "modifier is the one restricting the live set, while raw property truth survives"),
        "models": models,
        "panel_pass": bool(sum(model["causal_pass"] for model in models) >= config["gate"]["min_models_passing"]),
        "interpretation_guard": (
            "The direction is estimated on training property families only and applied to held-out families. "
            "A pass needs the role edit to beat a matched-norm random edit on the same token, and needs the "
            "property-truth denominator to survive the same edit."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "panel_pass": result["panel_pass"]}))


if __name__ == "__main__":
    main()
