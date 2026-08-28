from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean


POLARITIES = ("supports_target", "supports_other")
PROBE_THRESHOLDS = {"inadmissible": 0.80, "scope": 0.75, "polarity": 0.75}
MIN_ADMITTED_SHIFT = 0.08


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def decompose(summary_path: Path, raw_path: Path) -> dict:
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    rows = read_jsonl(raw_path)
    cases = summary["cases"]
    raw_by_sid: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        raw_by_sid[str(row["scenario_id"])].append(row)

    by_polarity = {}
    for polarity in POLARITIES:
        selected = [case for case in cases if case["polarity"] == polarity]
        probes = {}
        for probe, threshold in PROBE_THRESHOLDS.items():
            mean_pass = sum(case["recognition"][probe] >= threshold for case in selected)
            order_pass = 0
            order_gap = []
            for case in selected:
                probe_rows = [
                    row for row in raw_by_sid[case["scenario_id"]]
                    if row["kind"] == "recognition" and row["probe"] == probe
                ]
                values = [float(row["p_correct"]) for row in sorted(probe_rows, key=lambda row: row["label_order"])]
                order_pass += int(len(values) == 2 and min(values) >= threshold)
                if len(values) == 2:
                    order_gap.append(abs(values[0] - values[1]))
            probes[probe] = {
                "mean_probability_pass": mean_pass,
                "both_answer_orders_pass": order_pass,
                "total": len(selected),
                "mean_probability": mean(case["recognition"][probe] for case in selected),
                "mean_answer_order_gap": mean(order_gap),
            }
        admitted = [case["admitted_directional_shift"] for case in selected]
        by_polarity[polarity] = {
            "probes": probes,
            "admitted_directional_pass": sum(value >= MIN_ADMITTED_SHIFT for value in admitted),
            "mean_admitted_directional_shift": mean(admitted),
            "total": len(selected),
        }

    case_by_pair: dict[str, dict[str, dict]] = defaultdict(dict)
    for case in cases:
        case_by_pair[case["polarity_pair_id"]][case["polarity"]] = case

    pair_rows = []
    for pair_id, members in sorted(case_by_pair.items()):
        target = members["supports_target"]
        other = members["supports_other"]
        legal_gate = all(
            case["recognition"]["inadmissible"] >= PROBE_THRESHOLDS["inadmissible"]
            and case["recognition"]["scope"] >= PROBE_THRESHOLDS["scope"]
            for case in (target, other)
        )
        explicit_polarity_gate = all(
            case["recognition"]["polarity"] >= PROBE_THRESHOLDS["polarity"]
            for case in (target, other)
        )
        admitted_delta = target["p_target_admitted"] - other["p_target_admitted"]
        both_case_admitted = all(
            case["admitted_directional_shift"] >= MIN_ADMITTED_SHIFT
            for case in (target, other)
        )

        variant_deltas = []
        target_verdict_rows = [
            row for row in raw_by_sid[target["scenario_id"]]
            if row["kind"] == "verdict" and row["template_kind"] == "natural" and row["condition"] == "admitted"
        ]
        other_verdict_rows = [
            row for row in raw_by_sid[other["scenario_id"]]
            if row["kind"] == "verdict" and row["template_kind"] == "natural" and row["condition"] == "admitted"
        ]
        other_by_variant = {
            (int(row["template_id"]), int(row["label_order"])): float(row["p_target"])
            for row in other_verdict_rows
        }
        for row in target_verdict_rows:
            key = (int(row["template_id"]), int(row["label_order"]))
            if key in other_by_variant:
                variant_deltas.append(float(row["p_target"]) - other_by_variant[key])

        pair_capability_candidate = legal_gate and admitted_delta >= MIN_ADMITTED_SHIFT
        pair_rows.append({
            "polarity_pair_id": pair_id,
            "legal_recognition_gate": legal_gate,
            "explicit_polarity_gate": explicit_polarity_gate,
            "both_case_admitted_directional_gate": both_case_admitted,
            "admitted_polarity_delta": admitted_delta,
            "admitted_variant_positive_fraction": mean(float(value > 0) for value in variant_deltas),
            "admitted_variant_min_delta": min(variant_deltas),
            "pair_capability_candidate": pair_capability_candidate,
            "polarity_probe_induced_failure": pair_capability_candidate and not explicit_polarity_gate,
        })

    candidate_pairs = [row for row in pair_rows if row["pair_capability_candidate"]]
    probe_killed = [row for row in candidate_pairs if row["polarity_probe_induced_failure"]]
    complete_current = [
        row for row in pair_rows
        if row["legal_recognition_gate"] and row["explicit_polarity_gate"]
        and row["both_case_admitted_directional_gate"]
    ]
    return {
        "model": summary["model"],
        "source_summary": str(summary_path),
        "source_raw": str(raw_path),
        "thresholds": {
            "inadmissible": PROBE_THRESHOLDS["inadmissible"],
            "scope": PROBE_THRESHOLDS["scope"],
            "polarity": PROBE_THRESHOLDS["polarity"],
            "admitted_directional_or_pair_delta": MIN_ADMITTED_SHIFT,
        },
        "by_polarity": by_polarity,
        "pair_decomposition": {
            "total_pairs": len(pair_rows),
            "legal_recognition_pairs": sum(row["legal_recognition_gate"] for row in pair_rows),
            "pair_admitted_operator_candidates": len(candidate_pairs),
            "polarity_probe_induced_failures": len(probe_killed),
            "current_fully_gated_pairs": len(complete_current),
            "probe_induced_failure_pair_ids": [row["polarity_pair_id"] for row in probe_killed],
        },
        "pairs": pair_rows,
        "interpretation": (
            "POLARITY-PROBE-INDUCED-FALSE-FAILURE is a harness diagnosis, not a claim that every excluded "
            "pair is scientifically valid. It flags pairs that pass rule/scope recognition and show the paired "
            "admitted content-swap operator, but are rejected only by the asymmetric Yes/No polarity probe."
        ),
    }


