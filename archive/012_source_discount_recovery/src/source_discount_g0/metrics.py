from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any
import json
import math
import random

from .data import load_scenarios
from .prompts import CONDITIONS, DIRECTIONS, MEMORY_PROBES, READOUT_TEMPLATES, SOURCES, SUPPORT_PROBES


def read_jsonl(path: str) -> list[dict]:
    out = []
    with Path(path).open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid results JSONL line {lineno}") from exc
    return out


def bootstrap_ci(values: list[float], *, seed: int, n_boot: int) -> tuple[float, float]:
    if not values:
        return math.nan, math.nan
    if n_boot <= 0:
        raise ValueError("n_boot must be > 0")
    rng = random.Random(seed)
    n = len(values)
    draws = sorted(mean(values[rng.randrange(n)] for _ in range(n)) for _ in range(n_boot))
    return draws[int(.025 * (n_boot - 1))], draws[int(.975 * (n_boot - 1))]


def cell_bootstrap_ci(cell_values: dict[str, list[float]], *, seed: int, n_boot: int) -> tuple[float, float]:
    """Resample eligible cells, then scenarios within each resampled cell.

    The estimator weights every eligible cell equally, so the cell is the unit the
    interval must be built on: a cell holding fifteen source pairs is not fifteen
    independent draws on the question the headline asks. Capability is deliberately not
    a third level — the primary set has three capabilities contributing two, three and
    three eligible cells, so resampling capabilities first would hand capability 53 the
    same third of the weight as the two capabilities that carry more cells, which is a
    new arbitrary weighting rather than a correction for one.
    """
    keys = sorted(cell_values)
    if not keys:
        return math.nan, math.nan
    if n_boot <= 0:
        raise ValueError("n_boot must be > 0")
    rng = random.Random(seed)
    draws = []
    for _ in range(n_boot):
        cell_means = []
        for _ in range(len(keys)):
            values = cell_values[keys[rng.randrange(len(keys))]]
            n = len(values)
            cell_means.append(mean(values[rng.randrange(n)] for _ in range(n)))
        draws.append(mean(cell_means))
    draws.sort()
    return draws[int(.025 * (n_boot - 1))], draws[int(.975 * (n_boot - 1))]


def signed_influence(direction: str, p_message: float, p_baseline: float) -> float:
    raw = p_message - p_baseline
    if direction == "supports_target":
        return raw
    if direction == "supports_other":
        return -raw
    raise ValueError(direction)


def _assert_metadata(rows: list[dict]) -> None:
    for field in ("model", "family", "revision", "size_b", "requested_dtype"):
        vals = {json.dumps(r.get(field), sort_keys=True) for r in rows}
        if len(vals) != 1:
            raise ValueError(f"inconsistent run metadata for {field}: {vals}")


