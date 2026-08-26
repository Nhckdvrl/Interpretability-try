from __future__ import annotations

from typing import TypeAlias
from .dataset import Scenario

ChatPrompt: TypeAlias = tuple[tuple[str,str], ...]

COMPREHENSION_TEMPLATES=(
    "{context}\n\nEvidence:\n{evidence}\n\nCritical fact: {critical_fact}\n\nDoes the evidence establish the critical fact under the stated assumptions? Answer exactly Yes or No.",
    "Use only the rule and record below.\n\n{context}\n\nRecord:\n{evidence}\n\nQuestion: Is this statement supported?\n{critical_fact}\n\nReturn only Yes or No.",
)
NATURAL_JUDGMENT_TEMPLATES=(
    "{context}\n\nEvidence:\n{evidence}\n\nWhich conclusion is warranted under the stated rule?\nA. {a}\nB. {b}\n\nAnswer exactly A or B.",
    "Apply the stated rule to the record without adding outside assumptions.\n\n{context}\n\nRecord:\n{evidence}\n\nChoose the supported conclusion:\nA. {a}\nB. {b}\n\nReturn only A or B.",
)
BRIDGED_JUDGMENT_TEMPLATES=(
    "Given your previous answer, which conclusion is warranted under the stated rule?\nA. {a}\nB. {b}\n\nAnswer exactly A or B.",
    "Using the fact you just confirmed, choose the conclusion supported by the stated rule.\nA. {a}\nB. {b}\n\nReturn only A or B.",
)


def evidence_for(s:Scenario,mode:str)->str:
    if mode=="direct": return s.direct_evidence
    if mode=="inference": return s.inference_evidence
    raise ValueError(f"unknown evidence mode {mode!r}")


def _labels(s:Scenario,label_order:int)->tuple[str,str,str]:
    if label_order==0: return s.target_conclusion,s.alternative_conclusion,"A"
    if label_order==1: return s.alternative_conclusion,s.target_conclusion,"B"
    raise ValueError(f"unknown label_order={label_order}")


def comprehension_user_text(s:Scenario,mode:str,template_id:int)->str:
    try: template=COMPREHENSION_TEMPLATES[template_id]
    except IndexError as e: raise ValueError(f"unknown comprehension template_id={template_id}") from e
    return template.format(context=s.context,evidence=evidence_for(s,mode),critical_fact=s.critical_fact)


def build_comprehension_prompt(s:Scenario,mode:str,template_id:int)->ChatPrompt:
    return (("user",comprehension_user_text(s,mode,template_id)),)


def build_natural_judgment_prompt(s:Scenario,mode:str,template_id:int,label_order:int)->tuple[ChatPrompt,str]:
    try: template=NATURAL_JUDGMENT_TEMPLATES[template_id]
    except IndexError as e: raise ValueError(f"unknown natural judgment template_id={template_id}") from e
    a,b,target=_labels(s,label_order)
    return (("user",template.format(context=s.context,evidence=evidence_for(s,mode),a=a,b=b)),),target


def build_bridged_judgment_prompt(s:Scenario,mode:str,comprehension_template_id:int,judgment_template_id:int,label_order:int)->tuple[ChatPrompt,str]:
    try: template=BRIDGED_JUDGMENT_TEMPLATES[judgment_template_id]
    except IndexError as e: raise ValueError(f"unknown bridged judgment template_id={judgment_template_id}") from e
    a,b,target=_labels(s,label_order)
    history=(("user",comprehension_user_text(s,mode,comprehension_template_id)),("assistant","Yes"),("user",template.format(a=a,b=b)))
    return history,target
