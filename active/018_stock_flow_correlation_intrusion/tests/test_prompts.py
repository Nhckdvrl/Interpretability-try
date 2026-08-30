from stock_flow_intrusion.prompts import net_messages, stock_messages, table_text


ITEM = {
    "start_date": "2020-01-01", "initial_storage_mcm": 10.0,
    "net_direction": "negative", "storage_direction": "down",
    "daily_flows": [
        {"date": f"2020-01-0{i}", "inflow_cumecs": float(i), "outflow_cumecs": float(i + 2)}
        for i in range(2, 8)
    ],
}


def test_column_order_changes_presentation_not_values():
    left = table_text(ITEM, "inflow_first")
    right = table_text(ITEM, "outflow_first")
    assert "Inflow" in left and "Outflow" in right
    assert left != right and left.count("2020-") == right.count("2020-") == 6


def test_option_counterbalance_preserves_semantics():
    _, canonical = net_messages(ITEM, "inflow_first", "canonical")
    _, reversed_map = net_messages(ITEM, "inflow_first", "reversed")
    assert canonical["negative"] == "B" and reversed_map["negative"] == "A"


def test_masked_history_hides_net_identity():
    messages, _ = stock_messages(ITEM, "masked_net_history", "inflow_first", "canonical", "negative")
    assert "negative" not in messages[2]["content"].lower()


def test_formula_condition_states_correct_relation():
    messages, _ = stock_messages(ITEM, "formula_reminder", "inflow_first", "canonical", "negative")
    assert "Storage change equals cumulative inflow minus cumulative outflow" in messages[2]["content"]
