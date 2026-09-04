"""Aggregate the two-intention PM validation over Latin-square response mappings."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


SEMANTICS = ["TARGET_ACTION", "OTHER_ACTION", "YES", "NO"]


def aggregate(rows: list[dict]) -> list[dict]:
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["semantic_id"], row["cue_present"], row["focality"], row["expectancy"])].append(row)
    result = []
    for key, values in grouped.items():
        if len(values) != 4:
            raise ValueError(f"Expected four Latin-square maps for {key}, got {len(values)}")
        scores = {s: float(np.mean([x["semantic_scores"][s] for x in values])) for s in SEMANTICS}
        prediction = max(scores, key=scores.get)
        result.append({
            "semantic_id": key[0], "cue_present": key[1], "focality": key[2], "expectancy": key[3],
            "scores": scores, "prediction": prediction, "correct_semantic": values[0]["correct_semantic"],
            "correct": prediction == values[0]["correct_semantic"],
            "target_action_margin": scores["TARGET_ACTION"] - max(scores[x] for x in SEMANTICS if x != "TARGET_ACTION"),
        })
    return result


def bootstrap_focality(rows: list[dict], seed: int, n_boot: int = 5000) -> dict:
    by_id = defaultdict(dict)
    for row in rows:
        by_id[row["semantic_id"]][(row["cue_present"], row["focality"], row["expectancy"])] = row
    ids = sorted(by_id)

    def stat(sample, expectancy):
        return float(np.mean([
            by_id[item][(True, "focal", expectancy)]["target_action_margin"]
            - by_id[item][(True, "nonfocal", expectancy)]["target_action_margin"] for item in sample
        ]))

    rng = np.random.default_rng(seed)
    result = {}
    for expectancy in ["expected", "unexpected"]:
        observed = stat(ids, expectancy)
        draws = [stat(list(rng.choice(ids, size=len(ids), replace=True)), expectancy) for _ in range(n_boot)]
        result[expectancy] = {"estimate": observed, "ci95": [float(x) for x in np.quantile(draws, [0.025, 0.975])]}
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
                        "mean_target_action_margin": float(np.mean([x["target_action_margin"] for x in selected])),
                        "prediction_counts": dict(Counter(x["prediction"] for x in selected)),
                    }
        cue_rows = [x for x in rows if x["cue_present"]]
        no_cue_rows = [x for x in rows if not x["cue_present"]]
        other_intrusion = float(np.mean([x["prediction"] == "OTHER_ACTION" for x in cue_rows]))
        contrasts = bootstrap_focality(rows, int(config["seed"]))
        cue_acc = [v["accuracy"] for k, v in cells.items() if k.startswith("cue/")]
        no_cue_acc = [v["accuracy"] for k, v in cells.items() if k.startswith("no_cue/")]
        max_focality = max(abs(x["estimate"]) for x in contrasts.values())
        gate = bool(
            min(no_cue_acc) >= config["gate"]["min_no_cue_accuracy"]
            and min(cue_acc) >= config["gate"]["min_cue_cell_accuracy"]
            and other_intrusion <= config["gate"]["max_other_intention_intrusion"]
            and min(cue_acc) < config["gate"]["all_cue_cells_ceiling"]
            and max_focality >= config["gate"]["min_abs_shared_focality_margin_effect"]
        )
        summaries.append({
            "model": meta["model_checkpoint"], "model_revision": meta["model_revision"],
            "n_semantic_cells": len(rows), "cells": cells,
            "cue_other_intention_intrusion": other_intrusion,
            "focal_minus_nonfocal_target_margin": contrasts, "behavior_gate_pass": gate,
        })
    signs = [np.sign(max(x["focal_minus_nonfocal_target_margin"].values(), key=lambda y: abs(y["estimate"]))["estimate"])
             for x in summaries]
    result = {
        "contract": "delayed two-intention focality x expectancy PM validation",
        "models": summaries,
        "panel_gate_pass": bool(len(summaries) >= 2 and all(x["behavior_gate_pass"] for x in summaries)
                                and len(set(signs)) == 1 and signs[0] != 0),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
