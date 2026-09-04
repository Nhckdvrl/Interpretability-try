#!/usr/bin/env python3
"""Scan the original FraCaS semantic test suite for structured failures."""

import argparse
import asyncio
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import httpx


GOLD = {"yes": "ENTAILED", "no": "CONTRADICTED", "unknown": "UNKNOWN",
        "don't know": "UNKNOWN"}


def load_rows(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8"), delimiter="\t"))
    out = []
    for row in rows:
        answer = row["answer"].strip().lower()
        if answer not in GOLD:
            continue
        premise = row["premises_original"].strip()
        hypothesis = row["hypothesis_original"].strip()
        if not premise or not hypothesis:
            continue
        out.append({
            "id": row["id"], "topic": row["topic"], "premise": premise,
            "hypothesis": hypothesis, "gold": GOLD[answer], "note": row["note"],
        })
    return out


def parse(text):
    matches = re.findall(
        r"\b(ENTAILED|ENTAILMENT|ENTAILLED|CONTRADICTED|CONTRADICTION|UNKNOWN|NEUTRAL)\b",
        text.upper(),
    )
    if not matches:
        return "INVALID"
    return {
        "ENTAILMENT": "ENTAILED", "ENTAILLED": "ENTAILED",
        "CONTRADICTION": "CONTRADICTED", "NEUTRAL": "UNKNOWN",
    }.get(matches[-1], matches[-1])


async def ask(client, endpoint, model, row, semaphore):
    prompt = (
        "Premises:\n" + row["premise"] + "\n\nHypothesis:\n" + row["hypothesis"]
        + "\n\nBased only on the premises, is the hypothesis definitely entailed, "
          "definitely contradicted, or neither? Answer only ENTAILED, CONTRADICTED, "
          "or UNKNOWN."
    )
    async with semaphore:
        response = await client.post(
            endpoint.rstrip("/") + "/v1/chat/completions",
            json={"model": model, "messages": [{"role": "user", "content": prompt}],
                  "temperature": 0, "max_tokens": 12,
                  "chat_template_kwargs": {"enable_thinking": False}},
            timeout=180,
        )
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        return {**row, "response": text, "prediction": parse(text),
                "correct": parse(text) == row["gold"]}


async def run(args):
    rows = load_rows(args.data)
    semaphore = asyncio.Semaphore(args.concurrency)
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*[
            ask(client, args.endpoint, args.model, row, semaphore) for row in rows
        ])
    by_topic = defaultdict(list)
    confusion = Counter()
    for row in results:
        by_topic[row["topic"]].append(row["correct"])
        confusion[(row["gold"], row["prediction"])] += 1
    summary = {
        "model": args.model,
        "n": len(results),
        "accuracy": sum(r["correct"] for r in results) / len(results),
        "by_topic": {k: {"n": len(v), "accuracy": sum(v) / len(v)}
                     for k, v in sorted(by_topic.items())},
        "confusion": {f"{a}->{b}": n for (a, b), n in sorted(confusion.items())},
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"summary": summary, "rows": results}, indent=2,
                              ensure_ascii=False))
    print(json.dumps(summary, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--concurrency", type=int, default=48)
    asyncio.run(run(parser.parse_args()))


if __name__ == "__main__":
    main()
