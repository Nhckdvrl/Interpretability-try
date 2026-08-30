from __future__ import annotations


def table_text(item: dict, column_order: str) -> str:
    if column_order == "inflow_first":
        columns = ("Inflow (m^3/s)", "Outflow (m^3/s)")
        keys = ("inflow_cumecs", "outflow_cumecs")
    elif column_order == "outflow_first":
        columns = ("Outflow (m^3/s)", "Inflow (m^3/s)")
        keys = ("outflow_cumecs", "inflow_cumecs")
    else:
        raise ValueError(column_order)
    lines = [f"Date | {columns[0]} | {columns[1]}", "---|---:|---:"]
    for row in item["daily_flows"]:
        lines.append(f"{row['date']} | {row[keys[0]]:.2f} | {row[keys[1]]:.2f}")
    return "\n".join(lines)


def option_block(kind: str, order: str) -> tuple[str, dict[str, str]]:
    labels = ["positive", "negative"] if kind == "net" else ["higher", "lower"]
    if order == "reversed":
        labels.reverse()
    elif order != "canonical":
        raise ValueError(order)
    mapping = {label: "AB"[index] for index, label in enumerate(labels)}
    text = "\n".join(f"{'AB'[index]}. {label.capitalize()}" for index, label in enumerate(labels))
    return text, mapping


def scenario(item: dict, column_order: str) -> str:
    return (
        f"At the end of {item['start_date']}, a reservoir held "
        f"{item['initial_storage_mcm']:.4f} million cubic meters of water. "
        "The following are the measured daily-average flow rates for the next six days.\n\n"
        f"{table_text(item, column_order)}"
    )


def net_messages(item: dict, column_order: str, option_order: str) -> tuple[list[dict], dict[str, str]]:
    options, mapping = option_block("net", option_order)
    user = (
        f"{scenario(item, column_order)}\n\n"
        "Over these six days, is cumulative inflow minus cumulative outflow positive or negative?\n\n"
        f"{options}\n\nReply with only A or B."
    )
    return [
        {"role": "system", "content": "Answer the quantitative reservoir question with exactly one option letter."},
        {"role": "user", "content": user},
    ], mapping


def stock_messages(item: dict, condition: str, column_order: str, option_order: str,
                   predicted_net: str) -> tuple[list[dict], dict[str, str]]:
    options, mapping = option_block("stock", option_order)
    stock_question = (
        "At the end of the six days, is the reservoir's storage higher or lower than its initial storage?\n\n"
        f"{options}\n\nReply with only A or B."
    )
    system = {"role": "system", "content": "Answer the quantitative reservoir question with exactly one option letter."}
    if condition == "direct":
        return [system, {"role": "user", "content": f"{scenario(item, column_order)}\n\n{stock_question}"}], mapping

    net_options, _ = option_block("net", "canonical")
    first = {
        "role": "user",
        "content": (
            f"{scenario(item, column_order)}\n\n"
            "Over these six days, is cumulative inflow minus cumulative outflow positive or negative?\n\n"
            f"{net_options}\n\nReply with only A or B."
        ),
    }
    if condition == "actual_net_history":
        assistant = f"The cumulative net flow is {predicted_net}."
    elif condition == "explicit_correct_net":
        assistant = f"The cumulative net flow is {item['net_direction']}."
    elif condition == "masked_net_history":
        assistant = "I have determined the cumulative net-flow direction."
    elif condition == "formula_reminder":
        assistant = (
            f"The cumulative net flow is {item['net_direction']}. "
            "Storage change equals cumulative inflow minus cumulative outflow."
        )
    else:
        raise ValueError(condition)
    return [system, first, {"role": "assistant", "content": assistant},
            {"role": "user", "content": stock_question}], mapping
