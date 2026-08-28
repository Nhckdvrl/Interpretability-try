from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any
import json, math, random
from .data import load_scenarios
from .prompts import READOUT_TEMPLATES

READOUTS = ("probability", "decision", "frequency")
PRIMARY_READOUTS = ("probability", "decision")
RECOGNITION_PROBES = ("focal_equivalent", "focal_disjoint", "focal_exhaustive", "complement_equivalent", "complement_disjoint", "complement_exhaustive", "pair_disjoint", "pair_exhaustive")

def read_jsonl(path):
    out=[]
    with Path(path).open(encoding="utf-8") as f:
        for i,line in enumerate(f,1):
            if line.strip():
                try: out.append(json.loads(line))
                except json.JSONDecodeError as e: raise ValueError(f"invalid results JSONL line {i}") from e
    return out

def bootstrap_ci(values, *, seed, n_boot):
    if not values: return math.nan, math.nan
    rng=random.Random(seed); n=len(values)
    draws=sorted(mean(values[rng.randrange(n)] for _ in range(n)) for _ in range(n_boot))
    return draws[int(.025*(n_boot-1))], draws[int(.975*(n_boot-1))]

def _variant_bias(r):
    return (float(r["p_right_more"])-float(r["p_left_more"])) if r["variant_side"]=="right" else (float(r["p_left_more"])-float(r["p_right_more"]))
def _variant_more_prob(r): return float(r["p_right_more"] if r["variant_side"]=="right" else r["p_left_more"])
def _focal_score(r): return (float(r["p_left_more"])-float(r["p_right_more"])) if r["focal_side"]=="left" else (float(r["p_right_more"])-float(r["p_left_more"]))

