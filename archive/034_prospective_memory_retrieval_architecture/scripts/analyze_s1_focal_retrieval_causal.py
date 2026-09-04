"""Analyze whether focal cue-token states selectively rescue a second intention."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


MODES = ["real_focal_state", "shuffled_item_focal_delta", "random_matched_norm"]
SEMANTICS = ["TARGET_ACTION", "OTHER_ACTION", "YES", "NO"]


def margin(scores: dict[str, float]) -> float:
    return scores["OTHER_ACTION"] - max(scores[value] for value in SEMANTICS if value != "OTHER_ACTION")


def bootstrap(items: list[dict], statistic, seed: int, n_boot: int) -> dict:
    identifiers = sorted({item["semantic_id"] for item in items})
    grouped = {identifier: [item for item in items if item["semantic_id"] == identifier] for identifier in identifiers}

    def evaluate(sample) -> float:
        return float(np.mean([statistic(item) for identifier in sample for item in grouped[identifier]]))

    observed = evaluate(identifiers)
    rng = np.random.default_rng(seed)
    draws = [evaluate(list(rng.choice(identifiers, size=len(identifiers), replace=True))) for _ in range(n_boot)]
    return {"estimate": observed, "ci95": [float(value) for value in np.quantile(draws, [0.025, 0.975])]}


def aggregate(rows: list[dict], residual_layer: str) -> list[dict]:
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["semantic_id"], row["cue_type"], row["expectancy"])].append(row)
    result = []
    for key, values in grouped.items():
        if len(values) != 4:
            raise ValueError(f"Expected four mappings for {key}, got {len(values)}")
        clean = {semantic: float(np.mean([row["clean_semantic_scores"][semantic] for row in values]))
                 for semantic in SEMANTICS}
        patched = {}
        for mode in MODES:
            patched[mode] = {
                semantic: float(np.mean([
                    row["patched_by_residual_layer"][residual_layer][mode][row["semantic_to_label"][semantic]]
                    for row in values
                ])) for semantic in SEMANTICS
            }
        result.append({
            "semantic_id": key[0], "cue_type": key[1], "expectancy": key[2],
            "clean": clean, "patched": patched,
            "clean_margin": margin(clean),
            "patched_margin": {mode: margin(scores) for mode, scores in patched.items()},
        })
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
        raw_rows = [row for row in lines if row["record_type"] == "example"]
        layers = {}
        positive_depths = 0
        for layer_index, residual_layer in enumerate(metadata["residual_layers"]):
            items = aggregate(raw_rows, str(residual_layer))
            cue = [item for item in items if item["cue_type"] == "other"]
            no_cue = [item for item in items if item["cue_type"] == "none"]
            effects = {
                mode: bootstrap(cue, lambda item, name=mode: item["patched_margin"][name] - item["clean_margin"],
                                int(config["seed"]) + 100 * model_index + 10 * layer_index + mode_index,
                                int(config["bootstrap_samples"]))
                for mode_index, mode in enumerate(MODES)
            }
            real_minus_controls = {
                control: bootstrap(
                    cue,
                    lambda item, name=control: (item["patched_margin"]["real_focal_state"] - item["clean_margin"])
                    - (item["patched_margin"][name] - item["clean_margin"]),
                    int(config["seed"]) + 1000 + 100 * model_index + 10 * layer_index + control_index,
                    int(config["bootstrap_samples"]),
                ) for control_index, control in enumerate(MODES[1:])
            }
            clean_no_cue_intrusion = float(np.mean([max(item["clean"], key=item["clean"].get) == "OTHER_ACTION" for item in no_cue]))
            patched_no_cue_intrusion = float(np.mean([
                max(item["patched"]["real_focal_state"], key=item["patched"]["real_focal_state"].get) == "OTHER_ACTION"
                for item in no_cue
            ]))
            depth_pass = bool(effects["real_focal_state"]["ci95"][0] > 0
                              and real_minus_controls["shuffled_item_focal_delta"]["ci95"][0] > 0
                              and patched_no_cue_intrusion - clean_no_cue_intrusion
                              <= config["gate"]["max_no_cue_other_action_intrusion_increase"])
            positive_depths += int(depth_pass)
            layers[str(residual_layer)] = {
                "n_other_cue_items": len(cue), "n_no_cue_items": len(no_cue),
                "other_action_margin_effect": effects, "real_minus_controls": real_minus_controls,
                "clean_no_cue_other_action_intrusion": clean_no_cue_intrusion,
                "patched_no_cue_other_action_intrusion": patched_no_cue_intrusion,
                "depth_pass": depth_pass,
            }
        models.append({
            "model": metadata["model_checkpoint"], "model_revision": metadata["model_revision"],
            "residual_layers": metadata["residual_layers"], "layers": layers,
            "positive_depths": positive_depths,
            "trajectory_gate_pass": positive_depths >= config["gate"]["min_positive_depths"],
        })
    result = {
        "contract": "focal cue-token state selectively rescues lower-priority intention retrieval",
        "models": models,
        "panel_gate_pass": bool(len(models) >= 2 and all(model["trajectory_gate_pass"] for model in models)),
        "interpretation_guard": (
            "A pass supports semantic retrieval gating only when focal-state effects exceed shuffled deltas across "
            "multiple fixed depths and do not induce OTHER_ACTION on no-cue controls."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
