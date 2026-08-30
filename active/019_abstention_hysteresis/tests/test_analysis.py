from abstention_hysteresis.analyze import bootstrap_mean, gated_items, paired_records


def test_gate_and_pairing_are_item_local():
    rows = [
        {"item_id": "x", "source": "s", "condition": "capability_full", "correct": True},
        {"item_id": "x", "source": "s", "condition": "initial_missing", "is_abstention": True},
        {"item_id": "x", "source": "s", "condition": "direct_full", "is_abstention": False,
         "prob_abstain_mode": .1, "correct": True},
        {"item_id": "x", "source": "s", "condition": "self_abstention", "is_abstention": True,
         "prob_abstain_mode": .8, "correct": False},
    ]
    gate = gated_items(rows)
    assert gate == {"x"}
    paired = paired_records(rows, gate, "self_abstention")
    assert paired[0]["abstention_delta"] == 1.0
    assert abs(paired[0]["probability_delta"] - .7) < 1e-9


def test_bootstrap_mean_reports_estimate():
    result = bootstrap_mean([{"x": 0.0}, {"x": 1.0}], "x", 100, 1)
    assert result["estimate"] == .5 and result["n_items"] == 2
