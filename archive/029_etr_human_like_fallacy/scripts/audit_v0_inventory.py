#!/usr/bin/env python3
"""Audit whether public ETR artifacts expose the paper's exact 383-item set."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from pathlib import Path


def line_count(path: Path) -> int:
    with path.open(encoding="utf-8", errors="replace") as handle:
        return sum(1 for line in handle if line.strip())


def audit(generator: Path) -> dict:
    datasets = []
    for path in sorted(generator.rglob("*.jsonl")):
        if "/.git/" in str(path):
            continue
        count = line_count(path)
        if count in {372, 383, 400} and "samples_" not in path.name:
            datasets.append({"path": str(path.relative_to(generator)), "rows": count})

    result_csv = generator / "lm_eval/tasks/etr_problems/good_results/all_results.csv"
    reverse_csv = generator / "lm_eval/tasks/etr_problems/good_results/reverse_all_results.csv"
    csv_summaries = {}
    for label, path in (("forward", result_csv), ("reverse", reverse_csv)):
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        csv_summaries[label] = {
            "rows": len(rows),
            "unique_doc_ids": len({row["doc_id"] for row in rows}),
            "models": len({row["model_name"] for row in rows}),
        }

    commit = subprocess.check_output(
        ["git", "-C", str(generator), "rev-parse", "HEAD"], text=True
    ).strip()
    exact_candidates = [row for row in datasets if row["rows"] == 383]
    return {
        "schema_version": 1,
        "generator_commit": commit,
        "paper_initial_population": 400,
        "paper_excluded_after_integrity_checks": 17,
        "paper_final_population": 383,
        "candidate_datasets": datasets,
        "public_result_tables": csv_summaries,
        "exact_383_candidates": exact_candidates,
        "exact_manifest_present": bool(exact_candidates),
        "status": "READY" if exact_candidates else "MISSING_EXACT_383_MANIFEST",
        "warning": "Commit c177357 marks the historical datasets invalid after a view_to_smt bug.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generator", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.generator)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
