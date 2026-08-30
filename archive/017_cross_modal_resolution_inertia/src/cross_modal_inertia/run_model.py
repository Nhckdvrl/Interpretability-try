"""Run the preregistered D0 conditions with one multimodal model."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch
from transformers import AutoModelForImageTextToText, AutoProcessor

from .io import read_jsonl, sha256, write_jsonl
from .prompts import displayed_gold, final_messages, original_index, text_only_messages


FINAL_CONDITIONS = (
    "simultaneous",
    "text_first_actual_label",
    "text_first_actual_ordinal",
    "text_first_masked",
    "matched_history",
    "image_first",
)


def answer_token_id(tokenizer, letter: str) -> int:
    candidates = (letter, f" {letter}")
    singletons = [(text, tokenizer.encode(text, add_special_tokens=False)) for text in candidates]
    for _, ids in singletons:
        if len(ids) == 1:
            return ids[0]
    raise ValueError(f"no single-token representation for {letter}: {singletons}")


def resolve_images(item: dict, images_root: Path) -> dict:
    resolved = dict(item)
    path = (images_root / item["image_path"]).resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    if sha256(path) != item["image_sha256"]:
        raise RuntimeError(f"image hash mismatch: {path}")
    resolved["image_path"] = str(path)
    return resolved


@torch.inference_mode()
def score_batches(model, processor, conversations: list[list[dict]], batch_size: int) -> list[dict]:
    tokenizer = processor.tokenizer
    token_a = answer_token_id(tokenizer, "A")
    token_b = answer_token_id(tokenizer, "B")
    output: list[dict] = []
    for start in range(0, len(conversations), batch_size):
        batch = conversations[start:start + batch_size]
        inputs = processor.apply_chat_template(
            batch,
            add_generation_prompt=True,
            tokenize=True,
            padding=True,
            return_dict=True,
            return_tensors="pt",
        )
        device = next(model.parameters()).device
        inputs = {key: value.to(device) if hasattr(value, "to") else value
                  for key, value in inputs.items()}
        logits = model(**inputs).logits[:, -1, :]
        pair = torch.stack((logits[:, token_a], logits[:, token_b]), dim=-1).float()
        probs = torch.softmax(pair, dim=-1).cpu().tolist()
        for p_a, p_b in probs:
            output.append({
                "prob_A": p_a,
                "prob_B": p_b,
                "pred_letter": "A" if p_a >= p_b else "B",
            })
    return output


def base_record(item: dict, order: str, condition: str, score: dict) -> dict:
    pred = score["pred_letter"]
    gold = displayed_gold(item, order)
    return {
        "item_id": item["item_id"],
        "source_id": item["source_id"],
        "pair_id": item["pair_id"],
        "language": item["language"],
        "order": order,
        "condition": condition,
        "gold_letter": gold,
        "gold_original_index": item["gold_index"],
        "pred_letter": pred,
        "pred_original_index": original_index(pred, order),
        "prob_A": score["prob_A"],
        "prob_B": score["prob_B"],
        "prob_gold": score["prob_A"] if gold == "A" else score["prob_B"],
        "image_sha256": item["image_sha256"],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--family", required=True, choices=("qwen", "gemma", "llama"))
    ap.add_argument("--bank", default="data/d0_v1/d0_bank.jsonl")
    ap.add_argument("--images", default="data/mucar_images")
    ap.add_argument("--output", required=True)
    ap.add_argument("--batch-size", type=int, default=4)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    started = time.time()
    bank = read_jsonl(args.bank)
    if args.limit:
        bank = bank[:args.limit]
    images_root = Path(args.images)
    resolved = [resolve_images(item, images_root) for item in bank]

    processor = AutoProcessor.from_pretrained(args.model, local_files_only=True)
    processor.tokenizer.padding_side = "left"
    if processor.tokenizer.pad_token_id is None:
        processor.tokenizer.pad_token = processor.tokenizer.eos_token
    model = AutoModelForImageTextToText.from_pretrained(
        args.model,
        torch_dtype=torch.bfloat16,
        device_map=args.device,
        local_files_only=True,
    ).eval()

    keys = [(item, order) for item in resolved for order in ("canonical", "reversed")]
    initial_scores = score_batches(
        model, processor,
        [text_only_messages(item, order) for item, order in keys],
        args.batch_size,
    )
    initial_records = [base_record(item, order, "text_only", score)
                       for (item, order), score in zip(keys, initial_scores)]

    rows = list(initial_records)
    for condition in FINAL_CONDITIONS:
        conversations = [
            final_messages(item, order, condition, initial["pred_letter"])
            for (item, order), initial in zip(keys, initial_records)
        ]
        scores = score_batches(model, processor, conversations, args.batch_size)
        for (item, order), initial, score in zip(keys, initial_records, scores):
            row = base_record(item, order, condition, score)
            row["initial_letter"] = initial["pred_letter"]
            row["initial_original_index"] = initial["pred_original_index"]
            rows.append(row)
        print(json.dumps({"family": args.family, "condition": condition,
                          "completed": len(scores)}, sort_keys=True), flush=True)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(out, rows)
    config = getattr(model, "config", None)
    metadata = {
        "contract_id": "017-d0-v1",
        "family": args.family,
        "model": args.model,
        "model_commit": getattr(config, "_commit_hash", None),
        "bank_sha256": sha256(args.bank),
        "bank_items": len(bank),
        "records": len(rows),
        "answer_token_ids": {
            "A": answer_token_id(processor.tokenizer, "A"),
            "B": answer_token_id(processor.tokenizer, "B"),
        },
        "dtype": str(getattr(model, "dtype", None)),
        "elapsed_seconds": time.time() - started,
    }
    out.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(metadata, indent=2), flush=True)


if __name__ == "__main__":
    main()
