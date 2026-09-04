"""Analyze entity-specific versus generic-order effects at the unresolved pronoun."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


MODES = ["real_same_item_opposite_order", "shuffled_item_same_order_delta", "random_matched_norm"]


def cluster_bootstrap(rows: list[dict], statistic, seed: int, n_boot: int) -> dict:
    clusters = sorted({row["semantic_id"] for row in rows})
    grouped = {cluster: [row for row in rows if row["semantic_id"] == cluster] for cluster in clusters}

    def evaluate(sample) -> float:
        values = [statistic(row) for cluster in sample for row in grouped[cluster]]
        return float(np.mean(values))

    observed = evaluate(clusters)
    rng = np.random.default_rng(seed)
    draws = [evaluate(list(rng.choice(clusters, size=len(clusters), replace=True))) for _ in range(n_boot)]
    return {"estimate": observed, "ci95": [float(x) for x in np.quantile(draws, [0.025, 0.975])]}


def margin(scores: dict[str, float], positive_candidates: list[str]) -> float:
    return float(scores[positive_candidates[0]] - scores[positive_candidates[1]])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    lines = [json.loads(line) for line in args.input.read_text().splitlines() if line]
    metadata = next(row for row in lines if row["record_type"] == "metadata")
    rows = [row for row in lines if row["record_type"] == "example"]
    for row in rows:
        positives = row["positive_candidates"]
        row["clean_margin"] = margin(row["clean_scores"], positives)
        row["donor_margin"] = margin(row["donor_clean_scores"], positives)
        row["direction"] = float(np.sign(row["donor_margin"] - row["clean_margin"]))
        row["aligned"] = {
            mode: (margin(row["patched_scores"][mode], positives) - row["clean_margin"]) * row["direction"]
            for mode in MODES
        }
    informative = [row for row in rows if row["direction"] != 0]
    n_boot = int(config["bootstrap_samples"])
    seed = int(config["seed"])
    aligned = {
        mode: cluster_bootstrap(informative, lambda row, name=mode: row["aligned"][name], seed + index, n_boot)
        for index, mode in enumerate(MODES)
    }
    real_minus_controls = {
        control: cluster_bootstrap(
            informative,
            lambda row, name=control: row["aligned"]["real_same_item_opposite_order"] - row["aligned"][name],
            seed + 10 + index, n_boot,
        )
        for index, control in enumerate(MODES[1:])
    }
    both_over_distractor = []
    clean_flips = []
    by_pair = defaultdict(list)
    for row in rows:
        distractor = row["negative_candidate"]
        both_over_distractor.append(all(row["clean_scores"][candidate] > row["clean_scores"][distractor]
                                         for candidate in row["positive_candidates"]))
        clean_flips.append(np.sign(row["clean_margin"]) != np.sign(row["donor_margin"]))
        pair_name = "-".join(sorted([row["permutation"], row["opposite_permutation"]]))
        by_pair[pair_name].append(row)
    pair_effects = {
        pair: {
            mode: float(np.mean([row["aligned"][mode] for row in values if row["direction"] != 0]))
            for mode in MODES
        }
        for pair, values in by_pair.items()
    }
    coverage = float(np.mean(both_over_distractor))
    real = aligned["real_same_item_opposite_order"]
    real_minus_shuffled = real_minus_controls["shuffled_item_same_order_delta"]
    gate = bool(
        coverage >= config["gate"]["min_both_candidates_over_distractor_rate"]
        and real["ci95"][0] > 0 and real_minus_shuffled["ci95"][0] > 0
    )
    result = {
        "contract": "same-content permutation state at unresolved pronoun -> semantic candidate preference",
        "model": metadata["model_checkpoint"], "model_revision": metadata["model_revision"],
        "block_index": metadata["block_index"], "residual_layer": metadata["residual_layer"],
        "n_rows": len(rows), "n_semantic_items": metadata["semantic_items"],
        "n_informative_donor_contrasts": len(informative),
        "clean_both_candidates_over_distractor_rate": coverage,
        "clean_opposite_permutation_preference_flip_rate": float(np.mean(clean_flips)),
        "aligned_effect_toward_same_item_donor": aligned,
        "real_minus_controls": real_minus_controls,
        "mean_effect_by_permutation_pair": pair_effects,
        "gate_pass": gate,
        "interpretation_guard": (
            "A pass shows that an entity-specific, order-induced winner state is already causally active at the "
            "unresolved pronoun beyond a generic order delta. It does not resurrect independent parallel alternatives."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
