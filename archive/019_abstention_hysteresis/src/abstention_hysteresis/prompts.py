"""Conversation construction with verbatim-equivalent final user payloads."""
from __future__ import annotations


FINAL_SYSTEM = (
    "Use only evidence in this conversation. Never rely on outside knowledge or guess. "
    "If the evidence determines the answer, reply on one line as ANSWER: <short answer>. "
    "Otherwise reply on one line as ABSTAIN: <brief reason>."
)

CAPABILITY_SYSTEM = (
    "Use only the supplied evidence to answer the question. Reply with only the short answer, "
    "without explanation. If the evidence is insufficient, reply ABSTAIN."
)

TEACHER_ABSTENTION = "ABSTAIN: The supplied evidence does not determine the answer."
PARAPHRASED_ABSTENTION = "I do not yet have enough evidence to determine this."
NEUTRAL_HISTORY = "I have reviewed the partial material and am ready for the updated evidence."


def evidence_text(paragraphs: list[dict]) -> str:
    blocks = []
    for index, paragraph in enumerate(paragraphs, 1):
        blocks.append(f"[{index}] {paragraph['title']}\n{paragraph['text']}")
    return "\n\n".join(blocks)


def final_payload(item: dict) -> str:
    return (
        f"EVIDENCE\n{evidence_text(item['full_evidence'])}\n\n"
        f"QUESTION\n{item['question']}"
    )


def missing_payload(item: dict) -> str:
    return (
        f"EVIDENCE\n{evidence_text(item['incomplete_evidence'])}\n\n"
        f"QUESTION\n{item['question']}"
    )


def messages(item: dict, condition: str, self_response: str | None = None) -> list[dict]:
    complete = final_payload(item)
    incomplete = missing_payload(item)
    if condition == "capability_full":
        return [
            {"role": "system", "content": CAPABILITY_SYSTEM},
            {"role": "user", "content": complete},
        ]
    if condition == "initial_missing":
        return [
            {"role": "system", "content": FINAL_SYSTEM},
            {"role": "user", "content": incomplete},
        ]
    if condition == "direct_full":
        return [
            {"role": "system", "content": FINAL_SYSTEM},
            {"role": "user", "content": complete},
        ]

    if condition == "answered_history":
        history = [
            {"role": "user", "content": "EVIDENCE\nThe verification code is cobalt.\n\nQUESTION\nWhat is the verification code?"},
            {"role": "assistant", "content": "ANSWER: cobalt"},
        ]
    else:
        assistant = {
            "self_abstention": self_response,
            "teacher_abstention": TEACHER_ABSTENTION,
            "paraphrased_abstention": PARAPHRASED_ABSTENTION,
            "neutral_same_context": NEUTRAL_HISTORY,
        }.get(condition)
        if not assistant:
            raise ValueError(f"invalid condition or missing self response: {condition}")
        history = [
            {"role": "user", "content": incomplete},
            {"role": "assistant", "content": assistant},
        ]
    return [
        {"role": "system", "content": FINAL_SYSTEM},
        *history,
        {"role": "user", "content": complete},
    ]
