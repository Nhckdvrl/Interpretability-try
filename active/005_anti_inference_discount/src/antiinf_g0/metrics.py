from __future__ import annotations

from collections import defaultdict
import json, math, random
from pathlib import Path
from statistics import mean
from typing import Any
from .dataset import FAMILIES,load_scenarios
from .prompts import COMPREHENSION_TEMPLATES,NATURAL_JUDGMENT_TEMPLATES,BRIDGED_JUDGMENT_TEMPLATES


def _read_jsonl(path:str|Path)->list[dict[str,Any]]:
    rows=[]
    with Path(path).open("r",encoding="utf-8") as f:
        for lineno,line in enumerate(f,1):
            if not line.strip(): continue
            try: rows.append(json.loads(line))
            except json.JSONDecodeError as e: raise ValueError(f"invalid JSONL line {lineno}") from e
    return rows


def _bootstrap_ci(values:list[float],seed:int=0,n_boot:int=5000)->tuple[float,float]:
    if not values: return math.nan,math.nan
    rng=random.Random(seed); n=len(values); draws=sorted(mean(values[rng.randrange(n)] for _ in range(n)) for _ in range(n_boot)); return draws[int(.025*(n_boot-1))],draws[int(.975*(n_boot-1))]


def _aggregate(results:list[dict[str,Any]],scenario_ids:set[str])->dict[str,dict[str,Any]]:
    grouped=defaultdict(list); seen=set()
    for row in results:
        sid=str(row["scenario_id"])
        if sid not in scenario_ids: raise ValueError(f"unknown scenario_id={sid}")
        kind=row["kind"]; mode=row["mode"]
        if mode not in ("direct","inference"): raise ValueError(f"unknown mode={mode!r}")
        if kind=="comprehension": key=(sid,kind,mode,int(row["template_id"]))
        elif kind=="natural_judgment": key=(sid,kind,mode,int(row["template_id"]),int(row["label_order"]))
        elif kind=="bridged_judgment":
            if not bool(row.get("conditioned_on_yes",False)): raise ValueError(f"{sid}: bridged judgment is not conditioned on Yes")
            key=(sid,kind,mode,int(row["comprehension_template_id"]),int(row["template_id"]),int(row["label_order"]))
        else: raise ValueError(f"unknown kind={kind!r}")
        if key in seen: raise ValueError(f"duplicate result variant {key}")
        seen.add(key); grouped[sid].append(row)
    missing=scenario_ids-set(grouped)
    if missing: raise ValueError(f"missing results for {len(missing)} scenarios; first={sorted(missing)[:5]}")
    ncomp=len(COMPREHENSION_TEMPLATES); nnat=len(NATURAL_JUDGMENT_TEMPLATES)*2; nbridge=len(COMPREHENSION_TEMPLATES)*len(BRIDGED_JUDGMENT_TEMPLATES)*2; out={}
    for sid,rows in grouped.items():
        families={r["family"] for r in rows}
        if len(families)!=1: raise ValueError(f"inconsistent family for {sid}")
        s={"scenario_id":sid,"family":rows[0]["family"]}; comp_modes={}; nat_modes={}; bridge_modes={}
        for mode in ("direct","inference"):
            comp=[r for r in rows if r["kind"]=="comprehension" and r["mode"]==mode]
            nat=[r for r in rows if r["kind"]=="natural_judgment" and r["mode"]==mode]
            bridge=[r for r in rows if r["kind"]=="bridged_judgment" and r["mode"]==mode]
            if len(comp)!=ncomp: raise ValueError(f"{sid}/{mode}: expected {ncomp} comprehension variants, found {len(comp)}")
            if len(nat)!=nnat: raise ValueError(f"{sid}/{mode}: expected {nnat} natural judgment variants, found {len(nat)}")
            if len(bridge)!=nbridge: raise ValueError(f"{sid}/{mode}: expected {nbridge} bridged judgment variants, found {len(bridge)}")
            cm={int(r["template_id"]):float(r["p_yes"]) for r in comp}
            nm={(int(r["template_id"]),int(r["label_order"])):float(r["p_target"]) for r in nat}
            bm={(int(r["comprehension_template_id"]),int(r["template_id"]),int(r["label_order"])):float(r["p_target"]) for r in bridge}
            if set(cm)!=set(range(ncomp)): raise ValueError(f"{sid}/{mode}: malformed comprehension coverage")
            if set(nm)!={(jt,lo) for jt in range(len(NATURAL_JUDGMENT_TEMPLATES)) for lo in (0,1)}: raise ValueError(f"{sid}/{mode}: malformed natural judgment coverage")
            if set(bm)!={(ct,jt,lo) for ct in range(ncomp) for jt in range(len(BRIDGED_JUDGMENT_TEMPLATES)) for lo in (0,1)}: raise ValueError(f"{sid}/{mode}: malformed bridged judgment coverage")
            comp_modes[mode]=cm; nat_modes[mode]=nm; bridge_modes[mode]=bm; s[f"p_yes_{mode}_min"]=min(cm.values()); s[f"p_target_natural_{mode}"]=mean(nm.values()); s[f"p_target_bridged_{mode}"]=mean(bm.values())
        s["max_comprehension_gap"]=max(abs(comp_modes["direct"][t]-comp_modes["inference"][t]) for t in range(ncomp))
        nat_deltas=[nat_modes["direct"][k]-nat_modes["inference"][k] for k in sorted(nat_modes["direct"])]
        bridge_deltas=[bridge_modes["direct"][k]-bridge_modes["inference"][k] for k in sorted(bridge_modes["direct"])]
        s["judgment_discount"]=mean(nat_deltas); s["positive_variant_fraction"]=sum(x>0 for x in nat_deltas)/len(nat_deltas); s["bridged_discount"]=mean(bridge_deltas); s["bridged_positive_variant_fraction"]=sum(x>0 for x in bridge_deltas)/len(bridge_deltas); out[sid]=s
    return out


