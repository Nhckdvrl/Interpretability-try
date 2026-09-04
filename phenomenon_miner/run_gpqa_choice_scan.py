#!/usr/bin/env python3
"""Test whether hard questions paradoxically require their wrong options."""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import random
from pathlib import Path
from typing import Any

from run_natural_scan import call_chat, normalized


GPQA = Path(
    "/home/xiang/.cache/huggingface/hub/datasets--Idavidrein--gpqa/"
    "snapshots/633f5ee89ab8ad4522a9f850766b73f62147ffdd/gpqa_diamond.csv"
)


def build_requests(seed: int) -> list[dict[str, Any]]:
    with GPQA.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    requests: list[dict[str, Any]] = []
    for item_id, row in enumerate(rows):
        correct = row["Correct Answer"].strip()
        wrong = [row[f"Incorrect Answer {i}"].strip() for i in range(1, 4)]
        options = [correct, *wrong]
        random.Random(f"{seed}:{item_id}").shuffle(options)
        variants: list[tuple[str, list[str]]] = [("all_four", options)]
        for index, removed in enumerate(x for x in options if x != correct):
            variants.append((f"remove_wrong_{index}", [x for x in options if x != removed]))
        variants.append(("only_correct", [correct]))
        for variant, shown in variants:
            option_text = "\n".join(f"- {option}" for option in shown)
            prompt = (
                f"Question: {row['Question'].strip()}\n\n"
                f"Candidate answers:\n{option_text}\n\n"
                "Return only the exact text of the best candidate answer."
            )
            requests.append(
                {
                    "item_id": item_id,
                    "record_id": row["Record ID"],
                    "domain": row["High-level domain"],
                    "question": row["Question"].strip(),
                    "correct": correct,
                    "shown_options": shown,
                    "variant": variant,
                    "prompt": prompt,
                }
            )
    return requests


def main(args: argparse.Namespace) -> None:
    requests = build_requests(args.seed)

    def evaluate(record: dict[str, Any]) -> dict[str, Any]:
        response = call_chat(args.base_url, args.model, record["prompt"])
        return {
            k: v for k, v in record.items() if k != "prompt"
        } | {
            "model": args.model,
            "response": response,
            "is_correct": normalized(response) == normalized(record["correct"]),
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
        "n_items": len(by_item),
        "accuracy": {k: sum(v) / len(v) for k, v in sorted(by_variant.items())},
        "all_four_correct": sum(v["all_four"] for v in by_item.values()),
        "some_wrong_removal_hurts": sum(
            v["all_four"] and any(not v[f"remove_wrong_{i}"] for i in range(3))
            for v in by_item.values()
        ),
        "every_wrong_removal_hurts": sum(
            v["all_four"] and all(not v[f"remove_wrong_{i}"] for i in range(3))
            for v in by_item.values()
        ),
    }
    out.with_suffix(".summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--seed", type=int, default=20260827)
    parser.add_argument("--workers", type=int, default=24)
    main(parser.parse_args())
