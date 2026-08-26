#!/usr/bin/env python3
"""Teacher-forced behavioral runner and family-level summary for V2."""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

from mechanism_behavior import HFScorer
from v2_data import action_for, dump_jsonl, load_jsonl


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return math.nan
    position = q * (len(ordered) - 1)
    low = int(math.floor(position))
    high = int(math.ceil(position))
    if low == high:
        return ordered[low]
    weight = position - low
    return ordered[low] * (1.0 - weight) + ordered[high] * weight


def deterministic_bootstrap(values: list[float], draws: int, seed: int) -> list[float]:
    import random

    rng = random.Random(seed)
    if not values:
        return [math.nan, math.nan]
    samples = []
    for _ in range(draws):
        samples.append(mean([values[rng.randrange(len(values))] for _ in values]))
    return [quantile(samples, 0.025), quantile(samples, 0.975)]


def run_posteriors(args: argparse.Namespace) -> dict:
    evidence = load_jsonl(args.evidence)
    if args.limit:
        evidence = evidence[: args.limit]
    scorer = HFScorer(args.model, dtype=args.dtype)
    candidates = tuple(f"{i / 100:.2f}" for i in range(101))
    scored = scorer.score_choices(
        [row["posterior_prompt"] for row in evidence],
        candidates,
        args.sequence_batch_size,
    )
    rows = []
    for row, result in zip(evidence, scored, strict=True):
        distribution = result["probabilities"]
        argmax_text = max(distribution, key=distribution.get)
        posterior_mean = sum(float(k) * v for k, v in distribution.items())
        rows.append(
            {
                **row,
                "model": args.model,
                "model_revision": args.model_revision,
                "posterior_mean": posterior_mean,
                "posterior_argmax": float(argmax_text),
                "posterior_peak_probability": distribution[argmax_text],
                "posterior_entropy": -sum(
                    value * math.log(max(value, 1e-45))
                    for value in distribution.values()
                ),
                "posterior_distribution": distribution,
            }
        )
    dump_jsonl(rows, args.out)
    return {
        "n": len(rows),
        "posterior_mean_mae": mean(
            [abs(row["posterior_mean"] - row["gold_p_a"]) for row in rows]
        ),
        "posterior_argmax_mae": mean(
            [abs(row["posterior_argmax"] - row["gold_p_a"]) for row in rows]
        ),
        "out": str(args.out),
    }


def run_factorial(args: argparse.Namespace) -> dict:
    rows = load_jsonl(args.dataset)
    group_ids = sorted({f"{row['family_id']}::{row['surface_id']}" for row in rows})
    selected = {
        group
        for index, group in enumerate(group_ids)
        if index % args.num_shards == args.shard_index
    }
    rows = [
        row
        for row in rows
        if f"{row['family_id']}::{row['surface_id']}" in selected
    ]
    if args.limit_groups:
        keep = set(sorted(selected)[: args.limit_groups])
        rows = [
            row
            for row in rows
            if f"{row['family_id']}::{row['surface_id']}" in keep
        ]
    posterior_rows = load_jsonl(args.posteriors)
    posterior = {
        row["evidence_surface_id"]: row for row in posterior_rows
    }
    scorer = HFScorer(args.model, dtype=args.dtype)
    scored = scorer.score_choices(
        [row["prompt"] for row in rows],
        ("A", "B"),
        args.sequence_batch_size,
    )
    for row, result in zip(rows, scored, strict=True):
        scores = result["log_scores"]
        probabilities = result["probabilities"]
        mapping = row["option_mapping"]
        act_label = "A" if mapping[0] == "ACT" else "B"
        wait_label = "B" if act_label == "A" else "A"
        row["model"] = args.model
        row["model_revision"] = args.model_revision
        row["label_log_scores"] = scores
        row["label_probs"] = probabilities
        row["semantic_logit"] = scores[act_label] - scores[wait_label]
        row["pred_label"] = max(probabilities, key=probabilities.get)
        row["pred_action"] = mapping[0] if row["pred_label"] == "A" else mapping[1]
        row["condition_correct"] = row["pred_action"] == row["condition_action"]
        p_row = posterior[f"{row['evidence_id']}::{row['observation_order']}"]
        row["posterior_mean"] = p_row["posterior_mean"]
        row["posterior_argmax"] = p_row["posterior_argmax"]
        max_error = args.inference_good_max_abs_error
        row["inference_good"] = (
            abs(p_row["posterior_mean"] - row["gold_p_a"]) <= max_error
            and action_for(p_row["posterior_mean"], row["threshold"])
            == row["evidence_action"]
        )
    dump_jsonl(rows, args.out)
    return {
        "shard_index": args.shard_index,
        "num_shards": args.num_shards,
        "n_groups": len(
            {f"{row['family_id']}::{row['surface_id']}" for row in rows}
        ),
        "n_rows": len(rows),
        "out": str(args.out),
    }


def merge(inputs: list[Path], out: Path) -> dict:
    rows = []
    for path in inputs:
        rows.extend(load_jsonl(path))
    if len(rows) != len({row["variant_id"] for row in rows}):
        raise ValueError("duplicate variant_id")
    rows.sort(key=lambda row: row["variant_id"])
    dump_jsonl(rows, out)
    return {"n": len(rows), "out": str(out)}


