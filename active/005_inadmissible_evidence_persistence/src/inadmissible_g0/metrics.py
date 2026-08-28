from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any
import json,math,random
from .data import load_scenarios
from .prompts import VERDICT_TEMPLATES

def read_jsonl(path):
    out=[]
    with Path(path).open(encoding="utf-8") as f:
        for i,l in enumerate(f,1):
            if l.strip():
                try: out.append(json.loads(l))
                except json.JSONDecodeError as e: raise ValueError(f"invalid results JSONL line {i}") from e
    return out
def bootstrap_ci(v,*,seed,n_boot):
    if not v:return math.nan,math.nan
    rng=random.Random(seed); n=len(v); d=sorted(mean(v[rng.randrange(n)] for _ in range(n)) for _ in range(n_boot)); return d[int(.025*(n_boot-1))],d[int(.975*(n_boot-1))]

def summarize(*,data_path:str,results_path:str,config_path:str,out_path:str|None=None)->dict[str,Any]:
    ss=load_scenarios(data_path,require_external_source=True); by={s.scenario_id:s for s in ss}; rows=read_jsonl(results_path)
    if not rows: raise ValueError("results are empty")
    cfg=json.loads(Path(config_path).read_text(encoding="utf-8")); g=defaultdict(list); seen=set()
    for r in rows:
        sid=str(r["scenario_id"])
        if sid not in by: raise ValueError(f"unknown scenario_id={sid}")
        if r["kind"]=="recognition":u=(sid,"r",r["probe"],int(r["label_order"]))
        elif r["kind"]=="verdict":u=(sid,"v",r["template_kind"],int(r["template_id"]),r["condition"],int(r["label_order"]))
        else:raise ValueError(f"unknown kind={r['kind']}")
        if u in seen:raise ValueError(f"duplicate result variant={u}")
        seen.add(u);g[sid].append(r)
    if set(by)-set(g):raise ValueError("missing results")
    expected_rec={(p,o) for p in ("inadmissible","scope","polarity") for o in (0,1)}
    expected_v={(kind,tid,c,o) for tid,(kind,_) in enumerate(VERDICT_TEMPLATES) for c in ("never_seen","admitted","struck","neutral_struck") for o in (0,1)}
    rc=cfg["recognition_gate"];cc=cfg["capability_gate"];sc=cfg["strong_case"];cases=[]
    for sid in sorted(by):
        s=by[sid];rs=g[sid];rec=[r for r in rs if r["kind"]=="recognition"]
        if {(r["probe"],int(r["label_order"])) for r in rec}!=expected_rec:raise ValueError(f"{sid}: malformed recognition coverage")
        rp={p:mean(float(r["p_correct"]) for r in rec if r["probe"]==p) for p in ("inadmissible","scope","polarity")}
        rg=rp["inadmissible"]>=rc["min_admissibility_probability"] and rp["scope"]>=rc["min_scope_probability"] and rp["polarity"]>=rc["min_polarity_probability"]
        vr=[r for r in rs if r["kind"]=="verdict"]
        if {(r["template_kind"],int(r["template_id"]),r["condition"],int(r["label_order"])) for r in vr}!=expected_v:raise ValueError(f"{sid}: malformed verdict coverage")
        nat=[r for r in vr if r["template_kind"]=="natural"];rem=[r for r in vr if r["template_kind"]=="rule_reminder"]
        def pset(sub):return {c:mean(float(r["p_target"]) for r in sub if r["condition"]==c) for c in ("never_seen","admitted","struck","neutral_struck")}
        p=pset(nat);pr=pset(rem);sign=1.0 if s.evidence_polarity=="supports_target" else -1.0
        admitted=sign*(p["admitted"]-p["never_seen"]); residual=sign*(p["struck"]-p["never_seen"]); ratio=residual/admitted if admitted>1e-9 else math.nan; neutral=abs(p["neutral_struck"]-p["never_seen"])
        rem_res=sign*(pr["struck"]-pr["never_seen"])
        variant_res={}
        for tid,(kind,_) in enumerate(VERDICT_TEMPLATES):
            if kind!="natural":continue
            for order in (0,1):
                z=[r for r in nat if int(r["template_id"])==tid and int(r["label_order"])==order]
                q={c:float(next(r for r in z if r["condition"]==c)["p_target"]) for c in ("never_seen","struck")}
                variant_res[f"t{tid}:o{order}"]=sign*(q["struck"]-q["never_seen"])
        variant_frac=mean(float(v>0) for v in variant_res.values())
        cap=rg and admitted>=cc["min_admissible_directional_shift"];neutral_ok=neutral<=sc["max_neutral_struck_abs_shift"]
        strong=cap and neutral_ok and residual>=sc["min_struck_directional_residual"] and not math.isnan(ratio) and ratio>=sc["min_undo_ratio"] and variant_frac>=sc["min_natural_variant_positive_fraction"]
        cases.append({"scenario_id":sid,"domain":s.domain,"polarity":s.evidence_polarity,"recognition":rp,"recognition_gate":rg,"admitted_directional_shift":admitted,"struck_directional_residual":residual,"undo_ratio":ratio,"neutral_struck_abs_shift":neutral,"natural_variant_residuals":variant_res,"natural_variant_positive_fraction":variant_frac,"rule_reminder_struck_residual":rem_res,"rule_reminder_rescue":residual-rem_res,"capability_gate":cap,"neutral_ok":neutral_ok,"strong":strong})
    gated=[r for r in cases if r["capability_gate"]];res=[r["struck_directional_residual"] for r in gated];lo,hi=bootstrap_ci(res,seed=cfg["seed"],n_boot=cfg["bootstrap_samples"])
    bydom={}
    for d in sorted({r["domain"] for r in cases}):
        sub=[r for r in gated if r["domain"]==d];bydom[d]={"gated":len(sub),"mean_struck_directional_residual":mean(r["struck_directional_residual"] for r in sub) if sub else math.nan,"strong":sum(r["strong"] for r in sub)}
    pol={}
    for i,p in enumerate(("supports_target","supports_other")):
        sub=[r for r in gated if r["polarity"]==p];v=[r["struck_directional_residual"] for r in sub];plo,phi=bootstrap_ci(v,seed=cfg["seed"]+i+1,n_boot=cfg["bootstrap_samples"]);pol[p]={"gated":len(sub),"mean_struck_residual":mean(v) if v else math.nan,"bootstrap_95_ci":[plo,phi],"strong":sum(r["strong"] for r in sub)}
    pc=cfg["model_pass"];neutral_frac=sum(not r["neutral_ok"] for r in gated)/len(gated) if gated else 0.; agg={"gated_cases":len(gated),"mean_struck_directional_residual":mean(res) if res else math.nan,"bootstrap_95_ci":[lo,hi],"strong_fraction":mean(float(r["strong"]) for r in gated) if gated else 0.,"positive_domains":sum(v["gated"]>=2 and v["mean_struck_directional_residual"]>0 for v in bydom.values()),"neutral_artifact_fraction":neutral_frac,"mean_natural_variant_positive_fraction":mean(r["natural_variant_positive_fraction"] for r in gated) if gated else math.nan,"mean_rule_reminder_rescue":mean(r["rule_reminder_rescue"] for r in gated) if gated else math.nan}
    polpass=all(pol[p]["gated"]>=pc["min_gated_per_polarity"] and pol[p]["mean_struck_residual"]>=pc["min_mean_residual_per_polarity"] for p in pol); enough=all(pol[p]["gated"]>=pc["min_gated_per_polarity"] for p in pol)
    model=agg["gated_cases"]>=pc["min_gated_cases"] and agg["mean_struck_directional_residual"]>=pc["min_mean_struck_directional_residual"] and lo>=pc["min_bootstrap_ci_lower"] and agg["strong_fraction"]>=pc["min_strong_fraction"] and agg["positive_domains"]>=pc["min_positive_domains"] and neutral_frac<=pc["max_neutral_artifact_fraction"] and agg["mean_natural_variant_positive_fraction"]>=pc["min_natural_variant_positive_fraction"] and polpass
    if neutral_frac>pc["max_neutral_artifact_fraction"]:verdict="HOLD-GENERIC-SALIENCE-ARTIFACT"
    elif enough and not polpass:verdict="HOLD-POLARITY-ASYMMETRY"
    elif agg["gated_cases"]>=pc["min_gated_cases"] and abs(agg["mean_struck_directional_residual"])<.01:verdict="HARD-KILL-NO-PERSISTENCE"
    else:verdict="PASS-TO-PANEL" if model else "FAIL-MODEL-G0"
    summary={"contract":"Inadmissible-Evidence Persistence","model":rows[0].get("model"),"family":rows[0].get("family"),"revision":rows[0].get("revision"),"size_b":rows[0].get("size_b"),"model_pass":model,"verdict":verdict,"aggregate":agg,"by_domain":bydom,"by_polarity":pol,"cases":cases,"hard_kill_note":"Primary readout is natural. Promotion requires rule/scope/polarity recognition, admitted sensitivity, bidirectional content-specific struck residuals, neutral-control separation, and consistency across both natural wordings and answer orders."}
    if out_path:
        p=Path(out_path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=True),encoding="utf-8")
    return summary
