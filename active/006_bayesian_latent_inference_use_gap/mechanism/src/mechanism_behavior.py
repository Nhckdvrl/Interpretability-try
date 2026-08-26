#!/usr/bin/env python3
"""Behavioral preflight runner for the project-006 mechanism corpus."""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

from mechanism_data import (
    action_for,
    action_prompt,
    dump_jsonl,
    load_jsonl,
    make_evidence_states,
    make_policy_cases,
    make_surface_variants,
    posterior_prompt,
)


def chat_prefix(tokenizer, prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]
    kwargs = dict(tokenize=False, add_generation_prompt=True)
    try:
        return tokenizer.apply_chat_template(messages, enable_thinking=False, **kwargs)
    except TypeError:
        return tokenizer.apply_chat_template(messages, **kwargs)


class HFScorer:
    def __init__(self, model_name: str, dtype: str = "bfloat16"):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, trust_remote_code=True, local_files_only=True
        )
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        dtype_arg = getattr(torch, dtype)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=dtype_arg,
            device_map={"": 0},
            trust_remote_code=True,
            local_files_only=True,
            low_cpu_mem_usage=True,
            attn_implementation="sdpa",
        )
        self.model.eval()
        self.device = next(self.model.parameters()).device

    def score_choices(
        self,
        prompts: list[str],
        candidates: tuple[str, ...],
        sequence_batch_size: int,
    ) -> list[dict]:
        flat: list[dict] = []
        for prompt_i, prompt in enumerate(prompts):
            prefix = chat_prefix(self.tokenizer, prompt)
            prefix_ids = self.tokenizer(prefix, add_special_tokens=False).input_ids
            for candidate in candidates:
                full_ids = self.tokenizer(
                    prefix + candidate, add_special_tokens=False
                ).input_ids
                if full_ids[: len(prefix_ids)] != prefix_ids:
                    raise ValueError(
                        f"candidate changes prefix tokenization: {candidate!r}"
                    )
                flat.append(
                    {
                        "prompt_i": prompt_i,
                        "candidate": candidate,
                        "ids": full_ids,
                        "prefix_len": len(prefix_ids),
                    }
                )
        # Reduce padding while preserving the result order through prompt_i/candidate.
        flat.sort(key=lambda row: len(row["ids"]))
        log_scores: list[dict[str, float]] = [dict() for _ in prompts]
        for start in range(0, len(flat), sequence_batch_size):
            chunk = flat[start : start + sequence_batch_size]
            max_len = max(len(row["ids"]) for row in chunk)
            input_ids = []
            attention_mask = []
            for row in chunk:
                pad = max_len - len(row["ids"])
                input_ids.append(row["ids"] + [self.tokenizer.pad_token_id] * pad)
                attention_mask.append([1] * len(row["ids"]) + [0] * pad)
            ids_tensor = self.torch.tensor(input_ids, device=self.device)
            mask_tensor = self.torch.tensor(attention_mask, device=self.device)
            with self.torch.inference_mode():
                logits = self.model(
                    input_ids=ids_tensor, attention_mask=mask_tensor
                ).logits.float()
            log_probs = self.torch.log_softmax(logits, dim=-1)
            for row_i, row in enumerate(chunk):
                score = 0.0
                for pos in range(row["prefix_len"], len(row["ids"])):
                    score += float(log_probs[row_i, pos - 1, row["ids"][pos]])
                log_scores[row["prompt_i"]][row["candidate"]] = score

        results = []
        for scores in log_scores:
            peak = max(scores.values())
            exp_scores = {key: math.exp(value - peak) for key, value in scores.items()}
            total = sum(exp_scores.values())
            probabilities = {key: value / total for key, value in exp_scores.items()}
            results.append({"log_scores": scores, "probabilities": probabilities})
        return results


def run_posteriors(args: argparse.Namespace) -> dict:
    states = make_evidence_states(likelihood_ids=args.likelihood_ids)
    if args.limit:
        states = states[: args.limit]
    prompts = [posterior_prompt(state) for state in states]
    candidates = tuple(f"{i / 100:.2f}" for i in range(101))
    scorer = HFScorer(args.model, dtype=args.dtype)
    scored = scorer.score_choices(prompts, candidates, args.sequence_batch_size)
    rows = []
    for state, prompt, result in zip(states, prompts, scored, strict=True):
        distribution = result["probabilities"]
        argmax_text = max(distribution, key=distribution.get)
        mean = sum(float(value) * prob for value, prob in distribution.items())
        entropy = -sum(prob * math.log(max(prob, 1e-45)) for prob in distribution.values())
        rows.append(
            {
                **state,
                "model": args.model,
                "posterior_prompt": prompt,
                "posterior_mean": mean,
                "posterior_argmax": float(argmax_text),
                "posterior_peak_probability": distribution[argmax_text],
                "posterior_entropy": entropy,
                "posterior_distribution": distribution,
            }
        )
    dump_jsonl(rows, Path(args.out))
    return {
        "model": args.model,
        "n_evidence": len(rows),
        "posterior_mean_mae": (
            sum(abs(row["posterior_mean"] - row["gold_p_a"]) for row in rows)
            / len(rows)
            if rows
            else None
        ),
        "posterior_argmax_mae": (
            sum(abs(row["posterior_argmax"] - row["gold_p_a"]) for row in rows)
            / len(rows)
            if rows
            else None
        ),
        "out": args.out,
    }


