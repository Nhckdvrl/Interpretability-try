from __future__ import annotations
from typing import Iterable

RECOGNITION_ORDERS = (
    {"A": "yes", "B": "no"},
    {"A": "no", "B": "yes"},
)

PROBABILITY_TEMPLATES = (
    "Use only the stated information set. Estimate the event probability, not how detailed or vivid its wording is.",
    "Judge the event from the information available at the stated time. Description length and number of listed branches are not evidence.",
)

DECISION_TEMPLATES = (
    "A risk-neutral contract pays $100 exactly if the event occurs. Judge its fair price from the stated information only.",
    "Treat this as a fair-value question for a $100 event contract; presentation style must not change value.",
)

def _binary_options(mapping: dict[str, str]) -> tuple[str, str]:
    options = "\n".join(f"{lab}. {'Yes' if sem == 'yes' else 'No'}" for lab, sem in mapping.items())
    correct_yes = next(lab for lab, sem in mapping.items() if sem == "yes")
    return options, correct_yes

def recognition_prompt(packed: str, branches: Iterable[str], probe: str, mapping: dict[str, str], *, partial_text: str | None = None) -> tuple[str, str]:
    branch_text = "\n".join(f"- {b}" for b in branches)
    if probe == "equivalent":
        q = "Do the packed event and the union of ALL listed branches denote exactly the same event?"
        body = f"Packed event:\n{packed}\n\nBranches:\n{branch_text}"
    elif probe == "disjoint":
        q = "Are the listed branches mutually exclusive, so at most one can occur?"
        body = f"Packed event:\n{packed}\n\nBranches:\n{branch_text}"
    elif probe == "exhaustive":
        q = "Do the listed branches exhaust the packed event, so every packed-event outcome is in one listed branch?"
        body = f"Packed event:\n{packed}\n\nBranches:\n{branch_text}"
    elif probe == "partial_strict_subset":
        if partial_text is None:
            raise ValueError("partial_text is required for partial_strict_subset")
        q = "Is the PARTIAL event a strict subset of the PACKED event, rather than an equivalent description?"
        body = f"PACKED event:\n{packed}\n\nPARTIAL event:\n{partial_text}"
    else:
        raise ValueError(probe)
    options, correct = _binary_options(mapping)
    return f"{body}\n\n{q}\n{options}\nAnswer exactly A or B.", correct

def threshold_prompt(information_context: str, event_text: str, readout: str, threshold: float, template: str, mapping: dict[str, str], *, alternative_text: str | None = None) -> tuple[str, str]:
    if readout == "probability":
        q = f"Is the probability of the FOCAL event at least {100.0 * threshold:g}%?"
    elif readout == "decision":
        q = f"Is the fair price of the FOCAL $100 event contract at least ${threshold:g}?"
    else:
        raise ValueError(readout)

    if alternative_text is None:
        frame = f"FOCAL EVENT:\n{event_text}"
    else:
        frame = (
            f"FOCAL EVENT:\n{event_text}\n\nALTERNATIVE OUTCOME DESCRIPTION:\n{alternative_text}\n\n"
            "The focal event and the alternative outcome exhaust the relevant outcome space."
        )
    options, correct = _binary_options(mapping)
    return (
        f"INFORMATION AVAILABLE:\n{information_context}\n\n{frame}\n\n{template}\n{q}\n"
        f"{options}\nAnswer exactly A or B."
    ), correct
