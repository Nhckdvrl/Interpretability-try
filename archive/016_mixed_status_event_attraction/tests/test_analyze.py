import pytest

from mixed_status_attraction.analyze import aggregate_orders


def row(order):
    return {
        "pair_id": "p",
        "condition": "target_local",
        "option_order": order,
        "doc_id": "d",
        "direction": "CT+->PS+",
        "target_label": "CT+",
        "neighbor_label": "PS+",
        "has_explicit_relation": False,
        "same_sentence": False,
        "target_event_type": "A",
        "neighbor_event_type": "B",
        "label_probabilities": {"CT+": 0.8, "PS+": 0.1, "PS-": 0.03, "CT-": 0.04, "Uu": 0.03},
        "correct": True,
        "toward_neighbor": False,
    }


def test_aggregate_averages_counterbalance():
    result = aggregate_orders([row("canonical"), row("reversed")])[("p", "target_local")]
    assert result["target_probability"] == pytest.approx(0.8)
    assert result["both_correct"]


def test_aggregate_rejects_missing_order():
    with pytest.raises(ValueError, match="Missing option counterbalance"):
        aggregate_orders([row("canonical")])
