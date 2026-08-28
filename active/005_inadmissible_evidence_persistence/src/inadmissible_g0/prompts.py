from __future__ import annotations

BINARY_ORDERS = (
    {"A": "target", "B": "other"},
    {"A": "other", "B": "target"},
)

RECOGNITION_ORDERS = (
    {"A": "yes", "B": "no"},
    {"A": "no", "B": "yes"},
)

VERDICT_TEMPLATES = (
    ("natural", "Which outcome is better supported by the case record?"),
    ("rule_reminder", "Apply the evidentiary ruling before deciding. Based only on material legally available for the verdict, which outcome is better supported?"),
)


def condition_text(case_facts: str, evidence: str, ruling: str | None,
                   condition: str, exclusion_scope: str | None = None) -> str:
    if condition == "never_seen":
        return f"CASE RECORD:\n{case_facts}"
    if condition in {"admitted", "struck", "neutral_struck"}:
        scope = f"\n\nEXCLUSION SCOPE:\n{exclusion_scope}" if exclusion_scope else ""
        return f"CASE RECORD:\n{case_facts}\n\nEVIDENCE PRESENTED:\n{evidence}\n\nRULING:\n{ruling}{scope}"
    raise ValueError(condition)


def verdict_prompt(context: str, target: str, other: str, template: str,
                   mapping: dict[str, str]) -> str:
    text = {"target": target, "other": other}
    options = "\n".join(f"{lab}. {text[sem]}" for lab, sem in mapping.items())
    return f"{context}\n\n{template}\n{options}\nAnswer exactly A or B."


def recognition_prompt(case_facts: str, evidence: str, struck_ruling: str,
                       exclusion_scope: str, probe: str, mapping: dict[str, str],
                       polarity: str) -> tuple[str, str]:
    context = (
        f"CASE RECORD:\n{case_facts}\n\nEVIDENCE PRESENTED:\n{evidence}\n\n"
        f"RULING:\n{struck_ruling}\n\nEXCLUSION SCOPE:\n{exclusion_scope}"
    )
    if probe == "inadmissible":
        question = "Under the ruling, must this evidence be excluded from the verdict?"
        truth = "yes"
    elif probe == "scope":
        question = "Does the stated exclusion scope apply to the verdict question being asked?"
        truth = "yes"
    elif probe == "polarity":
        question = "Ignoring admissibility, does the evidence favor the TARGET verdict rather than the OTHER verdict?"
        truth = "yes" if polarity == "supports_target" else "no"
    else:
        raise ValueError(probe)
    options = "\n".join(
        f"{lab}. {'Yes' if sem == 'yes' else 'No'}" for lab, sem in mapping.items()
    )
    correct_label = next(lab for lab, sem in mapping.items() if sem == truth)
    return f"{context}\n\n{question}\n{options}\nAnswer exactly A or B.", correct_label
