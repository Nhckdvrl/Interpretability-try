"""Build frozen ItDepends ClearRef/SharedRef candidate panels."""

from __future__ import annotations

import argparse
import glob
import json
import re
import subprocess
from pathlib import Path


ORDER_RE = re.compile(r"-(\d{2,3})\.jsonl$")


def semantic_id(entry: dict) -> str:
    positives = sorted(x["entity"] for x in entry["positive"])
    return "|".join([entry["question"], *positives, entry["negative"]["entity"]])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source-root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    repo = args.source_root / "itdepends"
    commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    records = []
    expected = {"clear_ref": set(["01", "10"]), "shared_ref": set(["012", "021", "102", "120", "201", "210"])}
    seen_orders = {k: set() for k in expected}
    for split in ["clear_ref", "shared_ref"]:
        pattern = str(repo / "data" / "judged_outputs" / split / "en" / "llama-8b" / f"outputs-{split}-en-llama-8b-normal-*.jsonl")
        for name in sorted(glob.glob(pattern)):
            match = ORDER_RE.search(name)
            if not match:
                continue
            order = match.group(1)
            seen_orders[split].add(order)
            with open(name) as f:
                for row_index, line in enumerate(f):
                    released = json.loads(line)
                    entry = released["entry"]
                    positives = [x["entity"] for x in entry["positive"]]
                    negative = entry["negative"]["entity"]
                    records.append(
                        {
                            "item_id": f"{split}_{order}_{row_index:04d}",
                            "semantic_id": semantic_id(entry),
                            "split": split,
                            "permutation": order,
                            "row_index": row_index,
                            "conversation": released["conversation"],
                            "positive_candidates": positives,
                            "negative_candidate": negative,
                            "candidates": positives + [negative],
                            "source_commit": commit,
                        }
                    )
    if seen_orders != expected:
        raise ValueError(f"Missing frozen permutations: got {seen_orders}, expected {expected}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        for row in records:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"records": len(records), "orders": {k: sorted(v) for k, v in seen_orders.items()}, "source_commit": commit}))


if __name__ == "__main__":
    main()
