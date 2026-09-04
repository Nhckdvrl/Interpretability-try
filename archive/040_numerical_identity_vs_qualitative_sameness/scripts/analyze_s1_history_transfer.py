"""Aggregate S1 behavior across cue, identity, and state-change cells."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    lines = [json.loads(x) for x in args.input.read_text().splitlines() if x]
    meta = next(x for x in lines if x["record_type"] == "metadata")
    rows = [x for x in lines if x["record_type"] == "example"]
    cells = defaultdict(list)
    for row in rows:
        cells[(row["readout"], row["competitor_relation"], row["cue_family"], row["identity"], row["object_order"], row["state_change"])].append(row)
    cell_summary = {
        "/".join(key): {"n": len(values), "accuracy": float(np.mean([x["correct"] for x in values])),
                        "mean_target_margin": float(np.mean([x["target_margin"] for x in values]))}
        for key, values in cells.items()
    }
    history_by_cue = {
        cue: float(np.mean([row["correct"] for row in rows if row["readout"] == "history_transfer" and row["cue_family"] == cue]))
        for cue in ["explicit_object_label", "continuity_description"]
    }
    history_identity_order = {
        f"{relation}/{cue}/{identity}/{order}": float(np.mean([
            row["correct"] for row in rows
            if row["readout"] == "history_transfer" and row["competitor_relation"] == relation
            and row["cue_family"] == cue
            and row["identity"] == identity and row["object_order"] == order
        ]))
        for relation in ["same_type", "different_type"]
        for cue in ["explicit_object_label", "continuity_description"]
        for identity in ["same_token", "different_token"]
        for order in ["alpha_first", "beta_first"]
    }
    history_rows = [row for row in rows if row["readout"] == "history_transfer"]
    binding_recency = {
        relation: {
        "target_code_binding_last": float(np.mean([
            row["correct"] for row in history_rows
            if row["competitor_relation"] == relation
            if (row["identity"] == "same_token") == (row["object_order"] == "beta_first")
        ])),
        "target_code_binding_not_last": float(np.mean([
            row["correct"] for row in history_rows
            if row["competitor_relation"] == relation
            if (row["identity"] == "same_token") != (row["object_order"] == "beta_first")
        ])),
        }
        for relation in ["same_type", "different_type"]
    }
    type_accuracy = float(np.mean([row["correct"] for row in rows if row["readout"] == "type_knowledge"]))
    result = {
        "contract": "arbitrary episode-history inheritance with preserved type knowledge",
        "model": meta["model_checkpoint"], "model_revision": meta["model_revision"],
        "n": len(rows), "history_accuracy_by_cue": history_by_cue,
        "history_accuracy_by_cue_identity_order": history_identity_order,
        "binding_recency_prediction": binding_recency, "type_accuracy": type_accuracy,
        "cells": cell_summary,
        "gate_pass": bool(
            all(
                value >= config["gate"]["min_history_accuracy_per_cue_identity_order_cell"]
                for key, value in history_identity_order.items() if key.startswith("same_type/")
            )
            and type_accuracy >= config["gate"]["min_type_accuracy"]
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
