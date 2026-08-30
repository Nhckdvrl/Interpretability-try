from __future__ import annotations

import argparse
import json
import math
import os
import platform
import time
from pathlib import Path
from typing import Any

from .io import file_sha256, read_jsonl, write_json
from .prompts import CONDITIONS, ORDERS, build_messages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run exact A/B next-token scoring.")
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-label", required=True)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-pairs", type=int)
    parser.add_argument("--dtype", choices=("bfloat16", "float16"), default="bfloat16")
    parser.add_argument("--trust-remote-code", action="store_true")
    return parser.parse_args()


def render_prompt(tokenizer: Any, messages: list[dict[str, str]], model: str) -> str:
    kwargs: dict[str, Any] = {"tokenize": False, "add_generation_prompt": True}
    if "qwen" in model.casefold():
        kwargs["enable_thinking"] = False
    return tokenizer.apply_chat_template(messages, **kwargs)


def option_token_ids(tokenizer: Any, prompts: list[str]) -> tuple[int, int]:
    expected: dict[str, int] = {}
    for label in ("A", "B"):
        ids = tokenizer.encode(label, add_special_tokens=False)
        if len(ids) != 1:
            raise ValueError(f"Label {label!r} is not one token in isolation: {ids}")
        expected[label] = ids[0]
    for prompt in prompts[: min(16, len(prompts))]:
        base = tokenizer.encode(prompt, add_special_tokens=False)
        for label in ("A", "B"):
            full = tokenizer.encode(prompt + label, add_special_tokens=False)
            if full[: len(base)] != base or full[len(base) :] != [expected[label]]:
                raise ValueError("Prompt boundary does not preserve the single-token A/B continuation.")
    return expected["A"], expected["B"]


def main() -> None:
    args = parse_args()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    pairs = list(read_jsonl(args.data))
    if args.max_pairs:
        pairs = pairs[: args.max_pairs]

    tokenizer = AutoTokenizer.from_pretrained(
        args.model, local_files_only=True, trust_remote_code=args.trust_remote_code
    )
    tokenizer.padding_side = "left"
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    records: list[dict[str, Any]] = []
    prompts: list[str] = []
    for pair in pairs:
        for condition in CONDITIONS:
            for order in ORDERS:
                messages, gold_label = build_messages(pair, condition, order, contract)
                prompt = render_prompt(tokenizer, messages, args.model)
                prompts.append(prompt)
                records.append(
                    {
                        "pair_id": pair["pair_id"],
                        "question_id": pair["question_id"],
                        "property_count": pair["property_count"],
                        "condition": condition,
                        "answer_order": order,
                        "gold_label": gold_label,
                        "prompt_chars": len(prompt),
                    }
                )

    token_a, token_b = option_token_ids(tokenizer, prompts)
    torch_dtype = torch.bfloat16 if args.dtype == "bfloat16" else torch.float16
    started = time.time()
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        local_files_only=True,
        trust_remote_code=args.trust_remote_code,
        torch_dtype=torch_dtype,
        attn_implementation="sdpa",
        device_map={"": args.device},
    )
    model.eval()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    token_lengths: list[int] = []
    with args.output.open("w", encoding="utf-8") as handle, torch.inference_mode():
        for start in range(0, len(prompts), args.batch_size):
            local_prompts = prompts[start : start + args.batch_size]
            encoded = tokenizer(
                local_prompts, return_tensors="pt", padding=True, add_special_tokens=False
            ).to(args.device)
            token_lengths.extend(encoded["attention_mask"].sum(dim=1).tolist())
            # Both supported model families can project only the final hidden state.
            # This avoids materializing batch x sequence x vocabulary logits.
            logits = model(
                **encoded, use_cache=False, logits_to_keep=1
            ).logits[:, -1, [token_a, token_b]].float()
            probabilities = torch.softmax(logits, dim=-1).cpu().tolist()
            for record, (prob_a, prob_b) in zip(records[start : start + args.batch_size], probabilities):
                predicted = "A" if prob_a >= prob_b else "B"
                gold_probability = prob_a if record["gold_label"] == "A" else prob_b
                output = {
                    **record,
                    "model_label": args.model_label,
                    "prob_a_normalized": prob_a,
                    "prob_b_normalized": prob_b,
                    "gold_probability": gold_probability,
                    "gold_log_odds": math.log(max(gold_probability, 1e-12))
                    - math.log(max(1.0 - gold_probability, 1e-12)),
                    "predicted_label": predicted,
                    "correct": predicted == record["gold_label"],
                }
                handle.write(json.dumps(output, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()

    metadata = {
        "model": args.model,
        "model_label": args.model_label,
        "model_revision": getattr(model.config, "_commit_hash", None),
        "contract_version": contract["contract_version"],
        "data_path": str(args.data.resolve()),
        "data_sha256": file_sha256(args.data),
        "records": len(records),
        "pairs": len(pairs),
        "device": args.device,
        "dtype": args.dtype,
        "batch_size": args.batch_size,
        "option_token_ids": {"A": token_a, "B": token_b},
        "min_prompt_tokens": min(token_lengths),
        "max_prompt_tokens": max(token_lengths),
        "mean_prompt_tokens": sum(token_lengths) / len(token_lengths),
        "elapsed_seconds": time.time() - started,
        "torch_version": torch.__version__,
        "transformers_version": __import__("transformers").__version__,
        "python": platform.python_version(),
    }
    write_json(args.output.with_suffix(".metadata.json"), metadata)
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
