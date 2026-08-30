from __future__ import annotations

import argparse
import json
import os
import platform
import time
from pathlib import Path
from typing import Any

from .io import file_sha256, read_jsonl, write_json
from .prompts import build_messages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-label", required=True)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--max-pairs", type=int)
    return parser.parse_args()


def render(tokenizer: Any, messages: list[dict[str, str]], model_name: str) -> str:
    kwargs: dict[str, Any] = {"tokenize": False, "add_generation_prompt": True}
    if "qwen" in model_name.casefold():
        kwargs["enable_thinking"] = False
    return tokenizer.apply_chat_template(messages, **kwargs)


def validate_option_tokens(tokenizer: Any, prompts: list[str]) -> dict[str, int]:
    result = {}
    for letter in "ABCDE":
        ids = tokenizer.encode(letter, add_special_tokens=False)
        if len(ids) != 1:
            raise ValueError(f"Option {letter} is not one token: {ids}")
        result[letter] = ids[0]
    for prompt in prompts[:12]:
        base = tokenizer.encode(prompt, add_special_tokens=False)
        for letter, token_id in result.items():
            full = tokenizer.encode(prompt + letter, add_special_tokens=False)
            if full[: len(base)] != base or full[len(base) :] != [token_id]:
                raise ValueError("Option continuation changes prompt tokenization.")
    return result


def main() -> None:
    args = parse_args()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    pairs = list(read_jsonl(args.data))
    if args.max_pairs:
        pairs = pairs[: args.max_pairs]
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    tokenizer.padding_side = "left"
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    prompts, records = [], []
    for pair in pairs:
        for condition in contract["conditions"]:
            for option_order in contract["option_orders"]:
                messages, label_to_letter = build_messages(pair, condition, option_order, contract)
                prompts.append(render(tokenizer, messages, args.model))
                records.append(
                    {
                        "pair_id": pair["pair_id"],
                        "doc_id": pair["doc_id"],
                        "direction": pair["direction"],
                        "target_label": pair["target_label"],
                        "neighbor_label": pair["neighbor_label"],
                        "condition": condition,
                        "option_order": option_order,
                        "gold_letter": label_to_letter[pair["target_label"]],
                        "label_to_letter": label_to_letter,
                        "has_explicit_relation": pair["has_explicit_relation"],
                        "same_sentence": pair["same_sentence"],
                        "sentence_distance": pair["sentence_distance"],
                        "target_event_type": pair["target_event_type"],
                        "neighbor_event_type": pair["neighbor_event_type"],
                    }
                )
    token_ids = validate_option_tokens(tokenizer, prompts)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        local_files_only=True,
        torch_dtype=torch.bfloat16,
        attn_implementation="sdpa",
        device_map={"": args.device},
    )
    model.eval()
    started = time.time()
    token_lengths = []
    args.output.parent.mkdir(parents=True, exist_ok=True)
    indices = [token_ids[letter] for letter in "ABCDE"]
    with args.output.open("w", encoding="utf-8") as handle, torch.inference_mode():
        for start in range(0, len(prompts), args.batch_size):
            encoded = tokenizer(
                prompts[start : start + args.batch_size],
                return_tensors="pt",
                padding=True,
                add_special_tokens=False,
            ).to(args.device)
            token_lengths.extend(encoded["attention_mask"].sum(1).tolist())
            logits = model(**encoded, use_cache=False, logits_to_keep=1).logits[:, -1, indices].float()
            probabilities = torch.softmax(logits, -1).cpu().tolist()
            for record, local_probs in zip(records[start : start + args.batch_size], probabilities):
                letter_probs = dict(zip("ABCDE", local_probs))
                label_probs = {
                    label: letter_probs[letter] for label, letter in record["label_to_letter"].items()
                }
                predicted_label = max(label_probs, key=label_probs.get)
                output = {
                    **record,
                    "model_label": args.model_label,
                    "label_probabilities": label_probs,
                    "predicted_label": predicted_label,
                    "correct": predicted_label == record["target_label"],
                    "toward_neighbor": predicted_label == record["neighbor_label"],
                }
                handle.write(json.dumps(output, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()
    metadata = {
        "model": args.model,
        "model_label": args.model_label,
        "model_revision": getattr(model.config, "_commit_hash", None),
        "records": len(records),
        "pairs": len(pairs),
        "contract_version": contract["contract_version"],
        "data_sha256": file_sha256(args.data),
        "option_token_ids": token_ids,
        "min_prompt_tokens": min(token_lengths),
        "max_prompt_tokens": max(token_lengths),
        "mean_prompt_tokens": sum(token_lengths) / len(token_lengths),
        "elapsed_seconds": time.time() - started,
        "batch_size": args.batch_size,
        "device": args.device,
        "dtype": "bfloat16",
        "python": platform.python_version(),
        "torch_version": torch.__version__,
        "transformers_version": __import__("transformers").__version__,
    }
    write_json(args.output.with_suffix(".metadata.json"), metadata)
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
