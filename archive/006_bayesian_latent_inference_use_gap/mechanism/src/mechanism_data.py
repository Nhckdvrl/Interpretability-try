"""Orthogonalized mechanism data for project 006.

The primary corpus uses exact same-posterior decompositions under the symmetric
0.8/0.2 likelihood.  Surface variants independently manipulate policy form,
branch mention order, action vocabulary, and option mapping.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Iterable
from pathlib import Path


PRIORS = (0.2, 0.5, 0.8)
COUNT_DIFFERENCES = (-2, -1, 0, 1, 2)
THRESHOLDS = (0.3, 0.5, 0.7)
LIKELIHOOD_REGIMES = (
    ("sym80", 0.8, 0.2),
    ("sym70", 0.7, 0.3),
    ("sym90", 0.9, 0.1),
)
ACTION_WORD_PAIRS = {
    "natural": {"ACT": "ACT", "WAIT": "WAIT"},
    "neutral": {"ACT": "ZORP", "WAIT": "KETA"},
}
OPTION_MAPPINGS = (("ACT", "WAIT"), ("WAIT", "ACT"))
RULE_FORMS = (
    ("gt", "high_first"),
    ("gt", "low_first"),
    ("le", "low_first"),
    ("le", "high_first"),
)


def logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def posterior_a(
    prior_a: float,
    n_red: int,
    n_blue: int,
    p_red_a: float,
    p_red_b: float,
) -> float:
    z = (
        logit(prior_a)
        + n_red * math.log(p_red_a / p_red_b)
        + n_blue * math.log((1.0 - p_red_a) / (1.0 - p_red_b))
    )
    return 1.0 / (1.0 + math.exp(-z))


def action_for(posterior: float, threshold: float) -> str:
    return "ACT" if posterior > threshold else "WAIT"


def counts_for_difference(difference: int, pair_offset: int = 0) -> tuple[int, int]:
    """Return nonzero counts with the requested red-minus-blue difference."""
    if difference % 2 == 0:
        total = 4 + 2 * pair_offset
    else:
        total = 3 + 2 * pair_offset
    n_red = (total + difference) // 2
    n_blue = (total - difference) // 2
    if n_red < 0 or n_blue < 0:
        raise ValueError((difference, pair_offset))
    return n_red, n_blue


def make_evidence_states(
    likelihood_ids: Iterable[str] = ("sym80",),
    pair_offsets: Iterable[int] = (0,),
) -> list[dict]:
    regimes = {row[0]: row for row in LIKELIHOOD_REGIMES}
    states: list[dict] = []
    for likelihood_id in likelihood_ids:
        _, p_red_a, p_red_b = regimes[likelihood_id]
        for prior in PRIORS:
            for difference in COUNT_DIFFERENCES:
                for pair_offset in pair_offsets:
                    n_red, n_blue = counts_for_difference(difference, pair_offset)
                    posterior = posterior_a(prior, n_red, n_blue, p_red_a, p_red_b)
                    prior_logit = logit(prior)
                    evidence_llr = (
                        n_red * math.log(p_red_a / p_red_b)
                        + n_blue * math.log((1.0 - p_red_a) / (1.0 - p_red_b))
                    )
                    state_id = (
                        f"{likelihood_id}-pi{prior:.2f}-d{difference:+d}-o{pair_offset}"
                    )
                    states.append(
                        {
                            "evidence_id": state_id,
                            "likelihood_id": likelihood_id,
                            "prior_a": prior,
                            "prior_logit": prior_logit,
                            "p_red_a": p_red_a,
                            "p_red_b": p_red_b,
                            "n_red": n_red,
                            "n_blue": n_blue,
                            "count_difference": difference,
                            "pair_offset": pair_offset,
                            "evidence_llr": evidence_llr,
                            "gold_p_a": posterior,
                            "posterior_logit": logit(posterior),
                        }
                    )
    return states


def make_policy_cases(
    likelihood_ids: Iterable[str] = ("sym80",),
    thresholds: Iterable[float] = THRESHOLDS,
    min_raw_margin: float = 0.08,
) -> list[dict]:
    rows: list[dict] = []
    for state in make_evidence_states(likelihood_ids=likelihood_ids):
        for threshold in thresholds:
            raw_margin = state["gold_p_a"] - threshold
            if abs(raw_margin) < min_raw_margin:
                continue
            threshold_logit = logit(threshold)
            row = {
                **state,
                "threshold": threshold,
                "threshold_logit": threshold_logit,
                "raw_margin": raw_margin,
                "decision_margin": state["posterior_logit"] - threshold_logit,
                "gold_action": action_for(state["gold_p_a"], threshold),
            }
            row["case_id"] = f"{state['evidence_id']}-t{threshold:.2f}"
            rows.append(row)
    return rows


def base_prompt(case: dict) -> str:
    return (
        "A hidden source is Type A or Type B. "
        f"Prior P(A)={case['prior_a']:.2f}. "
        f"Type A emits red with probability {case['p_red_a']:.2f} and blue with "
        f"probability {1.0 - case['p_red_a']:.2f}; Type B emits red with probability "
        f"{case['p_red_b']:.2f} and blue with probability {1.0 - case['p_red_b']:.2f}. "
        f"Observed counts: red count {case['n_red']:02d}; blue count {case['n_blue']:02d}."
    )


def posterior_prompt(case: dict) -> str:
    return (
        base_prompt(case)
        + " What is P(A | observations)? Answer as a probability with exactly two "
        "digits after the decimal point."
    )


def rule_text(
    threshold: float,
    words: dict[str, str],
    predicate: str,
    clause_order: str,
) -> str:
    high, low = words["ACT"], words["WAIT"]
    t = f"{threshold:.6f}"
    if (predicate, clause_order) == ("gt", "high_first"):
        return (
            f"If P(A | observations) is greater than {t}, the policy selects {high}; "
            f"otherwise it selects {low}."
        )
    if (predicate, clause_order) == ("gt", "low_first"):
        return (
            f"The policy selects {low} by default and switches to {high} exactly if "
            f"P(A | observations) is greater than {t}."
        )
    if (predicate, clause_order) == ("le", "low_first"):
        return (
            f"If P(A | observations) is less than or equal to {t}, the policy selects "
            f"{low}; otherwise it selects {high}."
        )
    if (predicate, clause_order) == ("le", "high_first"):
        return (
            f"The policy selects {high} by default and switches to {low} exactly if "
            f"P(A | observations) is less than or equal to {t}."
        )
    raise ValueError((predicate, clause_order))


def counterfactual_posterior(case: dict, distance: float = 0.18) -> float:
    threshold = case["threshold"]
    if case["gold_action"] == "ACT":
        return max(0.01, threshold - distance)
    return min(0.99, threshold + distance)


def belief_text(
    condition: str,
    case: dict,
    self_mean: float | None = None,
    self_argmax: float | None = None,
) -> tuple[str, float | None, str]:
    """Return text, serialized value, and the action implied by that condition."""
    if condition == "direct":
        return "", None, case["gold_action"]
    if condition == "gold_bridge":
        value = case["gold_p_a"]
        action = action_for(value, case["threshold"])
        return (
            f" For this decision, use the posterior value P(A | observations)={value:.6f}.",
            value,
            action,
        )
    if condition == "self_mean_bridge":
        if self_mean is None:
            raise ValueError("self_mean is required")
        action = action_for(self_mean, case["threshold"])
        return (
            f" For this decision, use the posterior value P(A | observations)={self_mean:.6f}.",
            self_mean,
            action,
        )
    if condition == "self_argmax_bridge":
        if self_argmax is None:
            raise ValueError("self_argmax is required")
        action = action_for(self_argmax, case["threshold"])
        return (
            f" For this decision, use the posterior value P(A | observations)={self_argmax:.6f}.",
            self_argmax,
            action,
        )
    if condition == "counterfactual_bridge":
        value = counterfactual_posterior(case)
        action = action_for(value, case["threshold"])
        return (
            f" For this decision, use the posterior value P(A | observations)={value:.6f}.",
            value,
            action,
        )
    if condition == "irrelevant_number":
        if self_mean is None:
            raise ValueError("self_mean is required")
        return (
            " Calibration identifier (not a probability and irrelevant to the policy)="
            f"{self_mean:.6f}.",
            self_mean,
            case["gold_action"],
        )
    raise ValueError(condition)


def make_surface_variants() -> list[dict]:
    rows = []
    for action_words_id, words in ACTION_WORD_PAIRS.items():
        for predicate, clause_order in RULE_FORMS:
            for mapping in OPTION_MAPPINGS:
                rows.append(
                    {
                        "action_words_id": action_words_id,
                        "action_words": words,
                        "rule_predicate": predicate,
                        "clause_order": clause_order,
                        "option_mapping": mapping,
                    }
                )
    return rows


def action_prompt(
    case: dict,
    surface: dict,
    condition: str,
    self_mean: float | None = None,
    self_argmax: float | None = None,
) -> dict:
    belief, serialized_value, condition_action = belief_text(
        condition, case, self_mean=self_mean, self_argmax=self_argmax
    )
    words = surface["action_words"]
    mapping = surface["option_mapping"]
    option_a, option_b = words[mapping[0]], words[mapping[1]]
    rule = rule_text(
        case["threshold"], words, surface["rule_predicate"], surface["clause_order"]
    )
    prompt = (
        base_prompt(case)
        + belief
        + " A fixed policy is defined as follows: "
        + rule
        + f" Option A is {option_a}. Option B is {option_b}."
        + " Which option does the fixed policy select? Answer only A or B."
    )
    expected_label = "A" if mapping[0] == condition_action else "B"
    gold_label = "A" if mapping[0] == case["gold_action"] else "B"
    surface_id = (
        f"{surface['action_words_id']}-{surface['rule_predicate']}-"
        f"{surface['clause_order']}-map{mapping[0]}{mapping[1]}"
    )
    variant_id = f"{case['case_id']}::{surface_id}::{condition}"
    return {
        **case,
        "variant_id": variant_id,
        "surface_id": surface_id,
        "condition": condition,
        "serialized_value": serialized_value,
        "condition_action": condition_action,
        "expected_label": expected_label,
        "gold_label": gold_label,
        "action_words_id": surface["action_words_id"],
        "rule_predicate": surface["rule_predicate"],
        "clause_order": surface["clause_order"],
        "option_mapping": list(mapping),
        "prompt": prompt,
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
    }


def dump_jsonl(rows: Iterable[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
