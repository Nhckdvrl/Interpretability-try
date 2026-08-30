from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from .io import file_sha256, stable_hash, write_json, write_jsonl


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize the CondAmbigQA D0 bank.")
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--audit-n", type=int, default=40)
    parser.add_argument("--max-smoke-pairs", type=int)
    return parser.parse_args()


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def comparison_text(text: str) -> str:
    return re.sub(r"[^\w]+", " ", text.casefold()).strip()


def load_source(contract: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise SystemExit("Install the data extra (datasets) to build the bank.") from exc

    source = contract["source"]
    dataset = load_dataset(
        source["dataset"], source.get("config", "default"), split=source["split"]
    )
    rows = [dict(row) for row in dataset]
    return rows, str(getattr(dataset, "_fingerprint", "unknown"))


def flatten_source(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    questions: list[dict[str, Any]] = []
    properties: list[dict[str, Any]] = []
    for row_index, row in enumerate(rows):
        question_id = str(row["id"])
        source_properties = list(row.get("properties") or [])
        questions.append(
            {
                "question_id": question_id,
                "source_row_index": row_index,
                "question": normalize_text(str(row["question"])),
                "property_count": len(source_properties),
                "ctx_count": len(row.get("ctxs") or []),
            }
        )
        for property_index, prop in enumerate(source_properties):
            condition = normalize_text(str(prop.get("condition", "")))
            answer = normalize_text(str(prop.get("groundtruth", "")))
            properties.append(
                {
                    "property_id": f"{question_id}:p{property_index}",
                    "question_id": question_id,
                    "source_row_index": row_index,
                    "property_index": property_index,
                    "property_count": len(source_properties),
                    "question": normalize_text(str(row["question"])),
                    "condition": condition,
                    "answer": answer,
                    "condition_chars": len(condition),
                    "answer_chars": len(answer),
                    "citation_count": len(prop.get("citations") or []),
                    "has_reason": bool(prop.get("reason")),
                }
            )
    return questions, properties


def enumerate_pairs(properties: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_question: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for prop in properties:
        by_question[prop["question_id"]].append(prop)

    pairs: list[dict[str, Any]] = []
    for question_id, local in by_question.items():
        for target in local:
            for distractor in local:
                if target["property_index"] == distractor["property_index"]:
                    continue
                target_cmp = comparison_text(target["answer"])
                distractor_cmp = comparison_text(distractor["answer"])
                reasons: list[str] = []
                if not target["condition"] or not target["answer"]:
                    reasons.append("empty_target_field")
                if not distractor["condition"] or not distractor["answer"]:
                    reasons.append("empty_distractor_field")
                if target_cmp == distractor_cmp:
                    reasons.append("identical_answers")
                elif target_cmp in distractor_cmp or distractor_cmp in target_cmp:
                    reasons.append("answer_string_containment")
                pair_id = (
                    f"{question_id}:t{target['property_index']}:d{distractor['property_index']}"
                )
                pairs.append(
                    {
                        "pair_id": pair_id,
                        "question_id": question_id,
                        "question": target["question"],
                        "property_count": target["property_count"],
                        "target_property_index": target["property_index"],
                        "distractor_property_index": distractor["property_index"],
                        "target_condition": target["condition"],
                        "target_answer": target["answer"],
                        "distractor_condition": distractor["condition"],
                        "distractor_answer": distractor["answer"],
                        "target_condition_chars": target["condition_chars"],
                        "distractor_condition_chars": distractor["condition_chars"],
                        "target_answer_chars": target["answer_chars"],
                        "distractor_answer_chars": distractor["answer_chars"],
                        "validity_eligible": not reasons,
                        "validity_exclusion_reasons": reasons,
                        "stable_hash": stable_hash(pair_id),
                    }
                )
    return pairs


def choose_matched_pairs(pairs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Choose one distractor per target without deleting the full ordered-pair bank."""
    eligible = [pair for pair in pairs if pair["validity_eligible"]]
    by_target: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for pair in eligible:
        by_target[(pair["question_id"], pair["target_property_index"])].append(pair)
    selected: list[dict[str, Any]] = []
    for candidates in by_target.values():
        selected.append(min(candidates, key=lambda row: row["stable_hash"]))
    return sorted(selected, key=lambda row: row["stable_hash"])


def stratified_smoke_sample(
    matched: list[dict[str, Any]], max_pairs: int, seed: int
) -> list[dict[str, Any]]:
    """Cost sample with broad property-count coverage and no content/effect filter."""
    if max_pairs <= 0 or len(matched) <= max_pairs:
        return list(matched)
    strata: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in matched:
        key = str(min(int(row["property_count"]), 4))
        salted = stable_hash([seed, row["pair_id"]])
        copied = dict(row)
        copied["smoke_hash"] = salted
        strata[key].append(copied)
    total = len(matched)
    quotas = {key: max(1, round(max_pairs * len(group) / total)) for key, group in strata.items()}
    while sum(quotas.values()) > max_pairs:
        key = max(quotas, key=lambda k: (quotas[k], len(strata[k])))
        if quotas[key] > 1:
            quotas[key] -= 1
        else:
            break
    while sum(quotas.values()) < max_pairs:
        candidates = [k for k in strata if quotas[k] < len(strata[k])]
        if not candidates:
            break
        key = max(candidates, key=lambda k: len(strata[k]) - quotas[k])
        quotas[key] += 1
    sample = []
    for key, group in strata.items():
        sample.extend(sorted(group, key=lambda row: row["smoke_hash"])[: quotas[key]])
    return sorted(sample, key=lambda row: row["smoke_hash"])


def count_by(rows: Iterable[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row[key]) for row in rows).items()))


def write_audit_markdown(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Deterministic source audit sample",
        "",
        "This sample checks source mapping only; it does not add or revise gold labels.",
        "",
    ]
    for index, row in enumerate(rows, 1):
        lines.extend(
            [
                f"## {index}. `{row['pair_id']}`",
                "",
                f"**Question:** {row['question']}",
                "",
                f"**Target condition:** {row['target_condition']}",
                "",
                f"**Target answer:** {row['target_answer']}",
                "",
                f"**Alternative condition:** {row['distractor_condition']}",
                "",
                f"**Alternative answer:** {row['distractor_answer']}",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    source_rows, fingerprint = load_source(contract)
    questions, properties = flatten_source(source_rows)
    pairs = enumerate_pairs(properties)
    validity_pairs = [row for row in pairs if row["validity_eligible"]]
    matched = choose_matched_pairs(pairs)
    max_pairs = args.max_smoke_pairs or int(contract["smoke"]["max_pairs"])
    smoke = stratified_smoke_sample(matched, max_pairs, int(contract["smoke"]["seed"]))

    paths = {
        "source_snapshot": output_dir / "source_snapshot.jsonl",
        "raw_questions": output_dir / "raw_questions.jsonl",
        "raw_properties": output_dir / "raw_properties.jsonl",
        "all_ordered_pairs": output_dir / "all_ordered_pairs.jsonl",
        "validity_eligible_pairs": output_dir / "validity_eligible_pairs.jsonl",
        "matched_pairs": output_dir / "matched_pairs.jsonl",
        "d0_smoke_pairs": output_dir / "d0_smoke_pairs.jsonl",
    }
    write_jsonl(paths["source_snapshot"], source_rows)
    write_jsonl(paths["raw_questions"], questions)
    write_jsonl(paths["raw_properties"], properties)
    write_jsonl(paths["all_ordered_pairs"], pairs)
    write_jsonl(paths["validity_eligible_pairs"], validity_pairs)
    write_jsonl(paths["matched_pairs"], matched)
    write_jsonl(paths["d0_smoke_pairs"], smoke)

    audit = sorted(validity_pairs, key=lambda row: stable_hash(["audit", row["pair_id"]]))[
        : args.audit_n
    ]
    write_jsonl(output_dir / "source_audit_sample.jsonl", audit)
    write_audit_markdown(output_dir / "SOURCE_AUDIT_SAMPLE.md", audit)

    matched_ids = {row["pair_id"] for row in matched}
    nonselected = [row for row in validity_pairs if row["pair_id"] not in matched_ids]
    attrition_audit = []
    for status, pool in (("matched_survivor", matched), ("alternate_distractor_not_selected", nonselected)):
        local = sorted(pool, key=lambda row: stable_hash(["attrition", status, row["pair_id"]]))[:20]
        attrition_audit.extend({**row, "attrition_audit_status": status} for row in local)
    write_jsonl(output_dir / "attrition_audit_sample.jsonl", attrition_audit)

    exclusions = Counter(
        reason for row in pairs for reason in row["validity_exclusion_reasons"]
    )
    property_counts = count_by(questions, "property_count")
    summary = {
        "contract_version": contract["contract_version"],
        "source": contract["source"],
        "source_fingerprint": fingerprint,
        "stages": [
            {"stage": "source_questions", "n_rows": len(source_rows), "n_questions": len(source_rows)},
            {"stage": "raw_properties", "n_rows": len(properties), "n_questions": len(questions)},
            {
                "stage": "all_ordered_pairs",
                "n_rows": len(pairs),
                "n_questions": len({row["question_id"] for row in pairs}),
            },
            {
                "stage": "validity_eligible_pairs",
                "n_rows": len(validity_pairs),
                "n_questions": len({row["question_id"] for row in validity_pairs}),
            },
            {
                "stage": "one_distractor_per_target_matched",
                "n_rows": len(matched),
                "n_questions": len({row["question_id"] for row in matched}),
            },
            {
                "stage": "cost_limited_d0_smoke",
                "n_rows": len(smoke),
                "n_questions": len({row["question_id"] for row in smoke}),
            },
        ],
        "question_property_count_distribution": property_counts,
        "pair_property_count_distribution": count_by(pairs, "property_count"),
        "validity_exclusion_counts": dict(sorted(exclusions.items())),
        "single_property_questions_retained_in_raw": property_counts.get("1", 0),
        "source_audit_sample_n": len(audit),
        "attrition_audit_sample_n": len(attrition_audit),
        "scope_note": (
            "All source questions, properties, and ordered directions are preserved. "
            "One distractor per target is a matched measurement layer; the smoke cap is a "
            "hash-based cost sample, not a scientific-population filter."
        ),
        "file_sha256": {name: file_sha256(path) for name, path in paths.items()},
    }
    write_json(output_dir / "scope_summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
