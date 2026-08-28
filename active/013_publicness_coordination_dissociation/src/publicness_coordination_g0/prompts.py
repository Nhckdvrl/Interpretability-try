from __future__ import annotations

PARTICIPANTS = ("a", "b")
YES_NO_ORDERS = (
    {"A": "yes", "B": "no"},
    {"A": "no", "B": "yes"},
)
ACTION_ORDERS = (
    {"A": "coordinate", "B": "safe"},
    {"A": "safe", "B": "coordinate"},
)
ACTION_TEMPLATES = (
    "From {participant}'s perspective, which action is better justified by what {participant} can know?",
    "Given only the information available to {participant}, which action should {participant} prefer?",
)
VERSIONS = ("primary", "paraphrase", "length")
CONDITIONS = tuple(f"{state}_{version}" for version in VERSIONS for state in ("private", "public", "explicit_ck"))
CAPABILITY_PROBES = (
    "self_knows_proposition",
    "other_knows_proposition_world",
    "event_publicly_observable",
    "knows_other_received",
    "knows_other_knows_self_received",
    "knows_other_knows_self_knows_other_received",
)


def participant_name(s, who: str) -> str:
    if who == "a": return s.participant_a
    if who == "b": return s.participant_b
    raise ValueError(who)


def other_name(s, who: str) -> str:
    return s.participant_b if who == "a" else s.participant_a


def event_for(s, state: str, version: str) -> str:
    table = {
        ("private", "primary"): s.private_event_text,
        ("public", "primary"): s.public_event_text,
        ("explicit_ck", "primary"): s.explicit_ck_text,
        ("private", "paraphrase"): s.private_paraphrase_text,
        ("public", "paraphrase"): s.public_paraphrase_text,
        ("explicit_ck", "paraphrase"): s.explicit_ck_paraphrase_text,
        ("private", "length"): s.private_length_text,
        ("public", "length"): s.public_length_text,
        ("explicit_ck", "length"): s.explicit_ck_length_text,
    }
    return table[(state, version)]


def context_text(s, *, state: str, version: str) -> str:
    return (
        f"BACKGROUND:\n{s.background}\n\n"
        f"PROPOSITION:\n{s.proposition}\n\n"
        f"INFORMATION EVENT:\n{event_for(s, state, version)}"
    )


def yes_no_options(mapping: dict[str, str], *, expected: str) -> tuple[str, str]:
    options = "\n".join(f"{lab}. {'Yes' if sem == 'yes' else 'No'}" for lab, sem in mapping.items())
    correct = next(lab for lab, sem in mapping.items() if sem == expected)
    return options, correct


def capability_prompt(s, *, who: str, state: str, probe: str,
                      mapping: dict[str, str]) -> tuple[str, str]:
    if state not in {"private", "public"}:
        raise ValueError(state)
    me, other = participant_name(s, who), other_name(s, who)
    context = context_text(s, state=state, version="primary")
    if probe == "self_knows_proposition":
        q, expected = f"In the described world, does {me} know the proposition?", "yes"
    elif probe == "other_knows_proposition_world":
        q, expected = f"In the described world, does {other} know the proposition?", "yes"
    elif probe == "event_publicly_observable":
        q, expected = f"From {me}'s perspective, was the information event itself observable to both participants?", "yes" if state == "public" else "no"
    elif probe == "knows_other_received":
        q, expected = f"Can {me} know from the information structure that {other} received the proposition?", "yes" if state == "public" else "no"
    elif probe == "knows_other_knows_self_received":
        q, expected = f"Can {me} know from the information structure that {other} knows that {me} received the proposition?", "yes" if state == "public" else "no"
    elif probe == "knows_other_knows_self_knows_other_received":
        q, expected = f"Can {me} know from the information structure that {other} knows that {me} knows that {other} received the proposition?", "yes" if state == "public" else "no"
    else:
        raise ValueError(probe)
    options, correct = yes_no_options(mapping, expected=expected)
    return f"{context}\n\n{q}\n{options}\nAnswer exactly A or B.", correct


def action_texts(s, who: str) -> tuple[str, str]:
    if who == "a": return s.coordinate_action_a, s.safe_action_a
    if who == "b": return s.coordinate_action_b, s.safe_action_b
    raise ValueError(who)


def action_prompt(s, *, who: str, state: str, version: str, template: str,
                  mapping: dict[str, str]) -> tuple[str, str]:
    me = participant_name(s, who)
    context = context_text(s, state=state, version=version)
    coordinate, safe = action_texts(s, who)
    text = {"coordinate": coordinate, "safe": safe}
    options = "\n".join(f"{lab}. {text[sem]}" for lab, sem in mapping.items())
    correct = next(lab for lab, sem in mapping.items() if sem == "coordinate")
    question = template.format(participant=me)
    return f"{context}\n\n{question}\n{options}\nAnswer exactly A or B.", correct
