import json
from pathlib import Path

from stock_flow_intrusion.analyze_v2 import aggregate_v2
from stock_flow_intrusion.prompts import net_semantic_messages, stock_messages_v2
from stock_flow_intrusion.run_model_v2 import single_token_candidates


ITEM = {
    "item_id": "x", "dam_id": "d", "cell": "net_down__inflow_up",
    "congruence": "conflict", "start_date": "2020-01-01",
    "initial_storage_mcm": 10.0, "net_direction": "negative",
    "storage_direction": "down", "inflow_trend_direction": "up",
    "daily_flows": [
        {"date": f"2020-01-0{i}", "inflow_cumecs": float(i), "outflow_cumecs": float(i + 2)}
        for i in range(2, 8)
    ],
}


def test_v2_contract_preserves_bank_and_forbids_letter_gate():
    root = Path(__file__).resolve().parents[1]
    contract = json.loads((root / "configs" / "d0_v2_contract.json").read_text())
    assert contract["bank_items"] == 600
    assert contract["items_per_cell"] == 150
    assert contract["recognition_measure"]["candidates"] == ["positive", "negative"]
    assert contract["recognition_measure"]["letter_options"] == "forbidden"
    assert "explicit_correct_net" in contract["conditions"]


def test_semantic_prompt_has_no_arbitrary_answer_letters():
    text = net_semantic_messages(ITEM, "inflow_first")[-1]["content"]
    assert "positive or negative" in text
    assert "A." not in text and "B." not in text


def test_v2_history_uses_semantic_model_answer():
    messages, _ = stock_messages_v2(
        ITEM, "actual_net_history", "inflow_first", "canonical", "negative"
    )
    assert messages[2] == {"role": "assistant", "content": "negative"}


def test_single_token_candidates_reject_multitoken_values():
    class Tokenizer:
        @staticmethod
        def encode(value, add_special_tokens=False):
            if " " in value:
                return [1, 2]
            return [{"positive": 1, "negative": 2}[value]]

    assert single_token_candidates(Tokenizer(), ("positive", "negative")) == {
        "positive": 1, "negative": 2
    }
    try:
        single_token_candidates(Tokenizer(), ("two words", "negative"))
    except ValueError as error:
        assert "not one token" in str(error)
    else:
        raise AssertionError("multi-token candidate was accepted")


def test_semantic_gate_averages_column_orders_instead_of_requiring_both():
    rows = []
    for column, p_negative in (("inflow_first", 0.9), ("outflow_first", 0.4)):
        rows.append({
            **{key: ITEM[key] for key in ("item_id", "dam_id", "cell", "congruence",
                                          "net_direction", "inflow_trend_direction")},
            "condition": "net_recognition_v2", "column_order": column,
            "gold_label": "negative", "predicted_label": "negative" if p_negative > .5 else "positive",
            "prob_positive": 1 - p_negative, "prob_negative": p_negative,
            "correct": p_negative > .5,
        })
    for condition in ("direct", "actual_net_history", "explicit_correct_net",
                      "masked_net_history", "formula_reminder"):
        for column in ("inflow_first", "outflow_first"):
            for option in ("canonical", "reversed"):
                rows.append({
                    **{key: ITEM[key] for key in ("item_id", "dam_id", "cell", "congruence",
                                                  "net_direction", "inflow_trend_direction")},
                    "condition": condition, "column_order": column, "option_order": option,
                    "prob_stock_up": .2, "correct": True,
                })
    aggregated, audit = aggregate_v2(rows)
    assert audit["gated_items"] == 1
    assert len(aggregated) == 5
