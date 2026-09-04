#!/usr/bin/env python3
"""Minimal, neutral-prompt audit of event actuality on MAVEN-Fact."""

import argparse
import asyncio
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

import httpx


GOLD = {"CT+": "YES", "CT-": "NO", "PS+": "UNCERTAIN", "PS-": "UNCERTAIN", "Uu": "UNCERTAIN"}


def load_items(path: Path, per_label: int, seed: int):
    pools = defaultdict(list)
    with path.open() as f:
        for line in f:
            doc = json.loads(line)
            for event in doc["events"]:
                for mention in event["mention"]:
                    label = mention["factuality"]
                    if label not in {"CT+", "CT-", "PS+"}:
                        continue
                    sentence = doc["sentences"][mention["sent_id"]]
                    pools[label].append({
                        "doc_id": doc["id"],
                        "sentence": sentence,
                        "trigger": mention["trigger_word"],
                        "evidence": mention.get("evidence_word"),
                        "label": label,
                        "gold": GOLD[label],
                    })
    rng = random.Random(seed)
    out = []
    for label in ("CT+", "CT-", "PS+"):
        rng.shuffle(pools[label])
        out.extend(pools[label][:per_label])
    rng.shuffle(out)
    return out


def prompt(item):
    return (
        f'Sentence: "{item["sentence"]}"\n'
        f'Question: Does the sentence present the event “{item["trigger"]}” as something that definitely happened?\n'
        "Answer only YES, NO, or UNCERTAIN."
    )


def parse_answer(text):
    m = re.search(r"\b(YES|NO|UNCERTAIN)\b", text.upper())
    return m.group(1) if m else "INVALID"


async def query(client, base_url, model, item, sem):
    async with sem:
        response = await client.post(
            f"{base_url}/v1/chat/completions",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt(item)}],
                "temperature": 0,
                "max_tokens": 32,
                "chat_template_kwargs": {"enable_thinking": False},
            },
            timeout=120,
        )
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        return {**item, "response": text, "prediction": parse_answer(text)}


async def main_async(args):
    items = load_items(Path(args.data), args.per_label, args.seed)
    sem = asyncio.Semaphore(args.concurrency)
    async with httpx.AsyncClient() as client:
        rows = await asyncio.gather(*(query(client, args.base_url, args.model, x, sem) for x in items))
    by_label = {}
    for label in ("CT+", "CT-", "PS+"):
        subset = [x for x in rows if x["label"] == label]
        by_label[label] = {
            "n": len(subset),
            "accuracy": sum(x["prediction"] == x["gold"] for x in subset) / len(subset),
            "predictions": dict(Counter(x["prediction"] for x in subset)),
        }
    summary = {
        "model": args.model,
        "n": len(rows),
        "accuracy": sum(x["prediction"] == x["gold"] for x in rows) / len(rows),
        "by_label": by_label,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"summary": summary, "rows": rows}, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", default="phenomenon_miner/data/MAVEN-FACT/data/valid.jsonl")
    p.add_argument("--base-url", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--per-label", type=int, default=100)
    p.add_argument("--seed", type=int, default=17)
    p.add_argument("--concurrency", type=int, default=24)
    args = p.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
