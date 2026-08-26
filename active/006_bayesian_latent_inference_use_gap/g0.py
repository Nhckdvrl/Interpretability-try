#!/usr/bin/env python3
"""Minimal behavioral scaffold for topic 006.

No LLM judge. Gold posterior/action are computed analytically.
If --endpoint/--model are omitted, the script only writes the cases.
Example local endpoint: http://localhost:8245/v1
"""

from __future__ import annotations

import argparse
import json
import math
import re
import urllib.request
from pathlib import Path


def posterior_a(prior_a: float, n_red: int, n_blue: int, p_red_a=0.8, p_red_b=0.2) -> float:
    la = prior_a * (p_red_a ** n_red) * ((1 - p_red_a) ** n_blue)
    lb = (1 - prior_a) * (p_red_b ** n_red) * ((1 - p_red_b) ** n_blue)
    return la / (la + lb)


def make_cases():
    cases = []
    idx = 0
    for prior in (0.3, 0.5, 0.7):
        for n_red, n_blue in ((1, 0), (0, 1), (2, 1), (1, 2), (3, 1), (1, 3), (3, 2), (2, 3)):
            p = posterior_a(prior, n_red, n_blue)
            for loss_if_b in (0.5, 1.0, 2.0):
                # INVEST payoff: +1 if A, -loss_if_b if B; HOLD payoff: 0.
                threshold = loss_if_b / (1.0 + loss_if_b)
                gold_action = "INVEST" if p > threshold else "HOLD"
                obs = ["red"] * n_red + ["blue"] * n_blue
                base = (
                    f"A hidden source is either Type A or Type B. Prior P(A)={prior:.1f}. "
                    "Type A emits red with probability 0.8 and blue with 0.2; "
                    "Type B emits red with probability 0.2 and blue with 0.8. "
                    f"Observed signals: {', '.join(obs)}."
                )
                cases.append({
                    "id": f"bayes-{idx:04d}",
                    "prior_a": prior,
                    "n_red": n_red,
                    "n_blue": n_blue,
                    "gold_p_a": p,
                    "loss_if_b": loss_if_b,
                    "decision_threshold": threshold,
                    "gold_action": gold_action,
                    "bayes_margin": abs(p - threshold),
                    "posterior_prompt": base + " What is P(A | observations)? Answer only a number from 0 to 1.",
                    "action_prompt": base + (
                        f" You may INVEST: payoff +1 if A, payoff -{loss_if_b:g} if B; "
                        "or HOLD: payoff 0. Which has higher expected payoff? Answer only INVEST or HOLD."
                    ),
                })
                idx += 1
    return cases


def chat(endpoint: str, model: str, prompt: str) -> str:
    url = endpoint.rstrip("/") + "/chat/completions"
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "Follow the requested output format exactly. Do not explain."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "max_tokens": 24,
    }).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        obj = json.loads(r.read().decode())
    return obj["choices"][0]["message"]["content"].strip()


def parse_probability(text: str):
    m = re.search(r"(?:^|\s)(0(?:\.\d+)?|1(?:\.0+)?)\b", text.strip())
    return float(m.group(1)) if m else None


def parse_action(text: str):
    t = text.upper()
    hits = [x for x in ("INVEST", "HOLD") if re.search(rf"\b{x}\b", t)]
    return hits[0] if len(hits) == 1 else None


def summarize(rows):
    analyzable = [r for r in rows if r.get("pred_p_a") is not None and r.get("pred_action")]
    if not analyzable:
        return {"n": 0}
    mae = sum(abs(r["pred_p_a"] - r["gold_p_a"]) for r in analyzable) / len(analyzable)
    inferred = [r for r in analyzable if abs(r["pred_p_a"] - r["gold_p_a"]) <= 0.15 and r["bayes_margin"] >= 0.10]
    use_fail = [r for r in inferred if r["pred_action"] != r["gold_action"]]
    return {
        "n": len(analyzable),
        "posterior_mae": mae,
        "n_inference_good_nonboundary": len(inferred),
        "n_know_use_fail": len(use_fail),
        "know_use_failure_rate": (len(use_fail) / len(inferred)) if inferred else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", help="OpenAI-compatible base, e.g. http://localhost:8245/v1")
    ap.add_argument("--model")
    ap.add_argument("--out", default="g0_results.jsonl")
    args = ap.parse_args()

    cases = make_cases()
    if not args.endpoint or not args.model:
        Path(args.out).write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in cases) + "\n")
        print(json.dumps({"mode": "generate-only", "n_cases": len(cases), "out": args.out}, indent=2))
        return

    rows = []
    for c in cases:
        row = dict(c)
        row["posterior_raw"] = chat(args.endpoint, args.model, c["posterior_prompt"])
        row["action_raw"] = chat(args.endpoint, args.model, c["action_prompt"])
        row["pred_p_a"] = parse_probability(row["posterior_raw"])
        row["pred_action"] = parse_action(row["action_raw"])
        rows.append(row)

    Path(args.out).write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n")
    print(json.dumps(summarize(rows), indent=2))


if __name__ == "__main__":
    main()
