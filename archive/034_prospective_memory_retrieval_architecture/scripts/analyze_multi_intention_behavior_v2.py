"""Analyze the final two-live-intention PM behavioral validation."""

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
        grouped[(row["semantic_id"], row["cue_type"], row["focality"], row["expectancy"])].append(row)
    result = []
    for key, values in grouped.items():
        if len(values) != 4:
            raise ValueError(f"Expected four Latin-square maps for {key}, got {len(values)}")
        scores = {semantic: float(np.mean([row["semantic_scores"][semantic] for row in values])) for semantic in SEMANTICS}
        prediction = max(scores, key=scores.get)
        result.append({
            "semantic_id": key[0], "cue_type": key[1], "focality": key[2], "expectancy": key[3],
            "scores": scores, "prediction": prediction, "correct_semantic": values[0]["correct_semantic"],
            "correct": prediction == values[0]["correct_semantic"],
            "target_action_margin": scores["TARGET_ACTION"] - max(scores[value] for value in SEMANTICS if value != "TARGET_ACTION"),
        })
    return result


def paired_bootstrap(rows: list[dict], cue_type: str, left: tuple[str, str], right: tuple[str, str],
                     seed: int, n_boot: int = 5000) -> dict:
    grouped = defaultdict(dict)
    for row in rows:
        if row["cue_type"] == cue_type:
            grouped[row["semantic_id"]][(row["focality"], row["expectancy"])] = row
    identifiers = sorted(grouped)

    def statistic(sample) -> float:
        return float(np.mean([
            grouped[identifier][left]["target_action_margin"] - grouped[identifier][right]["target_action_margin"]
            for identifier in sample
        ]))

    rng = np.random.default_rng(seed)
    observed = statistic(identifiers)
    draws = [statistic(list(rng.choice(identifiers, size=len(identifiers), replace=True))) for _ in range(n_boot)]
    return {"estimate": observed, "ci95": [float(value) for value in np.quantile(draws, [0.025, 0.975])]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    summaries = []
    for path in args.inputs:
        lines = [json.loads(line) for line in path.read_text().splitlines() if line]
        metadata = next(row for row in lines if row["record_type"] == "metadata")
        rows = aggregate([row for row in lines if row["record_type"] == "example"])
        cells = {}
        for cue_type in ["none", "target", "other"]:
            for focality in ["focal", "nonfocal"]:
                for expectancy in ["expected", "unexpected"]:
                    chosen = [row for row in rows if row["cue_type"] == cue_type and row["focality"] == focality
                              and row["expectancy"] == expectancy]
                    cells[f"{cue_type}/{focality}/{expectancy}"] = {
                        "n": len(chosen), "accuracy": float(np.mean([row["correct"] for row in chosen])),
                        "mean_target_action_margin": float(np.mean([row["target_action_margin"] for row in chosen])),
                        "prediction_counts": dict(Counter(row["prediction"] for row in chosen)),
                    }
        target_rows = [row for row in rows if row["cue_type"] == "target"]
        other_rows = [row for row in rows if row["cue_type"] == "other"]
        cross_confusion = float(np.mean(
            [row["prediction"] == "OTHER_ACTION" for row in target_rows]
            + [row["prediction"] == "TARGET_ACTION" for row in other_rows]
        ))
        focality = {
            expectancy: paired_bootstrap(rows, "target", ("focal", expectancy), ("nonfocal", expectancy),
                                         int(config["seed"]) + index)
            for index, expectancy in enumerate(["expected", "unexpected"])
        }
        expectancy_effect = {
            focal: paired_bootstrap(rows, "target", (focal, "expected"), (focal, "unexpected"),
                                    int(config["seed"]) + 10 + index)
            for index, focal in enumerate(["focal", "nonfocal"])
        }
        no_cue_accuracy = [value["accuracy"] for key, value in cells.items() if key.startswith("none/")]
        target_accuracy = [value["accuracy"] for key, value in cells.items() if key.startswith("target/")]
        other_accuracy = [value["accuracy"] for key, value in cells.items() if key.startswith("other/")]
        strongest_focality = max(abs(value["estimate"]) for value in focality.values())
        gate = bool(
            min(no_cue_accuracy) >= config["gate"]["min_no_cue_accuracy"]
            and min(target_accuracy) >= config["gate"]["min_target_cue_cell_accuracy"]
            and min(other_accuracy) >= config["gate"]["min_other_cue_cell_accuracy"]
            and cross_confusion <= config["gate"]["max_cross_intention_confusion"]
            and min(target_accuracy) < config["gate"]["all_target_cue_cells_ceiling"]
            and strongest_focality >= config["gate"]["min_abs_shared_focality_margin_effect"]
        )
        summaries.append({
            "model": metadata["model_checkpoint"], "model_revision": metadata["model_revision"],
            "n_semantic_cells": len(rows), "cells": cells,
            "cross_intention_confusion": cross_confusion,
            "focal_minus_nonfocal_target_margin": focality,
            "expected_minus_unexpected_target_margin": expectancy_effect,
            "behavior_gate_pass": gate,
        })
    signs = [np.sign(max(summary["focal_minus_nonfocal_target_margin"].values(),
                         key=lambda value: abs(value["estimate"]))["estimate"]) for summary in summaries]
    result = {
        "contract": "delayed two-live-intention focality x expectancy validation without exact cue repetition",
        "models": summaries,
        "panel_gate_pass": bool(len(summaries) >= 2 and all(summary["behavior_gate_pass"] for summary in summaries)
                                and len(set(signs)) == 1 and signs[0] != 0),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
