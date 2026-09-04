"""Align released AmbiCoref human judgments to exact generated minimal pairs."""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd


def answer_class(value: object) -> str:
    text = str(value)
    if "Name1" in text:
        return "candidate_0"
    if "Name2" in text:
        return "candidate_1"
    if "Ambiguous" in text:
        return "unresolved"
    return "invalid"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source-root", type=Path, required=True)
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    source = args.source_root / "ambicoref"
    config = json.loads(args.config.read_text())

    lookup: dict[str, list[dict]] = defaultdict(list)
    sentence_dir = source / "Data" / "Sentences"
    for path in sorted(sentence_dir.glob("*.txt")):
        family, condition = path.stem.rsplit("_", 1)
        lines = [x.strip() for x in path.read_text().splitlines() if x.strip()]
        counterpart_path = sentence_dir / f"{family}_{'ambiguous' if condition == 'unambiguous' else 'unambiguous'}.txt"
        counterparts = [x.strip() for x in counterpart_path.read_text().splitlines() if x.strip()]
        if len(lines) != len(counterparts):
            raise ValueError(f"Pair length mismatch for {family}")
        for index, (sentence, counterpart) in enumerate(zip(lines, counterparts)):
            lookup[sentence].append({
                "family": family,
                "condition": condition,
                "pair_index": index,
                "counterpart_sentence": counterpart,
            })

    judgments = pd.read_csv(source / "Data" / "Human_judgements" / "human_judgements_data.csv")
    grouped: dict[tuple, Counter] = defaultdict(Counter)
    total_responses = 0
    unmapped_responses = 0
    ambiguous_lookup_responses = 0
    for _, row in judgments.iterrows():
        for q in range(10):
            total_responses += 1
            sentence = str(row[f"Input.sentence{q}"]).strip()
            matches = lookup.get(sentence, [])
            if len(matches) != 1:
                unmapped_responses += 1
                if len(matches) > 1:
                    ambiguous_lookup_responses += 1
                continue
            candidate_0 = str(row[f"Input.Q{q}-Name1"]).strip()
            candidate_1 = str(row[f"Input.Q{q}-Name2"]).strip()
            question = str(row[f"Input.question{q}"]).strip()
            meta = matches[0]
            key = (
                sentence,
                question,
                candidate_0,
                candidate_1,
                meta["family"],
                meta["condition"],
                meta["pair_index"],
                meta["counterpart_sentence"],
            )
            grouped[key][answer_class(row[f"Answer.Q{q}"])] += 1

    family_to_split = {
        family: split
        for split, families in config["family_split"].items()
        for family in families
    }
    records = []
    resolved_eligible = 0
    for item_index, (key, votes) in enumerate(sorted(grouped.items())):
        sentence, question, candidate_0, candidate_1, family, condition, pair_index, counterpart = key
        candidate_votes = [votes["candidate_0"], votes["candidate_1"]]
        winner = max(range(2), key=candidate_votes.__getitem__)
        valid_votes = sum(votes.values()) - votes["invalid"]
        agreement = candidate_votes[winner] / valid_votes if valid_votes else 0.0
        is_resolved_calibration = (
            condition == "unambiguous"
            and candidate_votes[winner] >= int(config["resolved_min_votes"])
            and agreement >= float(config["resolved_min_agreement"])
            and candidate_votes[0] != candidate_votes[1]
        )
        resolved_eligible += int(is_resolved_calibration)
        records.append({
            "item_id": f"ambicoref_human_{item_index:04d}",
            "family": family,
            "split": family_to_split[family],
            "condition": condition,
            "pair_index": pair_index,
            "sentence": sentence,
            "paired_sentence": counterpart,
            "question": question,
            "candidates": [candidate_0, candidate_1],
            "vote_counts": dict(votes),
            "human_preferred_candidate": winner,
            "human_agreement": agreement,
            "resolved_calibration_eligible": is_resolved_calibration,
        })

    commit = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        for record in records:
            f.write(json.dumps({**record, "source_commit": commit}, ensure_ascii=False) + "\n")
    summary = {
        "records": len(records),
        "resolved_calibration_eligible": resolved_eligible,
        "total_human_responses": total_responses,
        "unmapped_responses": unmapped_responses,
        "ambiguous_lookup_responses": ambiguous_lookup_responses,
        "by_family_condition": {
            f"{family}/{condition}": count
            for (family, condition), count in Counter(
                (r["family"], r["condition"]) for r in records
            ).items()
        },
        "source_commit": commit,
        "output": str(args.output),
    }
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
