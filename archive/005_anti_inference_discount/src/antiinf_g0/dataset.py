from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Iterable

FAMILIES=("legal","medical","eligibility")

@dataclass(frozen=True)
class Scenario:
    scenario_id:str; family:str; context:str; critical_fact:str; direct_evidence:str; inference_evidence:str; target_conclusion:str; alternative_conclusion:str


def generate_scenarios()->list[Scenario]:
    rows=[]
    legal_events=["shipment","court filing","inspection","safety report","permit renewal","payment","appeal","incident notice"]
    legal_times=[(9,20),(11,35),(14,50),(16,10)]
    for event_i,event in enumerate(legal_events):
        for time_i,(hour,minute) in enumerate(legal_times):
            deadline=hour*60+minute; actual=deadline+(15,25,40,55)[time_i]; dh,dm=divmod(deadline,60); ah,am=divmod(actual,60)
            rows.append(Scenario(f"legal-{event_i:02d}-{time_i:02d}","legal",f"A compliance rule says the {event} violates the timing requirement exactly when it occurs after the deadline. Treat a direct statement in the official record and the record's listed timestamps as equally authoritative and accurate.",f"The {event} occurred after the deadline.",f"The official record directly states that the {event} occurred later than the deadline.",f"The official record lists the deadline as {dh:02d}:{dm:02d} and the {event} time as {ah:02d}:{am:02d}.","The timing requirement was violated.","The timing requirement was satisfied."))
    tests=["troponin","D-dimer","CRP","fasting glucose","ALT","TSH","LDL","serum lactate"]
    vals=[(10,13),(20,27),(50,63),(100,118)]
    for ti,test in enumerate(tests):
        for vi,(cutoff,measured) in enumerate(vals):
            rows.append(Scenario(f"medical-{ti:02d}-{vi:02d}","medical",f"For this screening protocol, the {test} screen is positive exactly when the measured value is above the cutoff. Treat a direct classification in the laboratory record and the record's listed numeric values as equally authoritative and accurate.",f"The measured {test} value was above the cutoff.",f"The laboratory record directly classifies the measured {test} value as exceeding the cutoff.",f"The laboratory record lists the {test} cutoff as {cutoff} units and the measured value as {measured} units.","The screen is positive under the stated protocol.","The screen is negative under the stated protocol."))
    quantities=["annual income","monthly rent burden","household assets","commute distance","weekly work hours","annual electricity use","outstanding balance","response time"]
    vals=[(100,85),(250,210),(500,430),(1000,880)]
    for qi,q in enumerate(quantities):
        for vi,(cutoff,observed) in enumerate(vals):
            rows.append(Scenario(f"eligibility-{qi:02d}-{vi:02d}","eligibility",f"Under this program, an applicant qualifies exactly when their {q} is below the cutoff. Treat a direct classification in the application record and the record's listed numeric values as equally authoritative and accurate.",f"The applicant's {q} was below the cutoff.",f"The application record directly classifies the applicant's {q} as under the cutoff.",f"The application record lists the cutoff for {q} as {cutoff} units and the applicant's value as {observed} units.","The applicant qualifies under the stated rule.","The applicant does not qualify under the stated rule."))
    return _validate_scenarios(rows,strict=True)


def _validate_scenarios(rows:Iterable[Scenario],*,strict:bool)->list[Scenario]:
    rows=list(rows); ids=[x.scenario_id for x in rows]
    if len(ids)!=len(set(ids)): raise ValueError("duplicate scenario IDs")
    for row in rows:
        if row.family not in FAMILIES: raise ValueError(f"unknown family {row.family!r}")
        if any(not str(v).strip() for v in asdict(row).values()): raise ValueError(f"empty field in {row.scenario_id}")
        if row.target_conclusion==row.alternative_conclusion: raise ValueError(f"identical conclusions in {row.scenario_id}")
        d=row.direct_evidence.strip().lower(); i=row.inference_evidence.strip().lower(); fact=row.critical_fact.lower().rstrip(".")
        if d in i or i in d: raise ValueError(f"one evidence condition contains the other in {row.scenario_id}")
        if fact in d or fact in i: raise ValueError(f"evidence repeats the critical-fact query verbatim in {row.scenario_id}")
    if strict:
        if len(rows)!=96: raise ValueError(f"expected 96 scenarios, found {len(rows)}")
        for family in FAMILIES:
            n=sum(x.family==family for x in rows)
            if n!=32: raise ValueError(f"expected 32 {family} scenarios, found {n}")
    return rows


def write_scenarios(path:str|Path)->list[Scenario]:
    rows=generate_scenarios(); out=Path(path); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",encoding="utf-8") as f:
        for row in rows: f.write(json.dumps(asdict(row),ensure_ascii=False)+"\n")
    return rows


def load_scenarios(path:str|Path,*,strict:bool=True)->list[Scenario]:
    rows=[]
    with Path(path).open("r",encoding="utf-8") as f:
        for lineno,line in enumerate(f,1):
            if not line.strip(): continue
            try: rows.append(Scenario(**json.loads(line)))
            except (json.JSONDecodeError,TypeError) as e: raise ValueError(f"malformed scenario line {lineno}") from e
    return _validate_scenarios(rows,strict=strict)
