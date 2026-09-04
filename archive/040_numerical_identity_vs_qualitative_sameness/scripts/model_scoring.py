"""Small deterministic causal-LM choice scorer shared by 040 scripts."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def resolve_snapshot(model_name: str) -> tuple[str, str | None]:
    cache = Path("/home/xiang/.cache/huggingface/hub")
    model_dir = cache / ("models--" + model_name.replace("/", "--"))
    ref = model_dir / "refs" / "main"
    revision = ref.read_text().strip() if ref.exists() else None
    return model_name, revision


def load_model(model_name: str, dtype: str = "bfloat16"):
    torch_dtype = getattr(torch, dtype)
    tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        local_files_only=True,
        dtype=torch_dtype,
        device_map={"": "cuda:0"},
        low_cpu_mem_usage=True,
    )
    model.eval()
    return tokenizer, model


def format_chat(tokenizer, user_text: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "Answer the final multiple-choice question using only A or B. Do not explain.",
        },
        {"role": "user", "content": user_text},
    ]
    kwargs = {"tokenize": False, "add_generation_prompt": True}
    try:
        return tokenizer.apply_chat_template(messages, enable_thinking=False, **kwargs)
    except TypeError:
        return tokenizer.apply_chat_template(messages, **kwargs)


@torch.inference_mode()
def score_variable_choices(
    tokenizer,
    model,
    prompts: Iterable[str],
    candidate_lists: list[list[str]],
    batch_size: int = 8,
):
    """Return summed conditional log probabilities for variable candidate sets."""
    prompts = list(prompts)
    if len(prompts) != len(candidate_lists):
        raise ValueError("prompts and candidate_lists must align")
    flat = []
    for prompt_index, (prompt, candidates) in enumerate(zip(prompts, candidate_lists)):
        prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
        for candidate_index, candidate in enumerate(candidates):
            full_ids = tokenizer(prompt + candidate, add_special_tokens=False)["input_ids"]
            if full_ids[: len(prompt_ids)] != prompt_ids:
                raise ValueError("Candidate tokenization changed the prompt boundary")
            continuation = full_ids[len(prompt_ids) :]
            flat.append((prompt_index, candidate_index, candidate, prompt_ids, continuation, full_ids))
    output = [[None for _ in candidates] for candidates in candidate_lists]
    device = model.device
    pad_id = tokenizer.pad_token_id
    for start_index in range(0, len(flat), batch_size):
        batch = flat[start_index : start_index + batch_size]
        max_len = max(len(x[5]) for x in batch)
        input_ids, attention = [], []
        for *_, full_ids in batch:
            padding = max_len - len(full_ids)
            input_ids.append(full_ids + [pad_id] * padding)
            attention.append([1] * len(full_ids) + [0] * padding)
        ids = torch.tensor(input_ids, device=device)
        mask = torch.tensor(attention, device=device)
        logits = model(input_ids=ids, attention_mask=mask, use_cache=False).logits
        for batch_index, (prompt_index, candidate_index, candidate, prompt_ids, continuation, _) in enumerate(batch):
            first = len(prompt_ids) - 1
            token_logits = logits[batch_index, first : first + len(continuation)]
            target = torch.tensor(continuation, device=device)
            score = token_logits.log_softmax(dim=-1).gather(-1, target[:, None]).sum().item()
            output[prompt_index][candidate_index] = {
                "candidate": candidate,
                "logprob": score,
                "token_count": len(continuation),
                "token_ids": continuation,
            }
    return output


def score_choices(tokenizer, model, prompts: Iterable[str], candidates: list[str], batch_size: int = 8):
    prompts = list(prompts)
    return score_variable_choices(tokenizer, model, prompts, [candidates] * len(prompts), batch_size)


def stable_id(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
