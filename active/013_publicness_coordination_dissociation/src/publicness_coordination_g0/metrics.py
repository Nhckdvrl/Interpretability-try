from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any
import json
import math
import random

from .data import load_scenarios
from .prompts import ACTION_TEMPLATES, CAPABILITY_PROBES, PARTICIPANTS, VERSIONS


def read_jsonl(path: str) -> list[dict]:
    out = []
    with Path(path).open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if not line.strip(): continue
            try: out.append(json.loads(line))
            except json.JSONDecodeError as exc: raise ValueError(f"invalid results JSONL line {lineno}") from exc
    return out


def bootstrap_ci(values: list[float], *, seed: int, n_boot: int) -> tuple[float, float]:
    if not values: return math.nan, math.nan
    rng = random.Random(seed); n = len(values)
    draws = sorted(mean(values[rng.randrange(n)] for _ in range(n)) for _ in range(n_boot))
    return draws[int(.025*(n_boot-1))], draws[int(.975*(n_boot-1))]


def _assert_metadata(rows: list[dict]) -> None:
    for field in ("model", "family", "revision", "size_b", "requested_dtype"):
        vals = {json.dumps(r.get(field), sort_keys=True) for r in rows}
        if len(vals) != 1: raise ValueError(f"inconsistent run metadata for {field}: {vals}")


def compute_participant_features(*, capability: dict[tuple[str, str], float], capability_min: float,
                                 action: dict[str, dict[str, float]], variants: dict[str, dict[str, list[float]]],
                                 cfg: dict) -> dict[str, Any]:
    cg = cfg["capability_gate"]; sc = cfg["strong_case"]
    required = [capability[(state, probe)] for state in ("private", "public") for probe in CAPABILITY_PROBES]
    capability_gate = min(required) >= cg["min_mean_probe_probability"] and capability_min >= cg["min_probe_variant_probability"]

    metrics = {}
    version_ok = {}
    for version in VERSIONS:
        p = action[version]
        ck_gain = p["explicit_ck"] - p["private"]
        public_gain = p["public"] - p["private"]
        dissociation = ck_gain - public_gain
        ratio = public_gain / ck_gain if ck_gain > 1e-6 else math.inf
        metrics[f"{version}_ck_gain"] = ck_gain
        metrics[f"{version}_public_gain"] = public_gain
        metrics[f"{version}_dissociation"] = dissociation
        metrics[f"{version}_public_use_ratio"] = ratio
        vals = variants[version]
        n = len(vals["ck_gain"])
        if n == 0: raise ValueError("variant matrix is empty")
        version_ok[version] = mean(float(
            vals["ck_gain"][i] >= sc["min_explicit_ck_gain"]
            and vals["dissociation"][i] >= sc["min_dissociation"]
            and vals["public_use_ratio"][i] <= sc["max_public_use_ratio"]
        ) for i in range(n))

    action_capability = capability_gate and metrics["primary_ck_gain"] >= sc["min_explicit_ck_gain"]
    target = (
        action_capability
        and metrics["primary_dissociation"] >= sc["min_dissociation"]
        and metrics["primary_public_use_ratio"] <= sc["max_public_use_ratio"]
    )
    controls = (
        metrics["paraphrase_dissociation"] >= sc["min_control_dissociation"]
        and metrics["length_dissociation"] >= sc["min_control_dissociation"]
        and metrics["paraphrase_public_use_ratio"] <= sc["max_control_public_use_ratio"]
        and metrics["length_public_use_ratio"] <= sc["max_control_public_use_ratio"]
        and all(version_ok[v] >= sc["min_variant_signature_fraction"] for v in VERSIONS)
    )
    strong = target and controls
    return {
        "capability_gate": capability_gate,
        "action_capability": action_capability,
        "target_dissociation": target,
        "controls_robust": controls,
        "strong": strong,
        "capability_min_variant_probability": capability_min,
        "primary_variant_signature_fraction": version_ok["primary"],
        "paraphrase_variant_signature_fraction": version_ok["paraphrase"],
        "length_variant_signature_fraction": version_ok["length"],
        **metrics,
    }


