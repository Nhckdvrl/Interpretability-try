#!/usr/bin/env python3
"""Cross-model, cross-task phenomenon meta-G0 for project 006."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
import math
import random
from collections import defaultdict
from pathlib import Path

from mechanism_behavior import HFScorer


def logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def posterior(prior: float, evidence: list[tuple[float, float, bool]]) -> float:
    value = logit(prior)
    for p_positive_target, p_positive_other, observed_positive in evidence:
        if observed_positive:
            value += math.log(p_positive_target / p_positive_other)
        else:
            value += math.log(
                (1.0 - p_positive_target) / (1.0 - p_positive_other)
            )
    return sigmoid(value)


def action_for(value: float, threshold: float) -> str:
    return "ACT" if value > threshold else "WAIT"


def stable_hash(*values: object) -> str:
    return hashlib.sha256("::".join(map(str, values)).encode()).hexdigest()


def write_jsonl_gz(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n"
    path.write_bytes(gzip.compress(text.encode(), mtime=0))


def read_jsonl_gz(path: Path) -> list[dict]:
    text = gzip.decompress(path.read_bytes()).decode()
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def make_urn_states() -> list[dict]:
    rows = []
    for prior in (0.20, 0.35, 0.50, 0.65, 0.80):
        for n_red, n_blue in ((0, 3), (1, 2), (2, 1), (3, 0), (1, 4), (2, 3), (3, 2), (4, 1)):
            evidence = [(0.75, 0.25, True)] * n_red + [(0.75, 0.25, False)] * n_blue
            gold = posterior(prior, evidence)
            evidence_id = f"urn-p{prior:.2f}-r{n_red}b{n_blue}"
            base = (
                "A container was selected from Type A or Type B. "
                f"Prior P(Type A)={prior:.2f}. Type A produces red objects with "
                "probability 0.75; Type B produces red objects with probability 0.25. "
                f"The observations contain {n_red} red and {n_blue} blue objects."
            )
            rows.append(
                {
                    "task_family": "iid_source_counts",
                    "evidence_id": evidence_id,
                    "target_name": "Type A",
                    "gold_p": gold,
                    "base_prompt": base,
                }
            )
    return rows


def make_medical_states() -> list[dict]:
    tests = (
        ("rapid antigen", 0.85, 0.20),
        ("laboratory assay", 0.92, 0.05),
        ("imaging screen", 0.75, 0.10),
    )
    rows = []
    for prior in (0.05, 0.10, 0.20, 0.35, 0.50):
        for outcomes in itertools.product((False, True), repeat=len(tests)):
            evidence = [
                (p_disease, p_no_disease, outcome)
                for (_, p_disease, p_no_disease), outcome in zip(tests, outcomes, strict=True)
            ]
            gold = posterior(prior, evidence)
            result_text = "; ".join(
                f"{name}: {'positive' if outcome else 'negative'}"
                for (name, _, _), outcome in zip(tests, outcomes, strict=True)
            )
            evidence_id = f"medical-p{prior:.2f}-o{''.join(map(lambda x: str(int(x)), outcomes))}"
            base = (
                f"A condition has prior probability {prior:.2f}. The rapid antigen "
                "test is positive with probabilities 0.85 with the condition and 0.20 "
                "without it. The laboratory assay is positive with probabilities 0.92 "
                "and 0.05. The imaging screen is positive with probabilities 0.75 and "
                f"0.10. Observed results: {result_text}. Tests are conditionally independent."
            )
            rows.append(
                {
                    "task_family": "heterogeneous_medical_tests",
                    "evidence_id": evidence_id,
                    "target_name": "the condition",
                    "gold_p": gold,
                    "base_prompt": base,
                }
            )
    return rows


def make_sensor_states() -> list[dict]:
    sensors = (
        ("sensor Alpha", 0.90, 0.10),
        ("sensor Beta", 0.75, 0.25),
        ("sensor Gamma", 0.65, 0.35),
        ("sensor Delta", 0.82, 0.18),
    )
    rows = []
    for prior in (0.10, 0.25, 0.50, 0.70):
        for outcomes in itertools.product((False, True), repeat=len(sensors)):
            evidence = [
                (p_fault, p_normal, outcome)
                for (_, p_fault, p_normal), outcome in zip(sensors, outcomes, strict=True)
            ]
            gold = posterior(prior, evidence)
            result_text = "; ".join(
                f"{name}: {'alarm' if outcome else 'clear'}"
                for (name, _, _), outcome in zip(sensors, outcomes, strict=True)
            )
            evidence_id = f"sensor-p{prior:.2f}-o{''.join(str(int(x)) for x in outcomes)}"
            base = (
                f"A machine has prior fault probability {prior:.2f}. Four independent "
                "sensors emit an alarm with probabilities (fault, normal): Alpha "
                "(0.90, 0.10), Beta (0.75, 0.25), Gamma (0.65, 0.35), Delta "
                f"(0.82, 0.18). Readings: {result_text}."
            )
            rows.append(
                {
                    "task_family": "conflicting_sensor_fusion",
                    "evidence_id": evidence_id,
                    "target_name": "machine fault",
                    "gold_p": gold,
                    "base_prompt": base,
                }
            )
    return rows


def make_recommender_states() -> list[dict]:
    items = (
        ("experimental film", 0.80, 0.30),
        ("spicy meal", 0.65, 0.20),
        ("traditional concert", 0.40, 0.75),
        ("adventure trip", 0.85, 0.35),
    )
    rows = []
    for prior in (0.20, 0.40, 0.60, 0.80):
        for outcomes in itertools.product((False, True), repeat=len(items)):
            evidence = [
                (p_explorer, p_routine, outcome)
                for (_, p_explorer, p_routine), outcome in zip(items, outcomes, strict=True)
            ]
            gold = posterior(prior, evidence)
            result_text = "; ".join(
                f"{name}: {'liked' if outcome else 'disliked'}"
                for (name, _, _), outcome in zip(items, outcomes, strict=True)
            )
            evidence_id = f"recommend-p{prior:.2f}-o{''.join(str(int(x)) for x in outcomes)}"
            base = (
                f"A user is Explorer-type rather than Routine-type with prior probability "
                f"{prior:.2f}. Conditional probabilities of liking each item for "
                "(Explorer, Routine) are: experimental film (0.80, 0.30), spicy meal "
                "(0.65, 0.20), traditional concert (0.40, 0.75), adventure trip "
                f"(0.85, 0.35). Feedback: {result_text}. Feedback items are conditionally independent."
            )
            rows.append(
                {
                    "task_family": "preference_recommender",
                    "evidence_id": evidence_id,
                    "target_name": "Explorer type",
                    "gold_p": gold,
                    "base_prompt": base,
                }
            )
    return rows


def select_policy_cases(states: list[dict], per_task: int, seed: int) -> list[dict]:
    candidates = []
    for state in states:
        for threshold in (0.30, 0.50, 0.70):
            if abs(state["gold_p"] - threshold) < 0.08:
                continue
            action = action_for(state["gold_p"], threshold)
            candidates.append(
                {
                    **state,
                    "threshold": threshold,
                    "gold_action": action,
                    "case_id": f"{state['evidence_id']}-t{threshold:.2f}",
                }
            )
    selected = []
    target_per_action = per_task // 2
    for action in ("ACT", "WAIT"):
        group = [row for row in candidates if row["gold_action"] == action]
        group.sort(key=lambda row: stable_hash(seed, row["case_id"]))
        if len(group) < target_per_action:
            raise ValueError((states[0]["task_family"], action, len(group)))
        selected.extend(group[:target_per_action])
    selected.sort(key=lambda row: row["case_id"])
    return selected


def make_dataset(per_task: int, seed: int) -> list[dict]:
    task_states = (
        make_urn_states(),
        make_medical_states(),
        make_sensor_states(),
        make_recommender_states(),
    )
    rows = []
    for states in task_states:
        rows.extend(select_policy_cases(states, per_task, seed))
    if len(rows) != 4 * per_task:
        raise AssertionError(len(rows))
    if len({row["case_id"] for row in rows}) != len(rows):
        raise AssertionError("case id collision")
    return rows


def report_prompt(row: dict) -> str:
    return (
        row["base_prompt"]
        + f" What is P({row['target_name']} | evidence)? Answer as a probability "
        "with exactly two digits after the decimal point."
    )


def surfaces() -> list[dict]:
    rows = []
    for vocabulary_id, words in (
        ("natural", {"ACT": "ACT", "WAIT": "WAIT"}),
        ("pseudoword", {"ACT": "ZORP", "WAIT": "KETA"}),
    ):
        for mapping in (("ACT", "WAIT"), ("WAIT", "ACT")):
            for rule_form in ("high_first", "low_first"):
                rows.append(
                    {
                        "vocabulary_id": vocabulary_id,
                        "words": words,
                        "mapping": mapping,
                        "rule_form": rule_form,
                        "surface_id": f"{vocabulary_id}-map{mapping[0]}{mapping[1]}-{rule_form}",
                    }
                )
    return rows


def action_prompt(row: dict, surface: dict, condition: str, self_p: float) -> dict:
    if condition == "direct":
        belief = ""
        condition_action = row["gold_action"]
    elif condition == "gold_bridge":
        belief = (
            f" For this decision, use the supplied posterior probability "
            f"P({row['target_name']} | evidence)={row['gold_p']:.6f}."
        )
        condition_action = row["gold_action"]
    elif condition == "self_bridge":
        belief = (
            f" For this decision, use the supplied posterior probability "
            f"P({row['target_name']} | evidence)={self_p:.6f}."
        )
        condition_action = action_for(self_p, row["threshold"])
    else:
        raise ValueError(condition)
    words = surface["words"]
    high, low = words["ACT"], words["WAIT"]
    if surface["rule_form"] == "high_first":
        rule = (
            f"If the posterior is greater than {row['threshold']:.6f}, select {high}; "
            f"otherwise select {low}."
        )
    else:
        rule = (
            f"Select {low} unless the posterior is greater than {row['threshold']:.6f}; "
            f"in that case select {high}."
        )
    mapping = surface["mapping"]
    option_a, option_b = words[mapping[0]], words[mapping[1]]
    prompt = (
        row["base_prompt"]
        + belief
        + " A fixed policy is defined as follows: "
        + rule
        + f" Option A is {option_a}. Option B is {option_b}."
        + " Which option does the fixed policy select? Answer only A or B."
    )
    expected_label = "A" if mapping[0] == condition_action else "B"
    return {
        **row,
        "condition": condition,
        "condition_action": condition_action,
        "surface_id": surface["surface_id"],
        "vocabulary_id": surface["vocabulary_id"],
        "rule_form": surface["rule_form"],
        "option_mapping": list(mapping),
        "expected_label": expected_label,
        "self_p": self_p,
        "prompt": prompt,
        "variant_id": f"{row['case_id']}::{surface['surface_id']}::{condition}",
    }


def score_model(args: argparse.Namespace) -> dict:
    dataset = read_jsonl_gz(args.dataset)
    if args.limit_cases:
        limited = []
        by_task: dict[str, list[dict]] = defaultdict(list)
        for row in dataset:
            by_task[row["task_family"]].append(row)
        for task in sorted(by_task):
            limited.extend(by_task[task][: args.limit_cases])
        dataset = limited
    scorer = HFScorer(args.model, dtype=args.dtype)
    evidence = {}
    for row in dataset:
        evidence[row["evidence_id"]] = row
    evidence_rows = sorted(evidence.values(), key=lambda row: row["evidence_id"])
    posterior_candidates = tuple(f"{i / 100:.2f}" for i in range(101))
    report_scores = scorer.score_choices(
        [report_prompt(row) for row in evidence_rows],
        posterior_candidates,
        args.posterior_batch_size,
    )
    report_rows = []
    posterior_by_evidence = {}
    for row, result in zip(evidence_rows, report_scores, strict=True):
        distribution = result["probabilities"]
        argmax = max(distribution, key=distribution.get)
        mean_p = sum(float(value) * prob for value, prob in distribution.items())
        posterior_by_evidence[row["evidence_id"]] = mean_p
        report_rows.append(
            {
                "row_type": "report",
                "model": args.model,
                "model_revision": getattr(scorer.model.config, "_commit_hash", args.model_revision),
                "task_family": row["task_family"],
                "evidence_id": row["evidence_id"],
                "gold_p": row["gold_p"],
                "posterior_mean": mean_p,
                "posterior_argmax": float(argmax),
                "posterior_peak_probability": distribution[argmax],
                "posterior_distribution": distribution,
                "prompt": report_prompt(row),
            }
        )
    action_rows = []
    for row in dataset:
        self_p = posterior_by_evidence[row["evidence_id"]]
        for surface in surfaces():
            for condition in ("direct", "gold_bridge", "self_bridge"):
                action_rows.append(action_prompt(row, surface, condition, self_p))
    scored_actions = scorer.score_choices(
        [row["prompt"] for row in action_rows],
        ("A", "B"),
        args.action_batch_size,
    )
    for row, result in zip(action_rows, scored_actions, strict=True):
        scores = result["log_scores"]
        probs = result["probabilities"]
        mapping = row["option_mapping"]
        act_label = "A" if mapping[0] == "ACT" else "B"
        wait_label = "B" if act_label == "A" else "A"
        row["row_type"] = "action"
        row["model"] = args.model
        row["model_revision"] = getattr(scorer.model.config, "_commit_hash", args.model_revision)
        row["label_log_scores"] = scores
        row["label_probs"] = probs
        row["semantic_logit"] = scores[act_label] - scores[wait_label]
        row["pred_label"] = max(probs, key=probs.get)
        row["pred_action"] = mapping[0] if row["pred_label"] == "A" else mapping[1]
        row["condition_correct"] = row["pred_action"] == row["condition_action"]
        row["gold_correct"] = row["pred_action"] == row["gold_action"]
        row["report_implied_action"] = action_for(row["self_p"], row["threshold"])
        row["inference_good"] = row["report_implied_action"] == row["gold_action"]
    raw_rows = report_rows + action_rows
    write_jsonl_gz(raw_rows, args.out)
    summary = summarize_model(raw_rows)
    summary["raw_path"] = str(args.out)
    summary["smoke"] = bool(args.limit_cases)
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def summarize_model(rows: list[dict]) -> dict:
    reports = [row for row in rows if row["row_type"] == "report"]
    actions = [row for row in rows if row["row_type"] == "action"]
    model = reports[0]["model"] if reports else actions[0]["model"]
    model_revision = reports[0]["model_revision"] if reports else actions[0]["model_revision"]
    report_by_evidence = {row["evidence_id"]: row for row in reports}

    def summarize_cells(group: list[dict]) -> dict:
        by_condition = defaultdict(list)
        for row in group:
            by_condition[row["condition"]].append(row)
        cases = {}
        for row in group:
            cases[row["case_id"]] = row
        report_action = [
            float(
                action_for(report_by_evidence[row["evidence_id"]]["posterior_mean"], row["threshold"])
                == row["gold_action"]
            )
            for row in cases.values()
        ]
        direct = by_condition["direct"]
        gold_bridge = by_condition["gold_bridge"]
        self_bridge = by_condition["self_bridge"]
        inference_good_direct = [row for row in direct if row["inference_good"]]
        mapping_groups = defaultdict(list)
        for row in direct:
            key = (row["case_id"], row["vocabulary_id"], row["rule_form"])
            mapping_groups[key].append(row)
        mapping_consistency = [
            len(group_rows) == 2
            and len({row["pred_action"] for row in group_rows}) == 1
            for group_rows in mapping_groups.values()
        ]
        return {
            "n_cases": len(cases),
            "report_implied_action_accuracy": mean(report_action),
            "direct_use_accuracy": mean([float(row["gold_correct"]) for row in direct]),
            "gold_bridge_execution_accuracy": mean(
                [float(row["condition_correct"]) for row in gold_bridge]
            ),
            "self_bridge_execution_accuracy": mean(
                [float(row["condition_correct"]) for row in self_bridge]
            ),
            "direct_error_rate_given_inference_good": (
                1.0 - mean([float(row["gold_correct"]) for row in inference_good_direct])
                if inference_good_direct
                else None
            ),
            "n_inference_good_direct_rows": len(inference_good_direct),
            "mapping_semantic_consistency": mean([float(x) for x in mapping_consistency]),
            "report_use_gap": (
                mean(report_action)
                - mean([float(row["gold_correct"]) for row in direct])
            ),
            "self_bridge_gain": (
                mean([float(row["gold_correct"]) for row in self_bridge])
                - mean([float(row["gold_correct"]) for row in direct])
            ),
        }

    task_summary = {}
    for task in sorted({row["task_family"] for row in actions}):
        task_actions = [row for row in actions if row["task_family"] == task]
        task_reports = [row for row in reports if row["task_family"] == task]
        cell = summarize_cells(task_actions)
        cell["posterior_mean_mae"] = mean(
            [abs(row["posterior_mean"] - row["gold_p"]) for row in task_reports]
        )
        task_summary[task] = cell
    overall = summarize_cells(actions)
    overall["posterior_mean_mae"] = mean(
        [abs(row["posterior_mean"] - row["gold_p"]) for row in reports]
    )
    return {
        "model": model,
        "model_revision": model_revision,
        "n_report_rows": len(reports),
        "n_action_rows": len(actions),
        "overall": overall,
        "tasks": task_summary,
    }


def aggregate(summary_paths: list[Path], out: Path) -> dict:
    summaries = [json.loads(path.read_text()) for path in summary_paths]
    cells = []
    for summary in summaries:
        for task, metrics in summary["tasks"].items():
            cells.append(
                {
                    "model": summary["model"],
                    "task_family": task,
                    **metrics,
                }
            )
    result = {
        "mother_question": "systematic dissociation among explicit belief report, direct behavioral use, and supplied-belief execution",
        "n_models": len(summaries),
        "n_task_families": len({row["task_family"] for row in cells}),
        "model_summaries": summaries,
        "model_task_cells": cells,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    generate = sub.add_parser("generate")
    generate.add_argument("--out", type=Path, required=True)
    generate.add_argument("--per-task", type=int, default=24)
    generate.add_argument("--seed", type=int, default=6060)

    run = sub.add_parser("run")
    run.add_argument("--model", required=True)
    run.add_argument("--model-revision", default="local-cache")
    run.add_argument("--dataset", type=Path, required=True)
    run.add_argument("--out", type=Path, required=True)
    run.add_argument("--summary-out", type=Path, required=True)
    run.add_argument("--dtype", default="bfloat16")
    run.add_argument("--posterior-batch-size", type=int, default=32)
    run.add_argument("--action-batch-size", type=int, default=64)
    run.add_argument("--limit-cases", type=int)

    agg = sub.add_parser("aggregate")
    agg.add_argument("--summaries", type=Path, nargs="+", required=True)
    agg.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "generate":
        rows = make_dataset(args.per_task, args.seed)
        write_jsonl_gz(rows, args.out)
        result = {
            "n_cases": len(rows),
            "n_tasks": len({row["task_family"] for row in rows}),
            "cases_per_task": {
                task: sum(row["task_family"] == task for row in rows)
                for task in sorted({row["task_family"] for row in rows})
            },
            "act_wait": {
                action: sum(row["gold_action"] == action for row in rows)
                for action in ("ACT", "WAIT")
            },
            "sha256": hashlib.sha256(args.out.read_bytes()).hexdigest(),
            "out": str(args.out),
        }
    elif args.command == "run":
        result = score_model(args)
    else:
        result = aggregate(args.summaries, args.out)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
