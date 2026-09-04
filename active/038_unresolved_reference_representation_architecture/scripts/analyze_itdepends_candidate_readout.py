"""Train on resolved ClearRef order pairs and diagnose SharedRef commitment."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def semantic_split(value: str) -> str:
    bucket = int(hashlib.sha256(value.encode()).hexdigest()[:8], 16) % 10
    return "train" if bucket < 6 else "validation" if bucket < 8 else "test"


def positions(row: dict) -> dict[str, int]:
    request = row["conversation"][0]["content"]
    if "following:" not in request:
        raise ValueError(f"Unexpected entity-list prompt for {row['item_id']}")
    listed = [value.strip() for value in request.split("following:", 1)[1].split(",")]
    if set(listed) != set(row["candidates"]) or len(listed) != len(row["candidates"]):
        raise ValueError(f"Could not uniquely locate candidates for {row['item_id']}")
    return {candidate: index for index, candidate in enumerate(listed)}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--stimuli", type=Path, required=True)
    p.add_argument("--behavior", type=Path, required=True)
    p.add_argument("--activations", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    rows = [json.loads(x) for x in args.stimuli.read_text().splitlines() if x]
    behavior_lines = [json.loads(x) for x in args.behavior.read_text().splitlines() if x]
    behavior = {x["item_id"]: x for x in behavior_lines if x["record_type"] == "example"}
    archive = np.load(args.activations, allow_pickle=False)
    x = archive["activations"].astype(np.float32)
    metadata = json.loads(str(archive["metadata"]))
    if metadata["item_ids"] != [row["item_id"] for row in rows]:
        raise ValueError("Activation/stimulus order mismatch")

    clear_indices = [i for i, row in enumerate(rows) if row["split"] == "clear_ref"]
    clear_labels = np.array([positions(rows[i])[rows[i]["positive_candidates"][0]] for i in clear_indices])
    clear_splits = np.array([semantic_split(rows[i]["semantic_id"]) for i in clear_indices])
    if set(clear_labels) != {0, 1}:
        raise ValueError("ClearRef permutations are not position-balanced")
    middle_layers = list(range(int(0.4 * x.shape[1]), int(0.8 * x.shape[1]) + 1))
    trajectory = []
    shared_diagnostics = []
    for layer in range(x.shape[1]):
        train = clear_splits == "train"
        probe = make_pipeline(
            StandardScaler(),
            LogisticRegression(C=0.01, class_weight="balanced", max_iter=2000, random_state=20260904),
        )
        probe.fit(x[clear_indices, layer][train], clear_labels[train])
        metric = {"layer": layer}
        for split_name in ["train", "validation", "test"]:
            mask = clear_splits == split_name
            prob = probe.predict_proba(x[clear_indices, layer][mask])[:, 1]
            metric[split_name] = {
                "n": int(mask.sum()),
                "balanced_accuracy": float(balanced_accuracy_score(clear_labels[mask], prob >= 0.5)),
                "roc_auc": float(roc_auc_score(clear_labels[mask], prob)),
                "mean_confidence": float(np.mean(np.abs(prob - 0.5) * 2)),
            }
        trajectory.append(metric)

        diagnostic_rows = []
        for i, row in enumerate(rows):
            if row["split"] != "shared_ref":
                continue
            pos = positions(row)
            licensed_positions = sorted(pos[c] for c in row["positive_candidates"])
            if licensed_positions != [0, 1]:
                continue
            probability_position_1 = float(probe.predict_proba(x[i, layer][None, :])[0, 1])
            scores = behavior[row["item_id"]]["scores"]
            preferred = max(row["positive_candidates"], key=lambda c: scores[c]["logprob"])
            preferred_position = pos[preferred]
            diagnostic_rows.append((probability_position_1, preferred_position))
        agreement = np.mean([(p >= 0.5) == bool(y) for p, y in diagnostic_rows])
        confidence = np.mean([abs(p - 0.5) * 2 for p, _ in diagnostic_rows])
        shared_diagnostics.append({
            "layer": layer,
            "n": len(diagnostic_rows),
            "agreement_with_output_preference": float(agreement),
            "mean_commitment_confidence": float(confidence),
        })

    result = {
        "contract": "position-balanced ClearRef referent readout; SharedRef diagnostic is non-causal",
        "model": metadata["model_checkpoint"],
        "model_revision": metadata["model_revision"],
        "semantic_split_rule": "sha256 semantic_id modulo 10: 0-5 train, 6-7 validation, 8-9 test",
        "middle_layer_family": middle_layers,
        "trajectory": trajectory,
        "sharedref_diagnostic": shared_diagnostics,
        "middle_family_summary": {
            "median_clearref_test_auc": float(np.median([trajectory[i]["test"]["roc_auc"] for i in middle_layers])),
            "median_sharedref_output_agreement": float(np.median([shared_diagnostics[i]["agreement_with_output_preference"] for i in middle_layers])),
            "median_sharedref_commitment_confidence": float(np.median([shared_diagnostics[i]["mean_commitment_confidence"] for i in middle_layers])),
        },
        "scope_note": "An extreme single-axis projection can support an H3 follow-up, but cannot distinguish H1 from H2 and is not causal evidence.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["middle_family_summary"], indent=2))


if __name__ == "__main__":
    main()
