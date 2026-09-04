"""Deterministic aggregate and bootstrap analysis for 040 S0."""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def bootstrap_difference(rows, cue, readout, seed=20260901, draws=2000):
    frame_rows = defaultdict(list)
    for r in rows:
        if r["cue_family"] == cue and r["readout"] == readout:
            frame_rows[r["frame"]].append(r)
    frames = sorted(frame_rows)
    rng = random.Random(seed)
    estimates = []
    for _ in range(draws):
        sampled = [rng.choice(frames) for _ in frames]
        same, diff = [], []
        for frame in sampled:
            for r in frame_rows[frame]:
                (same if r["identity"] == "same_token" else diff).append(r["margin_same_different"])
        estimates.append(mean(same) - mean(diff))
    estimates.sort()
    return [estimates[int(0.025 * draws)], estimates[int(0.975 * draws)]]


def main():
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
        rows = [x for x in lines if x["record_type"] == "example"]
        model_summary = {"model": meta["model_checkpoint"], "model_revision": meta["model_revision"], "n": len(rows), "cells": {}}
        history_effects = []
        history_pass = True
        for cue in ["released_determiner", "continuity_description"]:
            hr = [r for r in rows if r["cue_family"] == cue and r["readout"] == "history_transfer"]
            same = [r["margin_same_different"] for r in hr if r["identity"] == "same_token"]
            diff = [r["margin_same_different"] for r in hr if r["identity"] == "different_token_same_type"]
            accuracy = mean([r["prediction_semantic"] == r["gold_semantic"] for r in hr])
            same_accuracy = mean([r["prediction_semantic"] == "same" for r in hr if r["identity"] == "same_token"])
            different_accuracy = mean([r["prediction_semantic"] == "different" for r in hr if r["identity"] == "different_token_same_type"])
            effect = mean(same) - mean(diff)
            history_effects.append(abs(effect))
            history_pass &= (
                same_accuracy >= config["gate"]["min_history_accuracy_per_identity_cell"]
                and different_accuracy >= config["gate"]["min_history_accuracy_per_identity_cell"]
                and mean(same) > 0
                and mean(diff) < 0
                and effect > 0
            )
            model_summary["cells"][f"history/{cue}"] = {
                "accuracy": accuracy,
                "same_accuracy": same_accuracy,
                "different_accuracy": different_accuracy,
                "same_margin": mean(same),
                "different_margin": mean(diff),
                "identity_effect": effect,
                "frame_bootstrap_95ci": bootstrap_difference(rows, cue, "history_transfer"),
            }
        tr = [r for r in rows if r["readout"] == "type_knowledge"]
        type_accuracy = mean([r["prediction_semantic"] == "same" for r in tr])
        same_t = [r["margin_same_different"] for r in tr if r["identity"] == "same_token"]
        diff_t = [r["margin_same_different"] for r in tr if r["identity"] == "different_token_same_type"]
        type_identity_effect = abs(mean(same_t) - mean(diff_t))
        fraction = type_identity_effect / (mean(history_effects) + 1e-12)
        type_pass = type_accuracy >= config["gate"]["min_type_accuracy"] and fraction <= config["gate"]["max_type_identity_effect_fraction"]
        model_summary["cells"]["type_control"] = {
            "accuracy": type_accuracy,
            "same_margin": mean(same_t),
            "different_margin": mean(diff_t),
            "absolute_identity_effect": type_identity_effect,
            "fraction_of_history_effect": fraction,
        }
        model_summary["gate_pass"] = bool(history_pass and type_pass)
        summaries.append(model_summary)
    output = {
        "contract": "040 S0 identity-sensitive history transfer with preserved same-type knowledge",
        "models": summaries,
        "panel_gate_pass": len(summaries) >= 2 and all(x["gate_pass"] for x in summaries),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
