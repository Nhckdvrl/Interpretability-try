#!/usr/bin/env python3
"""Build a same-graph, multi-query reachability calibration panel."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


QUERY_TYPES = ("left_reachable", "right_reachable", "cross_unreachable")
POLARITIES = ("positive", "reverse")


def parse_edge(edge: str) -> tuple[str, str]:
    left, separator, right = edge.partition("->")
    if not separator:
        raise ValueError(f"Malformed edge: {edge!r}")
    return left.strip(), right.strip()


def graph_queries(problem: dict[str, Any]) -> list[tuple[str, str, str, bool]]:
    chain = list(problem["linked_list"])
    broken = [parse_edge(edge) for edge in problem["broken_edges"]]
    if len(broken) != 1:
        raise ValueError("Expected one missing edge")
    all_edges = list(zip(chain, chain[1:]))
    break_index = all_edges.index(broken[0])
    if break_index < 1 or break_index + 2 >= len(chain):
        raise ValueError("Both components need a non-trivial reachable query")
    return [
        ("left_reachable", chain[0], chain[break_index], True),
        ("right_reachable", chain[break_index + 1], chain[-1], True),
        ("cross_unreachable", chain[0], chain[-1], False),
    ]


def replace_query(prompt: str, source: str, target: str, polarity: str) -> str:
    _first_line, separator, body = prompt.partition("\n")
    if not separator:
        raise ValueError("Prompt has no body")
    if polarity == "positive":
        query = f"Determine whether {source} can contact {target} using the rules and facts below."
    elif polarity == "reverse":
        query = f"Determine whether {source} cannot contact {target} using the rules and facts below."
    else:
        raise ValueError(f"Unknown polarity: {polarity}")
    return f"{query} Respond with only one word: 'Yes' or 'No'.\n{body}"


def make_rows(problem: dict[str, Any], source_row: int, split: str) -> list[dict[str, Any]]:
    graph_hash = hashlib.sha256(problem["problem"].encode()).hexdigest()
    rows = []
    for query_type, source, target, reachable in graph_queries(problem):
        for polarity in POLARITIES:
            answer_yes = reachable if polarity == "positive" else not reachable
            rows.append(
                {
                    "schema_version": 1,
                    "graph_id": f"l10:b5:i{source_row:04d}:{graph_hash[:12]}",
                    "source_row": source_row,
                    "split": split,
                    "query_type": query_type,
                    "polarity": polarity,
                    "source": source,
                    "target": target,
                    "reachable": reachable,
                    "expected_answer": "Yes" if answer_yes else "No",
                    "prompt": replace_query(problem["problem"], source, target, polarity),
                    "problem_sha256": graph_hash,
                    "missing_edge": problem["broken_edges"][0],
                }
            )
    return rows


def build_panel(
    problems: list[dict[str, Any]], recipient_source_rows: set[int], *,
    n_calibration_graphs: int, train_fraction: float, seed: int,
) -> list[dict[str, Any]]:
    candidates = [i for i in range(len(problems)) if i not in recipient_source_rows]
    rng = random.Random(seed)
    selected = sorted(rng.sample(candidates, n_calibration_graphs))
    shuffled = selected[:]
    rng.shuffle(shuffled)
    n_train = round(len(shuffled) * train_fraction)
    train_ids = set(shuffled[:n_train])
    rows = []
    for source_row in selected:
        rows.extend(make_rows(problems[source_row], source_row, "train" if source_row in train_ids else "test"))
    for source_row in sorted(recipient_source_rows):
        rows.extend(make_rows(problems[source_row], source_row, "recipient"))
    return sorted(rows, key=lambda row: (row["split"], row["graph_id"], row["query_type"], row["polarity"]))


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            line = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
            handle.write(line)
            digest.update(line.encode())
    return digest.hexdigest()


def summarize(rows: list[dict[str, Any]], digest: str, args: argparse.Namespace) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "design": "same graph/facts; three queried pairs; positive/reverse wording",
        "seed": args.seed,
        "n_calibration_graphs": args.n_calibration_graphs,
        "train_fraction": args.train_fraction,
        "n_rows": len(rows),
        "n_graphs_by_split": {
            split: len({row["graph_id"] for row in rows if row["split"] == split})
            for split in ("train", "test", "recipient")
        },
        "rows_by_split_reachability_polarity": {
            "/".join(map(str, key)): value
            for key, value in sorted(Counter(
                (row["split"], row["reachable"], row["polarity"]) for row in rows
            ).items())
        },
        "panel_sha256": digest,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--problems", type=Path, required=True)
    parser.add_argument("--v2-population", type=Path, required=True)
    parser.add_argument("--panel-out", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    parser.add_argument("--n-calibration-graphs", type=int, default=256)
    parser.add_argument("--train-fraction", type=float, default=0.75)
    parser.add_argument("--seed", type=int, default=31033)
    args = parser.parse_args()
    problems = json.loads(args.problems.read_text())
    recipients = {
        json.loads(line)["source_row"]
        for line in args.v2_population.read_text().splitlines()
        if line.strip() and json.loads(line)["role"] == "hard_deceptive"
    }
    rows = build_panel(
        problems, recipients, n_calibration_graphs=args.n_calibration_graphs,
        train_fraction=args.train_fraction, seed=args.seed,
    )
    digest = write_jsonl(args.panel_out, rows)
    summary = summarize(rows, digest, args)
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