def summarize(*, data_path: str, results_path: str, config_path: str, out_path: str | None=None) -> dict[str,Any]:
    scenarios=load_scenarios(data_path, require_external_source=True); valid={(s.scenario_id,p.partition_id) for s in scenarios for p in s.partitions}; rows=read_jsonl(results_path)
    if not rows: raise ValueError("results are empty")
    cfg=json.loads(Path(config_path).read_text(encoding="utf-8")); grouped=defaultdict(list); seen=set()
    for r in rows:
        key=(str(r["scenario_id"]),str(r["partition_id"]))
        if key not in valid: raise ValueError(f"unknown result key={key}")
        if r["kind"]=="recognition": u=key+("r",r["probe"],int(r["label_order"]))
        elif r["kind"] in {"judgment","focal_alternative"}: u=key+(r["kind"],r["readout"],r["template_kind"],int(r["template_id"]),r["condition"],int(r["side_order"]),int(r["label_order"]))
        else: raise ValueError(f"unknown kind={r['kind']}")
        if u in seen: raise ValueError(f"duplicate result variant={u}")
        seen.add(u); grouped[key].append(r)
    if valid-set(grouped): raise ValueError(f"missing result groups; first={sorted(valid-set(grouped))[:3]}")
    rec_cfg=cfg["recognition_gate"]; ctrl=cfg["artifact_controls"]; strong_cfg=cfg["strong_case"]
    expected_rec={(p,o) for p in RECOGNITION_PROBES for o in (0,1)}
    expected_j={(ro,kind,tid,c,so,lo) for ro in READOUTS for tid,(kind,_) in enumerate(READOUT_TEMPLATES[ro]) for c in ("core","reordered","paraphrase","partial_subset","repacked") for so in (0,1) for lo in range(6)}
    expected_f={(ro,kind,tid,c,so,lo) for ro in READOUTS for tid,(kind,_) in enumerate(READOUT_TEMPLATES[ro]) for c in ("baseline","focal_unpacked","alternative_unpacked","focal_length_control","alternative_length_control") for so in (0,1) for lo in range(6)}
    cases=[]
    for key in sorted(valid):
        rs=grouped[key]; rec=[r for r in rs if r["kind"]=="recognition"]
        if {(r["probe"],int(r["label_order"])) for r in rec}!=expected_rec: raise ValueError(f"{key}: malformed recognition coverage")
        rp={p:mean(float(r["p_correct"]) for r in rec if r["probe"]==p) for p in RECOGNITION_PROBES}; gated=min(rp.values())>=rec_cfg["min_probe_probability"] and mean(rp.values())>=rec_cfg["min_mean_probability"]
        js=[r for r in rs if r["kind"]=="judgment"]
        if {(r["readout"],r["template_kind"],int(r["template_id"]),r["condition"],int(r["side_order"]),int(r["label_order"])) for r in js}!=expected_j: raise ValueError(f"{key}: malformed judgment coverage")
        fs=[r for r in rs if r["kind"]=="focal_alternative"]
        if {(r["readout"],r["template_kind"],int(r["template_id"]),r["condition"],int(r["side_order"]),int(r["label_order"])) for r in fs}!=expected_f: raise ValueError(f"{key}: malformed focal/alternative coverage")
        natural=[r for r in js if r["template_kind"]=="natural"]; reminder=[r for r in js if r["template_kind"]=="extensional_reminder"]; pn=[r for r in natural if r["readout"] in PRIMARY_READOUTS]; pr=[r for r in reminder if r["readout"] in PRIMARY_READOUTS]
        def mb(sub,c,ro=None):
            z=[r for r in sub if r["condition"]==c and (ro is None or r["readout"]==ro)]; return mean(_variant_bias(r) for r in z)
        def mp(sub,c): return mean(_variant_more_prob(r) for r in sub if r["condition"]==c)
        core=mb(pn,"core"); reordered=mb(pn,"reordered"); paraphrase=mb(pn,"paraphrase"); partial=-mb(pn,"partial_subset"); repacked=mb(pn,"repacked"); reorder_gap=abs(core-reordered); repack_recovery=core-repacked; reminder_core=mb(pr,"core")
        fn=[r for r in fs if r["template_kind"]=="natural" and r["readout"] in PRIMARY_READOUTS]; fscore={c:mean(_focal_score(r) for r in fn if r["condition"]==c) for c in ("baseline","focal_unpacked","alternative_unpacked","focal_length_control","alternative_length_control")}
        focal_unpack=fscore["focal_unpacked"]-fscore["baseline"]; alt_unpack=fscore["alternative_unpacked"]-fscore["baseline"]; focal_len=fscore["focal_length_control"]-fscore["baseline"]; alt_len=fscore["alternative_length_control"]-fscore["baseline"]; focal_alt=(focal_unpack-focal_len)-(alt_unpack-alt_len)
        rb={ro:mb(natural,"core",ro) for ro in READOUTS}; template_bias={f"{ro}:{tid}":mean(_variant_bias(r) for r in natural if r["readout"]==ro and int(r["template_id"])==tid and r["condition"]=="core") for ro in PRIMARY_READOUTS for tid,(kind,_) in enumerate(READOUT_TEMPLATES[ro]) if kind=="natural"}; tpl_frac=mean(float(v>0) for v in template_bias.values())
        control_ok=abs(paraphrase)<=ctrl["max_abs_paraphrase_bias"] and partial>=ctrl["min_partial_subset_discrimination"] and reorder_gap<=ctrl["max_reorder_gap"]
        structural_ok=repack_recovery>=strong_cfg["min_repacking_recovery"] and focal_alt>=strong_cfg["min_unpacked_specific_focal_alternative_shift"] and all(rb[r]>0 for r in PRIMARY_READOUTS) and tpl_frac>=strong_cfg["min_natural_template_positive_fraction"]
        strong=gated and control_ok and structural_ok and core>=strong_cfg["min_core_unpacked_bias"] and mp(pn,"core")>=strong_cfg["min_unpacked_more_probability"]
        cases.append({"scenario_id":key[0],"partition_id":key[1],"domain":rs[0]["domain"],"branch_count":int(rs[0]["branch_count"]),"branch_count_family":rs[0]["branch_count_family"],"recognition":rp,"gated":gated,"core_unpacked_bias":core,"core_bias_by_readout":rb,"natural_template_core_bias":template_bias,"natural_template_positive_fraction":tpl_frac,"paraphrase_bias":paraphrase,"partial_subset_discrimination":partial,"reordered_bias":reordered,"reorder_gap":reorder_gap,"repacking_recovery":repack_recovery,"unpacking_specific_focal_alternative_shift":focal_alt,"reminder_rescue":core-reminder_core,"control_ok":control_ok,"structural_ok":structural_ok,"strong":strong})
    by_sid=defaultdict(list)
    for r in cases:
        if r["gated"]: by_sid[r["scenario_id"]].append(r)
    scenarios_out=[]
    for sid,sub in sorted(by_sid.items()): scenarios_out.append({"scenario_id":sid,"domain":sub[0]["domain"],"mean_core_unpacked_bias":mean(r["core_unpacked_bias"] for r in sub),"mean_focal_alternative_shift":mean(r["unpacking_specific_focal_alternative_shift"] for r in sub),"mean_repacking_recovery":mean(r["repacking_recovery"] for r in sub),"mean_template_positive_fraction":mean(r["natural_template_positive_fraction"] for r in sub),"control_ok_fraction":mean(float(r["control_ok"]) for r in sub),"strong":mean(float(r["strong"]) for r in sub)>=.5})
    vals=[r["mean_core_unpacked_bias"] for r in scenarios_out]; lo,hi=bootstrap_ci(vals,seed=cfg["seed"],n_boot=cfg["bootstrap_samples"]); by_domain={}
    for d in sorted({r["domain"] for r in scenarios_out}):
        sub=[r for r in scenarios_out if r["domain"]==d]; by_domain[d]={"gated_scenarios":len(sub),"mean_core_unpacked_bias":mean(r["mean_core_unpacked_bias"] for r in sub),"strong_scenarios":sum(r["strong"] for r in sub)}
    slopes={}; groups=defaultdict(list)
    for r in cases:
        if r["gated"]: groups[(r["scenario_id"],r["branch_count_family"])].append(r)
    for (sid,fam),sub in groups.items():
        bk=defaultdict(list)
        for r in sub: bk[r["branch_count"]].append(r["core_unpacked_bias"])
        ks=sorted(bk)
        if len(ks)>=2 and ks[-1]!=ks[0]: slopes[f"{sid}::{fam}"]=(mean(bk[ks[-1]])-mean(bk[ks[0]]))/(ks[-1]-ks[0])
    agg={"gated_scenarios":len(scenarios_out),"mean_core_unpacked_bias":mean(vals) if vals else math.nan,"bootstrap_95_ci_clustered_by_scenario":[lo,hi],"strong_fraction":mean(float(r["strong"]) for r in scenarios_out) if scenarios_out else 0.0,"positive_domains":sum(v["gated_scenarios"]>=2 and v["mean_core_unpacked_bias"]>0 for v in by_domain.values()),"mean_focal_alternative_shift":mean(r["mean_focal_alternative_shift"] for r in scenarios_out) if scenarios_out else math.nan,"mean_template_positive_fraction":mean(r["mean_template_positive_fraction"] for r in scenarios_out) if scenarios_out else math.nan,"branch_count_matched_groups":len(slopes),"mean_within_family_branch_count_slope":mean(slopes.values()) if slopes else math.nan,"artifact_failure_scenarios":sum(r["control_ok_fraction"]<.75 for r in scenarios_out)}
    pc=cfg["model_pass"]; branch_ok=agg["branch_count_matched_groups"]>=pc["min_branch_count_matched_groups"] and agg["mean_within_family_branch_count_slope"]>=pc["min_mean_branch_count_slope"]
    model_pass=agg["gated_scenarios"]>=pc["min_gated_scenarios"] and agg["mean_core_unpacked_bias"]>=pc["min_mean_core_unpacked_bias"] and lo>=pc["min_bootstrap_ci_lower"] and agg["strong_fraction"]>=pc["min_strong_fraction"] and agg["positive_domains"]>=pc["min_positive_domains"] and agg["mean_focal_alternative_shift"]>=pc["min_mean_focal_alternative_shift"] and agg["mean_template_positive_fraction"]>=pc["min_natural_template_positive_fraction"] and branch_ok
    if agg["gated_scenarios"]>=pc["min_gated_scenarios"] and abs(agg["mean_core_unpacked_bias"])<.02: verdict="HARD-KILL-NO-PHENOMENON"
    elif agg["artifact_failure_scenarios"]>max(2,agg["gated_scenarios"]//4): verdict="HOLD-ARTIFACT-CONTROLS"
    elif not branch_ok: verdict="HOLD-BRANCH-COUNT-STRUCTURE"
    else: verdict="PASS-TO-PANEL" if model_pass else "FAIL-MODEL-G0"
    summary={"contract":"Packed-Unpacked Event Splitting","model":rows[0].get("model"),"family":rows[0].get("family"),"revision":rows[0].get("revision"),"size_b":rows[0].get("size_b"),"model_pass":model_pass,"verdict":verdict,"aggregate":agg,"by_domain":by_domain,"within_refinement_family_branch_count_slopes":slopes,"scenarios":scenarios_out,"cases":cases,"hard_kill_note":"Primary evidence is natural probability+decision behavior after focal/complement relation gates. Generic wording/position/order/length effects, an unstructured branch-count pattern, or failure of repacking/focal-alternative diagnostics block promotion."}
    if out_path:
        p=Path(out_path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=True),encoding="utf-8")
    return summary
