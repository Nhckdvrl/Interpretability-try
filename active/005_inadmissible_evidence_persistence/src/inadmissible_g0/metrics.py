from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any
import json, math, random

from .data import load_scenarios


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    out = []
    with Path(path).open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if line.strip():
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


def summarize(*, data_path: str, results_path: str, config_path: str,
              out_path: str | None = None) -> dict[str, Any]:
    scenarios = load_scenarios(data_path, require_external_source=True)
    by_id = {s.scenario_id: s for s in scenarios}
    rows = read_jsonl(results_path)
    if not rows:
        raise ValueError("results are empty")
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen = set()

    for row in rows:
        sid = str(row["scenario_id"])
        if sid not in by_id:
            raise ValueError(f"unknown scenario_id={sid}")
        if row["kind"] == "recognition":
            uniq = (sid, "r", row["probe"], int(row["label_order"]))
        elif row["kind"] == "verdict":
            uniq = (
                sid, "v", row["template_kind"], int(row["template_id"]),
                row["condition"], int(row["label_order"]),
            )
        else:
            raise ValueError(f"unknown kind={row['kind']}")
        if uniq in seen:
            raise ValueError(f"duplicate result variant={uniq}")
        seen.add(uniq)
        grouped[sid].append(row)

    missing = set(by_id) - set(grouped)
    if missing:
        raise ValueError(f"missing results; first={sorted(missing)[:3]}")

    rec_cfg = cfg["recognition_gate"]
    cap_cfg = cfg["capability_gate"]
    strong_cfg = cfg["strong_case"]
    cases = []

    expected_rec = {(p, o) for p in ("inadmissible", "scope", "polarity") for o in (0, 1)}
    expected_verdict = {
        (kind, tid, cond, order)
        for tid, kind in ((0, "natural"), (1, "rule_reminder"))
        for cond in ("never_seen", "admitted", "struck", "neutral_struck")
        for order in (0, 1)
    }

    for sid in sorted(by_id):
        s = by_id[sid]
        rs = grouped[sid]
        rec = [r for r in rs if r["kind"] == "recognition"]
        rec_keys = {(r["probe"], int(r["label_order"])) for r in rec}
        if rec_keys != expected_rec:
            raise ValueError(f"{sid}: malformed recognition coverage")
        rp = {
            probe: mean(float(r["p_correct"]) for r in rec if r["probe"] == probe)
            for probe in ("inadmissible", "scope", "polarity")
        }
        recognition_gate = (
            rp["inadmissible"] >= rec_cfg["min_admissibility_probability"]
            and rp["scope"] >= rec_cfg["min_scope_probability"]
            and rp["polarity"] >= rec_cfg["min_polarity_probability"]
        )

        verdict = [r for r in rs if r["kind"] == "verdict"]
        v_keys = {
            (r["template_kind"], int(r["template_id"]), r["condition"], int(r["label_order"]))
            for r in verdict
        }
        if v_keys != expected_verdict:
            raise ValueError(f"{sid}: malformed verdict coverage; missing={expected_verdict-v_keys} extra={v_keys-expected_verdict}")

        def probs(template_kind: str) -> dict[str, float]:
            sub = [r for r in verdict if r["template_kind"] == template_kind]
            return {
                cond: mean(float(r["p_target"]) for r in sub if r["condition"] == cond)
                for cond in ("never_seen", "admitted", "struck", "neutral_struck")
            }

        p = probs("natural")
        p_reminder = probs("rule_reminder")
        sign = 1.0 if s.evidence_polarity == "supports_target" else -1.0

        admitted_shift = sign * (p["admitted"] - p["never_seen"])
        struck_residual = sign * (p["struck"] - p["never_seen"])
        undo_ratio = struck_residual / admitted_shift if admitted_shift > 1e-9 else math.nan
        neutral_shift = abs(p["neutral_struck"] - p["never_seen"])

        reminder_admitted_shift = sign * (p_reminder["admitted"] - p_reminder["never_seen"])
        reminder_struck_residual = sign * (p_reminder["struck"] - p_reminder["never_seen"])
        reminder_rescue = struck_residual - reminder_struck_residual

        capability_gate = recognition_gate and admitted_shift >= cap_cfg["min_admissible_directional_shift"]
        neutral_ok = neutral_shift <= strong_cfg["max_neutral_struck_abs_shift"]
        strong = (
            capability_gate and neutral_ok
            and struck_residual >= strong_cfg["min_struck_directional_residual"]
            and not math.isnan(undo_ratio) and undo_ratio >= strong_cfg["min_undo_ratio"]
        )
        cases.append({
            "scenario_id": sid, "domain": s.domain, "polarity": s.evidence_polarity,
            "recognition": rp, "recognition_gate": recognition_gate,
            "p_target_never_seen": p["never_seen"],
            "p_target_admitted": p["admitted"],
            "p_target_struck": p["struck"],
            "p_target_neutral_struck": p["neutral_struck"],
            "admitted_directional_shift": admitted_shift,
            "struck_directional_residual": struck_residual,
            "undo_ratio": undo_ratio,
            "neutral_struck_abs_shift": neutral_shift,
            "rule_reminder_admitted_shift": reminder_admitted_shift,
            "rule_reminder_struck_residual": reminder_struck_residual,
            "rule_reminder_rescue": reminder_rescue,
            "capability_gate": capability_gate,
            "neutral_ok": neutral_ok,
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

    polarity_stats = {}
    for i, pol in enumerate(("supports_target", "supports_other")):
        sub = [r for r in gated if r["polarity"] == pol]
        vals = [r["struck_directional_residual"] for r in sub]
        plo, phi = bootstrap_ci(vals, seed=cfg["seed"] + i + 1, n_boot=cfg["bootstrap_samples"])
        polarity_stats[pol] = {
            "gated": len(sub),
            "mean_admitted_shift": mean(r["admitted_directional_shift"] for r in sub) if sub else math.nan,
            "mean_struck_residual": mean(vals) if vals else math.nan,
            "bootstrap_95_ci": [plo, phi],
            "strong": sum(bool(r["strong"]) for r in sub),
        }

    neutral_artifact_fraction = sum(not r["neutral_ok"] for r in gated) / len(gated) if gated else 0.0
    positive_domains = sum(
        v["gated"] >= 2 and v["mean_struck_directional_residual"] > 0
        for v in by_domain.values()
    )
    pcfg = cfg["model_pass"]
    aggregate = {
        "total_cases": len(cases),
        "gated_cases": len(gated),
        "mean_struck_directional_residual": mean(residuals) if residuals else math.nan,
        "bootstrap_95_ci": [ci_lo, ci_hi],
        "mean_undo_ratio": mean(r["undo_ratio"] for r in gated if not math.isnan(r["undo_ratio"])) if gated else math.nan,
        "strong_cases": sum(bool(r["strong"]) for r in gated),
        "strong_fraction": mean(float(r["strong"]) for r in gated) if gated else 0.0,
        "positive_domains": positive_domains,
        "neutral_artifact_fraction": neutral_artifact_fraction,
        "mean_rule_reminder_struck_residual": mean(r["rule_reminder_struck_residual"] for r in gated) if gated else math.nan,
        "mean_rule_reminder_rescue": mean(r["rule_reminder_rescue"] for r in gated) if gated else math.nan,
    }

    polarity_pass = all(
        polarity_stats[pol]["gated"] >= pcfg["min_gated_per_polarity"]
        and polarity_stats[pol]["mean_struck_residual"] >= pcfg["min_mean_residual_per_polarity"]
        for pol in ("supports_target", "supports_other")
    )
    enough_for_polarity_diagnosis = all(
        polarity_stats[pol]["gated"] >= pcfg["min_gated_per_polarity"]
        for pol in ("supports_target", "supports_other")
    )
    model_pass = (
        aggregate["gated_cases"] >= pcfg["min_gated_cases"]
        and aggregate["mean_struck_directional_residual"] >= pcfg["min_mean_struck_directional_residual"]
        and ci_lo >= pcfg["min_bootstrap_ci_lower"]
        and aggregate["strong_fraction"] >= pcfg["min_strong_fraction"]
        and positive_domains >= pcfg["min_positive_domains"]
        and neutral_artifact_fraction <= pcfg["max_neutral_artifact_fraction"]
        and polarity_pass
    )

    if neutral_artifact_fraction > pcfg["max_neutral_artifact_fraction"]:
        verdict = "HOLD-GENERIC-SALIENCE-ARTIFACT"
    elif enough_for_polarity_diagnosis and not polarity_pass:
        verdict = "HOLD-POLARITY-ASYMMETRY"
    elif aggregate["gated_cases"] >= pcfg["min_gated_cases"] and abs(aggregate["mean_struck_directional_residual"]) < 0.01:
        verdict = "HARD-KILL-NO-PERSISTENCE"
    else:
        verdict = "PASS-TO-PANEL" if model_pass else "FAIL-MODEL-G0"

    summary = {
        "contract": "Inadmissible-Evidence Persistence",
        "model": rows[0].get("model"),
        "family": rows[0].get("family"),
        "revision": rows[0].get("revision"),
        "size_b": rows[0].get("size_b"),
        "model_pass": model_pass,
        "verdict": verdict,
        "aggregate": aggregate,
        "by_domain": by_domain,
        "by_polarity": polarity_stats,
        "cases": cases,
        "hard_kill_note": (
            "Kill standalone novelty if persistence disappears after admissibility/scope/polarity gates. "
            "A one-sided polarity result is HOLD rather than a pooled hard kill; neutral salience artifacts also take precedence. "
            "Natural verdict readout is primary; explicit rule reminders are a rescue diagnostic, not part of the primary mean."
        ),
    }
    if out_path:
        pth = Path(out_path)
        pth.parent.mkdir(parents=True, exist_ok=True)
        pth.write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=True), encoding="utf-8")
    return summary
