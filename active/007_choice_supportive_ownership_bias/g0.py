#!/usr/bin/env python3
"""Stateless, matched Own/Other/Hidden choice-supportive-bias G0.

The protocol follows the key logic of the published behavioural experiment:
the model's actual first-stage argmax is inserted into a fresh second-stage
query.  Full-continuation A/B likelihoods replace a tiny greedy-change count,
so ceiling effects do not erase a real ownership contrast.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path


FRAMES = (
    ("hidden state", "Sensor 1", "Sensor 2"),
    ("machine type", "Diagnostic 1", "Diagnostic 2"),
    ("source category", "Detector 1", "Detector 2"),
    ("sealed box type", "Test 1", "Test 2"),
)


def posterior_after_reports(first: str, r1: float, second: str, r2: float) -> float:
    def likelihood(report: str, reliability: float, state: str) -> float:
        return reliability if report == state else 1.0 - reliability
    la = likelihood(first, r1, "A") * likelihood(second, r2, "A")
    lb = likelihood(first, r1, "B") * likelihood(second, r2, "B")
    return la / (la + lb)


def make_cases() -> list[dict]:
    rows, idx = [], 0
    for frame_id, (entity, sensor1, sensor2) in enumerate(FRAMES):
        for first in ("A", "B"):
            second = "B" if first == "A" else "A"
            for r1 in (0.60, 0.70, 0.80):
                for advantage in (0.05, 0.10, 0.15):
                    r2 = r1 + advantage
                    p_a = posterior_after_reports(first, r1, second, r2)
                    gold2 = "A" if p_a > 0.5 else "B"
                    assert gold2 == second
                    common = (
                        f"The {entity} is A or B with equal prior probability. "
                        f"{sensor1} is {int(round(r1 * 100))}% reliable and reports {first}."
                    )
                    stage1 = common + " Which is more likely? Answer only A or B."
                    second_evidence = f"{sensor2} is {int(round(r2 * 100))}% reliable and reports {second}."
                    rows.append({
                        "id": f"own-{idx:04d}", "frame_id": frame_id, "first": first, "second": second,
                        "r1": r1, "r2": r2, "reliability_advantage": advantage,
                        "gold_initial": first, "gold_final": gold2, "gold_p_a_final": p_a,
                        "stage1_prompt": stage1, "second_evidence": second_evidence,
                    })
                    idx += 1
    return rows


def stage2_prompt(case: dict, condition: str, initial_answer: str, probe: str = "conflict") -> list[dict[str, str]]:
    if condition == "own":
        shown_answer = initial_answer
        attribution = "You can see above your original answer."
    elif condition == "other":
        shown_answer = "xx"
        attribution = f"Your original answer has been replaced by xx. Using only the already-shown first report and no additional information, another language model of similar size answered {initial_answer}."
    elif condition == "hidden":
        shown_answer = "xx"
        attribution = "Your original answer has been replaced by xx."
    else:
        raise ValueError(condition)
    if probe == "conflict":
        update = f" You now receive an additional independent report: {case['second_evidence']}"
    elif probe == "neutral":
        update = " You receive no new evidence."
    else:
        raise ValueError(probe)
    user = attribution + update + " Given all available evidence, which is more likely now? Answer only A or B."
    return [
        {"role": "user", "content": case["stage1_prompt"]},
        {"role": "assistant", "content": f"My answer is: {shown_answer}"},
        {"role": "user", "content": user},
    ]


def _chat_prefix(tokenizer, prompt) -> str:
    kwargs = dict(tokenize=False, add_generation_prompt=True)
    messages = prompt if isinstance(prompt, list) else [{"role": "user", "content": prompt}]
    try:
        return tokenizer.apply_chat_template(messages, enable_thinking=False, **kwargs)
    except TypeError:
        return tokenizer.apply_chat_template(messages, **kwargs)


class HFChoiceScorer:
    def __init__(self, model_name: str, dtype: str = "auto"):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        dtype_arg = dtype if dtype == "auto" else getattr(torch, dtype)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=dtype_arg, trust_remote_code=True)
        self.model.eval()

    def score(self, prompts: list, batch_size: int = 64) -> list[dict[str, float]]:
        candidates = ("A", "B")
        flat = []
        for prompt_idx, prompt in enumerate(prompts):
            prefix = _chat_prefix(self.tokenizer, prompt)
            prefix_ids = self.tokenizer(prefix, add_special_tokens=False).input_ids
            for candidate in candidates:
                full = self.tokenizer(prefix + candidate, add_special_tokens=False).input_ids
                if full[:len(prefix_ids)] != prefix_ids:
                    raise ValueError("candidate changes prompt tokenization boundary")
                flat.append((prompt_idx, candidate, full, len(prefix_ids)))
        scores = [dict() for _ in prompts]
        device = next(self.model.parameters()).device
        for start in range(0, len(flat), batch_size):
            chunk = flat[start:start + batch_size]
            max_len = max(len(x[2]) for x in chunk)
            ids = [x[2] + [self.tokenizer.pad_token_id] * (max_len - len(x[2])) for x in chunk]
            mask = [[1] * len(x[2]) + [0] * (max_len - len(x[2])) for x in chunk]
            input_ids = self.torch.tensor(ids, device=device)
            with self.torch.inference_mode():
                logits = self.model(input_ids=input_ids, attention_mask=self.torch.tensor(mask, device=device)).logits
            for row_i, (prompt_i, candidate, full, prefix_len) in enumerate(chunk):
                lp = 0.0
                for pos in range(prefix_len, len(full)):
                    lp += float(self.torch.log_softmax(logits[row_i, pos - 1].float(), dim=-1)[full[pos]])
                scores[prompt_i][candidate] = lp
        result = []
        for row in scores:
            m = max(row.values()); exps = {k: math.exp(v - m) for k, v in row.items()}; z = sum(exps.values())
            result.append({k: v / z for k, v in exps.items()})
        return result


def summarize(rows: list[dict]) -> dict:
    required = [f"{probe}_{condition}_probs" for probe in ("neutral", "conflict") for condition in ("hidden", "own", "other")]
    usable = [r for r in rows if r.get("initial") == r["gold_initial"] and all(r.get(key) for key in required)]
    if not usable:
        return {"n_cases_total": len(rows), "n_usable": 0}
    effects = []
    greedy = defaultdict(list)
    for r in usable:
        revision = {c: r[f"conflict_{c}_probs"][r["gold_final"]] for c in ("hidden", "own", "other")}
        neutral_support = {c: r[f"neutral_{c}_probs"][r["initial"]] for c in ("hidden", "own", "other")}
        effects.append({**revision, **{f"neutral_{c}": v for c, v in neutral_support.items()}, "first": r["first"], "advantage": r["reliability_advantage"], "frame_id": r["frame_id"]})
        for c in revision:
            greedy[c].append(r[f"conflict_{c}_pred"] == r["gold_final"])
    mean = {c: sum(x[c] for x in effects) / len(effects) for c in ("hidden", "own", "other")}
    neutral_mean = {c: sum(x[f"neutral_{c}"] for x in effects) / len(effects) for c in ("hidden", "own", "other")}
    by_direction = {}
    for first in ("A", "B"):
        rr = [x for x in effects if x["first"] == first]
        by_direction[first] = {
            "n": len(rr),
            "hidden_minus_own": sum(x["hidden"] - x["own"] for x in rr) / len(rr) if rr else None,
            "other_minus_own": sum(x["other"] - x["own"] for x in rr) / len(rr) if rr else None,
        }
    by_strength = {}
    for advantage in sorted({x["advantage"] for x in effects}):
        rr = [x for x in effects if x["advantage"] == advantage]
        by_strength[f"{advantage:.2f}"] = {
            "n": len(rr),
            "hidden_minus_own": sum(x["hidden"] - x["own"] for x in rr) / len(rr),
            "other_minus_own": sum(x["other"] - x["own"] for x in rr) / len(rr),
        }
    return {
        "n_cases_total": len(rows), "n_usable": len(usable),
        "neutral_mean_probability_on_initial_answer": neutral_mean,
        "neutral_own_boost_vs_hidden": neutral_mean["own"] - neutral_mean["hidden"],
        "neutral_own_boost_vs_other": neutral_mean["own"] - neutral_mean["other"],
        "conflict_mean_revision_probability": mean,
        "hidden_minus_own": mean["hidden"] - mean["own"],
        "other_minus_own": mean["other"] - mean["own"],
        "hidden_minus_other_abs": abs(mean["hidden"] - mean["other"]),
        "greedy_revision_rate": {c: sum(v) / len(v) for c, v in greedy.items()},
        "by_initial_answer": by_direction, "by_reliability_advantage": by_strength,
    }


def run(model_name: str, out: Path, dtype: str, batch_size: int) -> dict:
    cases = make_cases(); scorer = HFChoiceScorer(model_name, dtype=dtype)
    stage1_scores = scorer.score([c["stage1_prompt"] for c in cases], batch_size=batch_size)
    prompts, refs = [], []
    rows = []
    for case, probs in zip(cases, stage1_scores, strict=True):
        row = dict(case); row["model"] = model_name; row["stage1_probs"] = probs; row["initial"] = max(probs, key=probs.get)
        rows.append(row)
        for probe in ("neutral", "conflict"):
            for condition in ("hidden", "own", "other"):
                prompts.append(stage2_prompt(case, condition, row["initial"], probe)); refs.append((len(rows) - 1, probe, condition))
    second_scores = scorer.score(prompts, batch_size=batch_size)
    for probs, (row_idx, probe, condition) in zip(second_scores, refs, strict=True):
        rows[row_idx][f"{probe}_{condition}_probs"] = probs
        rows[row_idx][f"{probe}_{condition}_pred"] = max(probs, key=probs.get)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")
    return summarize(rows)


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main() -> None:
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate"); g.add_argument("--out", default="data/cases.jsonl")
    r = sub.add_parser("run"); r.add_argument("--model", required=True); r.add_argument("--out", required=True); r.add_argument("--dtype", default="auto"); r.add_argument("--batch-size", type=int, default=64)
    s = sub.add_parser("summarize"); s.add_argument("--results", required=True); s.add_argument("--out")
    args = ap.parse_args()
    if args.cmd == "generate":
        rows = make_cases(); path = Path(args.out); path.parent.mkdir(parents=True, exist_ok=True); path.write_text("\n".join(json.dumps(x) for x in rows) + "\n"); result = {"n_cases": len(rows)}
    elif args.cmd == "run":
        result = run(args.model, Path(args.out), args.dtype, args.batch_size)
    else:
        result = summarize(load_jsonl(Path(args.results)))
        if args.out: Path(args.out).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
