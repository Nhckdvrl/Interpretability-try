#!/usr/bin/env python3
"""Scan whether truthful provenance changes use of identical evidence facts.

This is a discovery probe, not a benchmark proposal.  Every condition contains
the same query and the same evidence facts in the same order.  Only truthful
source/title metadata and whether it precedes or follows each fact changes.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import random
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from datasets import Dataset


DATA = Path(
    "/home/xiang/.cache/huggingface/datasets/yixuantt___multi_hop_rag/"
    "MultiHopRAG/0.0.0/71ac0d0bd1f951d2d6b70311f7d2ae404e1ffa82/"
    "multi_hop_rag-train.arrow"
)


def norm(text: str) -> str:
    text = text.casefold().replace("’", "'")
    text = re.sub(r"[^\w]+", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def correct(response: str, answer: str) -> bool:
    r, a = norm(response), norm(answer)
    return bool(a) and (r == a or re.search(rf"(?<!\w){re.escape(a)}(?!\w)", r) is not None)


def render(evidence: list[dict[str, Any]], variant: str) -> str:
    blocks = []
    for i, e in enumerate(evidence, 1):
        fact = e["fact"].strip()
        source = e["source"].strip()
        title = e["title"].strip()
        if variant == "facts_only":
            block = f"Evidence {i}: {fact}"
        elif variant == "source_before":
            block = f"Evidence {i} (Source: {source}): {fact}"
        elif variant == "source_title_before":
            block = f"Evidence {i}\nSource: {source}\nTitle: {title}\nFact: {fact}"
        elif variant == "source_title_after":
            block = f"Evidence {i}\nFact: {fact}\nSource: {source}\nTitle: {title}"
        else:
            raise ValueError(variant)
        blocks.append(block)
    return "\n\n".join(blocks)


def build(limit: int, seed: int) -> list[dict[str, Any]]:
    rows = list(Dataset.from_file(str(DATA)))
    # Avoid answers for which substring scoring is intrinsically ambiguous.
    rows = [x for x in rows if 1 <= len(x["answer"].split()) <= 12 and len(x["evidence_list"]) <= 6]
    random.Random(seed).shuffle(rows)
    variants = ["facts_only", "source_before", "source_title_before", "source_title_after"]
    out = []
    for item_id, row in enumerate(rows[:limit]):
        for variant in variants:
            prompt = (
                "Answer the question using the evidence. Return only the shortest exact answer, "
                "with no explanation.\n\n"
                f"{render(row['evidence_list'], variant)}\n\n"
                f"Question: {row['query']}\nAnswer:"
            )
            out.append({
                "item_id": item_id,
                "variant": variant,
                "prompt": prompt,
                "query": row["query"],
                "answer": row["answer"],
                "question_type": row["question_type"],
                "n_evidence": len(row["evidence_list"]),
            })
    return out


def call(base_url: str, model: str, prompt: str) -> str:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 48,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    last: Exception | None = None
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=180) as response:
                data = json.load(response)
            msg = data["choices"][0]["message"]
            return (msg.get("content") or msg.get("reasoning_content") or "").strip()
        except (urllib.error.URLError, TimeoutError) as error:
            last = error
            time.sleep(2**attempt)
    raise RuntimeError(last)


def run(args: argparse.Namespace) -> None:
    requests = build(args.limit, args.seed)

    def evaluate(x: dict[str, Any]) -> dict[str, Any]:
        response = call(args.base_url, args.model, x["prompt"])
        return {k: v for k, v in x.items() if k != "prompt"} | {
            "response": response,
            "is_correct": correct(response, x["answer"]),
            "model": args.model,
        }

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(evaluate, x) for x in requests]
        for done, future in enumerate(concurrent.futures.as_completed(futures), 1):
            results.append(future.result())
            if done % 100 == 0:
                print(f"completed {done}/{len(futures)}", flush=True)
    results.sort(key=lambda x: (x["item_id"], x["variant"]))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        for row in results:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    by_variant: dict[str, list[bool]] = {}
    by_item: dict[int, dict[str, bool]] = {}
    for row in results:
        by_variant.setdefault(row["variant"], []).append(row["is_correct"])
        by_item.setdefault(row["item_id"], {})[row["variant"]] = row["is_correct"]
    base = "facts_only"
    paired = {}
    for variant in sorted(by_variant):
        if variant == base:
            continue
        paired[variant] = {
            "helps": sum(not x[base] and x[variant] for x in by_item.values()),
            "hurts": sum(x[base] and not x[variant] for x in by_item.values()),
        }
    summary = {
        "model": args.model,
        "n_items": args.limit,
        "accuracy": {k: sum(v) / len(v) for k, v in sorted(by_variant.items())},
        "paired_vs_facts_only": paired,
    }
    out.with_suffix(".summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


def args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--base-url", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--limit", type=int, default=100)
    p.add_argument("--seed", type=int, default=20260827)
    p.add_argument("--workers", type=int, default=24)
    return p.parse_args()


if __name__ == "__main__":
    run(args())