def summarize(*, data_path: str, results_path: str, config_path: str,
              out_path: str | None = None) -> dict[str, Any]:
    scenarios = load_scenarios(data_path, require_external_source=True)
    by_id = {s.scenario_id: s for s in scenarios}
    rows = read_jsonl(results_path)
    if not rows: raise ValueError("results are empty")
    _assert_metadata(rows)
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
    grouped: dict[str, list[dict]] = defaultdict(list); seen = set()
    for r in rows:
        sid = str(r.get("scenario_id"))
        if sid not in by_id: raise ValueError(f"unknown scenario_id={sid}")
        if r.get("kind") == "capability_probe":
            key = (sid, "cap", r["participant"], r["state"], r["probe"], int(r["label_order"]))
        elif r.get("kind") == "action_readout":
            key = (sid, "act", r["participant"], r["state"], r["version"], int(r["template_id"]), int(r["label_order"]))
        else: raise ValueError(f"unknown kind={r.get('kind')}")
        if key in seen: raise ValueError(f"duplicate result variant={key}")
        seen.add(key); grouped[sid].append(r)
    if set(grouped) != set(by_id): raise ValueError(f"scenario coverage mismatch missing={sorted(set(by_id)-set(grouped))}")

    expected_cap = {(who,state,probe,o) for who in PARTICIPANTS for state in ("private","public") for probe in CAPABILITY_PROBES for o in (0,1)}
    expected_act = {(who,state,v,t,o) for who in PARTICIPANTS for v in VERSIONS for state in ("private","public","explicit_ck") for t in range(len(ACTION_TEMPLATES)) for o in (0,1)}
    participants = []; pairs = []
    for sid in sorted(by_id):
        rs=grouped[sid]; cr=[r for r in rs if r["kind"]=="capability_probe"]; ar=[r for r in rs if r["kind"]=="action_readout"]
        if {(r["participant"],r["state"],r["probe"],int(r["label_order"])) for r in cr} != expected_cap:
            raise ValueError(f"{sid}: malformed capability coverage")
        if {(r["participant"],r["state"],r["version"],int(r["template_id"]),int(r["label_order"])) for r in ar} != expected_act:
            raise ValueError(f"{sid}: malformed action coverage")
        entries=[]
        for who in PARTICIPANTS:
            cc=[r for r in cr if r["participant"]==who]
            capability={(state,probe):mean(float(r["p_correct"]) for r in cc if r["state"]==state and r["probe"]==probe) for state in ("private","public") for probe in CAPABILITY_PROBES}
            capability_min=min(float(r["p_correct"]) for r in cc)
            aa=[r for r in ar if r["participant"]==who]
            action={}
            variants={}
            for v in VERSIONS:
                vr=[r for r in aa if r["version"]==v]
                action[v]={state:mean(float(r["p_coordinate"]) for r in vr if r["state"]==state) for state in ("private","public","explicit_ck")}
                vals={"ck_gain":[],"dissociation":[],"public_use_ratio":[]}
                for tid in range(len(ACTION_TEMPLATES)):
                    for order in (0,1):
                        cell={r["state"]:float(r["p_coordinate"]) for r in vr if int(r["template_id"])==tid and int(r["label_order"])==order}
                        ck=cell["explicit_ck"]-cell["private"]; pub=cell["public"]-cell["private"]; dis=ck-pub
                        vals["ck_gain"].append(ck); vals["dissociation"].append(dis); vals["public_use_ratio"].append(pub/ck if ck>1e-6 else math.inf)
                variants[v]=vals
            f=compute_participant_features(capability=capability, capability_min=capability_min, action=action, variants=variants, cfg=cfg)
            e={"scenario_id":sid,"domain":by_id[sid].domain,"participant":who,
               "capability":{"|".join(k):v for k,v in capability.items()},**f}
            participants.append(e); entries.append(e)
        pair={
            "scenario_id":sid,"domain":by_id[sid].domain,
            "capability_gated":all(e["capability_gate"] for e in entries),
            "action_capable":all(e["action_capability"] for e in entries),
            "strong":all(e["strong"] for e in entries),
            "primary_dissociation_mean":mean(e["primary_dissociation"] for e in entries),
            "primary_ck_gain_mean":mean(e["primary_ck_gain"] for e in entries),
            "primary_public_gain_mean":mean(e["primary_public_gain"] for e in entries),
            "participant_asymmetry":abs(entries[0]["primary_dissociation"]-entries[1]["primary_dissociation"]),
            "controls_robust":all(e["controls_robust"] for e in entries),
        }
        pairs.append(pair)

    capable=[p for p in pairs if p["action_capable"]]
    diss=[p["primary_dissociation_mean"] for p in capable]
    ci=bootstrap_ci(diss,seed=cfg["seed"],n_boot=cfg["bootstrap_samples"])
    agg={
        "scenario_pairs":len(pairs),
        "capability_gated_pairs":sum(p["capability_gated"] for p in pairs),
        "action_capable_pairs":len(capable),
        "strong_pairs":sum(p["strong"] for p in capable),
        "strong_pair_fraction":mean(float(p["strong"]) for p in capable) if capable else 0.0,
        "controls_robust_fraction":mean(float(p["controls_robust"]) for p in capable) if capable else 0.0,
        "mean_primary_dissociation":mean(diss) if diss else math.nan,
        "dissociation_ci95":ci,
        "mean_public_use_ratio":mean(p["primary_public_gain_mean"]/p["primary_ck_gain_mean"] for p in capable if p["primary_ck_gain_mean"]>1e-6) if any(p["primary_ck_gain_mean"]>1e-6 for p in capable) else math.nan,
        "agent_asymmetry_fraction":mean(float(p["participant_asymmetry"]>cfg["strong_case"]["max_participant_dissociation_asymmetry"]) for p in capable) if capable else 0.0,
        "positive_domains":len({p["domain"] for p in capable if p["strong"]}),
    }
    pc=cfg["model_pass"]
    total=len(pairs)
    cap_frac=agg["capability_gated_pairs"]/total if total else 0.0
    action_frac=len(capable)/total if total else 0.0
    model_pass=(
        len(capable)>=pc["min_action_capable_pairs"]
        and agg["strong_pair_fraction"]>=pc["min_strong_pair_fraction"]
        and agg["controls_robust_fraction"]>=pc["min_controls_robust_fraction"]
        and agg["mean_primary_dissociation"]>=pc["min_mean_dissociation"]
        and ci[0]>=pc["min_dissociation_ci_lower"]
        and agg["agent_asymmetry_fraction"]<=pc["max_agent_asymmetry_fraction"]
        and agg["positive_domains"]>=pc["min_positive_domains"]
    )
    if cap_frac<pc["min_capability_gated_fraction"]:
        verdict="HARD-KILL-PUBLICNESS-TOM-CAPABILITY-FLOOR"
    elif action_frac<pc["min_action_capable_fraction"]:
        verdict="HARD-KILL-COORDINATION-POLICY-CAPABILITY-FLOOR"
    elif math.isfinite(agg["mean_primary_dissociation"]) and agg["mean_primary_dissociation"]<pc["no_effect_dissociation"]:
        verdict="HARD-KILL-NO-PUBLICNESS-COORDINATION-DISSOCIATION"
    elif agg["controls_robust_fraction"]<pc["min_controls_robust_fraction"]:
        verdict="HOLD-WORDING-OR-LENGTH-ARTIFACT"
    elif agg["agent_asymmetry_fraction"]>pc["max_agent_asymmetry_fraction"]:
        verdict="HOLD-PARTICIPANT-ASYMMETRY"
    elif model_pass:
        verdict="PASS-TO-PANEL"
    else:
        verdict="HOLD-BELOW-PROMOTION-THRESHOLD"
    result={"model":rows[0]["model"],"family":rows[0]["family"],"revision":rows[0].get("revision"),"size_b":rows[0]["size_b"],
            "requested_dtype":rows[0].get("requested_dtype"),"participants":participants,"pairs":pairs,"aggregate":agg,
            "model_pass":model_pass,"verdict":verdict}
    if out_path: Path(out_path).write_text(json.dumps(result,indent=2,allow_nan=True),encoding="utf-8")
    return result
