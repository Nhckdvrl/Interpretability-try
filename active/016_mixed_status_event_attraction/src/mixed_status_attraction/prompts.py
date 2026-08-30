from __future__ import annotations

from typing import Any


def option_mapping(contract: dict[str, Any], order: str) -> tuple[list[tuple[str, str, str]], dict[str, str]]:
    labels = list(contract["label_order"])
    if order == "reversed":
        labels.reverse()
    elif order != "canonical":
        raise ValueError(f"Unknown option order: {order}")
    letters = "ABCDE"
    options = [(letters[index], label, contract["labels"][label]) for index, label in enumerate(labels)]
    return options, {label: letter for letter, label, _ in options}


def build_messages(
    row: dict[str, Any], condition: str, option_order: str, contract: dict[str, Any]
) -> tuple[list[dict[str, str]], dict[str, str]]:
    if condition not in contract["conditions"]:
        raise ValueError(f"Unknown condition: {condition}")
    options, label_to_letter = option_mapping(contract, option_order)
    options_text = "\n".join(f"{letter}. {text}" for letter, _, text in options)
    user = (
        f"Document title: {row['title']}\n\n"
        f"Passage:\n{row[condition]}\n\n"
        "The target is the occurrence marked <TARGET_EVENT>...</TARGET_EVENT>. "
        "Classify the factuality assigned to that target occurrence by the passage's author.\n\n"
        f"{options_text}\n\nAnswer:"
    )
    messages = [
        {
            "role": "system",
            "content": "Classify only the marked target event. Reply with exactly one option letter: A, B, C, D, or E.",
        },
        {"role": "user", "content": user},
    ]
    return messages, label_to_letter
