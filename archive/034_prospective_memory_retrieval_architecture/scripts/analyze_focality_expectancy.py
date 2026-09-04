"""Aggregate label-counterbalanced 034 S0-2 results at semantic-item level."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


def paired_bootstrap(rows: list[dict], seed: int, n_boot: int = 5000) -> dict:
    """Bootstrap semantic items, preserving the full within-item factorial."""
    by_id = defaultdict(dict)
    for row in rows:
        by_id[row["semantic_id"]][(row["cue_present"], row["focality"], row["expectancy"])] = row
    ids = sorted(by_id)
    rng = np.random.default_rng(seed)

    def statistic(sampled: list[str]) -> tuple[float, float, float]:
        def mean_margin(focality: str, expectancy: str) -> float:
            return float(np.mean([
                by_id[item][(True, focality, expectancy)]["reminder_margin"] for item in sampled
            ]))
        expected = mean_margin("focal", "expected") - mean_margin("nonfocal", "expected")
        unexpected = mean_margin("focal", "unexpected") - mean_margin("nonfocal", "unexpected")
        return expected, unexpected, expected - unexpected

    observed = statistic(ids)
    draws = np.asarray([statistic(list(rng.choice(ids, size=len(ids), replace=True))) for _ in range(n_boot)])
    names = ["focality_expected", "focality_unexpected", "interaction"]
    return {
        name: {"estimate": float(observed[i]), "ci95": [float(x) for x in np.quantile(draws[:, i], [0.025, 0.975])]}
        for i, name in enumerate(names)
    }


def aggregate(rows: list[dict]) -> list[dict]:
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["semantic_id"], row["cue_present"], row["focality"], row["expectancy"])].append(row)
    result = []
    for key, values in grouped.items():
        if len(values) != 6:
            raise ValueError(f"Expected six label maps for {key}, got {len(values)}")
        semantic_scores = {name: [] for name in ["REMINDER", "YES", "NO"]}
        raw_semantic_predictions = []
        for row in values:
            inverse = {label: semantic for semantic, label in row["label_map"].items()}
            for semantic, label in row["label_map"].items():
                semantic_scores[semantic].append(row["scores"][label]["logprob"])
            raw_semantic_predictions.append(inverse[row["prediction"]])
        means = {k: float(np.mean(v)) for k, v in semantic_scores.items()}
        prediction = max(means, key=means.get)
        correct = values[0]["correct_semantic"]
        result.append({
            "semantic_id": key[0], "cue_present": key[1], "focality": key[2], "expectancy": key[3],
            "semantic_scores": means, "prediction": prediction, "correct_semantic": correct,
            "correct": prediction == correct,
            "reminder_margin": means["REMINDER"] - max(means["YES"], means["NO"]),
            "raw_label_map_stability": len(set(raw_semantic_predictions)) == 1,
        })
    return result


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--inputs", type=Path, nargs="+", required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    summaries = []
    for path in args.inputs:
        lines = [json.loads(x) for x in path.read_text().splitlines() if x]
        meta = next(x for x in lines if x["record_type"] == "metadata")
        rows = aggregate([x for x in lines if x["record_type"] == "example"])
        cells = {}
        for cue_present in [False, True]:
            for focality in ["focal", "nonfocal"]:
                for expectancy in ["expected", "unexpected"]:
                    selected = [x for x in rows if x["cue_present"] == cue_present and x["focality"] == focality and x["expectancy"] == expectancy]
                    cells[f"{'cue' if cue_present else 'no_cue'}/{focality}/{expectancy}"] = {
                        "n": len(selected), "accuracy": float(np.mean([x["correct"] for x in selected])),
                        "mean_reminder_margin": float(np.mean([x["reminder_margin"] for x in selected])),
                        "raw_label_map_stability": float(np.mean([x["raw_label_map_stability"] for x in selected])),
                    }
        cue_acc = lambda focality, expectancy: cells[f"cue/{focality}/{expectancy}"]["accuracy"]
        focality_effects = {e: cue_acc("focal", e) - cue_acc("nonfocal", e) for e in ["expected", "unexpected"]}
        expectancy_effects = {f: cue_acc(f, "expected") - cue_acc(f, "unexpected") for f in ["focal", "nonfocal"]}
        interaction = focality_effects["expected"] - focality_effects["unexpected"]
        margin_contrasts = paired_bootstrap(rows, int(config["seed"]))
        no_cue_ok = all(v["accuracy"] >= config["gate"]["min_no_cue_accuracy"] for k, v in cells.items() if k.startswith("no_cue/"))
        cue_values = [v["accuracy"] for k, v in cells.items() if k.startswith("cue/")]
        contrast_measurable = max(abs(x) for x in focality_effects.values()) >= config["gate"]["min_abs_focality_effect"]
        summaries.append({
            "model": meta["model_checkpoint"], "model_revision": meta["model_revision"], "n_semantic_cells": len(rows),
            "cells": cells, "focality_effects": focality_effects, "expectancy_effects": expectancy_effects,
            "focality_x_expectancy_interaction": interaction,
            "paired_reminder_margin_contrasts": margin_contrasts,
            "behavior_gate_pass": bool(no_cue_ok and min(cue_values) >= config["gate"]["min_cue_cell_accuracy"]
                                      and min(cue_values) < config["gate"]["all_cells_ceiling"] and contrast_measurable),
            "scope_note": "Behavioral interaction licenses but does not identify native monitoring or cue-time retrieval.",
        })
    effect_signs = [np.sign(max(x["focality_effects"].values(), key=abs)) for x in summaries]
    result = {
        "contract": "matched-cue focality x target-context-expectancy behavioral denominator",
        "models": summaries,
        "panel_gate_pass": bool(len(summaries) >= 2 and all(x["behavior_gate_pass"] for x in summaries)
                                and len(set(effect_signs)) == 1 and effect_signs[0] != 0),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
