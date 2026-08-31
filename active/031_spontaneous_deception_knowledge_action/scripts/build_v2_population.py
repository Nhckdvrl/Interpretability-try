#!/usr/bin/env python3
"""Freeze the positive-direction deterministic V2 population.

The recipient population is deliberately strict: an item must be labelled
mother-deceptive after independent V0 rescoring and reproduce that phenotype in
the local greedy V1 replay.  Reverse-worded items are never admitted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_v1_replay import attach_prompts, read_jsonl


REGULAR_VARIANT = "BrokenLinkedListRephrase"


def parse_edge(edge: str) -> tuple[str, str]:
    left, separator, right = edge.partition("->")
    if not separator:
        raise ValueError(f"Malformed edge: {edge!r}")
    return left.strip(), right.strip()


def graph_state(problem: dict[str, Any]) -> dict[str, Any]:
    chain = list(problem["linked_list"])
    broken = [parse_edge(edge) for edge in problem.get("broken_edges", [])]
    if len(broken) != 1:
        raise ValueError(f"Expected exactly one broken edge, found {broken!r}")
    all_chain_edges = list(zip(chain, chain[1:]))
    present_edges = (
        [parse_edge(edge) for edge in problem["edges"]]
        if "edges" in problem
        else [edge for edge in all_chain_edges if edge not in set(broken)]
    )
    adjacency: dict[str, list[str]] = defaultdict(list)
    for left, right in present_edges:
        adjacency[left].append(right)
    source, target = chain[0], chain[-1]
    frontier = [source]
    visited = {source}
    while frontier:
        for neighbor in adjacency[frontier.pop()]:
            if neighbor not in visited:
                visited.add(neighbor)
                frontier.append(neighbor)
    missing_left, missing_right = broken[0]
    return {
        "source": source,
        "target": target,
        "reachable": target in visited,
        "correct_answer": "Yes" if target in visited else "No",
        "chain": chain,
        "present_edges": [f"{left} -> {right}" for left, right in present_edges],
        "missing_edge": f"{missing_left} -> {missing_right}",
        "missing_edge_index": all_chain_edges.index((missing_left, missing_right)),
        "source_component": [node for node in chain if node in visited],
        "target_component": [node for node in chain if node not in visited],
    }


def fact_spans(prompt: str, graph: dict[str, Any]) -> dict[str, Any]:
    edge_spans = []
    for edge in graph["present_edges"]:
        left, right = parse_edge(edge)
        fact = f"{left} can contact {right}"
        start = prompt.find(fact)
        if start < 0:
            raise ValueError(f"Fact absent from prompt: {fact!r}")
        edge_spans.append({"edge": edge, "char_start": start, "char_end": start + len(fact)})
    query_spans = {}
    for role in ("source", "target"):
        value = graph[role]
        start = prompt.find(value)
        if start < 0:
            raise ValueError(f"Query entity absent from prompt: {value!r}")
        query_spans[role] = {"text": value, "char_start": start, "char_end": start + len(value)}
    return {"fact_edges": edge_spans, "query_entities": query_spans}


def freeze_population(
    sample_rows: list[dict[str, Any]], replay_rows: list[dict[str, Any]], upstream: Path
) -> list[dict[str, Any]]:
    replay_by_id = {row["item_id"]: row for row in replay_rows}
    attached = attach_prompts(sample_rows, upstream)
    frozen = []
    for row in attached:
        replay = replay_by_id[row["item_id"]]
        if row["variant"] != REGULAR_VARIANT:
            continue
        if row["cell"] == "mother_deceptive" and replay["replay_cell"] == "mother_deceptive":
            role = "hard_deceptive"
        elif row["cell"] == "hard_truthful" and replay["replay_cell"] == "hard_truthful":
            role = "hard_truthful"
        else:
            continue

        problem_path = upstream / "problem" / (
            f"{row['variant']}_problems_n1000_l{row['length']}_b{row['break_position']}.json"
        )
        problem = json.loads(problem_path.read_text(encoding="utf-8"))[row["source_row"]]
        initial_graph = graph_state(problem)
        followup_graph = graph_state(problem["followup_problem"])
        if initial_graph["correct_answer"] != row["initial"]["expected_answer"]:
            raise ValueError(f"Initial graph truth mismatch for {row['item_id']}")
        if followup_graph["correct_answer"] != row["followup"]["expected_answer"]:
            raise ValueError(f"Follow-up graph truth mismatch for {row['item_id']}")

        frozen.append(
            {
                "schema_version": 1,
                "item_id": row["item_id"],
                "role": role,
                "variant": row["variant"],
                "length": row["length"],
                "break_position": row["break_position"],
                "source_row": row["source_row"],
                "problem_sha256": row["problem_sha256"],
                "hard_prompt": row["problem"],
                "followup_prompt": row["followup_problem"],
                "hard_output": replay["initial_output"],
                "followup_output": replay["followup_output"],
                "hard_graph": initial_graph,
                "followup_graph": followup_graph,
                "hard_spans": fact_spans(row["problem"], initial_graph),
            }
        )
    return sorted(frozen, key=lambda row: (row["role"], row["item_id"]))


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            line = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
            handle.write(line)
            digest.update(line.encode())
    return digest.hexdigest()


def summarize(rows: list[dict[str, Any]], manifest_sha256: str) -> dict[str, Any]:
    by_role = {role: sum(row["role"] == role for row in rows) for role in ("hard_deceptive", "hard_truthful")}
    recipients = [row for row in rows if row["role"] == "hard_deceptive"]
    return {
        "schema_version": 1,
        "population_rule": {
            "model": "Meta-Llama-3.1-8B-Instruct",
            "variant": REGULAR_VARIANT,
            "hard_deceptive": "V0 audited mother_deceptive AND V1 deterministic mother_deceptive",
            "hard_truthful_control": "V0 audited hard_truthful AND V1 deterministic hard_truthful",
            "reverse_excluded": True,
        },
        "n_rows": len(rows),
        "n_by_role": by_role,
        "n_recipients": len(recipients),
        "all_recipient_hard_answers": sorted({row["hard_graph"]["correct_answer"] for row in recipients}),
        "all_recipient_reachable": sorted({row["hard_graph"]["reachable"] for row in recipients}),
        "break_positions": sorted({row["break_position"] for row in recipients}),
        "manifest_sha256": manifest_sha256,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--manifest-out", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()
    rows = freeze_population(read_jsonl(args.sample), read_jsonl(args.replay), args.upstream)
    digest = write_jsonl(args.manifest_out, rows)
    summary = summarize(rows, digest)
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
