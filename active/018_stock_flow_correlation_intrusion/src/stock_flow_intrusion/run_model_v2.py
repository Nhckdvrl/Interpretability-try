"""Run the frozen D0-v2 semantic-recognition measurement repair."""
from __future__ import annotations

import argparse
import json
import platform
import time
from collections import defaultdict
from pathlib import Path

from .io import read_jsonl, sha256
from .prompts import net_semantic_messages, stock_messages_v2
from .run_model import COLUMN_ORDERS, CONDITIONS, OPTION_ORDERS, common


CONTRACT_ID = "018-d0-v2-semantic-recognition"
SEMANTIC_LABELS = ("positive", "negative")


def render_ids(tokenizer, messages: list[dict], model_name: str) -> list[int]:
    """Render directly to IDs, avoiding decode/re-encode chat-template drift."""
    kwargs = {"tokenize": True, "add_generation_prompt": True}
    if "qwen" in model_name.casefold():
        kwargs["enable_thinking"] = False
    ids = tokenizer.apply_chat_template(messages, **kwargs)
    if ids and isinstance(ids[0], list):
        raise ValueError("expected one unbatched chat template")
    return list(ids)


def single_token_candidates(tokenizer, candidates: tuple[str, ...]) -> dict[str, int]:
    result = {}
    for candidate in candidates:
        ids = tokenizer.encode(candidate, add_special_tokens=False)
        if len(ids) != 1:
            raise ValueError(f"semantic response {candidate!r} is not one token: {ids}")
        result[candidate] = ids[0]
    if len(set(result.values())) != len(result):
        raise ValueError(f"candidate tokens collide: {result}")
    return result


def score_ids(model, prompt_ids: list[list[int]], batch_size: int, device: str,
              candidate_ids: dict[str, int]) -> list[dict]:
    import torch

    labels = list(candidate_ids)
    indices = [candidate_ids[label] for label in labels]
    pad_id = model.config.pad_token_id
    if pad_id is None:
        raise ValueError("model.config.pad_token_id must be set before scoring")
    output = []
    with torch.inference_mode():
        for start in range(0, len(prompt_ids), batch_size):
            local = prompt_ids[start:start + batch_size]
            width = max(map(len, local))
            input_ids = torch.full((len(local), width), pad_id, dtype=torch.long)
            attention = torch.zeros((len(local), width), dtype=torch.long)
            for row, ids in enumerate(local):
                input_ids[row, width - len(ids):] = torch.tensor(ids)
                attention[row, width - len(ids):] = 1
            logits = model(
                input_ids=input_ids.to(device), attention_mask=attention.to(device),
                use_cache=False, logits_to_keep=1,
            ).logits[:, -1, indices].float()
            probabilities = torch.softmax(logits, dim=-1).cpu().tolist()
            for values in probabilities:
                record = {f"prob_{label}": value for label, value in zip(labels, values)}
                record["predicted_label"] = labels[max(range(len(values)), key=values.__getitem__)]
                output.append(record)
    return output


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--family", required=True)
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

    semantic_ids = single_token_candidates(tokenizer, SEMANTIC_LABELS)
    letter_ids = single_token_candidates(tokenizer, ("A", "B"))
    model = AutoModelForCausalLM.from_pretrained(
        args.model, local_files_only=True, dtype=torch.bfloat16,
        attn_implementation="sdpa", device_map={"": args.device},
    ).eval()
    model.config.pad_token_id = tokenizer.pad_token_id

    net_prompt_ids, net_specs = [], []
    for item in bank:
        for column_order in COLUMN_ORDERS:
            net_prompt_ids.append(render_ids(
                tokenizer, net_semantic_messages(item, column_order), args.model,
            ))
            net_specs.append((item, column_order))
    net_scores = score_ids(model, net_prompt_ids, args.batch_size, args.device, semantic_ids)

    rows = []
    probabilities: dict[str, list[float]] = defaultdict(list)
    for (item, column_order), local in zip(net_specs, net_scores):
        probabilities[item["item_id"]].append(local["prob_positive"])
        rows.append({
            **common(item), "condition": "net_recognition_v2", "column_order": column_order,
            "gold_label": item["net_direction"],
            "correct": local["predicted_label"] == item["net_direction"], **local,
        })
    mean_positive = {
        item_id: sum(values) / len(values) for item_id, values in probabilities.items()
    }
    predicted_net = {
        item_id: "positive" if value >= 0.5 else "negative"
        for item_id, value in mean_positive.items()
    }
    print(json.dumps({"family": args.family, "condition": "net_recognition_v2",
                      "completed": len(net_scores)}), flush=True)

    stock_prompt_ids, stock_specs = [], []
    for item in bank:
        for condition in CONDITIONS:
            for column_order in COLUMN_ORDERS:
                for option_order in OPTION_ORDERS:
                    messages, mapping = stock_messages_v2(
                        item, condition, column_order, option_order,
                        predicted_net[item["item_id"]],
                    )
                    stock_prompt_ids.append(render_ids(tokenizer, messages, args.model))
                    stock_specs.append((item, condition, column_order, option_order, mapping))
    stock_scores = score_ids(model, stock_prompt_ids, args.batch_size, args.device, letter_ids)
    for (item, condition, column_order, option_order, mapping), local in zip(stock_specs, stock_scores):
        inverse = {letter: label for label, letter in mapping.items()}
        predicted = inverse[local["predicted_label"]]
        p_higher = local["prob_A"] if mapping["higher"] == "A" else local["prob_B"]
        gold = "higher" if item["storage_direction"] == "up" else "lower"
        rows.append({
            **common(item), "condition": condition, "column_order": column_order,
            "option_order": option_order, "gold_label": gold,
            "predicted_label": predicted, "prob_stock_up": p_higher,
            "correct": predicted == gold,
            "actual_predicted_net": predicted_net[item["item_id"]],
            "recognition_mean_prob_positive": mean_positive[item["item_id"]],
            "prob_A": local["prob_A"], "prob_B": local["prob_B"],
        })

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
    metadata = {
        "contract_id": CONTRACT_ID, "family": args.family, "model": args.model,
        "model_revision": getattr(model.config, "_commit_hash", None),
        "bank_sha256": sha256(args.bank), "bank_items": len(bank), "records": len(rows),
        "semantic_token_ids": semantic_ids, "letter_token_ids": letter_ids,
        "batch_size": args.batch_size, "dtype": str(model.dtype),
        "elapsed_seconds": time.time() - started, "python": platform.python_version(),
        "torch": torch.__version__, "transformers": __import__("transformers").__version__,
    }
    out.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(metadata, indent=2), flush=True)


if __name__ == "__main__":
    main()
