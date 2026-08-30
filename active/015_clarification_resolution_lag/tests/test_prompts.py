import json
from pathlib import Path

from clarification_lag.prompts import build_messages


CONTRACT = json.loads(
    (Path(__file__).parents[1] / "configs" / "d0_contract.json").read_text(encoding="utf-8")
)
PAIR = {
    "question": "Where is the show located?",
    "target_condition": "The American series",
    "target_answer": "Colorado",
    "distractor_condition": "The Polish series",
    "distractor_answer": "Poland",
}


def test_final_evidence_and_options_are_identical_across_history_conditions():
    direct, _ = build_messages(PAIR, "direct", "target_first", CONTRACT)
    history, _ = build_messages(PAIR, "ambiguity_history", "target_first", CONTRACT)
    matched, _ = build_messages(PAIR, "matched_history", "target_first", CONTRACT)
    direct_block = direct[-1]["content"].split("Clarification:", 1)[1]
    history_block = history[-1]["content"].split("Clarification:", 1)[1]
    matched_block = matched[-1]["content"].split("Clarification:", 1)[1]
    assert direct_block == history_block == matched_block


def test_wrong_condition_flips_gold_without_changing_options():
    direct, direct_gold = build_messages(PAIR, "direct", "target_first", CONTRACT)
    wrong, wrong_gold = build_messages(PAIR, "wrong_condition", "target_first", CONTRACT)
    assert direct_gold == "A"
    assert wrong_gold == "B"
    assert "A. Colorado\nB. Poland" in direct[-1]["content"]
    assert "A. Colorado\nB. Poland" in wrong[-1]["content"]


def test_answer_order_counterbalance_flips_target_label():
    _, first_gold = build_messages(PAIR, "direct", "target_first", CONTRACT)
    _, second_gold = build_messages(PAIR, "direct", "target_second", CONTRACT)
    assert (first_gold, second_gold) == ("A", "B")
