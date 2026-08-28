from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any
import json
import math
import random

from .data import load_scenarios

def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"invalid results JSONL line {i}") from e
    return out

def bootstrap_ci(values: list[float], *, seed: int, n_boot: int) -> tuple[float, float]:
    if not values:
        return math.nan, math.nan
    rng = random.Random(seed)
    n = len(values)
    draws = sorted(mean(values[rng.randrange(n)] for _ in range(n)) for _ in range(n_boot))
    return draws[int(.025 * (n_boot - 1))], draws[int(.975 * (n_boot - 1))]

def _metadata(rows: list[dict[str, Any]]) -> tuple[Any, str, float, Any]:
    if not rows:
        raise ValueError("results file is empty")
    vals = {k: {r.get(k) for r in rows} for k in ("model", "family", "size_b", "revision")}
    for k, v in vals.items():
        if len(v) != 1:
            raise ValueError(f"mixed result metadata for {k}: {sorted(map(str, v))[:5]}")
    model = next(iter(vals["model"]))
    family = next(iter(vals["family"]))
    size_b = next(iter(vals["size_b"]))
    revision = next(iter(vals["revision"]))
    if not family or size_b is None or float(size_b) <= 0:
        raise ValueError("family and positive size_b are required")
    return model, str(family), float(size_b), revision

