#!/usr/bin/env python3
"""Current-model smoke test for same-name entity merging on public AmbigDocs."""
import argparse
import concurrent.futures
import json
import random
import re
import urllib.request
from pathlib import Path


def norm(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def call(url, model, prompt):
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 320,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    req = urllib.request.Request(
        url.rstrip("/") + "/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=240) as response:
        return json.load(response)["choices"][0]["message"]["content"]


def make_items(path, n, seed):
    rows = json.load(open(path))
    eligible = [
        row for row in rows
        if 2 <= len(row["documents"]) <= 4
        and sum(len(doc["text"]) for doc in row["documents"]) <= 10500
        and len({norm(doc["answer"]) for doc in row["documents"]}) == len(row["documents"])
    ]
    random.Random(seed).shuffle(eligible)
    items = []
    for row in eligible[:n]:
        docs = "\n\n".join(
            f"DOCUMENT {i+1} — {doc['title']}\n{doc['text']}"
            for i, doc in enumerate(row["documents"])
        )
        prompt = (
            f"Several distinct entities share the name {row['ambiguous_entity']!r}.\n\n{docs}\n\n"
            f"Question: {row['question']}\n\n"
            "Answer separately for every entity represented above. Use exactly one line per entity in the form "
            "FULL DOCUMENT TITLE: ANSWER. Do not merge entities."
        )
        items.append({"qid": row["qid"], "question": row["question"], "documents": row["documents"], "prompt": prompt})
    return items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--data", default="phenomenon_miner/data/ambigdocs/dev.json")
    parser.add_argument("--n", type=int, default=40)
    parser.add_argument("--seed", type=int, default=37)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    items = make_items(args.data, args.n, args.seed)

    def run(item):
        output = call(args.url, args.model, item["prompt"])
        nout = norm(output)
        title_hits = [norm(doc["title"]) in nout for doc in item["documents"]]
        answer_hits = [norm(doc["answer"]) in nout for doc in item["documents"]]
        return {
            "qid": item["qid"],
            "question": item["question"],
            "documents": item["documents"],
            "output": output,
            "title_hits": title_hits,
            "answer_hits": answer_hits,
            "complete": all(title_hits) and all(answer_hits),
            "all_answers_without_all_identities": all(answer_hits) and not all(title_hits),
        }

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        records = list(pool.map(run, items))
    total_slots = sum(len(x["documents"]) for x in records)
    summary = {
        "model": args.model,
        "n": len(records),
        "complete_rate": sum(x["complete"] for x in records) / len(records),
        "title_slot_recall": sum(sum(x["title_hits"]) for x in records) / total_slots,
        "answer_slot_recall": sum(sum(x["answer_hits"]) for x in records) / total_slots,
        "all_answers_without_all_identities_rate": sum(x["all_answers_without_all_identities"] for x in records) / len(records),
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps({"summary": summary, "records": records}, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
