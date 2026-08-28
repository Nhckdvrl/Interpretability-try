from __future__ import annotations

import argparse
import json
from pathlib import Path

from inadmissible_g0.data import load_scenarios
from inadmissible_g0.prompts import BINARY_ORDERS, POLARITY_ORDERS, condition_text, recognition_prompt, verdict_prompt
from inadmissible_g0.scoring import VLLMChoiceScorer

NUMERICAL_STABILITY_TOLERANCE = 1e-6

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--served-model", required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    scenario = load_scenarios(args.data)[0]
    polarity_prompt, _ = recognition_prompt(
        scenario.case_facts, scenario.evidence_text, scenario.struck_ruling,
        scenario.exclusion_scope, scenario.target_verdict, scenario.other_verdict,
        "polarity", POLARITY_ORDERS[0], scenario.evidence_polarity,
    )
    context = condition_text(
        scenario.case_facts, scenario.evidence_text, scenario.admissible_ruling, "admitted"
    )
    decision_prompt = verdict_prompt(
        context, scenario.target_verdict, scenario.other_verdict,
        "Which outcome is better supported by the case record?", BINARY_ORDERS[0],
    )
    requests = [(polarity_prompt, ("A", "B")), (decision_prompt, ("A", "B"))]

    scorer_one = VLLMChoiceScorer(
        args.model, base_url=args.base_url, revision=args.revision, served_model=args.served_model
    )
    prefix = scorer_one._prefix(polarity_prompt)
    prefix_ids = scorer_one.tokenizer(prefix, add_special_tokens=False).input_ids
    tokenization = {}
    for candidate in ("A", "B"):
        full_ids = scorer_one.tokenizer(prefix + candidate, add_special_tokens=False).input_ids
        suffix = full_ids[len(prefix_ids):] if full_ids[:len(prefix_ids)] == prefix_ids else []
        tokenization[candidate] = {
            "prefix_preserved": full_ids[:len(prefix_ids)] == prefix_ids,
            "continuation_token_count": len(suffix),
            "continuation_token_ids": suffix,
            "continuation_tokens": scorer_one.tokenizer.convert_ids_to_tokens(suffix),
        }
    first = scorer_one.score_batch(requests, sequence_batch_size=1)
    cached_repeat = scorer_one.score_batch(requests, sequence_batch_size=1)
    scorer_eight = VLLMChoiceScorer(
        args.model, base_url=args.base_url, revision=args.revision, served_model=args.served_model
    )
    batch_eight = scorer_eight.score_batch(requests, sequence_batch_size=8)

    def max_difference(left, right):
        return max(
            abs(left[index].probs[candidate] - right[index].probs[candidate])
            for index in range(len(left)) for candidate in ("A", "B")
        )

    report = {
        "model_repo": args.model,
        "served_model": args.served_model,
        "revision": args.revision,
        "base_url": args.base_url,
        "chat_template": scorer_one.tokenizer.chat_template,
        "thinking_disabled_when_supported": True,
        "tokenization": tokenization,
        "cached_repeat_max_probability_difference": max_difference(first, cached_repeat),
        "batch_1_vs_8_max_probability_difference": max_difference(first, batch_eight),
        "numerical_stability_tolerance": NUMERICAL_STABILITY_TOLERANCE,
        "requests_checked": len(requests),
        "pass": (
            all(item["prefix_preserved"] and item["continuation_token_count"] == 1 for item in tokenization.values())
            and max_difference(first, cached_repeat) == 0.0
            and max_difference(first, batch_eight) <= NUMERICAL_STABILITY_TOLERANCE
        ),
    }
    Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: report[key] for key in (
        "model_repo", "revision", "cached_repeat_max_probability_difference",
        "batch_1_vs_8_max_probability_difference", "pass",
    )}, indent=2))


if __name__ == "__main__":
    main()
