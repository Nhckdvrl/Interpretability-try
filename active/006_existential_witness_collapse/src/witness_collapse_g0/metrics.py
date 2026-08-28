from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from statistics import mean
import json, math, random
from .data import load_scenarios
from .prompts import CONDITIONS, DOWNSTREAM_TEMPLATES
from .run import RECOGNITION_PROBES

def read_jsonl(path):
    rows=[]
    with Path(path).open(encoding="utf-8") as f:
        for i,line in enumerate(f,1):
            if not line.strip(): continue
            try: rows.append(json.loads(line))
            except json.JSONDecodeError as e: raise ValueError(f"invalid results JSONL line {i}") from e
    return rows

def bootstrap_ci(values,*,seed,n_boot):
    if not values:return math.nan,math.nan
    if n_boot<=0:raise ValueError("n_boot must be > 0")
    rng=random.Random(seed);n=len(values);draws=sorted(mean(values[rng.randrange(n)] for _ in range(n)) for _ in range(n_boot));return draws[int(.025*(n_boot-1))],draws[int(.975*(n_boot-1))]

def compute_case_features(*,recognition,p,variant_unknown,variant_paraphrase,cfg):
    rg,cg,sc=cfg["recognition_gate"],cfg["capability_gate"],cfg["strong_case"]
    rg_ok=recognition["p_exists"]>=rg["min_existence_probability"] and recognition["q_exists"]>=rg["min_existence_probability"] and recognition["shared_entailment"]>=rg["min_no_shared_entailment_probability"] and recognition["identity_determined"]>=rg["min_identity_underdetermined_probability"]
    control_ok=p["same_explicit"]>=cg["min_same_explicit_established_probability"] and p["distinct_explicit"]<=cg["max_distinct_explicit_established_probability"]
    gate=rg_ok and control_ok;unknown=p["unknown"]-.5;para=p["paraphrase"]-.5;uvd=p["unknown"]-p["distinct_explicit"];neutral=abs(p["neutral_control"]-p["unknown"]);vf=mean(float(x>.5) for x in variant_unknown+variant_paraphrase)
    strong=gate and p["unknown"]>=sc["min_unknown_established_probability"] and p["paraphrase"]>=sc["min_paraphrase_established_probability"] and uvd>=sc["min_unknown_minus_distinct"] and neutral<=sc["max_neutral_abs_shift"] and vf>=sc["min_natural_variant_positive_fraction"]
    return {"recognition_gate":rg_ok,"downstream_control_gate":control_ok,"capability_gate":gate,"unknown_margin":unknown,"paraphrase_margin":para,"unknown_vs_distinct":uvd,"same_sensitivity":p["same_explicit"]-p["unknown"],"neutral_abs_shift":neutral,"neutral_ok":neutral<=sc["max_neutral_abs_shift"],"reminder_rescue":p["unknown"]-p["relation_reminder"],"natural_variant_positive_fraction":vf,"strong":strong}

