from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any
import json,math,random
from .data import load_scenarios
from .prompts import CONDITIONS,DIRECTIONS,READOUT_TEMPLATES
from .run import SUPPORT_PROBES

def read_jsonl(path):
    out=[]
    with Path(path).open(encoding="utf-8") as f:
        for i,l in enumerate(f,1):
            if l.strip():
                try:out.append(json.loads(l))
                except json.JSONDecodeError as e:raise ValueError(f"invalid results JSONL line {i}") from e
    return out

def bootstrap_ci(v,*,seed,n_boot):
    if not v:return math.nan,math.nan
    if n_boot<=0:raise ValueError("n_boot must be > 0")
    rng=random.Random(seed);n=len(v);d=sorted(mean(v[rng.randrange(n)] for _ in range(n)) for _ in range(n_boot));return d[int(.025*(n_boot-1))],d[int(.975*(n_boot-1))]
def signed_update(direction:str,p_condition:float,p_baseline:float)->float:
    raw=p_condition-p_baseline
    if direction=="supports_target":return raw
    if direction=="supports_other":return -raw
    raise ValueError(direction)
def _assert_metadata(rows):
    for field in ("model","family","revision","size_b","requested_dtype"):
        vals={json.dumps(r.get(field),sort_keys=True) for r in rows}
        if len(vals)!=1:raise ValueError(f"inconsistent run metadata for {field}: {vals}")
def compute_direction_features(*,direction:str,support:dict[str,float],readouts:dict[str,dict[str,float]],variants:dict[str,dict[str,list[float]]],cfg:dict)->dict[str,Any]:
    sg=cfg["support_gate"];cg=cfg["capability_gate"];sc=cfg["strong_case"]
    support_gate=(support["support"]>=sg["min_support_probability"] and support["likelihood_relation"]>=sg["min_likelihood_relation_probability"] and support["support_complete"]>=sg["min_complete_support_probability"] and support["strong_support"]>=sg["min_strong_support_probability"])
    b=readouts["belief"];a=readouts["action"]
    strong_b=signed_update(direction,b["strong"],b["no_evidence"]);strong_a=signed_update(direction,a["strong"],a["no_evidence"]);capability=support_gate and strong_b>=cg["min_strong_belief_directional_shift"] and strong_a>=cg["min_strong_action_directional_shift"]
    weak_b=-signed_update(direction,b["weak"],b["no_evidence"]);weak_a=-signed_update(direction,a["weak"],a["no_evidence"]);complete_b=-signed_update(direction,b["weak_complete"],b["no_evidence_complete"]);complete_a=-signed_update(direction,a["weak_complete"],a["no_evidence_complete"]);length_b=-signed_update(direction,b["weak_length"],b["length_control"]);length_a=-signed_update(direction,a["weak_length"],a["length_control"]);neutral_b=abs(b["neutral"]-b["no_evidence"]);neutral_a=abs(a["neutral"]-a["no_evidence"])
    var=variants["belief"]["weak"]+variants["action"]["weak"];variant_frac=mean(float(x>0) for x in var);pragmatic=complete_b>=sc["min_complete_belief_backfire"] and complete_a>=sc["min_complete_action_backfire"];length_ok=length_b>=sc["min_length_belief_backfire"] and length_a>=sc["min_length_action_backfire"];neutral_ok=neutral_b<=sc["max_neutral_abs_shift"] and neutral_a<=sc["max_neutral_abs_shift"];strong=capability and weak_b>=sc["min_belief_backfire"] and weak_a>=sc["min_action_backfire"] and pragmatic and length_ok and neutral_ok and variant_frac>=sc["min_variant_backfire_fraction"]
    return {"support_gate":support_gate,"capability_gate":capability,"strong_belief_directional_shift":strong_b,"strong_action_directional_shift":strong_a,"belief_backfire":weak_b,"action_backfire":weak_a,"complete_belief_backfire":complete_b,"complete_action_backfire":complete_a,"length_belief_backfire":length_b,"length_action_backfire":length_a,"neutral_belief_abs_shift":neutral_b,"neutral_action_abs_shift":neutral_a,"pragmatic_robust":pragmatic,"length_robust":length_ok,"neutral_ok":neutral_ok,"variant_backfire_fraction":variant_frac,"strong":strong}
