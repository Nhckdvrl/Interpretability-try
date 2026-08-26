from __future__ import annotations

import math
import sys
from pathlib import Path


SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from mechanism_data import (  # noqa: E402
    ACTION_WORD_PAIRS,
    action_for,
    action_prompt,
    counterfactual_posterior,
    make_evidence_states,
    make_policy_cases,
    make_surface_variants,
)
from activation_cache import char_anchor_ends  # noqa: E402
from residual_interchange import baseline_correct, causal_action, causal_value  # noqa: E402


def test_exact_same_posterior_decompositions() -> None:
    states = make_evidence_states()
    by_key = {(row["prior_a"], row["count_difference"]): row for row in states}
    half = [by_key[(0.2, 1)], by_key[(0.5, 0)], by_key[(0.8, -1)]]
    low = [by_key[(0.2, 0)], by_key[(0.5, -1)], by_key[(0.8, -2)]]
    high = [by_key[(0.2, 2)], by_key[(0.5, 1)], by_key[(0.8, 0)]]
    for group, expected in ((half, 0.5), (low, 0.2), (high, 0.8)):
        assert all(math.isclose(row["gold_p_a"], expected, abs_tol=1e-12) for row in group)
        assert len({(row["prior_a"], row["n_red"], row["n_blue"]) for row in group}) == 3


def test_primary_policy_grid_and_margins() -> None:
    cases = make_policy_cases()
    assert len(cases) == 42
    assert sum(row["gold_action"] == "ACT" for row in cases) == 21
    assert sum(row["gold_action"] == "WAIT" for row in cases) == 21
    assert all(abs(row["raw_margin"]) >= 0.08 for row in cases)
    assert all(
        (row["decision_margin"] > 0) == (row["gold_action"] == "ACT")
        for row in cases
    )


def test_surface_factorial_and_mapping_truth_table() -> None:
    surfaces = make_surface_variants()
    assert len(surfaces) == 16
    case = next(row for row in make_policy_cases() if row["gold_action"] == "ACT")
    for surface in surfaces:
        row = action_prompt(case, surface, "gold_bridge")
        expected = "A" if surface["option_mapping"][0] == "ACT" else "B"
        assert row["expected_label"] == expected
        assert row["gold_label"] == expected
        assert ACTION_WORD_PAIRS[surface["action_words_id"]]["ACT"] in row["prompt"]
        assert ACTION_WORD_PAIRS[surface["action_words_id"]]["WAIT"] in row["prompt"]


def test_counterfactual_and_irrelevant_number_controls() -> None:
    case = make_policy_cases()[0]
    surface = make_surface_variants()[0]
    value = counterfactual_posterior(case)
    assert action_for(value, case["threshold"]) != case["gold_action"]
    self_mean = 0.123456
    bridge = action_prompt(
        case, surface, "self_mean_bridge", self_mean=self_mean, self_argmax=0.12
    )
    irrelevant = action_prompt(
        case, surface, "irrelevant_number", self_mean=self_mean, self_argmax=0.12
    )
    assert f"{self_mean:.6f}" in bridge["prompt"]
    assert f"{self_mean:.6f}" in irrelevant["prompt"]
    assert "not a probability" in irrelevant["prompt"]
    assert irrelevant["condition_action"] == case["gold_action"]


def test_variant_ids_unique() -> None:
    case = make_policy_cases()[0]
    rows = [
        action_prompt(
            case,
            surface,
            condition,
            self_mean=case["gold_p_a"],
            self_argmax=round(case["gold_p_a"], 2),
        )
        for surface in make_surface_variants()
        for condition in (
            "direct",
            "gold_bridge",
            "self_mean_bridge",
            "self_argmax_bridge",
            "counterfactual_bridge",
            "irrelevant_number",
        )
    ]
    assert len({row["variant_id"] for row in rows}) == len(rows)


def test_bridge_belief_anchor_ends_after_full_fixed_width_number() -> None:
    case = make_policy_cases()[0]
    surface = make_surface_variants()[0]
    bridge = action_prompt(case, surface, "gold_bridge")
    anchors = char_anchor_ends(bridge["prompt"], case["threshold"])
    assert bridge["prompt"][: anchors["BELIEF_NUM_END"]].endswith(
        f"{case['gold_p_a']:.6f}"
    )
    direct = action_prompt(case, surface, "direct")
    direct_anchors = char_anchor_ends(direct["prompt"], case["threshold"])
    assert direct_anchors["BELIEF_NUM_END"] == direct_anchors["EVIDENCE_END"]


def test_self_bridge_interchanges_use_serialized_belief_semantics() -> None:
    row = {
        "condition": "self_mean_bridge",
        "posterior_mean": 0.72,
        "posterior_argmax": 0.68,
        "gold_p_a": 0.2,
        "condition_action": "ACT",
        "gold_action": "WAIT",
        "condition_correct": True,
        "gold_correct": False,
    }
    assert causal_value(row) == 0.72
    assert causal_action(row) == "ACT"
    assert baseline_correct(row)