def summarize(*, data_path: str, results_path: str, config_path: str,
              out_path: str | None = None) -> dict[str, Any]:
    scenarios = load_scenarios(data_path, require_external_source=True)
    by_id = {s.scenario_id: s for s in scenarios}
    rows = read_jsonl(results_path)
    model, family, size_b, revision = _metadata(rows)
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
    pcfg = cfg["model_pass"]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen: set[tuple[Any, ...]] = set()

    for row in rows:
        sid = str(row["scenario_id"])
        if sid not in by_id:
            raise ValueError(f"unknown scenario_id={sid}")
        s = by_id[sid]
        if row.get("domain") != s.domain or row.get("polarity") != s.evidence_polarity:
            raise ValueError(f"{sid}: result metadata disagrees with D0")
        if row.get("polarity_pair_id") != s.polarity_pair_id:
            raise ValueError(f"{sid}: polarity_pair_id disagrees with D0")
        if row["kind"] == "recognition":
            uniq = (sid, "r", row["probe"], int(row["label_order"]))
        elif row["kind"] == "verdict":
            uniq = (sid, "v", row["condition"], int(row["template_id"]), int(row["label_order"]))
        else:
            raise ValueError(f"unknown kind={row['kind']}")
        if uniq in seen:
            raise ValueError(f"duplicate result variant={uniq}")
        seen.add(uniq)
        grouped[sid].append(row)

    missing = set(by_id) - set(grouped)
    if missing:
        raise ValueError(f"missing results; first={sorted(missing)[:3]}")

    raw_polarity_counts = {
        pol: sum(s.evidence_polarity == pol for s in scenarios)
        for pol in ("supports_target", "supports_other")
    }
    raw_neutral_coverage = sum(s.neutral_evidence_text is not None for s in scenarios) / len(scenarios)
    raw_pair_ids: dict[str, list[Any]] = defaultdict(list)
    for s in scenarios:
        if s.polarity_pair_id is not None:
            raw_pair_ids[s.polarity_pair_id].append(s)
    raw_complete_pairs = sum(
        len(ss) == 2 and {s.evidence_polarity for s in ss} == {"supports_target", "supports_other"}
        for ss in raw_pair_ids.values()
    )
    d0_coverage_ok = (
        all(raw_polarity_counts[p] >= pcfg["min_gated_per_polarity"] for p in raw_polarity_counts)
        and raw_neutral_coverage >= pcfg["min_neutral_coverage"]
        and raw_complete_pairs >= pcfg["min_polarity_pairs"]
    )

    rec_cfg = cfg["recognition_gate"]
    cap_cfg = cfg["capability_gate"]
    strong_cfg = cfg["strong_case"]
    cases: list[dict[str, Any]] = []

    for sid in sorted(by_id):
        s = by_id[sid]
        rs = grouped[sid]
        rec = [r for r in rs if r["kind"] == "recognition"]
        if len(rec) != 6:
            raise ValueError(f"{sid}: expected 6 recognition rows, found {len(rec)}")
        recognition: dict[str, dict[str, float]] = {}
        for probe in ("inadmissible", "scope", "polarity"):
            z = sorted([r for r in rec if r["probe"] == probe], key=lambda x: int(x["label_order"]))
            if len(z) != 2 or {int(r["label_order"]) for r in z} != {0, 1}:
                raise ValueError(f"{sid}/{probe}: incomplete label reversal")
            vals = [float(r["p_correct"]) for r in z]
            recognition[probe] = {"mean": mean(vals), "min": min(vals), "gap": abs(vals[0] - vals[1])}
        recognition_gate = (
            recognition["inadmissible"]["min"] >= rec_cfg["min_admissibility_probability"]
            and recognition["scope"]["min"] >= rec_cfg["min_scope_probability"]
            and recognition["polarity"]["min"] >= rec_cfg["min_polarity_probability"]
            and max(v["gap"] for v in recognition.values()) <= rec_cfg["max_label_order_gap"]
        )

        verdict = [r for r in rs if r["kind"] == "verdict"]
        required = {"never_seen", "admitted", "struck"}
        if s.neutral_evidence_text is not None:
            required.add("neutral_struck")
        conditions = {r["condition"] for r in verdict}
        if conditions != required:
            raise ValueError(f"{sid}: condition set mismatch; expected={sorted(required)}, found={sorted(conditions)}")

        p_by_template: dict[int, dict[str, float]] = {0: {}, 1: {}}
        label_gaps: list[float] = []
        for template_id in (0, 1):
            for cond in required:
                z = sorted(
                    [r for r in verdict if int(r["template_id"]) == template_id and r["condition"] == cond],
                    key=lambda x: int(x["label_order"]),
                )
                if len(z) != 2 or {int(r["label_order"]) for r in z} != {0, 1}:
                    raise ValueError(f"{sid}/{template_id}/{cond}: incomplete answer-label reversal")
                vals = [float(r["p_target"]) for r in z]
                p_by_template[template_id][cond] = mean(vals)
                label_gaps.append(abs(vals[0] - vals[1]))

        sign = 1.0 if s.evidence_polarity == "supports_target" else -1.0
        template_rows = []
        for template_id in (0, 1):
            p = p_by_template[template_id]
            admitted_shift = sign * (p["admitted"] - p["never_seen"])
            struck_residual = sign * (p["struck"] - p["never_seen"])
            undo_ratio = struck_residual / admitted_shift if admitted_shift > 1e-9 else math.nan
            template_rows.append({
                "template_id": template_id,
                "admitted_shift": admitted_shift,
                "struck_residual": struck_residual,
                "undo_ratio": undo_ratio,
            })
        admitted_shift = mean(r["admitted_shift"] for r in template_rows)
        struck_residual = mean(r["struck_residual"] for r in template_rows)
        valid_ratios = [r["undo_ratio"] for r in template_rows if not math.isnan(r["undo_ratio"])]
        undo_ratio = mean(valid_ratios) if valid_ratios else math.nan
        verdict_label_gap = max(label_gaps)
        capability_gate = (
            recognition_gate
            and admitted_shift >= cap_cfg["min_admissible_directional_shift"]
            and verdict_label_gap <= cap_cfg["max_verdict_label_order_gap"]
        )
        neutral_shift = math.nan
        if s.neutral_evidence_text is not None:
            neutral_shift = mean(
                abs(p_by_template[t]["neutral_struck"] - p_by_template[t]["never_seen"])
                for t in (0, 1)
            )
        neutral_ok = math.isnan(neutral_shift) or neutral_shift <= strong_cfg["max_neutral_struck_abs_shift"]
        each_template_ok = min(r["struck_residual"] for r in template_rows) >= strong_cfg["min_each_template_residual"]
        strong = (
            capability_gate and neutral_ok and each_template_ok
            and struck_residual >= strong_cfg["min_struck_directional_residual"]
            and not math.isnan(undo_ratio) and undo_ratio >= strong_cfg["min_undo_ratio"]
        )
        cases.append({
            "scenario_id": sid, "domain": s.domain, "polarity": s.evidence_polarity,
            "polarity_pair_id": s.polarity_pair_id,
            "recognition": recognition, "recognition_gate": recognition_gate,
            "p_target_by_template": p_by_template,
            "admitted_directional_shift": admitted_shift,
            "struck_directional_residual": struck_residual,
            "undo_ratio": undo_ratio,
            "template_effects": template_rows,
            "verdict_label_order_gap": verdict_label_gap,
            "neutral_struck_abs_shift": neutral_shift,
            "capability_gate": capability_gate, "neutral_ok": neutral_ok,
            "strong": strong,
        })

    gated = [r for r in cases if r["capability_gate"]]
    residuals = [r["struck_directional_residual"] for r in gated]
    ci_lo, ci_hi = bootstrap_ci(residuals, seed=cfg["seed"], n_boot=cfg["bootstrap_samples"])

    by_domain = {}
    for d in sorted({r["domain"] for r in cases}):
        sub = [r for r in gated if r["domain"] == d]
        by_domain[d] = {
            "gated": len(sub),
            "mean_struck_directional_residual": mean(r["struck_directional_residual"] for r in sub) if sub else math.nan,
            "strong": sum(bool(r["strong"]) for r in sub),
        }

    by_polarity = {}
    for pol in ("supports_target", "supports_other"):
        sub = [r for r in gated if r["polarity"] == pol]
        by_polarity[pol] = {
            "gated": len(sub),
            "mean_admitted_shift": mean(r["admitted_directional_shift"] for r in sub) if sub else math.nan,
            "mean_struck_residual": mean(r["struck_directional_residual"] for r in sub) if sub else math.nan,
        }

    by_template = {}
    for template_id in (0, 1):
        vals = [next(x["struck_residual"] for x in r["template_effects"] if x["template_id"] == template_id) for r in gated]
        by_template[str(template_id)] = {
            "gated": len(vals), "mean_struck_residual": mean(vals) if vals else math.nan,
        }

    neutral_available = [r for r in gated if not math.isnan(r["neutral_struck_abs_shift"])]
    neutral_coverage = len(neutral_available) / len(gated) if gated else 0.0
    neutral_artifact_fraction = (
        sum(not r["neutral_ok"] for r in neutral_available) / len(neutral_available)
        if neutral_available else 0.0
    )

    by_pair: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in gated:
        if r["polarity_pair_id"] is not None:
            by_pair[str(r["polarity_pair_id"])].append(r)
    complete_pairs = {
        pid: rr for pid, rr in by_pair.items()
        if len(rr) == 2 and {r["polarity"] for r in rr} == {"supports_target", "supports_other"}
    }
    pair_consistent = {
        pid: all(r["struck_directional_residual"] > 0 for r in rr)
        for pid, rr in complete_pairs.items()
    }
    pair_direction_consistency = sum(pair_consistent.values()) / len(pair_consistent) if pair_consistent else 0.0

    positive_domains = sum(v["gated"] >= 2 and v["mean_struck_directional_residual"] > 0 for v in by_domain.values())
    aggregate = {
        "total_cases": len(cases), "gated_cases": len(gated),
        "mean_struck_directional_residual": mean(residuals) if residuals else math.nan,
        "bootstrap_95_ci": [ci_lo, ci_hi],
        "mean_undo_ratio": mean([r["undo_ratio"] for r in gated if not math.isnan(r["undo_ratio"])]) if gated else math.nan,
        "strong_cases": sum(bool(r["strong"]) for r in gated),
        "strong_fraction": sum(bool(r["strong"]) for r in gated) / len(gated) if gated else 0.0,
        "positive_domains": positive_domains,
        "neutral_coverage": neutral_coverage,
        "neutral_artifact_fraction": neutral_artifact_fraction,
        "complete_polarity_pairs": len(complete_pairs),
        "pair_direction_consistency": pair_direction_consistency,
        "raw_polarity_counts": raw_polarity_counts,
        "raw_neutral_coverage": raw_neutral_coverage,
        "raw_complete_polarity_pairs": raw_complete_pairs,
    }
    polarity_pass = all(
        by_polarity[p]["gated"] >= pcfg["min_gated_per_polarity"]
        and by_polarity[p]["mean_struck_residual"] >= pcfg["min_mean_residual_per_polarity"]
        for p in ("supports_target", "supports_other")
    )
    template_pass = all(
        by_template[str(t)]["mean_struck_residual"] >= pcfg["min_mean_residual_per_template"]
        for t in (0, 1)
    )
    neutral_coverage_pass = neutral_coverage >= pcfg["min_neutral_coverage"]
    pair_pass = (
        len(complete_pairs) >= pcfg["min_polarity_pairs"]
        and pair_direction_consistency >= pcfg["min_pair_direction_consistency"]
    )
    model_pass = (
        d0_coverage_ok
        and aggregate["gated_cases"] >= pcfg["min_gated_cases"]
        and aggregate["mean_struck_directional_residual"] >= pcfg["min_mean_struck_directional_residual"]
        and ci_lo >= pcfg["min_bootstrap_ci_lower"]
        and aggregate["strong_fraction"] >= pcfg["min_strong_fraction"]
        and positive_domains >= pcfg["min_positive_domains"]
        and polarity_pass and template_pass and neutral_coverage_pass
        and neutral_artifact_fraction <= pcfg["max_neutral_artifact_fraction"]
        and pair_pass
    )

    if not d0_coverage_ok:
        verdict = "HOLD-D0-COVERAGE"
    elif aggregate["gated_cases"] < pcfg["min_gated_cases"]:
        verdict = "FAIL-CAPABILITY-GATE"
    elif abs(aggregate["mean_struck_directional_residual"]) < 0.01:
        verdict = "HARD-KILL-NO-PERSISTENCE"
    elif not polarity_pass:
        verdict = "HARD-KILL-NO-BIDIRECTIONAL-PERSISTENCE"
    elif not template_pass:
        verdict = "HOLD-TEMPLATE-DEPENDENCE"
    elif not neutral_coverage_pass:
        verdict = "HOLD-INSUFFICIENT-NEUTRAL-CONTROLS"
    elif neutral_artifact_fraction > pcfg["max_neutral_artifact_fraction"]:
        verdict = "HOLD-GENERIC-SALIENCE-ARTIFACT"
    elif not pair_pass:
        verdict = "HOLD-POLARITY-PAIR-STRUCTURE"
    else:
        verdict = "PASS-TO-PANEL" if model_pass else "FAIL-MODEL-G0"

    summary = {
        "contract": "Inadmissible-Evidence Persistence",
        "model": model, "family": family, "size_b": size_b, "revision": revision,
        "model_pass": model_pass, "verdict": verdict,
        "d0_coverage_ok": d0_coverage_ok,
        "aggregate": aggregate, "by_domain": by_domain,
        "by_polarity": by_polarity, "by_template": by_template,
        "polarity_pairs": {pid: {"consistent": pair_consistent[pid], "cases": [r["scenario_id"] for r in rr]} for pid, rr in complete_pairs.items()},
        "cases": cases,
        "hard_kill_note": (
            "Kill standalone novelty if persistence disappears after same-context admissibility/scope/polarity gates, "
            "fails either evidence direction, or cannot survive matched neutral/pair controls."
        ),
    }
    if out_path:
        pth = Path(out_path)
        pth.parent.mkdir(parents=True, exist_ok=True)
        pth.write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=True), encoding="utf-8")
    return summary
