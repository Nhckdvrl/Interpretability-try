from __future__ import annotations

import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from .data import load_scenarios
from .prompts import VERDICT_TEMPLATES


def read_jsonl(path):
    out = []
    with Path(path).open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid results JSONL line {line_number}") from exc
    return out


def bootstrap_ci(values, *, seed, n_boot):
    """Ordinary bootstrap over the supplied independent units.

    The r5 caller supplies one value per polarity_pair_id, so this is a
    pair-cluster bootstrap rather than a case-level bootstrap.
    """
    if not values:
        return math.nan, math.nan
    rng = random.Random(seed)
    n = len(values)
    draws = sorted(mean(values[rng.randrange(n)] for _ in range(n)) for _ in range(n_boot))
    return draws[int(0.025 * (n_boot - 1))], draws[int(0.975 * (n_boot - 1))]


def _assert_run_metadata_consistent(rows):
    for field in ("model", "family", "revision", "size_b", "requested_dtype"):
        values = {json.dumps(row.get(field), sort_keys=True) for row in rows}
        if len(values) != 1:
            raise ValueError(f"inconsistent run metadata for {field}: {values}")


def _neutral_ok(neutral_shift, residual, strong_case):
    if neutral_shift > strong_case["max_neutral_struck_abs_shift"]:
        return False
    if abs(residual) >= strong_case["min_struck_directional_residual"]:
        return neutral_shift <= strong_case["max_neutral_to_struck_ratio"] * abs(residual)
    return True


def _mean_by_condition(rows):
    return {
        condition: mean(float(row["p_target"]) for row in rows if row["condition"] == condition)
        for condition in ("never_seen", "admitted", "struck", "neutral_struck")
    }


