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
    return draws[int(.025 * (n_boot - 1))], draws[int(.975 * (n_boot - 1))]


def signed_update(direction: str, p_condition: float, p_baseline: float) -> float:
    raw = p_condition - p_baseline
    if direction == "supports_target":
        return raw
    if direction == "supports_other":
        return -raw
    raise ValueError(direction)


def _assert_metadata(rows: list[dict]) -> None:
    for field in ("model", "family", "revision", "size_b", "requested_dtype"):
        values = {json.dumps(row.get(field), sort_keys=True) for row in rows}
        if len(values) != 1:
            raise ValueError(f"inconsistent run metadata for {field}: {values}")


def compute_direction_features(*, direction: str, support: dict[str, float], support_min_variant: float,
                               readouts: dict[str, dict[str, float]], variants: dict[str, dict[str, list[float]]],
                               strong_variants: dict[str, list[float]], cfg: dict) -> dict[str, Any]:
    sg = cfg["support_gate"]
    cg = cfg["capability_gate"]
    sc = cfg["strong_case"]
    support_gate = (
        support["support"] >= sg["min_support_probability"]
        and support["likelihood_relation"] >= sg["min_likelihood_relation_probability"]
        and support["support_complete"] >= sg["min_complete_support_probability"]
        and support["strong_support"] >= sg["min_strong_support_probability"]
        and support["strong_gt_weak"] >= sg["min_strong_gt_weak_probability"]
        and support["neutral_non_support"] >= sg["min_neutral_non_support_probability"]
        and support_min_variant >= sg["min_probe_variant_probability"]
    )
    belief = readouts["belief"]
    action = readouts["action"]
    strong_b = signed_update(direction, belief["strong"], belief["no_evidence"])
    strong_a = signed_update(direction, action["strong"], action["no_evidence"])
    strong_variant_fraction = mean(
        float(value > 0) for value in (strong_variants["belief"] + strong_variants["action"])
    )
    capability = (
        support_gate
        and strong_b >= cg["min_strong_belief_directional_shift"]
        and strong_a >= cg["min_strong_action_directional_shift"]
        and strong_variant_fraction >= cg["min_strong_variant_positive_fraction"]
    )

    weak_b = -signed_update(direction, belief["weak"], belief["no_evidence"])
    weak_a = -signed_update(direction, action["weak"], action["no_evidence"])
    complete_b = -signed_update(direction, belief["weak_complete"], belief["no_evidence_complete"])
    complete_a = -signed_update(direction, action["weak_complete"], action["no_evidence_complete"])
    length_b = -signed_update(direction, belief["weak_length"], belief["no_evidence_length"])
    length_a = -signed_update(direction, action["weak_length"], action["no_evidence_length"])
    neutral_b = abs(belief["neutral"] - belief["no_evidence"])
    neutral_a = abs(action["neutral"] - action["no_evidence"])

    variant_fractions = {}
    for condition in ("weak", "weak_complete", "weak_length"):
        values = variants["belief"][condition] + variants["action"][condition]
        variant_fractions[condition] = mean(float(value > 0) for value in values)

    pragmatic = (
        complete_b >= sc["min_complete_belief_backfire"]
        and complete_a >= sc["min_complete_action_backfire"]
        and variant_fractions["weak_complete"] >= sc["min_control_variant_backfire_fraction"]
    )
    length_ok = (
        length_b >= sc["min_length_belief_backfire"]
        and length_a >= sc["min_length_action_backfire"]
        and variant_fractions["weak_length"] >= sc["min_control_variant_backfire_fraction"]
    )
    neutral_ok = neutral_b <= sc["max_neutral_abs_shift"] and neutral_a <= sc["max_neutral_abs_shift"]
    strong = (
        capability
        and weak_b >= sc["min_belief_backfire"]
        and weak_a >= sc["min_action_backfire"]
        and pragmatic
        and length_ok
        and neutral_ok
        and variant_fractions["weak"] >= sc["min_primary_variant_backfire_fraction"]
    )
    return {
        "support_gate": support_gate,
        "support_min_variant_probability": support_min_variant,
        "capability_gate": capability,
        "strong_belief_directional_shift": strong_b,
        "strong_action_directional_shift": strong_a,
        "strong_variant_positive_fraction": strong_variant_fraction,
        "belief_backfire": weak_b,
        "action_backfire": weak_a,
        "complete_belief_backfire": complete_b,
        "complete_action_backfire": complete_a,
        "length_belief_backfire": length_b,
        "length_action_backfire": length_a,
        "neutral_belief_abs_shift": neutral_b,
        "neutral_action_abs_shift": neutral_a,
        "primary_variant_backfire_fraction": variant_fractions["weak"],
        "complete_variant_backfire_fraction": variant_fractions["weak_complete"],
        "length_variant_backfire_fraction": variant_fractions["weak_length"],
        "pragmatic_robust": pragmatic,
        "length_robust": length_ok,
        "neutral_ok": neutral_ok,
        "strong": strong,
    }


