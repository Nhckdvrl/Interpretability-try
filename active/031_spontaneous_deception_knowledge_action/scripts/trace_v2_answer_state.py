#!/usr/bin/env python3
"""Trace the correct-vs-wrong answer margin through Llama residual layers.

This is a mechanistic preflight, not evidence of a graph-state representation.
It measures when the next-token state begins to favor the correct answer while
holding answer polarity fixed (all analyzed graph truths are ``No``).
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def build_cohorts(rows: list[dict[str, Any]], tokenizer: Any) -> list[dict[str, str]]:
    cohorts = []
    for row in rows:
        hard_prompt = tokenizer.apply_chat_template(
            [{"role": "user", "content": row["hard_prompt"]}],
            tokenize=False,
            add_generation_prompt=True,
        )
        cohorts.append(
            {
                "item_id": row["item_id"],
                "condition": row["role"],
                "prompt": hard_prompt,
                "correct_answer": row["hard_graph"]["correct_answer"],
            }
        )
        if row["role"] == "hard_deceptive":
            easy_prompt = tokenizer.apply_chat_template(
                [
                    {"role": "user", "content": row["hard_prompt"]},
                    {"role": "assistant", "content": row["hard_output"]},
                    {"role": "user", "content": row["followup_prompt"]},
                ],
                tokenize=False,
                add_generation_prompt=True,
            )
            cohorts.append(
                {
                    "item_id": row["item_id"],
                    "condition": "easy_correct",
                    "prompt": easy_prompt,
                    "correct_answer": row["followup_graph"]["correct_answer"],
                }
            )
    if {row["correct_answer"] for row in cohorts} != {"No"}:
        raise ValueError("V2 polarity control requires every analyzed truth to be No")
    return sorted(cohorts, key=lambda row: (row["condition"], row["item_id"]))


def single_token_id(tokenizer: Any, text: str) -> int:
    ids = tokenizer.encode(text, add_special_tokens=False)
    if len(ids) != 1:
        raise ValueError(f"Expected one token for {text!r}, found {ids}")
    return ids[0]


def layer_summary(margins: Any, conditions: list[str]) -> dict[str, Any]:
    import numpy as np

    output: dict[str, Any] = {}
    condition_array = np.asarray(conditions)
    for condition in sorted(set(conditions)):
        values = margins[condition_array == condition]
        output[condition] = {
            "n": int(values.shape[0]),
            "mean_correct_minus_wrong": values.mean(axis=0).tolist(),
            "median_correct_minus_wrong": np.median(values, axis=0).tolist(),
            "fraction_correct_margin_positive": (values > 0).mean(axis=0).tolist(),
        }
    return output


def trace(
    cohorts: list[dict[str, str]], model_path: Path, *, batch_size: int, device: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    import numpy as np
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        str(model_path), local_files_only=True, trust_remote_code=True, padding_side="left"
    )
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    no_id = single_token_id(tokenizer, "No")
    yes_id = single_token_id(tokenizer, "Yes")
    model = AutoModelForCausalLM.from_pretrained(
        str(model_path),
        local_files_only=True,
        trust_remote_code=True,
        dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
    ).to(device)
    model.eval()
    final_norm = model.model.norm
    answer_weights = model.lm_head.weight[[no_id, yes_id]].detach()

    all_hidden = []
    all_margins = []
    token_counts = []
    for start in range(0, len(cohorts), batch_size):
        batch = cohorts[start : start + batch_size]
        encoded = tokenizer(
            [row["prompt"] for row in batch],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=4096,
        ).to(device)
        last_indices = encoded["attention_mask"].sum(dim=1) - 1
        if tokenizer.padding_side == "left":
            last_indices = last_indices + (encoded["attention_mask"].shape[1] - encoded["attention_mask"].sum(dim=1))
        with torch.inference_mode():
            outputs = model(**encoded, output_hidden_states=True, return_dict=True, use_cache=False)
            per_layer = []
            for hidden in outputs.hidden_states:
                batch_indices = torch.arange(hidden.shape[0], device=hidden.device)
                per_layer.append(hidden[batch_indices, last_indices].float().cpu())
            hidden_stack = torch.stack(per_layer, dim=1)
            normalized = final_norm(hidden_stack.to(device, dtype=model.dtype))
            # Transformers exposes the already-final-normalized state as the
            # last element of ``hidden_states``.  Applying RMSNorm twice changes
            # its direction because of the learned per-feature weights.
            normalized[:, -1] = hidden_stack[:, -1].to(device, dtype=model.dtype)
            logits = torch.einsum("blh,ah->bla", normalized, answer_weights)
            margins = logits[:, :, 0] - logits[:, :, 1]
        all_hidden.append(hidden_stack.to(torch.float16).numpy())
        all_margins.append(margins.float().cpu().numpy())
        token_counts.extend(encoded["attention_mask"].sum(dim=1).cpu().tolist())
        del outputs, hidden_stack, normalized, logits, margins

    hidden_array = np.concatenate(all_hidden)
    margin_array = np.concatenate(all_margins)
    conditions = [row["condition"] for row in cohorts]
    expected_final_no = np.asarray([condition != "hard_deceptive" for condition in conditions])
    # Greedy argmax resolves an exact bf16 tie in favor of the lower token ID;
    # here No=2822 and Yes=9642.
    predicted_final_no = margin_array[:, -1] >= 0 if no_id < yes_id else margin_array[:, -1] > 0
    final_margin_agreement = predicted_final_no == expected_final_no
    mismatch_rows = [
        {
            "item_id": cohorts[index]["item_id"],
            "condition": conditions[index],
            "margin": float(margin_array[index, -1]),
        }
        for index in np.flatnonzero(~final_margin_agreement)
    ]
    summary = {
        "schema_version": 1,
        "measurement": "prompt-final-token residual-stream logit lens",
        "interpretation_limit": "answer-state preflight only; not graph-state or causal evidence",
        "answer_polarity_control": "all correct answers are No; margin is No minus Yes",
        "model_path": str(model_path.resolve()),
        "model_snapshot": model_path.name,
        "n": len(cohorts),
        "n_layers_including_embedding": int(margin_array.shape[1]),
        "hidden_size": int(hidden_array.shape[2]),
        "token_ids": {"No": no_id, "Yes": yes_id},
        "final_margin_replay_agreement": float(final_margin_agreement.mean()),
        "final_margin_replay_mismatches": mismatch_rows,
        "by_condition": layer_summary(margin_array, conditions),
    }
    arrays = {
        "hidden_states": hidden_array,
        "correct_minus_wrong": margin_array,
        "item_ids": np.asarray([row["item_id"] for row in cohorts]),
        "conditions": np.asarray(conditions),
        "token_counts": np.asarray(token_counts),
    }
    return summary, arrays


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--population", type=Path, required=True)
    parser.add_argument("--model-path", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    parser.add_argument("--arrays-out", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--device", default="cuda:0")
    args = parser.parse_args()
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

    from transformers import AutoTokenizer
    import numpy as np

    tokenizer = AutoTokenizer.from_pretrained(
        str(args.model_path), local_files_only=True, trust_remote_code=True
    )
    cohorts = build_cohorts(read_jsonl(args.population), tokenizer)
    summary, arrays = trace(cohorts, args.model_path, batch_size=args.batch_size, device=args.device)
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.arrays_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    np.savez_compressed(args.arrays_out, **arrays)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
