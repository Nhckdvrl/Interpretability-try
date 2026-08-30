from __future__ import annotations


def ordered_options(item: dict, order: str) -> tuple[list[str], list[int]]:
    mapping = [0, 1] if order == "canonical" else [1, 0]
    return [item["options"][i] for i in mapping], mapping


def question_text(item: dict, order: str) -> str:
    options, _ = ordered_options(item, order)
    return (
        f"Context and question:\n{item['question'].strip()}\n\n"
        f"Options:\n(A) {options[0]}\n(B) {options[1]}\n\n"
        "Choose exactly one option. Reply with only A or B."
    )


def displayed_gold(item: dict, order: str) -> str:
    _, mapping = ordered_options(item, order)
    return "A" if mapping[0] == item["gold_index"] else "B"


def original_index(letter: str, order: str) -> int:
    mapping = [0, 1] if order == "canonical" else [1, 0]
    return mapping[0 if letter == "A" else 1]


def text_only_messages(item: dict, order: str) -> list[dict]:
    return [{"role": "user", "content": question_text(item, order)}]


def final_messages(item: dict, order: str, condition: str, initial_letter: str) -> list[dict]:
    text = question_text(item, order)
    image = {"type": "image", "url": item["image_path"]}
    ask = {"type": "text", "text": text}
    settle = {"type": "text", "text": "Now use the image to settle the ambiguity. Reply only A or B."}
    if condition == "simultaneous":
        return [{"role": "user", "content": [image, ask]}]
    if condition == "matched_history":
        return [
            {"role": "user", "content": "Please prepare to answer a two-option ambiguity question."},
            {"role": "assistant", "content": "I am ready to consider both possibilities."},
            {"role": "user", "content": [image, ask]},
        ]
    if condition == "image_first":
        return [
            {"role": "user", "content": [image, {"type": "text", "text": "Study this image and wait for the question."}]},
            {"role": "assistant", "content": "I have studied the image and will wait."},
            {"role": "user", "content": text},
        ]
    first = {"role": "user", "content": text}
    if condition == "text_first_actual_label":
        assistant = {"role": "assistant", "content": initial_letter}
    elif condition == "text_first_actual_ordinal":
        ordinal = "first" if initial_letter == "A" else "second"
        assistant = {"role": "assistant", "content": f"My provisional choice is the {ordinal} option."}
    elif condition == "text_first_masked":
        assistant = {"role": "assistant", "content": "I made a provisional choice, but its identity is hidden."}
    else:
        raise ValueError(condition)
    return [first, assistant, {"role": "user", "content": [image, settle]}]
