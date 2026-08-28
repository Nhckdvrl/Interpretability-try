from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any
import json
import math
import random

from .data import load_scenarios, Scenario, Partition

def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"invalid results JSONL line {i}") from e
    return rows

def bootstrap_ci(values: list[float], *, seed: int, n_boot: int) -> tuple[float, float]:
    if not values:
        return math.nan, math.nan
    rng = random.Random(seed)
    n = len(values)
    draws = sorted(mean(values[rng.randrange(n)] for _ in range(n)) for _ in range(n_boot))
    return draws[int(.025 * (n_boot - 1))], draws[int(.975 * (n_boot - 1))]

def threshold_auc(thresholds: list[float], yes_probs: list[float], *, scale: float = 1.0) -> float:
    if len(thresholds) != len(yes_probs) or not thresholds:
        raise ValueError("threshold_auc needs aligned non-empty inputs")
    xs = [float(x) / scale for x in thresholds]
    if xs != sorted(xs) or xs[0] <= 0 or xs[-1] >= 1:
        raise ValueError("normalized thresholds must be strictly inside (0,1) and sorted")
    ys = [float(y) for y in yes_probs]
    points = [(0.0, 1.0)] + list(zip(xs, ys)) + [(1.0, 0.0)]
    area = 0.0
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        area += (x1 - x0) * (y0 + y1) / 2.0
    return area

def max_monotonicity_violation(thresholds: list[float], yes_probs: list[float]) -> float:
    pairs = sorted(zip(thresholds, yes_probs))
    return max((float(y1) - float(y0) for (_, y0), (_, y1) in zip(pairs, pairs[1:])), default=0.0)

def _validate_metadata(rows: list[dict[str, Any]]) -> tuple[str | None, str | None, float | None, str | None]:
    if not rows:
        raise ValueError("results file is empty")
    fields = ("model", "family", "size_b", "revision")
    vals: dict[str, set[Any]] = {f: {r.get(f) for r in rows} for f in fields}
    for f, s in vals.items():
        if len(s) != 1:
            raise ValueError(f"mixed result metadata for {f}: {sorted(map(str, s))[:5]}")
    model = next(iter(vals["model"]))
    family = next(iter(vals["family"]))
    size = next(iter(vals["size_b"]))
    revision = next(iter(vals["revision"]))
    if not family:
        raise ValueError("family metadata is required")
    if size is None or float(size) <= 0:
        raise ValueError("size_b must be positive")
    return model, family, float(size), revision

