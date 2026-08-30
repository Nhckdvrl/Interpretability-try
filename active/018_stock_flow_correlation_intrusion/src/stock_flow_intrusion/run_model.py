"""Score net-flow recognition and downstream stock judgments."""
from __future__ import annotations

import argparse
import json
import platform
import time
from collections import defaultdict
from pathlib import Path

from .io import read_jsonl, sha256
from .prompts import net_messages, stock_messages


CONDITIONS = ("direct", "actual_net_history", "explicit_correct_net",
              "masked_net_history", "formula_reminder")
COLUMN_ORDERS = ("inflow_first", "outflow_first")
OPTION_ORDERS = ("canonical", "reversed")


def render(tokenizer, messages: list[dict], model_name: str) -> str:
    kwargs = {"tokenize": False, "add_generation_prompt": True}
    if "qwen" in model_name.casefold():
        kwargs["enable_thinking"] = False
    return tokenizer.apply_chat_template(messages, **kwargs)


def option_tokens(tokenizer, prompts: list[str]) -> dict[str, int]:
    result = {}
    for letter in "AB":
        ids = tokenizer.encode(letter, add_special_tokens=False)
        if len(ids) != 1:
            raise ValueError(f"{letter} is not one token: {ids}")
        result[letter] = ids[0]
    for prompt in prompts[:20]:
        base = tokenizer.encode(prompt, add_special_tokens=False)
        for letter, token in result.items():
            full = tokenizer.encode(prompt + letter, add_special_tokens=False)
            if full[:len(base)] != base or full[len(base):] != [token]:
                raise ValueError("answer continuation changes prompt tokenization")
    return result


def score(model, tokenizer, prompts: list[str], batch_size: int, device: str,
          token_ids: dict[str, int]) -> list[dict]:
    import torch

    output = []
    indices = [token_ids["A"], token_ids["B"]]
    with torch.inference_mode():
        for start in range(0, len(prompts), batch_size):
            inputs = tokenizer(prompts[start:start + batch_size], return_tensors="pt",
                               padding=True, add_special_tokens=False).to(device)
            logits = model(**inputs, use_cache=False, logits_to_keep=1).logits[:, -1, indices].float()
            for p_a, p_b in torch.softmax(logits, -1).cpu().tolist():
                output.append({"prob_A": p_a, "prob_B": p_b,
                               "pred_letter": "A" if p_a >= p_b else "B"})
    return output


def common(item: dict) -> dict:
    return {key: item[key] for key in (
        "item_id", "dam_id", "cell", "congruence", "net_direction",
        "storage_direction", "inflow_trend_direction", "closure_ratio",
        "flow_margin", "inflow_time_correlation", "inflow_range_ratio",
    )}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--family", required=True, choices=("qwen", "gemma", "llama"))
    ap.add_argument("--bank", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    started = time.time()
    bank = read_jsonl(args.bank)
    if args.limit:
        bank = bank[:args.limit]
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    tokenizer.padding_side = "left"
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    net_prompts, net_specs = [], []
    for item in bank:
        for column_order in COLUMN_ORDERS:
            for option_order in OPTION_ORDERS:
                messages, mapping = net_messages(item, column_order, option_order)
                net_prompts.append(render(tokenizer, messages, args.model))
                net_specs.append((item, column_order, option_order, mapping))
    token_ids = option_tokens(tokenizer, net_prompts)
    model = AutoModelForCausalLM.from_pretrained(
        args.model, local_files_only=True, dtype=torch.bfloat16,
        attn_implementation="sdpa", device_map={"": args.device},
    ).eval()
    net_scores = score(model, tokenizer, net_prompts, args.batch_size, args.device, token_ids)
    rows = []
    predictions: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for (item, column_order, option_order, mapping), local in zip(net_specs, net_scores):
        inverse = {letter: label for label, letter in mapping.items()}
        predicted = inverse[local["pred_letter"]]
        p_positive = local["prob_A"] if mapping["positive"] == "A" else local["prob_B"]
        predictions[item["item_id"]].append((predicted, p_positive))
        rows.append({
            **common(item), "condition": "net_recognition", "column_order": column_order,
            "option_order": option_order, "gold_label": item["net_direction"],
            "predicted_label": predicted, "prob_positive": p_positive,
            "correct": predicted == item["net_direction"], **local,
        })
    predicted_net = {
        item_id: "positive" if sum(p for _, p in values) / len(values) >= 0.5 else "negative"
        for item_id, values in predictions.items()
    }
    print(json.dumps({"family": args.family, "condition": "net_recognition",
                      "completed": len(net_scores)}), flush=True)

    stock_prompts, stock_specs = [], []
    for item in bank:
        for condition in CONDITIONS:
            for column_order in COLUMN_ORDERS:
                for option_order in OPTION_ORDERS:
                    messages, mapping = stock_messages(
                        item, condition, column_order, option_order, predicted_net[item["item_id"]],
                    )
                    stock_prompts.append(render(tokenizer, messages, args.model))
                    stock_specs.append((item, condition, column_order, option_order, mapping))
    stock_scores = score(model, tokenizer, stock_prompts, args.batch_size, args.device, token_ids)
    for (item, condition, column_order, option_order, mapping), local in zip(stock_specs, stock_scores):
        inverse = {letter: label for label, letter in mapping.items()}
        predicted = inverse[local["pred_letter"]]
        p_higher = local["prob_A"] if mapping["higher"] == "A" else local["prob_B"]
        gold = "higher" if item["storage_direction"] == "up" else "lower"
        rows.append({
            **common(item), "condition": condition, "column_order": column_order,
            "option_order": option_order, "gold_label": gold,
            "predicted_label": predicted, "prob_stock_up": p_higher,
            "correct": predicted == gold, "actual_predicted_net": predicted_net[item["item_id"]],
            **local,
        })

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
    metadata = {
        "contract_id": "018-d0-v1", "family": args.family, "model": args.model,
        "model_revision": getattr(model.config, "_commit_hash", None),
        "bank_sha256": sha256(args.bank), "bank_items": len(bank), "records": len(rows),
        "option_token_ids": token_ids, "batch_size": args.batch_size,
        "dtype": str(model.dtype), "elapsed_seconds": time.time() - started,
        "python": platform.python_version(), "torch": torch.__version__,
        "transformers": __import__("transformers").__version__,
    }
    out.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(metadata, indent=2), flush=True)


if __name__ == "__main__":
    main()