def compute_direction_features(*, support: dict[str, float], support_min: float,
                               memory: dict[tuple[str, str, str], float], memory_min: float,
                               readouts: dict[str, dict[str, float]],
                               variant_readouts: dict[str, dict[str, list[float]]], cfg: dict) -> dict[str, Any]:
    sg = cfg["support_gate"]
    mg = cfg["memory_gate"]
    sc = cfg["strong_case"]
    support_gate = (
        support["low_positive"] >= sg["min_low_positive_probability"]
        and support["high_positive"] >= sg["min_high_positive_probability"]
        and support["high_gt_low"] >= sg["min_high_gt_low_probability"]
        and support_min >= sg["min_probe_variant_probability"]
    )
    required_memory = [
        memory[(source, delay, probe)]
        for source in SOURCES for delay in ("short", "long") for probe in MEMORY_PROBES
    ]
    memory_gate = min(required_memory) >= mg["min_mean_probe_probability"] and memory_min >= mg["min_probe_variant_probability"]

    features: dict[str, float] = {}
    variant_ok: dict[str, float] = {}
    for kind in ("belief", "action"):
        r = readouts[kind]
        low_i = r["low_immediate"]
        high_i = r["high_immediate"]
        low_l = r["low_long"]
        high_l = r["high_long"]
        low_re = r["low_long_reinstated"]
        high_re = r["high_long_reinstated"]
        low_len = r["low_long_length"]
        high_len = r["high_long_length"]
        initial_gap = high_i - low_i
        long_gap = high_l - low_l
        reinstated_gap = high_re - low_re
        length_gap = high_len - low_len
        low_rebound = low_l - low_i
        gap_shrink = initial_gap - long_gap
        reinstatement_gain = reinstated_gap - long_gap
        length_gain = length_gap - long_gap
        high_retention = high_l / max(high_i, 1e-6)
        features.update({
            f"{kind}_initial_gap": initial_gap,
            f"{kind}_long_gap": long_gap,
            f"{kind}_low_rebound": low_rebound,
            f"{kind}_gap_shrink": gap_shrink,
            f"{kind}_high_retention": high_retention,
            f"{kind}_reinstatement_gain": reinstatement_gain,
            f"{kind}_length_gain": length_gain,
            f"{kind}_selective_reinstatement": reinstatement_gain - length_gain,
            f"{kind}_baseline_drift": abs(r["baseline_long"] - r["baseline_immediate"]),
        })
        vals = variant_readouts[kind]
        n = len(vals["initial_gap"])
        if n == 0:
            raise ValueError("variant matrix is empty")
        variant_ok[kind] = mean(
            float(
                vals["initial_gap"][i] >= sc[f"min_{kind}_initial_discount_gap"]
                and vals["low_rebound"][i] >= sc[f"min_{kind}_low_rebound"]
                and vals["gap_shrink"][i] >= sc[f"min_{kind}_gap_shrink"]
                and vals["selective_reinstatement"][i] >= sc[f"min_{kind}_selective_reinstatement"]
            ) for i in range(n)
        )

    weighting_capability = (
        support_gate and memory_gate
        and readouts["belief"]["low_immediate"] >= sc["min_belief_low_initial_influence"]
        and readouts["belief"]["high_immediate"] >= sc["min_belief_high_initial_influence"]
        and readouts["action"]["low_immediate"] >= sc["min_action_low_initial_influence"]
        and readouts["action"]["high_immediate"] >= sc["min_action_high_initial_influence"]
        and features["belief_initial_gap"] >= sc["min_belief_initial_discount_gap"]
        and features["action_initial_gap"] >= sc["min_action_initial_discount_gap"]
    )
    generic_delay_ok = (
        features["belief_high_retention"] >= sc["min_high_source_retention_fraction"]
        and features["action_high_retention"] >= sc["min_high_source_retention_fraction"]
        and features["belief_baseline_drift"] <= sc["max_no_message_baseline_drift"]
        and features["action_baseline_drift"] <= sc["max_no_message_baseline_drift"]
    )
    recovery = (
        features["belief_low_rebound"] >= sc["min_belief_low_rebound"]
        and features["action_low_rebound"] >= sc["min_action_low_rebound"]
        and features["belief_gap_shrink"] >= sc["min_belief_gap_shrink"]
        and features["action_gap_shrink"] >= sc["min_action_gap_shrink"]
    )
    reinstatement = (
        features["belief_reinstatement_gain"] >= sc["min_belief_reinstatement_gain"]
        and features["action_reinstatement_gain"] >= sc["min_action_reinstatement_gain"]
        and features["belief_selective_reinstatement"] >= sc["min_belief_selective_reinstatement"]
        and features["action_selective_reinstatement"] >= sc["min_action_selective_reinstatement"]
        and abs(features["belief_length_gain"]) <= sc["max_matched_length_gap_change"]
        and abs(features["action_length_gain"]) <= sc["max_matched_length_gap_change"]
    )
    variant_consistent = (
        variant_ok["belief"] >= sc["min_variant_signature_fraction"]
        and variant_ok["action"] >= sc["min_variant_signature_fraction"]
    )
    strong = weighting_capability and generic_delay_ok and recovery and reinstatement and variant_consistent
    return {
        "support_gate": support_gate, "memory_gate": memory_gate,
        "weighting_capability": weighting_capability, "generic_delay_ok": generic_delay_ok,
        "recovery": recovery, "reinstatement": reinstatement,
        "variant_consistent": variant_consistent, "strong": strong,
        "support_min_variant_probability": support_min,
        "memory_min_variant_probability": memory_min,
        "belief_variant_signature_fraction": variant_ok["belief"],
        "action_variant_signature_fraction": variant_ok["action"],
        **features,
    }


