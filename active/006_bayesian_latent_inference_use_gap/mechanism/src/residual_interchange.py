#!/usr/bin/env python3
"""Natural whole-residual interchange on the project-006 mechanism corpus."""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

from activation_cache import ANCHORS, token_anchor_positions
from mechanism_behavior import HFScorer, chat_prefix
from mechanism_data import dump_jsonl, load_jsonl


def pair_key(row: dict) -> tuple:
    return row["surface_id"], row["threshold"], row["condition"]


def causal_value(row: dict) -> float:
    if row["condition"] == "self_mean_bridge":
        return row["posterior_mean"]
    if row["condition"] == "self_argmax_bridge":
        return row["posterior_argmax"]
    return row["gold_p_a"]


def causal_action(row: dict) -> str:
    return row["condition_action"] if row["condition"] != "direct" else row["gold_action"]


def baseline_correct(row: dict) -> bool:
    return row["gold_correct"] if row["condition"] == "direct" else row["condition_correct"]


def token_patch_positions(tokenizer, prefix: str, row: dict, anchor: str, span: str) -> list[int]:
    if span == "single":
        return [
            token_anchor_positions(tokenizer, prefix, row["prompt"], row["threshold"])[
                anchor
            ]
        ]

    prompt = row["prompt"]
    prompt_start = prefix.index(prompt)
    if span == "belief_number":
        marker = "use the posterior value P(A | observations)="
        if marker not in prompt:
            raise ValueError("belief_number span requires a bridge prompt")
        start = prompt.index(marker) + len(marker)
        end = prompt.index(". A fixed policy", start)
    elif span == "belief_statement":
        marker = "For this decision, use the posterior value"
        if marker not in prompt:
            raise ValueError("belief_statement span requires a bridge prompt")
        start = prompt.index(marker)
        end = prompt.index(" A fixed policy", start)
    elif span == "evidence_statement":
        start = prompt.index("Observed counts:")
        end = prompt.index(".", start) + 1
    else:
        raise ValueError(f"unknown patch span: {span}")

    absolute_start = prompt_start + start
    absolute_end = prompt_start + end
    offsets = tokenizer(
        prefix, add_special_tokens=False, return_offsets_mapping=True
    )["offset_mapping"]
    positions = [
        i
        for i, (token_start, token_end) in enumerate(offsets)
        if token_end > absolute_start and token_start < absolute_end
    ]
    if not positions:
        raise ValueError((span, absolute_start, absolute_end))
    return positions


def build_pairs(rows: list[dict], max_per_type: int) -> list[dict]:
    by_context: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        by_context[pair_key(row)].append(row)

    pair_lists: dict[str, list[dict]] = defaultdict(list)
    for context, group in sorted(by_context.items()):
        act = [row for row in group if causal_action(row) == "ACT"]
        wait = [row for row in group if causal_action(row) == "WAIT"]
        # Matched crossing donors, both directions.
        for receiver_group, donor_group in ((act, wait), (wait, act)):
            if not receiver_group or not donor_group:
                continue
            for receiver in receiver_group:
                donor = min(
                    donor_group,
                    key=lambda row: (
                        abs(
                            abs(causal_value(row) - row["threshold"])
                            - abs(causal_value(receiver) - receiver["threshold"])
                        ),
                        row["variant_id"],
                    ),
                )
                pair_lists["posterior_crossing"].append(
                    {"receiver": receiver, "donor": donor}
                )

        # Same-posterior, different decomposition placebo.
        by_posterior: dict[float, list[dict]] = defaultdict(list)
        for row in group:
            by_posterior[round(causal_value(row), 12)].append(row)
        for same_group in by_posterior.values():
            same_group.sort(key=lambda row: row["variant_id"])
            if len(same_group) >= 2:
                for i, receiver in enumerate(same_group):
                    donor = same_group[(i + 1) % len(same_group)]
                    if donor["evidence_id"] != receiver["evidence_id"]:
                        pair_lists["posterior_equivalent"].append(
                            {"receiver": receiver, "donor": donor}
                        )

        # Different posterior but no action crossing: graded/selectivity control.
        for action_group in (act, wait):
            action_group = sorted(action_group, key=causal_value)
            if len(action_group) >= 2:
                pair_lists["posterior_noncrossing"].append(
                    {"receiver": action_group[0], "donor": action_group[-1]}
                )
                pair_lists["posterior_noncrossing"].append(
                    {"receiver": action_group[-1], "donor": action_group[0]}
                )

    selected = []
    for pair_type in (
        "posterior_crossing",
        "posterior_equivalent",
        "posterior_noncrossing",
    ):
        candidates = pair_lists[pair_type]
        candidates.sort(
            key=lambda pair: (
                pair["receiver"]["surface_id"],
                pair["receiver"]["threshold"],
                pair["receiver"]["variant_id"],
                pair["donor"]["variant_id"],
            )
        )
        # Spread the subset over contexts instead of taking one threshold first.
        if len(candidates) > max_per_type:
            indices = [
                round(i * (len(candidates) - 1) / (max_per_type - 1))
                for i in range(max_per_type)
            ] if max_per_type > 1 else [0]
            candidates = [candidates[i] for i in indices]
        for pair in candidates:
            receiver, donor = pair["receiver"], pair["donor"]
            selected.append(
                {
                    "pair_type": pair_type,
                    "pair_id": (
                        f"{pair_type}::{receiver['variant_id']}<-{donor['variant_id']}"
                    ),
                    "receiver": receiver,
                    "donor": donor,
                }
            )
    return selected