def summarize(*, data_path: str, results_path: str, config_path: str, out_path: str | None = None) -> dict[str, Any]:
    scenarios = load_scenarios(data_path, require_external_source=True)
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
    rows = read_jsonl(results_path)
    model, family, size_b, revision = _validate_metadata(rows)

    scenario_map: dict[str, Scenario] = {s.scenario_id: s for s in scenarios}
    part_map: dict[tuple[str, str], Partition] = {(s.scenario_id, p.partition_id): p for s in scenarios for p in s.partitions}
    valid_keys = set(part_map)
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    seen: set[tuple[Any, ...]] = set()

    for row in rows:
        key = (str(row["scenario_id"]), str(row["partition_id"]))
        if key not in valid_keys:
            raise ValueError(f"unknown result key={key}")
        s = scenario_map[key[0]]
        p = part_map[key]
        if row.get("domain") != s.domain:
            raise ValueError(f"{key}: result domain does not match D0")
        if int(row.get("branch_count")) != p.branch_count:
            raise ValueError(f"{key}: result branch_count does not match D0")
        if row["kind"] == "recognition":
            uniq = key + ("r", row["scope"], row["probe"], int(row["label_order"]))
        elif row["kind"] == "readout":
            uniq = key + ("o", row["readout"], int(row["template_id"]), row["condition"], float(row["threshold"]), int(row["label_order"]))
        else:
            raise ValueError(f"unknown kind={row['kind']}")
        if uniq in seen:
            raise ValueError(f"duplicate result variant={uniq}")
        seen.add(uniq)
        grouped[key].append(row)

    missing = valid_keys - set(grouped)
    if missing:
        raise ValueError(f"missing result groups; first={sorted(missing)[:3]}")

    rec_cfg = cfg["recognition_gate"]
    ctrl_cfg = cfg["artifact_controls"]
    strong_cfg = cfg["strong_case"]
    readout_cfg = cfg["readout"]
    thresholds_by_readout = {
        "probability": [float(x) for x in readout_cfg["probability_thresholds"]],
        "decision": [float(x) for x in readout_cfg["decision_thresholds"]],
    }
    template_counts = {"probability": 2, "decision": 2}
    case_rows: list[dict[str, Any]] = []

    for key in sorted(valid_keys):
        s = scenario_map[key[0]]
        p = part_map[key]
        rs = grouped[key]
        rec = [r for r in rs if r["kind"] == "recognition"]
        expected_rec_scopes = {"focal": {"equivalent", "disjoint", "exhaustive", "partial_strict_subset"}}
        if p.alternative_packed_text is not None:
            expected_rec_scopes["alternative"] = {"equivalent", "disjoint", "exhaustive"}
        expected_rec_n = 2 * sum(len(v) for v in expected_rec_scopes.values())
        if len(rec) != expected_rec_n:
            raise ValueError(f"{key}: expected {expected_rec_n} recognition rows, found {len(rec)}")

        recognition: dict[str, dict[str, dict[str, float]]] = {}
        all_core_rec_probs: list[float] = []
        for scope, probes in expected_rec_scopes.items():
            recognition[scope] = {}
            for probe in probes:
                z = [r for r in rec if r["scope"] == scope and r["probe"] == probe]
                if {int(r["label_order"]) for r in z} != {0, 1} or len(z) != 2:
                    raise ValueError(f"{key}/{scope}/{probe}: incomplete label reversal")
                vals = [float(r["p_correct"]) for r in z]
                recognition[scope][probe] = {"mean": mean(vals), "min": min(vals), "gap": abs(vals[0] - vals[1])}
                if scope == "focal":
                    all_core_rec_probs.extend(vals)
        recognition_min = min(v["min"] for v in recognition["focal"].values())
        recognition_mean = mean(all_core_rec_probs)
        recognition_label_gap = max(v["gap"] for v in recognition["focal"].values())
        gated = (
            recognition_min >= rec_cfg["min_probe_probability"]
            and recognition_mean >= rec_cfg["min_mean_probability"]
            and recognition_label_gap <= rec_cfg["max_label_order_gap"]
        )
        alternative_gated = True
        if "alternative" in recognition:
            alternative_gated = min(v["min"] for v in recognition["alternative"].values()) >= rec_cfg["min_probe_probability"]

        out_rows = [r for r in rs if r["kind"] == "readout"]
        base_conditions = {"packed", "core_unpacked", "paraphrase", "partial_subset"}
        if p.repacked_text is not None:
            base_conditions.add("repacked")
        if p.alternative_packed_text is not None:
            base_conditions |= {"alt_frame_packed", "alt_frame_unpacked"}
        present_conditions = {r["condition"] for r in out_rows}
        if present_conditions != base_conditions:
            raise ValueError(f"{key}: condition set mismatch; expected={sorted(base_conditions)}, found={sorted(present_conditions)}")

        scores: dict[tuple[str, int, str], float] = {}
        mono: dict[tuple[str, int, str], float] = {}
        order_gap: dict[tuple[str, int, str], float] = {}
        for readout in ("probability", "decision"):
            thresholds = thresholds_by_readout[readout]
            scale = 1.0 if readout == "probability" else 100.0
            for template_id in range(template_counts[readout]):
                for condition in base_conditions:
                    z = [r for r in out_rows if r["readout"] == readout and int(r["template_id"]) == template_id and r["condition"] == condition]
                    expected_n = len(thresholds) * 2
                    if len(z) != expected_n:
                        raise ValueError(f"{key}/{readout}/{template_id}/{condition}: expected {expected_n} rows, found {len(z)}")
                    by_t: dict[float, list[dict[str, Any]]] = defaultdict(list)
                    for r in z:
                        by_t[float(r["threshold"])].append(r)
                    if set(by_t) != set(thresholds):
                        raise ValueError(f"{key}/{readout}/{condition}: threshold coverage mismatch")
                    yes_probs: list[float] = []
                    gaps: list[float] = []
                    for t in thresholds:
                        zz = by_t[t]
                        if {int(r["label_order"]) for r in zz} != {0, 1} or len(zz) != 2:
                            raise ValueError(f"{key}/{readout}/{condition}/{t}: incomplete label reversal")
                        vals = [float(r["p_yes"]) for r in sorted(zz, key=lambda x: int(x["label_order"]))]
                        yes_probs.append(mean(vals))
                        gaps.append(abs(vals[0] - vals[1]))
                    scores[(readout, template_id, condition)] = threshold_auc(thresholds, yes_probs, scale=scale)
                    mono[(readout, template_id, condition)] = max_monotonicity_violation(thresholds, yes_probs)
                    order_gap[(readout, template_id, condition)] = max(gaps)

        core_variant_biases = []
        core_by_readout: dict[str, float] = {}
        paraphrase_abs = []
        partial_violations = []
        repacked_abs = []
        max_mono = 0.0
        max_order_gap = 0.0
        for readout in ("probability", "decision"):
            rb = []
            for template_id in range(template_counts[readout]):
                packed_score = scores[(readout, template_id, "packed")]
                unpacked_score = scores[(readout, template_id, "core_unpacked")]
                b = unpacked_score - packed_score
                rb.append(b)
                core_variant_biases.append(b)
                paraphrase_abs.append(abs(scores[(readout, template_id, "paraphrase")] - packed_score))
                partial_violations.append(scores[(readout, template_id, "partial_subset")] - packed_score)
                if p.repacked_text is not None:
                    repacked_abs.append(abs(scores[(readout, template_id, "repacked")] - packed_score))
                for cond in base_conditions:
                    max_mono = max(max_mono, mono[(readout, template_id, cond)])
                    max_order_gap = max(max_order_gap, order_gap[(readout, template_id, cond)])
            core_by_readout[readout] = mean(rb)

        core_bias = mean(core_variant_biases)
        positive_variant_fraction = sum(v > 0 for v in core_variant_biases) / len(core_variant_biases)
        max_abs_paraphrase_bias = max(paraphrase_abs)
        max_partial_subset_violation = max(partial_violations)
        max_abs_repacked_bias = max(repacked_abs) if repacked_abs else math.nan
        control_ok = (
            max_abs_paraphrase_bias <= ctrl_cfg["max_abs_paraphrase_bias"]
            and max_partial_subset_violation <= ctrl_cfg["max_partial_subset_violation"]
            and (math.isnan(max_abs_repacked_bias) or max_abs_repacked_bias <= ctrl_cfg["max_abs_repacked_bias"])
            and max_mono <= ctrl_cfg["max_threshold_monotonicity_violation"]
            and max_order_gap <= ctrl_cfg["max_readout_label_order_gap"]
        )

        alternative_frame_shift_by_readout: dict[str, float] = {}
        if p.alternative_packed_text is not None and alternative_gated:
            for readout in ("probability", "decision"):
                vals = [scores[(readout, template_id, "alt_frame_unpacked")] - scores[(readout, template_id, "alt_frame_packed")] for template_id in range(template_counts[readout])]
                alternative_frame_shift_by_readout[readout] = mean(vals)

        strong = (
            gated and control_ok
            and core_bias >= strong_cfg["min_core_unpacked_bias"]
            and max(core_by_readout.values()) >= strong_cfg["min_any_readout_core_bias"]
            and min(core_by_readout.values()) >= strong_cfg["min_each_readout_core_bias"]
            and positive_variant_fraction >= strong_cfg["min_positive_variant_fraction"]
        )
        case_rows.append({
            "scenario_id": s.scenario_id, "partition_id": p.partition_id,
            "branch_count": p.branch_count, "domain": s.domain,
            "recognition": recognition, "recognition_min": recognition_min,
            "recognition_mean": recognition_mean, "recognition_label_gap": recognition_label_gap,
            "gated": gated, "core_unpacked_bias": core_bias,
            "core_bias_by_readout": core_by_readout,
            "positive_variant_fraction": positive_variant_fraction,
            "max_abs_paraphrase_bias": max_abs_paraphrase_bias,
            "max_partial_subset_violation": max_partial_subset_violation,
            "max_abs_repacked_bias": max_abs_repacked_bias,
            "max_threshold_monotonicity_violation": max_mono,
            "max_readout_label_order_gap": max_order_gap,
            "control_ok": control_ok, "alternative_relation_gated": alternative_gated,
            "alternative_frame_shift_by_readout": alternative_frame_shift_by_readout,
            "strong": strong,
        })

    gated_rows = [r for r in case_rows if r["gated"]]
    core = [r["core_unpacked_bias"] for r in gated_rows]
    ci_lo, ci_hi = bootstrap_ci(core, seed=cfg["seed"], n_boot=cfg["bootstrap_samples"])
    by_domain = {}
    for d in sorted({r["domain"] for r in case_rows}):
        sub = [r for r in gated_rows if r["domain"] == d]
        by_domain[d] = {
            "gated": len(sub),
            "mean_core_unpacked_bias": mean(r["core_unpacked_bias"] for r in sub) if sub else math.nan,
            "strong": sum(bool(r["strong"]) for r in sub),
        }
    by_readout = {}
    for readout in ("probability", "decision"):
        vals = [r["core_bias_by_readout"][readout] for r in gated_rows]
        by_readout[readout] = {"gated": len(vals), "mean_core_unpacked_bias": mean(vals) if vals else math.nan}

    per_scenario_k: dict[str, dict[int, list[float]]] = defaultdict(lambda: defaultdict(list))
    for r in gated_rows:
        per_scenario_k[r["scenario_id"]][int(r["branch_count"])].append(r["core_unpacked_bias"])
    branch_slopes: list[float] = []
    branch_details = {}
    for sid, km in per_scenario_k.items():
        means = {k: mean(v) for k, v in km.items()}
        ks = sorted(means)
        if len(ks) >= 2:
            slope = (means[ks[-1]] - means[ks[0]]) / (ks[-1] - ks[0])
            branch_slopes.append(slope)
            branch_details[sid] = {"by_k": means, "endpoint_slope": slope}

    alt_rows = [r for r in gated_rows if r["alternative_frame_shift_by_readout"] and r["alternative_relation_gated"]]
    alt_summary = {}
    for readout in ("probability", "decision"):
        vals = [r["alternative_frame_shift_by_readout"][readout] for r in alt_rows]
        alt_summary[readout] = {"cases": len(vals), "mean_focal_shift_when_alternative_unpacked": mean(vals) if vals else math.nan}

    pcfg = cfg["model_pass"]
    positive_domains = sum(v["gated"] >= 2 and v["mean_core_unpacked_bias"] > 0 for v in by_domain.values())
    positive_readouts = sum(v["gated"] > 0 and v["mean_core_unpacked_bias"] > 0 for v in by_readout.values())
    aggregate = {
        "total_partition_cases": len(case_rows),
        "gated_cases": len(gated_rows),
        "mean_core_unpacked_bias": mean(core) if core else math.nan,
        "bootstrap_95_ci": [ci_lo, ci_hi],
        "strong_cases": sum(bool(r["strong"]) for r in gated_rows),
        "strong_fraction": (sum(bool(r["strong"]) for r in gated_rows) / len(gated_rows)) if gated_rows else 0.0,
        "positive_domains": positive_domains,
        "positive_readouts": positive_readouts,
        "artifact_failures": sum(r["gated"] and not r["control_ok"] for r in case_rows),
        "paired_branch_scenarios": len(branch_slopes),
        "mean_within_scenario_branch_slope": mean(branch_slopes) if branch_slopes else math.nan,
    }
    model_pass = (
        aggregate["gated_cases"] >= pcfg["min_gated_cases"]
        and aggregate["mean_core_unpacked_bias"] >= pcfg["min_mean_core_unpacked_bias"]
        and ci_lo >= pcfg["min_bootstrap_ci_lower"]
        and aggregate["strong_fraction"] >= pcfg["min_strong_fraction"]
        and positive_domains >= pcfg["min_positive_domains"]
        and positive_readouts >= pcfg["min_positive_readouts"]
        and min(v["mean_core_unpacked_bias"] for v in by_readout.values()) >= pcfg["min_each_readout_bias"]
    )
    if aggregate["gated_cases"] >= pcfg["min_gated_cases"] and abs(aggregate["mean_core_unpacked_bias"]) < 0.02:
        verdict = "HARD-KILL-NO-PHENOMENON"
    elif aggregate["artifact_failures"] > max(2, aggregate["gated_cases"] // 4):
        verdict = "HOLD-ARTIFACT-CONTROLS"
    else:
        verdict = "PASS-TO-PANEL" if model_pass else "FAIL-MODEL-G0"

    summary = {
        "contract": "Packed-Unpacked Event Splitting",
        "model": model, "family": family, "size_b": size_b, "revision": revision,
        "model_pass": model_pass, "verdict": verdict, "aggregate": aggregate,
        "by_domain": by_domain, "by_readout": by_readout,
        "branch_count_within_scenario": branch_details, "alternative_frame": alt_summary,
        "cases": case_rows,
        "hard_kill_note": (
            "Kill standalone novelty if the isolated packed/unpacked effect vanishes after relation gating, "
            "is matched by ordinary paraphrase/repacked controls, violates subset monotonicity, depends on "
            "label order/threshold-interface artifacts, or fails cross-family replication."
        ),
    }
    if out_path:
        pth = Path(out_path)
        pth.parent.mkdir(parents=True, exist_ok=True)
        pth.write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=True), encoding="utf-8")
    return summary