def summarize(*, data_path: str, results_path: str, config_path: str, out_path: str | None = None) -> dict[str, Any]:
    scenarios = load_scenarios(data_path, require_external_source=True)
    by_id = {scenario.scenario_id: scenario for scenario in scenarios}
    rows = read_jsonl(results_path)
    if not rows:
        raise ValueError("results are empty")
    _assert_run_metadata_consistent(rows)
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))

    grouped: dict[str, list[dict]] = defaultdict(list)
    seen = set()
    for row in rows:
        scenario_id = str(row["scenario_id"])
        if scenario_id not in by_id:
            raise ValueError(f"unknown scenario_id={scenario_id}")
        if row.get("polarity_pair_id") != by_id[scenario_id].polarity_pair_id:
            raise ValueError(f"{scenario_id}: polarity_pair_id mismatch")
        if row["kind"] == "recognition":
            unique = (scenario_id, "recognition", row["probe"], int(row["label_order"]))
        elif row["kind"] == "verdict":
            unique = (
                scenario_id, "verdict", row["template_kind"], int(row["template_id"]),
                row["condition"], int(row["label_order"]),
            )
        else:
            raise ValueError(f"unknown kind={row['kind']}")
        if unique in seen:
            raise ValueError(f"duplicate result variant={unique}")
        seen.add(unique)
        grouped[scenario_id].append(row)
    if set(by_id) - set(grouped):
        raise ValueError("missing results")

    expected_recognition = {(probe, order) for probe in ("inadmissible", "scope", "polarity") for order in (0, 1)}
    expected_verdict = {
        (kind, template_id, condition, order)
        for template_id, (kind, _) in enumerate(VERDICT_TEMPLATES)
        for condition in ("never_seen", "admitted", "struck", "neutral_struck")
        for order in (0, 1)
    }
    recognition_contract = config["recognition_gate"]
    capability_contract = config["capability_gate"]
    strong_contract = config["strong_case"]

    cases = []
    for scenario_id in sorted(by_id):
        scenario = by_id[scenario_id]
        scenario_rows = grouped[scenario_id]
        recognition_rows = [row for row in scenario_rows if row["kind"] == "recognition"]
        coverage = {(row["probe"], int(row["label_order"])) for row in recognition_rows}
        if coverage != expected_recognition:
            raise ValueError(f"{scenario_id}: malformed recognition coverage")
        recognition = {}
        recognition_order_gap = {}
        for probe in ("inadmissible", "scope", "polarity"):
            values = [
                float(row["p_correct"]) for row in sorted(
                    (row for row in recognition_rows if row["probe"] == probe),
                    key=lambda row: int(row["label_order"]),
                )
            ]
            recognition[probe] = mean(values)
            recognition_order_gap[probe] = abs(values[0] - values[1])
        legal_recognition_gate = (
            recognition["inadmissible"] >= recognition_contract["min_admissibility_probability"]
            and recognition["scope"] >= recognition_contract["min_scope_probability"]
            and recognition_order_gap["inadmissible"] <= recognition_contract["max_answer_order_probability_gap"]
            and recognition_order_gap["scope"] <= recognition_contract["max_answer_order_probability_gap"]
        )
        polarity_diagnostic_gate = (
            recognition["polarity"] >= recognition_contract["min_polarity_probability_diagnostic"]
            and recognition_order_gap["polarity"] <= recognition_contract["max_answer_order_probability_gap"]
        )

        verdict_rows = [row for row in scenario_rows if row["kind"] == "verdict"]
        coverage = {
            (row["template_kind"], int(row["template_id"]), row["condition"], int(row["label_order"]))
            for row in verdict_rows
        }
        if coverage != expected_verdict:
            raise ValueError(f"{scenario_id}: malformed verdict coverage")
        natural = [row for row in verdict_rows if row["template_kind"] == "natural"]
        reminder = [row for row in verdict_rows if row["template_kind"] == "rule_reminder"]
        probabilities = _mean_by_condition(natural)
        reminder_probabilities = _mean_by_condition(reminder)
        sign = 1.0 if scenario.evidence_polarity == "supports_target" else -1.0
        admitted_shift = sign * (probabilities["admitted"] - probabilities["never_seen"])
        struck_residual = sign * (probabilities["struck"] - probabilities["never_seen"])
        reminder_residual = sign * (reminder_probabilities["struck"] - reminder_probabilities["never_seen"])
        natural_variants = {
            (int(row["template_id"]), int(row["label_order"]), row["condition"]): float(row["p_target"])
            for row in natural
        }
        cases.append({
            "scenario_id": scenario_id,
            "polarity_pair_id": scenario.polarity_pair_id,
            "domain": scenario.domain,
            "polarity": scenario.evidence_polarity,
            "exclusion_reason_type": scenario.exclusion_reason_type,
            "recognition": recognition,
            "recognition_answer_order_gap": recognition_order_gap,
            "legal_recognition_gate": legal_recognition_gate,
            "polarity_diagnostic_gate": polarity_diagnostic_gate,
            "p_target_never_seen": probabilities["never_seen"],
            "p_target_admitted": probabilities["admitted"],
            "p_target_struck": probabilities["struck"],
            "p_target_neutral_struck": probabilities["neutral_struck"],
            "admitted_directional_shift_diagnostic": admitted_shift,
            "struck_directional_residual_diagnostic": struck_residual,
            "rule_reminder_rescue_diagnostic": struck_residual - reminder_residual,
            "natural_variants": {f"t{key[0]}:o{key[1]}:{key[2]}": value for key, value in natural_variants.items()},
        })

    case_groups: dict[str, list[dict]] = defaultdict(list)
    for case in cases:
        case_groups[case["polarity_pair_id"]].append(case)
    pairs = []
    for pair_id, pair_cases in sorted(case_groups.items()):
        if len(pair_cases) != 2:
            raise ValueError(f"{pair_id}: malformed polarity pair")
        members = {case["polarity"]: case for case in pair_cases}
        target = members["supports_target"]
        other = members["supports_other"]
        target_variants = target["natural_variants"]
        other_variants = other["natural_variants"]
        variant_keys = sorted({key.rsplit(":", 1)[0] for key in target_variants})
        admitted_deltas = []
        struck_deltas = []
        baseline_deltas = []
        neutral_shifts = []
        for prefix in variant_keys:
            target_base = target_variants[f"{prefix}:never_seen"]
            other_base = other_variants[f"{prefix}:never_seen"]
            admitted_deltas.append(target_variants[f"{prefix}:admitted"] - other_variants[f"{prefix}:admitted"])
            struck_deltas.append(target_variants[f"{prefix}:struck"] - other_variants[f"{prefix}:struck"])
            baseline_deltas.append(abs(target_base - other_base))
            neutral_shifts.extend((
                abs(target_variants[f"{prefix}:neutral_struck"] - target_base),
                abs(other_variants[f"{prefix}:neutral_struck"] - other_base),
            ))
        admitted_delta = mean(admitted_deltas)
        struck_delta = mean(struck_deltas)
        baseline_delta = mean(baseline_deltas)
        neutral_shift = mean(neutral_shifts)
        admitted_positive_fraction = mean(float(value > 0) for value in admitted_deltas)
        struck_positive_fraction = mean(float(value > 0) for value in struck_deltas)
        pair_capability_gate = (
            target["legal_recognition_gate"] and other["legal_recognition_gate"]
            and admitted_delta >= capability_contract["min_admitted_polarity_delta"]
            and admitted_positive_fraction >= capability_contract["min_admitted_variant_positive_fraction"]
            and baseline_delta <= capability_contract["max_never_seen_pair_delta"]
        )
        neutral_ok = _neutral_ok(neutral_shift, struck_delta, strong_contract)
        pair_undo_ratio = struck_delta / admitted_delta if admitted_delta > 1e-9 else math.nan
        strong = (
            pair_capability_gate and neutral_ok
            and struck_delta >= strong_contract["min_struck_directional_residual"]
            and pair_undo_ratio >= strong_contract["min_undo_ratio"]
            and struck_positive_fraction >= strong_contract["min_natural_variant_positive_fraction"]
        )
        pairs.append({
            "polarity_pair_id": pair_id,
            "exclusion_reason_type": target["exclusion_reason_type"],
            "pair_capability_gate": pair_capability_gate,
            "polarity_diagnostic_pair_gate": target["polarity_diagnostic_gate"] and other["polarity_diagnostic_gate"],
            "never_seen_pair_delta": baseline_delta,
            "admitted_polarity_delta": admitted_delta,
            "admitted_variant_positive_fraction": admitted_positive_fraction,
            "struck_polarity_delta": struck_delta,
            "struck_variant_positive_fraction": struck_positive_fraction,
            "pair_undo_ratio": pair_undo_ratio,
            "neutral_struck_abs_shift": neutral_shift,
            "neutral_ok": neutral_ok,
            "strong": strong,
        })

    gated_pairs = [pair for pair in pairs if pair["pair_capability_gate"]]
    pair_values = [pair["struck_polarity_delta"] for pair in gated_pairs]
    lower, upper = bootstrap_ci(pair_values, seed=config["seed"], n_boot=config["bootstrap_samples"])
    neutral_artifact_fraction = (
        mean(float(not pair["neutral_ok"]) for pair in gated_pairs) if gated_pairs else 1.0
    )
    reason_breakdown = {}
    for reason in ("procedural_truth_neutral", "reliability_based"):
        selected = [pair for pair in gated_pairs if pair["exclusion_reason_type"] == reason]
        values = [pair["struck_polarity_delta"] for pair in selected]
        reason_lower, reason_upper = bootstrap_ci(
            values, seed=config["seed"] + len(reason), n_boot=config["bootstrap_samples"]
        )
        reason_breakdown[reason] = {
            "gated_pairs": len(selected),
            "mean_struck_polarity_delta": mean(values) if values else math.nan,
            "pair_cluster_bootstrap_95_ci": [reason_lower, reason_upper],
            "neutral_artifact_fraction": mean(float(not pair["neutral_ok"]) for pair in selected) if selected else math.nan,
        }

    calibration = config["calibration_gate"]
    pair_capability_fraction = len(gated_pairs) / len(pairs)
    calibration_contract_pass = (
        pair_capability_fraction >= calibration["min_pair_capability_fraction"]
        and neutral_artifact_fraction <= calibration["max_neutral_artifact_fraction"]
        and all(
            reason_breakdown[reason]["gated_pairs"] >= calibration["min_pairs_per_exclusion_reason"]
            for reason in reason_breakdown
        )
    )
    paired = config["paired_operator"]
    phenotype_present = (
        calibration_contract_pass
        and len(gated_pairs) >= paired["min_gated_pairs"]
        and mean(pair_values) >= paired["min_mean_struck_polarity_delta"]
        and lower >= paired["min_bootstrap_ci_lower"]
        and mean(pair["struck_variant_positive_fraction"] for pair in gated_pairs)
        >= paired["min_struck_variant_positive_fraction"]
    )
    if not calibration_contract_pass:
        verdict = "TERMINAL-HOLD-D0V3-CONTRACT"
    elif phenotype_present:
        verdict = "CALIBRATION-PHENOTYPE-PRESENT"
    elif upper < -paired["min_bootstrap_ci_lower"]:
        verdict = "CALIBRATION-INVERSION-DIAGNOSTIC"
    elif abs(mean(pair_values)) < 0.01:
        verdict = "CALIBRATION-HARD-NULL"
    else:
        verdict = "CALIBRATION-NO-STABLE-PHENOTYPE"

    aggregate = {
        "total_pairs": len(pairs),
        "gated_pairs": len(gated_pairs),
        "pair_capability_fraction": pair_capability_fraction,
        "polarity_diagnostic_pair_fraction": mean(float(pair["polarity_diagnostic_pair_gate"]) for pair in pairs),
        "mean_struck_polarity_delta": mean(pair_values) if pair_values else math.nan,
        "pair_cluster_bootstrap_95_ci": [lower, upper],
        "mean_struck_variant_positive_fraction": (
            mean(pair["struck_variant_positive_fraction"] for pair in gated_pairs) if gated_pairs else math.nan
        ),
        "neutral_artifact_fraction": neutral_artifact_fraction,
        "strong_pair_fraction": mean(float(pair["strong"]) for pair in gated_pairs) if gated_pairs else 0.0,
    }
    summary = {
        "contract": "Inadmissible-Evidence Persistence r5 final calibration",
        "model": rows[0].get("model"),
        "family": rows[0].get("family"),
        "revision": rows[0].get("revision"),
        "size_b": rows[0].get("size_b"),
        "model_pass": False,
        "calibration_contract_pass": calibration_contract_pass,
        "phenotype_present": phenotype_present,
        "verdict": verdict,
        "aggregate": aggregate,
        "by_exclusion_reason": reason_breakdown,
        "pairs": pairs,
        "cases": cases,
        "stop_rule": "This is the single final D0 v3 calibration. Do not create a v4/v5 rescue loop.",
        "authorization_note": "EXPLORATORY-LOCAL; formal N0/D0 registry authorization remains false.",
    }
    if out_path:
        output = Path(out_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=True), encoding="utf-8")
    return summary