def interchange_scores(
    scorer: HFScorer,
    model_layer,
    batch_items: list[dict],
) -> list[dict]:
    """Score a natural interchange with a batch-local residual capture.

    Receiver and donor continuations share one unpatched forward.  The patched
    forward uses the identical padded batch and replaces only receiver states
    with donor states captured in the first pass.  This avoids treating BF16
    batch-shape drift as a causal effect.
    """
    torch = scorer.torch
    flat = []
    for pair_i, item in enumerate(batch_items):
        for role in ("receiver", "donor"):
            row = item[role]
            prefix = chat_prefix(scorer.tokenizer, row["prompt"])
            prefix_ids = scorer.tokenizer(prefix, add_special_tokens=False).input_ids
            patch_positions = token_patch_positions(
                scorer.tokenizer, prefix, row, item["anchor"], item["span"]
            )
            for candidate in ("A", "B"):
                full_ids = scorer.tokenizer(
                    prefix + candidate, add_special_tokens=False
                ).input_ids
                if full_ids[: len(prefix_ids)] != prefix_ids:
                    raise ValueError("candidate changes prefix boundary")
                flat.append(
                    {
                        "pair_i": pair_i,
                        "role": role,
                        "candidate": candidate,
                        "ids": full_ids,
                        "prefix_len": len(prefix_ids),
                        "patch_positions": patch_positions,
                    }
                )

    max_len = max(len(row["ids"]) for row in flat)
    ids, masks = [], []
    for row in flat:
        pad = max_len - len(row["ids"])
        ids.append(row["ids"] + [scorer.tokenizer.pad_token_id] * pad)
        masks.append([1] * len(row["ids"]) + [0] * pad)
    input_ids = torch.tensor(ids, device=scorer.device)
    attention_mask = torch.tensor(masks, device=scorer.device)

    captured = None

    def capture_hook(_module, _inputs, output):
        nonlocal captured
        hidden = output[0] if isinstance(output, tuple) else output
        captured = hidden.detach().clone()

    handle = model_layer.register_forward_hook(capture_hook)
    try:
        with torch.inference_mode():
            baseline_logits = scorer.model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                use_cache=False,
                return_dict=True,
            ).logits
    finally:
        handle.remove()
    if captured is None:
        raise RuntimeError("layer hook did not capture activations")

    row_index = {
        (row["pair_i"], row["role"], row["candidate"]): row_i
        for row_i, row in enumerate(flat)
    }

    def patch_hook(_module, _inputs, output):
        if isinstance(output, tuple):
            hidden = output[0].clone()
            for row_i, row in enumerate(flat):
                if row["role"] != "receiver":
                    continue
                donor_i = row_index[(row["pair_i"], "donor", row["candidate"])]
                donor_positions = flat[donor_i]["patch_positions"]
                if len(row["patch_positions"]) != len(donor_positions):
                    raise ValueError("receiver and donor patch spans are not token-aligned")
                for receiver_pos, donor_pos in zip(
                    row["patch_positions"], donor_positions, strict=True
                ):
                    hidden[row_i, receiver_pos] = captured[donor_i, donor_pos]
            return (hidden, *output[1:])
        hidden = output.clone()
        for row_i, row in enumerate(flat):
            if row["role"] != "receiver":
                continue
            donor_i = row_index[(row["pair_i"], "donor", row["candidate"])]
            donor_positions = flat[donor_i]["patch_positions"]
            if len(row["patch_positions"]) != len(donor_positions):
                raise ValueError("receiver and donor patch spans are not token-aligned")
            for receiver_pos, donor_pos in zip(
                row["patch_positions"], donor_positions, strict=True
            ):
                hidden[row_i, receiver_pos] = captured[donor_i, donor_pos]
        return hidden

    handle = model_layer.register_forward_hook(patch_hook)
    try:
        with torch.inference_mode():
            patched_logits = scorer.model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                use_cache=False,
                return_dict=True,
            ).logits
    finally:
        handle.remove()

    baseline_scores = [
        {"receiver": {}, "donor": {}} for _ in batch_items
    ]
    patched_scores = [dict() for _ in batch_items]

    def continuation_score(logits, row_i, row):
        score = 0.0
        for pos in range(row["prefix_len"], len(row["ids"])):
            token_logits = logits[row_i, pos - 1].float()
            score += float(torch.log_softmax(token_logits, dim=-1)[row["ids"][pos]])
        return score

    for row_i, row in enumerate(flat):
        baseline_scores[row["pair_i"]][row["role"]][row["candidate"]] = (
            continuation_score(baseline_logits, row_i, row)
        )
        if row["role"] == "receiver":
            patched_scores[row["pair_i"]][row["candidate"]] = continuation_score(
                patched_logits, row_i, row
            )
    return [
        {"baseline": baseline, "patched": patched}
        for baseline, patched in zip(baseline_scores, patched_scores, strict=True)
    ]