def summarize(*, data_path: str, results_path: str, config_path: str,
              out_path: str | None = None) -> dict[str, Any]:
    scenarios = load_scenarios(data_path, require_external_source=True)
    by_id = {s.scenario_id: s for s in scenarios}
    rows = read_jsonl(results_path)
    if not rows:
        raise ValueError("results are empty")
    _assert_metadata(rows)
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
    grouped: dict[str, list[dict]] = defaultdict(list)
    seen: set[tuple] = set()
    for r in rows:
        sid = str(r.get("scenario_id"))
        if sid not in by_id:
            raise ValueError(f"unknown scenario_id={sid}")
        kind = r.get("kind")
        if kind == "support_probe":
            key = (sid, kind, r["direction"], r["probe"], int(r["label_order"]))
        elif kind == "memory_probe":
            key = (sid, kind, r["direction"], r["source"], r["delay"], r["probe"], int(r["label_order"]))
        elif kind == "readout":
            key = (sid, kind, r["direction"], r["condition"], int(r["template_id"]), int(r["label_order"]))
        else:
            raise ValueError(f"unknown kind={kind}")
        if key in seen:
            raise ValueError(f"duplicate result variant={key}")
        seen.add(key)
        grouped[sid].append(r)
    if set(grouped) != set(by_id):
        raise ValueError(f"scenario coverage mismatch missing={sorted(set(by_id)-set(grouped))}")

    expected_support = {(d, p, o) for d in DIRECTIONS for p in SUPPORT_PROBES for o in (0, 1)}
    expected_memory = {(d, s, delay, p, o) for d in DIRECTIONS for s in SOURCES for delay in ("short", "long") for p in MEMORY_PROBES for o in (0, 1)}
    expected_readout = {(d, c, t, o) for d in DIRECTIONS for c in CONDITIONS for t in range(len(READOUT_TEMPLATES)) for o in (0, 1)}

    directions = []
    pairs = []
    for sid in sorted(by_id):
        rs = grouped[sid]
        sr = [r for r in rs if r["kind"] == "support_probe"]
        mr = [r for r in rs if r["kind"] == "memory_probe"]
        rr = [r for r in rs if r["kind"] == "readout"]
        if {(r["direction"], r["probe"], int(r["label_order"])) for r in sr} != expected_support:
            raise ValueError(f"{sid}: malformed support coverage")
        if {(r["direction"], r["source"], r["delay"], r["probe"], int(r["label_order"])) for r in mr} != expected_memory:
            raise ValueError(f"{sid}: malformed memory coverage")
        if {(r["direction"], r["condition"], int(r["template_id"]), int(r["label_order"])) for r in rr} != expected_readout:
            raise ValueError(f"{sid}: malformed readout coverage")

        dir_entries = []
        for direction in DIRECTIONS:
            ss = [r for r in sr if r["direction"] == direction]
            support = {p: mean(float(r["p_correct"]) for r in ss if r["probe"] == p) for p in SUPPORT_PROBES}
            support_min = min(float(r["p_correct"]) for r in ss)
            mm = [r for r in mr if r["direction"] == direction]
            memory = {(source, delay, probe): mean(float(r["p_correct"]) for r in mm if r["source"] == source and r["delay"] == delay and r["probe"] == probe) for source in SOURCES for delay in ("short", "long") for probe in MEMORY_PROBES}
            memory_min = min(float(r["p_correct"]) for r in mm)

            norm: dict[str, dict[str, float]] = {}
            variants: dict[str, dict[str, list[float]]] = {}
            for kind in ("belief", "action"):
                kr = [r for r in rr if r["direction"] == direction and r["template_kind"] == kind]
                p = {c: mean(float(r["p_target"]) for r in kr if r["condition"] == c) for c in CONDITIONS}
                n = {
                    "baseline_immediate": p["no_message_immediate"],
                    "baseline_long": p["no_message_long"],
                }
                for source in SOURCES:
                    for delay in ("immediate", "short", "long"):
                        n[f"{source}_{delay}"] = signed_influence(direction, p[f"{source}_{delay}"], p[f"no_message_{delay}"])
                    n[f"{source}_long_reinstated"] = signed_influence(direction, p[f"{source}_long_reinstated"], p["no_message_long"])
                    n[f"{source}_long_length"] = signed_influence(direction, p[f"{source}_long_length"], p["no_message_long"])
                norm[kind] = n

                v = {k: [] for k in ("initial_gap", "low_rebound", "gap_shrink", "selective_reinstatement")}
                template_ids = sorted({int(r["template_id"]) for r in kr})
                for tid in template_ids:
                    for order in (0, 1):
                        cell = {(r["condition"]): float(r["p_target"]) for r in kr if int(r["template_id"]) == tid and int(r["label_order"]) == order}
                        def inf(cond: str, base: str) -> float:
                            return signed_influence(direction, cell[cond], cell[base])
                        low_i = inf("low_immediate", "no_message_immediate")
                        high_i = inf("high_immediate", "no_message_immediate")
                        low_l = inf("low_long", "no_message_long")
                        high_l = inf("high_long", "no_message_long")
                        low_re = inf("low_long_reinstated", "no_message_long")
                        high_re = inf("high_long_reinstated", "no_message_long")
                        low_len = inf("low_long_length", "no_message_long")
                        high_len = inf("high_long_length", "no_message_long")
                        initial = high_i - low_i
                        long_gap = high_l - low_l
                        rein_gain = (high_re - low_re) - long_gap
                        len_gain = (high_len - low_len) - long_gap
                        v["initial_gap"].append(initial)
                        v["low_rebound"].append(low_l - low_i)
                        v["gap_shrink"].append(initial - long_gap)
                        v["selective_reinstatement"].append(rein_gain - len_gain)
                variants[kind] = v

            features = compute_direction_features(
                support=support, support_min=support_min, memory=memory, memory_min=memory_min,
                readouts=norm, variant_readouts=variants, cfg=cfg,
            )
            entry = {"scenario_id": sid, "domain": by_id[sid].domain, "cell_id": by_id[sid].cell_id, "direction": direction,
                     "support": support, "memory": {"|".join(k): v for k, v in memory.items()}, **features}
            directions.append(entry)
            dir_entries.append(entry)

        pair = {
            "scenario_id": sid,
            "domain": by_id[sid].domain,
            "cell_id": by_id[sid].cell_id,
            "support_gated": all(x["support_gate"] for x in dir_entries),
            "memory_gated": all(x["memory_gate"] for x in dir_entries),
            "weighting_capable": all(x["weighting_capability"] for x in dir_entries),
            "generic_delay_ok": all(x["generic_delay_ok"] for x in dir_entries),
            "recovery": all(x["recovery"] for x in dir_entries),
            "reinstatement": all(x["reinstatement"] for x in dir_entries),
            "strong": all(x["strong"] for x in dir_entries),
            "belief_gap_shrink_mean": mean(x["belief_gap_shrink"] for x in dir_entries),
            "action_gap_shrink_mean": mean(x["action_gap_shrink"] for x in dir_entries),
            "belief_low_rebound_mean": mean(x["belief_low_rebound"] for x in dir_entries),
            "action_low_rebound_mean": mean(x["action_low_rebound"] for x in dir_entries),
            "belief_reinstatement_gain_mean": mean(x["belief_reinstatement_gain"] for x in dir_entries),
            "action_reinstatement_gain_mean": mean(x["action_reinstatement_gain"] for x in dir_entries),
        }
        pairs.append(pair)

    pc = cfg["model_pass"]

    # Stratum membership is fixed by the frozen bank, before any model call: a cell is
    # primary if the D0 bank gave it at least `min_primary_cell_size` scenarios. It is
    # never decided from how the cell performed, and an undersized cell can never be
    # promoted into the inferential set after the fact.
    min_cell = int(pc["min_primary_cell_size"])
    bank_cell_size: dict[str, int] = defaultdict(int)
    cell_domain: dict[str, str] = {}
    for s in scenarios:
        bank_cell_size[s.cell_id] += 1
        cell_domain[s.cell_id] = s.domain
    primary_cells = {c for c, n in bank_cell_size.items() if n >= min_cell}
    secondary_cells = set(bank_cell_size) - primary_cells

    def gap_of(p: dict) -> float:
        return mean((p["belief_gap_shrink_mean"], p["action_gap_shrink_mean"]))

    eligible = [p for p in pairs if p["weighting_capable"]]
    primary_pairs = [p for p in pairs if p["cell_id"] in primary_cells]
    primary_eligible = [p for p in eligible if p["cell_id"] in primary_cells]
    gap_vals = [gap_of(p) for p in eligible]

    cell_values: dict[str, list[float]] = defaultdict(list)
    for p in primary_eligible:
        cell_values[p["cell_id"]].append(gap_of(p))
    cell_means = {c: mean(v) for c, v in sorted(cell_values.items())}
    cell_mean_gap_shrink = mean(cell_means.values()) if cell_means else math.nan
    ci = cell_bootstrap_ci(dict(cell_values), seed=cfg["seed"], n_boot=cfg["bootstrap_samples"])

    # Capability is reported for heterogeneity only and gates nothing.
    by_capability: dict[str, list[float]] = defaultdict(list)
    for c, m in cell_means.items():
        by_capability[cell_domain[c]].append(m)

    def frac(rows: list[dict], key: str, negate: bool = False) -> float:
        if not rows:
            return 0.0
        return mean(float(not r[key] if negate else r[key]) for r in rows)

    agg = {
        "scenario_pairs": len(pairs),
        "support_gated_pairs": sum(p["support_gated"] for p in pairs),
        "memory_gated_pairs": sum(p["memory_gated"] for p in pairs),
        "weighting_capable_pairs": len(eligible),
        "strong_pairs": sum(p["strong"] for p in eligible),
        "strong_pair_fraction": frac(eligible, "strong"),
        "mean_gap_shrink": mean(gap_vals) if gap_vals else math.nan,
        # --- primary inferential set: cells the frozen bank sized at >= min_primary_cell_size
        "min_primary_cell_size": min_cell,
        "primary_cells": sorted(primary_cells),
        "secondary_cells": sorted(secondary_cells),
        "primary_scenarios": len(primary_pairs),
        "secondary_scenarios": len(pairs) - len(primary_pairs),
        "eligible_cells": sorted(cell_values),
        "primary_weighting_capable_pairs": len(primary_eligible),
        "cell_mean_gap_shrink": cell_mean_gap_shrink,
        "cell_means": cell_means,
        "gap_shrink_ci95": ci,
        "primary_strong_pair_fraction": frac(primary_eligible, "strong"),
        "generic_delay_failure_fraction": frac(primary_eligible, "generic_delay_ok", negate=True),
        "recovery_pair_fraction": frac(primary_eligible, "recovery"),
        "reinstatement_pair_fraction": frac(primary_eligible, "reinstatement"),
        "positive_domains": len({p["domain"] for p in primary_eligible if p["strong"]}),
        "capability_cell_means": {d: sorted(v) for d, v in sorted(by_capability.items())},
        # --- secondary cells are executed and described, but gate nothing
        "secondary_weighting_capable_pairs": len(eligible) - len(primary_eligible),
        "secondary_strong_pair_fraction": frac([p for p in eligible if p["cell_id"] in secondary_cells], "strong"),
    }
    model_pass = (
        len(cell_values) >= pc["min_primary_cells"]
        and len(primary_eligible) >= pc["min_weighting_capable_pairs"]
        and agg["primary_strong_pair_fraction"] >= pc["min_strong_pair_fraction"]
        and cell_mean_gap_shrink >= pc["min_mean_gap_shrink"]
        and ci[0] >= pc["min_gap_shrink_ci_lower"]
        and agg["recovery_pair_fraction"] >= pc["min_recovery_pair_fraction"]
        and agg["reinstatement_pair_fraction"] >= pc["min_reinstatement_pair_fraction"]
        and agg["generic_delay_failure_fraction"] <= pc["max_generic_delay_failure_fraction"]
        and agg["positive_domains"] >= pc["min_positive_domains"]
    )

    # Capability floors are read over the whole executed bank: whether the model can do
    # the task at all is not a question about the inferential stratification.
    total = len(pairs)
    support_frac = agg["support_gated_pairs"] / total if total else 0.0
    memory_frac = agg["memory_gated_pairs"] / total if total else 0.0
    weighting_frac = len(eligible) / total if total else 0.0
    if support_frac < pc["min_support_gated_fraction"]:
        verdict = "HARD-KILL-SOURCE-EVIDENCE-CAPABILITY-FLOOR"
    elif memory_frac < pc["min_memory_gated_fraction"]:
        verdict = "HARD-KILL-SOURCE-MEMORY-CAPABILITY-FLOOR"
    elif weighting_frac < pc["min_weighting_capable_fraction"]:
        verdict = "HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR"
    elif agg["generic_delay_failure_fraction"] > pc["max_generic_delay_failure_fraction"]:
        verdict = "HOLD-GENERIC-DELAY-DEGRADATION"
    elif agg["recovery_pair_fraction"] < pc["min_recovery_pair_fraction"] or (math.isfinite(cell_mean_gap_shrink) and cell_mean_gap_shrink < pc["no_effect_gap_shrink"]):
        verdict = "HARD-KILL-NO-SOURCE-DISCOUNT-RECOVERY"
    elif agg["reinstatement_pair_fraction"] < pc["min_reinstatement_pair_fraction"]:
        verdict = "HOLD-NO-SELECTIVE-SOURCE-CUE-REINSTATEMENT"
    elif model_pass:
        verdict = "PASS-TO-PANEL"
    else:
        verdict = "HOLD-BELOW-PROMOTION-THRESHOLD"

    result = {
        "model": rows[0]["model"], "family": rows[0]["family"], "revision": rows[0].get("revision"),
        "size_b": rows[0]["size_b"], "requested_dtype": rows[0].get("requested_dtype"),
        "directions": directions, "pairs": pairs, "aggregate": agg,
        "model_pass": model_pass, "verdict": verdict,
    }
    if out_path:
        Path(out_path).write_text(json.dumps(result, indent=2, allow_nan=True), encoding="utf-8")
    return result
