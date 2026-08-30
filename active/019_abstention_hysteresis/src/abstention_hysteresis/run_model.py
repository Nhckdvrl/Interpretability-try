"""Run capability, initial-abstention, and matched final-history conditions."""
from __future__ import annotations

import argparse
import json
import platform
import re
import time
from collections import Counter
from pathlib import Path

from .build_bank import normalize
from .io import read_jsonl, sha256_file, write_jsonl
from .prompts import messages


HISTORY_CONDITIONS = (
    "self_abstention",
    "teacher_abstention",
    "paraphrased_abstention",
    "neutral_same_context",
    "answered_history",
)
MODE_CONTINUATIONS = ("ANSWER", "ABSTAIN")
ABSTENTION_PATTERNS = (
    r"^\s*abstain\b",
    r"\bcannot determine\b",
    r"\bcannot answer\b",
    r"\bcan(?:not|'t) be determined\b",
    r"\binsufficient (?:information|evidence)\b",
    r"\bnot enough (?:information|evidence)\b",
    r"\bunable to (?:determine|answer)\b",
)


def render(tokenizer, conversation: list[dict], model_name: str) -> str:
    kwargs = {"tokenize": False, "add_generation_prompt": True}
    if "qwen" in model_name.casefold():
        kwargs["enable_thinking"] = False
    return tokenizer.apply_chat_template(conversation, **kwargs)


def is_abstention(response: str) -> bool:
    text = response.casefold().strip()
    return any(re.search(pattern, text) for pattern in ABSTENTION_PATTERNS)


def extracted_answer(response: str) -> str:
    if is_abstention(response):
        return ""
    text = response.strip()
    text = re.sub(r"^\s*(?:answer\s*:|final answer\s*:)", "", text,
                  flags=re.IGNORECASE).strip()
    return text.splitlines()[0].strip()


def answer_scores(response: str, item: dict) -> tuple[bool, float, bool]:
    prediction = normalize(extracted_answer(response))
    golds = {normalize(item["answer"]), *(normalize(alias) for alias in item["answer_aliases"])}
    exact = bool(prediction) and prediction in golds
    prediction_tokens = prediction.split()
    best_f1 = 0.0
    for gold in golds:
        gold_tokens = gold.split()
        common = sum((Counter(prediction_tokens) & Counter(gold_tokens)).values())
        if common:
            precision = common / len(prediction_tokens)
            recall = common / len(gold_tokens)
            best_f1 = max(best_f1, 2 * precision * recall / (precision + recall))
    return exact, best_f1, exact or best_f1 >= .80


def generate(model, tokenizer, prompts: list[str], batch_size: int, device: str,
             max_new_tokens: int) -> list[str]:
    import torch

    outputs = []
    with torch.inference_mode():
        for start in range(0, len(prompts), batch_size):
            batch = tokenizer(prompts[start:start + batch_size], return_tensors="pt", padding=True,
                              add_special_tokens=False).to(device)
            prompt_width = batch["input_ids"].shape[1]
            generated = model.generate(
                **batch,
                do_sample=False,
                max_new_tokens=max_new_tokens,
                pad_token_id=tokenizer.pad_token_id,
            )
            outputs.extend(tokenizer.batch_decode(generated[:, prompt_width:], skip_special_tokens=True))
    return [response.strip() for response in outputs]


def validate_continuations(tokenizer, prompts: list[str]) -> None:
    for prompt in prompts[:20]:
        base = tokenizer.encode(prompt, add_special_tokens=False)
        for continuation in MODE_CONTINUATIONS:
            combined = tokenizer.encode(prompt + continuation, add_special_tokens=False)
            if combined[:len(base)] != base or not combined[len(base):]:
                raise ValueError(f"continuation tokenization is not append-only: {continuation}")


def mode_probabilities(model, tokenizer, prompts: list[str], batch_size: int,
                       device: str) -> list[dict]:
    """Length-normalized continuation scores for ANSWER versus ABSTAIN."""
    import torch

    validate_continuations(tokenizer, prompts)
    paired = []
    lengths = []
    for prompt in prompts:
        base = tokenizer.encode(prompt, add_special_tokens=False)
        for continuation in MODE_CONTINUATIONS:
            combined = tokenizer.encode(prompt + continuation, add_special_tokens=False)
            continuation_ids = combined[len(base):]
            paired.append(prompt + continuation)
            lengths.append((len(continuation_ids), continuation_ids))

    mean_scores = []
    with torch.inference_mode():
        for start in range(0, len(paired), batch_size):
            texts = paired[start:start + batch_size]
            local_lengths = lengths[start:start + batch_size]
            batch = tokenizer(texts, return_tensors="pt", padding=True,
                              add_special_tokens=False).to(device)
            keep = max(length for length, _ in local_lengths) + 1
            logits = model(**batch, use_cache=False, logits_to_keep=keep).logits.float()
            log_probs = torch.log_softmax(logits, dim=-1)
            for row_index, (length, token_ids) in enumerate(local_lengths):
                positions = log_probs[row_index, -(length + 1):-1]
                targets = torch.tensor(token_ids, device=positions.device)
                mean_scores.append(float(positions.gather(1, targets[:, None]).mean().cpu()))

    output = []
    for index in range(0, len(mean_scores), 2):
        answer_score, abstain_score = mean_scores[index:index + 2]
        maximum = max(answer_score, abstain_score)
        answer_weight = pow(2.718281828459045, answer_score - maximum)
        abstain_weight = pow(2.718281828459045, abstain_score - maximum)
        output.append({
            "answer_mode_mean_logp": answer_score,
            "abstain_mode_mean_logp": abstain_score,
            "prob_abstain_mode": abstain_weight / (answer_weight + abstain_weight),
        })
    return output


