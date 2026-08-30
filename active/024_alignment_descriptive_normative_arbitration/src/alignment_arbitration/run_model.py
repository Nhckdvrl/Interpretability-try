"""Deterministically score F/J decisions for one frozen base/aligned checkpoint."""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path

import torch
from huggingface_hub import model_info
from transformers import AutoModelForCausalLM, AutoTokenizer


ROOT = Path(__file__).resolve().parents[2]
PREFIX = '{"decision":"'


def game_text(item: dict) -> str:
    if item["game"] == "PD":
        rules = (
            "Prisoner's Dilemma payoffs (your points, other player's points): "
            "F/F=(5,5), F/J=(10,0), J/F=(0,10), J/J=(8,8)."
        )
    else:
        rules = (
            "Battle of the Sexes payoffs (your points, other player's points): "
            "F/F=(10,7), F/J=(0,0), J/F=(0,0), J/J=(7,10)."
        )
    if item["history"]:
        history = "\n".join(
            f"Round {row['round']}: you chose {row['human_action']}; the other player chose "
            f"{row['opponent_action']}; you received {row['human_score']} points."
            for row in item["history"]
        )
    else:
        history = "No previous rounds."
    return (
        "Predict the action taken by the human participant in the next round. "
        "Do not recommend what the participant should do.\n"
        f"{rules}\nThe game lasts exactly 10 rounds. This is round {item['round']}.\n"
        f"History:\n{history}\n"
        "Return one action, F or J, in the JSON object.\n"
    )


def render(tokenizer, item: dict, prompt_format: str) -> str:
    content = game_text(item)
    if prompt_format == "plain":
        return content + PREFIX
    messages = [
        {"role": "user", "content": content},
        {"role": "assistant", "content": PREFIX},
    ]
    kwargs = {
        "tokenize": False,
        "continue_final_message": True,
    }
    if "qwen" in tokenizer.name_or_path.lower():
        kwargs["enable_thinking"] = False
    return tokenizer.apply_chat_template(messages, **kwargs)


def token_id(tokenizer, text: str) -> int:
    ids = tokenizer.encode(text, add_special_tokens=False)
    if len(ids) != 1:
        raise ValueError(f"frozen decision token {text!r} is not atomic: {ids}")
    return ids[0]


def batches(items: list, size: int):
    for start in range(0, len(items), size):
        yield items[start : start + size]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", required=True)
    parser.add_argument("--role", required=True, choices=["base", "aligned"])
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--bank", type=Path, default=ROOT / "data" / "d0_bank.jsonl")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    contract = json.loads((ROOT / "configs" / "d0_contract.json").read_text())
    model_id = contract["models"][args.family][args.role]
    revision = model_info(model_id).sha
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
    tokenizer.padding_side = "left"
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    f_id, j_id = token_id(tokenizer, "F"), token_id(tokenizer, "J")
    if f_id == j_id:
        raise ValueError("F and J map to the same token")

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
    formats = ["plain"] if args.role == "base" else ["native", "plain"]
    output = args.output or ROOT / "results" / "d0" / f"{args.family}_{args.role}.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)

    n_written = 0
    with output.open("w", encoding="utf-8") as handle, torch.inference_mode():
        for prompt_format in formats:
            for batch in batches(bank, args.batch_size):
                rendered_format = "chat" if prompt_format == "native" else "plain"
                prompts = [render(tokenizer, item, rendered_format) for item in batch]
                encoded = tokenizer(
                    prompts,
                    return_tensors="pt",
                    padding=True,
                    add_special_tokens=False,
                ).to("cuda")
                logits = model(**encoded, use_cache=False).logits[:, -1, :].float()
                log_probs = torch.log_softmax(logits, dim=-1)
                f_logp = log_probs[:, f_id]
                j_logp = log_probs[:, j_id]
                normalized_f = torch.softmax(torch.stack([f_logp, j_logp], dim=1), dim=1)[:, 0]
                mass = torch.exp(f_logp) + torch.exp(j_logp)
                for item, p_f, p_mass in zip(batch, normalized_f.tolist(), mass.tolist()):
                    record = {
                        "contract_id": contract["contract_id"],
                        "item_id": item["item_id"],
                        "participant_id": item["participant_id"],
                        "game": item["game"],
                        "round": item["round"],
                        "human_action": item["human_action"],
                        "target_f": item["descriptive_target_f"],
                        "normative_target_f": item["normative_target_f"],
                        "family": args.family,
                        "role": args.role,
                        "model_id": model_id,
                        "revision": revision,
                        "format": prompt_format,
                        "p_f": p_f,
                        "decision_mass": p_mass,
                    }
                    if not (math.isfinite(p_f) and math.isfinite(p_mass)):
                        raise FloatingPointError(record)
                    handle.write(json.dumps(record, sort_keys=True) + "\n")
                    n_written += 1

    metadata = {
        "contract_id": contract["contract_id"],
        "family": args.family,
        "role": args.role,
        "model_id": model_id,
        "revision": revision,
        "formats": formats,
        "decision_token_ids": {"F": f_id, "J": j_id},
        "n_bank_items": len(bank),
        "n_records": n_written,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "torch_version": torch.__version__,
    }
    output.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
