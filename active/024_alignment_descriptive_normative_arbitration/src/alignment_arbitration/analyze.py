"""Analyze the frozen 024 D0 mother-reproduction experiment."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]


def correlation(frame: pd.DataFrame) -> float:
    if frame["p_f"].nunique() < 2 or frame["target_f"].nunique() < 2:
        return float("nan")
    return float(frame["p_f"].corr(frame["target_f"]))


def summarize(frame: pd.DataFrame) -> dict:
    return {
        "n": int(len(frame)),
        "n_participants": int(frame["participant_id"].nunique()),
        "r": correlation(frame),
        "brier": float(np.mean((frame["p_f"] - frame["target_f"]) ** 2)),
        "mean_decision_mass": float(frame["decision_mass"].mean()),
        "mean_p_f": float(frame["p_f"].mean()),
    }


def cluster_bootstrap_delta(base: pd.DataFrame, aligned: pd.DataFrame, seed: int, replicates: int) -> dict:
    merged = base[["item_id", "participant_id", "target_f", "p_f"]].merge(
        aligned[["item_id", "p_f"]], on="item_id", suffixes=("_base", "_aligned"), validate="one_to_one"
    )
    participants = np.array(sorted(merged["participant_id"].unique()))
    by_participant = {pid: merged[merged["participant_id"] == pid] for pid in participants}
    rng = np.random.default_rng(seed)
    deltas = []
    for _ in range(replicates):
        sampled = rng.choice(participants, size=len(participants), replace=True)
        boot = pd.concat([by_participant[pid] for pid in sampled], ignore_index=True)
        r_base = boot["p_f_base"].corr(boot["target_f"])
        r_aligned = boot["p_f_aligned"].corr(boot["target_f"])
        deltas.append(float(r_base - r_aligned))
    point = float(merged["p_f_base"].corr(merged["target_f"]) - merged["p_f_aligned"].corr(merged["target_f"]))
    return {
        "delta_r": point,
        "ci95": [float(np.quantile(deltas, 0.025)), float(np.quantile(deltas, 0.975))],
        "bootstrap_replicates": replicates,
    }


def load_result(path: Path) -> pd.DataFrame:
    with path.open(encoding="utf-8") as handle:
        return pd.DataFrame(json.loads(line) for line in handle)


def validate_result(frame: pd.DataFrame, contract: dict, family: str, role: str) -> None:
    expected_model = contract["models"][family][role]
    expected_formats = {"plain"} if role == "base" else {"native", "plain"}
    if set(frame["contract_id"]) != {contract["contract_id"]}:
        raise ValueError(f"{family}/{role}: contract mismatch")
    if set(frame["model_id"]) != {expected_model}:
        raise ValueError(f"{family}/{role}: model mismatch")
    if set(frame["format"]) != expected_formats:
        raise ValueError(f"{family}/{role}: format mismatch")
    counts = frame.groupby("format")["item_id"].nunique().to_dict()
    if counts != {prompt_format: 3870 for prompt_format in expected_formats}:
        raise ValueError(f"{family}/{role}: incomplete item counts {counts}")
    if frame.duplicated(["format", "item_id"]).any():
        raise ValueError(f"{family}/{role}: duplicate format/item rows")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=ROOT / "results" / "d0")
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "d0_analysis.json")
    parser.add_argument("--summary-csv", type=Path, default=ROOT / "results" / "d0_summary.csv")
    args = parser.parse_args()

    contract = json.loads((ROOT / "configs" / "d0_contract.json").read_text())
    gates = contract["quality_gates"]
    seed = contract["randomness"]["bootstrap_seed"]
    reps = contract["randomness"]["bootstrap_replicates"]
    report = {"contract_id": contract["contract_id"], "families": {}}

    native_deltas, plain_deltas = [], []
    native_passes, mass_passes = 0, 0
    summary_rows = []
    for family in contract["models"]:
        base_all = load_result(args.results_dir / f"{family}_base.jsonl")
        aligned_all = load_result(args.results_dir / f"{family}_aligned.jsonl")
        validate_result(base_all, contract, family, "base")
        validate_result(aligned_all, contract, family, "aligned")
        family_report = {"comparisons": {}}
        for comparison, aligned_format in [("native", "native"), ("shared_plain", "plain")]:
            base = base_all[(base_all["format"] == "plain") & (base_all["round"] > 1)].copy()
            aligned = aligned_all[(aligned_all["format"] == aligned_format) & (aligned_all["round"] > 1)].copy()
            base_summary, aligned_summary = summarize(base), summarize(aligned)
            bootstrap = cluster_bootstrap_delta(base, aligned, seed, reps)
            mass_ok = min(base_summary["mean_decision_mass"], aligned_summary["mean_decision_mass"]) >= gates[
                "minimum_mean_decision_mass_each_checkpoint"
            ]
            informative = max(base_summary["r"], aligned_summary["r"]) >= gates[
                "minimum_informative_correlation_either_checkpoint"
            ]
            passed = (
                mass_ok
                and informative
                and bootstrap["delta_r"] >= gates["family_effect_minimum_r"]
                and bootstrap["ci95"][0] > 0
            )
            game_summaries = {}
            for game in ["PD", "BoS"]:
                b_game, a_game = base[base["game"] == game], aligned[aligned["game"] == game]
                game_summaries[game] = {
                    "base": summarize(b_game),
                    "aligned": summarize(a_game),
                    "delta_r": correlation(b_game) - correlation(a_game),
                }
            pd_base = base[base["game"] == "PD"]
            pd_aligned = aligned[aligned["game"] == "PD"]
            family_report["comparisons"][comparison] = {
                "base": base_summary,
                "aligned": aligned_summary,
                **bootstrap,
                "mass_gate": bool(mass_ok),
                "informative_gate": bool(informative),
                "family_pass": bool(passed),
                "games": game_summaries,
                "pd_normative_distance": {
                    "base_mean_1_minus_p_f": float((1 - pd_base["p_f"]).mean()),
                    "aligned_mean_1_minus_p_f": float((1 - pd_aligned["p_f"]).mean()),
                },
            }
            summary_rows.append(
                {
                    "family": family,
                    "comparison": comparison,
                    "base_r": base_summary["r"],
                    "aligned_r": aligned_summary["r"],
                    "delta_r": bootstrap["delta_r"],
                    "ci95_low": bootstrap["ci95"][0],
                    "ci95_high": bootstrap["ci95"][1],
                    "base_mass": base_summary["mean_decision_mass"],
                    "aligned_mass": aligned_summary["mean_decision_mass"],
                    "mass_gate": mass_ok,
                    "informative_gate": informative,
                    "family_pass": passed,
                }
            )
            if comparison == "native":
                native_deltas.append(bootstrap["delta_r"])
                native_passes += int(passed)
                mass_passes += int(mass_ok)
            else:
                plain_deltas.append(bootstrap["delta_r"])

        round_trajectory = {}
        for round_index in range(1, 11):
            base_round = base_all[(base_all["format"] == "plain") & (base_all["round"] == round_index)]
            aligned_round = aligned_all[(aligned_all["format"] == "native") & (aligned_all["round"] == round_index)]
            round_trajectory[str(round_index)] = {
                "base": summarize(base_round),
                "aligned": summarize(aligned_round),
            }
        family_report["native_round_trajectory"] = round_trajectory
        report["families"][family] = family_report

    if mass_passes < 3:
        verdict = "HOLD_LOW_DECISION_MASS"
    elif native_passes >= 3 and float(np.median(native_deltas)) >= 0.05 and sum(d > 0 for d in plain_deltas) >= 3:
        verdict = "PROMOTE_BEHAVIOR"
    elif sum(d > 0 for d in native_deltas) < 2 or float(np.median(native_deltas)) <= 0:
        verdict = "KILL_MOTHER_NOT_REPRODUCED"
    else:
        verdict = "HOLD_INCONCLUSIVE_D0"
    report["aggregate"] = {
        "native_family_passes": native_passes,
        "native_mass_passes": mass_passes,
        "native_delta_r": native_deltas,
        "native_median_delta_r": float(np.median(native_deltas)),
        "shared_plain_positive_families": int(sum(d > 0 for d in plain_deltas)),
        "shared_plain_delta_r": plain_deltas,
        "verdict": verdict,
        "mechanism_authorized": verdict == "PROMOTE_BEHAVIOR",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    with args.summary_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(summary_rows)
    print(json.dumps(report["aggregate"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
