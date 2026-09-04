"""Analyze cross-task causal transfer from identity judgment to history inheritance."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


DIRECTIONS = ["identity", "shuffled", "random"]


def aggregate_label_orders(rows: list[dict]) -> list[dict]:
    grouped = defaultdict(list)
    for row in rows:
        key = tuple(row[name] for name in ["source_row", "frame", "state_change", "competitor_relation",
                                             "identity", "cue_family", "readout", "object_order"])
        grouped[key].append(row)
    result = []
    for key, values in grouped.items():
        if len(values) != 2:
            raise ValueError(f"Expected two label orders for {key}, got {len(values)}")
        item = {name: value for name, value in zip(
            ["source_row", "frame", "state_change", "competitor_relation", "identity", "cue_family", "readout", "object_order"], key
        )}
        margins = {}
        for condition in ["baseline", *[f"{name}_{sign}" for name in DIRECTIONS for sign in ["plus", "minus"]]]:
            margins[condition] = float(np.mean([
                row["intervention_scores"][condition][row["target_label"]]
                - row["intervention_scores"][condition][row["foil_label"]] for row in values
            ]))
        item["margins"] = margins
        item["target_binding_last"] = (
            (item["identity"] == "same_token" and item["object_order"] == "beta_first")
            or (item["identity"] == "different_token" and item["object_order"] == "alpha_first")
        )
        identity_sign = 1.0 if item["identity"] == "same_token" else -1.0
        item["aligned_effect"] = {
            name: identity_sign * (margins[f"{name}_plus"] - margins[f"{name}_minus"]) / 2.0
            for name in DIRECTIONS
        }
        result.append(item)
    return result


def cluster_bootstrap(items: list[dict], statistic, seed: int, n_boot: int) -> dict:
    frames = sorted({item["frame"] for item in items})
    grouped = {frame: [item for item in items if item["frame"] == frame] for frame in frames}

    def evaluate(sample) -> float:
        return float(np.mean([statistic(item) for frame in sample for item in grouped[frame]]))

    observed = evaluate(frames)
    rng = np.random.default_rng(seed)
    draws = [evaluate(list(rng.choice(frames, size=len(frames), replace=True))) for _ in range(n_boot)]
    return {"estimate": observed, "ci95": [float(value) for value in np.quantile(draws, [0.025, 0.975])]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    lines = [json.loads(line) for line in args.input.read_text().splitlines() if line]
    metadata = next(row for row in lines if row["record_type"] == "metadata")
    items = aggregate_label_orders([row for row in lines if row["record_type"] == "example"])
    history = [item for item in items if item["readout"] == "history_transfer"]
    type_items = [item for item in items if item["readout"] == "type_knowledge"]
    seed = int(config["seed"])
    n_boot = int(config["bootstrap_samples"])
    aligned = {
        name: cluster_bootstrap(history, lambda item, direction=name: item["aligned_effect"][direction], seed + index, n_boot)
        for index, name in enumerate(DIRECTIONS)
    }
    identity_minus_controls = {
        control: cluster_bootstrap(
            history,
            lambda item, name=control: item["aligned_effect"]["identity"] - item["aligned_effect"][name],
            seed + 10 + index, n_boot,
        )
        for index, control in enumerate(DIRECTIONS[1:])
    }
    by_binding_order = {
        ("target_binding_last" if last else "target_binding_not_last"): {
            name: cluster_bootstrap([item for item in history if item["target_binding_last"] == last],
                                    lambda item, direction=name: item["aligned_effect"][direction], seed + 20 + index, n_boot)
            for index, name in enumerate(DIRECTIONS)
        }
        for last in [True, False]
    }
    clean_type_accuracy = float(np.mean([item["margins"]["baseline"] > 0 for item in type_items]))
    patched_type_accuracy = {
        condition: float(np.mean([item["margins"][condition] > 0 for item in type_items]))
        for condition in ["identity_plus", "identity_minus", "shuffled_plus", "shuffled_minus", "random_plus", "random_minus"]
    }
    worst_identity_drop = clean_type_accuracy - min(patched_type_accuracy["identity_plus"], patched_type_accuracy["identity_minus"])
    readout = metadata["identity_readout"]
    gate = bool(
        readout["test_cross_surface_auc"] >= config["gate"]["min_cross_surface_identity_auc"]
        and aligned["identity"]["ci95"][0] > 0
        and identity_minus_controls["shuffled"]["ci95"][0] > 0
        and clean_type_accuracy >= config["gate"]["min_clean_type_accuracy"]
        and worst_identity_drop <= config["gate"]["max_type_accuracy_drop"]
    )
    result = {
        "contract": "cross-surface identity state -> arbitrary history inheritance with type knowledge preserved",
        "model": metadata["model_checkpoint"], "model_revision": metadata["model_revision"],
        "block_index": metadata["block_index"], "residual_layer": metadata["residual_layer"],
        "test_frames": metadata["test_frames"], "identity_readout": readout,
        "n_label_aggregated_items": len(items),
        "history_identity_aligned_bidirectional_effect": aligned,
        "identity_minus_controls": identity_minus_controls,
        "history_effect_by_binding_order": by_binding_order,
        "clean_type_accuracy": clean_type_accuracy, "patched_type_accuracy": patched_type_accuracy,
        "worst_identity_type_accuracy_drop": worst_identity_drop,
        "gate_pass": gate,
        "interpretation_guard": (
            "A pass is cross-task causal evidence for an abstract numerical-identity state. A readable direction "
            "without selective history transfer is representation without established causal use."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
