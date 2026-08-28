from __future__ import annotations
DIRECTIONS=("supports_target","supports_other")
YES_NO_ORDERS=({"A":"yes","B":"no"},{"A":"no","B":"yes"})
CHOICE_ORDERS=({"A":"target","B":"other"},{"A":"other","B":"target"})
READOUT_TEMPLATES=(("belief","Which hypothesis is better supported by the record as it stands?"),("belief","Based only on the available information, which explanation is more plausible?"),("action","Which action is better justified by the record as it stands?"),("action","Given only the information above, which action should be preferred?"))
CONDITIONS=("no_evidence","weak","strong","neutral","no_evidence_complete","weak_complete","length_control","weak_length")

def base_text(background:str,calibration:str,protocol:str|None=None)->str:
    x=f"BACKGROUND:\n{background}\n\nCALIBRATION:\n{calibration}"
    if protocol:x+=f"\n\nREPORTING PROTOCOL:\n{protocol}"
    return x
def evidence_for(s,direction:str,strength:str)->str:
    if direction=="supports_target":return s.weak_target_evidence if strength=="weak" else s.strong_target_evidence
    if direction=="supports_other":return s.weak_other_evidence if strength=="weak" else s.strong_other_evidence
    raise ValueError(direction)
def length_control_for(s,direction:str)->str:
    if direction=="supports_target":return s.target_length_control_evidence
    if direction=="supports_other":return s.other_length_control_evidence
    raise ValueError(direction)
def condition_text(s,*,direction:str,condition:str)->str:
    protocol=s.pragmatic_completeness_text if condition in {"no_evidence_complete","weak_complete"} else None;base=base_text(s.background,s.calibration_text,protocol)
    if condition in {"no_evidence","no_evidence_complete"}:return base+"\n\nNo case-specific cue is observed."
    if condition in {"weak","weak_complete","weak_length"}:ev=evidence_for(s,direction,"weak")
    elif condition=="strong":ev=evidence_for(s,direction,"strong")
    elif condition=="neutral":ev=s.neutral_evidence
    elif condition=="length_control":ev=length_control_for(s,direction)
    else:raise ValueError(condition)
    return base+f"\n\nOBSERVATION:\n{ev}"
def support_prompt(*,base:str,evidence:str,focal_hypothesis:str,other_hypothesis:str,probe:str,mapping:dict[str,str],pragmatic_text:str)->tuple[str,str]:
    if probe=="support":q=f"Relative to the same background without this observation, does the observation provide genuine positive evidence for {focal_hypothesis}?";truth="yes"
    elif probe=="likelihood_relation":q=f"According to the stated calibration, is this observation more likely if {focal_hypothesis} is true than if {other_hypothesis} is true?";truth="yes"
    elif probe=="support_complete":q=f"Even under this reporting rule — {pragmatic_text} — does the observation remain genuine positive evidence for {focal_hypothesis}?";truth="yes"
    elif probe=="strong_support":q=f"Does this observation provide genuine positive evidence for {focal_hypothesis}?";truth="yes"
    else:raise ValueError(probe)
    opts="\n".join(f"{lab}. {'Yes' if sem=='yes' else 'No'}" for lab,sem in mapping.items());correct=next(l for l,s in mapping.items() if s==truth);return f"{base}\n\nFOCAL HYPOTHESIS: {focal_hypothesis}\nOTHER HYPOTHESIS: {other_hypothesis}\nOBSERVATION: {evidence}\n\n{q}\n{opts}\nAnswer exactly A or B.",correct
def readout_prompt(*,context:str,target_text:str,other_text:str,template:str,mapping:dict[str,str])->tuple[str,str]:
    text={"target":target_text,"other":other_text};opts="\n".join(f"{lab}. {text[sem]}" for lab,sem in mapping.items());target=next(l for l,s in mapping.items() if s=="target");return f"{context}\n\n{template}\n{opts}\nAnswer exactly A or B.",target
