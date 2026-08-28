from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any
import json, math, random

from .data import load_scenarios

def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows = []
    with Path(path).open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if line.strip():
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

def _mean(rows: list[dict[str, Any]], field: str) -> float:
    return mean(float(r[field]) for r in rows)

def summarize(*, data_path: str, results_path: str, config_path: str,
              out_path: str | None = None) -> dict[str, Any]:
    scenarios = load_scenarios(data_path, require_external_source=True)
    valid_keys = {(s.scenario_id, p.partition_id) for s in scenarios for p in s.partitions}
    rows = read_jsonl(results_path)
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    seen = set()
    for row in rows:
        key = (str(row["scenario_id"]), str(row["partition_id"]))
        if key not in valid_keys:
            raise ValueError(f"unknown result key={key}")
        if row["kind"] == "recognition":
            uniq = key + ("r", row["probe"], int(row["label_order"]))
        elif row["kind"] == "judgment":
            uniq = key + ("j", row["readout"], int(row["template_id"]), row["condition"], int(row["label_order"]))
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
    case_rows = []

    for key in sorted(valid_keys):
        rs = grouped[key]
        rec = [r for r in rs if r["kind"] == "recognition"]
        expected_rec = 3 * 2
        if len(rec) != expected_rec:
            raise ValueError(f"{key}: expected {expected_rec} recognition rows, found {len(rec)}")
        probe_probs = {probe: _mean([r for r in rec if r["probe"] == probe], "p_correct")
                       for probe in ("equivalent", "disjoint", "exhaustive")}
        recognition_min = min(probe_probs.values())
        recognition_mean = mean(probe_probs.values())
        gated = recognition_min >= rec_cfg["min_probe_probability"] and recognition_mean >= rec_cfg["min_mean_probability"]

        js = [r for r in rs if r["kind"] == "judgment"]
        expected_per_condition = 2 * 2 * 6
        present_conditions = {r["condition"] for r in js}
        for cond in present_conditions:
            n = sum(r["condition"] == cond for r in js)
            if n != expected_per_condition:
                raise ValueError(f"{key}/{cond}: expected {expected_per_condition} rows, found {n}")

        def bias(condition: str) -> float:
            z = [r for r in js if r["condition"] == condition]
            return mean(float(r["p_right_more"]) - float(r["p_left_more"]) for r in z)

        def right_prob(condition: str) -> float:
            return _mean([r for r in js if r["condition"] == condition], "p_right_more")

        core_bias = bias("core")
        paraphrase_bias = bias("paraphrase")
        partial_discrimination = -bias("partial_subset")
        repacked_bias = bias("repacked") if "repacked" in present_conditions else math.nan
        repacking_recovery = core_bias - repacked_bias if not math.isnan(repacked_bias) else math.nan
        control_ok = (
            abs(paraphrase_bias) <= ctrl_cfg["max_abs_paraphrase_bias"]
            and partial_discrimination >= ctrl_cfg["min_partial_subset_discrimination"]
        )
        repack_ok = math.isnan(repacking_recovery) or repacking_recovery >= strong_cfg["min_repacking_recovery"]
        strong = (
            gated and control_ok and repack_ok
            and core_bias >= strong_cfg["min_core_unpacked_bias"]
            and right_prob("core") >= strong_cfg["min_unpacked_more_probability"]
        )
        case_rows.append({
            "scenario_id": key[0], "partition_id": key[1],
            "branch_count": int(next(r["branch_count"] for r in rs)),
            "domain": next(r["domain"] for r in rs),
            "recognition": probe_probs, "recognition_min": recognition_min,
            "recognition_mean": recognition_mean, "gated": gated,
            "core_unpacked_bias": core_bias,
            "core_p_unpacked_more": right_prob("core"),
            "paraphrase_bias": paraphrase_bias,
            "partial_subset_discrimination": partial_discrimination,
            "repacked_bias": repacked_bias,
            "repacking_recovery": repacking_recovery,
            "control_ok": control_ok, "strong": strong,
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

    by_k = {}
    for k in sorted({r["branch_count"] for r in gated_rows}):
        sub = [r for r in gated_rows if r["branch_count"] == k]
        by_k[str(k)] = mean(r["core_unpacked_bias"] for r in sub)
    ks = sorted(int(k) for k in by_k)
    branch_count_slope = (
        (by_k[str(ks[-1])] - by_k[str(ks[0])]) / (ks[-1] - ks[0])
        if len(ks) >= 2 and ks[-1] != ks[0] else math.nan
    )

    pcfg = cfg["model_pass"]
    positive_domains = sum(v["gated"] >= 2 and v["mean_core_unpacked_bias"] > 0 for v in by_domain.values())
    aggregate = {
        "total_partition_cases": len(case_rows),
        "gated_cases": len(gated_rows),
        "mean_core_unpacked_bias": mean(core) if core else math.nan,
        "bootstrap_95_ci": [ci_lo, ci_hi],
        "strong_cases": sum(bool(r["strong"]) for r in gated_rows),
        "strong_fraction": (sum(bool(r["strong"]) for r in gated_rows) / len(gated_rows)) if gated_rows else 0.0,
        "positive_domains": positive_domains,
        "branch_count_bias": by_k,
        "branch_count_slope": branch_count_slope,
        "artifact_failures": sum(r["gated"] and not r["control_ok"] for r in case_rows),
    }
    model_pass = (
        aggregate["gated_cases"] >= pcfg["min_gated_cases"]
        and aggregate["mean_core_unpacked_bias"] >= pcfg["min_mean_core_unpacked_bias"]
        and ci_lo >= pcfg["min_bootstrap_ci_lower"]
        and aggregate["strong_fraction"] >= pcfg["min_strong_fraction"]
        and positive_domains >= pcfg["min_positive_domains"]
    )
    if aggregate["gated_cases"] >= pcfg["min_gated_cases"] and abs(aggregate["mean_core_unpacked_bias"]) < 0.02:
        verdict = "HARD-KILL-NO-PHENOMENON"
    elif aggregate["artifact_failures"] > max(2, aggregate["gated_cases"] // 4):
        verdict = "HOLD-ARTIFACT-CONTROLS"
    else:
        verdict = "PASS-TO-PANEL" if model_pass else "FAIL-MODEL-G0"

    summary = {
        "contract": "Packed-Unpacked Event Splitting",
        "model": rows[0].get("model") if rows else None,
        "family": rows[0].get("family") if rows else None,
        "revision": rows[0].get("revision") if rows else None,
        "model_pass": model_pass,
        "verdict": verdict,
        "aggregate": aggregate,
        "by_domain": by_domain,
        "cases": case_rows,
        "hard_kill_note": (
            "Standalone novelty is killed if the core effect vanishes after recognition gating, "
            "is matched by packed-paraphrase wording bias, or the model cannot distinguish a true strict subset."
        ),
    }
    if out_path:
        p = Path(out_path); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=True), encoding="utf-8")
    return summary