def run_actions(args: argparse.Namespace) -> dict:
    posterior_rows = load_jsonl(Path(args.posteriors))
    posterior_by_evidence = {row["evidence_id"]: row for row in posterior_rows}
    likelihood_ids = sorted({row["likelihood_id"] for row in posterior_rows})
    cases = [
        case
        for case in make_policy_cases(likelihood_ids=likelihood_ids)
        if case["evidence_id"] in posterior_by_evidence
    ]
    surfaces = make_surface_variants()
    families = [(case, surface) for case in cases for surface in surfaces]
    families = [
        family
        for index, family in enumerate(families)
        if index % args.num_shards == args.shard_index
    ]
    if args.limit_families:
        families = families[: args.limit_families]

    rows = []
    for case, surface in families:
        posterior = posterior_by_evidence[case["evidence_id"]]
        for condition in args.conditions:
            row = action_prompt(
                case,
                surface,
                condition,
                self_mean=posterior["posterior_mean"],
                self_argmax=posterior["posterior_argmax"],
            )
            row["model"] = args.model
            row["posterior_mean"] = posterior["posterior_mean"]
            row["posterior_argmax"] = posterior["posterior_argmax"]
            row["posterior_peak_probability"] = posterior[
                "posterior_peak_probability"
            ]
            rows.append(row)

    scorer = HFScorer(args.model, dtype=args.dtype)
    scored = scorer.score_choices(
        [row["prompt"] for row in rows], ("A", "B"), args.sequence_batch_size
    )
    for row, result in zip(rows, scored, strict=True):
        probs = result["probabilities"]
        scores = result["log_scores"]
        mapping = row["option_mapping"]
        act_label = "A" if mapping[0] == "ACT" else "B"
        wait_label = "B" if act_label == "A" else "A"
        row["label_log_scores"] = scores
        row["label_probs"] = probs
        row["pred_label"] = max(probs, key=probs.get)
        row["pred_action"] = mapping[0] if row["pred_label"] == "A" else mapping[1]
        row["semantic_logit"] = scores[act_label] - scores[wait_label]
        row["condition_gold_logit"] = (
            row["semantic_logit"]
            if row["condition_action"] == "ACT"
            else -row["semantic_logit"]
        )
        row["original_gold_logit"] = (
            row["semantic_logit"]
            if row["gold_action"] == "ACT"
            else -row["semantic_logit"]
        )
        row["condition_correct"] = row["pred_action"] == row["condition_action"]
        row["gold_correct"] = row["pred_action"] == row["gold_action"]

    dump_jsonl(rows, Path(args.out))
    return {
        "model": args.model,
        "shard_index": args.shard_index,
        "num_shards": args.num_shards,
        "n_families": len(families),
        "n_prompts": len(rows),
        "out": args.out,
    }


