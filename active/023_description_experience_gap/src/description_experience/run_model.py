"""Score all frozen choice/capability candidates for one checkpoint."""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


ROOT = Path(__file__).resolve().parents[2]


def prompt_text(item: dict) -> str:
    candidate_text = ", ".join(item["candidates"])
    return (
        "Treat payoffs as numerical points. Do not invent outcomes or probabilities that are not shown.\n\n"
        f"{item['stimulus']}\n\n"
        f"Question: {item['question']}\n"
        f"Answer exactly one of: {candidate_text}."
    )


def render(tokenizer, item: dict) -> str:
    messages = [
        {"role": "user", "content": prompt_text(item)},
        {"role": "assistant", "content": "Answer:"},
    ]
    kwargs = {"tokenize": False, "continue_final_message": True}
    if "qwen" in tokenizer.name_or_path.lower():
        kwargs["enable_thinking"] = False
    return tokenizer.apply_chat_template(messages, **kwargs)


def chunks(items: list, size: int):
    for start in range(0, len(items), size):
        yield items[start : start + size]


def score_pairs(model, tokenizer, prompts: list[str], candidates: list[str]) -> torch.Tensor:
    prompt_ids = [tokenizer.encode(prompt, add_special_tokens=False) for prompt in prompts]
    candidate_ids = [tokenizer.encode(" " + candidate, add_special_tokens=False) for candidate in candidates]
    if any(not ids for ids in candidate_ids):
        raise ValueError("empty candidate tokenization")
    sequences = [prefix + suffix for prefix, suffix in zip(prompt_ids, candidate_ids)]
    max_length = max(map(len, sequences))
    input_ids = torch.full((len(sequences), max_length), tokenizer.pad_token_id, dtype=torch.long)
    attention_mask = torch.zeros_like(input_ids)
    for row_index, sequence in enumerate(sequences):
        input_ids[row_index, -len(sequence) :] = torch.tensor(sequence)
        attention_mask[row_index, -len(sequence) :] = 1
    max_candidate_length = max(map(len, candidate_ids))
    logits = model(
        input_ids=input_ids.to("cuda"),
        attention_mask=attention_mask.to("cuda"),
        use_cache=False,
        logits_to_keep=max_candidate_length + 1,
    ).logits.float()
    scores = []
    for row_index, ids in enumerate(candidate_ids):
        length = len(ids)
        prediction_logits = logits[row_index, -(length + 1) : -1, :]
        targets = torch.tensor(ids, device="cuda")
        token_logp = torch.log_softmax(prediction_logits, dim=-1).gather(-1, targets[:, None]).squeeze(-1)
        scores.append(token_logp.mean())
    return torch.stack(scores)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", required=True)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--bank", type=Path, default=ROOT / "data" / "d0_bank.jsonl")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    contract = json.loads((ROOT / "configs" / "d0_contract.json").read_text())
    specification = contract["models"].get(args.family)
    if specification is None:
        raise ValueError(f"unknown frozen family: {args.family}")
    model_id, revision = specification["model_id"], specification["revision"]
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
    tokenizer.padding_side = "left"
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        revision=revision,
        dtype=torch.bfloat16,
        attn_implementation="sdpa",
        low_cpu_mem_usage=True,
    ).to("cuda")
    model.eval()
    with args.bank.open(encoding="utf-8") as handle:
        bank = [json.loads(line) for line in handle]
    if args.limit is not None:
        bank = bank[: args.limit]
    output = args.output or ROOT / "results" / "d0" / f"{args.family}.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as handle, torch.inference_mode():
        for batch in chunks(bank, args.batch_size):
            expanded_prompts, expanded_candidates, slices = [], [], []
            for item in batch:
                prompt = render(tokenizer, item)
                start = len(expanded_candidates)
                expanded_prompts.extend([prompt] * len(item["candidates"]))
                expanded_candidates.extend(item["candidates"])
                slices.append((start, len(expanded_candidates)))
            scores = score_pairs(model, tokenizer, expanded_prompts, expanded_candidates)
            for item, (start, end) in zip(batch, slices):
                item_scores = scores[start:end]
                probabilities = torch.softmax(item_scores, dim=0)
                score_map = {candidate: score for candidate, score in zip(item["candidates"], item_scores.tolist())}
                probability_map = {candidate: probability for candidate, probability in zip(item["candidates"], probabilities.tolist())}
                prediction = item["candidates"][int(torch.argmax(item_scores).item())]
                record = {
                    **item,
                    "contract_id": contract["contract_id"],
                    "family": args.family,
                    "model_id": model_id,
                    "revision": revision,
                    "candidate_mean_logp": score_map,
                    "candidate_probability": probability_map,
                    "prediction": prediction,
                    "correct": None if item["gold_label"] is None else prediction == item["gold_label"],
                    "p_target": probability_map[item["target_display_label"]] if item["query_type"] == "choice" else None,
                }
                if not all(math.isfinite(value) for value in score_map.values()):
                    raise FloatingPointError(record)
                handle.write(json.dumps(record, sort_keys=True) + "\n")
    unique_candidates = sorted({candidate for item in bank for candidate in item["candidates"]})
    metadata = {
        "contract_id": contract["contract_id"],
        "family": args.family,
        "model_id": model_id,
        "revision": revision,
        "n_records": len(bank),
        "candidate_token_ids": {candidate: tokenizer.encode(" " + candidate, add_special_tokens=False) for candidate in unique_candidates},
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "torch_version": torch.__version__,
    }
    output.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
