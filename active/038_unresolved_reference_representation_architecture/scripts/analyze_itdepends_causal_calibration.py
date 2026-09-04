"""Summarize held-out causal direction qualification and SharedRef specificity."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def positions(row: dict) -> dict[str, int]:
    listed = [x.strip() for x in row["conversation"][0]["content"].split("following:", 1)[1].split(",")]
    return {candidate: index for index, candidate in enumerate(listed)}


def mean_ci(values, seed=20260904, draws=5000):
    values = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    means = np.mean(rng.choice(values, size=(draws, len(values)), replace=True), axis=1)
    return {"mean": float(values.mean()), "bootstrap_95ci": [float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))]}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    lines = [json.loads(x) for x in args.input.read_text().splitlines() if x]
    meta = next(x for x in lines if x["record_type"] == "metadata")
    rows = [x for x in lines if x["record_type"] == "example"]
    summary = {}
    for control in ["direction", "random_direction", "shuffled_direction"]:
        clear_effects, shared_effects, ccs_values, coverage_values = [], [], [], []
        candidate_effects = {"self_position0": [], "cross_position0": [], "self_position1": [], "cross_position1": []}
        for row in rows:
            pos = positions(row)
            plus = row["intervention_scores"][f"{control}_plus"]
            minus = row["intervention_scores"][f"{control}_minus"]
            if row["split"] == "clear_ref":
                positive = row["positive_candidates"][0]
                negative = row["negative_candidate"]
                label_sign = 1 if pos[positive] == 1 else -1
                clear_effects.append(label_sign * ((plus[positive] - plus[negative]) - (minus[positive] - minus[negative])))
            else:
                by_position = {position: candidate for candidate, position in pos.items()}
                shared_effects.append((plus[by_position[1]] - plus[by_position[0]]) - (minus[by_position[1]] - minus[by_position[0]]))
                baseline = row["intervention_scores"]["baseline"]
                candidate0, candidate1, distractor = by_position[0], by_position[1], by_position[2]
                self0 = (minus[candidate0] - minus[distractor]) - (baseline[candidate0] - baseline[distractor])
                cross0 = (minus[candidate1] - minus[distractor]) - (baseline[candidate1] - baseline[distractor])
                self1 = (plus[candidate1] - plus[distractor]) - (baseline[candidate1] - baseline[distractor])
                cross1 = (plus[candidate0] - plus[distractor]) - (baseline[candidate0] - baseline[distractor])
                candidate_effects["self_position0"].append(self0)
                candidate_effects["cross_position0"].append(cross0)
                candidate_effects["self_position1"].append(self1)
                candidate_effects["cross_position1"].append(cross1)
                eps = 1e-9
                ccs_values.append(0.5 * (
                    (abs(self0) - abs(cross0)) / (abs(self0) + abs(cross0) + eps)
                    + (abs(self1) - abs(cross1)) / (abs(self1) + abs(cross1) + eps)
                ))
                coverage_values.append(min(abs(self0), abs(self1)) / (max(abs(self0), abs(self1)) + eps))
        summary[control] = {
            "heldout_clearref_aligned_bidirectional_effect": mean_ci(clear_effects),
            "sharedref_position1_vs_position0_effect": mean_ci(shared_effects),
            "sharedref_candidate_effects_relative_to_distractor": {
                name: mean_ci(values) for name, values in candidate_effects.items()
            },
            "sharedref_CCS": mean_ci(ccs_values),
            "sharedref_Coverage": mean_ci(coverage_values),
        }
    result = {
        "contract": "J1 causal qualification on held-out ClearRef; SharedRef effect is basis validation, not architecture adjudication",
        "model": meta["model_checkpoint"],
        "model_revision": meta["model_revision"],
        "intervention_alpha": meta["intervention_alpha"],
        "n_clearref": sum(row["split"] == "clear_ref" for row in rows),
        "n_sharedref": sum(row["split"] == "shared_ref" for row in rows),
        "effects": summary,
        "scope_note": "Passing J1 only qualifies the direction. It does not establish simultaneous candidate coverage or distinguish H1/H2/H3.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
