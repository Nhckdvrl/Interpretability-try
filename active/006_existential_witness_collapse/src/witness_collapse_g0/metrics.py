from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any
import json
import math
import random

from .data import load_scenarios
from .prompts import CONDITIONS, DOWNSTREAM_TEMPLATES
from .run import RECOGNITION_PROBES


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


def compute_case_features(*, recognition: dict[str, float], p: dict[str, float],
                          variant_unknown: list[float], variant_paraphrase: list[float],
                          cfg: dict) -> dict[str, Any]:
    rg = cfg["recognition_gate"]
    cg = cfg["capability_gate"]
    sc = cfg["strong_case"]
    recognition_gate = (
        recognition["p_exists"] >= rg["min_existence_probability"]
        and recognition["q_exists"] >= rg["min_existence_probability"]
        and recognition["shared_entailment"] >= rg["min_no_shared_entailment_probability"]
        and recognition["identity_determined"] >= rg["min_identity_underdetermined_probability"]
    )
    downstream_control_gate = (
        p["same_explicit"] >= cg["min_same_explicit_established_probability"]
        and p["distinct_explicit"] <= cg["max_distinct_explicit_established_probability"]
    )
    capability_gate = recognition_gate and downstream_control_gate
    unknown_margin = p["unknown"] - 0.5
    paraphrase_margin = p["paraphrase"] - 0.5
    unknown_vs_distinct = p["unknown"] - p["distinct_explicit"]
    same_sensitivity = p["same_explicit"] - p["unknown"]
    neutral_shift = abs(p["neutral_control"] - p["unknown"])
    reminder_rescue = p["unknown"] - p["relation_reminder"]
    variant_positive_fraction = mean(
        float(x > 0.5) for x in (variant_unknown + variant_paraphrase)
    )
    neutral_ok = neutral_shift <= sc["max_neutral_abs_shift"]
    strong = (
        capability_gate
        and p["unknown"] >= sc["min_unknown_established_probability"]
        and p["paraphrase"] >= sc["min_paraphrase_established_probability"]
        and unknown_vs_distinct >= sc["min_unknown_minus_distinct"]
        and neutral_ok
        and variant_positive_fraction >= sc["min_natural_variant_positive_fraction"]
    )
    return {
        "recognition_gate": recognition_gate,
        "downstream_control_gate": downstream_control_gate,
        "capability_gate": capability_gate,
        "unknown_margin": unknown_margin,
        "paraphrase_margin": paraphrase_margin,
        "unknown_vs_distinct": unknown_vs_distinct,
        "same_sensitivity": same_sensitivity,
        "neutral_abs_shift": neutral_shift,
        "neutral_ok": neutral_ok,
        "reminder_rescue": reminder_rescue,
        "natural_variant_positive_fraction": variant_positive_fraction,
        "strong": strong,
    }


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
        if row.get("kind") == "recognition":
            key = (sid, "recognition", row.get("probe"), int(row.get("label_order")))
        elif row.get("kind") == "downstream":
            key = (
                sid,
                "downstream",
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

    expected_recognition = {(p, order) for p in RECOGNITION_PROBES for order in (0, 1)}
    expected_downstream = {
        (condition, template_id, order)
        for condition in CONDITIONS
        for template_id in range(len(DOWNSTREAM_TEMPLATES))
        for order in (0, 1)
    }

    cases: list[dict[str, Any]] = []
    for sid in sorted(by_id):
        scenario = by_id[sid]
        rs = grouped[sid]
        rec = [r for r in rs if r["kind"] == "recognition"]
        coverage = {(r["probe"], int(r["label_order"])) for r in rec}
        if coverage != expected_recognition:
            raise ValueError(f"{sid}: malformed recognition coverage")
        recognition = {
            probe: mean(float(r["p_correct"]) for r in rec if r["probe"] == probe)
            for probe in RECOGNITION_PROBES
        }

        downstream = [r for r in rs if r["kind"] == "downstream"]
        coverage2 = {
            (r["condition"], int(r["template_id"]), int(r["label_order"]))
            for r in downstream
        }
        if coverage2 != expected_downstream:
            raise ValueError(f"{sid}: malformed downstream coverage")
        p = {
            condition: mean(float(r["p_established"]) for r in downstream if r["condition"] == condition)
            for condition in CONDITIONS
        }
        variant_unknown = [
            float(r["p_established"]) for r in downstream if r["condition"] == "unknown"
        ]
        variant_paraphrase = [
            float(r["p_established"]) for r in downstream if r["condition"] == "paraphrase"
        ]
        features = compute_case_features(
            recognition=recognition,
            p=p,
            variant_unknown=variant_unknown,
            variant_paraphrase=variant_paraphrase,
            cfg=cfg,
        )
        cases.append({
            "scenario_id": sid,
            "domain": scenario.domain,
            "recognition": recognition,
            "p_established": p,
            **features,
        })

    gated = [case for case in cases if case["capability_gate"]]
    margins = [case["unknown_margin"] for case in gated]
    ci_lo, ci_hi = bootstrap_ci(margins, seed=cfg["seed"], n_boot=cfg["bootstrap_samples"])
    pc = cfg["model_pass"]

    by_domain: dict[str, dict[str, Any]] = {}
    for domain in sorted({case["domain"] for case in cases}):
        sub = [case for case in gated if case["domain"] == domain]
        by_domain[domain] = {
            "gated": len(sub),
            "mean_unknown_margin": mean(case["unknown_margin"] for case in sub) if sub else math.nan,
            "strong": sum(case["strong"] for case in sub),
        }

    neutral_artifact_fraction = (
        mean(float(not case["neutral_ok"]) for case in gated) if gated else 0.0
    )
    aggregate = {
        "total_cases": len(cases),
        "recognition_gated_cases": sum(case["recognition_gate"] for case in cases),
        "gated_cases": len(gated),
        "mean_unknown_established_probability": mean(case["p_established"]["unknown"] for case in gated) if gated else math.nan,
        "mean_unknown_margin": mean(margins) if margins else math.nan,
        "bootstrap_95_ci": [ci_lo, ci_hi],
        "mean_paraphrase_margin": mean(case["paraphrase_margin"] for case in gated) if gated else math.nan,
        "mean_unknown_minus_distinct": mean(case["unknown_vs_distinct"] for case in gated) if gated else math.nan,
        "mean_reminder_rescue": mean(case["reminder_rescue"] for case in gated) if gated else math.nan,
        "mean_natural_variant_positive_fraction": mean(case["natural_variant_positive_fraction"] for case in gated) if gated else math.nan,
        "neutral_artifact_fraction": neutral_artifact_fraction,
        "strong_fraction": mean(float(case["strong"]) for case in gated) if gated else 0.0,
        "positive_domains": sum(
            info["gated"] >= 2 and info["mean_unknown_margin"] > 0 for info in by_domain.values()
        ),
    }

    enough_gated = aggregate["gated_cases"] >= pc["min_gated_cases"]
    model_pass = (
        enough_gated
        and aggregate["mean_unknown_margin"] >= pc["min_mean_unknown_margin"]
        and ci_lo >= pc["min_bootstrap_ci_lower"]
        and aggregate["mean_paraphrase_margin"] >= pc["min_mean_paraphrase_margin"]
        and aggregate["mean_unknown_minus_distinct"] >= pc["min_mean_unknown_minus_distinct"]
        and aggregate["strong_fraction"] >= pc["min_strong_fraction"]
        and aggregate["positive_domains"] >= pc["min_positive_domains"]
        and neutral_artifact_fraction <= pc["max_neutral_artifact_fraction"]
        and aggregate["mean_natural_variant_positive_fraction"] >= pc["min_natural_variant_positive_fraction"]
    )

    recognition_fraction = aggregate["recognition_gated_cases"] / len(cases) if cases else 0.0
    if len(cases) >= pc["min_gated_cases"] and recognition_fraction < pc["min_recognition_gate_fraction"]:
        verdict = "HARD-KILL-QUANTIFIER-CAPABILITY-FLOOR"
    elif enough_gated and abs(aggregate["mean_unknown_margin"]) < pc["no_effect_abs_margin"]:
        verdict = "HARD-KILL-NO-ILLEGAL-JOIN"
    elif enough_gated and aggregate["mean_unknown_margin"] > 0 and aggregate["mean_paraphrase_margin"] <= 0:
        verdict = "HOLD-WORDING-ARTIFACT"
    elif neutral_artifact_fraction > pc["max_neutral_artifact_fraction"]:
        verdict = "HOLD-GENERIC-CONTEXT-ARTIFACT"
    else:
        verdict = "PASS-TO-PANEL" if model_pass else "FAIL-MODEL-G0"

    summary = {
        "contract": "Existential Witness Collapse",
        "model": rows[0].get("model"),
        "family": rows[0].get("family"),
        "revision": rows[0].get("revision"),
        "size_b": rows[0].get("size_b"),
        "model_pass": model_pass,
        "verdict": verdict,
        "aggregate": aggregate,
        "by_domain": by_domain,
        "cases": cases,
        "hard_kill_note": (
            "Only gate-correct cases count. The primary error is an ESTABLISHED preference in the identity-unknown world, "
            "replicated under a natural paraphrase, while explicit-same and explicit-distinct controls remain correct. "
            "Failure of the quantifier/identity gate is ordinary reasoning error, not witness collapse."
        ),
    }
    if out_path:
        p = Path(out_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=True), encoding="utf-8")
    return summary
