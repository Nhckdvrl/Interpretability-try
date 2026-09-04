#!/usr/bin/env python3
"""Paired polarity-invariance audit on naturally occurring NOPE items."""

import argparse
import asyncio
import csv
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

import httpx


LABELS = {"E": "ENTAILMENT", "C": "CONTRADICTION", "N": "UNKNOWN"}


def load_pairs(path: Path, limit: int, seed: int):
    groups = defaultdict(dict)
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            uid = row["uid"]
            if uid.endswith("-neg"):
                key, side = uid[:-4], "negated"
            else:
                key, side = uid, "original"
            groups[key][side] = row
    pairs = []
    for key, pair in groups.items():
        if set(pair) != {"original", "negated"}:
            continue
        a, b = pair["original"], pair["negated"]
        if a["hypothesis"] != b["hypothesis"] or a["label"] != b["label"]:
            continue
        if a["label"] not in LABELS:
            continue
        pairs.append({
            "id": key,
            "original": a["premise"],
            "negated": b["premise"],
            "hypothesis": a["hypothesis"],
            "gold": LABELS[a["label"]],
            "trigger_type": a["trigger_type"],
        })
    random.Random(seed).shuffle(pairs)
    return pairs[:limit]


def prompt(premise, hypothesis):
    return (
        f'Passage: "{premise}"\n'
        f'Statement: "{hypothesis}"\n'
        "Based only on the passage, is the statement necessarily true, necessarily false, "
        "or neither? Answer only ENTAILMENT, CONTRADICTION, or UNKNOWN."
    )


def parse(text):
    m = re.search(r"\b(ENTAILMENT|CONTRADICTION|UNKNOWN)\b", text.upper())
    return m.group(1) if m else "INVALID"


async def query(client, url, model, item, side, sem):
    async with sem:
        response = await client.post(
            f"{url}/v1/chat/completions",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt(item[side], item["hypothesis"])}],
                "temperature": 0,
                "max_tokens": 24,
                "chat_template_kwargs": {"enable_thinking": False},
            },
            timeout=120,
        )
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        return side, text, parse(text)


async def main_async(args):
    items = load_pairs(Path(args.data), args.limit, args.seed)
    sem = asyncio.Semaphore(args.concurrency)
    async with httpx.AsyncClient() as client:
        tasks = [query(client, args.base_url, args.model, x, side, sem)
                 for x in items for side in ("original", "negated")]
        answers = await asyncio.gather(*tasks)
    for item, pair_answers in zip(items, zip(answers[::2], answers[1::2])):
        for side, text, pred in pair_answers:
            item[f"{side}_response"] = text
            item[f"{side}_prediction"] = pred
    n = len(items)
    summary = {
        "model": args.model,
        "n_pairs": n,
        "original_accuracy": sum(x["original_prediction"] == x["gold"] for x in items) / n,
        "negated_accuracy": sum(x["negated_prediction"] == x["gold"] for x in items) / n,
        "pair_consistency": sum(x["original_prediction"] == x["negated_prediction"] for x in items) / n,
        "both_correct": sum(x["original_prediction"] == x["gold"] == x["negated_prediction"] for x in items) / n,
        "flip_counts": dict(Counter(
            f'{x["original_prediction"]}->{x["negated_prediction"]}' for x in items
            if x["original_prediction"] != x["negated_prediction"]
        )),
    }
    Path(args.output).write_text(json.dumps({"summary": summary, "rows": items}, ensure_ascii=False, indent=2))
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", default="phenomenon_miner/data/NOPE_raw/nli_corpus.main.csv")
    p.add_argument("--base-url", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--limit", type=int, default=400)
    p.add_argument("--seed", type=int, default=31)
    p.add_argument("--concurrency", type=int, default=32)
    asyncio.run(main_async(p.parse_args()))


if __name__ == "__main__":
    main()
