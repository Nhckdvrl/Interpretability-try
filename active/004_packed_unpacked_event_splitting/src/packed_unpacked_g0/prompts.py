from __future__ import annotations
from itertools import permutations
from typing import Iterable

LABELS = ("A", "B", "C")
SEMANTICS = ("left_more", "equal", "right_more")
LABEL_ORDERS = tuple(dict(zip(LABELS, order)) for order in permutations(SEMANTICS))

READOUT_TEMPLATES = {
    "probability": (
        ("natural", "Considering the situation described, compare the probability of the two events."),
        ("extensional_reminder", "Compare only the sets of possible worlds in which each event occurs; logically equivalent events should receive the same probability."),
    ),
    "decision": (
        ("natural", "Two contracts each pay $100 exactly when the event written on that contract occurs. Which contract is worth more?"),
        ("extensional_reminder", "Two equal-payoff contracts should have equal value whenever their triggering events are logically equivalent. Compare the two contracts on that basis."),
    ),
}


def recognition_prompt(packed: str, branches: Iterable[str], probe: str, label_yes: str, label_no: str) -> str:
    branch_text = "\n".join(f"- {b}" for b in branches)
    if probe == "equivalent":
        q = "Do the packed event and the union of ALL listed branches denote exactly the same event?"
    elif probe == "disjoint":
        q = "Are the listed branches mutually exclusive, so at most one can occur?"
    elif probe == "exhaustive":
        q = "Do the listed branches exhaust the packed event, so every packed-event outcome is in one listed branch?"
    else:
        raise ValueError(probe)
    return (
        f"Packed event:\n{packed}\n\nBranches:\n{branch_text}\n\n{q}\n"
        f"Answer exactly one letter: {label_yes}=Yes, {label_no}=No."
    )


def comparison_prompt(left: str, right: str, instruction: str, mapping: dict[str, str]) -> str:
    semantic_text = {
        "left_more": "the LEFT event should receive the higher probability/value",
        "equal": "the two events should receive the SAME probability/value",
        "right_more": "the RIGHT event should receive the higher probability/value",
    }
    options = "\n".join(f"{lab}. {semantic_text[mapping[lab]]}" for lab in LABELS)
    return (
        f"{instruction}\n\nLEFT:\n{left}\n\nRIGHT:\n{right}\n\n"
        f"{options}\nAnswer exactly one letter: A, B, or C."
    )