def summarize(rows: list[dict], bootstrap_draws: int, seed: int) -> dict:
    by_group: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        by_group[(row["family_id"], row["surface_id"])].append(row)
    group_effects = []
    for (family_id, surface_id), group in sorted(by_group.items()):
        index = {
            (row["condition"], row["value_side"]): row for row in group
        }
        required = {
            (condition, side)
            for condition in (
                "posterior_use",
                "posterior_ignore",
                "generic_use",
                "generic_ignore",
            )
            for side in ("low", "high")
        }
        if set(index) != required:
            raise ValueError((family_id, surface_id, set(index)))
        g_posterior = (
            index[("posterior_use", "high")]["semantic_logit"]
            - index[("posterior_use", "low")]["semantic_logit"]
            - index[("posterior_ignore", "high")]["semantic_logit"]
            + index[("posterior_ignore", "low")]["semantic_logit"]
        )
        g_generic = (
            index[("generic_use", "high")]["semantic_logit"]
            - index[("generic_use", "low")]["semantic_logit"]
            - index[("generic_ignore", "high")]["semantic_logit"]
            + index[("generic_ignore", "low")]["semantic_logit"]
        )
        group_effects.append(
            {
                "family_id": family_id,
                "surface_id": surface_id,
                "G_posterior": g_posterior,
                "G_generic_control": g_generic,
                "G_specific": g_posterior - g_generic,
                "inference_good": all(row["inference_good"] for row in group),
            }
        )
    by_family: dict[str, list[dict]] = defaultdict(list)
    for row in group_effects:
        by_family[row["family_id"]].append(row)
    family_effects = []
    for family_id, group in sorted(by_family.items()):
        family_effects.append(
            {
                "family_id": family_id,
                "n_surfaces": len(group),
                "G_posterior": mean([row["G_posterior"] for row in group]),
                "G_generic_control": mean(
                    [row["G_generic_control"] for row in group]
                ),
                "G_specific": mean([row["G_specific"] for row in group]),
                "inference_good": all(row["inference_good"] for row in group),
            }
        )
    condition_groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        condition_groups[row["condition"]].append(row)
    condition_summary = {
        condition: {
            "n": len(group),
            "accuracy": mean([float(row["condition_correct"]) for row in group]),
            "mean_semantic_logit": mean([row["semantic_logit"] for row in group]),
        }
        for condition, group in sorted(condition_groups.items())
    }
    effects = {}
    for key in ("G_posterior", "G_generic_control", "G_specific"):
        values = [row[key] for row in family_effects]
        effects[key] = {
            "mean": mean(values),
            "family_bootstrap_95ci": deterministic_bootstrap(
                values, bootstrap_draws, seed
            ),
            "positive_family_fraction": mean([float(value > 0) for value in values]),
        }
    inference_good = [row for row in family_effects if row["inference_good"]]
    return {
        "evidence_class": "D1-development"
        if rows and rows[0]["split"] == "d1"
        else rows[0]["split"] if rows else None,
        "n_rows": len(rows),
        "n_family_surface_groups": len(group_effects),
        "n_families": len(family_effects),
        "n_inference_good_families": len(inference_good),
        "conditions": condition_summary,
        "family_first_effects": effects,
        "inference_good_effects": {
            key: mean([row[key] for row in inference_good])
            for key in ("G_posterior", "G_generic_control", "G_specific")
        },
        "family_effects": family_effects,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    post = sub.add_parser("posteriors")
    post.add_argument("--model", required=True)
    post.add_argument("--model-revision", required=True)
    post.add_argument("--evidence", type=Path, required=True)
    post.add_argument("--out", type=Path, required=True)
    post.add_argument("--dtype", default="bfloat16")
    post.add_argument("--sequence-batch-size", type=int, default=32)
    post.add_argument("--limit", type=int)

    factorial = sub.add_parser("factorial")
    factorial.add_argument("--model", required=True)
    factorial.add_argument("--model-revision", required=True)
    factorial.add_argument("--dataset", type=Path, required=True)
    factorial.add_argument("--posteriors", type=Path, required=True)
    factorial.add_argument("--out", type=Path, required=True)
    factorial.add_argument("--dtype", default="bfloat16")
    factorial.add_argument("--sequence-batch-size", type=int, default=64)
    factorial.add_argument("--shard-index", type=int, default=0)
    factorial.add_argument("--num-shards", type=int, default=1)
    factorial.add_argument("--limit-groups", type=int)
    factorial.add_argument("--inference-good-max-abs-error", type=float, default=0.10)

    merger = sub.add_parser("merge")
    merger.add_argument("--inputs", type=Path, nargs="+", required=True)
    merger.add_argument("--out", type=Path, required=True)

    summary = sub.add_parser("summarize")
    summary.add_argument("--results", type=Path, required=True)
    summary.add_argument("--out", type=Path, required=True)
    summary.add_argument("--bootstrap-draws", type=int, default=10_000)
    summary.add_argument("--seed", type=int, default=6001)

    args = parser.parse_args()
    if args.command == "posteriors":
        result = run_posteriors(args)
    elif args.command == "factorial":
        result = run_factorial(args)
    elif args.command == "merge":
        result = merge(args.inputs, args.out)
    else:
        result = summarize(load_jsonl(args.results), args.bootstrap_draws, args.seed)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