def summarize(*,data_path:str,results_path:str,config_path:str,out_path:str|None=None)->dict[str,Any]:
    ss=load_scenarios(data_path,require_external_source=True);by={s.scenario_id:s for s in ss};rows=read_jsonl(results_path)
    if not rows:raise ValueError("results are empty")
    _assert_metadata(rows);cfg=json.loads(Path(config_path).read_text(encoding="utf-8"));g=defaultdict(list);seen=set()
    for r in rows:
        sid=str(r.get("scenario_id"))
        if sid not in by:raise ValueError(f"unknown scenario_id={sid}")
        if r.get("direction") not in DIRECTIONS:raise ValueError(f"bad direction={r.get('direction')}")
        if r.get("kind")=="support_probe":key=(sid,"s",r["direction"],r["probe"],int(r["label_order"]))
        elif r.get("kind")=="readout":key=(sid,"r",r["direction"],r["condition"],int(r["template_id"]),int(r["label_order"]))
        else:raise ValueError(f"unknown kind={r.get('kind')}")
        if key in seen:raise ValueError(f"duplicate result variant={key}")
        seen.add(key);g[sid].append(r)
    if set(by)!=set(g):raise ValueError(f"scenario coverage mismatch missing={sorted(set(by)-set(g))}")
    exp_s={(d,p,o) for d in DIRECTIONS for p in SUPPORT_PROBES for o in (0,1)};exp_r={(d,c,t,o) for d in DIRECTIONS for c in CONDITIONS for t in range(len(READOUT_TEMPLATES)) for o in (0,1)};directions=[];pairs=[]
    for sid in sorted(by):
        rs=g[sid];sr=[r for r in rs if r["kind"]=="support_probe"];rr=[r for r in rs if r["kind"]=="readout"]
        if {(r["direction"],r["probe"],int(r["label_order"])) for r in sr}!=exp_s:raise ValueError(f"{sid}: malformed support coverage")
        if {(r["direction"],r["condition"],int(r["template_id"]),int(r["label_order"])) for r in rr}!=exp_r:raise ValueError(f"{sid}: malformed readout coverage")
        drows=[]
        for direction in DIRECTIONS:
            support={p:mean(float(r["p_correct"]) for r in sr if r["direction"]==direction and r["probe"]==p) for p in SUPPORT_PROBES};readouts={};variants={"belief":{"weak":[]},"action":{"weak":[]}}
            for kind in ("belief","action"):
                kr=[r for r in rr if r["direction"]==direction and r["template_kind"]==kind];readouts[kind]={c:mean(float(r["p_target"]) for r in kr if r["condition"]==c) for c in CONDITIONS};paired=[]
                for wr in (r for r in kr if r["condition"]=="weak"):
                    br=next(r for r in kr if r["condition"]=="no_evidence" and int(r["template_id"])==int(wr["template_id"]) and int(r["label_order"])==int(wr["label_order"]));paired.append(-signed_update(direction,float(wr["p_target"]),float(br["p_target"])))
                variants[kind]["weak"]=paired
            feat=compute_direction_features(direction=direction,support=support,readouts=readouts,variants=variants,cfg=cfg);x={"scenario_id":sid,"domain":by[sid].domain,"direction":direction,"support":support,"readouts":readouts,**feat};directions.append(x);drows.append(x)
        m={x["direction"]:x for x in drows};pairs.append({"scenario_id":sid,"domain":by[sid].domain,"gated":all(x["capability_gate"] for x in drows),"strong":all(x["strong"] for x in drows),"belief_backfire_mean":mean(x["belief_backfire"] for x in drows),"action_backfire_mean":mean(x["action_backfire"] for x in drows),"complete_backfire_mean":mean((x["complete_belief_backfire"]+x["complete_action_backfire"])/2 for x in drows),"direction_asymmetry_belief":abs(m["supports_target"]["belief_backfire"]-m["supports_other"]["belief_backfire"])})
    gd=[x for x in directions if x["capability_gate"]];gp=[x for x in pairs if x["gated"]];bv=[x["belief_backfire"] for x in gd];av=[x["action_backfire"] for x in gd];pvals=[x["belief_backfire_mean"] for x in gp];blo,bhi=bootstrap_ci(bv,seed=cfg["seed"],n_boot=cfg["bootstrap_samples"]);alo,ahi=bootstrap_ci(av,seed=cfg["seed"]+1,n_boot=cfg["bootstrap_samples"]);plo,phi=bootstrap_ci(pvals,seed=cfg["seed"]+2,n_boot=cfg["bootstrap_samples"]);bydom={}
    for dom in sorted({x["domain"] for x in pairs}):
        sub=[x for x in gp if x["domain"]==dom];bydom[dom]={"gated_pairs":len(sub),"mean_belief_backfire":mean(x["belief_backfire_mean"] for x in sub) if sub else math.nan,"strong_pairs":sum(x["strong"] for x in sub)}
    pc=cfg["model_pass"];rec_frac=sum(x["support_gate"] for x in directions)/len(directions) if directions else 0.;neutral_frac=mean(float(not x["neutral_ok"]) for x in gd) if gd else 0.;prag_frac=mean(float(x["pragmatic_robust"]) for x in gd) if gd else 0.;length_frac=mean(float(x["length_robust"]) for x in gd) if gd else 0.;agg={"gated_directions":len(gd),"gated_scenario_pairs":len(gp),"mean_belief_backfire":mean(bv) if bv else math.nan,"belief_bootstrap_95_ci":[blo,bhi],"mean_action_backfire":mean(av) if av else math.nan,"action_bootstrap_95_ci":[alo,ahi],"mean_pair_belief_backfire":mean(pvals) if pvals else math.nan,"pair_bootstrap_95_ci":[plo,phi],"strong_pair_fraction":mean(float(x["strong"]) for x in gp) if gp else 0.,"support_gate_fraction":rec_frac,"pragmatic_survival_fraction":prag_frac,"length_survival_fraction":length_frac,"neutral_artifact_fraction":neutral_frac,"positive_domains":sum(v["gated_pairs"]>=2 and v["mean_belief_backfire"]>0 for v in bydom.values())}
    enough=len(gp)>=pc["min_gated_pairs"];model=enough and agg["mean_belief_backfire"]>=pc["min_mean_belief_backfire"] and blo>=pc["min_bootstrap_ci_lower"] and agg["mean_action_backfire"]>=pc["min_mean_action_backfire"] and alo>=pc["min_bootstrap_ci_lower"] and agg["mean_pair_belief_backfire"]>=pc["min_mean_pair_backfire"] and plo>=pc["min_pair_bootstrap_ci_lower"] and agg["strong_pair_fraction"]>=pc["min_strong_pair_fraction"] and prag_frac>=pc["min_pragmatic_survival_fraction"] and length_frac>=pc["min_length_survival_fraction"] and neutral_frac<=pc["max_neutral_artifact_fraction"] and agg["positive_domains"]>=pc["min_positive_domains"]
    if len(pairs)>=pc["min_gated_pairs"] and rec_frac<pc["min_support_gate_fraction"]:verdict="HARD-KILL-EVIDENCE-DIRECTION-CAPABILITY-FLOOR"
    elif enough and agg["mean_pair_belief_backfire"]<pc["no_effect_backfire"]:verdict="HARD-KILL-NO-BACKFIRE"
    elif enough and prag_frac<pc["min_pragmatic_survival_fraction"]:verdict="HARD-KILL-PRAGMATIC-ABSENCE-IMPLICATURE"
    elif enough and agg["mean_belief_backfire"]>0 and agg["mean_action_backfire"]<=0:verdict="HOLD-READOUT-ONLY"
    elif neutral_frac>pc["max_neutral_artifact_fraction"]:verdict="HOLD-GENERIC-MENTION-ARTIFACT"
    else:verdict="PASS-TO-PANEL" if model else "FAIL-MODEL-G0"
    summary={"contract":"Weak-Evidence Backfire","model":rows[0].get("model"),"family":rows[0].get("family"),"revision":rows[0].get("revision"),"size_b":rows[0].get("size_b"),"model_pass":model,"verdict":verdict,"aggregate":agg,"by_domain":bydom,"directions":directions,"scenario_pairs":pairs,"hard_kill_note":"A backfire direction counts only if the model recognizes the weak cue as positive evidence and strong evidence moves toward that focal hypothesis. Promotion additionally requires bidirectional polarity, belief+action concordance, completeness survival, a direction-specific LR=1 length-matched filler comparison, and neutral separation."}
    if out_path:
        p=Path(out_path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=True),encoding="utf-8")
    return summary
