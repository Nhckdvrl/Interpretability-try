from __future__ import annotations

import argparse
import json
from collections import Counter

from .bfcl import index_by_id, load_jsonl, write_jsonl
from .classify import binding_eligible_pairs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--answers", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    tests = load_jsonl(args.data)
    answers = index_by_id(load_jsonl(args.answers))
    rows = []
    type_counts: Counter[str] = Counter()
    for test in tests:
        ans = answers.get(test["id"])
        if ans is None:
            continue
        pairs = binding_eligible_pairs(test, ans)
        if not pairs:
            continue
        for p in pairs:
            type_counts[str(p["type"])] += 1
        rows.append({"id": test["id"], "pairs": pairs})
    write_jsonl(rows, args.out)
    print(json.dumps({"eligible_examples": len(rows), "eligible_pairs": sum(len(r["pairs"]) for r in rows), "pair_types": type_counts}, indent=2, default=dict))


if __name__ == "__main__":
    main()
