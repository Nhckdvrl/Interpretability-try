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


def _variant_bias(row: dict[str, Any]) -> float:
    if row["variant_side"] == "right":
        return float(row["p_right_more"]) - float(row["p_left_more"])
    if row["variant_side"] == "left":
        return float(row["p_left_more"]) - float(row["p_right_more"])
    raise ValueError(f"unknown variant_side={row['variant_side']}")


def _variant_more_prob(row: dict[str, Any]) -> float:
    return float(row["p_right_more"] if row["variant_side"] == "right" else row["p_left_more"])


def _focal_score(row: dict[str, Any]) -> float:
    if row["focal_side"] == "left":
        return float(row["p_left_more"]) - float(row["p_right_more"])
    if row["focal_side"] == "right":
        return float(row["p_right_more"]) - float(row["p_left_more"])
    raise ValueError(f"unknown focal_side={row['focal_side']}")


def summarize(*, data_path: str, results_path: str, config_path: str,
              out_path: str | None = None) -> dict[str, Any]:
    scenarios = load_scenarios(data_path, require_external_source=True)
    valid_keys = {(s.scenario_id, p.partition_id) for s in scenarios for p in s.partitions}
    rows = read_jsonl(results_path)
    if not rows:
        raise ValueError("results are empty")
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    seen = set()
    for row in rows:
        key = (str(row["scenario_id"]), str(row["partition_id"]))
        if key not in valid_keys:
            raise ValueError(f"unknown result key={key}")
        kind = row["kind"]
        if kind == "recognition":
            uniq = key + ("r", row["probe"], int(row["label_order"]))
        elif kind == "judgment":
            uniq = key + (
                "j", row["readout"], row["template_kind"], int(row["template_id"]),
                row["condition"], int(row["side_order"]), int(row["label_order"]),
            )
        elif kind == "focal_alternative":
            uniq = key + (
                "f", row["readout"], row["template_kind"], int(row["template_id"]),
                row["condition"], int(row["side_order"]), int(row["label_order"]),
            )
        else:
            raise ValueError(f"unknown kind={kind}")
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

    expected_j_keys = {
        (readout, template_kind, template_id, condition, side_order, label_order)
        for readout in ("probability", "decision")
        for template_id, template_kind in ((0, "natural"), (1, "extensional_reminder"))
        for condition in ("core", "paraphrase", "partial_subset", "repacked")
        for side_order in (0, 1)
        for label_order in range(6)
    }
    expected_f_keys = {
        (readout, template_kind, template_id, condition, side_order, label_order)
        for readout in ("probability", "decision")
        for template_id, template_kind in ((0, "natural"), (1, "extensional_reminder"))
        for condition in ("focal_unpacked_context", "alternative_unpacked_context")
        for side_order in (0, 1)
        for label_order in range(6)
    }

    for key in sorted(valid_keys):
        rs = grouped[key]
        rec = [r for r in rs if r["kind"] == "recognition"]
        expected_rec_keys = {(p, o) for p in ("equivalent", "disjoint", "exhaustive") for o in (0, 1)}
        rec_keys = {(r["probe"], int(r["label_order"])) for r in rec}
        if rec_keys != expected_rec_keys:
            raise ValueError(f"{key}: malformed recognition coverage")
        probe_probs = {
            probe: mean(float(r["p_correct"]) for r in rec if r["probe"] == probe)
            for probe in ("equivalent", "disjoint", "exhaustive")
        }
        recognition_min = min(probe_probs.values())
        recognition_mean = mean(probe_probs.values())
        gated = (
            recognition_min >= rec_cfg["min_probe_probability"]
            and recognition_mean >= rec_cfg["min_mean_probability"]
        )

        js = [r for r in rs if r["kind"] == "judgment"]
        j_keys = {
            (r["readout"], r["template_kind"], int(r["template_id"]), r["condition"], int(r["side_order"]), int(r["label_order"]))
            for r in js
        }
        if j_keys != expected_j_keys:
            raise ValueError(f"{key}: malformed judgment coverage; missing={len(expected_j_keys-j_keys)} extra={len(j_keys-expected_j_keys)}")

        fs = [r for r in rs if r["kind"] == "focal_alternative"]
        f_keys = {
            (r["readout"], r["template_kind"], int(r["template_id"]), r["condition"], int(r["side_order"]), int(r["label_order"]))
            for r in fs
        }
        if f_keys != expected_f_keys:
            raise ValueError(f"{key}: malformed focal/alternative coverage")

        natural = [r for r in js if r["template_kind"] == "natural"]
        reminder = [r for r in js if r["template_kind"] == "extensional_reminder"]

        def mean_bias(sub: list[dict[str, Any]], condition: str, readout: str | None = None) -> float:
            z = [r for r in sub if r["condition"] == condition and (readout is None or r["readout"] == readout)]
            if not z:
                return math.nan
            return mean(_variant_bias(r) for r in z)

        def mean_variant_more(sub: list[dict[str, Any]], condition: str) -> float:
            z = [r for r in sub if r["condition"] == condition]
            return mean(_variant_more_prob(r) for r in z)

        core_bias = mean_bias(natural, "core")
        paraphrase_bias = mean_bias(natural, "paraphrase")
        partial_discrimination = -mean_bias(natural, "partial_subset")
        repacked_bias = mean_bias(natural, "repacked")
        repacking_recovery = core_bias - repacked_bias
        reminder_core_bias = mean_bias(reminder, "core")
        reminder_rescue = core_bias - reminder_core_bias

        natural_f = [r for r in fs if r["template_kind"] == "natural"]
        focal_unpacked_score = mean(_focal_score(r) for r in natural_f if r["condition"] == "focal_unpacked_context")
        alternative_unpacked_score = mean(_focal_score(r) for r in natural_f if r["condition"] == "alternative_unpacked_context")
        focal_alternative_shift = focal_unpacked_score - alternative_unpacked_score

        readout_bias = {
            readout: mean_bias(natural, "core", readout)
            for readout in ("probability", "decision")
        }
        positive_readouts = sum(v > 0 for v in readout_bias.values())
        control_ok = (
            abs(paraphrase_bias) <= ctrl_cfg["max_abs_paraphrase_bias"]
            and partial_discrimination >= ctrl_cfg["min_partial_subset_discrimination"]
        )
        structural_ok = (
            repacking_recovery >= strong_cfg["min_repacking_recovery"]
            and focal_alternative_shift >= strong_cfg["min_focal_alternative_shift"]
            and positive_readouts >= strong_cfg["min_positive_readouts"]
        )
        strong = (
            gated and control_ok and structural_ok
            and core_bias >= strong_cfg["min_core_unpacked_bias"]
            and mean_variant_more(natural, "core") >= strong_cfg["min_unpacked_more_probability"]
        )
        case_rows.append({
            "scenario_id": key[0], "partition_id": key[1],
            "branch_count": int(next(r["branch_count"] for r in rs)),
            "domain": next(r["domain"] for r in rs),
            "recognition": probe_probs, "recognition_min": recognition_min,
            "recognition_mean": recognition_mean, "gated": gated,
            "core_unpacked_bias": core_bias,
            "core_p_unpacked_more": mean_variant_more(natural, "core"),
            "core_bias_by_readout": readout_bias,
            "paraphrase_bias": paraphrase_bias,
            "partial_subset_discrimination": partial_discrimination,
            "repacked_bias": repacked_bias,
            "repacking_recovery": repacking_recovery,
            "focal_unpacked_score": focal_unpacked_score,
            "alternative_unpacked_score": alternative_unpacked_score,
            "focal_alternative_shift": focal_alternative_shift,
            "reminder_core_bias": reminder_core_bias,
            "reminder_rescue": reminder_rescue,
            "control_ok": control_ok, "structural_ok": structural_ok, "strong": strong,
        })

    by_scenario_cases: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in case_rows:
        if r["gated"]:
            by_scenario_cases[r["scenario_id"]].append(r)
    scenario_rows = []
    for sid, sub in sorted(by_scenario_cases.items()):
        scenario_rows.append({
            "scenario_id": sid,
            "domain": sub[0]["domain"],
            "gated_partitions": len(sub),
            "mean_core_unpacked_bias": mean(r["core_unpacked_bias"] for r in sub),
            "mean_focal_alternative_shift": mean(r["focal_alternative_shift"] for r in sub),
            "mean_repacking_recovery": mean(r["repacking_recovery"] for r in sub),
            "control_ok_fraction": mean(float(r["control_ok"]) for r in sub),
            "strong_partition_fraction": mean(float(r["strong"]) for r in sub),
            "strong": mean(float(r["strong"]) for r in sub) >= 0.5,
        })

    scenario_core = [r["mean_core_unpacked_bias"] for r in scenario_rows]
    ci_lo, ci_hi = bootstrap_ci(scenario_core, seed=cfg["seed"], n_boot=cfg["bootstrap_samples"])

    by_domain = {}
    for d in sorted({r["domain"] for r in scenario_rows}):
        sub = [r for r in scenario_rows if r["domain"] == d]
        by_domain[d] = {
            "gated_scenarios": len(sub),
            "mean_core_unpacked_bias": mean(r["mean_core_unpacked_bias"] for r in sub),
            "strong_scenarios": sum(bool(r["strong"]) for r in sub),
        }

    within_scenario_slopes = {}
    for sid, sub in by_scenario_cases.items():
        by_k: dict[int, list[float]] = defaultdict(list)
        for r in sub:
            by_k[int(r["branch_count"])].append(float(r["core_unpacked_bias"]))
        ks = sorted(by_k)
        if len(ks) >= 2 and ks[-1] != ks[0]:
            low = mean(by_k[ks[0]])
            high = mean(by_k[ks[-1]])
            within_scenario_slopes[sid] = (high - low) / (ks[-1] - ks[0])

    readout_scenario_means = {}
    for readout in ("probability", "decision"):
        vals = [mean(r["core_bias_by_readout"][readout] for r in sub) for sub in by_scenario_cases.values()]
        readout_scenario_means[readout] = mean(vals) if vals else math.nan

    pcfg = cfg["model_pass"]
    positive_domains = sum(
        v["gated_scenarios"] >= 2 and v["mean_core_unpacked_bias"] > 0
        for v in by_domain.values()
    )
    aggregate = {
        "total_partition_cases": len(case_rows),
        "gated_partition_cases": sum(r["gated"] for r in case_rows),
        "gated_scenarios": len(scenario_rows),
        "mean_core_unpacked_bias": mean(scenario_core) if scenario_core else math.nan,
        "bootstrap_95_ci_clustered_by_scenario": [ci_lo, ci_hi],
        "strong_scenarios": sum(bool(r["strong"]) for r in scenario_rows),
        "strong_fraction": mean(float(r["strong"]) for r in scenario_rows) if scenario_rows else 0.0,
        "positive_domains": positive_domains,
        "mean_focal_alternative_shift": mean(r["mean_focal_alternative_shift"] for r in scenario_rows) if scenario_rows else math.nan,
        "mean_repacking_recovery": mean(r["mean_repacking_recovery"] for r in scenario_rows) if scenario_rows else math.nan,
        "core_bias_by_readout": readout_scenario_means,
        "branch_count_matched_scenarios": len(within_scenario_slopes),
        "mean_within_scenario_branch_count_slope": mean(within_scenario_slopes.values()) if within_scenario_slopes else math.nan,
        "artifact_failure_scenarios": sum(r["control_ok_fraction"] < 0.75 for r in scenario_rows),
    }
    model_pass = (
        aggregate["gated_scenarios"] >= pcfg["min_gated_scenarios"]
        and aggregate["mean_core_unpacked_bias"] >= pcfg["min_mean_core_unpacked_bias"]
        and ci_lo >= pcfg["min_bootstrap_ci_lower"]
        and aggregate["strong_fraction"] >= pcfg["min_strong_fraction"]
        and positive_domains >= pcfg["min_positive_domains"]
        and aggregate["mean_focal_alternative_shift"] >= pcfg["min_mean_focal_alternative_shift"]
        and sum(v > 0 for v in readout_scenario_means.values()) >= pcfg["min_positive_readouts"]
    )

    if aggregate["gated_scenarios"] >= pcfg["min_gated_scenarios"] and abs(aggregate["mean_core_unpacked_bias"]) < 0.02:
        verdict = "HARD-KILL-NO-PHENOMENON"
    elif aggregate["artifact_failure_scenarios"] > max(2, aggregate["gated_scenarios"] // 4):
        verdict = "HOLD-ARTIFACT-CONTROLS"
    else:
        verdict = "PASS-TO-PANEL" if model_pass else "FAIL-MODEL-G0"

    summary = {
        "contract": "Packed-Unpacked Event Splitting",
        "model": rows[0].get("model"),
        "family": rows[0].get("family"),
        "revision": rows[0].get("revision"),
        "size_b": rows[0].get("size_b"),
        "model_pass": model_pass,
        "verdict": verdict,
        "aggregate": aggregate,
        "by_domain": by_domain,
        "within_scenario_branch_count_slopes": within_scenario_slopes,
        "scenarios": scenario_rows,
        "cases": case_rows,
        "hard_kill_note": (
            "Kill standalone novelty if the natural-readout effect vanishes after relation gating, "
            "is matched by packed-paraphrase bias, fails the strict-subset control, or lacks the "
            "focal-vs-alternative/repacking structure that distinguishes partition support from generic wording sensitivity."
        ),
    }
    if out_path:
        p = Path(out_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=True), encoding="utf-8")
    return summary