def merge_rows(inputs: list[str], out: str) -> dict:
    rows = []
    for path in inputs:
        rows.extend(load_jsonl(Path(path)))
    if len({row["variant_id"] for row in rows}) != len(rows):
        raise ValueError("duplicate variant_id while merging shards")
    rows.sort(key=lambda row: row["variant_id"])
    dump_jsonl(rows, Path(out))
    return {"n": len(rows), "out": out}


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def summarize_rows(rows: list[dict]) -> dict:
    by_condition: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_condition[row["condition"]].append(row)
    condition_summary = {}
    for condition, group in sorted(by_condition.items()):
        condition_summary[condition] = {
            "n": len(group),
            "condition_accuracy": mean(
                [float(row["condition_correct"]) for row in group]
            ),
            "original_gold_accuracy": mean(
                [float(row["gold_correct"]) for row in group]
            ),
            "mean_condition_gold_logit": mean(
                [row["condition_gold_logit"] for row in group]
            ),
        }

    direct = by_condition.get("direct", [])
    direct_by_gold = {}
    for action in ("ACT", "WAIT"):
        group = [row for row in direct if row["gold_action"] == action]
        direct_by_gold[action] = {
            "n": len(group),
            "accuracy": mean([float(row["gold_correct"]) for row in group]),
            "mean_gold_logit": mean([row["original_gold_logit"] for row in group]),
        }

    mapping_groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in direct:
        key = (
            row["case_id"],
            row["action_words_id"],
            row["rule_predicate"],
            row["clause_order"],
        )
        mapping_groups[key].append(row)
    mapping_consistent = [
        len(group) == 2 and len({row["pred_action"] for row in group}) == 1
        for group in mapping_groups.values()
    ]

    posterior_by_evidence = {}
    for row in rows:
        posterior_by_evidence[row["evidence_id"]] = (
            row["posterior_mean"],
            row["posterior_argmax"],
            row["gold_p_a"],
        )
    posterior_mean_mae = mean(
        [abs(pred - gold) for pred, _, gold in posterior_by_evidence.values()]
    )
    posterior_argmax_mae = mean(
        [abs(pred - gold) for _, pred, gold in posterior_by_evidence.values()]
    )

    # Analyze every balanced surface variant whose elicited mean implies the gold action.
    eligible_keys = set()
    for row in direct:
        if (
            abs(row["posterior_mean"] - row["gold_p_a"]) <= 0.10
            and action_for(row["posterior_mean"], row["threshold"])
            == row["gold_action"]
        ):
            eligible_keys.add((row["case_id"], row["surface_id"]))

    indexed = {(row["case_id"], row["surface_id"], row["condition"]): row for row in rows}
    direct_errors = []
    gold_rescues = []
    self_rescues = []
    irrelevant_on_direct_errors = []
    for case_id, surface_id in eligible_keys:
        direct_row = indexed[(case_id, surface_id, "direct")]
        if not direct_row["gold_correct"]:
            direct_errors.append(direct_row)
            gold_row = indexed.get((case_id, surface_id, "gold_bridge"))
            self_row = indexed.get((case_id, surface_id, "self_mean_bridge"))
            irrelevant_row = indexed.get((case_id, surface_id, "irrelevant_number"))
            if gold_row:
                gold_rescues.append(float(gold_row["gold_correct"]))
            if self_row:
                self_rescues.append(float(self_row["gold_correct"]))
            if irrelevant_row:
                irrelevant_on_direct_errors.append(float(irrelevant_row["gold_correct"]))

    counterfactual = by_condition.get("counterfactual_bridge", [])
    summary = {
        "n_rows": len(rows),
        "n_evidence": len(posterior_by_evidence),
        "posterior_mean_mae": posterior_mean_mae,
        "posterior_argmax_mae": posterior_argmax_mae,
        "conditions": condition_summary,
        "direct_by_gold_action": direct_by_gold,
        "mapping_semantic_consistency": mean([float(x) for x in mapping_consistent]),
        "n_mapping_groups": len(mapping_groups),
        "n_eligible_surface_variants": len(eligible_keys),
        "n_direct_errors_eligible": len(direct_errors),
        "direct_error_rate_eligible": (
            len(direct_errors) / len(eligible_keys) if eligible_keys else None
        ),
        "gold_bridge_rescue_rate": mean(gold_rescues),
        "self_mean_bridge_rescue_rate": mean(self_rescues),
        "irrelevant_number_accuracy_on_direct_errors": mean(
            irrelevant_on_direct_errors
        ),
        "counterfactual_follow_rate": mean(
            [float(row["condition_correct"]) for row in counterfactual]
        ),
    }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    posterior = sub.add_parser("posteriors")
    posterior.add_argument("--model", required=True)
    posterior.add_argument("--out", required=True)
    posterior.add_argument("--dtype", default="bfloat16")
    posterior.add_argument("--sequence-batch-size", type=int, default=64)
    posterior.add_argument("--likelihood-ids", nargs="+", default=["sym80"])
    posterior.add_argument("--limit", type=int)

    actions = sub.add_parser("actions")
    actions.add_argument("--model", required=True)
    actions.add_argument("--posteriors", required=True)
    actions.add_argument("--out", required=True)
    actions.add_argument("--dtype", default="bfloat16")
    actions.add_argument("--sequence-batch-size", type=int, default=64)
    actions.add_argument("--shard-index", type=int, default=0)
    actions.add_argument("--num-shards", type=int, default=1)
    actions.add_argument("--limit-families", type=int)
    actions.add_argument(
        "--conditions",
        nargs="+",
        default=[
            "direct",
            "gold_bridge",
            "self_mean_bridge",
            "self_argmax_bridge",
            "counterfactual_bridge",
            "irrelevant_number",
        ],
    )

    merge = sub.add_parser("merge")
    merge.add_argument("--inputs", nargs="+", required=True)
    merge.add_argument("--out", required=True)

    summarize = sub.add_parser("summarize")
    summarize.add_argument("--results", required=True)
    summarize.add_argument("--out", required=True)

    args = parser.parse_args()
    if args.command == "posteriors":
        result = run_posteriors(args)
    elif args.command == "actions":
        result = run_actions(args)
    elif args.command == "merge":
        result = merge_rows(args.inputs, args.out)
    else:
        summary = summarize_rows(load_jsonl(Path(args.results)))
        Path(args.out).write_text(json.dumps(summary, indent=2) + "\n")
        result = summary
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
