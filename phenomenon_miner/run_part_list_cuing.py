#!/usr/bin/env python3
"""Test whether reminding an LLM of part of a fact list impairs target recall."""

from __future__ import annotations

import argparse
import ast
import concurrent.futures
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any

import pyarrow.ipc as ipc

from run_natural_scan import call_chat, normalized


POPQA = Path(
    "/home/xiang/.cache/huggingface/datasets/akariasai___pop_qa/default/0.0.0/"
    "098765c79ea10a2cb19c828324e33281b8336ec0/pop_qa-test.arrow"
)


def read_rows() -> list[dict[str, Any]]:
    with POPQA.open("rb") as handle:
        rows = ipc.open_stream(handle).read_all().to_pylist()
    clean = []
    for row in rows:
        question = (row.get("question") or "").strip()
        answer = (row.get("obj") or "").strip()
        prop = (row.get("prop") or "").strip()
        if question and answer and prop and len(answer) <= 60:
            clean.append(row)
    return clean


def aliases(row: dict[str, Any]) -> list[str]:
    values = [row["obj"]]
    raw = row.get("possible_answers") or row.get("o_aliases") or ""
    for parser in (json.loads, ast.literal_eval):
        try:
            parsed = parser(raw)
            if isinstance(parsed, list):
                values.extend(str(x) for x in parsed)
                break
        except Exception:
            pass
    return list(dict.fromkeys(x.strip() for x in values if x and x.strip()))


def record(row: dict[str, Any]) -> str:
    return f"Q: {row['question'].strip()}\nA: {row['obj'].strip()}"


def build_requests(
    n_episodes: int,
    seed: int,
    related_study: int,
    unrelated_study: int,
) -> list[dict[str, Any]]:
    rows = read_rows()
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[row["prop"]].append(row)
    eligible = [prop for prop, members in groups.items() if len(members) >= related_study + 2]
    rng = random.Random(seed)
    requests: list[dict[str, Any]] = []
    used_targets: set[int] = set()

    for episode_id in range(n_episodes):
        prop = eligible[episode_id % len(eligible)]
        candidates = [r for r in groups[prop] if r["id"] not in used_targets]
        if len(candidates) < related_study + 1:
            candidates = groups[prop]
        target = rng.choice(candidates)
        used_targets.add(target["id"])
        related = rng.sample(
            [r for r in groups[prop] if r["id"] != target["id"]], related_study
        )
        other_pool = [r for r in rows if r["prop"] != prop]
        unrelated = rng.sample(other_pool, unrelated_study)
        studied = [target, *related, *unrelated]
        rng.shuffle(studied)

        cue_small = min(8, related_study)
        cue_medium = min(24, related_study)
        cue_large = min(48, related_study)
        unrelated_cue = min(cue_medium, unrelated_study)
        conditions: list[tuple[str, list[dict[str, Any]]]] = [
            ("no_cues", []),
            (f"related_cues_{cue_small}", related[:cue_small]),
            (f"related_cues_{cue_medium}", related[:cue_medium]),
            (f"related_cues_{cue_large}", related[:cue_large]),
            (f"unrelated_cues_{unrelated_cue}", unrelated[:unrelated_cue]),
            ("target_cue", [target]),
        ]
        study_text = "\n\n".join(record(row) for row in studied)
        for condition, cues in conditions:
            cue_text = "\n\n".join(record(row) for row in cues) if cues else "(none)"
            prompt = (
                "Study the following factual records.\n\n"
                f"{study_text}\n\n"
                "Some records are repeated below as reminders. They do not replace or invalidate "
                "any of the records above.\n\n"
                f"{cue_text}\n\n"
                f"Now answer this question from the studied records:\n{target['question'].strip()}\n\n"
                "Return only the exact answer from the record."
            )
            requests.append(
                {
                    "episode_id": episode_id,
                    "target_id": target["id"],
                    "property": prop,
                    "question": target["question"].strip(),
                    "answer": target["obj"].strip(),
                    "aliases": aliases(target),
                    "condition": condition,
                    "cue_ids": [row["id"] for row in cues],
                    "prompt": prompt,
                }
            )
    return requests


def main(args: argparse.Namespace) -> None:
    requests = build_requests(
        args.episodes, args.seed, args.related_study, args.unrelated_study
    )

    def evaluate(item: dict[str, Any]) -> dict[str, Any]:
        response = call_chat(args.base_url, args.model, item["prompt"])
        norm = normalized(response)
        accepted = {normalized(answer) for answer in item["aliases"]}
        return {k: v for k, v in item.items() if k != "prompt"} | {
            "model": args.model,
            "response": response,
            "is_correct": norm in accepted,
        }

    results: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(evaluate, item) for item in requests]
        for done, future in enumerate(concurrent.futures.as_completed(futures), 1):
            results.append(future.result())
            if done % 100 == 0:
                print(f"completed {done}/{len(futures)}", flush=True)
    results.sort(key=lambda x: (x["episode_id"], x["condition"]))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        for row in results:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    by_condition: dict[str, list[bool]] = defaultdict(list)
    by_episode: dict[int, dict[str, bool]] = defaultdict(dict)
    for row in results:
        by_condition[row["condition"]].append(row["is_correct"])
        by_episode[row["episode_id"]][row["condition"]] = row["is_correct"]
    summary = {
        "model": args.model,
        "n_episodes": args.episodes,
        "accuracy": {k: sum(v) / len(v) for k, v in sorted(by_condition.items())},
        "paired_flips": {
            condition: {
                "help": sum((not v["no_cues"]) and v[condition] for v in by_episode.values()),
                "hurt": sum(v["no_cues"] and (not v[condition]) for v in by_episode.values()),
            }
            for condition in sorted(k for k in by_condition if k != "no_cues")
        },
    }
    out.with_suffix(".summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--episodes", type=int, default=240)
    parser.add_argument("--seed", type=int, default=20260827)
    parser.add_argument("--workers", type=int, default=24)
    parser.add_argument("--related-study", type=int, default=60)
    parser.add_argument("--unrelated-study", type=int, default=40)
    main(parser.parse_args())
