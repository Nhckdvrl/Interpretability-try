"""Audit PMBench's frozen scenario and released model-level summary."""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path


def pct(text: str) -> float:
    return float(text.rstrip("%")) / 100.0


def parse_monitoring_categories(report: Path) -> dict[str, dict[str, float | int]]:
    """Read the scorer's prespecified monitoring-demand partition."""
    lines = report.read_text().splitlines()
    start = lines.index("## Monitoring Categories")
    result = {}
    for line in lines[start + 4 :]:
        if not line.startswith("|"):
            if result:
                break
            continue
        fields = [x.strip() for x in line.strip("|").split("|")]
        if len(fields) != 7 or fields[0] not in {
            "no_proactive_monitoring", "proactive_monitoring_required"
        }:
            continue
        result[fields[0]] = {
            "hit": int(fields[1]), "late": int(fields[2]), "miss": int(fields[3]),
            "total": int(fields[4]), "hit_rate": pct(fields[5]), "any_rate": pct(fields[6]),
        }
    if set(result) != {"no_proactive_monitoring", "proactive_monitoring_required"}:
        raise ValueError(f"Missing monitoring categories in {report}")
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--source-root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    repo = args.source_root / "pmbench"
    commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    if commit != config["source_commit"]:
        raise ValueError(f"Source commit changed: {commit}")
    scenario = json.loads((repo / "data" / "synthetic_week_v9.json").read_text())
    task_cells = Counter()
    total_tasks = 0
    for day in scenario["days"]:
        for task in day["tasks"]:
            total_tasks += 1
            visibility = "hidden_channel" if task.get("cue_channel") else ("time" if task["type"] == "time" else "visible_event")
            task_cells[(task["type"], "regular" if task.get("regular") else "irregular", visibility)] += 1

    lines = (repo / "runs" / "all_results_v9" / "experiment_output_comparison_report.md").read_text().splitlines()
    rows = []
    for line in lines:
        if not line.startswith("|"):
            continue
        fields = [x.strip() for x in line.strip("|").split("|")]
        if len(fields) != 15 or fields[0] not in config["models"] or fields[1] not in config["setups"]:
            continue
        rows.append({
            "model": fields[0], "setup": fields[1], "run_type": fields[2],
            "tp": int(fields[3]), "fp": int(fields[4]), "fn": int(fields[5]),
            "set_precision": pct(fields[6]), "set_recall": pct(fields[7]),
            "micro_set_f1": pct(fields[8]), "hit_rate": pct(fields[9]), "exact_set_match": pct(fields[10]),
            "state_queries": int(fields[11]), "check_time_actions": int(fields[12]),
            "actions": int(fields[13]), "duration": fields[14],
        })
    baseline = {r["model"]: r for r in rows if r["setup"] == "single-baseline"}
    gate = all(config["nonfloor_set_f1"] < baseline[m]["micro_set_f1"] < config["nonceiling_set_f1"] for m in config["models"])
    artifact_dirs = {
        "Qwen3-8B": "qwen3-8b",
        "Llama 3.3 70B Instruct": "llama-33-70b-instruct",
        "Mistral Small 3.2 24B Instruct": "mistral-small-32-24b-instruct",
    }
    monitoring_rows = []
    run_root = repo / "runs" / "all_results_v9"
    for model in config["models"]:
        for setup in config["setups"]:
            reports = list((run_root / artifact_dirs[model]).glob(f"{setup}-*/*.score.md"))
            if len(reports) != 1:
                raise ValueError(f"Expected one score report for {model}/{setup}, got {reports}")
            categories = parse_monitoring_categories(reports[0])
            monitoring_rows.append({
                "model": model,
                "setup": setup,
                "categories": categories,
                "demand_gap": (
                    categories["no_proactive_monitoring"]["hit_rate"]
                    - categories["proactive_monitoring_required"]["hit_rate"]
                ),
            })
    result = {
        "source_commit": commit,
        "scenario": scenario["scenario_name"],
        "total_tasks": total_tasks,
        "task_cells": [{"type": k[0], "regularity": k[1], "visibility": k[2], "n": v} for k, v in sorted(task_cells.items())],
        "released_rows": rows,
        "monitoring_demand_rows": monitoring_rows,
        "behavior_denominator_pass": gate,
        "scientific_limit": (
            "Released heartbeat effects do not identify native strategic monitoring: heartbeat text changes "
            "the model's current input and may itself trigger retrieval. The scorer's monitoring-demand "
            "partition is descriptive because cue visibility/channel and monitoring demand are not matched."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
