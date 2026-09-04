"""Audit the exact overlapping Llama checkpoint in the two mother releases."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path


RATING_RE = re.compile(r"Final Rating:\s*([1-7])", re.I)


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--source-root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    ana = args.source_root / "anaphora"
    pre = args.source_root / "presupposition"
    commits = {
        "anaphora": subprocess.check_output(["git", "-C", str(ana), "rev-parse", "HEAD"], text=True).strip(),
        "presupposition": subprocess.check_output(["git", "-C", str(pre), "rev-parse", "HEAD"], text=True).strip(),
    }
    if commits["anaphora"] != config["anaphora_commit"] or commits["presupposition"] != config["presupposition_commit"]:
        raise ValueError(f"Source commit mismatch: {commits}")
    with (ana / config["anaphora_file"]).open() as f:
        anaphora = list(csv.DictReader(f))
    by_comp = defaultdict(list)
    for row in anaphora:
        by_comp[row["comp"]].append(row)
    ana_summary = {
        comp: {"n": len(rows), "accuracy": mean([int(x["correct"]) for x in rows]),
               "mean_effect_size": mean([float(x["effect_size"]) for x in rows])}
        for comp, rows in sorted(by_comp.items())
    }
    presupp = json.loads((pre / config["presupposition_file"]).read_text())
    ratings = defaultdict(list)
    exclusions = []
    for row in presupp:
        matches = RATING_RE.findall(row["response"])
        if not matches:
            exclusions.append(row["id"])
            continue
        ratings[row["probability"]].append(int(matches[-1]))
    pre_summary = {band: {"n": len(xs), "mean_rating": mean(xs)} for band, xs in sorted(ratings.items())}
    ana_effect = mean([float(x["effect_size"]) for x in anaphora])
    ana_nontrivial = 0.05 < mean([int(x["correct"]) for x in anaphora]) < 0.95 and abs(ana_effect) > 0
    pre_ordered = pre_summary["high"]["mean_rating"] > pre_summary["low"]["mean_rating"]
    result = {
        "checkpoint": config["checkpoint"], "source_commits": commits,
        "anaphora": {"n": len(anaphora), "overall_accuracy": mean([int(x["correct"]) for x in anaphora]),
                     "overall_mean_effect": ana_effect, "by_comparison": ana_summary},
        "presupposition": {"n": len(presupp), "parsed_n": sum(len(x) for x in ratings.values()),
                           "excluded_ids": exclusions, "by_gold_band": pre_summary},
        "behavior_denominator_pass": bool(ana_nontrivial and pre_ordered),
        "scientific_limit": "Two within-task behavioral effects do not imply a shared causal dynamic-context state.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
