from cross_modal_inertia.analyze import analyze_family, gated_rows


def make_rows(actual="A", ordinal="A", matched="B"):
    rows = []
    for item in range(60):
        base = {"item_id": str(item), "order": "canonical", "pair_id": str(item // 2),
                "language": 1, "gold_letter": "B", "prob_gold": 0.2}
        values = {
            "text_only": ("A", .2), "simultaneous": ("B", .9),
            "text_first_actual_label": (actual, .3),
            "text_first_actual_ordinal": (ordinal, .3),
            "text_first_masked": (matched, .8), "matched_history": (matched, .8),
            "image_first": ("B", .9),
        }
        for condition, (pred, prob) in values.items():
            rows.append({**base, "condition": condition, "pred_letter": pred, "prob_gold": prob})
    return rows


def test_gate_requires_initial_wrong_and_simultaneous_correct():
    gate, audit = gated_rows(make_rows())
    assert len(gate) == 60 and audit["missing"] == []


def test_synthetic_clear_inertia_promotes_family():
    result = analyze_family(make_rows(), replicates=200, seed=3)
    assert result["promotion"]
    assert result["actual_minus_matched_persistence"]["estimate"] == 1.0
