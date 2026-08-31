#!/usr/bin/env python3
"""Run a controlled final-prompt-token residual transplantation preflight.

Whole residual states are intentionally used only as an upper-bound test of the
intervention primitive.  Matched-easy donors are compared with shuffled-easy,
hard-truthful, and same-norm random controls; rescue is not interpreted as a
graph-specific causal effect.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trace_v2_answer_state import build_cohorts, read_jsonl, single_token_id


INTERVENTIONS = ("matched_easy", "shuffled_easy", "hard_truthful", "random_same_norm")


def donor_indices(item_ids: list[str], conditions: list[str], excluded_easy: set[str]) -> dict[str, Any]:
    index = {(item_id, condition): i for i, (item_id, condition) in enumerate(zip(item_ids, conditions))}
    recipients = [
        index[(item_id, "hard_deceptive")]
        for item_id in sorted({item for item, condition in index if condition == "hard_deceptive"})
        if item_id not in excluded_easy
    ]
    easy = [index[(item_ids[i], "easy_correct")] for i in recipients]
    truthful = [i for i, condition in enumerate(conditions) if condition == "hard_truthful"]
    if not truthful:
        raise ValueError("No hard-truthful donor states")
    return {
        "recipient": recipients,
        "matched_easy": easy,
        "shuffled_easy": easy[1:] + easy[:1],
        "hard_truthful": [truthful[i % len(truthful)] for i in range(len(recipients))],
    }


def summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in records:
        grouped[(row["layer"], row["intervention"])].append(row)
    output = {}
    for (layer, intervention), rows in sorted(grouped.items()):
        deltas = [row["patched_margin"] - row["base_margin"] for row in rows]
        output[f"layer_{layer}/{intervention}"] = {
            "n": len(rows),
            "rescue_rate": sum(row["patched_margin"] >= 0 for row in rows) / len(rows),
            "mean_base_margin": sum(row["base_margin"] for row in rows) / len(rows),
            "mean_patched_margin": sum(row["patched_margin"] for row in rows) / len(rows),
            "mean_margin_delta": sum(deltas) / len(deltas),
        }
    return output


def run(
    population: list[dict[str, Any]], arrays_path: Path, trace_summary: dict[str, Any],
    model_path: Path, layers: list[int], *, batch_size: int, device: str, seed: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    import numpy as np
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        str(model_path), local_files_only=True, trust_remote_code=True, padding_side="left"
    )
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    cohorts = build_cohorts(population, tokenizer)
    stored = np.load(arrays_path)
    item_ids = stored["item_ids"].astype(str).tolist()
    conditions = stored["conditions"].astype(str).tolist()
    expected_order = [(row["item_id"], row["condition"]) for row in cohorts]
    if expected_order != list(zip(item_ids, conditions)):
        raise ValueError("Trace arrays do not match the current frozen population")
    hidden = torch.from_numpy(stored["hidden_states"])
    excluded = {row["item_id"] for row in trace_summary["final_margin_replay_mismatches"]}
    indices = donor_indices(item_ids, conditions, excluded)
    recipient_indices = indices["recipient"]
    recipient_rows = [cohorts[i] for i in recipient_indices]

    no_id = single_token_id(tokenizer, "No")
    yes_id = single_token_id(tokenizer, "Yes")
    model = AutoModelForCausalLM.from_pretrained(
        str(model_path), local_files_only=True, trust_remote_code=True,
        dtype=torch.bfloat16, low_cpu_mem_usage=True,
    ).to(device)
    model.eval()
    records = []
    generator = torch.Generator(device=device).manual_seed(seed)

    for start in range(0, len(recipient_rows), batch_size):
        batch_rows = recipient_rows[start : start + batch_size]
        batch_recipient_indices = recipient_indices[start : start + batch_size]
        encoded = tokenizer(
            [row["prompt"] for row in batch_rows], return_tensors="pt", padding=True,
            truncation=True, max_length=4096,
        ).to(device)
        with torch.inference_mode():
            base_output = model(**encoded, return_dict=True, use_cache=False, logits_to_keep=1)
            base_logits = base_output.logits[:, -1, [no_id, yes_id]].float().cpu()
            base_margins = base_logits[:, 0] - base_logits[:, 1]

        for layer in layers:
            hidden_index = layer + 1
            recipients_at_layer = hidden[batch_recipient_indices, hidden_index].to(device, dtype=model.dtype)
            for intervention in INTERVENTIONS:
                if intervention == "random_same_norm":
                    matched_indices = indices["matched_easy"][start : start + len(batch_rows)]
                    matched = hidden[matched_indices, hidden_index].to(device, dtype=model.dtype)
                    delta = matched - recipients_at_layer
                    random_delta = torch.randn(
                        delta.shape, generator=generator, device=device, dtype=torch.float32
                    )
                    random_delta /= random_delta.norm(dim=-1, keepdim=True)
                    random_delta *= delta.float().norm(dim=-1, keepdim=True)
                    targets = recipients_at_layer + random_delta.to(model.dtype)
                else:
                    selected = indices[intervention][start : start + len(batch_rows)]
                    targets = hidden[selected, hidden_index].to(device, dtype=model.dtype)

                def replace_final_state(_module: Any, _inputs: Any, output: Any) -> Any:
                    if isinstance(output, tuple):
                        state = output[0].clone()
                        state[:, -1] = targets
                        return (state,) + output[1:]
                    state = output.clone()
                    state[:, -1] = targets
                    return state

                handle = model.model.layers[layer].register_forward_hook(replace_final_state)
                try:
                    with torch.inference_mode():
                        patched = model(**encoded, return_dict=True, use_cache=False, logits_to_keep=1)
                        logits = patched.logits[:, -1, [no_id, yes_id]].float().cpu()
                        patched_margins = logits[:, 0] - logits[:, 1]
                finally:
                    handle.remove()
                for row, base_margin, patched_margin in zip(batch_rows, base_margins, patched_margins):
                    records.append(
                        {
                            "item_id": row["item_id"],
                            "layer": layer,
                            "intervention": intervention,
                            "base_margin": float(base_margin),
                            "patched_margin": float(patched_margin),
                        }
                    )

    summary = {
        "schema_version": 1,
        "measurement": "whole residual replacement at hard-prompt final token",
        "interpretation_limit": "transplantation upper bound; not graph-specific causal evidence",
        "model_snapshot": model_path.name,
        "layers": layers,
        "n_frozen_recipients": sum(row["role"] == "hard_deceptive" for row in population),
        "n_analyzed_recipients": len(recipient_rows),
        "excluded_instrumentation_unstable_items": sorted(excluded),
        "seed": seed,
        "by_layer_and_intervention": summarize_records(records),
    }
    return records, summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--population", type=Path, required=True)
    parser.add_argument("--trace-arrays", type=Path, required=True)
    parser.add_argument("--trace-summary", type=Path, required=True)
    parser.add_argument("--model-path", type=Path, required=True)
    parser.add_argument("--records-out", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    parser.add_argument("--layers", type=int, nargs="+", default=[15, 18, 20, 22, 24, 26, 28, 30])
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--seed", type=int, default=31032)
    args = parser.parse_args()
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    records, summary = run(
        read_jsonl(args.population), args.trace_arrays,
        json.loads(args.trace_summary.read_text()), args.model_path, args.layers,
        batch_size=args.batch_size, device=args.device, seed=args.seed,
    )
    args.records_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    with args.records_out.open("w", encoding="utf-8") as handle:
        for row in records:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    args.summary_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
