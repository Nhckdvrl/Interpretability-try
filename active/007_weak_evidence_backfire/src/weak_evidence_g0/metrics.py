from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any
import json
import math
import random

from .data import load_scenarios
from .prompts import CONDITIONS, DIRECTIONS, READOUT_TEMPLATES
from .run import SUPPORT_PROBES


def read_jsonl(path: str) -> list[dict]:
    out: list[dict] = []
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
    return draws[int(0.025 * (n_boot - 1))], draws[int(0.975 * (n_boot - 1))]


def _assert_run_metadata_consistent(rows: list[dict]) -> None:
    for field in ("model", "family", "revision", "size_b", "requested_dtype"):
        vals = {json.dumps(row.get(field), sort_keys=True) for row in rows}
        if len(vals) != 1:
            raise ValueError(f"inconsistent run metadata for {field}: {vals}")


def signed_update(direction: str, p_evidence: float, p_baseline: float) -> float:
    """Positive is normatively correct movement toward the evidence-supported hypothesis."""
    if direction == "supports_target":
        sign = 1.0
    elif direction == "supports_other":
        sign = -1.0
    else:
        raise ValueError(f"unknown direction={direction}")
    return sign * (p_evidence - p_baseline)


def compute_direction_features(*, direction: str, support: dict[str, float],
                               readouts: dict[str, dict[str, float]],
                               variants: dict[str, dict[str, list[float]]], cfg: dict) -> dict[str, Any]:
    rg = cfg["support_gate"]
    cg = cfg["capability_gate"]
    sc = cfg["strong_case"]
    support_gate = (
        support["support"] >= rg["min_support_probability"]
        and support["likelihood_relation"] >= rg["min_likelihood_relation_probability"]
        and support["support_complete"] >= rg["min_complete_support_probability"]
    )

    per_kind: dict[str, dict[str, float | bool]] = {}
    for kind, p in readouts.items():
        weak_update = signed_update(direction, p["weak"], p["no_evidence"])
        strong_update = signed_update(direction, p["strong"], p["no_evidence"])
        complete_update = signed_update(direction, p["weak_complete"], p["no_evidence_complete"])
        length_update = signed_update(direction, p["weak_length"], p["no_evidence_length"])
        neutral_shift = abs(p["neutral"] - p["no_evidence"])
        weak_backfire = -weak_update
        complete_backfire = -complete_update
        length_backfire = -length_update
        variant_backfire_fraction = mean(
            float(signed_update(direction, v, p["no_evidence"]) < 0)
            for v in variants[kind]["weak"]
        )
        per_kind[kind] = {
            "weak_signed_update": weak_update,
            "weak_backfire": weak_backfire,
            "strong_signed_update": strong_update,
            "complete_signed_update": complete_update,
            "complete_backfire": complete_backfire,
            "length_signed_update": length_update,
            "length_backfire": length_backfire,
            "neutral_abs_shift": neutral_shift,
            "variant_backfire_fraction": variant_backfire_fraction,
            "strong_control_gate": strong_update >= cg["min_strong_directional_shift"],
            "neutral_ok": neutral_shift <= sc["max_neutral_abs_shift"],
        }

    capability_gate = support_gate and all(bool(x["strong_control_gate"]) for x in per_kind.values())
    belief = per_kind["belief"]
    action = per_kind["action"]
    pragmatic_robust = belief["complete_backfire"] >= sc["min_complete_backfire"]
    length_robust = belief["length_backfire"] >= sc["min_length_control_backfire"]
    strong = (
        capability_gate
        and belief["weak_backfire"] >= sc["min_belief_backfire"]
        and action["weak_backfire"] >= sc["min_action_backfire"]
        and pragmatic_robust
        and length_robust
        and belief["neutral_ok"]
        and action["neutral_ok"]
        and belief["variant_backfire_fraction"] >= sc["min_belief_variant_backfire_fraction"]
    )
    return {
        "support_gate": support_gate,
        "capability_gate": capability_gate,
        "per_kind": per_kind,
        "pragmatic_robust": pragmatic_robust,
        "length_robust": length_robust,
        "strong": strong,
    }


