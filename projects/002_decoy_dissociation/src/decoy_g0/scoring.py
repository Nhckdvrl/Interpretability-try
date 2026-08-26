from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

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
    """Deterministic teacher-forced scoring of complete candidate strings."""

    def __init__(self, model_name: str, device_map: str = "auto", dtype: str = "auto"):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        dtype_arg = dtype if dtype == "auto" else getattr(torch, dtype)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map=device_map, torch_dtype=dtype_arg, trust_remote_code=True)
        self.model.eval()

    def _chat_prefix(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        if hasattr(self.tokenizer, "apply_chat_template") and self.tokenizer.chat_template:
            return self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        return prompt.rstrip() + "\nAnswer:"

    def score(self, prompt: str, candidates: Iterable[str]) -> ScoreResult:
        torch = self.torch
        prefix = self._chat_prefix(prompt)
        prefix_ids = self.tokenizer(prefix, add_special_tokens=False).input_ids
        if not prefix_ids:
            raise ValueError("empty tokenized prefix")
        device = next(self.model.parameters()).device
        logprobs: dict[str, float] = {}
        for cand in candidates:
            full_ids = self.tokenizer(prefix + " " + cand, add_special_tokens=False).input_ids
            if len(full_ids) <= len(prefix_ids):
                raise ValueError(f"candidate {cand!r} produced no continuation tokens")
            input_ids = torch.tensor([full_ids], device=device)
            with torch.inference_mode():
                logits = self.model(input_ids=input_ids).logits[0]
            total = 0.0
            for pos in range(len(prefix_ids), len(full_ids)):
                token_id = full_ids[pos]
                total += float(torch.log_softmax(logits[pos - 1].float(), dim=-1)[token_id].item())
            logprobs[cand] = total
        return ScoreResult(logprobs=logprobs, probs=softmax_dict(logprobs))
