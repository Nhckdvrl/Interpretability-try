from __future__ import annotations

BINARY_ORDERS = ({"A":"target","B":"other"},{"A":"other","B":"target"})
RECOGNITION_ORDERS = ({"A":"yes","B":"no"},{"A":"no","B":"yes"})
VERDICT_TEMPLATES = (
    ("natural", "Which outcome is better supported by the case record?"),
    ("natural", "Considering the record as it now stands, which of the two outcomes has stronger support?"),
    ("rule_reminder", "Apply the evidentiary ruling before deciding. Based only on material legally available for the verdict, which outcome is better supported?"),
)

def condition_text(case_facts: str, evidence: str, ruling: str | None, condition: str, exclusion_scope: str | None=None) -> str:
    if condition=="never_seen": return f"CASE RECORD:\n{case_facts}"
    if condition in {"admitted","struck","neutral_struck"}:
        scope=f"\n\nEXCLUSION SCOPE:\n{exclusion_scope}" if exclusion_scope else ""
        return f"CASE RECORD:\n{case_facts}\n\nEVIDENCE PRESENTED:\n{evidence}\n\nRULING:\n{ruling}{scope}"
    raise ValueError(condition)

def verdict_prompt(context: str, target: str, other: str, template: str, mapping: dict[str,str]) -> str:
    text={"target":target,"other":other}; opts="\n".join(f"{lab}. {text[sem]}" for lab,sem in mapping.items())
    return f"{context}\n\n{template}\n{opts}\nAnswer exactly A or B."

def recognition_prompt(case_facts: str, evidence: str, struck_ruling: str, exclusion_scope: str,
                       target_verdict: str, other_verdict: str, probe: str,
                       mapping: dict[str,str], polarity: str) -> tuple[str,str]:
    context=(f"CASE RECORD:\n{case_facts}\n\nTARGET VERDICT:\n{target_verdict}\n\nOTHER VERDICT:\n{other_verdict}\n\n"
             f"EVIDENCE PRESENTED:\n{evidence}\n\nRULING:\n{struck_ruling}\n\nEXCLUSION SCOPE:\n{exclusion_scope}")
    if probe=="inadmissible": question="Under the ruling, must this evidence be excluded from the verdict?"; truth="yes"
    elif probe=="scope": question="Does the stated exclusion scope apply to the verdict question being asked?"; truth="yes"
    elif probe=="polarity": question="Ignoring admissibility, does the evidence favor the TARGET verdict rather than the OTHER verdict?"; truth="yes" if polarity=="supports_target" else "no"
    else: raise ValueError(probe)
    opts="\n".join(f"{lab}. {'Yes' if sem=='yes' else 'No'}" for lab,sem in mapping.items())
    correct=next(l for l,s in mapping.items() if s==truth)
    return f"{context}\n\n{question}\n{opts}\nAnswer exactly A or B.", correct
