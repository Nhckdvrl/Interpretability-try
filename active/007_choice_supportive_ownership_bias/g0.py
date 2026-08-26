#!/usr/bin/env python3
"""Minimal ownership-specific revision G0.

Uses only programmatic Bayesian gold and A/B parsing. No LLM judge.
The second-stage prompts are fresh contexts so the only matched difference is
Hidden vs Own-Shown vs Other-Shown attribution of the same initial answer.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path


def chat(endpoint: str, model: str, prompt: str) -> str:
    url = endpoint.rstrip("/") + "/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "Answer exactly A or B. No explanation."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "max_tokens": 4,
    }).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())["choices"][0]["message"]["content"].strip()


def parse_ab(text: str):
    hits = re.findall(r"\b([AB])\b", text.upper())
    return hits[0] if len(set(hits)) == 1 and hits else None


def posterior_after_reports(first: str, r1: float, second: str, r2: float) -> float:
    """P(state=A | two conditionally independent sensor reports), prior=.5."""
    def likelihood(report, reliability, state):
        return reliability if report == state else 1.0 - reliability

    la = likelihood(first, r1, "A") * likelihood(second, r2, "A")
    lb = likelihood(first, r1, "B") * likelihood(second, r2, "B")
    return la / (la + lb)


def make_cases():
    cases = []
    idx = 0
    for first in ("A", "B"):
        second = "B" if first == "A" else "A"
        for r1 in (0.60, 0.70, 0.80):
            for r2 in (0.90, 0.95):
                p_a = posterior_after_reports(first, r1, second, r2)
                gold2 = "A" if p_a > 0.5 else "B"
                assert gold2 == second
                stem1 = (
                    "The hidden state is A or B with equal prior probability. "
                    f"Sensor 1 is {int(r1*100)}% reliable and reports {first}. "
                    "Which state is more likely? Answer A or B."
                )
                evidence2 = (
                    "The hidden state is A or B with equal prior probability. "
                    f"Sensor 1 is {int(r1*100)}% reliable and reports {first}. "
                    f"Sensor 2 is {int(r2*100)}% reliable and reports {second}. "
                )
                cases.append({
                    "id": f"own-{idx:03d}",
                    "first": first,
                    "second": second,
                    "r1": r1,
                    "r2": r2,
                    "gold_initial": first,
                    "gold_final": gold2,
                    "gold_p_a_final": p_a,
                    "stage1_prompt": stem1,
                    "stage2_stem": evidence2,
                })
                idx += 1
    return cases


def stage2_prompt(case, condition: str, initial_answer: str):
    stem = case["stage2_stem"]
    if condition == "own":
        attribution = f"Earlier, you answered {initial_answer}. "
    elif condition == "other":
        attribution = f"Another model previously answered {initial_answer}. "
    elif condition == "hidden":
        attribution = ""
    else:
        raise ValueError(condition)
    return stem + attribution + "Given all the evidence, which state is more likely now? Answer A or B."


def summarize(rows):
    usable = [r for r in rows if r.get("initial") == r["gold_initial"]]
    by = defaultdict(list)
    for r in usable:
        for c in ("hidden", "own", "other"):
            pred = r.get(c)
            if pred in ("A", "B"):
                by[c].append(pred != r["initial"])
    rates = {c: (sum(v) / len(v) if v else None) for c, v in by.items()}
    return {
        "n_cases_total": len(rows),
        "n_cases_initial_expected": len(usable),
        "revision_rate_hidden": rates.get("hidden"),
        "revision_rate_own": rates.get("own"),
        "revision_rate_other": rates.get("other"),
        "hidden_minus_own": None if rates.get("hidden") is None or rates.get("own") is None else rates["hidden"] - rates["own"],
        "other_minus_own": None if rates.get("other") is None or rates.get("own") is None else rates["other"] - rates["own"],
        "hidden_minus_other_abs": None if rates.get("hidden") is None or rates.get("other") is None else abs(rates["hidden"] - rates["other"]),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", help="e.g. http://localhost:8245/v1")
    ap.add_argument("--model")
    ap.add_argument("--out", default="g0_results.jsonl")
    args = ap.parse_args()

    cases = make_cases()
    if not args.endpoint or not args.model:
        Path(args.out).write_text("\n".join(json.dumps(x) for x in cases) + "\n")
        print(json.dumps({"mode": "generate-only", "n_cases": len(cases), "out": args.out}, indent=2))
        return

    rows = []
    for case in cases:
        row = dict(case)
        row["initial_raw"] = chat(args.endpoint, args.model, case["stage1_prompt"])
        row["initial"] = parse_ab(row["initial_raw"])
        if row["initial"] not in ("A", "B"):
            rows.append(row)
            continue
        for cond in ("hidden", "own", "other"):
            raw = chat(args.endpoint, args.model, stage2_prompt(case, cond, row["initial"]))
            row[f"{cond}_raw"] = raw
            row[cond] = parse_ab(raw)
        rows.append(row)

    Path(args.out).write_text("\n".join(json.dumps(x) for x in rows) + "\n")
    print(json.dumps(summarize(rows), indent=2))


if __name__ == "__main__":
    main()
