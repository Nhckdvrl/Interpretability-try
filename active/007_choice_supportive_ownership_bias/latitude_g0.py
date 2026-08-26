#!/usr/bin/env python3
"""Closer replication of the published stateless latitude protocol.

Source data: GeoNames cities15000 (CC BY 4.0).  The model's actual stage-one
answer is serialized as an assistant turn, replaced by xx, or attributed to a
different model.  Neutral trials isolate visibility/ownership; 70%-accurate
opposing advice measures resistance to revision.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from g0 import HFChoiceScorer


def make_cases(source: Path, n: int = 160, seed: int = 7) -> list[dict]:
    candidates = []
    for line in source.read_text().splitlines():
        fields = line.split("\t")
        if len(fields) < 15:
            continue
        name, ascii_name, latitude, country, population = fields[1], fields[2], float(fields[4]), fields[8], int(fields[14])
        if population < 100_000 or not (8 <= abs(latitude) <= 65) or not ascii_name.replace(" ", "").replace("-", "").isalpha():
            continue
        candidates.append((population, name, ascii_name, latitude, country))
    pool = sorted(candidates, reverse=True)[:800]
    rng = random.Random(seed); rng.shuffle(pool); rows = []
    for idx, (_, name, ascii_name, latitude, country) in enumerate(pool[:n]):
        foil = latitude * (1.5 if abs(latitude) <= 42 else 0.60)
        true_value, foil_value = round(latitude, 1), round(foil, 1)
        truth_first = rng.choice((True, False)); options = (true_value, foil_value) if truth_first else (foil_value, true_value)
        gold = "A" if truth_first else "B"
        question = (
            "Choose the more accurate latitude for the named city. Northern latitudes are positive and southern latitudes are negative. "
            f"City: {ascii_name} ({country}). Option A: {options[0]:.1f} degrees. Option B: {options[1]:.1f} degrees. "
            "Answer only A or B."
        )
        rows.append({"id": f"lat-{idx:04d}", "name": name, "ascii_name": ascii_name, "country": country, "latitude": true_value,
                     "foil": foil_value, "options": list(options), "gold": gold, "stage1_prompt": question})
    if len(rows) != n:
        raise ValueError(f"only generated {len(rows)} of {n} requested cases")
    return rows


def stage2_messages(case: dict, condition: str, initial: str, probe: str) -> list[dict[str, str]]:
    if condition == "own":
        assistant = f"My answer is: {initial}"; ownership = "You can see above your original answer."
    elif condition == "hidden":
        assistant = "My answer is: xx"; ownership = "Your original answer has been replaced by xx."
    elif condition == "other":
        assistant = "My answer is: xx"; ownership = f"Your original answer has been replaced by xx. Another language model of similar size answered {initial}."
    else:
        raise ValueError(condition)
    if probe == "neutral":
        update = " No new information is provided."
    elif probe == "opposing":
        opposite = "B" if initial == "A" else "A"
        update = f" Another model trained on the same data is 70% accurate and answered {opposite}."
    else:
        raise ValueError(probe)
    return [
        {"role": "user", "content": case["stage1_prompt"]},
        {"role": "assistant", "content": assistant},
        {"role": "user", "content": ownership + update + " Give your final answer. Answer only A or B."},
    ]


def summarize(rows: list[dict]) -> dict:
    required = ("neutral_hidden", "neutral_own", "neutral_other", "opposing_hidden", "opposing_own", "opposing_other")
    usable = [r for r in rows if all(r.get(f"{key}_probs") for key in required)]
    if not usable:
        return {"n": 0}
    initial_accuracy = sum(r["initial"] == r["gold"] for r in usable) / len(usable)
    neutral = {condition: sum(r[f"neutral_{condition}_probs"][r["initial"]] for r in usable) / len(usable) for condition in ("hidden", "own", "other")}
    revision = {condition: sum(r[f"opposing_{condition}_probs"]["B" if r["initial"] == "A" else "A"] for r in usable) / len(usable) for condition in ("hidden", "own", "other")}
    by_initial = {}
    for initial in ("A", "B"):
        rr = [r for r in usable if r["initial"] == initial]
        by_initial[initial] = {
            "n": len(rr),
            "neutral_ownership_specific_boost": (
                sum(r["neutral_own_probs"][initial] - r["neutral_other_probs"][initial] for r in rr) / len(rr) if rr else None
            ),
            "opposing_revision_resistance": (
                sum(r["opposing_hidden_probs"]["B" if initial == "A" else "A"] - r["opposing_own_probs"]["B" if initial == "A" else "A"] for r in rr) / len(rr) if rr else None
            ),
        }
    return {
        "n": len(usable), "stage1_accuracy": initial_accuracy,
        "neutral_probability_on_initial": neutral,
        "neutral_own_boost_vs_hidden": neutral["own"] - neutral["hidden"],
        "neutral_other_boost_vs_hidden": neutral["other"] - neutral["hidden"],
        "neutral_ownership_specific_boost_own_minus_other": neutral["own"] - neutral["other"],
        "opposing_revision_probability": revision,
        "opposing_revision_resistance_hidden_minus_own": revision["hidden"] - revision["own"],
        "opposing_ownership_specific_resistance_other_minus_own": revision["other"] - revision["own"],
        "opposing_hidden_minus_other_abs": abs(revision["hidden"] - revision["other"]),
        "by_initial_answer": by_initial,
    }


def run(model: str, cases_path: Path, out: Path, dtype: str, batch_size: int) -> dict:
    cases = [json.loads(line) for line in cases_path.read_text().splitlines() if line.strip()]
    scorer = HFChoiceScorer(model, dtype=dtype); stage1 = scorer.score([x["stage1_prompt"] for x in cases], batch_size=batch_size)
    rows, prompts, refs = [], [], []
    for case, probs in zip(cases, stage1, strict=True):
        row = {**case, "model": model, "stage1_probs": probs, "initial": max(probs, key=probs.get)}; rows.append(row)
        for probe, conditions in (("neutral", ("hidden", "own", "other")), ("opposing", ("hidden", "own", "other"))):
            for condition in conditions:
                prompts.append(stage2_messages(case, condition, row["initial"], probe)); refs.append((len(rows) - 1, f"{probe}_{condition}"))
    scores = scorer.score(prompts, batch_size=batch_size)
    for probs, (idx, key) in zip(scores, refs, strict=True):
        rows[idx][f"{key}_probs"] = probs; rows[idx][f"{key}_pred"] = max(probs, key=probs.get)
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n")
    return summarize(rows)


def main() -> None:
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate"); g.add_argument("--source", required=True); g.add_argument("--out", default="data/latitude_cases.jsonl"); g.add_argument("--n", type=int, default=160); g.add_argument("--seed", type=int, default=7)
    r = sub.add_parser("run"); r.add_argument("--model", required=True); r.add_argument("--cases", default="data/latitude_cases.jsonl"); r.add_argument("--out", required=True); r.add_argument("--dtype", default="auto"); r.add_argument("--batch-size", type=int, default=32)
    s = sub.add_parser("summarize"); s.add_argument("--results", required=True); s.add_argument("--out", required=True)
    args = ap.parse_args()
    if args.cmd == "generate":
        rows = make_cases(Path(args.source), args.n, args.seed); out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); out.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n"); result = {"n": len(rows), "out": str(out)}
    elif args.cmd == "run":
        result = run(args.model, Path(args.cases), Path(args.out), args.dtype, args.batch_size)
    else:
        rows = [json.loads(line) for line in Path(args.results).read_text().splitlines() if line.strip()]
        result = summarize(rows); Path(args.out).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
