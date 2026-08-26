from __future__ import annotations

from collections import defaultdict
import json, math, random
from pathlib import Path
from statistics import mean
from typing import Any
from .dataset import FAMILIES,load_scenarios
from .prompts import COMPREHENSION_TEMPLATES,JUDGMENT_TEMPLATES


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
        elif kind=="judgment":
            if not bool(row.get("conditioned_on_yes",False)): raise ValueError(f"{sid}: judgment row is not conditioned on successful acknowledgement")
            key=(sid,kind,mode,int(row["comprehension_template_id"]),int(row["template_id"]),int(row["label_order"]))
        else: raise ValueError(f"unknown kind={kind!r}")
        if key in seen: raise ValueError(f"duplicate result variant {key}")
        seen.add(key); grouped[sid].append(row)
    missing=scenario_ids-set(grouped)
    if missing: raise ValueError(f"missing results for {len(missing)} scenarios; first={sorted(missing)[:5]}")
    expected_comp=len(COMPREHENSION_TEMPLATES); expected_judg=len(COMPREHENSION_TEMPLATES)*len(JUDGMENT_TEMPLATES)*2; out={}
    for sid,rows in grouped.items():
        families={r["family"] for r in rows}
        if len(families)!=1: raise ValueError(f"inconsistent family for {sid}")
        s={"scenario_id":sid,"family":rows[0]["family"]}; comp_by_mode={}; judg_by_mode={}
        for mode in ("direct","inference"):
            comp=[r for r in rows if r["kind"]=="comprehension" and r["mode"]==mode]; judg=[r for r in rows if r["kind"]=="judgment" and r["mode"]==mode]
            if len(comp)!=expected_comp: raise ValueError(f"{sid}/{mode}: expected {expected_comp} comprehension variants, found {len(comp)}")
            if len(judg)!=expected_judg: raise ValueError(f"{sid}/{mode}: expected {expected_judg} judgment variants, found {len(judg)}")
            cm={int(r["template_id"]):float(r["p_yes"]) for r in comp}; jm={(int(r["comprehension_template_id"]),int(r["template_id"]),int(r["label_order"])):float(r["p_target"]) for r in judg}
            if set(cm)!=set(range(expected_comp)): raise ValueError(f"{sid}/{mode}: malformed comprehension coverage")
            expected_keys={(ct,jt,lo) for ct in range(expected_comp) for jt in range(len(JUDGMENT_TEMPLATES)) for lo in (0,1)}
            if set(jm)!=expected_keys: raise ValueError(f"{sid}/{mode}: malformed matched judgment coverage")
            comp_by_mode[mode]=cm; judg_by_mode[mode]=jm; s[f"p_yes_{mode}"]=mean(cm.values()); s[f"p_yes_{mode}_min"]=min(cm.values()); s[f"p_target_{mode}"]=mean(jm.values())
        gaps=[abs(comp_by_mode["direct"][t]-comp_by_mode["inference"][t]) for t in range(expected_comp)]; deltas=[judg_by_mode["direct"][k]-judg_by_mode["inference"][k] for k in sorted(judg_by_mode["direct"])]
        s["max_comprehension_gap"]=max(gaps); s["judgment_discount"]=mean(deltas); s["positive_variant_fraction"]=sum(x>0 for x in deltas)/len(deltas); out[sid]=s
    return out


def summarize(*,data_path:str|Path,results_path:str|Path,config_path:str|Path,out_path:str|Path|None=None)->dict[str,Any]:
    scenarios=load_scenarios(data_path,strict=True); stats=_aggregate(_read_jsonl(results_path),{s.scenario_id for s in scenarios}); cfg=json.loads(Path(config_path).read_text(encoding="utf-8")); gate=cfg["comprehension_gate"]; strong_cfg=cfg["strong_scenario"]; pass_cfg=cfg["model_pass"]
    rows=[]
    for sid in sorted(stats):
        s=stats[sid]; gated=s["p_yes_direct_min"]>=gate["p_yes_direct_min"] and s["p_yes_inference_min"]>=gate["p_yes_inference_min"] and s["max_comprehension_gap"]<=gate["max_abs_gap"]
        strong=gated and s["p_target_direct"]>=strong_cfg["p_target_direct_min"] and s["judgment_discount"]>=strong_cfg["judgment_discount_min"] and s["positive_variant_fraction"]>=strong_cfg["positive_variant_fraction_min"]
        rows.append({**s,"gated":gated,"strong":strong})
    gated=[r for r in rows if r["gated"]]; discounts=[r["judgment_discount"] for r in gated]; ci_lo,ci_hi=_bootstrap_ci(discounts); by_family={}
    for family in FAMILIES:
        sub=[r for r in gated if r["family"]==family]; by_family[family]={"gated":len(sub),"mean_discount":mean(r["judgment_discount"] for r in sub) if sub else math.nan,"strong":sum(bool(r["strong"]) for r in sub)}
    qualifying_positive_families=sum(by_family[f]["gated"]>=pass_cfg["gated_per_positive_family_min"] and by_family[f]["mean_discount"]>0 for f in FAMILIES)
    strong_families=sum(by_family[f]["strong"]>=pass_cfg["strong_per_family_min"] for f in FAMILIES)
    agg={"total_scenarios":len(rows),"gated_scenarios":len(gated),"mean_judgment_discount":mean(discounts) if discounts else math.nan,"bootstrap_95_ci":[ci_lo,ci_hi],"positive_families":qualifying_positive_families,"strong_families":strong_families,"strong_scenarios":sum(bool(r["strong"]) for r in gated),"positive_discount_fraction":sum(r["judgment_discount"]>0 for r in gated)/len(gated) if gated else 0.0}
    model_pass=agg["gated_scenarios"]>=pass_cfg["gated_scenarios_min"] and agg["mean_judgment_discount"]>=pass_cfg["mean_judgment_discount_min"] and ci_lo>pass_cfg["bootstrap_ci_lower_min"] and agg["positive_families"]>=pass_cfg["positive_families_min"] and agg["strong_families"]>=pass_cfg["strong_families_min"] and agg["strong_scenarios"]>=pass_cfg["strong_scenarios_min"] and agg["positive_discount_fraction"]>=pass_cfg["positive_discount_fraction_min"]
    summary={"model_pass":model_pass,"aggregate":agg,"by_family":by_family,"scenarios":rows}
    if out_path is not None:
        out=Path(out_path); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    return summary
