import math

from stock_flow_intrusion.analyze import (
    attraction,
    cluster_bootstrap,
    json_safe,
    recognition_diagnostics,
)


def test_attraction_controls_net_direction():
    rows = []
    for net in ("positive", "negative"):
        for inflow, value in (("up", .8), ("down", .2)):
            rows.append({"net_direction": net, "inflow_trend_direction": inflow,
                         "prob_stock_up": value})
    assert abs(attraction(rows) - .6) < 1e-9


def test_empty_stratum_is_reported_not_crashed():
    result = cluster_bootstrap([], attraction, 10, 1)
    assert result["n_items"] == 0 and math.isnan(result["estimate"])


def test_json_safe_replaces_nonfinite_values_recursively():
    value = {"estimate": float("nan"), "nested": [1.0, float("inf")]}
    assert json_safe(value) == {"estimate": None, "nested": [1.0, None]}


def test_recognition_diagnostics_splits_presentation_factors():
    rows = []
    for column in ("inflow_first", "outflow_first"):
        for option in ("canonical", "reversed"):
            rows.append({
                "condition": "net_recognition",
                "cell": "net_down__inflow_up",
                "column_order": column,
                "option_order": option,
                "correct": option == "canonical",
            })
    result = recognition_diagnostics(rows)["net_down__inflow_up"]
    assert result["overall"] == 0.5
    assert result["presentations"]["inflow_first__canonical"] == 1.0
    assert result["presentations"]["outflow_first__reversed"] == 0.0
