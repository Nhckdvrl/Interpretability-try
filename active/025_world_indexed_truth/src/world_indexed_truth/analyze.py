"""Adjudicate the frozen four-family world-indexed capability experiment."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]


def accuracy(frame: pd.DataFrame) -> float:
    return float(frame["correct"].mean())


def joint_frame(frame: pd.DataFrame) -> pd.DataFrame:
    counts = frame.groupby("context_id")["query_world"].nunique()
    if not (counts == 2).all():
        raise ValueError("every context must have actual and local queries")
    joint = frame.groupby("context_id", as_index=False).agg(
        joint_correct=("correct", "all"),
        local_relation=("local_relation", "first"),
        actual_truth=("actual_truth", "first"),
        domain=("domain", "first"),
        world_frame=("world_frame", "first"),
    )
    return joint


def minimum_group_accuracy(frame: pd.DataFrame, column: str, target: str) -> tuple[float, dict[str, float]]:
    selected = frame[frame["local_relation"] == target]
    values = {str(key): float(group["joint_correct"].mean()) for key, group in selected.groupby(column)}
    return min(values.values()), values


def summarize_family(frame: pd.DataFrame, gates: dict) -> dict:
    joint = joint_frame(frame)
    relation_joint = {
        key: float(group["joint_correct"].mean()) for key, group in joint.groupby("local_relation")
    }
    polarity_min, polarity = minimum_group_accuracy(joint, "actual_truth", "conflict")
    domain_min, domains = minimum_group_accuracy(joint, "domain", "conflict")
    frame_min, frames = minimum_group_accuracy(joint, "world_frame", "conflict")
    paraphrases = {
        key: accuracy(group) for key, group in frame.groupby("query_paraphrase")
    }
    paraphrase_min = min(paraphrases.values())
    metrics = {
        "query_accuracy": accuracy(frame),
        "query_accuracy_by_world": {
            key: accuracy(group) for key, group in frame.groupby("query_world")
        },
        "overall_joint_accuracy": float(joint["joint_correct"].mean()),
        "joint_accuracy_by_relation": relation_joint,
        "conflict_joint_accuracy_by_actual_truth": polarity,
        "conflict_joint_accuracy_by_domain": domains,
        "conflict_joint_accuracy_by_world_frame": frames,
        "query_accuracy_by_paraphrase": paraphrases,
        "minimum_conflict_polarity_joint_accuracy": polarity_min,
        "minimum_conflict_domain_joint_accuracy": domain_min,
        "minimum_conflict_world_frame_joint_accuracy": frame_min,
        "minimum_query_paraphrase_accuracy": paraphrase_min,
    }
    checks = {
        "overall_joint": metrics["overall_joint_accuracy"] >= gates["minimum_overall_joint_accuracy"],
        "conflict_joint": relation_joint["conflict"] >= gates["minimum_conflict_joint_accuracy"],
        "aligned_joint": relation_joint["aligned"] >= gates["minimum_aligned_joint_accuracy"],
        "conflict_polarities": polarity_min >= gates["minimum_each_conflict_polarity_joint_accuracy"],
        "conflict_domains": domain_min >= gates["minimum_each_domain_conflict_joint_accuracy"],
        "conflict_world_frames": frame_min >= gates["minimum_each_world_frame_conflict_joint_accuracy"],
        "query_paraphrases": paraphrase_min >= gates["minimum_each_query_paraphrase_accuracy"],
    }
    return {**metrics, "gate_checks": checks, "family_pass": all(checks.values())}


def load_and_validate(path: Path, contract: dict, family: str) -> pd.DataFrame:
    with path.open(encoding="utf-8") as handle:
        frame = pd.DataFrame(json.loads(line) for line in handle)
    expected = contract["models"][family]
    if len(frame) != 256 or frame["item_id"].nunique() != 256:
        raise ValueError(f"{family}: incomplete or duplicate result rows")
    if set(frame["contract_id"]) != {contract["contract_id"]}:
        raise ValueError(f"{family}: contract mismatch")
    if set(frame["model_id"]) != {expected["model_id"]} or set(frame["revision"]) != {expected["revision"]}:
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
        frame = load_and_validate(args.results_dir / f"{family}.jsonl", contract, family)
        summary = summarize_family(frame, contract["family_gates"])
        report["families"][family] = summary
        rows.append({
            "family": family,
            "query_accuracy": summary["query_accuracy"],
            "overall_joint_accuracy": summary["overall_joint_accuracy"],
            "conflict_joint_accuracy": summary["joint_accuracy_by_relation"]["conflict"],
            "aligned_joint_accuracy": summary["joint_accuracy_by_relation"]["aligned"],
            "family_pass": summary["family_pass"],
        })
    passes = sum(row["family_pass"] for row in rows)
    median_conflict = float(np.median([row["conflict_joint_accuracy"] for row in rows]))
    rule = contract["aggregate_rule"]
    if passes >= rule["promote_behavior_minimum_family_passes"] and median_conflict >= rule["promote_behavior_minimum_median_conflict_joint_accuracy"]:
        verdict = "PROMOTE_BEHAVIOR"
    elif passes >= rule["limited_evidence_minimum_family_passes"] and median_conflict >= rule["limited_evidence_minimum_median_conflict_joint_accuracy"]:
        verdict = "HOLD_LIMITED_CROSS_FAMILY_EVIDENCE"
    else:
        verdict = "HOLD_PREREQUISITE_CAPABILITY"
    report["aggregate"] = {
        "family_passes": int(passes),
        "median_conflict_joint_accuracy": median_conflict,
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