def common(item: dict) -> dict:
    return {key: item[key] for key in (
        "item_id", "source", "source_id", "stratum", "question", "answer",
    )}


def make_row(item: dict, condition: str, response: str, mode: dict | None) -> dict:
    exact, token_f1, correct = answer_scores(response, item)
    return {
        **common(item),
        "condition": condition,
        "response": response,
        "predicted_answer": extracted_answer(response),
        "is_abstention": is_abstention(response),
        "exact_match": exact,
        "token_f1": token_f1,
        "correct": correct,
        **(mode or {"answer_mode_mean_logp": None, "abstain_mode_mean_logp": None,
                    "prob_abstain_mode": None}),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--family", required=True, choices=("qwen", "gemma", "llama"))
    parser.add_argument("--bank", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--score-batch-size", type=int, default=8)
    parser.add_argument("--max-new-tokens", type=int, default=32)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

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
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        local_files_only=True,
        dtype=torch.bfloat16,
        attn_implementation="sdpa",
        device_map={"": args.device},
    ).eval()

    phase_conditions = ("capability_full", "initial_missing", "direct_full")
    phase_prompts, phase_specs = [], []
    for item in bank:
        for condition in phase_conditions:
            phase_prompts.append(render(tokenizer, messages(item, condition), args.model))
            phase_specs.append((item, condition))
    phase_responses = generate(model, tokenizer, phase_prompts, args.batch_size, args.device,
                               args.max_new_tokens)
    scored_indices = [index for index, (_, condition) in enumerate(phase_specs)
                      if condition != "capability_full"]
    phase_modes = mode_probabilities(
        model, tokenizer, [phase_prompts[index] for index in scored_indices],
        args.score_batch_size, args.device,
    )
    mode_by_index = dict(zip(scored_indices, phase_modes))
    rows = [
        make_row(item, condition, response, mode_by_index.get(index))
        for index, ((item, condition), response) in enumerate(zip(phase_specs, phase_responses))
    ]
    by_key = {(row["item_id"], row["condition"]): row for row in rows}
    gated = [item for item in bank
             if by_key[item["item_id"], "capability_full"]["correct"]
             and by_key[item["item_id"], "initial_missing"]["is_abstention"]]
    print(json.dumps({"family": args.family, "phase": "gate", "bank": len(bank),
                      "gated": len(gated)}), flush=True)

    history_prompts, history_specs = [], []
    for item in gated:
        initial_response = by_key[item["item_id"], "initial_missing"]["response"]
        for condition in HISTORY_CONDITIONS:
            history_prompts.append(render(
                tokenizer, messages(item, condition, initial_response), args.model,
            ))
            history_specs.append((item, condition))
    if history_prompts:
        history_responses = generate(
            model, tokenizer, history_prompts, args.batch_size, args.device, args.max_new_tokens,
        )
        history_modes = mode_probabilities(
            model, tokenizer, history_prompts, args.score_batch_size, args.device,
        )
        rows.extend(
            make_row(item, condition, response, mode)
            for (item, condition), response, mode
            in zip(history_specs, history_responses, history_modes)
        )

    write_jsonl(args.output, rows)
    metadata = {
        "contract_id": "019-d0-v1",
        "family": args.family,
        "model": args.model,
        "model_revision": getattr(model.config, "_commit_hash", None),
        "bank_sha256": sha256_file(args.bank),
        "bank_items": len(bank),
        "gated_items": len(gated),
        "records": len(rows),
        "batch_size": args.batch_size,
        "score_batch_size": args.score_batch_size,
        "max_new_tokens": args.max_new_tokens,
        "dtype": str(model.dtype),
        "elapsed_seconds": time.time() - started,
        "python": platform.python_version(),
        "torch": torch.__version__,
        "transformers": __import__("transformers").__version__,
    }
    destination = Path(args.output)
    destination.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(metadata, indent=2), flush=True)


if __name__ == "__main__":
    main()
