#!/usr/bin/env python3
"""Probe graph-isomorphic StepGame instances under entity-name changes."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import random
import re
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

from datasets import load_dataset


HUMAN = ["Alice", "Bob", "Carol", "David", "Emma", "Frank", "Grace", "Henry", "Iris", "James", "Karen", "Leo"]
NONCE = ["Zorp", "Flim", "Dax", "Nup", "Krel", "Vesh", "Tob", "Miv", "Prax", "Seln", "Gub", "Wex"]
LABELS = ["upper-left", "above", "upper-right", "left", "right", "lower-left", "below", "lower-right", "overlap"]


def rename(text: str, mapping: dict[str, str]) -> str:
    return re.sub(r"\b[A-Z]\b", lambda m: mapping.get(m.group(0), m.group(0)), text)


def entities(row: dict[str, Any]) -> list[str]:
    text = " ".join(row["story"] + [row["question"]])
    return sorted(set(re.findall(r"\b[A-Z]\b", text)))


def make_mapping(names: list[str], pool: list[str], key: str) -> dict[str, str]:
    selected = pool[:]
    random.Random(key).shuffle(selected)
    return dict(zip(names, selected))


def build(per_hop: int, seed: int) -> list[dict[str, Any]]:
    data = load_dataset("ZhengyanShi/StepGame", split="validation")
    by_hop: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in data:
        by_hop[int(row["k_hop"])].append(row)
    rng = random.Random(seed)
    variants = ["original_letters", "permuted_letters", "human_names", "nonce_names"]
    out = []
    item_id = 0
    for hop in sorted(by_hop):
        rng.shuffle(by_hop[hop])
        for row in by_hop[hop][:per_hop]:
            ents = entities(row)
            pools = {
                "original_letters": ents,
                "permuted_letters": list(reversed(ents)),
                "human_names": HUMAN,
                "nonce_names": NONCE,
            }
            for variant in variants:
                mapping = make_mapping(ents, pools[variant], f"{seed}:{item_id}:{variant}")
                # Preserve original names exactly in the baseline.
                if variant == "original_letters":
                    mapping = {x: x for x in ents}
                story = [rename(s, mapping) for s in row["story"]]
                question = rename(row["question"], mapping)
                prompt = (
                    "Use the statements to determine the spatial relation.\n\n"
                    + "\n".join(f"- {s}" for s in story)
                    + f"\n\nQuestion: {question}\n"
                    + "Choose exactly one answer: " + ", ".join(LABELS) + ".\nAnswer:"
                )
                out.append({"item_id": item_id, "hop": hop, "variant": variant, "label": row["label"], "prompt": prompt})
            item_id += 1
    return out


def parse(text: str) -> str:
    t = text.casefold().replace("_", "-")
    aliases = {"northwest": "upper-left", "north-east": "upper-right", "northeast": "upper-right",
               "southwest": "lower-left", "south-east": "lower-right", "southeast": "lower-right",
               "north": "above", "south": "below", "east": "right", "west": "left",
               "same": "overlap", "overlapping": "overlap"}
    for label in LABELS:
        if re.search(rf"(?<!\w){re.escape(label)}(?!\w)", t):
            return label
    for key, value in aliases.items():
        if re.search(rf"(?<!\w){re.escape(key)}(?!\w)", t):
            return value
    return ""


def call(base_url: str, model: str, prompt: str) -> str:
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0,
               "max_tokens": 20, "chat_template_kwargs": {"enable_thinking": False}}
    req = urllib.request.Request(f"{base_url.rstrip('/')}/v1/chat/completions", data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    last = None
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
    requests = build(args.per_hop, args.seed)
    def evaluate(x: dict[str, Any]) -> dict[str, Any]:
        response = call(args.base_url, args.model, x["prompt"])
        parsed = parse(response)
        return {k: v for k, v in x.items() if k != "prompt"} | {"response": response, "parsed": parsed,
                                                               "is_correct": parsed == x["label"], "model": args.model}
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(evaluate, x) for x in requests]
        for done, future in enumerate(concurrent.futures.as_completed(futures), 1):
            results.append(future.result())
            if done % 200 == 0:
                print(f"completed {done}/{len(futures)}", flush=True)
    results.sort(key=lambda x: (x["item_id"], x["variant"]))
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for x in results: f.write(json.dumps(x, ensure_ascii=False) + "\n")
    cells: dict[tuple[str, int], list[bool]] = defaultdict(list)
    item: dict[int, dict[str, bool]] = defaultdict(dict)
    for x in results:
        cells[(x["variant"], x["hop"])].append(x["is_correct"]); item[x["item_id"]][x["variant"]] = x["is_correct"]
    summary = {"model": args.model, "n_items": len(item), "accuracy_by_hop": {
        v: {str(h): sum(cells[(v,h)])/len(cells[(v,h)]) for h in range(1,6)}
        for v in ["original_letters", "permuted_letters", "human_names", "nonce_names"]},
        "paired_vs_original": {v: {"helps": sum(not q["original_letters"] and q[v] for q in item.values()),
                                    "hurts": sum(q["original_letters"] and not q[v] for q in item.values())}
                               for v in ["permuted_letters", "human_names", "nonce_names"]}}
    out.with_suffix(".summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


def cli() -> argparse.Namespace:
    p=argparse.ArgumentParser(); p.add_argument("--base-url", required=True); p.add_argument("--model", required=True)
    p.add_argument("--out", required=True); p.add_argument("--per-hop", type=int, default=50); p.add_argument("--seed", type=int, default=20260827)
    p.add_argument("--workers", type=int, default=24); return p.parse_args()


if __name__ == "__main__": run(cli())
