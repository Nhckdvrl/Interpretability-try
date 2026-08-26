#!/usr/bin/env python3
"""Cache every token state in the fixed-width serialized posterior span."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from mechanism_behavior import HFScorer, chat_prefix
from mechanism_data import dump_jsonl, load_jsonl


def belief_positions(tokenizer, prefix: str, prompt: str) -> list[int]:
    marker = "use the posterior value P(A | observations)="
    prompt_start = prefix.index(prompt)
    start = prompt.index(marker) + len(marker)
    end = prompt.index(". A fixed policy", start)
    absolute_start, absolute_end = prompt_start + start, prompt_start + end
    offsets = tokenizer(
        prefix, add_special_tokens=False, return_offsets_mapping=True
    )["offset_mapping"]
    positions = [
        i
        for i, (token_start, token_end) in enumerate(offsets)
        if token_end > absolute_start and token_start < absolute_end
    ]
    if len(positions) != 8:
        raise ValueError(f"expected 8 fixed-width belief tokens, got {positions}")
    return positions


def run(args: argparse.Namespace) -> dict:
    import torch

    rows = [
        row
        for row in load_jsonl(Path(args.results))
        if row["condition"] in args.conditions
        and row["surface_id"].startswith(args.surface_prefix)
    ]
    rows.sort(key=lambda row: row["variant_id"])
    scorer = HFScorer(args.model, dtype=args.dtype)
    prefixes = [chat_prefix(scorer.tokenizer, row["prompt"]) for row in rows]
    positions = [
        belief_positions(scorer.tokenizer, prefix, row["prompt"])
        for prefix, row in zip(prefixes, rows, strict=True)
    ]
    for row, pos in zip(rows, positions, strict=True):
        row["belief_span_token_positions"] = pos

    chunks = []
    for start in range(0, len(rows), args.batch_size):
        batch_prefixes = prefixes[start : start + args.batch_size]
        batch_positions = positions[start : start + args.batch_size]
        batch = scorer.tokenizer(batch_prefixes, padding=True, return_tensors="pt").to(
            scorer.device
        )
        with torch.inference_mode():
            output = scorer.model(
                **batch, output_hidden_states=True, use_cache=False, return_dict=True
            )
        hidden_states = output.hidden_states
        chunk = torch.empty(
            (len(batch_prefixes), len(hidden_states), 8, hidden_states[0].shape[-1]),
            dtype=torch.bfloat16,
        )
        for row_i, pos in enumerate(batch_positions):
            for layer_i, hidden in enumerate(hidden_states):
                chunk[row_i, layer_i] = hidden[row_i, pos].detach().to(
                    device="cpu", dtype=torch.bfloat16
                )
        chunks.append(chunk)
        del output, hidden_states, batch

    activations = torch.cat(chunks)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "activations": activations,
            "model": args.model,
            "conditions": args.conditions,
            "span": "serialized_posterior_8_tokens",
        },
        args.out,
    )
    dump_jsonl(rows, Path(args.metadata))
    return {
        "n": len(rows),
        "shape": list(activations.shape),
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
        "--conditions", nargs="+", default=["gold_bridge", "self_mean_bridge"]
    )
    parser.add_argument("--surface-prefix", default="natural-gt-high_first")
    args = parser.parse_args()
    print(json.dumps(run(args), indent=2))


if __name__ == "__main__":
    main()
