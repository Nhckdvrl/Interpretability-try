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
    "Based only on evidence legally available for the verdict, which outcome is better supported?",
    "Apply the stated evidentiary ruling and exclusion scope, then choose the outcome supported by the usable record.",
)

def condition_text(case_facts: str, evidence: str, ruling: str | None, condition: str,
                   exclusion_scope: str | None = None) -> str:
    if condition == "never_seen":
        return f"CASE RECORD:\n{case_facts}"
    if condition in {"admitted", "struck"}:
        out = f"CASE RECORD:\n{case_facts}\n\nEVIDENCE PRESENTED:\n{evidence}\n\nRULING:\n{ruling}"
        if exclusion_scope is not None:
            out += f"\n\nEXCLUSION SCOPE:\n{exclusion_scope}"
        return out
    raise ValueError(condition)

def verdict_prompt(context: str, target: str, other: str, template: str,
                   mapping: dict[str, str]) -> str:
    text = {"target": target, "other": other}
    options = "\n".join(f"{lab}. {text[sem]}" for lab, sem in mapping.items())
    return f"{context}\n\n{template}\n{options}\nAnswer exactly A or B."

def recognition_prompt(context: str, target: str, other: str, probe: str,
                       mapping: dict[str, str], polarity: str) -> tuple[str, str]:
    verdict_frame = f"TARGET VERDICT:\n{target}\n\nOTHER VERDICT:\n{other}"
    if probe == "inadmissible":
        question = "Under the stated ruling, must the presented evidence be excluded from the verdict?"
        truth = "yes"
    elif probe == "scope":
        question = "Does the stated exclusion scope apply to the verdict question being asked?"
        truth = "yes"
    elif probe == "polarity":
        question = "Ignoring admissibility, does the presented evidence favor the TARGET verdict rather than the OTHER verdict?"
        truth = "yes" if polarity == "supports_target" else "no"
    else:
        raise ValueError(probe)
    options = "\n".join(f"{lab}. {'Yes' if sem == 'yes' else 'No'}" for lab, sem in mapping.items())
    correct_label = next(lab for lab, sem in mapping.items() if sem == truth)
    return f"{context}\n\n{verdict_frame}\n\n{question}\n{options}\nAnswer exactly A or B.", correct_label
