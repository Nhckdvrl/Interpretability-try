"""Analyze capability, dual-candidate coverage, asymmetry and order sensitivity."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--inputs", type=Path, nargs="+", required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    summaries = []
    for path in args.inputs:
        lines = [json.loads(x) for x in path.read_text().splitlines() if x]
        meta = next(x for x in lines if x["record_type"] == "metadata")
        rows = [x for x in lines if x["record_type"] == "example"]
        clear = [r for r in rows if r["split"] == "clear_ref"]
        shared = [r for r in rows if r["split"] == "shared_ref"]
        clear_correct = []
        for r in clear:
            clear_correct.append(r["prediction"] == r["positive_candidates"][0])
        coverage, asymmetries, preferred_positions = [], [], []
        by_semantic = defaultdict(list)
        for r in shared:
            scores = {k: v["logprob"] for k, v in r["scores"].items()}
            pos = r["positive_candidates"]
            neg = r["negative_candidate"]
            coverage.append(min(scores[pos[0]], scores[pos[1]]) > scores[neg])
            asymmetries.append(abs(scores[pos[0]] - scores[pos[1]]))
            preferred = pos[0] if scores[pos[0]] >= scores[pos[1]] else pos[1]
            ordered_entities = [x for x in r["candidates"] if x in r["conversation"][0]["content"]]
            mention_text = " ".join(turn["content"] for turn in r["conversation"][:2])
            positions = sorted([(mention_text.lower().find(x.lower()), x) for x in pos])
            preferred_positions.append(next(i for i, (_, x) in enumerate(positions) if x == preferred))
            by_semantic[r["semantic_id"]].append(preferred)
        flips = []
        for prefs in by_semantic.values():
            flips.append(len(set(prefs)) > 1)
        clear_acc = mean(clear_correct)
        coverage_rate = mean(coverage)
        gate = clear_acc >= config["gate"]["min_clearref_accuracy"] and coverage_rate >= config["gate"]["min_sharedref_both_over_distractor_rate"]
        summaries.append({
            "model": meta["model_checkpoint"],
            "model_revision": meta["model_revision"],
            "n_clearref": len(clear),
            "n_sharedref": len(shared),
            "clearref_accuracy": clear_acc,
            "sharedref_both_licensed_over_distractor_rate": coverage_rate,
            "sharedref_mean_abs_candidate_margin": mean(asymmetries),
            "sharedref_preferred_mention_position": dict(Counter(preferred_positions)),
            "semantic_items_with_preference_flip_across_permutations": mean(flips),
            "gate_pass": gate,
            "scope_note": "Behavioral candidate scores do not identify H1 versus H2.",
        })
    result = {"contract": "038 cheap capability and candidate-coverage denominator", "models": summaries,
              "panel_gate_pass": len(summaries) >= 2 and all(x["gate_pass"] for x in summaries)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
