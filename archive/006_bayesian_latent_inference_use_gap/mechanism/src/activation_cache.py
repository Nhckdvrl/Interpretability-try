#!/usr/bin/env python3
"""Cache Qwen2.5 residual states at named semantic positions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from mechanism_behavior import HFScorer, chat_prefix
from mechanism_data import dump_jsonl, load_jsonl


ANCHORS = (
    "EVIDENCE_END",
    "BELIEF_NUM_END",
    "THRESHOLD_NUM_END",
    "RULE_END",
    "MAPPING_END",
    "QUERY_END",
)


def char_anchor_ends(prompt: str, threshold: float) -> dict[str, int]:
    evidence_start = prompt.index("Observed counts:")
    evidence_end = prompt.index(".", evidence_start) + 1
    belief_marker = "use the posterior value P(A | observations)="
    if belief_marker in prompt:
        belief_start = prompt.index(belief_marker) + len(belief_marker)
        belief_end = prompt.index(". A fixed policy", belief_start)
    else:
        # Direct prompts have no serialized belief.  Retain a defined placeholder
        # for rectangular caches, but never interpret it as a belief position.
        belief_end = evidence_end
    rule_start = prompt.index("A fixed policy is defined as follows:")
    threshold_text = f"{threshold:.6f}"
    threshold_end = prompt.index(threshold_text, rule_start) + len(threshold_text)
    option_a_start = prompt.index(" Option A is ", rule_start)
    rule_end = option_a_start
    mapping_end = prompt.index(" Which option", option_a_start)
    query_end = len(prompt)
    return {
        "EVIDENCE_END": evidence_end,
        "BELIEF_NUM_END": belief_end,
        "THRESHOLD_NUM_END": threshold_end,
        "RULE_END": rule_end,
        "MAPPING_END": mapping_end,
        "QUERY_END": query_end,
    }


def token_anchor_positions(tokenizer, prefix: str, prompt: str, threshold: float) -> dict[str, int]:
    prompt_start = prefix.index(prompt)
    encoded = tokenizer(prefix, add_special_tokens=False, return_offsets_mapping=True)
    offsets = encoded["offset_mapping"]
    positions = {}
    for name, relative_end in char_anchor_ends(prompt, threshold).items():
        absolute_end = prompt_start + relative_end
        candidates = [
            index
            for index, (start, end) in enumerate(offsets)
            if end > start and end <= absolute_end
        ]
        if not candidates:
            raise ValueError((name, absolute_end))
        positions[name] = max(candidates)
    return positions


def select_rows(args: argparse.Namespace) -> list[dict]:
    rows = load_jsonl(Path(args.results))
    selected = [
        row
        for row in rows
        if row["condition"] in args.conditions
        and any(row["surface_id"].startswith(prefix) for prefix in args.surface_prefixes)
    ]
    selected.sort(key=lambda row: row["variant_id"])
    if args.limit:
        selected = selected[: args.limit]
    return selected


def run(args: argparse.Namespace) -> dict:
    import torch

    rows = select_rows(args)
    scorer = HFScorer(args.model, dtype=args.dtype)
    tokenizer = scorer.tokenizer
    prefixes = [chat_prefix(tokenizer, row["prompt"]) for row in rows]
    positions = [
        token_anchor_positions(tokenizer, prefix, row["prompt"], row["threshold"])
        for prefix, row in zip(prefixes, rows, strict=True)
    ]
    for row, prefix, pos in zip(rows, prefixes, positions, strict=True):
        row["chat_prefix_token_count"] = len(
            tokenizer(prefix, add_special_tokens=False).input_ids
        )
        row["anchor_token_positions"] = pos

    cached_chunks = []
    for start in range(0, len(rows), args.batch_size):
        batch_prefixes = prefixes[start : start + args.batch_size]
        batch_positions = positions[start : start + args.batch_size]
        batch = tokenizer(batch_prefixes, padding=True, return_tensors="pt").to(
            scorer.device
        )
        with torch.inference_mode():
            outputs = scorer.model(
                **batch, output_hidden_states=True, use_cache=False, return_dict=True
            )
        hidden_states = outputs.hidden_states
        chunk = torch.empty(
            (
                len(batch_prefixes),
                len(hidden_states),
                len(ANCHORS),
                hidden_states[0].shape[-1],
            ),
            dtype=torch.bfloat16,
        )
        for layer_i, hidden in enumerate(hidden_states):
            for row_i, anchor_map in enumerate(batch_positions):
                for anchor_i, anchor in enumerate(ANCHORS):
                    chunk[row_i, layer_i, anchor_i] = hidden[
                        row_i, anchor_map[anchor]
                    ].detach().to(device="cpu", dtype=torch.bfloat16)
        cached_chunks.append(chunk)
        del outputs, hidden_states, batch

    activations = torch.cat(cached_chunks, dim=0) if cached_chunks else torch.empty(0)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "activations": activations,
            "anchors": list(ANCHORS),
            "model": args.model,
            "conditions": args.conditions,
            "surface_prefixes": args.surface_prefixes,
        },
        out,
    )
    dump_jsonl(rows, Path(args.metadata))
    return {
        "n": len(rows),
        "shape": list(activations.shape),
        "anchors": list(ANCHORS),
        "out": args.out,
        "metadata": args.metadata,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--results", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--dtype", default="bfloat16")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument(
        "--conditions", nargs="+", default=["direct", "gold_bridge", "self_mean_bridge"]
    )
    parser.add_argument(
        "--surface-prefixes", nargs="+", default=["natural-gt-high_first"]
    )
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    print(json.dumps(run(args), indent=2))


if __name__ == "__main__":
    main()