def summarize(*, data_path: str, results_path: str, config_path: str,
              out_path: str | None = None) -> dict[str, Any]:
    scenarios = load_scenarios(data_path, require_external_source=True)
    by_id = {scenario.scenario_id: scenario for scenario in scenarios}
    rows = read_jsonl(results_path)
    if not rows:
        raise ValueError("results are empty")
    _assert_metadata(rows)
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
    grouped: dict[str, list[dict]] = defaultdict(list)
    seen: set[tuple] = set()

    for row in rows:
        sid = str(row.get("scenario_id"))
        if sid not in by_id:
            raise ValueError(f"unknown scenario_id={sid}")
        if row.get("direction") not in DIRECTIONS:
            raise ValueError(f"bad direction={row.get('direction')}")
        if row.get("kind") == "support_probe":
            key = (sid, "support", row["direction"], row["probe"], int(row["label_order"]))
        elif row.get("kind") == "readout":
            key = (sid, "readout", row["direction"], row["condition"], int(row["template_id"]), int(row["label_order"]))
        else:
            raise ValueError(f"unknown kind={row.get('kind')}")
        if key in seen:
            raise ValueError(f"duplicate result variant={key}")
        seen.add(key)
        grouped[sid].append(row)

    if set(by_id) != set(grouped):
        raise ValueError(f"scenario coverage mismatch missing={sorted(set(by_id) - set(grouped))}")

    expected_support = {(direction, probe, order) for direction in DIRECTIONS for probe in SUPPORT_PROBES for order in (0, 1)}
    expected_readout = {
        (direction, condition, template_id, order)
        for direction in DIRECTIONS
        for condition in CONDITIONS
        for template_id in range(len(READOUT_TEMPLATES))
        for order in (0, 1)
    }

    directions: list[dict[str, Any]] = []
    pairs: list[dict[str, Any]] = []
    for sid in sorted(by_id):
        scenario = by_id[sid]
        rs = grouped[sid]
        support_rows = [r for r in rs if r["kind"] == "support_probe"]
        readout_rows = [r for r in rs if r["kind"] == "readout"]
        if {(r["direction"], r["probe"], int(r["label_order"])) for r in support_rows} != expected_support:
            raise ValueError(f"{sid}: malformed support coverage")
        if {(r["direction"], r["condition"], int(r["template_id"]), int(r["label_order"])) for r in readout_rows} != expected_readout:
            raise ValueError(f"{sid}: malformed readout coverage")

        direction_rows = []
        for direction in DIRECTIONS:
            sr = [r for r in support_rows if r["direction"] == direction]
            support = {
                probe: mean(float(r["p_correct"]) for r in sr if r["probe"] == probe)
                for probe in SUPPORT_PROBES
            }
            support_min_variant = min(float(r["p_correct"]) for r in sr)
            readouts: dict[str, dict[str, float]] = {}
            variants = {
                "belief": {"weak": [], "weak_complete": [], "weak_length": []},
                "action": {"weak": [], "weak_complete": [], "weak_length": []},
            }
            strong_variants = {"belief": [], "action": []}
            for kind in ("belief", "action"):
                kr = [r for r in readout_rows if r["direction"] == direction and r["template_kind"] == kind]
                readouts[kind] = {
                    condition: mean(float(r["p_target"]) for r in kr if r["condition"] == condition)
                    for condition in CONDITIONS
                }
                baseline_for = {
                    "weak": "no_evidence",
                    "weak_complete": "no_evidence_complete",
                    "weak_length": "no_evidence_length",
                    "strong": "no_evidence",
                }
                for condition in ("weak", "weak_complete", "weak_length", "strong"):
                    updates = []
                    for cond_row in (r for r in kr if r["condition"] == condition):
                        base_row = next(
                            r for r in kr
                            if r["condition"] == baseline_for[condition]
                            and int(r["template_id"]) == int(cond_row["template_id"])
                            and int(r["label_order"]) == int(cond_row["label_order"])
                        )
                        directional = signed_update(direction, float(cond_row["p_target"]), float(base_row["p_target"]))
                        updates.append(directional)
                    if condition == "strong":
                        strong_variants[kind] = updates
                    else:
                        variants[kind][condition] = [-value for value in updates]

            features = compute_direction_features(
                direction=direction,
                support=support,
                support_min_variant=support_min_variant,
                readouts=readouts,
                variants=variants,
                strong_variants=strong_variants,
                cfg=cfg,
            )
            entry = {
                "scenario_id": sid,
                "domain": scenario.domain,
                "direction": direction,
                "support": support,
                "readouts": readouts,
                **features,
            }
            directions.append(entry)
            direction_rows.append(entry)

        by_direction = {entry["direction"]: entry for entry in direction_rows}
        pair_gate = all(entry["capability_gate"] for entry in direction_rows)
        pair_strong = all(entry["strong"] for entry in direction_rows)
        pair_pragmatic = all(entry["pragmatic_robust"] for entry in direction_rows)
        pair_length = all(entry["length_robust"] for entry in direction_rows)
        pair_neutral = all(entry["neutral_ok"] for entry in direction_rows)
        pair_bidirectional = all(entry["belief_backfire"] > 0 and entry["action_backfire"] > 0 for entry in direction_rows)
        pairs.append({
            "scenario_id": sid,
            "domain": scenario.domain,
            "gated": pair_gate,
            "strong": pair_strong,
            "pragmatic_robust": pair_pragmatic,
            "length_robust": pair_length,
            "neutral_ok": pair_neutral,
            "bidirectional_backfire": pair_bidirectional,
            "belief_backfire_mean": mean(entry["belief_backfire"] for entry in direction_rows),
            "action_backfire_mean": mean(entry["action_backfire"] for entry in direction_rows),
            "complete_belief_backfire_mean": mean(entry["complete_belief_backfire"] for entry in direction_rows),
            "complete_action_backfire_mean": mean(entry["complete_action_backfire"] for entry in direction_rows),
            "length_belief_backfire_mean": mean(entry["length_belief_backfire"] for entry in direction_rows),
            "length_action_backfire_mean": mean(entry["length_action_backfire"] for entry in direction_rows),
            "direction_asymmetry_belief": abs(by_direction["supports_target"]["belief_backfire"] - by_direction["supports_other"]["belief_backfire"]),
        })

    gated_directions = [entry for entry in directions if entry["capability_gate"]]
    gated_pairs = [pair for pair in pairs if pair["gated"]]
    belief_pair_values = [pair["belief_backfire_mean"] for pair in gated_pairs]
    action_pair_values = [pair["action_backfire_mean"] for pair in gated_pairs]
    belief_ci = bootstrap_ci(belief_pair_values, seed=cfg["seed"], n_boot=cfg["bootstrap_samples"])
    action_ci = bootstrap_ci(action_pair_values, seed=cfg["seed"] + 1, n_boot=cfg["bootstrap_samples"])

    by_domain: dict[str, dict[str, Any]] = {}
    for domain in sorted({pair["domain"] for pair in pairs}):
        sub = [pair for pair in gated_pairs if pair["domain"] == domain]
        by_domain[domain] = {
            "gated_pairs": len(sub),
            "mean_belief_backfire": mean(pair["belief_backfire_mean"] for pair in sub) if sub else math.nan,
            "mean_action_backfire": mean(pair["action_backfire_mean"] for pair in sub) if sub else math.nan,
            "strong_pairs": sum(pair["strong"] for pair in sub),
        }

    pc = cfg["model_pass"]
    support_gate_fraction = mean(float(entry["support_gate"]) for entry in directions) if directions else 0.0
    pragmatic_pair_fraction = mean(float(pair["pragmatic_robust"]) for pair in gated_pairs) if gated_pairs else 0.0
    length_pair_fraction = mean(float(pair["length_robust"]) for pair in gated_pairs) if gated_pairs else 0.0
    neutral_artifact_fraction = mean(float(not pair["neutral_ok"]) for pair in gated_pairs) if gated_pairs else 0.0
    bidirectional_fraction = mean(float(pair["bidirectional_backfire"]) for pair in gated_pairs) if gated_pairs else 0.0
    aggregate = {
        "gated_directions": len(gated_directions),
        "gated_scenario_pairs": len(gated_pairs),
        "mean_pair_belief_backfire": mean(belief_pair_values) if belief_pair_values else math.nan,
        "pair_belief_bootstrap_95_ci": list(belief_ci),
        "mean_pair_action_backfire": mean(action_pair_values) if action_pair_values else math.nan,
        "pair_action_bootstrap_95_ci": list(action_ci),
        "strong_pair_fraction": mean(float(pair["strong"]) for pair in gated_pairs) if gated_pairs else 0.0,
        "support_gate_fraction": support_gate_fraction,
        "pragmatic_pair_survival_fraction": pragmatic_pair_fraction,
        "length_pair_survival_fraction": length_pair_fraction,
        "bidirectional_backfire_fraction": bidirectional_fraction,
        "neutral_artifact_fraction": neutral_artifact_fraction,
        "mean_direction_asymmetry_belief": mean(pair["direction_asymmetry_belief"] for pair in gated_pairs) if gated_pairs else math.nan,
        "positive_domains": sum(
            info["gated_pairs"] >= 2 and info["mean_belief_backfire"] > 0 and info["mean_action_backfire"] > 0
            for info in by_domain.values()
        ),
    }

    enough = len(gated_pairs) >= pc["min_gated_pairs"]
    model_pass = (
        enough
        and aggregate["mean_pair_belief_backfire"] >= pc["min_mean_pair_belief_backfire"]
        and belief_ci[0] >= pc["min_pair_bootstrap_ci_lower"]
        and aggregate["mean_pair_action_backfire"] >= pc["min_mean_pair_action_backfire"]
        and action_ci[0] >= pc["min_pair_bootstrap_ci_lower"]
        and aggregate["strong_pair_fraction"] >= pc["min_strong_pair_fraction"]
        and pragmatic_pair_fraction >= pc["min_pragmatic_pair_survival_fraction"]
        and length_pair_fraction >= pc["min_length_pair_survival_fraction"]
        and bidirectional_fraction >= pc["min_bidirectional_backfire_fraction"]
        and neutral_artifact_fraction <= pc["max_neutral_artifact_fraction"]
        and aggregate["positive_domains"] >= pc["min_positive_domains"]
    )

    if len(pairs) >= pc["min_gated_pairs"] and support_gate_fraction < pc["min_support_gate_fraction"]:
        verdict = "HARD-KILL-EVIDENCE-DIRECTION-CAPABILITY-FLOOR"
    elif enough and aggregate["mean_pair_belief_backfire"] <= pc["no_effect_backfire"] and belief_ci[1] <= pc["no_effect_ci_upper"]:
        verdict = "HARD-KILL-NO-BACKFIRE"
    elif enough and aggregate["mean_pair_belief_backfire"] > 0 and pragmatic_pair_fraction < pc["min_pragmatic_pair_survival_fraction"]:
        verdict = "HARD-KILL-PRAGMATIC-ABSENCE-IMPLICATURE"
    elif enough and aggregate["mean_pair_belief_backfire"] > 0 and aggregate["mean_pair_action_backfire"] <= 0:
        verdict = "HOLD-READOUT-ONLY"
    elif enough and aggregate["mean_pair_belief_backfire"] > 0 and bidirectional_fraction < pc["min_bidirectional_backfire_fraction"]:
        verdict = "HOLD-DIRECTION-ASYMMETRY"
    elif neutral_artifact_fraction > pc["max_neutral_artifact_fraction"]:
        verdict = "HOLD-GENERIC-MENTION-ARTIFACT"
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
        "by_domain": by_domain,
        "directions": directions,
        "scenario_pairs": pairs,
        "hard_kill_note": (
            "The primary statistical unit is the scenario, not the two evidence directions. "
            "A pair counts only when both directions understand support, strong evidence moves in the correct direction, "
            "weak evidence reverses both belief and action, the reversal survives completeness and matched-length protocols, "
            "and neutral evidence does not move similarly."
        ),
    }
    if out_path:
        p = Path(out_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=True), encoding="utf-8")
    return summary
