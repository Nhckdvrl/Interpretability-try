"""Score TRUE/FALSE for one frozen checkpoint without free-form generation."""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .contracts import load_contract


ROOT = Path(__file__).resolve().parents[2]


def prompt_text(item: dict) -> str:
    return (
        "Truth can be evaluated relative to different worlds. Keep actual-world facts separate "
        "from the explicitly defined local world.\n\n"
        f"Local-world description:\n{item['context']}\n\n"
        f"Question:\n{item['question']}\n\n"
        "Answer exactly TRUE or FALSE."
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


def conditional_scores(model, tokenizer, prompts: list[str], candidate: str) -> torch.Tensor:
    candidate_ids = tokenizer.encode(" " + candidate, add_special_tokens=False)
    if not candidate_ids:
        raise ValueError(f"empty candidate tokenization: {candidate}")
    encoded_prompts = [tokenizer.encode(prompt, add_special_tokens=False) for prompt in prompts]
    sequences = [prompt_ids + candidate_ids for prompt_ids in encoded_prompts]
    max_length = max(map(len, sequences))
    pad_id = tokenizer.pad_token_id
    input_ids = torch.full((len(sequences), max_length), pad_id, dtype=torch.long)
    attention_mask = torch.zeros_like(input_ids)
    for row_index, sequence in enumerate(sequences):
        input_ids[row_index, -len(sequence) :] = torch.tensor(sequence)
        attention_mask[row_index, -len(sequence) :] = 1
    input_ids = input_ids.to("cuda")
    attention_mask = attention_mask.to("cuda")
    keep = len(candidate_ids) + 1
    logits = model(
        input_ids=input_ids,
        attention_mask=attention_mask,
        use_cache=False,
        logits_to_keep=keep,
    ).logits.float()
    prediction_logits = logits[:, -(len(candidate_ids) + 1) : -1, :]
    targets = torch.tensor(candidate_ids, device="cuda").expand(len(sequences), -1)
    token_logp = torch.log_softmax(prediction_logits, dim=-1).gather(-1, targets.unsqueeze(-1)).squeeze(-1)
    return token_logp.mean(dim=1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", required=True)
    parser.add_argument("--contract", type=Path, default=ROOT / "configs" / "d0_contract.json")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--bank", type=Path, default=ROOT / "data" / "d0_bank.jsonl")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    contract = load_contract(args.contract)
    if args.family not in contract["models"]:
        raise ValueError(f"unknown frozen family: {args.family}")
    specification = contract["models"][args.family]
    model_id, revision = specification["model_id"], specification["revision"]
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
    tokenizer.padding_side = "left"
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    label_tokens = {
        label: tokenizer.encode(" " + label, add_special_tokens=False)
        for label in contract["scoring"]["labels"]
    }
    if label_tokens["TRUE"] == label_tokens["FALSE"]:
        raise ValueError("TRUE and FALSE tokenize identically")

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
            prompts = [render(tokenizer, item) for item in batch]
            true_scores = conditional_scores(model, tokenizer, prompts, "TRUE")
            false_scores = conditional_scores(model, tokenizer, prompts, "FALSE")
            p_true = torch.sigmoid(true_scores - false_scores)
            for item, score_true, score_false, probability in zip(
                batch, true_scores.tolist(), false_scores.tolist(), p_true.tolist()
            ):
                record = {
                    **item,
                    "contract_id": contract["contract_id"],
                    "family": args.family,
                    "model_id": model_id,
                    "revision": revision,
                    "true_mean_logp": score_true,
                    "false_mean_logp": score_false,
                    "p_true": probability,
                    "prediction": "TRUE" if score_true > score_false else "FALSE",
                    "correct": ("TRUE" if score_true > score_false else "FALSE") == item["gold_label"],
                }
                if not all(math.isfinite(record[key]) for key in ("true_mean_logp", "false_mean_logp", "p_true")):
                    raise FloatingPointError(record)
                handle.write(json.dumps(record, sort_keys=True) + "\n")

    metadata = {
        "contract_id": contract["contract_id"],
        "family": args.family,
        "model_id": model_id,
        "revision": revision,
        "label_token_ids": label_tokens,
        "n_records": len(bank),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "torch_version": torch.__version__,
    }
    output.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
