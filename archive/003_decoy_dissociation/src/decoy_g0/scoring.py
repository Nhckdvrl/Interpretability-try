from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, Sequence

@dataclass(frozen=True)
class ScoreResult:
    logprobs: dict[str, float]
    probs: dict[str, float]


def softmax_dict(logprobs: dict[str, float]) -> dict[str, float]:
    m = max(logprobs.values())
    exps = {k: math.exp(v - m) for k, v in logprobs.items()}
    z = sum(exps.values())
    return {k: v / z for k, v in exps.items()}


class HFChoiceScorer:
    """Deterministic teacher-forced scoring of complete candidate strings.

    Candidate strings may tokenize to multiple tokens. `score_batch` flattens all
    prompt/candidate pairs into padded batches, so the full G0 does not require
    hundreds of thousands of separate model forwards.
    """

    def __init__(self, model_name: str, device_map: str = "auto", dtype: str = "auto"):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        dtype_arg = dtype if dtype == "auto" else getattr(torch, dtype)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device_map,
            torch_dtype=dtype_arg,
            trust_remote_code=True,
        )
        self.model.eval()
        self._score_cache: dict[tuple[str, str], float] = {}

    def _chat_prefix(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        if hasattr(self.tokenizer, "apply_chat_template") and self.tokenizer.chat_template:
            # Qwen3 accepts enable_thinking=False; templates that do not reference
            # this variable simply ignore the extra Jinja argument.
            return self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=False,
            )
        return prompt.rstrip() + "\nAnswer:\n"

    def _encode_pair(self, prompt: str, candidate: str) -> tuple[list[int], int]:
        prefix = self._chat_prefix(prompt)
        prefix_ids = self.tokenizer(prefix, add_special_tokens=False).input_ids
        # Score the candidate exactly as supplied. In particular, do not insert a
        # leading space: chat templates already provide a generation boundary,
        # and " A" can be a completely different token from the requested "A".
        full_ids = self.tokenizer(prefix + candidate, add_special_tokens=False).input_ids
        if not prefix_ids or len(full_ids) <= len(prefix_ids):
            raise ValueError(f"candidate {candidate!r} produced invalid continuation tokens")
        if full_ids[: len(prefix_ids)] != prefix_ids:
            raise ValueError(f"candidate {candidate!r} changed the prompt tokenization boundary")
        return full_ids, len(prefix_ids)

    def score_batch(
        self,
        requests: Sequence[tuple[str, Sequence[str]]],
        sequence_batch_size: int = 96,
    ) -> list[ScoreResult]:
        torch = self.torch
        # Identical prompts occur across mirror targets and decoy strengths. Score
        # each continuation once over the scorer's full lifetime, both to save
        # work and to prevent padding-shape-dependent numerical differences.
        pending: dict[tuple[str, str], list[tuple[int, str]]] = {}
        per_request: list[dict[str, float]] = [dict() for _ in requests]
        for req_idx, (prompt, candidates) in enumerate(requests):
            for cand in candidates:
                cache_key = (prompt, cand)
                if cache_key in self._score_cache:
                    per_request[req_idx][cand] = self._score_cache[cache_key]
                else:
                    pending.setdefault(cache_key, []).append((req_idx, cand))

        flat = []
        for cache_key, destinations in pending.items():
            ids, prefix_len = self._encode_pair(*cache_key)
            flat.append((cache_key, destinations, ids, prefix_len))
        device = next(self.model.parameters()).device

        for start in range(0, len(flat), sequence_batch_size):
            chunk = flat[start : start + sequence_batch_size]
            max_len = max(len(x[2]) for x in chunk)
            input_ids = []
            attention_mask = []
            metadata = []
            for cache_key, destinations, ids, prefix_len in chunk:
                pad = max_len - len(ids)
                # Right padding keeps prefix/candidate positions unchanged.
                input_ids.append(ids + [self.tokenizer.pad_token_id] * pad)
                attention_mask.append([1] * len(ids) + [0] * pad)
                metadata.append((cache_key, destinations, prefix_len, len(ids)))

            input_ids_t = torch.tensor(input_ids, device=device)
            attention_mask_t = torch.tensor(attention_mask, device=device)
            with torch.inference_mode():
                logits = self.model(input_ids=input_ids_t, attention_mask=attention_mask_t).logits

            for row_idx, (cache_key, destinations, prefix_len, seq_len) in enumerate(metadata):
                total = 0.0
                for pos in range(prefix_len, seq_len):
                    token_id = input_ids[row_idx][pos]
                    total += float(torch.log_softmax(logits[row_idx, pos - 1].float(), dim=-1)[token_id].item())
                self._score_cache[cache_key] = total
                for req_idx, cand in destinations:
                    per_request[req_idx][cand] = total

        return [ScoreResult(logprobs=d, probs=softmax_dict(d)) for d in per_request]

    def score(self, prompt: str, candidates: Iterable[str]) -> ScoreResult:
        return self.score_batch([(prompt, tuple(candidates))], sequence_batch_size=16)[0]
