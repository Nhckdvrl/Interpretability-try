from __future__ import annotations
from itertools import permutations
from typing import Iterable

LABELS = ("A", "B", "C")
SEMANTICS = ("left_more", "equal", "right_more")
LABEL_ORDERS = tuple(dict(zip(LABELS, order)) for order in permutations(SEMANTICS))

PROBABILITY_TEMPLATES = (
    "Compare the probability of the two event descriptions. Do not use wording length as evidence.",
    "Treat the descriptions extensionally: compare only which worlds make each event true.",
)
DECISION_TEMPLATES = (
    "Two contracts each pay $100 exactly when their described event occurs. Which contract is worth more, ignoring presentation style?",
    "Suppose two fair bets have the same payoff and differ only in the described triggering event. Which should command a higher price?",
)

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
        "left_more": "the LEFT description should receive the higher probability/value",
        "equal": "they should receive the SAME probability/value",
        "right_more": "the RIGHT description should receive the higher probability/value",
    }
    options = "\n".join(f"{lab}. {semantic_text[mapping[lab]]}" for lab in LABELS)
    return (
        f"{instruction}\n\nLEFT:\n{left}\n\nRIGHT:\n{right}\n\n"
        f"{options}\nAnswer exactly one letter: A, B, or C."
    )

def partial_text(branches: tuple[str, ...]) -> str:
    kept = branches[:-1]
    return " or ".join(f"({x})" for x in kept)
