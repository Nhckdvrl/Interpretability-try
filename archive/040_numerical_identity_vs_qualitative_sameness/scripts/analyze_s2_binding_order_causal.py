"""Analyze whether a content-preserving binding-order state causally controls history use."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


MODES = ["real_opposite_order", "shuffled_opposite_order_delta", "random_matched_norm"]


def aggregate_label_orders(rows: list[dict]) -> list[dict]:
    grouped = defaultdict(list)
    for row in rows:
        key = (row["source_row"], row["frame"], row["state_change"], row["competitor_relation"],
               row["identity"], row["cue_family"], row["readout"], row["object_order"])
        grouped[key].append(row)
    result = []
    for key, values in grouped.items():
        if len(values) != 2:
            raise ValueError(f"Expected both label orders for {key}, got {len(values)}")
        item = {
            "source_row": key[0], "frame": key[1], "state_change": key[2],
            "competitor_relation": key[3], "identity": key[4], "cue_family": key[5],
            "readout": key[6], "object_order": key[7],
            "clean_margin": float(np.mean([x["clean_margin"] for x in values])),
            "opposite_clean_margin": float(np.mean([x["opposite_order_clean_margin"] for x in values])),
        }
        item["patched_margin"] = {
            mode: float(np.mean([x["patched"][mode]["target_margin"] for x in values])) for mode in MODES
        }
        direction = np.sign(item["opposite_clean_margin"] - item["clean_margin"])
        item["opposite_direction"] = float(direction)
        item["aligned_effect"] = {
            mode: float((item["patched_margin"][mode] - item["clean_margin"]) * direction) for mode in MODES
        }
        result.append(item)
    return result


def cluster_bootstrap(items: list[dict], field, seed: int, n_boot: int) -> dict:
    frames = sorted({x["frame"] for x in items})
    by_frame = {frame: [x for x in items if x["frame"] == frame] for frame in frames}

    def stat(sample):
        values = [field(x) for frame in sample for x in by_frame[frame]]
        return float(np.mean(values))

    observed = stat(frames)
    rng = np.random.default_rng(seed)
    draws = [stat(list(rng.choice(frames, size=len(frames), replace=True))) for _ in range(n_boot)]
    return {"estimate": observed, "ci95": [float(x) for x in np.quantile(draws, [0.025, 0.975])]}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    lines = [json.loads(x) for x in args.input.read_text().splitlines() if x]
    meta = next(x for x in lines if x["record_type"] == "metadata")
    items = aggregate_label_orders([x for x in lines if x["record_type"] == "example"])
    history = [x for x in items if x["readout"] == "history_transfer" and x["opposite_direction"] != 0]
    type_items = [x for x in items if x["readout"] == "type_knowledge"]
    n_boot = int(config["bootstrap_samples"])
    seed = int(config["seed"])
    aligned = {
        mode: cluster_bootstrap(history, lambda x, m=mode: x["aligned_effect"][m], seed, n_boot)
        for mode in MODES
    }
    real_minus_controls = {
        control: cluster_bootstrap(
            history,
            lambda x, c=control: x["aligned_effect"]["real_opposite_order"] - x["aligned_effect"][c],
            seed + index + 1, n_boot,
        )
        for index, control in enumerate(MODES[1:])
    }
    clean_type_accuracy = float(np.mean([x["clean_margin"] > 0 for x in type_items]))
    type_accuracy = {
        mode: float(np.mean([x["patched_margin"][mode] > 0 for x in type_items])) for mode in MODES
    }
    type_abs_margin_change = {
        mode: cluster_bootstrap(type_items, lambda x, m=mode: abs(x["patched_margin"][m] - x["clean_margin"]), seed, n_boot)
        for mode in MODES
    }
    real = aligned["real_opposite_order"]
    real_minus_shuffled = real_minus_controls["shuffled_opposite_order_delta"]
    gate = bool(
        real["ci95"][0] > 0
        and real_minus_shuffled["ci95"][0] > 0
        and clean_type_accuracy >= config["gate"]["min_clean_type_accuracy"]
        and clean_type_accuracy - type_accuracy["real_opposite_order"] <= config["gate"]["max_type_accuracy_drop"]
    )
    result = {
        "contract": "content-preserving binding-order state -> history transfer while preserving type knowledge",
        "model": meta["model_checkpoint"], "model_revision": meta["model_revision"],
        "block_index": meta["block_index"], "residual_layer": meta["residual_layer"],
        "test_frames": meta["test_frames"], "n_label_aggregated_items": len(items),
        "n_history_nonzero_donor_contrasts": len(history),
        "history_aligned_effect_toward_opposite_order": aligned,
        "history_real_minus_controls": real_minus_controls,
        "clean_type_accuracy": clean_type_accuracy, "patched_type_accuracy": type_accuracy,
        "type_absolute_margin_change": type_abs_margin_change,
        "gate_pass": gate,
        "interpretation_guard": (
            "A pass identifies causal use of a content-preserving binding-order state, not a numerical-identity "
            "representation. It develops 040 only through its identity-use failure and preserved type control."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
