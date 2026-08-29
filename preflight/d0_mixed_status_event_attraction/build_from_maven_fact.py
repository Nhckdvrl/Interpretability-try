#!/usr/bin/env python3
"""Build a data-first D0 bank for Mixed-Status Event Attraction.

This script does NOT invent scenarios. It preserves MAVEN-FACT documents and
source-authored factuality labels, then enumerates naturally co-occurring event
mentions with different factuality states inside the same document.

Outputs:
  raw_mentions.jsonl       one row per annotated event mention
  eligible_pairs.jsonl     all same-document mixed-status ordered pairs
  audit_sample.jsonl       deterministic source-audit sample
  scope_summary.json       counts / attrition / factor coverage
  AUDIT_SAMPLE.md          human-readable sample for the mandatory D0 audit

Usage with the Hugging Face mirror:
  python build_from_maven_fact.py --output-dir data/maven_d0

Usage with the official downloaded JSONL files:
  python build_from_maven_fact.py \
      --input-jsonl /path/to/train.jsonl /path/to/valid.jsonl \
      --output-dir data/maven_d0
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Iterator

FACTUALITY = {"CT+", "PS+", "PS-", "CT-", "Uu"}
DECISIVE_NONFACT = {"PS+", "PS-", "CT-"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--input-jsonl", nargs="*", type=Path, default=[])
    p.add_argument("--hf-dataset", default="upasanachatterjee/maven-fact")
    p.add_argument("--hf-splits", nargs="+", default=["train", "validation"])
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--audit-n", type=int, default=40)
    return p.parse_args()


def iter_jsonl(paths: list[Path]) -> Iterator[dict[str, Any]]:
    for path in paths:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield json.loads(line)


def iter_hf(name: str, splits: list[str]) -> Iterator[dict[str, Any]]:
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise SystemExit(
            "datasets is required when --input-jsonl is not supplied: pip install datasets"
        ) from exc
    for split in splits:
        try:
            ds = load_dataset(name, split=split)
        except Exception:
            # Mirrors sometimes call the dev split 'test' or omit validation.
            # A missing requested split is not silently substituted.
            continue
        for row in ds:
            row = dict(row)
            row["_source_split"] = split
            yield row


def sentence_text(doc: dict[str, Any], sent_id: int) -> str:
    sents = doc.get("sentences") or []
    if 0 <= sent_id < len(sents):
        return str(sents[sent_id])
    toks = doc.get("tokens") or []
    if 0 <= sent_id < len(toks):
        return " ".join(map(str, toks[sent_id]))
    return ""


def flatten_mentions(doc: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    doc_id = str(doc.get("id", ""))
    title = str(doc.get("title", ""))
    source_split = str(doc.get("_source_split", "official_jsonl"))
    for event in doc.get("events") or []:
        event_id = str(event.get("id", ""))
        event_type = str(event.get("type", ""))
        for mention in event.get("mention") or []:
            factuality = mention.get("factuality")
            if factuality not in FACTUALITY:
                continue
            sent_id = int(mention.get("sent_id", -1))
            rows.append(
                {
                    "doc_id": doc_id,
                    "title": title,
                    "source_split": source_split,
                    "event_id": event_id,
                    "event_type": event_type,
                    "mention_id": str(mention.get("id", "")),
                    "trigger_word": str(mention.get("trigger_word", "")),
                    "sent_id": sent_id,
                    "sentence": sentence_text(doc, sent_id),
                    "factuality": factuality,
                    "evidence_word": mention.get("evidence_word") or [],
                }
            )
    return rows


def stable_key(row: dict[str, Any]) -> str:
    payload = "|".join(
        [
            row["doc_id"],
            row["left_mention_id"],
            row["right_mention_id"],
            row["left_factuality"],
            row["right_factuality"],
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def enumerate_pairs(mentions: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:
    # Ordered pairs are intentional: attraction may be directional.
    for i, left in enumerate(mentions):
        for j, right in enumerate(mentions):
            if i == j:
                continue
            if left["event_id"] == right["event_id"]:
                continue
            if left["factuality"] == right["factuality"]:
                continue
            distance = abs(left["sent_id"] - right["sent_id"])
            decisive = (
                (left["factuality"] == "CT+" and right["factuality"] in DECISIVE_NONFACT)
                or (right["factuality"] == "CT+" and left["factuality"] in DECISIVE_NONFACT)
            )
            yield {
                "doc_id": left["doc_id"],
                "title": left["title"],
                "source_split": left["source_split"],
                "left_event_id": left["event_id"],
                "left_mention_id": left["mention_id"],
                "left_event_type": left["event_type"],
                "left_trigger": left["trigger_word"],
                "left_sent_id": left["sent_id"],
                "left_sentence": left["sentence"],
                "left_factuality": left["factuality"],
                "right_event_id": right["event_id"],
                "right_mention_id": right["mention_id"],
                "right_event_type": right["event_type"],
                "right_trigger": right["trigger_word"],
                "right_sent_id": right["sent_id"],
                "right_sentence": right["sentence"],
                "right_factuality": right["factuality"],
                "sentence_distance": distance,
                "same_sentence": left["sent_id"] == right["sent_id"],
                "decisive_ct_plus_vs_nonfact": decisive,
                "pair_class": f"{left['factuality']}->{right['factuality']}",
            }


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    n = 0
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    return n


def main() -> None:
    args = parse_args()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    docs = iter_jsonl(args.input_jsonl) if args.input_jsonl else iter_hf(args.hf_dataset, args.hf_splits)

    mention_path = out / "raw_mentions.jsonl"
    pair_path = out / "eligible_pairs.jsonl"
    pair_counts: Counter[str] = Counter()
    distance_counts: Counter[str] = Counter()
    split_counts: Counter[str] = Counter()
    docs_with_mixed = 0
    doc_count = 0
    mention_count = 0
    pair_count = 0
    decisive_count = 0
    audit_pool: list[dict[str, Any]] = []

    with mention_path.open("w", encoding="utf-8") as fm, pair_path.open("w", encoding="utf-8") as fp:
        for doc in docs:
            doc_count += 1
            mentions = flatten_mentions(doc)
            mention_count += len(mentions)
            split = str(doc.get("_source_split", "official_jsonl"))
            split_counts[split] += 1
            for m in mentions:
                fm.write(json.dumps(m, ensure_ascii=False) + "\n")

            local_pairs = list(enumerate_pairs(mentions))
            if local_pairs:
                docs_with_mixed += 1
            for pair in local_pairs:
                pair["stable_key"] = stable_key(pair)
                fp.write(json.dumps(pair, ensure_ascii=False) + "\n")
                pair_count += 1
                pair_counts[pair["pair_class"]] += 1
                d = pair["sentence_distance"]
                distance_counts["0" if d == 0 else "1" if d == 1 else "2-3" if d <= 3 else "4+"] += 1
                if pair["decisive_ct_plus_vs_nonfact"]:
                    decisive_count += 1
                    audit_pool.append(pair)

    # Deterministic audit sample. No effect-driven selection is allowed here.
    audit_pool.sort(key=lambda r: r["stable_key"])
    # Spread the sample across pair classes, then fill by stable hash.
    by_class: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in audit_pool:
        by_class[row["pair_class"]].append(row)
    selected: list[dict[str, Any]] = []
    classes = sorted(by_class)
    per_class = max(1, args.audit_n // max(1, len(classes)))
    seen_keys: set[str] = set()
    for cls in classes:
        for row in by_class[cls][:per_class]:
            if row["stable_key"] not in seen_keys:
                selected.append(row)
                seen_keys.add(row["stable_key"])
    for row in audit_pool:
        if len(selected) >= args.audit_n:
            break
        if row["stable_key"] not in seen_keys:
            selected.append(row)
            seen_keys.add(row["stable_key"])

    write_jsonl(out / "audit_sample.jsonl", selected)

    summary = {
        "source": "MAVEN-FACT",
        "source_definition": "source-authored event factuality annotations; no synthetic scenarios",
        "documents": doc_count,
        "documents_with_mixed_status_pairs": docs_with_mixed,
        "mentions": mention_count,
        "ordered_mixed_status_pairs": pair_count,
        "decisive_ct_plus_vs_nonfact_pairs": decisive_count,
        "pair_class_counts": dict(sorted(pair_counts.items())),
        "sentence_distance_counts": dict(distance_counts),
        "split_counts": dict(split_counts),
        "audit_sample_n": len(selected),
        "scope_note": (
            "All source-valid mixed-status ordered pairs are preserved. Sentence distance, "
            "event type, factuality direction, and split are factors, not construction filters."
        ),
        "d0_status": "SOURCE-BANK-MATERIALIZED; HUMAN SOURCE AUDIT STILL REQUIRED",
    }
    (out / "scope_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md = [
        "# MAVEN-FACT D0 source audit sample",
        "",
        "This file is generated deterministically before any model call.",
        "",
    ]
    for idx, row in enumerate(selected, 1):
        md.extend(
            [
                f"## {idx}. {row['title']} — {row['pair_class']}",
                f"- doc_id: `{row['doc_id']}`",
                f"- left: **{row['left_trigger']}** ({row['left_factuality']}, sent {row['left_sent_id']}) — {row['left_sentence']}",
                f"- right: **{row['right_trigger']}** ({row['right_factuality']}, sent {row['right_sent_id']}) — {row['right_sentence']}",
                f"- sentence distance: {row['sentence_distance']}",
                "- audit: [ ] both mentions are valid natural events; [ ] source label matches context; [ ] joint span does not leak an annotation label",
                "",
            ]
        )
    (out / "AUDIT_SAMPLE.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