def render_markdown(reports: list[dict]) -> str:
    lines = [
        "# D0 v2 gate-failure forensic decomposition",
        "",
        "Status: `EXPLORATORY-LOCAL / INVALIDATED-HARNESS-DIAGNOSTIC`",
        "",
        "The v2 polarity probe maps pro-TARGET to semantic Yes and pro-OTHER to semantic No. "
        "The counts below separate that probe from the paired admitted operator.",
        "",
        "| Model | Polarity | Inadmissible mean-gate | Scope mean-gate | Polarity mean-gate | Polarity both-orders | Admitted directional |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for report in reports:
        for polarity in POLARITIES:
            row = report["by_polarity"][polarity]
            probes = row["probes"]
            total = row["total"]
            lines.append(
                f"| {report['model']} | {polarity} | {probes['inadmissible']['mean_probability_pass']}/{total} | "
                f"{probes['scope']['mean_probability_pass']}/{total} | {probes['polarity']['mean_probability_pass']}/{total} | "
                f"{probes['polarity']['both_answer_orders_pass']}/{total} | {row['admitted_directional_pass']}/{total} |"
            )
    lines += ["", "## Pair-level diagnosis", ""]
    for report in reports:
        pair = report["pair_decomposition"]
        lines += [
            f"- **{report['model']}**: {pair['pair_admitted_operator_candidates']}/{pair['total_pairs']} pairs pass "
            f"rule/scope plus admitted pair delta; {pair['polarity_probe_induced_failures']} of those are killed only "
            f"by the explicit polarity probe. Current fully gated pairs: {pair['current_fully_gated_pairs']}.",
            f"  - Probe-induced pair IDs: {', '.join(pair['probe_induced_failure_pair_ids']) or 'none'}",
        ]
    lines += [
        "",
        "## Verdict",
        "",
        "`POLARITY-PROBE-INDUCED-FALSE-FAILURE` is confirmed as a harness failure mode. This does not rescue D0 v2: "
        "the dangling never-seen baseline, generic neutral salience, and exclusion-reason confound remain independent blockers.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", action="append", nargs=2, metavar=("SUMMARY", "RAW"), required=True)
    parser.add_argument("--json-out", required=True)
    parser.add_argument("--md-out", required=True)
    args = parser.parse_args()
    reports = [decompose(Path(summary), Path(raw)) for summary, raw in args.model]
    Path(args.json_out).write_text(json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.md_out).write_text(render_markdown(reports), encoding="utf-8")


if __name__ == "__main__":
    main()
