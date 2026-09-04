#!/usr/bin/env python3
"""Test illicit existential narrowing along an explicit subclass relation."""

import argparse
import asyncio
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import httpx


CASES = [
    ("mammal", "dog", "escaped from the shelter"),
    ("employee", "engineer", "reported the security flaw"),
    ("medication", "antibiotic", "caused the allergic reaction"),
    ("vehicle", "ambulance", "blocked the road"),
    ("city", "capital city", "introduced a curfew"),
    ("bird", "robin", "nested in the old barn"),
    ("financial transaction", "wire transfer", "was fraudulent"),
    ("electronic device", "temperature sensor", "failed during the test"),
    ("researcher", "biologist", "received the award"),
    ("company", "software company", "filed for bankruptcy"),
    ("building", "hospital", "lost power during the storm"),
    ("chemical", "solvent", "contaminated the water sample"),
    ("contractor", "electrician", "submitted an incorrect invoice"),
    ("court case", "patent case", "was settled last week"),
    ("machine component", "bearing", "caused the vibration"),
    ("account", "administrator account", "downloaded the confidential file"),
    ("crop", "wheat crop", "was damaged by frost"),
    ("document", "passport", "was found in the waiting room"),
    ("course", "mathematics course", "was cancelled this semester"),
    ("animal", "horse", "required emergency treatment"),
    ("publication", "medical journal", "issued a correction"),
    ("public official", "mayor", "resigned after the investigation"),
    ("shipment", "international shipment", "was delayed at the depot"),
    ("computer program", "web browser", "contained the vulnerability"),
]


def article(noun):
    return "an" if noun[0].lower() in "aeiou" else "a"


def build_items():
    rows = []
    for i, (superclass, subclass, predicate) in enumerate(CASES):
        a_sup, a_sub = article(superclass), article(subclass)
        relation = f"Every {subclass} is {a_sup} {superclass}."
        conditions = [
            ("narrow_explicit", f"{a_sup.capitalize()} {superclass} {predicate}. {relation}",
             f"{a_sub.capitalize()} {subclass} {predicate}.", "UNKNOWN"),
            ("narrow_no_rule", f"{a_sup.capitalize()} {superclass} {predicate}.",
             f"{a_sub.capitalize()} {subclass} {predicate}.", "UNKNOWN"),
            ("widen_valid", f"{a_sub.capitalize()} {subclass} {predicate}. {relation}",
             f"{a_sup.capitalize()} {superclass} {predicate}.", "ENTAILED"),
            ("universal_valid", f"Every {superclass} {predicate}. {relation}",
             f"Every {subclass} {predicate}.", "ENTAILED"),
            ("negative_valid", f"No {superclass} {predicate}. {relation}",
             f"No {subclass} {predicate}.", "ENTAILED"),
        ]
        for condition, premises, hypothesis, gold in conditions:
            prompt = (
                f"Premises:\n{premises}\n\nHypothesis:\n{hypothesis}\n\n"
                "Based only on the premises, is the hypothesis definitely entailed, "
                "definitely contradicted, or neither? Answer only ENTAILED, "
                "CONTRADICTED, or UNKNOWN."
            )
            rows.append({"id": f"{i:02d}_{condition}", "superclass": superclass,
                         "subclass": subclass, "condition": condition,
                         "premises": premises, "hypothesis": hypothesis,
                         "gold": gold, "prompt": prompt})
    return rows


def parse(text):
    matches = re.findall(
        r"\b(ENTAILED|ENTAILMENT|ENTAILLED|CONTRADICTED|CONTRADICTION|UNKNOWN|NEUTRAL)\b",
        text.upper(),
    )
    if not matches: return "INVALID"
    return {"ENTAILMENT": "ENTAILED", "ENTAILLED": "ENTAILED",
            "CONTRADICTION": "CONTRADICTED", "NEUTRAL": "UNKNOWN"}.get(
                matches[-1], matches[-1])


async def ask(client, endpoint, model, item, semaphore):
    async with semaphore:
        response = await client.post(
            endpoint.rstrip("/") + "/v1/chat/completions",
            json={"model": model, "messages": [{"role": "user", "content": item["prompt"]}],
                  "temperature": 0, "max_tokens": 24,
                  "chat_template_kwargs": {"enable_thinking": False}}, timeout=180)
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        prediction = parse(text)
        return {**item, "response": text, "prediction": prediction,
                "correct": prediction == item["gold"]}


async def run(args):
    items = build_items(); sem = asyncio.Semaphore(args.concurrency)
    async with httpx.AsyncClient() as client:
        rows = await asyncio.gather(*[
            ask(client, args.endpoint, args.model, item, sem) for item in items])
    by = defaultdict(list)
    for row in rows: by[row["condition"]].append(row)
    summary = {"model": args.model, "by_condition": {}}
    for condition, rs in by.items():
        summary["by_condition"][condition] = {
            "n": len(rs), "accuracy": sum(r["correct"] for r in rs)/len(rs),
            "predictions": dict(Counter(r["prediction"] for r in rs)),
        }
    # Paired target signature: adding only the true subclass rule changes a
    # correct UNKNOWN into the invalid ENTAILED answer.
    keyed = {(r["id"].split("_")[0], r["condition"]): r for r in rows}
    summary["rule_induced_narrowing"] = sum(
        keyed[(f"{i:02d}", "narrow_no_rule")]["prediction"] == "UNKNOWN" and
        keyed[(f"{i:02d}", "narrow_explicit")]["prediction"] == "ENTAILED"
        for i in range(len(CASES)))
    out = Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"summary": summary, "rows": rows}, indent=2,
                              ensure_ascii=False))
    print(json.dumps(summary, indent=2))


def main():
    p = argparse.ArgumentParser(); p.add_argument("--endpoint", required=True)
    p.add_argument("--model", required=True); p.add_argument("--output", required=True)
    p.add_argument("--concurrency", type=int, default=48)
    asyncio.run(run(p.parse_args()))


if __name__ == "__main__": main()
