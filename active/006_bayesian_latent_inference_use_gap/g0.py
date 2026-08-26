#!/usr/bin/env python3
"""Closed-form G0 for a latent-inference -> downstream-use gap.

The decisive comparison is not merely "posterior close, action wrong".  A case
counts as inference-good only when the model's reported posterior implies the
Bayes-optimal action.  We then compare an unassisted action probe with a matched
bridge probe that explicitly supplies the correct posterior.  A bridge rescue
therefore isolates failure to carry/use the inferred quantity from inability to
apply the payoff rule itself.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path


def posterior_a(prior_a: float, n_red: int, n_blue: int, p_red_a: float = 0.8, p_red_b: float = 0.2) -> float:
    log_a = math.log(prior_a) + n_red * math.log(p_red_a) + n_blue * math.log1p(-p_red_a)
    log_b = math.log1p(-prior_a) + n_red * math.log(p_red_b) + n_blue * math.log1p(-p_red_b)
    m = max(log_a, log_b)
    a, b = math.exp(log_a - m), math.exp(log_b - m)
    return a / (a + b)


def action_for(p_a: float, threshold: float) -> str:
    return "ACT" if p_a > threshold else "WAIT"


def make_cases() -> list[dict]:
    rows, idx = [], 0
    evidence_specs = ((1, 0), (0, 1), (2, 1), (1, 2), (3, 1), (1, 3), (3, 2), (2, 3))
    for prior in (0.3, 0.5, 0.7):
        for n_red, n_blue in evidence_specs:
            p = posterior_a(prior, n_red, n_blue)
            observations = ["red"] * n_red + ["blue"] * n_blue
            base = (
                f"A hidden source is Type A or Type B. Prior P(A)={prior:.1f}. "
                "Type A emits red with probability 0.8 and blue with probability 0.2; "
                "Type B emits red with probability 0.2 and blue with probability 0.8. "
                f"The independent observations are: {', '.join(observations)}."
            )
            posterior_prompt = base + " What is P(A | observations)? Answer as a probability with exactly two digits after the decimal point."
            evidence_id = f"evidence-{prior:.1f}-{n_red}-{n_blue}"
            for threshold in (1 / 3, 1 / 2, 2 / 3):
                rows.append({
                    "id": f"bayes-{idx:04d}",
                    "evidence_id": evidence_id,
                    "prior_a": prior,
                    "n_red": n_red,
                    "n_blue": n_blue,
                    "gold_p_a": p,
                    "decision_threshold": threshold,
                    "gold_action": action_for(p, threshold),
                    "bayes_margin": abs(p - threshold),
                    "posterior_prompt": posterior_prompt,
                    "base_prompt": base,
                })
                idx += 1
    return rows


def action_prompt(case: dict, *, bridge: bool, mapping: tuple[str, str]) -> tuple[str, str]:
    def description(action: str) -> str:
        return action
    belief = f" The posterior probability P(A | observations) is {case['gold_p_a']:.6f}." if bridge else ""
    prompt = (
        case["base_prompt"] + belief +
        f" A fixed policy says to choose ACT exactly when P(A | observations) is greater than {case['decision_threshold']:.6f}; otherwise choose WAIT. "
        f" Option A is {description(mapping[0])}. Option B is {description(mapping[1])}. "
        "Which option does the fixed policy select? Answer only A or B."
    )
    gold_label = "A" if mapping[0] == case["gold_action"] else "B"
    return prompt, gold_label


def parse_probability(text: str) -> float | None:
    text = text.strip().replace(",", "")
    percent = re.search(r"(?<![\d.])(100(?:\.0+)?|\d{1,2}(?:\.\d+)?)\s*%", text)
    if percent:
        return float(percent.group(1)) / 100.0
    number = re.search(r"(?<![\d.])(?:0(?:\.\d+)?|1(?:\.0+)?|\.\d+)(?![\d.])", text)
    if not number:
        return None
    value = float(number.group(0))
    return value if 0.0 <= value <= 1.0 else None


def _chat_prefix(tokenizer, prompt: str) -> str:
    kwargs = dict(tokenize=False, add_generation_prompt=True)
    try:
        return tokenizer.apply_chat_template([{"role": "user", "content": prompt}], enable_thinking=False, **kwargs)
    except TypeError:
        return tokenizer.apply_chat_template([{"role": "user", "content": prompt}], **kwargs)


class HFRunner:
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

    def generate_numbers(self, prompts: list[str], batch_size: int = 16) -> list[str]:
        out: list[str] = []
        device = next(self.model.parameters()).device
        for start in range(0, len(prompts), batch_size):
            prefixes = [_chat_prefix(self.tokenizer, p) for p in prompts[start:start + batch_size]]
            batch = self.tokenizer(prefixes, padding=True, return_tensors="pt").to(device)
            with self.torch.inference_mode():
                generated = self.model.generate(**batch, max_new_tokens=12, do_sample=False, pad_token_id=self.tokenizer.pad_token_id)
            prompt_width = batch["input_ids"].shape[1]
            for seq in generated:
                out.append(self.tokenizer.decode(seq[prompt_width:], skip_special_tokens=True).strip())
        return out

    def score_choices(self, prompts: list[str], candidates=("INVEST", "HOLD"), sequence_batch_size: int = 32) -> list[dict[str, float]]:
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
        for start in range(0, len(flat), sequence_batch_size):
            chunk = flat[start:start + sequence_batch_size]
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
        probabilities = []
        for row in scores:
            m = max(row.values())
            exps = {k: math.exp(v - m) for k, v in row.items()}
            z = sum(exps.values())
            probabilities.append({k: v / z for k, v in exps.items()})
        return probabilities


def summarize(rows: list[dict]) -> dict:
    analyzable = [r for r in rows if r.get("pred_p_a") is not None and r.get("direct_probs") and r.get("bridged_probs")]
    if not analyzable:
        return {"n": 0}
    evidence = {}
    for r in analyzable:
        evidence[r["evidence_id"]] = (r["pred_p_a"], r["gold_p_a"])
    posterior_mae = sum(abs(p - g) for p, g in evidence.values()) / len(evidence)
    eligible = []
    for r in analyzable:
        pred_implied_action = action_for(r["pred_p_a"], r["decision_threshold"])
        if abs(r["pred_p_a"] - r["gold_p_a"]) <= 0.10 and pred_implied_action == r["gold_action"] and r["bayes_margin"] >= 0.10:
            eligible.append(r)
    direct_errors = [r for r in eligible if r["direct_pred"] != r["gold_action"]]
    bridge_errors = [r for r in eligible if r["bridged_pred"] != r["gold_action"]]
    rescues = [r for r in direct_errors if r["bridged_pred"] == r["gold_action"]]
    return {
        "n": len(analyzable),
        "n_unique_evidence": len(evidence),
        "posterior_mae_unique_evidence": posterior_mae,
        "n_inference_good_action_identified_nonboundary": len(eligible),
        "direct_action_error_rate": len(direct_errors) / len(eligible) if eligible else None,
        "bridged_action_error_rate": len(bridge_errors) / len(eligible) if eligible else None,
        "bridge_rescue_rate_among_direct_errors": len(rescues) / len(direct_errors) if direct_errors else None,
        "mean_p_gold_bridge_minus_direct": (
            sum(r["bridged_probs"][r["gold_action"]] - r["direct_probs"][r["gold_action"]] for r in eligible) / len(eligible)
            if eligible else None
        ),
        "n_bridge_rescues": len(rescues),
    }


def run(model_name: str, out: Path, dtype: str, generation_batch_size: int, sequence_batch_size: int) -> dict:
    cases = make_cases()
    runner = HFRunner(model_name, dtype=dtype)
    unique_prompts = list(dict.fromkeys(c["posterior_prompt"] for c in cases))
    probability_candidates = tuple(f"{i / 100:.2f}" for i in range(101))
    posterior_distributions = runner.score_choices(unique_prompts, candidates=probability_candidates, sequence_batch_size=sequence_batch_size)
    posterior_by_prompt = {
        prompt: {
            "distribution": distribution,
            "argmax": max(distribution, key=distribution.get),
            "mean": sum(float(value) * probability for value, probability in distribution.items()),
        }
        for prompt, distribution in zip(unique_prompts, posterior_distributions, strict=True)
    }
    mappings = (("ACT", "WAIT"), ("WAIT", "ACT"))
    direct_prompts, bridged_prompts, refs = [], [], []
    for case_idx, case in enumerate(cases):
        for mapping in mappings:
            direct_prompt, direct_gold = action_prompt(case, bridge=False, mapping=mapping)
            bridged_prompt, bridged_gold = action_prompt(case, bridge=True, mapping=mapping)
            direct_prompts.append(direct_prompt); bridged_prompts.append(bridged_prompt)
            refs.append((case_idx, mapping, direct_gold, bridged_gold))
    direct_scores = runner.score_choices(direct_prompts, candidates=("A", "B"), sequence_batch_size=sequence_batch_size)
    bridged_scores = runner.score_choices(bridged_prompts, candidates=("A", "B"), sequence_batch_size=sequence_batch_size)
    action_scores = [{"direct": [], "bridged": []} for _ in cases]
    for direct, bridged, (case_idx, mapping, direct_gold, bridged_gold) in zip(direct_scores, bridged_scores, refs, strict=True):
        for kind, probs, gold_label in (("direct", direct, direct_gold), ("bridged", bridged, bridged_gold)):
            invest_label = "A" if mapping[0] == "ACT" else "B"
            hold_label = "B" if invest_label == "A" else "A"
            action_scores[case_idx][kind].append({
                "mapping": list(mapping), "label_probs": probs, "gold_label": gold_label,
                "action_probs": {"ACT": probs[invest_label], "WAIT": probs[hold_label]},
            })
    rows = []
    for case_idx, c in enumerate(cases):
        row = dict(c)
        row["model"] = model_name
        posterior = posterior_by_prompt[c["posterior_prompt"]]
        row["posterior_argmax"] = posterior["argmax"]
        row["pred_p_a"] = posterior["mean"]
        row["posterior_distribution"] = posterior["distribution"]
        row["direct_variants"] = action_scores[case_idx]["direct"]
        row["bridged_variants"] = action_scores[case_idx]["bridged"]
        row["direct_probs"] = {action: sum(x["action_probs"][action] for x in row["direct_variants"]) / len(mappings) for action in ("ACT", "WAIT")}
        row["bridged_probs"] = {action: sum(x["action_probs"][action] for x in row["bridged_variants"]) / len(mappings) for action in ("ACT", "WAIT")}
        row["direct_pred"], row["bridged_pred"] = max(row["direct_probs"], key=row["direct_probs"].get), max(row["bridged_probs"], key=row["bridged_probs"].get)
        rows.append(row)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")
    return summarize(rows)


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate")
    g.add_argument("--out", default="data/cases.jsonl")
    r = sub.add_parser("run")
    r.add_argument("--model", required=True)
    r.add_argument("--out", required=True)
    r.add_argument("--dtype", default="auto")
    r.add_argument("--generation-batch-size", type=int, default=16)
    r.add_argument("--sequence-batch-size", type=int, default=32)
    s = sub.add_parser("summarize")
    s.add_argument("--results", required=True)
    s.add_argument("--out")
    args = ap.parse_args()
    if args.cmd == "generate":
        rows = make_cases(); path = Path(args.out); path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(json.dumps(x) for x in rows) + "\n")
        result = {"n_cases": len(rows), "n_unique_evidence": len({x['evidence_id'] for x in rows})}
    elif args.cmd == "run":
        result = run(args.model, Path(args.out), args.dtype, args.generation_batch_size, args.sequence_batch_size)
    else:
        result = summarize(load_jsonl(Path(args.results)))
        if args.out:
            Path(args.out).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
