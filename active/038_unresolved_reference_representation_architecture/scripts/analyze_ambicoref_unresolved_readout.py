"""Test cross-family transfer of an ambiguous-vs-resolved state readout."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
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
        raise ValueError("Activation/stimulus mismatch")
    by_pair = defaultdict(list)
    for index, row in enumerate(rows):
        by_pair[(row["family"], row["pair_index"])].append(index)
    complete_indices = sorted(
        index
        for indices in by_pair.values()
        if {rows[i]["condition"] for i in indices} == {"ambiguous", "unambiguous"}
        for index in indices
    )
    split = np.array([rows[i]["split"] for i in complete_indices])
    labels = np.array([rows[i]["condition"] == "ambiguous" for i in complete_indices])
    trajectories = {}
    for readout_index, readout in enumerate(metadata["readout_order"]):
        values = []
        for layer in range(x.shape[2]):
            train = split == "discovery"
            probe = make_pipeline(
                StandardScaler(),
                LogisticRegression(C=0.01, class_weight="balanced", max_iter=2000, random_state=20260904),
            )
            probe.fit(x[complete_indices, readout_index, layer][train], labels[train])
            metric = {"layer": layer}
            for name in ["discovery", "validation", "causal_test"]:
                mask = split == name
                probability = probe.predict_proba(x[complete_indices, readout_index, layer][mask])[:, 1]
                metric[name] = {
                    "n": int(mask.sum()),
                    "balanced_accuracy": float(balanced_accuracy_score(labels[mask], probability >= 0.5)),
                    "roc_auc": float(roc_auc_score(labels[mask], probability)),
                }
            values.append(metric)
        trajectories[readout] = values
    middle = list(range(int(0.4 * x.shape[2]), int(0.8 * x.shape[2]) + 1))
    result = {
        "contract": "paired ambiguous-vs-unambiguous readout: ECO/ECS discovery, IC validation, TOP held out",
        "model": metadata["model_checkpoint"],
        "model_revision": metadata["model_revision"],
        "n_complete_pairs": len(complete_indices) // 2,
        "middle_layer_family": middle,
        "trajectories": trajectories,
        "middle_family_summary": {
            readout: {
                split_name: {
                    "median_auc": float(np.median([trajectories[readout][i][split_name]["roc_auc"] for i in middle])),
                    "median_balanced_accuracy": float(np.median([trajectories[readout][i][split_name]["balanced_accuracy"] for i in middle])),
                }
                for split_name in ["validation", "causal_test"]
            }
            for readout in metadata["readout_order"]
        },
        "scope_note": "Cross-family decodability is necessary but not sufficient for H2; causal joint coupling is still required.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["middle_family_summary"], indent=2))


if __name__ == "__main__":
    main()
