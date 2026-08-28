from __future__ import annotations

SEMANTIC_ORDERS = (
    {"A": "gold", "B": "foil"},
    {"A": "foil", "B": "gold"},
)
ACTION_ORDERS = (
    {"A": "collapse", "B": "preserve"},
    {"A": "preserve", "B": "collapse"},
)
DOWNSTREAM_TEMPLATES = (
    "Which action is justified by the current record?",
    "What should the decision-maker do on the evidence currently available?",
)
CONDITIONS = (
    "unknown",
    "paraphrase",
    "same_explicit",
    "distinct_explicit",
    "neutral_control",
    "relation_reminder",
)


def base_text(premise_p: str, premise_q: str) -> str:
    return f"RECORD:\n{premise_p}\n{premise_q}"


def condition_text(*, premise_p: str, premise_q: str, premise_paraphrase: str,
                   same_addendum: str, distinct_addendum: str, neutral_addendum: str,
                   condition: str) -> str:
    base = base_text(premise_p, premise_q)
    if condition == "unknown":
        return base
    if condition == "paraphrase":
        return f"RECORD:\n{premise_paraphrase}"
    if condition == "same_explicit":
        return f"{base}\n{same_addendum}"
    if condition == "distinct_explicit":
        return f"{base}\n{distinct_addendum}"
    if condition == "neutral_control":
        return f"{base}\n{neutral_addendum}"
    if condition == "relation_reminder":
        return (
            f"{base}\n"
            "Logical note: two separate existential statements do not by themselves establish "
            "that their witnesses are the same individual."
        )
    raise ValueError(f"unknown condition={condition}")


def _recognition_options(*, p_property: str, q_property: str, probe: str) -> tuple[str, str, str]:
    """Return (question, gold_option, foil_option) without Yes/No semantics.

    Probe ids remain stable for metric compatibility, but r3 changes their surface form:
    `shared_entailment` tests that sameness is not established; `identity_determined`
    tests that distinctness is not established. Together they require both identity
    worlds to remain open in the unknown condition.
    """
    if probe == "p_exists":
        question = "Which statement about the first existential claim is supported by the record?"
        gold = f"The record establishes that at least one individual has this property: {p_property}."
        foil = f"The record does not establish that any individual has this property: {p_property}."
    elif probe == "q_exists":
        question = "Which statement about the second existential claim is supported by the record?"
        gold = f"The record establishes that at least one individual has this property: {q_property}."
        foil = f"The record does not establish that any individual has this property: {q_property}."
    elif probe == "shared_entailment":
        question = "What does the record establish about a single shared witness?"
        gold = (
            "The record does not establish that one and the same individual has both properties "
            f"({p_property}) and ({q_property}); a shared witness remains possible but unproven."
        )
        foil = (
            "The record establishes that one and the same individual has both properties "
            f"({p_property}) and ({q_property})."
        )
    elif probe == "identity_determined":
        question = "What does the record establish about the witnesses being different individuals?"
        gold = (
            "The record does not establish that the two witnesses are different individuals; "
            "both a shared-witness world and a distinct-witness world remain possible."
        )
        foil = "The record establishes that the two witnesses are different individuals."
    else:
        raise ValueError(f"unknown probe={probe}")
    return question, gold, foil


def recognition_prompt(*, premise_p: str, premise_q: str, p_property: str, q_property: str,
                       probe: str, mapping: dict[str, str]) -> tuple[str, str]:
    context = base_text(premise_p, premise_q)
    question, gold, foil = _recognition_options(
        p_property=p_property,
        q_property=q_property,
        probe=probe,
    )
    text = {"gold": gold, "foil": foil}
    options = "\n".join(f"{lab}. {text[sem]}" for lab, sem in mapping.items())
    correct = next(lab for lab, sem in mapping.items() if sem == "gold")
    return f"{context}\n\n{question}\n{options}\nAnswer exactly A or B.", correct


def downstream_prompt(*, context: str, requirement: str, decision_context: str,
                      collapse_action: str, preserve_action: str, template: str,
                      mapping: dict[str, str]) -> tuple[str, str]:
    text = {"collapse": collapse_action, "preserve": preserve_action}
    options = "\n".join(f"{lab}. {text[sem]}" for lab, sem in mapping.items())
    collapse_label = next(lab for lab, sem in mapping.items() if sem == "collapse")
    prompt = (
        f"{context}\n\nREQUIREMENT:\n{requirement}\n\nDECISION CONTEXT:\n{decision_context}\n\n"
        f"{template}\n{options}\nAnswer exactly A or B."
    )
    return prompt, collapse_label