def _check_duplicate_baselines(direction_rows: dict[str, dict[str, dict[str, float]]]) -> None:
    """Direction-invariant prompts must be bit-identical across the paired directions."""
    target = direction_rows["supports_target"]
    other = direction_rows["supports_other"]
    for kind in ("belief", "action"):
        for condition in ("no_evidence", "neutral", "no_evidence_complete", "no_evidence_length"):
            if abs(target[kind][condition] - other[kind][condition]) > 1e-12:
                raise ValueError(
                    f"direction-invariant {kind}/{condition} prompt produced inconsistent p_target; "
                    "this violates the paired run contract"
                )


def summarize(*, data_path: str, results_path: str, config_path: str,
              out_path: str | None = None) -> dict[str, Any]:
    scenarios = load_scenarios(data_path, require_external_source=True)
    by_id = {s.scenario_id: s for s in scenarios}
    rows = read_jsonl(results_path)
    if not rows:
        raise ValueError("results are empty")
    _assert_run_metadata_consistent(rows)
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))

    grouped: dict[str, list[dict]] = defaultdict(list)
    seen: set[tuple] = set()
    for row in rows:
        sid = str(row.get("scenario_id"))
        if sid not in by_id:
            raise ValueError(f"unknown scenario_id={sid}")
        if row.get("kind") == "support_probe":
            key = (sid, "support", row.get("direction"), row.get("probe"), int(row.get("label_order")))
        elif row.get("kind") == "readout":
            key = (
                sid,
                "readout",
                row.get("direction"),
                row.get("condition"),
                int(row.get("template_id")),
                int(row.get("label_order")),
            )
        else:
            raise ValueError(f"unknown kind={row.get('kind')}")
        if key in seen:
            raise ValueError(f"duplicate result variant={key}")
        seen.add(key)
        grouped[sid].append(row)

    if set(by_id) != set(grouped):
        missing = sorted(set(by_id) - set(grouped))
        extra = sorted(set(grouped) - set(by_id))
        raise ValueError(f"scenario coverage mismatch missing={missing} extra={extra}")

    expected_support = {
        (direction, probe, order)
        for direction in DIRECTIONS
        for probe in SUPPORT_PROBES
        for order in (0, 1)
    }
    expected_readout = {
        (direction, condition, template_id, order)
        for direction in DIRECTIONS
        for condition in CONDITIONS
        for template_id in range(len(READOUT_TEMPLATES))
        for order in (0, 1)
    }

    direction_cases: list[dict[str, Any]] = []
    scenario_pairs: list[dict[str, Any]] = []
    for sid in sorted(by_id):
        scenario = by_id[sid]
        rs = grouped[sid]
        support_rows = [r for r in rs if r["kind"] == "support_probe"]
        if {(r["direction"], r["probe"], int(r["label_order"])) for r in support_rows} != expected_support:
            raise ValueError(f"{sid}: malformed support-probe coverage")
        readout_rows = [r for r in rs if r["kind"] == "readout"]
        if {
            (r["direction"], r["condition"], int(r["template_id"]), int(r["label_order"]))
            for r in readout_rows
        } != expected_readout:
            raise ValueError(f"{sid}: malformed readout coverage")

        direction_probabilities: dict[str, dict[str, dict[str, float]]] = {}
        pair_records: dict[str, dict[str, Any]] = {}
        for direction in DIRECTIONS:
            support = {
                probe: mean(
                    float(r["p_correct"])
                    for r in support_rows
                    if r["direction"] == direction and r["probe"] == probe
                )
                for probe in SUPPORT_PROBES
            }
            readouts: dict[str, dict[str, float]] = {}
            variants: dict[str, dict[str, list[float]]] = {}
            for kind in ("belief", "action"):
                kind_rows = [r for r in readout_rows if r["direction"] == direction and r["template_kind"] == kind]
                readouts[kind] = {
                    condition: mean(float(r["p_target"]) for r in kind_rows if r["condition"] == condition)
                    for condition in CONDITIONS
                }
                variants[kind] = {
                    condition: [float(r["p_target"]) for r in kind_rows if r["condition"] == condition]
                    for condition in CONDITIONS
                }
            direction_probabilities[direction] = readouts
            features = compute_direction_features(
                direction=direction,
                support=support,
                readouts=readouts,
                variants=variants,
                cfg=cfg,
            )
            record = {
                "scenario_id": sid,
                "domain": scenario.domain,
                "direction": direction,
                "support": support,
                "p_target": readouts,
                **features,
            }
            direction_cases.append(record)
            pair_records[direction] = record

        _check_duplicate_baselines(direction_probabilities)
        t = pair_records["supports_target"]
        o = pair_records["supports_other"]
        pair_gated = t["capability_gate"] and o["capability_gate"]
        scenario_pairs.append({
            "scenario_id": sid,
            "domain": scenario.domain,
            "gated": pair_gated,
            "belief_backfire_mean": mean([
                t["per_kind"]["belief"]["weak_backfire"],
                o["per_kind"]["belief"]["weak_backfire"],
            ]),
            "belief_complete_backfire_mean": mean([
                t["per_kind"]["belief"]["complete_backfire"],
                o["per_kind"]["belief"]["complete_backfire"],
            ]),
            "action_backfire_mean": mean([
                t["per_kind"]["action"]["weak_backfire"],
                o["per_kind"]["action"]["weak_backfire"],
            ]),
            "strong": pair_gated and t["strong"] and o["strong"],
        })

    gated = [r for r in direction_cases if r["capability_gate"]]
    gated_pairs = [p for p in scenario_pairs if p["gated"]]
    pair_belief = [p["belief_backfire_mean"] for p in gated_pairs]
    ci_lo, ci_hi = bootstrap_ci(pair_belief, seed=cfg["seed"], n_boot=cfg["bootstrap_samples"])

    by_direction: dict[str, dict[str, Any]] = {}
    for direction in DIRECTIONS:
        sub = [r for r in gated if r["direction"] == direction]
        by_direction[direction] = {
            "gated": len(sub),
            "mean_belief_backfire": mean(r["per_kind"]["belief"]["weak_backfire"] for r in sub) if sub else math.nan,
            "mean_action_backfire": mean(r["per_kind"]["action"]["weak_backfire"] for r in sub) if sub else math.nan,
            "mean_complete_backfire": mean(r["per_kind"]["belief"]["complete_backfire"] for r in sub) if sub else math.nan,
            "strong": sum(r["strong"] for r in sub),
        }

    by_domain: dict[str, dict[str, Any]] = {}
    for domain in sorted({r["domain"] for r in direction_cases}):
        sub = [p for p in gated_pairs if p["domain"] == domain]
        by_domain[domain] = {
            "gated_pairs": len(sub),
            "mean_belief_backfire": mean(p["belief_backfire_mean"] for p in sub) if sub else math.nan,
            "strong_pairs": sum(p["strong"] for p in sub),
        }

    pc = cfg["model_pass"]
    neutral_bad = [
        r for r in gated
        if not (r["per_kind"]["belief"]["neutral_ok"] and r["per_kind"]["action"]["neutral_ok"])
    ]
    neutral_artifact_fraction = len(neutral_bad) / len(gated) if gated else 0.0
    aggregate = {
        "total_scenarios": len(scenarios),
        "total_directions": len(direction_cases),
        "support_gated_directions": sum(r["support_gate"] for r in direction_cases),
        "gated_directions": len(gated),
        "gated_direction_pairs": len(gated_pairs),
        "mean_belief_backfire": mean(r["per_kind"]["belief"]["weak_backfire"] for r in gated) if gated else math.nan,
        "paired_mean_belief_backfire": mean(pair_belief) if pair_belief else math.nan,
        "paired_bootstrap_95_ci": [ci_lo, ci_hi],
        "mean_action_backfire": mean(r["per_kind"]["action"]["weak_backfire"] for r in gated) if gated else math.nan,
        "mean_complete_backfire": mean(r["per_kind"]["belief"]["complete_backfire"] for r in gated) if gated else math.nan,
        "mean_length_control_backfire": mean(r["per_kind"]["belief"]["length_backfire"] for r in gated) if gated else math.nan,
        "mean_strong_directional_shift": mean(r["per_kind"]["belief"]["strong_signed_update"] for r in gated) if gated else math.nan,
        "neutral_artifact_fraction": neutral_artifact_fraction,
        "strong_direction_fraction": mean(float(r["strong"]) for r in gated) if gated else 0.0,
        "strong_pair_fraction": mean(float(p["strong"]) for p in gated_pairs) if gated_pairs else 0.0,
        "positive_domains": sum(
            info["gated_pairs"] >= 2 and info["mean_belief_backfire"] > 0
            for info in by_domain.values()
        ),
    }

    direction_pass = all(
        by_direction[d]["gated"] >= pc["min_gated_per_direction"]
        and by_direction[d]["mean_belief_backfire"] >= pc["min_mean_belief_backfire_per_direction"]
        for d in DIRECTIONS
    )
    model_pass = (
        aggregate["gated_direction_pairs"] >= pc["min_gated_pairs"]
        and aggregate["paired_mean_belief_backfire"] >= pc["min_paired_mean_belief_backfire"]
        and ci_lo >= pc["min_bootstrap_ci_lower"]
        and aggregate["mean_complete_backfire"] >= pc["min_mean_complete_backfire"]
        and aggregate["mean_length_control_backfire"] >= pc["min_mean_length_control_backfire"]
        and aggregate["mean_action_backfire"] >= pc["min_mean_action_backfire"]
        and aggregate["mean_strong_directional_shift"] >= pc["min_mean_strong_directional_shift"]
        and aggregate["strong_direction_fraction"] >= pc["min_strong_direction_fraction"]
        and aggregate["positive_domains"] >= pc["min_positive_domains"]
        and neutral_artifact_fraction <= pc["max_neutral_artifact_fraction"]
        and direction_pass
    )

    enough = aggregate["gated_direction_pairs"] >= pc["min_gated_pairs"]
    support_fraction = aggregate["support_gated_directions"] / len(direction_cases) if direction_cases else 0.0
    if len(direction_cases) >= 2 * pc["min_gated_pairs"] and support_fraction < pc["min_support_gate_fraction"]:
        verdict = "HARD-KILL-E-NOT-REPRESENTED-AS-SUPPORT"
    elif enough and aggregate["paired_mean_belief_backfire"] <= pc["no_backfire_ceiling"]:
        verdict = "HARD-KILL-NO-SIGN-REVERSAL"
    elif enough and aggregate["paired_mean_belief_backfire"] > 0 and aggregate["mean_complete_backfire"] <= 0:
        verdict = "HARD-KILL-PRAGMATIC-IMPLICATURE"
    elif enough and not direction_pass:
        verdict = "HOLD-DIRECTION-ASYMMETRY"
    elif neutral_artifact_fraction > pc["max_neutral_artifact_fraction"]:
        verdict = "HOLD-GENERIC-CONTEXT-ARTIFACT"
    else:
        verdict = "PASS-TO-PANEL" if model_pass else "FAIL-MODEL-G0"

    summary = {
        "contract": "Weak-Evidence Backfire",
        "model": rows[0].get("model"),
        "family": rows[0].get("family"),
        "revision": rows[0].get("revision"),
        "size_b": rows[0].get("size_b"),
        "model_pass": model_pass,
        "verdict": verdict,
        "aggregate": aggregate,
        "by_direction": by_direction,
        "by_domain": by_domain,
        "scenario_pairs": scenario_pairs,
        "directions": direction_cases,
        "hard_kill_note": (
            "Backfire is evaluated only after the same model recognizes the weak cue as positive evidence and responds correctly to stronger evidence. "
            "The primary statistic is a paired, sign-coded change from the identical no-evidence baseline, bootstrapped by scenario rather than treating the two evidence directions as independent. "
            "Persistence under the pragmatic-completeness control is required; otherwise the exact contract is killed as an absence-of-stronger-evidence implicature."
        ),
    }
    if out_path:
        p = Path(out_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=True), encoding="utf-8")
    return summary
