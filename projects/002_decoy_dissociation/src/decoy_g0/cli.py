from __future__ import annotations

import argparse
import json
from pathlib import Path

from .dataset import generate_scenarios, read_jsonl, write_jsonl
from .metrics import G0Thresholds, aggregate, summarize_scenarios, verdicts_to_dicts
from .prompts import build_choice_cases, build_dominance_cases
from .scoring import HFChoiceScorer


def generate_main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="data/scenarios.jsonl")
    p.add_argument("--strengths", nargs="+", type=float, default=[0.05, 0.10, 0.15])
    args = p.parse_args()
    scenarios = generate_scenarios(args.strengths)
    write_jsonl(args.out, scenarios)
    print(json.dumps({"n_scenarios": len(scenarios), "out": args.out}, indent=2))


def run_main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--data", default="data/scenarios.jsonl")
    p.add_argument("--out", required=True)
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--dtype", default="auto")
    args = p.parse_args()

    scenarios = read_jsonl(args.data)
    if args.limit is not None:
        scenarios = scenarios[: args.limit]
    scorer = HFChoiceScorer(args.model, dtype=args.dtype)
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for i, s in enumerate(scenarios, start=1):
            for case in build_choice_cases(s) + build_dominance_cases(s):
                score = scorer.score(case.prompt, case.labels)
                row = {
                    "model": args.model, "scenario_id": case.scenario_id, "case_id": case.case_id,
                    "kind": case.kind, "template_id": case.template_id, "permutation_id": case.permutation_id,
                    "semantic_by_label": case.semantic_by_label, "probs": score.probs, "logprobs": score.logprobs,
                }
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
            if i % 25 == 0:
                print(f"completed {i}/{len(scenarios)} scenarios", flush=True)


def summarize_main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--data", default="data/scenarios.jsonl")
    p.add_argument("--results", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    scenarios = read_jsonl(args.data)
    meta = {s.scenario_id: s.to_dict() for s in scenarios}
    with Path(args.results).open("r", encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if line.strip()]
    verdicts = summarize_scenarios(rows, meta, G0Thresholds())
    payload = {"thresholds": G0Thresholds().__dict__, "aggregate": aggregate(verdicts), "scenarios": verdicts_to_dicts(verdicts)}
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload["aggregate"], indent=2))


if __name__ == "__main__":
    raise SystemExit("Use decoy-generate, decoy-run, or decoy-summarize")
