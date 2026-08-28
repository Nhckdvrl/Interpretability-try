from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Sequence
import json
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor

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
    """Scores exact continuation strings without an API or LLM judge.

    The cache is deliberately lifetime-scoped: repeated identical requests must
    receive bit-identical stored scores even when model kernels are not perfectly
    deterministic across batches.
    """
    def __init__(self, model_name: str, *, revision: str | None = None,
                 device_map: str = "auto", dtype: str = "auto"):
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
            model_name, revision=revision, device_map=device_map,
            torch_dtype=dtype_arg, trust_remote_code=True
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
        prefix = self._prefix(prompt)
        pids = self.tokenizer(prefix, add_special_tokens=False).input_ids
        fids = self.tokenizer(prefix + candidate, add_special_tokens=False).input_ids
        if not pids or len(fids) <= len(pids) or fids[:len(pids)] != pids:
            raise ValueError(f"candidate {candidate!r} changes prompt tokenization boundary")
        return fids, len(pids)

    def score_batch(self, requests: Sequence[tuple[str, tuple[str, ...]]],
                    *, sequence_batch_size: int = 64) -> list[ScoreResult]:
        torch = self.torch
        pending: dict[tuple[str, str], list[tuple[int, str]]] = {}
        per_req: list[dict[str, float]] = [{} for _ in requests]
        for i, (prompt, candidates) in enumerate(requests):
            for cand in candidates:
                key = (prompt, cand)
                if key in self._cache:
                    per_req[i][cand] = self._cache[key]
                else:
                    pending.setdefault(key, []).append((i, cand))

        flat = []
        for key, destinations in pending.items():
            ids, plen = self._encode_pair(*key)
            flat.append((key, destinations, ids, plen))

        device = next(self.model.parameters()).device
        for start in range(0, len(flat), sequence_batch_size):
            chunk = flat[start:start + sequence_batch_size]
            max_len = max(len(x[2]) for x in chunk)
            ids_batch, masks, meta = [], [], []
            for key, destinations, ids, plen in chunk:
                pad = max_len - len(ids)
                ids_batch.append(ids + [self.tokenizer.pad_token_id] * pad)
                masks.append([1] * len(ids) + [0] * pad)
                meta.append((key, destinations, plen, len(ids)))
            input_ids = torch.tensor(ids_batch, device=device)
            attention_mask = torch.tensor(masks, device=device)
            with torch.inference_mode():
                logits = self.model(input_ids=input_ids, attention_mask=attention_mask).logits
            for row, (key, destinations, plen, slen) in enumerate(meta):
                total = 0.0
                for pos in range(plen, slen):
                    tok = ids_batch[row][pos]
                    total += float(torch.log_softmax(logits[row, pos - 1].float(), dim=-1)[tok].item())
                self._cache[key] = total
                for req_i, cand in destinations:
                    per_req[req_i][cand] = total
        return [ScoreResult(d, softmax_dict(d)) for d in per_req]

class VLLMChoiceScorer:
    """Exact one-token continuation scorer for an existing local vLLM server."""
    def __init__(self, model_name: str, *, base_url: str, revision: str | None = None, served_model: str | None = None):
        from transformers import AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, revision=revision, trust_remote_code=True)
        self.base_url = base_url.rstrip("/") + "/v1/completions"
        self.model_name = served_model or model_name
        self._cache = {}

    def _prefix(self, user_text: str) -> str:
        messages = [{"role": "user", "content": user_text}]
        if getattr(self.tokenizer, "chat_template", None):
            try:
                return self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
            except TypeError:
                return self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        return f"USER: {user_text}\nASSISTANT:"

    def score_batch(self, requests: Sequence[tuple[str, tuple[str, ...]]], *, sequence_batch_size: int = 64) -> list[ScoreResult]:
        prepared = [(self._prefix(prompt), candidates) for prompt, candidates in requests]
        pending = []
        seen = set()
        for prefix, candidates in prepared:
            for cand in candidates:
                key = (prefix, cand)
                if key not in self._cache and key not in seen:
                    pending.append(key); seen.add(key)
        def score_one(key):
            prefix, cand = key
            body = json.dumps({"model": self.model_name, "prompt": prefix + cand, "max_tokens": 0, "temperature": 0, "logprobs": 1, "echo": True}).encode()
            req = Request(self.base_url, data=body, headers={"Content-Type": "application/json"})
            with urlopen(req, timeout=120) as response: data = json.load(response)
            return key, float(data["choices"][0]["logprobs"]["token_logprobs"][-1])
        workers = max(1, min(int(sequence_batch_size), 16))
        with ThreadPoolExecutor(max_workers=workers) as pool:
            for key, lp in pool.map(score_one, pending):
                self._cache[key] = lp
        out = []
        for prefix, candidates in prepared:
            vals = {cand: self._cache[(prefix, cand)] for cand in candidates}
            out.append(ScoreResult(vals, softmax_dict(vals)))
        return out
