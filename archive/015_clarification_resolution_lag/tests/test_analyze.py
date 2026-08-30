import pytest

from clarification_lag.analyze import aggregate_orders, analyze_model


def measurement(pair_id, question_id, condition, order, correct, probability=0.8):
    return {
        "pair_id": pair_id,
        "question_id": question_id,
        "property_count": 2,
        "condition": condition,
        "answer_order": order,
        "gold_label": "A" if order == "target_first" else "B",
        "gold_probability": probability,
        "correct": correct,
        "model_label": "test-model",
    }


def test_gate_requires_direct_and_wrong_correct_in_both_orders():
    rows = []
    for condition in ("direct", "ambiguity_history", "matched_history", "wrong_condition"):
        for order in ("target_first", "target_second"):
            rows.append(
                measurement(
                    "p1",
                    "q1",
                    condition,
                    order,
                    correct=condition != "ambiguity_history",
                    probability=0.9 if condition != "ambiguity_history" else 0.4,
                )
            )
    report = analyze_model(rows, replicates=100, seed=1)
    assert report["recognition_gated_pairs"] == 1
    assert report["gated_contrasts"]["direct_minus_ambiguity_accuracy"]["estimate"] == 1.0
    assert report["gated_contrasts"]["matched_minus_ambiguity_accuracy"]["estimate"] == 1.0


def test_missing_counterbalance_is_rejected():
    rows = [measurement("p1", "q1", "direct", "target_first", True)]
    with pytest.raises(ValueError, match="Missing counterbalance"):
        aggregate_orders(rows)
