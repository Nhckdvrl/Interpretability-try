"""Analyze the S0 role swap: does omitting a modifier cost only when that modifier restricts?"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

CONDITIONS = ["full", "drop_dim1", "drop_dim2", "bare"]


def cluster_bootstrap(units: dict[str, float], seed: int, n_boot: int) -> dict:
    keys = sorted(units)
    values = np.array([units[key] for key in keys])
    rng = np.random.default_rng(seed)
    draws = [float(values[rng.integers(0, len(keys), len(keys))].mean()) for _ in range(n_boot)]
    return {"estimate": float(values.mean()), "ci95": [float(v) for v in np.quantile(draws, [0.025, 0.975])],
            "n_clusters": len(keys)}


def cell_means(rows: list[dict], key) -> dict:
    grouped = defaultdict(list)
    for row in rows:
        grouped[key(row)].append(row["referent_margin"])
    return {name: float(np.mean(values)) for name, values in grouped.items()}


def swap_units(rows: list[dict], restrict_to=None) -> dict[str, float]:
    """Same world, same lexical modifier: cost when it restricts minus cost when it does not."""
    selected = [row for row in rows if restrict_to is None or restrict_to(row)]
    margins = cell_means(selected, lambda row: (row["world_id"], row["context"],
                                                row["description_condition"]))
    units = {}
    for world in sorted({row["world_id"] for row in selected}):
        try:
            cost = {(context, condition): margins[(world, context, "full")] - margins[(world, context, condition)]
                    for context in ["AB", "AC"] for condition in ["drop_dim1", "drop_dim2"]}
        except KeyError:
            continue
        # dim1 restricts only in AC; dim2 restricts only in AB
        units[f"{world}|dim1"] = cost[("AC", "drop_dim1")] - cost[("AB", "drop_dim1")]
        units[f"{world}|dim2"] = cost[("AB", "drop_dim2")] - cost[("AC", "drop_dim2")]
    return units


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

        accuracy = {}
        for condition in CONDITIONS:
            subset = [row for row in rows if row["description_condition"] == condition]
            accuracy[condition] = {
                "n": len(subset),
                "accuracy": float(np.mean([row["correct"] for row in subset])),
                "mean_margin": float(np.mean([row["referent_margin"] for row in subset])),
            }
        for condition in ["drop_dim1", "drop_dim2"]:
            for restricting in [True, False]:
                subset = [row for row in rows if row["description_condition"] == condition
                          and row["dropped_modifier_is_restricting"] is restricting]
                accuracy[f"{condition}/{'restricting' if restricting else 'non_restricting'}"] = {
                    "n": len(subset),
                    "accuracy": float(np.mean([row["correct"] for row in subset])),
                    "mean_margin": float(np.mean([row["referent_margin"] for row in subset])),
                }

        overall = cluster_bootstrap(swap_units(rows), seed, n_boot)
        by_family = {family: cluster_bootstrap(swap_units(rows, lambda r, f=family: r["family"] == f),
                                               seed + 1, n_boot)
                     for family in sorted({row["family"] for row in rows})}
        by_surface = {surface: cluster_bootstrap(swap_units(rows, lambda r, s=surface: r["surface_form"] == s),
                                                 seed + 2, n_boot)
                      for surface in sorted({row["surface_form"] for row in rows})}
        by_question = {str(form): cluster_bootstrap(swap_units(rows, lambda r, q=form: r["question_form"] == q),
                                                    seed + 3, n_boot)
                       for form in sorted({row["question_form"] for row in rows})}
        by_mapping = {str(index): cluster_bootstrap(swap_units(rows, lambda r, m=index: r["mapping_index"] == m),
                                                    seed + 4, n_boot)
                      for index in sorted({row["mapping_index"] for row in rows})}

        capability_pass = (accuracy["full"]["accuracy"] >= config["gate"]["min_full_description_accuracy"]
                           and accuracy["bare"]["accuracy"] <= config["gate"]["max_bare_description_accuracy"])
        swap_pass = (overall["ci95"][0] > 0
                     and overall["estimate"] >= config["gate"]["min_omission_cost_interaction"])
        control_pass = all(entry["estimate"] > 0 for group in [by_surface, by_question, by_mapping]
                           for entry in group.values())
        models.append({
            "model": metadata["model_checkpoint"], "model_revision": metadata["model_revision"],
            "accuracy_by_condition": accuracy,
            "role_swap_interaction": overall,
            "role_swap_by_family": by_family, "role_swap_by_surface_form": by_surface,
            "role_swap_by_question_form": by_question, "role_swap_by_answer_mapping": by_mapping,
            "capability_pass": bool(capability_pass), "swap_pass": bool(swap_pass),
            "surface_control_pass": bool(control_pass),
            "s0_pass": bool(capability_pass and swap_pass and control_pass),
        })
    result = {
        "contract": "the same lexical modifier costs more to omit exactly when it restricts the live candidate set",
        "models": models,
        "panel_pass": bool(sum(model["s0_pass"] for model in models) >= config["gate"]["min_models_passing"]),
        "interpretation_guard": (
            "A pass means the omission cost tracks contextual set restriction with world facts, target "
            "phrase and lexical modifier held fixed. It does not by itself show an abstract role state; "
            "that is the causal contract in section H."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "panel_pass": result["panel_pass"]}))


if __name__ == "__main__":
    main()
