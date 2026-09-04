#!/usr/bin/env python3
"""Check whether identity/cardinality dissociation survives natural readouts."""

import argparse
import asyncio
import json
import re
from collections import defaultdict
from pathlib import Path

import httpx

from run_identity_cardinality import build_items


READOUTS = {
    "unique_individuals_open": (
        "How many unique human individuals authorized the action? "
        "Answer with a single integer.",
        "count",
    ),
    "deduplicated_people_open": (
        "After merging every name or role reference that denotes the same person, "
        "how many people remain among the approvers? Answer with a single integer.",
        "count",
    ),
    "two_humans": (
        "Did at least two distinct human beings authorize the action? "
        "Answer only YES or NO.",
        "binary",
    ),
    "one_person_twice": (
        "Did one person approve twice while acting in two roles? Answer only YES or NO.",
        "one_person_binary",
    ),
    "reversed_count_options": (
        "How many distinct people submitted approvals: 2 or 1? Answer only 2 or 1.",
        "count",
    ),
}


def parse(text, kind):
    patterns = {
        "count": r"\b([12])\b",
        "binary": r"\b(YES|NO)\b",
        "one_person_binary": r"\b(YES|NO)\b",
        "choice": r"\b([AB])\b",
    }
    matches = re.findall(patterns[kind], text.upper())
    return matches[-1] if matches else "INVALID"


async def ask_long(client, endpoint, model, prompt, semaphore):
    async with semaphore:
        response = await client.post(
            f"{endpoint}/v1/chat/completions",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "max_tokens": 160,
                "chat_template_kwargs": {"enable_thinking": False},
            },
            timeout=180,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()


async def run(args):
    wanted = {"same_name", "same_alias_log", "same_named_log", "distinct_named_log"}
    items = [item for item in build_items() if item["condition"] in wanted]
    semaphore = asyncio.Semaphore(args.concurrency)
    specs = []
    async with httpx.AsyncClient() as client:
        tasks = []
        for item in items:
            same = item["identity_gold"] == "YES"
            for readout, (question, kind) in READOUTS.items():
                gold = {
                    "count": "1" if same else "2",
                    "binary": "NO" if same else "YES",
                    "one_person_binary": "YES" if same else "NO",
                    "choice": "A" if same else "B",
                }[kind]
                specs.append((item, readout, kind, gold))
                tasks.append(
                    ask_long(client, args.endpoint, args.model,
                             item["context"] + "\n\n" + question, semaphore)
                )
        outputs = await asyncio.gather(*tasks)

    rows = []
    for (item, readout, kind, gold), output in zip(specs, outputs):
        prediction = parse(output, kind)
        rows.append({
            "id": item["id"], "domain": item["domain"],
            "condition": item["condition"], "readout": readout,
            "gold": gold, "prediction": prediction, "response": output,
            "correct": prediction == gold,
        })

    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["condition"], row["readout"])].append(row["correct"])
    summary = {
        condition: {
            readout: sum(grouped[(condition, readout)]) / len(grouped[(condition, readout)])
            for readout in READOUTS
        }
        for condition in sorted(wanted)
    }
    result = {"model": args.model, "summary": summary, "rows": rows}
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(json.dumps({"model": args.model, "summary": summary}, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--concurrency", type=int, default=32)
    asyncio.run(run(parser.parse_args()))


if __name__ == "__main__":
    main()
