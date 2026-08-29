"""Phase-1 behavioural run for 014 Alias Entrainment Transfer.

Two readouts, both frozen by configs/contract_r1.yaml:

  main    delta = logP(target | frame(mention) + carrier) - logP(target | carrier)
          over conditions EXACT / ALIAS / SEMREL / UNREL against the NOCTX baseline.
  probe   counterbalanced two-content-option alias-knowledge gate, plus a
          free-continuation top-5 check.

No probe / patching / ablation of any kind: phase 1 only reads output logits.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

CONDITIONS = ("EXACT", "ALIAS", "SEMREL", "UNREL")


def mention_for(item: dict, cond: str) -> str:
    return {"EXACT": item["target_form"], "ALIAS": item["seen_form"],
            "SEMREL": item["semrel"], "UNREL": item["unrel"]}[cond]


def build_prompt(context: str | None, question: str) -> str:
    body = f"Q: {question}\nA:"
    return f"{context}\n{body}" if context else body


class Scorer:
    def __init__(self, model_id: str, device: str = "cuda", batch_size: int = 32):
        self.tok = AutoTokenizer.from_pretrained(model_id)
        if self.tok.pad_token_id is None:
            self.tok.pad_token = self.tok.eos_token
        self.tok.padding_side = "left"
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, dtype=torch.bfloat16, device_map=device)
        self.model.eval()
        self.device = device
        self.bs = batch_size
        self.boundary_shifts = 0

    def _split(self, prompt: str, cont: str):
        """Token ids for prompt and for the scored continuation.

        The continuation always starts with a space and the prompt always ends
        with 'A:', so the BPE boundary is stable; we assert it rather than
        assume it, and count any shift.
        """
        p_ids = self.tok.encode(prompt, add_special_tokens=True)
        f_ids = self.tok.encode(prompt + cont, add_special_tokens=True)
        k = 0
        while k < min(len(p_ids), len(f_ids)) and p_ids[k] == f_ids[k]:
            k += 1
        if k != len(p_ids):
            self.boundary_shifts += 1
        return f_ids, k

    @torch.no_grad()
    def score(self, jobs: list[tuple[str, str]]) -> list[dict]:
        """jobs = [(prompt, continuation)] -> per-job logprob sum and first-token stats."""
        out: list[dict] = []
        for i in range(0, len(jobs), self.bs):
            chunk = jobs[i:i + self.bs]
            enc = [self._split(p, c) for p, c in chunk]
            maxlen = max(len(f) for f, _ in enc)
            pad = self.tok.pad_token_id
            input_ids = torch.full((len(chunk), maxlen), pad, dtype=torch.long)
            attn = torch.zeros((len(chunk), maxlen), dtype=torch.long)
            for j, (f, _) in enumerate(enc):
                input_ids[j, maxlen - len(f):] = torch.tensor(f)
                attn[j, maxlen - len(f):] = 1
            input_ids, attn = input_ids.to(self.device), attn.to(self.device)
            logits = self.model(input_ids=input_ids, attention_mask=attn).logits.float()
            logprobs = torch.log_softmax(logits, dim=-1)

            for j, (f, k) in enumerate(enc):
                off = maxlen - len(f)
                tgt = f[k:]
                # position predicting f[t] is t-1
                pos = [off + t - 1 for t in range(k, len(f))]
                lp = sum(logprobs[j, p, f[t]].item() for p, t in zip(pos, range(k, len(f))))
                first_pos, first_tok = pos[0], tgt[0]
                out.append(dict(
                    logprob_sum=lp,
                    n_target_tokens=len(tgt),
                    first_token_logit=logits[j, first_pos, first_tok].item(),
                    first_token_logprob=logprobs[j, first_pos, first_tok].item(),
                ))
        return out

    @torch.no_grad()
    def top_k_continuations(self, prompts: list[str], k: int = 5) -> list[list[str]]:
        res = []
        for i in range(0, len(prompts), self.bs):
            chunk = prompts[i:i + self.bs]
            enc = self.tok(chunk, return_tensors="pt", padding=True).to(self.device)
            gen = self.model.generate(**enc, max_new_tokens=8, do_sample=False,
                                      num_beams=k, num_return_sequences=k,
                                      pad_token_id=self.tok.pad_token_id)
            gen = gen[:, enc["input_ids"].shape[1]:]
            texts = self.tok.batch_decode(gen, skip_special_tokens=True)
            for j in range(len(chunk)):
                res.append(texts[j * k:(j + 1) * k])
        return res


def run_main(items, scorer) -> list[dict]:
    jobs, keys = [], []
    for it in items:
        cont = " " + it["target_form"]
        for c in it["carriers"]:
            jobs.append((build_prompt(None, c["question"]), cont))
            keys.append((it["item_id"], c["qid"], "NOCTX", "-"))
            for fname, ftpl in it["frames"].items():
                for cond in CONDITIONS:
                    ctx = ftpl.format(M=mention_for(it, cond))
                    jobs.append((build_prompt(ctx, c["question"]), cont))
                    keys.append((it["item_id"], c["qid"], cond, fname))
    print(f"  main jobs: {len(jobs)}")
    scored = scorer.score(jobs)
    return [dict(item_id=k[0], qid=k[1], condition=k[2], frame=k[3], **s)
            for k, s in zip(keys, scored)]


def run_probe(items, scorer) -> list[dict]:
    """Counterbalanced two-content-option alias gate + free-continuation check."""
    jobs, keys = [], []
    for it in items:
        for order, (a, b) in enumerate([(it["target_form"], it["semrel"]),
                                        (it["semrel"], it["target_form"])]):
            prompt = (f'Q: Which of the following is another name for '
                      f'{it["seen_form"]}?\n'
                      f'Options: (A) {a}  (B) {b}\nA: (')
            gold = "A" if order == 0 else "B"
            for letter in ("A", "B"):
                jobs.append((prompt, letter))
                keys.append((it["item_id"], order, letter, gold))
    print(f"  probe jobs: {len(jobs)}")
    scored = scorer.score(jobs)
    rows = [dict(item_id=k[0], order=k[1], letter=k[2], gold=k[3], **s)
            for k, s in zip(keys, scored)]

    # Secondary readout (amendment r1b): a paired log-prob comparison at one and
    # the same position, so no answer-order or generation-style artifact is
    # possible. Free-form beam search was discarded because chat-tuned models
    # answer the fragment instead of completing it.
    free_jobs, free_keys = [], []
    for it in items:
        prompt = f'{it["seen_form"]} is another name for'
        for role, cand in (("target", it["target_form"]), ("semrel", it["semrel"])):
            free_jobs.append((prompt, " " + cand))
            free_keys.append((it["item_id"], role))
    free_scored = scorer.score(free_jobs)
    per_item: dict[str, dict] = {}
    for (iid, role), sc in zip(free_keys, free_scored):
        # length-normalized: the two candidates differ in token count
        per_item.setdefault(iid, {})[role] = sc["logprob_sum"] / sc["n_target_tokens"]
    for iid, v in per_item.items():
        rows.append(dict(item_id=iid, order=-1, letter="FREE", gold="",
                         free_lp_target=v["target"], free_lp_semrel=v["semrel"],
                         free_hit=bool(v["target"] > v["semrel"])))
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--d0", default="data/frozen_d0.jsonl")
    ap.add_argument("--out-dir", default="results/phase1_r1")
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    items = [json.loads(l) for l in open(args.d0, encoding="utf-8")]
    if args.limit:
        items = items[:args.limit]
    print(f"{args.tag}: {len(items)} items")

    t0 = time.time()
    scorer = Scorer(args.model, batch_size=args.batch_size)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    probe_rows = run_probe(items, scorer)
    with (out / f"{args.tag}__probe.jsonl").open("w") as f:
        for r in probe_rows:
            f.write(json.dumps(r) + "\n")

    main_rows = run_main(items, scorer)
    with (out / f"{args.tag}__main.jsonl").open("w") as f:
        for r in main_rows:
            f.write(json.dumps(r) + "\n")

    print(f"{args.tag}: done in {time.time() - t0:.0f}s, "
          f"tokenizer boundary shifts = {scorer.boundary_shifts}")


if __name__ == "__main__":
    main()
