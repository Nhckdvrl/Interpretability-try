#!/usr/bin/env python3
"""Create the compact, uncertainty-aware summary for the first Phase-2 runs."""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import defaultdict
from pathlib import Path

from mechanism_data import load_jsonl


def bootstrap_ci(values: list[float], seed: int = 6, draws: int = 10_000) -> list[float]:
    rng = random.Random(seed)
    means = sorted(
        sum(rng.choice(values) for _ in values) / len(values) for _ in range(draws)
    )
    return [means[int(0.025 * draws)], means[int(0.975 * draws)]]


def wilson(successes: int, n: int, z: float = 1.959963984540054) -> list[float]:
    p = successes / n
    denominator = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denominator
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return [centre - half, centre + half]


def summarize_run(paths: list[str]) -> dict:
    rows = []
    for path in paths:
        rows.extend(load_jsonl(Path(path)))
    grouped: dict[tuple[int, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row["layer"], row["pair_type"])].append(row)
    layers = []
    for layer in sorted({row["layer"] for row in rows}):
        crossing = grouped[(layer, "posterior_crossing")]
        recoveries = [
            row["normalized_recovery"]
            for row in crossing
            if row["normalized_recovery"] is not None
        ]
        successes = sum(row["donor_action_iia"] for row in crossing)
        record = {
            "layer": layer,
            "n_crossing": len(crossing),
            "mean_recovery": sum(recoveries) / len(recoveries),
            "recovery_pair_bootstrap_95ci": bootstrap_ci(recoveries),
            "donor_action_iia": successes / len(crossing),
            "donor_action_iia_wilson_95ci": wilson(successes, len(crossing)),
            "directional_fraction": sum(
                row["raw_patch_effect"]
                * (row["donor_semantic_logit"] - row["receiver_semantic_logit"])
                > 0
                for row in crossing
            )
            / len(crossing),
            "mean_abs_crossing_effect": sum(
                abs(row["raw_patch_effect"]) for row in crossing
            )
            / len(crossing),
        }
        for placebo in ("posterior_equivalent", "posterior_noncrossing"):
            group = grouped.get((layer, placebo), [])
            record[f"n_{placebo}"] = len(group)
            record[f"mean_abs_{placebo}_effect"] = (
                sum(abs(row["raw_patch_effect"]) for row in group) / len(group)
                if group
                else None
            )
        layers.append(record)
    layer0 = next(row for row in layers if row["layer"] == 0)
    return {
        "n_rows": len(rows),
        "condition": rows[0]["condition"],
        "span": rows[0].get("span", "single"),
        "surface_coverage_at_layer0": sorted(
            {row["surface_id"] for row in rows if row["layer"] == 0}
        ),
        "threshold_coverage_at_layer0": sorted(
            {row["threshold"] for row in rows if row["layer"] == 0}
        ),
        "layer0": layer0,
        "layers": layers,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold-number", nargs="+", required=True)
    parser.add_argument("--gold-statement", nargs="+", required=True)
    parser.add_argument("--self-number", nargs="+", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    result = {
        "gold_belief_number": summarize_run(args.gold_number),
        "gold_belief_statement": summarize_run(args.gold_statement),
        "self_mean_belief_number": summarize_run(args.self_number),
    }
    Path(args.out).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value["layer0"] for key, value in result.items()}, indent=2))


if __name__ == "__main__":
    main()