def summarize(*,data_path:str|Path,results_path:str|Path,config_path:str|Path,out_path:str|Path|None=None)->dict[str,Any]:
    scenarios=load_scenarios(data_path,strict=True); stats=_aggregate(_read_jsonl(results_path),{s.scenario_id for s in scenarios}); cfg=json.loads(Path(config_path).read_text(encoding="utf-8")); gate=cfg["comprehension_gate"]; strong_cfg=cfg["strong_scenario"]; pass_cfg=cfg["model_pass"]
    rows=[]
    for sid in sorted(stats):
        s=stats[sid]; gated=s["p_yes_direct_min"]>=gate["p_yes_direct_min"] and s["p_yes_inference_min"]>=gate["p_yes_inference_min"] and s["max_comprehension_gap"]<=gate["max_abs_gap"]
        strong=gated and s["p_target_natural_direct"]>=strong_cfg["p_target_direct_min"] and s["judgment_discount"]>=strong_cfg["judgment_discount_min"] and s["positive_variant_fraction"]>=strong_cfg["positive_variant_fraction_min"]
        rows.append({**s,"gated":gated,"strong":strong})
    gated=[r for r in rows if r["gated"]]; discounts=[r["judgment_discount"] for r in gated]; ci_lo,ci_hi=_bootstrap_ci(discounts); by_family={}
    for family in FAMILIES:
        sub=[r for r in gated if r["family"]==family]; by_family[family]={"gated":len(sub),"mean_discount":mean(r["judgment_discount"] for r in sub) if sub else math.nan,"mean_bridged_discount":mean(r["bridged_discount"] for r in sub) if sub else math.nan,"strong":sum(bool(r["strong"]) for r in sub)}
    qualifying_positive_families=sum(by_family[f]["gated"]>=pass_cfg["gated_per_positive_family_min"] and by_family[f]["mean_discount"]>0 for f in FAMILIES); strong_families=sum(by_family[f]["strong"]>=pass_cfg["strong_per_family_min"] for f in FAMILIES)
    agg={"total_scenarios":len(rows),"gated_scenarios":len(gated),"mean_judgment_discount":mean(discounts) if discounts else math.nan,"mean_bridged_discount":mean(r["bridged_discount"] for r in gated) if gated else math.nan,"bootstrap_95_ci":[ci_lo,ci_hi],"positive_families":qualifying_positive_families,"strong_families":strong_families,"strong_scenarios":sum(bool(r["strong"]) for r in gated),"positive_discount_fraction":sum(r["judgment_discount"]>0 for r in gated)/len(gated) if gated else 0.0}
    model_pass=agg["gated_scenarios"]>=pass_cfg["gated_scenarios_min"] and agg["mean_judgment_discount"]>=pass_cfg["mean_judgment_discount_min"] and ci_lo>pass_cfg["bootstrap_ci_lower_min"] and agg["positive_families"]>=pass_cfg["positive_families_min"] and agg["strong_families"]>=pass_cfg["strong_families_min"] and agg["strong_scenarios"]>=pass_cfg["strong_scenarios_min"] and agg["positive_discount_fraction"]>=pass_cfg["positive_discount_fraction_min"]
    summary={"model_pass":model_pass,"aggregate":agg,"by_family":by_family,"scenarios":rows,"note":"Promotion uses natural judgment only. The Yes-bridged judgment is a secondary diagnostic, not a gate."}
    if out_path is not None:
        out=Path(out_path); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    return summary
