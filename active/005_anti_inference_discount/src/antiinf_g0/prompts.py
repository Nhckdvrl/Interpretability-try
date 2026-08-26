from __future__ import annotations

from typing import TypeAlias
from .dataset import Scenario

ChatPrompt: TypeAlias = tuple[tuple[str,str], ...]

COMPREHENSION_TEMPLATES=(
    "{context}\n\nEvidence:\n{evidence}\n\nCritical fact: {critical_fact}\n\nDoes the evidence establish the critical fact under the stated assumptions? Answer exactly Yes or No.",
    "Use only the rule and record below.\n\n{context}\n\nRecord:\n{evidence}\n\nQuestion: Is this statement supported?\n{critical_fact}\n\nReturn only Yes or No.",
)
JUDGMENT_TEMPLATES=(
    "Given your previous answer, which conclusion is warranted under the stated rule?\nA. {a}\nB. {b}\n\nAnswer exactly A or B.",
    "Using the fact you just confirmed, choose the conclusion supported by the stated rule.\nA. {a}\nB. {b}\n\nReturn only A or B.",
)


def evidence_for(s:Scenario,mode:str)->str:
    if mode=="direct": return s.direct_evidence
    if mode=="inference": return s.inference_evidence
    raise ValueError(f"unknown evidence mode {mode!r}")


def comprehension_user_text(s:Scenario,mode:str,template_id:int)->str:
    try: template=COMPREHENSION_TEMPLATES[template_id]
    except IndexError as e: raise ValueError(f"unknown comprehension template_id={template_id}") from e
    return template.format(context=s.context,evidence=evidence_for(s,mode),critical_fact=s.critical_fact)


def build_comprehension_prompt(s:Scenario,mode:str,template_id:int)->ChatPrompt:
    return (("user",comprehension_user_text(s,mode,template_id)),)


def build_judgment_prompt(s:Scenario,mode:str,comprehension_template_id:int,judgment_template_id:int,label_order:int)->tuple[ChatPrompt,str]:
    try: template=JUDGMENT_TEMPLATES[judgment_template_id]
    except IndexError as e: raise ValueError(f"unknown judgment template_id={judgment_template_id}") from e
    if label_order==0: a,b,target=s.target_conclusion,s.alternative_conclusion,"A"
    elif label_order==1: a,b,target=s.alternative_conclusion,s.target_conclusion,"B"
    else: raise ValueError(f"unknown label_order={label_order}")
    history=(("user",comprehension_user_text(s,mode,comprehension_template_id)),("assistant","Yes"),("user",template.format(a=a,b=b)))
    return history,target
