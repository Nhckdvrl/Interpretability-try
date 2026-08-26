#!/usr/bin/env python3
"""Behavior-only PI/RI preflight for the Primacy Lock candidate.

This script intentionally does NOT inspect activations.  It constructs matched
histories where the only experimental change is whether the query asks for the
FIRST or the LATEST value associated with each key, runs an OpenAI-compatible
local endpoint, and classifies same-key historical intrusions.

Use the public 46-key/400-value source dictionary from Unable-to-Forget for the
first smoke test.  Before a confirmatory run, compare the prompt template here
against the exact protocol of the target behavior paper and freeze any changes.
"""

from __future__ import annotations

import argparse
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

from common import load_json, load_jsonl, post_chat_completion, write_jsonl

DEFAULT_COUNTS = (3, 10, 50, 100, 200, 300)


def normalize(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[`*_\"']", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" .,:;!?()[]{}")


def choose_history(source: dict[str, list[str]], *, n_keys: int, n_updates: int, rng: random.Random) -> tuple[list[str], dict[str, list[str]]]:
    eligible = [k for k, values in source.items() if len(set(values)) >= n_updates]
    if len(eligible) < n_keys:
        raise ValueError(f"need {n_keys} keys with >= {n_updates} distinct values, found {len(eligible)}")
    keys = sorted(rng.sample(eligible, n_keys))
    history: dict[str, list[str]] = {}
    for key in keys:
        values = list(dict.fromkeys(source[key]))
        history[key] = rng.sample(values, n_updates)
    return keys, history


def render_history(keys: list[str], history: dict[str, list[str]]) -> str:
    n_updates = len(history[keys[0]])
    lines = [
        "The values associated with the following categories change over time.",
        "Read every assignment carefully. Different values for the same category are intentional.",
    ]
    for step in range(n_updates):
        lines.append(f"\nUpdate {step + 1}:")
        for key in keys:
            lines.append(f"{key}: {history[key][step]}")
    return "\n".join(lines)


def render_query(keys: list[str], target: str) -> str:
    if target == "first":
        phrase = "the FIRST value assigned to each category"
    elif target == "latest":
        phrase = "the MOST RECENT (LATEST) value assigned to each category"
    else:
        raise ValueError(target)
    joined = ", ".join(keys)
    return (
        f"\n\nQuestion: What was {phrase}?\n"
        f"Return exactly one mapping for every category in this order: {joined}.\n"
        "Use one line per category in the form `category: value`. Do not explain."
    )


def generate_cases(source: dict[str, list[str]], *, counts: list[int], seeds: list[int], n_keys: int) -> list[dict]:
    rows: list[dict] = []
    for seed in seeds:
        for n_updates in counts:
            rng = random.Random((seed + 1) * 1_000_003 + n_updates)
            keys, history = choose_history(source, n_keys=n_keys, n_updates=n_updates, rng=rng)
            base = render_history(keys, history)
            for target in ("first", "latest"):
                gold_index = 0 if target == "first" else n_updates - 1
                rows.append({
                    "case_id": f"seed{seed:03d}_u{n_updates:03d}_{target}",
                    "seed": seed,
                    "n_updates": n_updates,
                    "target": target,
                    "keys": keys,
                    "history": history,
                    "gold": {k: history[k][gold_index] for k in keys},
                    "prompt": base + render_query(keys, target),
                })
    return rows


def parse_mapping(text: str, keys: list[str]) -> dict[str, str]:
    """Parse either JSON dict output or key: value lines; unmatched keys stay absent."""
    stripped = text.strip()
    try:
        obj = json.loads(stripped)
        if isinstance(obj, dict):
            by_norm = {normalize(str(k)): str(v) for k, v in obj.items()}
            return {k: by_norm[normalize(k)] for k in keys if normalize(k) in by_norm}
    except Exception:
        pass

    key_lookup = {normalize(k): k for k in keys}
    parsed: dict[str, str] = {}
    for line in stripped.splitlines():
        m = re.match(r"\s*(?:[-*]\s*)?(.+?)\s*[:=\-]\s*(.+?)\s*$", line)
        if not m:
            continue
        left, right = normalize(m.group(1)), m.group(2).strip()
        if left in key_lookup:
            parsed[key_lookup[left]] = right
    return parsed


def classify_key(pred: str | None, values: list[str], target: str) -> dict:
    if pred is None:
        return {"class": "missing", "matched_index": None}
    p = normalize(pred)
    norm_values = [normalize(v) for v in values]
    matches = [i for i, v in enumerate(norm_values) if p == v]
    if not matches:
        matches = [i for i, v in enumerate(norm_values) if len(v) >= 3 and (p.endswith(v) or p.startswith(v))]
    if not matches:
        return {"class": "other", "matched_index": None}
    idx = matches[-1]
    gold_idx = 0 if target == "first" else len(values) - 1
    if idx == gold_idx:
        return {"class": "correct", "matched_index": idx}
    if target == "latest":
        return {"class": "primacy_intrusion" if idx == 0 else "stale_intrusion", "matched_index": idx}
    return {"class": "newer_intrusion", "matched_index": idx}


def score_case(case: dict, response: str) -> dict:
    mapping = parse_mapping(response, case["keys"])
    per_key = {}
    counts = Counter()
    for key in case["keys"]:
        result = classify_key(mapping.get(key), case["history"][key], case["target"])
        per_key[key] = {"prediction": mapping.get(key), **result}
        counts[result["class"]] += 1
    n = len(case["keys"])
    return {
        "parsed_fraction": (n - counts["missing"]) / n,
        "accuracy": counts["correct"] / n,
        "class_counts": dict(counts),
        "per_key": per_key,
    }


def summarize(rows: list[dict]) -> dict:
    complete = [r for r in rows if "score" in r]
    by_updates: dict[int, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in complete:
        by_updates[int(row["n_updates"])][row["target"]].append(row)

    summary_by_updates = {}
    for n_updates, targets in sorted(by_updates.items()):
        out = {"n_updates": n_updates}
        for target in ("first", "latest"):
            rr = targets.get(target, [])
            if not rr:
                continue
            out[target] = {
                "n_sessions": len(rr),
                "mean_accuracy": sum(x["score"]["accuracy"] for x in rr) / len(rr),
                "mean_parsed_fraction": sum(x["score"]["parsed_fraction"] for x in rr) / len(rr),
                "session_accuracy": [x["score"]["accuracy"] for x in rr],
            }
            if target == "latest":
                errors = Counter()
                for x in rr:
                    errors.update(x["score"]["class_counts"])
                wrong = sum(v for k, v in errors.items() if k != "correct")
                stale = errors["stale_intrusion"] + errors["primacy_intrusion"]
                out[target]["error_counts"] = dict(errors)
                out[target]["same_key_stale_share_of_all_errors"] = stale / wrong if wrong else None
                out[target]["primacy_share_of_all_errors"] = errors["primacy_intrusion"] / wrong if wrong else None
                out[target]["n_near_zero_sessions"] = sum(x["score"]["accuracy"] <= 0.05 for x in rr)
                out[target]["n_near_perfect_sessions"] = sum(x["score"]["accuracy"] >= 0.85 for x in rr)
        if "first" in out and "latest" in out:
            out["first_minus_latest_gap"] = out["first"]["mean_accuracy"] - out["latest"]["mean_accuracy"]
        summary_by_updates[str(n_updates)] = out

    paired = {}
    indexed = {(r["seed"], r["n_updates"], r["target"]): r for r in complete}
    for n_updates in sorted({r["n_updates"] for r in complete}):
        diffs = []
        for seed in sorted({r["seed"] for r in complete}):
            a = indexed.get((seed, n_updates, "first"))
            b = indexed.get((seed, n_updates, "latest"))
            if a and b:
                diffs.append(a["score"]["accuracy"] - b["score"]["accuracy"])
        if diffs:
            paired[str(n_updates)] = {"n_pairs": len(diffs), "mean_gap": sum(diffs) / len(diffs), "gaps": diffs}

    return {"n_rows": len(rows), "n_scored": len(complete), "by_updates": summary_by_updates, "paired": paired}


def run_cases(cases: list[dict], args) -> list[dict]:
    rows = []
    for i, case in enumerate(cases, 1):
        response = post_chat_completion(
            args.endpoint,
            args.model,
            [{"role": "user", "content": case["prompt"]}],
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            timeout=args.timeout,
            api_key=args.api_key,
            extra_body={"seed": args.generation_seed} if args.generation_seed is not None else None,
        )
        row = dict(case)
        row.update({"model": args.model, "endpoint": args.endpoint, "response": response})
        row["score"] = score_case(row, response)
        rows.append(row)
        if args.verbose:
            print(f"[{i}/{len(cases)}] {case['case_id']} acc={row['score']['accuracy']:.3f}")
    return rows


def parse_int_list(text: str) -> list[int]:
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate")
    g.add_argument("--source-json", required=True)
    g.add_argument("--counts", default=",".join(map(str, DEFAULT_COUNTS)))
    g.add_argument("--seeds", default="0,1,2,3,4")
    g.add_argument("--n-keys", type=int, default=46)
    g.add_argument("--out", required=True)

    r = sub.add_parser("run")
    r.add_argument("--cases", required=True)
    r.add_argument("--endpoint", required=True)
    r.add_argument("--model", required=True)
    r.add_argument("--out", required=True)
    r.add_argument("--api-key", default="EMPTY")
    r.add_argument("--temperature", type=float, default=0.0)
    r.add_argument("--max-tokens", type=int, default=2048)
    r.add_argument("--timeout", type=int, default=600)
    r.add_argument("--generation-seed", type=int, default=0)
    r.add_argument("--limit", type=int)
    r.add_argument("--verbose", action="store_true")

    s = sub.add_parser("summarize")
    s.add_argument("--results", required=True)
    s.add_argument("--out")

    args = ap.parse_args()
    if args.cmd == "generate":
        source = load_json(args.source_json)
        cases = generate_cases(source, counts=parse_int_list(args.counts), seeds=parse_int_list(args.seeds), n_keys=args.n_keys)
        write_jsonl(args.out, cases)
        result = {"n_cases": len(cases), "out": args.out}
    elif args.cmd == "run":
        cases = load_jsonl(args.cases)
        if args.limit:
            cases = cases[: args.limit]
        rows = run_cases(cases, args)
        write_jsonl(args.out, rows)
        result = summarize(rows)
    else:
        result = summarize(load_jsonl(args.results))
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
