from __future__ import annotations

from typing import Any


CONDITIONS = ("direct", "ambiguity_history", "matched_history", "wrong_condition")
ORDERS = ("target_first", "target_second")


def options_for(pair: dict[str, Any], order: str) -> tuple[str, str, str, str]:
    if order == "target_first":
        return pair["target_answer"], pair["distractor_answer"], "A", "B"
    if order == "target_second":
        return pair["distractor_answer"], pair["target_answer"], "B", "A"
    raise ValueError(f"Unknown answer order: {order}")


def choice_block(condition: str, answer_a: str, answer_b: str) -> str:
    return (
        f"Clarification: {condition}\n\n"
        "Choose the answer that matches the clarified question.\n"
        f"A. {answer_a}\n"
        f"B. {answer_b}\n\n"
        "Answer:"
    )


def build_messages(
    pair: dict[str, Any], condition: str, order: str, contract: dict[str, Any]
) -> tuple[list[dict[str, str]], str]:
    if condition not in CONDITIONS:
        raise ValueError(f"Unknown condition: {condition}")
    answer_a, answer_b, target_label, distractor_label = options_for(pair, order)
    resolving_condition = (
        pair["distractor_condition"] if condition == "wrong_condition" else pair["target_condition"]
    )
    block = choice_block(resolving_condition, answer_a, answer_b)
    system = {"role": "system", "content": contract["prompts"]["system"]}
    if condition in {"direct", "wrong_condition"}:
        messages = [
            system,
            {"role": "user", "content": f"Question: {pair['question']}\n\n{block}"},
        ]
    else:
        assistant_key = (
            "ambiguity_assistant" if condition == "ambiguity_history" else "matched_assistant"
        )
        messages = [
            system,
            {"role": "user", "content": pair["question"]},
            {"role": "assistant", "content": contract["prompts"][assistant_key]},
            {"role": "user", "content": block},
        ]
    gold_label = distractor_label if condition == "wrong_condition" else target_label
    return messages, gold_label
