"""Build paired complete/incomplete evidence items from cached QA sources."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

from datasets import Dataset

from .io import sha256_file, write_jsonl


def normalize(text: str) -> str:
    text = text.lower().replace("_", " ")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = [token for token in text.split() if token not in {"a", "an", "the"}]
    return " ".join(tokens)


def answer_leaks(answer: str, aliases: list[str], paragraphs: list[dict]) -> bool:
    haystack = f" {normalize(' '.join(p['text'] for p in paragraphs))} "
    return any(f" {normalize(candidate)} " in haystack for candidate in [answer, *aliases]
               if normalize(candidate))


def eligible_item(source: str, source_id: str, question: str, answer: str,
                  aliases: list[str], support: list[dict], distractors: list[dict],
                  stratum: str, metadata: dict) -> dict | None:
    if normalize(answer) in {"yes", "no"} or not (1 <= len(answer.split()) <= 8):
        return None
    if len(answer) > 80 or not (2 <= len(support) <= 4) or len(distractors) < 3:
        return None
    if answer_leaks(answer, aliases, distractors):
        return None
    full = sorted([*support, *distractors], key=lambda paragraph: paragraph["order"])
    full_characters = sum(len(paragraph["title"]) + len(paragraph["text"]) for paragraph in full)
    removed_characters = sum(len(paragraph["title"]) + len(paragraph["text"]) for paragraph in support)
    if not (500 <= full_characters <= 12000) or removed_characters > 6000:
        return None
    return {
        "item_id": f"{source}__{source_id}",
        "source": source,
        "source_id": source_id,
        "stratum": stratum,
        "question": question.strip(),
        "answer": answer.strip(),
        "answer_aliases": sorted(set(alias.strip() for alias in aliases if alias.strip())),
        "full_evidence": full,
        "incomplete_evidence": sorted(distractors, key=lambda paragraph: paragraph["order"]),
        "removed_support": sorted(support, key=lambda paragraph: paragraph["order"]),
        "metadata": metadata,
    }


def hotpot_candidates(path: str) -> list[dict]:
    output = []
    for row in Dataset.from_file(path):
        support_titles = set(row["supporting_facts"]["title"])
        paragraphs = [
            {"order": index, "title": title,
             "text": "".join(row["context"]["sentences"][index]).strip()}
            for index, title in enumerate(row["context"]["title"])
        ]
        support = [paragraph for paragraph in paragraphs if paragraph["title"] in support_titles]
        distractors = [paragraph for paragraph in paragraphs if paragraph["title"] not in support_titles]
        item = eligible_item(
            "hotpotqa", row["id"], row["question"], row["answer"], [], support, distractors,
            row["type"], {"level": row["level"], "support_titles": sorted(support_titles)},
        )
        if item:
            output.append(item)
    return output


def musique_candidates(path: str) -> list[dict]:
    output = []
    for row in Dataset.from_file(path):
        if not row["answerable"]:
            continue
        paragraphs = [
            {"order": int(paragraph["idx"]), "title": paragraph["title"],
             "text": paragraph["paragraph_text"].strip()}
            for paragraph in row["paragraphs"]
        ]
        support = [paragraph for paragraph, original in zip(paragraphs, row["paragraphs"])
                   if original["is_supporting"]]
        distractors = [paragraph for paragraph, original in zip(paragraphs, row["paragraphs"])
                       if not original["is_supporting"]]
        hop = row["id"].split("hop", 1)[0] + "hop"
        item = eligible_item(
            "musique", row["id"], row["question"], row["answer"], row["answer_aliases"],
            support, distractors, hop,
            {"decomposition_steps": len(row["question_decomposition"])},
        )
        if item:
            output.append(item)
    return output


def stratified_select(candidates: list[dict], count: int, seed: int) -> list[dict]:
    grouped = defaultdict(list)
    for item in candidates:
        grouped[item["stratum"]].append(item)
    rng = random.Random(seed)
    for items in grouped.values():
        rng.shuffle(items)
    strata = sorted(grouped)
    selected = []
    cursor = 0
    while len(selected) < count:
        stratum = strata[cursor % len(strata)]
        if grouped[stratum]:
            selected.append(grouped[stratum].pop())
        elif not any(grouped.values()):
            raise ValueError(f"only {len(selected)} eligible items for requested {count}")
        cursor += 1
    return sorted(selected, key=lambda item: item["item_id"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hotpot-arrow", required=True)
    parser.add_argument("--musique-arrow", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--audit", required=True)
    parser.add_argument("--per-source", type=int, default=150)
    parser.add_argument("--seed", type=int, default=20260830)
    args = parser.parse_args()

    pools = {
        "hotpotqa": hotpot_candidates(args.hotpot_arrow),
        "musique": musique_candidates(args.musique_arrow),
    }
    selected = []
    for offset, source in enumerate(sorted(pools)):
        selected.extend(stratified_select(pools[source], args.per_source, args.seed + offset))
    selected.sort(key=lambda item: item["item_id"])
    write_jsonl(args.output, selected)
    audit = []
    for source in sorted(pools):
        local = [item for item in selected if item["source"] == source][:20]
        for item in local:
            canonical = json.dumps(item["full_evidence"], ensure_ascii=False, sort_keys=True)
            audit.append({
                "item_id": item["item_id"],
                "source_id": item["source_id"],
                "source": source,
                "question": item["question"],
                "answer": item["answer"],
                "removed_titles": [paragraph["title"] for paragraph in item["removed_support"]],
                "full_evidence_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
            })
    write_jsonl(args.audit, audit)
    summary = {
        "contract_id": "019-d0-v1",
        "source_revisions": {
            "hotpotqa": "1908d6afbbead072334abe2965f91bd2709910ab",
            "musique": "c8f4f8c9465fb69d31a8eae894c3fd509c4ca321",
        },
        "source_arrow_sha256": {
            "hotpotqa": sha256_file(args.hotpot_arrow),
            "musique": sha256_file(args.musique_arrow),
        },
        "eligible": {source: len(items) for source, items in pools.items()},
        "eligible_strata": {
            source: dict(sorted(Counter(item["stratum"] for item in items).items()))
            for source, items in pools.items()
        },
        "selected": dict(sorted(Counter(item["source"] for item in selected).items())),
        "selected_strata": dict(sorted(Counter(
            f"{item['source']}__{item['stratum']}" for item in selected
        ).items())),
        "seed": args.seed,
    }
    summary["bank_sha256"] = sha256_file(args.output)
    Path(args.summary).parent.mkdir(parents=True, exist_ok=True)
    Path(args.summary).write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
