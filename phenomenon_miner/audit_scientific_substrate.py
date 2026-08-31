#!/usr/bin/env python3
"""Reproduce row-level S0 audits for natural factorization candidates.

This script never calls a model.  It records dataset versions, hashes, label
cross-cells, independent-unit counts, and a deterministic 20-row source audit.
The output is intended to decide whether an idea may proceed to N0/N1, not to
turn a dataset's existing task into a new research claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def audit_maven_fact(root: Path, seed: int) -> dict[str, Any]:
    files = [root / "data" / "train.jsonl", root / "data" / "valid.jsonl"]
    docs = [(split.stem, doc) for split in files for doc in read_jsonl(split)]
    label_counts: Counter[str] = Counter()
    chain_counts: Counter[str] = Counter()
    mentions: list[dict[str, Any]] = []
    mixed_chains: list[dict[str, Any]] = []

    for split, doc in docs:
        for event in doc["events"]:
            factualities = [mention["factuality"] for mention in event["mention"]]
            chain_counts[split] += 1
            if len(set(factualities)) > 1:
                mixed_chains.append(
                    {
                        "split": split,
                        "document_id": doc["id"],
                        "event_id": event["id"],
                        "event_type": event["type"],
                        "mentions": [
                            {
                                "trigger": mention["trigger_word"],
                                "sentence": doc["sentences"][mention["sent_id"]],
                                "factuality": mention["factuality"],
                            }
                            for mention in event["mention"]
                        ],
                    }
                )
            for mention in event["mention"]:
                label_counts[mention["factuality"]] += 1
                mentions.append(
                    {
                        "split": split,
                        "document_id": doc["id"],
                        "event_id": event["id"],
                        "event_type": event["type"],
                        "trigger": mention["trigger_word"],
                        "sentence": doc["sentences"][mention["sent_id"]],
                        "factuality": mention["factuality"],
                    }
                )

    rng = random.Random(seed)
    audit_rows = rng.sample(mentions, min(20, len(mentions)))
    mixed_audit = rng.sample(mixed_chains, min(20, len(mixed_chains)))
    return {
        "dataset": "MAVEN-FACT",
        "artifact_root": str(root.resolve()),
        "files": {str(path.relative_to(root)): sha256(path) for path in files},
        "document_counts": dict(Counter(split for split, _ in docs)),
        "event_chain_counts": dict(chain_counts),
        "mention_count": len(mentions),
        "factuality_counts": dict(sorted(label_counts.items())),
        "mixed_factuality_chain_count": len(mixed_chains),
        "random_seed": seed,
        "random_20_mentions": audit_rows,
        "random_up_to_20_mixed_chains": mixed_audit,
    }


def parse_modafact_file(path: Path, split: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sentence_tokens: list[str] = []
    sentence_events: list[dict[str, str]] = []
    sentence_id = 0

    def flush() -> None:
        nonlocal sentence_id
        if not sentence_tokens:
            return
        sentence = " ".join(sentence_tokens)
        for event in sentence_events:
            rows.append(
                {
                    "split": split,
                    "sentence_id": sentence_id,
                    "sentence": sentence,
                    **event,
                }
            )
        sentence_tokens.clear()
        sentence_events.clear()
        sentence_id += 1

    with path.open(encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            if not line:
                flush()
                continue
            token, factuality_bio, modality_bio = line.split("\t")
            sentence_tokens.append(token)
            if factuality_bio.startswith("B-"):
                modality = modality_bio[2:] if modality_bio.startswith("B-") else "NONE"
                sentence_events.append(
                    {
                        "trigger": token,
                        "factuality": factuality_bio[2:],
                        "modality": modality,
                    }
                )
        flush()
    return rows


def audit_modafact(root: Path, seed: int) -> dict[str, Any]:
    fold = root / "cg" / "multitask_seq_bio" / "fold_21"
    files = {
        "train": fold / "training_set.tsv",
        "dev": fold / "dev_set.tsv",
        "test": fold / "test_set.tsv",
    }
    rows = [row for split, path in files.items() for row in parse_modafact_file(path, split)]
    factuality = Counter(row["factuality"] for row in rows)
    modality = Counter(row["modality"] for row in rows)
    cross = Counter(f'{row["factuality"]} x {row["modality"]}' for row in rows)
    binary_cross = Counter(
        f'{row["factuality"]} x {"MODAL" if row["modality"] != "NONE" else "NONE"}'
        for row in rows
    )
    rng = random.Random(seed)
    return {
        "dataset": "ModaFact-ITA",
        "artifact_root": str(root.resolve()),
        "fold": 21,
        "representation": "coarse factuality + multitask modality BIO",
        "readme_sha256": sha256(root / "README.md"),
        "files": {split: {"path": str(path), "sha256": sha256(path)} for split, path in files.items()},
        "event_head_count": len(rows),
        "sentence_counts": {
            split: len({row["sentence_id"] for row in rows if row["split"] == split})
            for split in files
        },
        "factuality_counts": dict(factuality.most_common()),
        "modality_counts": dict(modality.most_common()),
        "factuality_by_modality_presence": dict(sorted(binary_cross.items())),
        "factuality_by_modality": dict(sorted(cross.items())),
        "random_seed": seed,
        "random_20_event_heads": rng.sample(rows, min(20, len(rows))),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", choices=("maven-fact", "modafact"))
    parser.add_argument("root", type=Path)
    parser.add_argument("--seed", type=int, default=20260831)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = (
        audit_maven_fact(args.root, args.seed)
        if args.dataset == "maven-fact"
        else audit_modafact(args.root, args.seed)
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
