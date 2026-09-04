"""Build all label-counterbalanced deterministic presupposition items."""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source-root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    source = args.source_root / "presupposition"
    items = json.loads((source / "problem_set.json").read_text())
    commit = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    semantics = ["low", "mid", "high"]
    records = []
    for item in items:
        for order_index, order in enumerate(itertools.permutations(semantics)):
            labels = dict(zip(order, ["A", "B", "C"]))
            records.append({
                **item,
                "item_id": f"presup_{item['id']:03d}_order{order_index}",
                "label_order": list(order),
                "semantic_to_label": labels,
                "question": (
                    "Given an honest, reliable speaker, how likely is the target statement?\n"
                    f"Speaker's statement: {item['statement_1']}\n"
                    f"Target statement: {item['statement_2']}\n"
                    f"{labels['low']}: low likelihood\n{labels['mid']}: mid likelihood\n"
                    f"{labels['high']}: high likelihood"
                ),
                "source_commit": commit,
            })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps({"records": len(records), "source_items": len(items), "source_commit": commit}))


if __name__ == "__main__":
    main()