def semantic_logit(row: dict, label_scores: dict[str, float]) -> float:
    act_label = "A" if row["option_mapping"][0] == "ACT" else "B"
    wait_label = "B" if act_label == "A" else "A"
    return label_scores[act_label] - label_scores[wait_label]


def run(args: argparse.Namespace) -> dict:
    import torch

    metadata = load_jsonl(Path(args.metadata))
    cache = torch.load(args.cache, map_location="cpu", weights_only=True)
    activations = cache["activations"]
    anchors = cache["anchors"]
    if args.anchor not in anchors:
        raise ValueError(args.anchor)
    anchor_i = anchors.index(args.anchor)
    cache_index = {row["variant_id"]: i for i, row in enumerate(metadata)}

    candidate_rows = [
        row
        for row in metadata
        if row["condition"] == args.condition
        and row["surface_id"].startswith(args.surface_prefix)
        and (not args.require_baseline_correct or baseline_correct(row))
    ]
    pairs = build_pairs(candidate_rows, args.max_pairs_per_type)
    for pair in pairs:
        pair["anchor"] = args.anchor
        pair["span"] = args.span
        pair["donor_cache_index"] = cache_index[pair["donor"]["variant_id"]]
        pair["receiver_cache_index"] = cache_index[pair["receiver"]["variant_id"]]

    scorer = HFScorer(args.model, dtype=args.dtype)
    model_layers = scorer.model.model.layers
    layers = list(range(args.layer_offset, len(model_layers), args.layer_stride))
    results = []
    for layer in layers:
        for start in range(0, len(pairs), args.pair_batch_size):
            pair_batch = pairs[start : start + args.pair_batch_size]
            scored = interchange_scores(scorer, model_layers[layer], pair_batch)
            for pair, scores in zip(pair_batch, scored, strict=True):
                receiver, donor = pair["receiver"], pair["donor"]
                receiver_label_scores = scores["baseline"]["receiver"]
                donor_label_scores = scores["baseline"]["donor"]
                patched_label_scores = scores["patched"]
                receiver_semantic = semantic_logit(receiver, receiver_label_scores)
                donor_semantic = semantic_logit(donor, donor_label_scores)
                patched_semantic = semantic_logit(receiver, patched_label_scores)
                recorded_receiver_semantic = receiver["semantic_logit"]
                denominator = donor_semantic - receiver_semantic
                normalized = (
                    (patched_semantic - receiver_semantic) / denominator
                    if abs(denominator) >= args.min_recovery_denominator
                    else None
                )
                patched_action = "ACT" if patched_semantic > 0 else "WAIT"
                results.append(
                    {
                        "pair_id": pair["pair_id"],
                        "pair_type": pair["pair_type"],
                        "condition": args.condition,
                        "surface_id": receiver["surface_id"],
                        "anchor": args.anchor,
                        "span": args.span,
                        "layer": layer,
                        "receiver_variant_id": receiver["variant_id"],
                        "donor_variant_id": donor["variant_id"],
                        "receiver_evidence_id": receiver["evidence_id"],
                        "donor_evidence_id": donor["evidence_id"],
                        "threshold": receiver["threshold"],
                        "receiver_posterior": causal_value(receiver),
                        "donor_posterior": causal_value(donor),
                        "receiver_action": causal_action(receiver),
                        "donor_action": causal_action(donor),
                        "receiver_gold_posterior": receiver["gold_p_a"],
                        "donor_gold_posterior": donor["gold_p_a"],
                        "receiver_gold_action": receiver["gold_action"],
                        "donor_gold_action": donor["gold_action"],
                        "receiver_semantic_logit": receiver_semantic,
                        "recorded_receiver_semantic_logit": recorded_receiver_semantic,
                        "identity_vs_recorded_delta": (
                            receiver_semantic - recorded_receiver_semantic
                        ),
                        "donor_semantic_logit": donor_semantic,
                        "patched_semantic_logit": patched_semantic,
                        "raw_patch_effect": patched_semantic - receiver_semantic,
                        "normalized_recovery": normalized,
                        "patched_action": patched_action,
                        "donor_action_iia": patched_action == causal_action(donor),
                        "receiver_label_scores": receiver_label_scores,
                        "donor_label_scores": donor_label_scores,
                        "patched_label_scores": patched_label_scores,
                    }
                )
    dump_jsonl(results, Path(args.out))
    return {
        "n_pairs": len(pairs),
        "pair_types": {
            pair_type: sum(pair["pair_type"] == pair_type for pair in pairs)
            for pair_type in sorted({pair["pair_type"] for pair in pairs})
        },
        "layers": layers,
        "n_results": len(results),
        "out": args.out,
    }


