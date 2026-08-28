from __future__ import annotations

YES_NO_ORDERS = (
    {"A": "yes", "B": "no"},
    {"A": "no", "B": "yes"},
)
OUTCOME_ORDERS = (
    {"A": "established", "B": "not_established"},
    {"A": "not_established", "B": "established"},
)
DOWNSTREAM_TEMPLATES = (
    "On the information stated in the record, is the single-person requirement already established?",
    "Can the record safely be treated as confirming that one and the same individual satisfies both required properties?",
)
CONDITIONS = ("unknown", "paraphrase", "same_explicit", "distinct_explicit", "neutral_control", "relation_reminder")

def base_text(premise_p: str, premise_q: str) -> str: return f"RECORD:\n{premise_p}\n{premise_q}"
def condition_text(*, premise_p:str,premise_q:str,premise_paraphrase:str,same_addendum:str,distinct_addendum:str,neutral_addendum:str,condition:str)->str:
    base=base_text(premise_p,premise_q)
    if condition=="unknown": return base
    if condition=="paraphrase": return f"RECORD:\n{premise_paraphrase}"
    if condition=="same_explicit": return f"{base}\n{same_addendum}"
    if condition=="distinct_explicit": return f"{base}\n{distinct_addendum}"
    if condition=="neutral_control": return f"{base}\n{neutral_addendum}"
    if condition=="relation_reminder": return f"{base}\nLogical note: two separate existential statements do not by themselves establish that their witnesses are the same individual."
    raise ValueError(f"unknown condition={condition}")
def recognition_prompt(*,premise_p:str,premise_q:str,p_property:str,q_property:str,probe:str,mapping:dict[str,str])->tuple[str,str]:
    context=base_text(premise_p,premise_q)
    if probe=="p_exists": question=f"Does the record establish that at least one individual has this property: {p_property}?";truth="yes"
    elif probe=="q_exists": question=f"Does the record establish that at least one individual has this property: {q_property}?";truth="yes"
    elif probe=="shared_entailment": question=f"Do these two statements logically establish that one and the same individual has both properties ({p_property}) and ({q_property})?";truth="no"
    elif probe=="identity_determined": question="Do the two statements determine whether the two existential witnesses are the same individual?";truth="no"
    else: raise ValueError(f"unknown probe={probe}")
    options="\n".join(f"{lab}. {'Yes' if sem=='yes' else 'No'}" for lab,sem in mapping.items());correct=next(lab for lab,sem in mapping.items() if sem==truth)
    return f"{context}\n\n{question}\n{options}\nAnswer exactly A or B.",correct
def downstream_prompt(*,context:str,requirement:str,decision_context:str,template:str,mapping:dict[str,str])->tuple[str,str]:
    labels={"established":"Yes — the record establishes the single-person requirement.","not_established":"No — the record does not establish the single-person requirement."};options="\n".join(f"{lab}. {labels[sem]}" for lab,sem in mapping.items());prompt=f"{context}\n\nREQUIREMENT:\n{requirement}\n\nDECISION CONTEXT:\n{decision_context}\n\n{template}\n{options}\nAnswer exactly A or B.";established=next(lab for lab,sem in mapping.items() if sem=="established");return prompt,established
