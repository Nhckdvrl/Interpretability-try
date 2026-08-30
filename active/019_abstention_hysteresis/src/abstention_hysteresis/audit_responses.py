"""Create a deterministic human-auditable response classification sample."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .io import read_jsonl, write_jsonl


def prefix(response: str) -> str:
    text = response.lstrip().casefold()
    if text.startswith("answer"):
        return "answer"
    if text.startswith("abstain"):
        return "abstain"
    return "other"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--output", required=True)
    parser.add_argument("--per-prefix", type=int, default=20)
    args = parser.parse_args()
    candidates = []
    for path in args.inputs:
        family = json.loads(Path(path).with_suffix(".metadata.json").read_text())["family"]
        for row in read_jsonl(path):
            if row["condition"] == "capability_full":
                continue
            candidates.append({
                "family": family,
                "item_id": row["item_id"],
                "source": row["source"],
                "condition": row["condition"],
                "response": row["response"],
                "protocol_prefix": prefix(row["response"]),
                "classified_abstention": row["is_abstention"],
                "correct": row["correct"],
            })
    selected = []
    for family in sorted({row["family"] for row in candidates}):
        for label in ("answer", "abstain", "other"):
            local = sorted(
                (row for row in candidates
                 if row["family"] == family and row["protocol_prefix"] == label),
                key=lambda row: (row["condition"], row["item_id"]),
            )
            selected.extend(local[:args.per_prefix])
    write_jsonl(args.output, selected)
    print(json.dumps({"output": args.output, "rows": len(selected)}, indent=2))


if __name__ == "__main__":
    main()
