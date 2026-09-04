"""Evaluate prespecified cross-family candidate readout trajectories."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--stimuli", type=Path, required=True)
    p.add_argument("--activations", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    rows = [json.loads(x) for x in args.stimuli.read_text().splitlines() if x]
    archive = np.load(args.activations, allow_pickle=False)
    x = archive["activations"].astype(np.float32)
    metadata = json.loads(str(archive["metadata"]))
    if metadata["item_ids"] != [row["item_id"] for row in rows]:
        raise ValueError("Activation/stimulus item order mismatch")
    eligible = np.array([row["resolved_calibration_eligible"] for row in rows])
    labels = np.array([row["human_preferred_candidate"] for row in rows])
    split = np.array([row["split"] for row in rows])

    class_counts = {
        name: {
            str(label): int(((eligible & (split == name)) & (labels == label)).sum())
            for label in [0, 1]
        }
        for name in ["discovery", "validation", "causal_test"]
    }
    if any(class_counts["discovery"][str(label)] == 0 for label in [0, 1]):
        result = {
            "contract": "candidate A/B direction learned on ECO/ECS and evaluated without refit on IC/TOP",
            "model": metadata["model_checkpoint"],
            "model_revision": metadata["model_revision"],
            "activation_shape": list(x.shape),
            "design_valid": False,
            "resolved_class_counts": class_counts,
            "reason": (
                "The released human-judgment calibration is not antecedent-direction balanced: "
                "candidate direction is confounded with structural family. No probe was fit."
            ),
            "scope_note": "This is a measurement-design failure, not evidence for H1, H2, or H3.",
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))
        return

    trajectories = {}
    for readout_index, readout in enumerate(metadata["readout_order"]):
        layer_rows = []
        for layer in range(x.shape[2]):
            train = eligible & (split == "discovery")
            model = make_pipeline(
                StandardScaler(),
                LogisticRegression(C=0.01, class_weight="balanced", max_iter=2000, random_state=20260904),
            )
            model.fit(x[train, readout_index, layer], labels[train])
            metrics = {"layer": layer}
            for name in ["discovery", "validation", "causal_test"]:
                mask = eligible & (split == name)
                probability = model.predict_proba(x[mask, readout_index, layer])[:, 1]
                prediction = probability >= 0.5
                metrics[name] = {
                    "n": int(mask.sum()),
                    "balanced_accuracy": float(balanced_accuracy_score(labels[mask], prediction)),
                    "roc_auc": float(roc_auc_score(labels[mask], probability)),
                }
            layer_rows.append(metrics)
        trajectories[readout] = layer_rows

    result = {
        "contract": "candidate A/B direction learned on ECO/ECS and evaluated without refit on IC/TOP",
        "model": metadata["model_checkpoint"],
        "model_revision": metadata["model_revision"],
        "activation_shape": list(x.shape),
        "fixed_probe": {"C": 0.01, "class_weight": "balanced", "scaling": "discovery_only"},
        "trajectories": trajectories,
        "scope_note": "Decodability is only a foothold; it does not identify H1/H2/H3 or license unresolved-state claims.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    for readout, values in trajectories.items():
        best_validation = max(values, key=lambda z: z["validation"]["roc_auc"])
        print(json.dumps({"readout": readout, "best_validation_layer_for_diagnostic_only": best_validation}))


if __name__ == "__main__":
    main()
