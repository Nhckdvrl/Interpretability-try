#!/usr/bin/env python3
"""Mine simple monotonicity violations on the public SciQ test set.

The scanner deliberately starts with relations that have a one-sentence natural
interpretation: correct support should not hurt, repeating the same correct
support should not hurt, and deleting a wrong option should not hurt.
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

import pyarrow.parquet as pq


SCIQ_TEST = Path(
    "/home/xiang/.cache/huggingface/hub/datasets--allenai--sciq/"
    "snapshots/2c94ad3e1aafab77146f384e23536f97a4849815/"
    "data/test-00000-of-00001.parquet"
)


def normalized(text: str) -> str:
    text = text.strip().splitlines()[0] if text.strip() else ""
    text = re.sub(r"^(answer\s*[:=-]?\s*)", "", text, flags=re.I)
    text = text.strip().strip("`*_ .,:;!?\"'")
    return re.sub(r"\s+", " ", text).casefold()


def build_items(limit: int, seed: int) -> list[dict[str, Any]]:
    rows = pq.read_table(SCIQ_TEST).to_pylist()
    rng = random.Random(seed)
    rng.shuffle(rows)
    out: list[dict[str, Any]] = []
    for item_id, row in enumerate(rows[:limit]):
        correct = row["correct_answer"].strip()
        wrong = [row[f"distractor{i}"] .strip() for i in range(1, 4)]
        options = [correct, *wrong]
        random.Random(f"{seed}:{item_id}").shuffle(options)
        base = {
            "item_id": item_id,
            "question": row["question"].strip(),
            "support": row["support"].strip(),
            "correct": correct,
            "options": options,
        }
        out.extend(make_variants(base))
    return out


def make_variants(base: dict[str, Any]) -> list[dict[str, Any]]:
    variants: list[tuple[str, str, list[str]]] = [
        ("closed_book", "", base["options"]),
        ("support_x1", base["support"], base["options"]),
        ("support_x2", "\n\n".join([base["support"]] * 2), base["options"]),
        ("support_x4", "\n\n".join([base["support"]] * 4), base["options"]),
    ]
    wrong = [x for x in base["options"] if x != base["correct"]]
    for index, removed in enumerate(wrong):
        variants.append(
            (
                f"remove_wrong_{index}",
                base["support"],
                [x for x in base["options"] if x != removed],
            )
        )
    variants.append(("only_correct", base["support"], [base["correct"]]))

    records: list[dict[str, Any]] = []
    for name, support, options in variants:
        evidence = f"Background evidence:\n{support}\n\n" if support else ""
        option_text = "\n".join(f"- {option}" for option in options)
        prompt = (
            f"{evidence}Question: {base['question']}\n\n"
            f"Candidate answers:\n{option_text}\n\n"
            "Return only the exact text of the best candidate answer."
        )
        records.append({**base, "variant": name, "prompt": prompt, "shown_options": options})
    return records


def call_chat(base_url: str, model: str, prompt: str) -> str:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 32,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    last_error: Exception | None = None
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                data = json.load(response)
            message = data["choices"][0]["message"]
            return (message.get("content") or message.get("reasoning_content") or "").strip()
        except (urllib.error.URLError, TimeoutError) as error:
            last_error = error
            time.sleep(2**attempt)
    raise RuntimeError(f"request failed after retries: {last_error}")


def run(args: argparse.Namespace) -> None:
    requests = build_items(args.limit, args.seed)

    def evaluate(record: dict[str, Any]) -> dict[str, Any]:
        response = call_chat(args.base_url, args.model, record["prompt"])
        return {
            "item_id": record["item_id"],
            "variant": record["variant"],
            "question": record["question"],
            "support": record["support"],
            "correct": record["correct"],
            "shown_options": record["shown_options"],
            "response": response,
            "is_correct": normalized(response) == normalized(record["correct"]),
            "model": args.model,
        }

    results: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(evaluate, record) for record in requests]
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
    summary = {
        "model": args.model,
        "n_items": args.limit,
        "accuracy": {k: sum(v) / len(v) for k, v in sorted(by_variant.items())},
        "violations": {
            "support_hurts": sum(v["closed_book"] and not v["support_x1"] for v in by_item.values()),
            "repeat_x2_hurts": sum(v["support_x1"] and not v["support_x2"] for v in by_item.values()),
            "repeat_x4_hurts": sum(v["support_x1"] and not v["support_x4"] for v in by_item.values()),
            "some_wrong_removal_hurts": sum(
                v["support_x1"] and any(not v[f"remove_wrong_{i}"] for i in range(3))
                for v in by_item.values()
            ),
        },
    }
    summary_path = out.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260827)
    parser.add_argument("--workers", type=int, default=32)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
