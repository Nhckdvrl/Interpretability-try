from __future__ import annotations

DIRECTIONS = ("supports_target", "supports_other")
YES_NO_ORDERS = (
    {"A": "yes", "B": "no"},
    {"A": "no", "B": "yes"},
)
CHOICE_ORDERS = (
    {"A": "target", "B": "other"},
    {"A": "other", "B": "target"},
)
READOUT_TEMPLATES = (
    ("belief", "Which hypothesis is better supported by the record as it stands?"),
    ("belief", "Based only on the available information, which explanation is more plausible?"),
    ("action", "Which action is better justified by the record as it stands?"),
    ("action", "Given only the information above, which action should be preferred?"),
)
CONDITIONS = (
    "no_evidence", "weak", "strong", "neutral",
    "no_evidence_complete", "weak_complete", "no_evidence_length", "weak_length",
)


def base_text(background: str, calibration: str, protocol: str | None = None) -> str:
    text = f"BACKGROUND:\n{background}\n\nCALIBRATION:\n{calibration}"
    if protocol:
        text += f"\n\nREPORTING PROTOCOL:\n{protocol}"
    return text


def evidence_for(scenario, direction: str, strength: str) -> str:
    if direction == "supports_target":
        return scenario.weak_target_evidence if strength == "weak" else scenario.strong_target_evidence
    if direction == "supports_other":
        return scenario.weak_other_evidence if strength == "weak" else scenario.strong_other_evidence
    raise ValueError(direction)


def condition_text(scenario, *, direction: str, condition: str) -> str:
    if condition in {"no_evidence_complete", "weak_complete"}:
        protocol = scenario.pragmatic_completeness_text
    elif condition in {"no_evidence_length", "weak_length"}:
        protocol = scenario.matched_length_control_text
    else:
        protocol = None
    base = base_text(scenario.background, scenario.calibration_text, protocol)
    if condition in {"no_evidence", "no_evidence_complete", "no_evidence_length"}:
        return base
    if condition in {"weak", "weak_complete", "weak_length"}:
        evidence = evidence_for(scenario, direction, "weak")
    elif condition == "strong":
        evidence = evidence_for(scenario, direction, "strong")
    elif condition == "neutral":
        evidence = scenario.neutral_evidence
    else:
        raise ValueError(condition)
    return base + f"\n\nOBSERVATION:\n{evidence}"


def support_prompt(*, base: str, weak_evidence: str, strong_evidence: str, neutral_evidence: str,
                   focal_hypothesis: str, other_hypothesis: str, probe: str,
                   mapping: dict[str, str], pragmatic_text: str) -> tuple[str, str]:
    if probe == "support":
        evidence_block = f"OBSERVATION:\n{weak_evidence}"
        question = f"Relative to the same background without this observation, does it provide genuine positive evidence for {focal_hypothesis}?"
    elif probe == "likelihood_relation":
        evidence_block = f"OBSERVATION:\n{weak_evidence}"
        question = f"According to the stated calibration, is this observation more likely if {focal_hypothesis} is true than if {other_hypothesis} is true?"
    elif probe == "support_complete":
        evidence_block = f"REPORTING PROTOCOL:\n{pragmatic_text}\n\nOBSERVATION:\n{weak_evidence}"
        question = f"Under that reporting protocol, does this observation still provide genuine positive evidence for {focal_hypothesis}?"
    elif probe == "strong_support":
        evidence_block = f"OBSERVATION:\n{strong_evidence}"
        question = f"Does this observation provide genuine positive evidence for {focal_hypothesis}?"
    elif probe == "strong_gt_weak":
        evidence_block = f"OBSERVATION 1:\n{weak_evidence}\n\nOBSERVATION 2:\n{strong_evidence}"
        question = f"According to the stated calibration, is OBSERVATION 2 more diagnostic in favor of {focal_hypothesis} than OBSERVATION 1?"
    elif probe == "neutral_non_support":
        evidence_block = f"OBSERVATION:\n{neutral_evidence}"
        question = (
            f"According to the stated calibration, is this observation approximately non-diagnostic between "
            f"{focal_hypothesis} and {other_hypothesis}, with nearly equal class-conditional rates?"
        )
    else:
        raise ValueError(probe)
    options = "\n".join(f"{lab}. {'Yes' if sem == 'yes' else 'No'}" for lab, sem in mapping.items())
    correct = next(lab for lab, sem in mapping.items() if sem == "yes")
    return (
        f"{base}\n\nFOCAL HYPOTHESIS: {focal_hypothesis}\nOTHER HYPOTHESIS: {other_hypothesis}\n\n"
        f"{evidence_block}\n\n{question}\n{options}\nAnswer exactly A or B.", correct,
    )


def readout_prompt(*, context: str, target_text: str, other_text: str,
                   template: str, mapping: dict[str, str]) -> tuple[str, str]:
    text = {"target": target_text, "other": other_text}
    options = "\n".join(f"{lab}. {text[sem]}" for lab, sem in mapping.items())
    target_label = next(lab for lab, sem in mapping.items() if sem == "target")
    return f"{context}\n\n{template}\n{options}\nAnswer exactly A or B.", target_label
