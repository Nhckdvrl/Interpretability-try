"""Analyze and adjudicate the frozen exact-frequency D0."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PROBABILITY = "description_probability"
COUNTS = "description_counts"
EXPERIENCE = "experience_exact"


def bootstrap_mean(frame: pd.DataFrame, column: str, seed: int, replicates: int) -> dict:
    cluster_ids = sorted(frame["gamble_id"].unique())
    clusters = {key: frame[frame["gamble_id"] == key] for key in cluster_ids}
    rng = np.random.default_rng(seed)
    values = []
    for _ in range(replicates):
        sample = rng.choice(cluster_ids, size=len(cluster_ids), replace=True)
        boot = pd.concat([clusters[key] for key in sample], ignore_index=True)
        values.append(float(boot[column].mean()))
    return {
        "mean": float(frame[column].mean()),
        "ci95": [float(np.quantile(values, 0.025)), float(np.quantile(values, 0.975))],
        "cluster_count": len(cluster_ids),
        "bootstrap_replicates": replicates,
    }


def choice_units(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    choice = frame[frame["query_type"] == "choice"].copy()
    order_differences = choice.groupby(
        ["gamble_id", "scale", "shuffle_index", "presentation_mode"]
    )["p_target"].agg(lambda values: float(max(values) - min(values))).reset_index(name="difference")
    averaged = choice.groupby(
        ["gamble_id", "gamble_family", "human_direction", "scale", "shuffle_index", "presentation_mode"],
        dropna=False,
        as_index=False,
    )["p_target"].mean()
    pivot = averaged.pivot(
        index=["gamble_id", "gamble_family", "human_direction", "scale", "shuffle_index"],
        columns="presentation_mode",
        values="p_target",
    ).reset_index()
    if pivot[[PROBABILITY, COUNTS, EXPERIENCE]].isna().any().any():
        raise ValueError("incomplete paired presentation units")
    directed = pivot[pivot["human_direction"].notna()].copy()
    directed["normalized_gap_probability"] = directed["human_direction"] * (directed[EXPERIENCE] - directed[PROBABILITY])
    directed["normalized_gap_counts"] = directed["human_direction"] * (directed[EXPERIENCE] - directed[COUNTS])
    return directed, order_differences


def summarize_family(frame: pd.DataFrame, contract: dict) -> dict:
    capability = frame[frame["query_type"] != "choice"].copy()
    frequency = capability[capability["query_type"].isin(["frequency_a", "frequency_b"])]
    ev = capability[capability["query_type"] == "expected_value"]
    choice = frame[frame["query_type"] == "choice"]
    dominance = choice[choice["gamble_family"] == "dominance"]
    directed, order_differences = choice_units(frame)
    seed = contract["effect_gates"]["bootstrap_seed"]
    reps = contract["effect_gates"]["bootstrap_replicates"]
    gap_probability = bootstrap_mean(directed, "normalized_gap_probability", seed, reps)
    gap_counts = bootstrap_mean(directed, "normalized_gap_counts", seed + 1, reps)
    by_gamble = directed.groupby("gamble_id").agg(
        gap_probability=("normalized_gap_probability", "mean"),
        gap_counts=("normalized_gap_counts", "mean"),
    )
    positive_gambles = int(((by_gamble["gap_probability"] > 0) & (by_gamble["gap_counts"] > 0)).sum())
    capability_metrics = {
        "frequency_accuracy": float(frequency["correct"].mean()),
        "frequency_accuracy_by_presentation": {
            key: float(group["correct"].mean()) for key, group in frequency.groupby("presentation_mode")
        },
        "expected_value_accuracy": float(ev["correct"].mean()),
        "expected_value_accuracy_by_presentation": {
            key: float(group["correct"].mean()) for key, group in ev.groupby("presentation_mode")
        },
        "dominance_mean_target_probability": float(dominance["p_target"].mean()),
        "mean_option_order_difference": float(order_differences["difference"].mean()),
    }
    gates = contract["capability_gates"]
    capability_checks = {
        "frequency": capability_metrics["frequency_accuracy"] >= gates["minimum_frequency_accuracy"],
        "expected_value": capability_metrics["expected_value_accuracy"] >= gates["minimum_expected_value_accuracy"],
        "dominance": capability_metrics["dominance_mean_target_probability"] >= gates["minimum_dominance_target_probability"],
        "option_order": capability_metrics["mean_option_order_difference"] <= gates["maximum_mean_option_order_difference"],
    }
    effects = contract["effect_gates"]
    effect_checks = {
        "gap_vs_probability": gap_probability["mean"] >= effects["minimum_human_direction_gap_vs_probability"] and gap_probability["ci95"][0] > effects["bootstrap_ci_lower_must_exceed"],
        "gap_vs_counts": gap_counts["mean"] >= effects["minimum_human_direction_gap_vs_counts"] and gap_counts["ci95"][0] > effects["bootstrap_ci_lower_must_exceed"],
        "directed_gambles": positive_gambles >= effects["minimum_positive_directed_gambles"],
    }
    experience_choice = choice[choice["presentation_mode"] == EXPERIENCE]
    shuffle_std = experience_choice.groupby(["gamble_id", "scale", "option_order"])["p_target"].std()
    return {
        **capability_metrics,
        "capability_checks": capability_checks,
        "capability_pass": all(capability_checks.values()),
        "normalized_gap_vs_probability": gap_probability,
        "normalized_gap_vs_counts": gap_counts,
        "positive_directed_gambles": positive_gambles,
        "directed_gamble_gaps": by_gamble.to_dict(orient="index"),
        "mean_experience_shuffle_std": float(shuffle_std.mean()),
        "choice_target_probability_by_presentation": {
            key: float(group["p_target"].mean()) for key, group in choice.groupby("presentation_mode")
        },
        "effect_checks": effect_checks,
        "family_pass": all(capability_checks.values()) and all(effect_checks.values()),
    }


def load_validate(path: Path, contract: dict, family: str) -> pd.DataFrame:
    with path.open(encoding="utf-8") as handle:
        frame = pd.DataFrame(json.loads(line) for line in handle)
    specification = contract["models"][family]
    expected = contract["data"]["expected_records"]
    if len(frame) != expected or frame["item_id"].nunique() != expected:
        raise ValueError(f"{family}: incomplete or duplicate rows")
    if set(frame["contract_id"]) != {contract["contract_id"]}:
        raise ValueError(f"{family}: contract mismatch")
    if set(frame["model_id"]) != {specification["model_id"]} or set(frame["revision"]) != {specification["revision"]}:
        raise ValueError(f"{family}: checkpoint mismatch")
    return frame


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=ROOT / "results" / "d0")
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "d0_analysis.json")
    parser.add_argument("--summary-csv", type=Path, default=ROOT / "results" / "d0_summary.csv")
    args = parser.parse_args()
    contract = json.loads((ROOT / "configs" / "d0_contract.json").read_text())
    report = {"contract_id": contract["contract_id"], "families": {}}
    rows = []
    for family in contract["models"]:
        summary = summarize_family(load_validate(args.results_dir / f"{family}.jsonl", contract, family), contract)
        report["families"][family] = summary
        rows.append({
            "family": family,
            "frequency_accuracy": summary["frequency_accuracy"],
            "expected_value_accuracy": summary["expected_value_accuracy"],
            "dominance_p_target": summary["dominance_mean_target_probability"],
            "option_order_difference": summary["mean_option_order_difference"],
            "gap_vs_probability": summary["normalized_gap_vs_probability"]["mean"],
            "gap_vs_counts": summary["normalized_gap_vs_counts"]["mean"],
            "positive_directed_gambles": summary["positive_directed_gambles"],
            "family_pass": summary["family_pass"],
        })
    passes = sum(row["family_pass"] for row in rows)
    positive_families = sum(report["families"][family]["normalized_gap_vs_probability"]["mean"] > 0 for family in contract["models"])
    effect_gates = contract["effect_gates"]
    if passes >= effect_gates["minimum_family_passes_for_promotion"] and positive_families >= effect_gates["minimum_families_with_positive_direction"]:
        verdict = "PROMOTE_BEHAVIOR"
    elif not any(report["families"][family]["capability_pass"] for family in contract["models"]):
        verdict = "HOLD_CAPABILITY_FAILURE"
    elif positive_families < 2:
        verdict = "KILL_NO_EXACT_FREQUENCY_GAP"
    else:
        verdict = "HOLD_INCONCLUSIVE_D0"
    report["aggregate"] = {
        "family_passes": int(passes),
        "families_with_positive_human_direction_gap": int(positive_families),
        "verdict": verdict,
        "mechanism_authorized": verdict == "PROMOTE_BEHAVIOR",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    with args.summary_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(report["aggregate"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
