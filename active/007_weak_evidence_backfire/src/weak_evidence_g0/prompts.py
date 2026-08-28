from __future__ import annotations

YES_NO_ORDERS = (
    {"A": "yes", "B": "no"},
    {"A": "no", "B": "yes"},
)
CHOICE_ORDERS = (
    {"A": "target", "B": "other"},
    {"A": "other", "B": "target"},
)
DIRECTIONS = ("supports_target", "supports_other")
CONDITIONS = (
    "no_evidence",
    "weak",
    "strong",
    "neutral",
    "no_evidence_complete",
    "weak_complete",
    "no_evidence_length",
    "weak_length",
)
READOUT_TEMPLATES = (
    ("belief", "Based on the information available, which hypothesis is better supported?"),
    ("belief", "If you must choose the more plausible explanation from these two, which one should receive more weight?"),
    ("action", "The two follow-up actions have equal cost and equal downside if wrong. Which action should receive priority based only on which hypothesis is more likely?"),
    ("action", "With equal action costs and no other considerations, which hypothesis-linked follow-up should you choose first?"),
)


def natural_base_context(background: str) -> str:
    return f"BACKGROUND:\n{background}"


def calibrated_context(background: str, calibration_text: str) -> str:
    return f"BACKGROUND:\n{background}\n\nCALIBRATION:\n{calibration_text}"


def evidence_for_direction(*, direction: str, weak_target: str, weak_other: str,
                           strong_target: str, strong_other: str) -> tuple[str, str]:
    if direction == "supports_target":
        return weak_target, strong_target
    if direction == "supports_other":
        return weak_other, strong_other
    raise ValueError(f"unknown direction={direction}")


def condition_context(*, base: str, weak_evidence: str, strong_evidence: str, neutral_evidence: str,
                      pragmatic_text: str, length_control_text: str, condition: str) -> str:
    if condition == "no_evidence":
        return base
    if condition == "weak":
        return f"{base}\n\nOBSERVATION:\n{weak_evidence}"
    if condition == "strong":
        return f"{base}\n\nOBSERVATION:\n{strong_evidence}"
    if condition == "neutral":
        return f"{base}\n\nOBSERVATION:\n{neutral_evidence}"
    if condition == "no_evidence_complete":
        return f"{base}\n\nREPORTING PROTOCOL:\n{pragmatic_text}"
    if condition == "weak_complete":
        return f"{base}\n\nOBSERVATION:\n{weak_evidence}\n\nREPORTING PROTOCOL:\n{pragmatic_text}"
    if condition == "no_evidence_length":
        return f"{base}\n\nREPORTING NOTE:\n{length_control_text}"
    if condition == "weak_length":
        return f"{base}\n\nOBSERVATION:\n{weak_evidence}\n\nREPORTING NOTE:\n{length_control_text}"
    raise ValueError(f"unknown condition={condition}")


def support_prompt(*, base: str, evidence: str, focal_hypothesis: str, other_hypothesis: str,
                   probe: str, mapping: dict[str, str], pragmatic_text: str | None = None) -> tuple[str, str]:
    context = f"{base}\n\nOBSERVATION:\n{evidence}"
    if probe == "support_complete":
        if not pragmatic_text:
            raise ValueError("support_complete requires pragmatic_text")
        context += f"\n\nREPORTING PROTOCOL:\n{pragmatic_text}"
        question = (
            f"Under this reporting protocol, does the observation itself still increase support for '{focal_hypothesis}' "
            f"relative to '{other_hypothesis}', compared with the same protocol and no observation?"
        )
        truth = "yes"
    elif probe == "support":
        question = (
            f"In this situation, does this observation by itself increase support for '{focal_hypothesis}' "
            f"relative to '{other_hypothesis}', compared with seeing no observation?"
        )
        truth = "yes"
    elif probe == "likelihood_relation":
        question = (
            f"According to the calibration, is this observation more expected when '{focal_hypothesis}' is true "
            f"than when '{other_hypothesis}' is true?"
        )
        truth = "yes"
    else:
        raise ValueError(f"unknown support probe={probe}")
    options = "\n".join(f"{lab}. {'Yes' if sem == 'yes' else 'No'}" for lab, sem in mapping.items())
    correct = next(lab for lab, sem in mapping.items() if sem == truth)
    return f"{context}\n\n{question}\n{options}\nAnswer exactly A or B.", correct


def choice_prompt(*, context: str, target_hypothesis: str, other_hypothesis: str,
                  target_action: str, other_action: str, template_kind: str, template: str,
                  mapping: dict[str, str]) -> tuple[str, str]:
    if template_kind == "belief":
        text = {"target": target_hypothesis, "other": other_hypothesis}
    elif template_kind == "action":
        text = {"target": target_action, "other": other_action}
    else:
        raise ValueError(f"unknown template_kind={template_kind}")
    options = "\n".join(f"{lab}. {text[sem]}" for lab, sem in mapping.items())
    target_label = next(lab for lab, sem in mapping.items() if sem == "target")
    return f"{context}\n\n{template}\n{options}\nAnswer exactly A or B.", target_label