def summarize(*,data_path,results_path,config_path,out_path=None):
    scenarios=load_scenarios(data_path,require_external_source=True);by={s.scenario_id:s for s in scenarios};rows=read_jsonl(results_path)
    if not rows:raise ValueError("results are empty")
    for field in ("model","family","revision","size_b","requested_dtype"):
        if len({json.dumps(r.get(field),sort_keys=True) for r in rows})!=1:raise ValueError(f"inconsistent run metadata for {field}")
    cfg=json.loads(Path(config_path).read_text(encoding="utf-8"));grouped=defaultdict(list);seen=set()
    for r in rows:
        sid=str(r.get("scenario_id"))
        if sid not in by:raise ValueError(f"unknown scenario_id={sid}")
        key=(sid,"r",r.get("probe"),int(r.get("label_order"))) if r.get("kind")=="recognition" else (sid,"d",r.get("condition"),int(r.get("template_id")),int(r.get("label_order"))) if r.get("kind")=="downstream" else None
        if key is None:raise ValueError(f"unknown kind={r.get('kind')}")
        if key in seen:raise ValueError(f"duplicate result variant={key}")
        seen.add(key);grouped[sid].append(r)
    if set(by)!=set(grouped):raise ValueError("scenario coverage mismatch")
    expected_r={(p,o) for p in RECOGNITION_PROBES for o in (0,1)};expected_d={(c,t,o) for c in CONDITIONS for t in range(len(DOWNSTREAM_TEMPLATES)) for o in (0,1)};cases=[]
    for sid in sorted(by):
        rr=[r for r in grouped[sid] if r["kind"]=="recognition"];dr=[r for r in grouped[sid] if r["kind"]=="downstream"]
        if {(r["probe"],int(r["label_order"])) for r in rr}!=expected_r:raise ValueError(f"{sid}: malformed recognition coverage")
        if {(r["condition"],int(r["template_id"]),int(r["label_order"])) for r in dr}!=expected_d:raise ValueError(f"{sid}: malformed downstream coverage")
        recognition={probe:min(float(r["p_correct"]) for r in rr if r["probe"]==probe) for probe in RECOGNITION_PROBES};p={c:mean(float(r["p_established"]) for r in dr if r["condition"]==c) for c in CONDITIONS}
        feat=compute_case_features(recognition=recognition,p=p,variant_unknown=[float(r["p_established"]) for r in dr if r["condition"]=="unknown"],variant_paraphrase=[float(r["p_established"]) for r in dr if r["condition"]=="paraphrase"],cfg=cfg);cases.append({"scenario_id":sid,"domain":by[sid].domain,"recognition":recognition,"p_established":p,**feat})
    gated=[x for x in cases if x["capability_gate"]];margins=[x["unknown_margin"] for x in gated];lo,hi=bootstrap_ci(margins,seed=cfg["seed"],n_boot=cfg["bootstrap_samples"]);pc=cfg["model_pass"];domains={}
    for d in sorted({x["domain"] for x in cases}):
        sub=[x for x in gated if x["domain"]==d];domains[d]={"gated":len(sub),"mean_unknown_margin":mean(x["unknown_margin"] for x in sub) if sub else math.nan,"strong":sum(x["strong"] for x in sub)}
    neutral=mean(float(not x["neutral_ok"]) for x in gated) if gated else 0.;agg={"total_cases":len(cases),"recognition_gated_cases":sum(x["recognition_gate"] for x in cases),"gated_cases":len(gated),"mean_unknown_margin":mean(margins) if margins else math.nan,"bootstrap_95_ci":[lo,hi],"mean_paraphrase_margin":mean(x["paraphrase_margin"] for x in gated) if gated else math.nan,"mean_unknown_minus_distinct":mean(x["unknown_vs_distinct"] for x in gated) if gated else math.nan,"mean_reminder_rescue":mean(x["reminder_rescue"] for x in gated) if gated else math.nan,"neutral_artifact_fraction":neutral,"strong_fraction":mean(float(x["strong"]) for x in gated) if gated else 0.,"mean_natural_variant_positive_fraction":mean(x["natural_variant_positive_fraction"] for x in gated) if gated else math.nan,"positive_domains":sum(v["gated"]>=2 and v["mean_unknown_margin"]>0 for v in domains.values())}
    enough=len(gated)>=pc["min_gated_cases"];model=enough and agg["mean_unknown_margin"]>=pc["min_mean_unknown_margin"] and lo>=pc["min_bootstrap_ci_lower"] and agg["mean_paraphrase_margin"]>=pc["min_mean_paraphrase_margin"] and agg["mean_unknown_minus_distinct"]>=pc["min_mean_unknown_minus_distinct"] and agg["strong_fraction"]>=pc["min_strong_fraction"] and agg["positive_domains"]>=pc["min_positive_domains"] and neutral<=pc["max_neutral_artifact_fraction"] and agg["mean_natural_variant_positive_fraction"]>=pc["min_natural_variant_positive_fraction"]
    recognition_fraction=agg["recognition_gated_cases"]/len(cases) if cases else 0
    if len(cases)>=pc["min_gated_cases"] and recognition_fraction<pc["min_recognition_gate_fraction"]:verdict="HARD-KILL-QUANTIFIER-CAPABILITY-FLOOR"
    elif enough and agg["mean_unknown_margin"]<=pc["no_effect_abs_margin"]:verdict="HARD-KILL-NO-ILLEGAL-JOIN"
    elif enough and agg["mean_unknown_margin"]>0 and agg["mean_paraphrase_margin"]<=0:verdict="HOLD-WORDING-ARTIFACT"
    elif neutral>pc["max_neutral_artifact_fraction"]:verdict="HOLD-GENERIC-CONTEXT-ARTIFACT"
    else:verdict="PASS-TO-PANEL" if model else "FAIL-MODEL-G0"
    out={"contract":"Existential Witness Collapse","model":rows[0].get("model"),"family":rows[0].get("family"),"revision":rows[0].get("revision"),"size_b":rows[0].get("size_b"),"model_pass":model,"verdict":verdict,"aggregate":agg,"by_domain":domains,"cases":cases,"hard_kill_note":"Recognition gates use the worse label order. A non-positive unknown-world margin argues against the target phenotype rather than being an ambiguous failure."}
    if out_path:Path(out_path).write_text(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=True),encoding="utf-8")
    return out
