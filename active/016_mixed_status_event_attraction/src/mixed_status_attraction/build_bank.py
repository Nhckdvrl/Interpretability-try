from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .io import file_sha256, stable_hash, write_json, write_jsonl

LABELS = ("CT+", "PS+", "PS-", "CT-", "Uu")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--audit-n", type=int, default=40)
    return parser.parse_args()


def load_docs(contract: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    from datasets import load_dataset

    docs, fingerprints = [], {}
    for split in contract["source"]["splits"]:
        dataset = load_dataset(contract["source"]["dataset"], split=split)
        fingerprints[split] = str(dataset._fingerprint)
        for row in dataset:
            item = dict(row)
            item["_source_split"] = split
            docs.append(item)
    return docs, fingerprints


def relation_index(doc: dict[str, Any]) -> dict[frozenset[str], list[str]]:
    index: dict[frozenset[str], list[str]] = defaultdict(list)
    for name, pairs in (doc.get("temporal_relations") or {}).items():
        for left, right in pairs or []:
            if left.startswith("EVENT_") and right.startswith("EVENT_"):
                index[frozenset((left, right))].append(f"temporal:{name}")
    for name, pairs in (doc.get("causal_relation") or {}).items():
        for left, right in pairs or []:
            index[frozenset((left, right))].append(f"causal:{name}")
    for left, right in doc.get("subevent_relations") or []:
        index[frozenset((left, right))].append("subevent")
    return index


def flatten_mentions(doc: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for event in doc.get("events") or []:
        for mention in event.get("mention") or []:
            if mention.get("factuality") not in LABELS:
                continue
            evidence_offsets = mention.get("evidence_offset") or []
            rows.append(
                {
                    "doc_id": str(doc["id"]),
                    "title": str(doc.get("title", "")),
                    "source_split": doc["_source_split"],
                    "event_id": str(event["id"]),
                    "event_type": str(event.get("type", "")),
                    "mention_id": str(mention["id"]),
                    "trigger": str(mention.get("trigger_word", "")),
                    "sent_id": int(mention["sent_id"]),
                    "offset": [int(x) for x in mention.get("offset") or []],
                    "factuality": str(mention["factuality"]),
                    "evidence_words": mention.get("evidence_word") or [],
                    "evidence_offsets": evidence_offsets,
                    "evidence_sent_ids": sorted({int(x[0]) for x in evidence_offsets if x}),
                }
            )
    return rows


def compact_pair(left: dict[str, Any], right: dict[str, Any], relations: list[str]) -> dict[str, Any]:
    pair_id = f"{left['doc_id']}:{left['mention_id']}->{right['mention_id']}"
    return {
        "pair_id": pair_id,
        "doc_id": left["doc_id"],
        "source_split": left["source_split"],
        "target_mention_id": left["mention_id"],
        "target_event_id": left["event_id"],
        "target_event_type": left["event_type"],
        "target_sent_id": left["sent_id"],
        "target_label": left["factuality"],
        "neighbor_mention_id": right["mention_id"],
        "neighbor_event_id": right["event_id"],
        "neighbor_event_type": right["event_type"],
        "neighbor_sent_id": right["sent_id"],
        "neighbor_label": right["factuality"],
        "direction": f"{left['factuality']}->{right['factuality']}",
        "sentence_distance": abs(left["sent_id"] - right["sent_id"]),
        "same_sentence": left["sent_id"] == right["sent_id"],
        "explicit_relations": sorted(relations),
        "has_explicit_relation": bool(relations),
        "stable_hash": stable_hash(pair_id),
    }


def render_sentences(
    doc: dict[str, Any], sent_ids: list[int], markers: dict[int, list[tuple[int, int, str]]], reverse: bool = False
) -> str:
    order = sorted(set(sent_ids), reverse=reverse)
    blocks = []
    tokens_by_sentence = doc.get("tokens") or []
    for sent_id in order:
        tokens = list(tokens_by_sentence[sent_id])
        opens: dict[int, list[str]] = defaultdict(list)
        closes: dict[int, list[str]] = defaultdict(list)
        for start, end, name in markers.get(sent_id, []):
            opens[start].append(f"<{name}>")
            closes[end].append(f"</{name}>")
        output = []
        for index, token in enumerate(tokens):
            output.extend(opens.get(index, []))
            output.append(str(token))
            output.extend(reversed(closes.get(index + 1, [])))
        blocks.append(f"Sentence {sent_id}: " + " ".join(output))
    return "\n".join(blocks)


def materialize_pair(
    doc: dict[str, Any], pair: dict[str, Any], mentions: dict[str, dict[str, Any]], same: dict[str, Any]
) -> dict[str, Any]:
    target = mentions[pair["target_mention_id"]]
    neighbor = mentions[pair["neighbor_mention_id"]]
    target_markers = defaultdict(list)
    mixed_markers = defaultdict(list)
    same_markers = defaultdict(list)
    for mention, name in ((target, "TARGET_EVENT"),):
        start, end = mention["offset"]
        target_markers[mention["sent_id"]].append((start, end, name))
        mixed_markers[mention["sent_id"]].append((start, end, name))
        same_markers[mention["sent_id"]].append((start, end, name))
    for mention, name, marker_set in (
        (neighbor, "OTHER_EVENT", mixed_markers),
        (same, "SAME_STATUS_EVENT", same_markers),
    ):
        start, end = mention["offset"]
        marker_set[mention["sent_id"]].append((start, end, name))
    target_ids = sorted({target["sent_id"], *target["evidence_sent_ids"]})
    neighbor_ids = sorted({neighbor["sent_id"], *neighbor["evidence_sent_ids"]})
    same_ids = sorted({same["sent_id"], *same["evidence_sent_ids"]})
    mixed_ids = sorted(set(target_ids + neighbor_ids))
    control_ids = sorted(set(target_ids + same_ids))
    full_ids = list(range(min(mixed_ids), max(mixed_ids) + 1))
    return {
        **pair,
        "title": str(doc.get("title", "")),
        "target_trigger": target["trigger"],
        "neighbor_trigger": neighbor["trigger"],
        "same_status_mention_id": same["mention_id"],
        "same_status_event_id": same["event_id"],
        "same_status_trigger": same["trigger"],
        "same_status_sent_id": same["sent_id"],
        "same_status_distance": abs(target["sent_id"] - same["sent_id"]),
        "same_status_distinct_sentence": target["sent_id"] != same["sent_id"],
        "target_local": render_sentences(doc, target_ids, target_markers),
        "same_status_natural": render_sentences(doc, control_ids, same_markers),
        "same_status_reversed": render_sentences(doc, control_ids, same_markers, reverse=True),
        "mixed_status_natural": render_sentences(doc, mixed_ids, mixed_markers),
        "mixed_status_reversed": render_sentences(doc, mixed_ids, mixed_markers, reverse=True),
        "full_local_discourse": render_sentences(doc, full_ids, mixed_markers),
        "full_window_sentence_count": len(full_ids),
    }


def main() -> None:
    args = parse_args()
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    docs, fingerprints = load_docs(contract)
    write_jsonl(out / "source_snapshot.jsonl", docs)

    raw_mentions, all_pairs, matched = [], [], []
    relation_counts, direction_counts = Counter(), Counter()
    for doc in docs:
        mentions = flatten_mentions(doc)
        raw_mentions.extend(mentions)
        by_id = {row["mention_id"]: row for row in mentions}
        by_label: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in mentions:
            by_label[row["factuality"]].append(row)
        relations = relation_index(doc)
        candidates_by_target_direction: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for left in mentions:
            for right in mentions:
                if left["mention_id"] == right["mention_id"] or left["event_id"] == right["event_id"]:
                    continue
                if left["factuality"] == right["factuality"]:
                    continue
                relation_types = relations.get(frozenset((left["event_id"], right["event_id"])), [])
                pair = compact_pair(left, right, relation_types)
                all_pairs.append(pair)
                direction_counts[pair["direction"]] += 1
                for relation in relation_types:
                    relation_counts[relation] += 1
                candidates_by_target_direction[(left["mention_id"], right["factuality"])].append(pair)

        for candidate_pairs in candidates_by_target_direction.values():
            pair = min(candidate_pairs, key=lambda row: row["stable_hash"])
            target = by_id[pair["target_mention_id"]]
            same_candidates = [
                row for row in by_label[target["factuality"]]
                if row["event_id"] != target["event_id"] and row["mention_id"] != target["mention_id"]
            ]
            if not same_candidates:
                continue
            distance = pair["sentence_distance"]
            # Prefer a truly added sentence, then match distance, then stable hash.
            same = min(
                same_candidates,
                key=lambda row: (
                    row["sent_id"] == target["sent_id"],
                    abs(abs(row["sent_id"] - target["sent_id"]) - distance),
                    stable_hash(row["mention_id"]),
                ),
            )
            matched.append(materialize_pair(doc, pair, by_id, same))

    write_jsonl(out / "raw_mentions.jsonl", raw_mentions)
    write_jsonl(out / "all_mixed_ordered_pairs.jsonl", all_pairs)
    write_jsonl(out / "matched_pairs.jsonl", matched)

    by_direction: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in matched:
        by_direction[row["direction"]].append(row)
    smoke = []
    primary = set(contract["primary_labels"])
    for direction, rows in sorted(by_direction.items()):
        left, right = direction.split("->")
        quota = (
            int(contract["smoke"]["per_primary_direction"])
            if left in primary and right in primary
            else int(contract["smoke"]["per_unknown_direction"])
        )
        ranked = sorted(rows, key=lambda row: stable_hash([contract["smoke"]["seed"], row["pair_id"]]))
        # Prefer document diversity without deleting the remaining matched bank.
        selected, seen_docs = [], set()
        for row in ranked:
            if row["doc_id"] not in seen_docs:
                selected.append(row)
                seen_docs.add(row["doc_id"])
            if len(selected) == quota:
                break
        if len(selected) < quota:
            used = {row["pair_id"] for row in selected}
            selected.extend(row for row in ranked if row["pair_id"] not in used)
        smoke.extend(selected[:quota])
    smoke.sort(key=lambda row: stable_hash(["smoke", row["pair_id"]]))
    write_jsonl(out / "d0_smoke_pairs.jsonl", smoke)

    audit = sorted(matched, key=lambda row: stable_hash(["audit", row["pair_id"]]))[: args.audit_n]
    write_jsonl(out / "source_audit_sample.jsonl", audit)
    summary = {
        "contract_version": contract["contract_version"],
        "source": contract["source"],
        "source_fingerprints": fingerprints,
        "stages": [
            {"stage": "source_documents", "n_rows": len(docs), "n_documents": len(docs)},
            {"stage": "raw_mentions", "n_rows": len(raw_mentions), "n_documents": len({r['doc_id'] for r in raw_mentions})},
            {"stage": "all_mixed_ordered_pairs", "n_rows": len(all_pairs), "n_documents": len({r['doc_id'] for r in all_pairs})},
            {"stage": "one_neighbor_per_target_direction_with_same_control", "n_rows": len(matched), "n_documents": len({r['doc_id'] for r in matched})},
            {"stage": "direction_stratified_d0_smoke", "n_rows": len(smoke), "n_documents": len({r['doc_id'] for r in smoke})}
        ],
        "mention_label_counts": dict(Counter(row["factuality"] for row in raw_mentions)),
        "all_pair_direction_counts": dict(sorted(direction_counts.items())),
        "matched_direction_counts": dict(sorted(Counter(row["direction"] for row in matched).items())),
        "smoke_direction_counts": dict(sorted(Counter(row["direction"] for row in smoke).items())),
        "explicit_relation_counts": dict(sorted(relation_counts.items())),
        "smoke_explicit_relation": dict(Counter(str(row["has_explicit_relation"]) for row in smoke)),
        "smoke_same_sentence": dict(Counter(str(row["same_sentence"]) for row in smoke)),
        "file_sha256": {},
        "scope_note": "All mentions and ordered mixed-status pairs are preserved. Direction balancing is only a cost-sampling layer. Distance, event type, relation, and same-sentence status remain factors."
    }
    for name in ("source_snapshot", "raw_mentions", "all_mixed_ordered_pairs", "matched_pairs", "d0_smoke_pairs"):
        summary["file_sha256"][name] = file_sha256(out / f"{name}.jsonl")
    write_json(out / "scope_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
