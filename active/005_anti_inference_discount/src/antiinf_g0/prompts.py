from __future__ import annotations

from .dataset import Scenario

COMPREHENSION_TEMPLATES = (
    "{context}\n\nEvidence:\n{evidence}\n\nCritical fact: {critical_fact}\n\nDoes the evidence establish the critical fact under the stated rule and record assumptions? Answer exactly Yes or No.",
    "Use only the rule and record below.\n\n{context}\n\nRecord:\n{evidence}\n\nQuestion: Is this statement supported?\n{critical_fact}\n\nReturn only Yes or No.",
)

JUDGMENT_TEMPLATES = (
    "{context}\n\nEvidence:\n{evidence}\n\nWhich conclusion is better supported under the stated rule?\nA. {a}\nB. {b}\n\nAnswer exactly A or B.",
    "Apply the stated rule to the record. Do not add outside assumptions.\n\n{context}\n\nRecord:\n{evidence}\n\nChoose the conclusion warranted by the information above:\nA. {a}\nB. {b}\n\nReturn only A or B.",
)


def evidence_for(scenario: Scenario, mode: str) -> str:
    if mode == "direct":
        return scenario.direct_evidence
    if mode == "inference":
        return scenario.inference_evidence
    raise ValueError(f"unknown evidence mode {mode!r}")


def build_comprehension_prompt(scenario: Scenario, mode: str, template_id: int) -> str:
    try:
        template = COMPREHENSION_TEMPLATES[template_id]
    except IndexError as e:
        raise ValueError(f"unknown comprehension template_id={template_id}") from e
    return template.format(
        context=scenario.context,
        evidence=evidence_for(scenario, mode),
        critical_fact=scenario.critical_fact,
    )


def build_judgment_prompt(scenario: Scenario, mode: str, template_id: int, label_order: int) -> tuple[str, str]:
    try:
        template = JUDGMENT_TEMPLATES[template_id]
    except IndexError as e:
        raise ValueError(f"unknown judgment template_id={template_id}") from e
    if label_order == 0:
        a, b = scenario.target_conclusion, scenario.alternative_conclusion
        target_label = "A"
    elif label_order == 1:
        a, b = scenario.alternative_conclusion, scenario.target_conclusion
        target_label = "B"
    else:
        raise ValueError(f"unknown label_order={label_order}")
    prompt = template.format(context=scenario.context, evidence=evidence_for(scenario, mode), a=a, b=b)
    return prompt, target_label
