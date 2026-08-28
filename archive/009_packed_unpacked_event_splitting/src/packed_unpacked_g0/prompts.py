from __future__ import annotations
from itertools import permutations
from typing import Iterable

LABELS = ("A", "B", "C")
SEMANTICS = ("left_more", "equal", "right_more")
LABEL_ORDERS = tuple(dict(zip(LABELS, order)) for order in permutations(SEMANTICS))

READOUT_TEMPLATES = {
    "probability": (
        ("natural", "Considering the situation described, compare the probability of the two events."),
        ("natural", "Without adding any extra assumptions, which of the two events is more likely in this situation?"),
        ("extensional_reminder", "Compare only the sets of possible worlds in which each event occurs; logically equivalent events should receive the same probability."),
    ),
    "decision": (
        ("natural", "Two contracts each pay $100 exactly when the event written on that contract occurs. Which contract is worth more?"),
        ("natural", "The two bets have identical payoffs and differ only in the event that triggers payment. Which should have the higher fair price?"),
        ("extensional_reminder", "Two equal-payoff contracts should have equal value whenever their triggering events are logically equivalent. Compare the two contracts on that basis."),
    ),
    "frequency": (
        ("natural", "Imagine many comparable repetitions of the situation. Which event would occur more often?"),
        ("natural", "Across many repetitions under the same conditions, compare how often the two events would occur."),
        ("extensional_reminder", "Across repeated comparable situations, logically equivalent events must occur equally often. Compare the two event descriptions on that basis."),
    ),
}

SEMANTIC_TEXT = {
    "probability": {
        "left_more": "the LEFT event is more probable",
        "equal": "the two events are equally probable",
        "right_more": "the RIGHT event is more probable",
    },
    "decision": {
        "left_more": "the LEFT contract/bet has higher value",
        "equal": "the two contracts/bets have equal value",
        "right_more": "the RIGHT contract/bet has higher value",
    },
    "frequency": {
        "left_more": "the LEFT event would occur more often",
        "equal": "the two events would occur equally often",
        "right_more": "the RIGHT event would occur more often",
    },
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
    return f"Packed event:\n{packed}\n\nBranches:\n{branch_text}\n\n{q}\nAnswer exactly one letter: {label_yes}=Yes, {label_no}=No."

def pair_relation_prompt(focal: str, complement: str, probe: str, label_yes: str, label_no: str) -> str:
    if probe == "disjoint":
        q = "Are these two events mutually exclusive, so they cannot both occur?"
    elif probe == "exhaustive":
        q = "Do these two events together exhaust the relevant outcome space for this question?"
    else:
        raise ValueError(probe)
    return f"EVENT 1:\n{focal}\n\nEVENT 2:\n{complement}\n\n{q}\nAnswer exactly one letter: {label_yes}=Yes, {label_no}=No."

def comparison_prompt(left: str, right: str, instruction: str, mapping: dict[str, str], readout: str) -> str:
    semantic_text = SEMANTIC_TEXT[readout]
    options = "\n".join(f"{lab}. {semantic_text[mapping[lab]]}" for lab in LABELS)
    return f"{instruction}\n\nLEFT:\n{left}\n\nRIGHT:\n{right}\n\n{options}\nAnswer exactly one letter: A, B, or C."
