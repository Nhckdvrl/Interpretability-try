from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence
import math


@dataclass(frozen=True)
class ScoreResult:
    logprobs: dict[str, float]
    probs: dict[str, float]


def softmax_dict(logprobs: dict[str, float]) -> dict[str, float]:
    if not logprobs:
        raise ValueError("logprobs cannot be empty")
    m = max(logprobs.values())
    exps = {k: math.exp(v - m) for k, v in logprobs.items()}
    z = sum(exps.values())
    return {k: v / z for k, v in exps.items()}


class HFChoiceScorer:
    """Exact continuation scorer for local Hugging Face causal LMs.

    It never uses an LLM judge. The cache is lifetime-scoped so repeated identical
    prompt/candidate requests receive the exact same stored score even if low-level
    kernels are not perfectly deterministic across batches.
    """

    def __init__(self, model_name: str, *, revision: str | None = None,
                 device_map: str = "auto", dtype: str = "auto") -> None:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, revision=revision, trust_remote_code=True
        )
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        dtype_arg = dtype if dtype == "auto" else getattr(torch, dtype)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            revision=revision,
            device_map=device_map,
            torch_dtype=dtype_arg,
            trust_remote_code=True,
        )
        self.model.eval()
        self._cache: dict[tuple[str, str], float] = {}

    def _prefix(self, user_text: str) -> str:
        messages = [{"role": "user", "content": user_text}]
        if getattr(self.tokenizer, "chat_template", None):
            kwargs = dict(tokenize=False, add_generation_prompt=True)
            try:
                return self.tokenizer.apply_chat_template(messages, enable_thinking=False, **kwargs)
            except TypeError:
                return self.tokenizer.apply_chat_template(messages, **kwargs)
        return f"USER: {user_text}\nASSISTANT:"

    def _encode_pair(self, prompt: str, candidate: str) -> tuple[list[int], int]:
        if not candidate:
            raise ValueError("candidate cannot be empty")
        prefix = self._prefix(prompt)
        prefix_ids = self.tokenizer(prefix, add_special_tokens=False).input_ids
        full_ids = self.tokenizer(prefix + candidate, add_special_tokens=False).input_ids
        if not prefix_ids or len(full_ids) <= len(prefix_ids) or full_ids[:len(prefix_ids)] != prefix_ids:
            raise ValueError(
                f"candidate {candidate!r} changes the prompt tokenization boundary; "
                "do not silently add whitespace to fix this"
            )
        return full_ids, len(prefix_ids)

    def score_batch(self, requests: Sequence[tuple[str, tuple[str, ...]]], *,
                    sequence_batch_size: int = 64) -> list[ScoreResult]:
        if sequence_batch_size <= 0:
            raise ValueError("sequence_batch_size must be > 0")
        per_request: list[dict[str, float]] = [{} for _ in requests]
        pending: dict[tuple[str, str], list[tuple[int, str]]] = {}
        for req_idx, (prompt, candidates) in enumerate(requests):
            if len(candidates) < 2 or len(set(candidates)) != len(candidates):
                raise ValueError("each request needs at least two unique candidates")
            for candidate in candidates:
                key = (prompt, candidate)
                if key in self._cache:
                    per_request[req_idx][candidate] = self._cache[key]
                else:
                    pending.setdefault(key, []).append((req_idx, candidate))

        flat = []
        for key, destinations in pending.items():
            ids, prefix_len = self._encode_pair(*key)
            flat.append((key, destinations, ids, prefix_len))

        input_device = self.model.get_input_embeddings().weight.device
        torch = self.torch
        for start in range(0, len(flat), sequence_batch_size):
            chunk = flat[start:start + sequence_batch_size]
            if not chunk:
                continue
            max_len = max(len(x[2]) for x in chunk)
            ids_batch: list[list[int]] = []
            masks: list[list[int]] = []
            meta = []
            for key, destinations, ids, prefix_len in chunk:
                pad = max_len - len(ids)
                ids_batch.append(ids + [self.tokenizer.pad_token_id] * pad)
                masks.append([1] * len(ids) + [0] * pad)
                meta.append((key, destinations, prefix_len, len(ids)))
            input_ids = torch.tensor(ids_batch, device=input_device)
            attention_mask = torch.tensor(masks, device=input_device)
            with torch.inference_mode():
                logits = self.model(input_ids=input_ids, attention_mask=attention_mask).logits
            for row_idx, (key, destinations, prefix_len, seq_len) in enumerate(meta):
                total = 0.0
                for pos in range(prefix_len, seq_len):
                    token_id = ids_batch[row_idx][pos]
                    total += float(
                        torch.log_softmax(logits[row_idx, pos - 1].float(), dim=-1)[token_id].item()
                    )
                self._cache[key] = total
                for req_idx, candidate in destinations:
                    per_request[req_idx][candidate] = total

        return [ScoreResult(scores, softmax_dict(scores)) for scores in per_request]
