"""Test whether ambiguity-specific preferences are constructed at response comparison."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


def score(row: dict, candidate: str) -> float:
    return float(row["scores"][candidate]["logprob"])


def bootstrap(values_by_cluster: dict[str, list[float]], seed: int, n_boot: int) -> dict:
    clusters = sorted(values_by_cluster)

    def statistic(sample) -> float:
        return float(np.mean([value for cluster in sample for value in values_by_cluster[cluster]]))

    observed = statistic(clusters)
    rng = np.random.default_rng(seed)
    draws = [statistic(list(rng.choice(clusters, size=len(clusters), replace=True))) for _ in range(n_boot)]
    return {"estimate": observed, "ci95": [float(value) for value in np.quantile(draws, [0.025, 0.975])]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    summaries = []
    for model_index, path in enumerate(args.inputs):
        lines = [json.loads(line) for line in path.read_text().splitlines() if line]
        metadata = next(row for row in lines if row["record_type"] == "metadata")
        rows = [row for row in lines if row["record_type"] == "example"]
        grouped = defaultdict(list)
        for row in rows:
            grouped[row["item_id"]].append(row)
        clear_accuracy, clear_flips, clear_order_effect = [], [], defaultdict(list)
        shared_coverage, shared_flips, shared_order_effect = [], [], defaultdict(list)
        for values in grouped.values():
            base = values[0]
            if base["split"] == "clear_ref":
                if len(values) != 2:
                    raise ValueError("ClearRef row must have both response orders")
                target = base["positive_candidates"][0]
                distractor = base["negative_candidate"]
                clear_accuracy.extend(score(row, target) > score(row, distractor) for row in values)
                clear_flips.append(len({row["prediction"] for row in values}) > 1)
                target_first = next(row for row in values if row["response_candidate_order"][0] == target)
                target_second = next(row for row in values if row["response_candidate_order"][1] == target)
                clear_order_effect[base["semantic_id"]].append(
                    (score(target_first, target) - score(target_first, distractor))
                    - (score(target_second, target) - score(target_second, distractor))
                )
            else:
                if len(values) != 6:
                    raise ValueError("SharedRef row must have all six response orders")
                first, second = base["positive_candidates"]
                distractor = base["negative_candidate"]
                shared_coverage.extend(
                    score(row, first) > score(row, distractor) and score(row, second) > score(row, distractor)
                    for row in values
                )
                shared_flips.append(len({first if score(row, first) > score(row, second) else second for row in values}) > 1)
                first_before = [row for row in values if row["response_candidate_order"].index(first) < row["response_candidate_order"].index(second)]
                second_before = [row for row in values if row["response_candidate_order"].index(second) < row["response_candidate_order"].index(first)]
                margin_first_before = np.mean([score(row, first) - score(row, second) for row in first_before])
                margin_second_before = np.mean([score(row, first) - score(row, second) for row in second_before])
                shared_order_effect[base["semantic_id"]].append(float(margin_first_before - margin_second_before))
        clear_flip_rate = float(np.mean(clear_flips))
        shared_flip_rate = float(np.mean(shared_flips))
        summary = {
            "model": metadata["model_checkpoint"], "model_revision": metadata["model_revision"],
            "n_source_discourse_rows": len(grouped),
            "clearref_accuracy": float(np.mean(clear_accuracy)),
            "clearref_preference_flip_across_response_orders": clear_flip_rate,
            "clearref_first_listed_target_margin_effect": bootstrap(clear_order_effect, int(config["seed"]) + model_index, int(config["bootstrap_samples"])),
            "sharedref_both_candidates_over_distractor_rate": float(np.mean(shared_coverage)),
            "sharedref_positive_preference_flip_across_response_orders": shared_flip_rate,
            "sharedref_first_positive_listed_margin_effect": bootstrap(shared_order_effect, int(config["seed"]) + 10 + model_index, int(config["bootstrap_samples"])),
            "ambiguity_specific_flip_gap": shared_flip_rate - clear_flip_rate,
        }
        shared_effect = summary["sharedref_first_positive_listed_margin_effect"]
        excludes_zero = shared_effect["ci95"][0] > 0 or shared_effect["ci95"][1] < 0
        summary["gate_pass"] = bool(
            summary["clearref_accuracy"] >= config["gate"]["min_clearref_accuracy"]
            and summary["sharedref_both_candidates_over_distractor_rate"] >= config["gate"]["min_sharedref_both_over_distractor_rate"]
            and summary["ambiguity_specific_flip_gap"] >= config["gate"]["min_ambiguity_specific_flip_gap"]
            and excludes_zero
        )
        summaries.append(summary)
    result = {
        "contract": "response-list sensitivity after unresolved but not resolved reference",
        "models": summaries,
        "panel_gate_pass": bool(len(summaries) >= 2 and all(summary["gate_pass"] for summary in summaries)),
        "interpretation_guard": (
            "A pass supports response-time construction of ambiguous preference when combined with the pronoun-state "
            "causal null; candidate-list bias alone is not a reference-representation claim."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
