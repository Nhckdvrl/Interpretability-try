"""Analyze the referential/attributive misdescription crossover and its raw-fact denominators."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

CONTEXTS = ["referential", "attributive_bare", "attributive_matched"]


def cluster_bootstrap(units: dict[str, float], seed: int, n_boot: int) -> dict:
    keys = sorted(units)
    values = np.array([units[key] for key in keys])
    rng = np.random.default_rng(seed)
    draws = [float(values[rng.integers(0, len(keys), len(keys))].mean()) for _ in range(n_boot)]
    return {"estimate": float(values.mean()), "ci95": [float(v) for v in np.quantile(draws, [0.025, 0.975])],
            "n_clusters": len(keys)}


def target_margin(row: dict) -> float:
    return row["label_scores"][row["target_option"]] - row["label_scores"][row["satisfier_option"]]


def by_item(rows: list[dict], select) -> dict[str, float]:
    grouped = defaultdict(list)
    for row in rows:
        if select(row):
            grouped[row["item"]].append(target_margin(row))
    return {key: float(np.mean(values)) for key, values in grouped.items()}


def contrast(left: dict[str, float], right: dict[str, float], seed: int, n_boot: int) -> dict:
    shared = sorted(set(left) & set(right))
    return cluster_bootstrap({key: left[key] - right[key] for key in shared}, seed, n_boot)


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

        denominators = {}
        for probe in ["description_truth", "speaker_target_fact", "entity_fact"]:
            subset = [row for row in rows if row["probe"] == probe]
            denominators[probe] = {"n": len(subset),
                                   "accuracy": float(np.mean([row["correct"] for row in subset]))}

        readouts = {}
        for probe_name in ["use_mode", "downstream_action"]:
            readouts[probe_name] = [row for row in rows if row["probe"] == probe_name]
        use_rows = readouts["use_mode"]
        cells = {}
        for context in CONTEXTS:
            subset = [row for row in use_rows if row["context"] == context]
            cells[context] = {
                "n": len(subset),
                "accuracy": float(np.mean([row["correct"] for row in subset])),
                "mean_target_vs_satisfier_margin": float(np.mean([target_margin(row) for row in subset])),
                "share_choosing_speaker_target": float(np.mean([target_margin(row) > 0 for row in subset])),
            }

        def cell(context, extra=lambda row: True):
            return by_item(use_rows, lambda row: row["context"] == context and extra(row))

        crossovers = {
            "referential_minus_attributive_matched": contrast(cell("referential"),
                                                              cell("attributive_matched"), seed, n_boot),
            "referential_minus_attributive_bare": contrast(cell("referential"),
                                                           cell("attributive_bare"), seed + 1, n_boot),
        }
        by_establishment = {
            name: contrast(cell("referential", lambda r, n=name: r["establishment"] == n),
                           cell("attributive_matched", lambda r, n=name: r["establishment"] == n),
                           seed + 2, n_boot)
            for name in sorted({row["establishment"] for row in use_rows})
        }
        by_description_family = {
            name: contrast(cell("referential", lambda r, n=name: r["description_family"] == n),
                           cell("attributive_matched", lambda r, n=name: r["description_family"] == n),
                           seed + 3, n_boot)
            for name in sorted({row["description_family"] for row in use_rows})
        }
        by_mapping = {
            str(index): contrast(cell("referential", lambda r, m=index: r["mapping_index"] == m),
                                 cell("attributive_matched", lambda r, m=index: r["mapping_index"] == m),
                                 seed + 4, n_boot)
            for index in sorted({row["mapping_index"] for row in use_rows})
        }

        action_cells = {}
        for context in CONTEXTS:
            subset = [row for row in readouts["downstream_action"] if row["context"] == context]
            action_cells[context] = {
                "n": len(subset),
                "accuracy": float(np.mean([row["correct"] for row in subset])),
                "mean_target_vs_satisfier_margin": float(np.mean([target_margin(row) for row in subset])),
                "share_choosing_speaker_target": float(np.mean([target_margin(row) > 0 for row in subset])),
            }

        def action_cell(context):
            return by_item(readouts["downstream_action"], lambda row: row["context"] == context)
        action_crossover = contrast(action_cell("referential"), action_cell("attributive_matched"),
                                    seed + 5, n_boot)
        denominator_pass = all(entry["accuracy"] >= 0.80 for entry in denominators.values())
        crossover_pass = (crossovers["referential_minus_attributive_matched"]["ci95"][0] > 0
                          and cells["referential"]["mean_target_vs_satisfier_margin"] > 0
                          and cells["attributive_matched"]["mean_target_vs_satisfier_margin"] < 0)
        control_pass = all(entry["ci95"][0] > 0 for group in [by_establishment, by_description_family, by_mapping]
                           for entry in group.values())
        models.append({
            "model": metadata["model_checkpoint"], "model_revision": metadata["model_revision"],
            "raw_fact_denominators": denominators, "use_mode_cells": cells,
            "downstream_action_cells": action_cells,
            "downstream_action_crossover": action_crossover,
            "crossovers": crossovers, "by_establishment": by_establishment,
            "by_description_family": by_description_family, "by_answer_mapping": by_mapping,
            "denominator_pass": bool(denominator_pass), "crossover_pass": bool(crossover_pass),
            "control_pass": bool(control_pass),
            "s0_pass": bool(denominator_pass and crossover_pass and control_pass),
        })
    result = {
        "contract": ("the same definite description follows the speaker's established target under referential "
                     "use and the descriptive satisfier under attributive use, with salience matched"),
        "models": models,
        "panel_pass": bool(sum(model["s0_pass"] for model in models) >= config["gate"]["min_models_passing"]),
        "interpretation_guard": (
            "The referential-minus-attributive_matched contrast is the only one that controls the speaker "
            "target's salience, mention count and recency. A pass on the bare contrast alone does not "
            "establish a use-mode effect."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "panel_pass": result["panel_pass"]}))


if __name__ == "__main__":
    main()