def summarize(rows: list[dict]) -> dict:
    by_key: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        by_key[
            (
                row["pair_type"],
                row["condition"],
                row["anchor"],
                row.get("span", "single"),
                row["layer"],
            )
        ].append(row)
    summaries = []
    for (pair_type, condition, anchor, span, layer), group in sorted(by_key.items()):
        normalized = [
            row["normalized_recovery"]
            for row in group
            if row["normalized_recovery"] is not None
            and math.isfinite(row["normalized_recovery"])
        ]
        summaries.append(
            {
                "pair_type": pair_type,
                "condition": condition,
                "anchor": anchor,
                "span": span,
                "layer": layer,
                "n": len(group),
                "mean_raw_patch_effect": sum(row["raw_patch_effect"] for row in group)
                / len(group),
                "mean_abs_patch_effect": sum(abs(row["raw_patch_effect"]) for row in group)
                / len(group),
                "mean_abs_identity_vs_recorded_delta": sum(
                    abs(row["identity_vs_recorded_delta"]) for row in group
                )
                / len(group),
                "mean_normalized_recovery": (
                    sum(normalized) / len(normalized) if normalized else None
                ),
                "donor_action_iia": sum(row["donor_action_iia"] for row in group)
                / len(group),
            }
        )
    return {"n_rows": len(rows), "layer_summaries": summaries}


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    run_parser = sub.add_parser("run")
    run_parser.add_argument("--model", required=True)
    run_parser.add_argument("--cache", required=True)
    run_parser.add_argument("--metadata", required=True)
    run_parser.add_argument("--out", required=True)
    run_parser.add_argument("--dtype", default="bfloat16")
    run_parser.add_argument("--condition", default="direct")
    run_parser.add_argument("--surface-prefix", default="natural-gt-high_first")
    run_parser.add_argument("--anchor", default="QUERY_END")
    run_parser.add_argument(
        "--span",
        choices=("single", "belief_number", "belief_statement", "evidence_statement"),
        default="single",
    )
    run_parser.add_argument("--max-pairs-per-type", type=int, default=12)
    run_parser.add_argument("--pair-batch-size", type=int, default=4)
    run_parser.add_argument(
        "--require-baseline-correct",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    run_parser.add_argument("--layer-offset", type=int, default=0)
    run_parser.add_argument("--layer-stride", type=int, default=1)
    run_parser.add_argument("--min-recovery-denominator", type=float, default=0.5)
    summary_parser = sub.add_parser("summarize")
    summary_parser.add_argument("--inputs", nargs="+", required=True)
    summary_parser.add_argument("--out", required=True)
    args = parser.parse_args()
    if args.command == "run":
        result = run(args)
    else:
        rows = []
        for path in args.inputs:
            rows.extend(load_jsonl(Path(path)))
        result = summarize(rows)
        Path(args.out).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
