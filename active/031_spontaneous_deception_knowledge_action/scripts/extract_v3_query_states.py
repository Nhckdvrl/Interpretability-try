#!/usr/bin/env python3
"""Extract prompt-final layer states for the V3 same-graph query panel."""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def single_token_id(tokenizer: Any, text: str) -> int:
    ids = tokenizer.encode(text, add_special_tokens=False)
    if len(ids) != 1:
        raise ValueError(f"Expected one token for {text!r}: {ids}")
    return ids[0]


def extract(
    rows: list[dict[str, Any]], model_path: Path, *, batch_size: int, device: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    import numpy as np
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        str(model_path), local_files_only=True, trust_remote_code=True, padding_side="left"
    )
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    prompts = [
        tokenizer.apply_chat_template(
            [{"role": "user", "content": row["prompt"]}],
            tokenize=False, add_generation_prompt=True,
        )
        for row in rows
    ]
    no_id, yes_id = single_token_id(tokenizer, "No"), single_token_id(tokenizer, "Yes")
    model = AutoModelForCausalLM.from_pretrained(
        str(model_path), local_files_only=True, trust_remote_code=True,
        dtype=torch.bfloat16, low_cpu_mem_usage=True,
    ).to(device)
    model.eval()
    answer_weights = model.lm_head.weight[[no_id, yes_id]].detach().float()
    hidden_batches, final_margins, token_counts = [], [], []
    for start in range(0, len(rows), batch_size):
        encoded = tokenizer(
            prompts[start : start + batch_size], return_tensors="pt", padding=True,
            truncation=True, max_length=4096,
        ).to(device)
        with torch.inference_mode():
            outputs = model(**encoded, output_hidden_states=True, return_dict=True, use_cache=False)
            last = encoded["attention_mask"].sum(dim=1) - 1
            if tokenizer.padding_side == "left":
                last += encoded["attention_mask"].shape[1] - encoded["attention_mask"].sum(dim=1)
            batch_indices = torch.arange(encoded["input_ids"].shape[0], device=device)
            states = torch.stack(
                [state[batch_indices, last].float().cpu() for state in outputs.hidden_states], dim=1
            )
            final_logits = states[:, -1].to(device) @ answer_weights.T
            final_margins.append((final_logits[:, 0] - final_logits[:, 1]).cpu().numpy())
        hidden_batches.append(states.to(torch.float16).numpy())
        token_counts.extend(encoded["attention_mask"].sum(dim=1).cpu().tolist())

    hidden = np.concatenate(hidden_batches)
    margins = np.concatenate(final_margins)
    predicted_no = margins >= 0 if no_id < yes_id else margins > 0
    expected_no = np.asarray([row["expected_answer"] == "No" for row in rows])
    correct = predicted_no == expected_no
    grouped = Counter()
    grouped_correct = Counter()
    for row, is_correct in zip(rows, correct):
        key = (row["split"], row["polarity"], row["query_type"])
        grouped[key] += 1
        grouped_correct[key] += int(is_correct)
    summary = {
        "schema_version": 1,
        "measurement": "prompt-final hidden state for same-graph query panel",
        "model_path": str(model_path.resolve()),
        "model_snapshot": model_path.name,
        "n": len(rows),
        "shape": list(hidden.shape),
        "token_ids": {"No": no_id, "Yes": yes_id},
        "pairwise_no_yes_accuracy": float(correct.mean()),
        "accuracy_by_split_polarity_query": {
            "/".join(key): grouped_correct[key] / grouped[key] for key in sorted(grouped)
        },
    }
    arrays = {
        "hidden_states": hidden,
        "final_no_minus_yes": margins,
        "graph_ids": np.asarray([row["graph_id"] for row in rows]),
        "splits": np.asarray([row["split"] for row in rows]),
        "query_types": np.asarray([row["query_type"] for row in rows]),
        "polarities": np.asarray([row["polarity"] for row in rows]),
        "reachable": np.asarray([row["reachable"] for row in rows]),
        "expected_answers": np.asarray([row["expected_answer"] for row in rows]),
        "token_counts": np.asarray(token_counts),
    }
    return summary, arrays


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--panel", type=Path, required=True)
    parser.add_argument("--model-path", type=Path, required=True)
    parser.add_argument("--arrays-out", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--device", default="cuda:0")
    args = parser.parse_args()
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    import numpy as np

    summary, arrays = extract(
        read_jsonl(args.panel), args.model_path, batch_size=args.batch_size, device=args.device
    )
    args.arrays_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.arrays_out, **arrays)
    args.summary_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
