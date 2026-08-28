from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import mean
import json

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
SOURCES = ROOT / "data" / "frozen_d0_sources.jsonl"
MODELS = (
    ("Qwen3-8B", RESULTS / "qwen3_8b.smoke.summary.json"),
    ("Gemma3-12B", RESULTS / "gemma3_12b.smoke.summary.json"),
)
OUT = RESULTS / "raw_case_audit_smoke.md"


def _fmt(x):
    if isinstance(x, float):
        return f"{x:.4f}"
    return str(x)


def _source_map():
    rows = [json.loads(line) for line in SOURCES.read_text(encoding="utf-8").splitlines() if line.strip()]
    out = {}
    for row in rows:
        sid = f"football:{row['country_key']}:{row['season'].replace('–', '-')}"
        out[sid] = row
    return out


def _domain_table(summary):
    lines = ["| domain | gated | mean unknown margin | strong |", "|---|---:|---:|---:|"]
    for domain, info in sorted(summary["by_domain"].items()):
        lines.append(
            f"| {domain} | {info['gated']} | {_fmt(info['mean_unknown_margin'])} | {info['strong']} |"
        )
    return lines


def main():
    src = _source_map()
    lines = [
        "# 006 Frozen Smoke Raw-Case Audit",
        "",
        "Generated deterministically from the two frozen model summaries. No thresholds are changed here.",
        "",
    ]
    for model_name, path in MODELS:
        summary = json.loads(path.read_text(encoding="utf-8"))
        agg = summary["aggregate"]
        cases = summary["cases"]
        recognition_fail = [c for c in cases if not c["recognition_gate"]]
        control_fail = [c for c in cases if c["recognition_gate"] and not c["downstream_control_gate"]]
        gated = [c for c in cases if c["capability_gate"]]
        positive = [c for c in gated if c["unknown_margin"] > 0]
        strong = [c for c in gated if c["strong"]]

        lines += [
            f"## {model_name}",
            "",
            f"- verdict: `{summary['verdict']}`",
            f"- model_pass: `{summary['model_pass']}`",
            f"- total cases: {agg['total_cases']}",
            f"- recognition-gated: {agg['recognition_gated_cases']}",
            f"- capability-gated: {agg['gated_cases']}",
            f"- recognition failures: {len(recognition_fail)}",
            f"- explicit-control failures after recognition: {len(control_fail)}",
            f"- positive unknown-margin gated cases: {len(positive)} / {len(gated)}",
            f"- strong cases: {len(strong)} / {len(gated)}",
            f"- mean unknown collapse probability: {_fmt(agg['mean_unknown_collapse_probability'])}",
            f"- mean unknown margin: {_fmt(agg['mean_unknown_margin'])}",
            f"- bootstrap 95% CI: [{_fmt(agg['bootstrap_95_ci'][0])}, {_fmt(agg['bootstrap_95_ci'][1])}]",
            f"- mean paraphrase margin: {_fmt(agg['mean_paraphrase_margin'])}",
            f"- mean unknown-minus-distinct: {_fmt(agg['mean_unknown_minus_distinct'])}",
            f"- neutral artifact fraction: {_fmt(agg['neutral_artifact_fraction'])}",
            f"- natural variant positive fraction: {_fmt(agg['mean_natural_variant_positive_fraction'])}",
            "",
            "### By country/domain",
            "",
            *_domain_table(summary),
            "",
            "### Case audit",
            "",
            "| scenario | source club (audit only) | rec | ctrl | unknown | paraphrase | same | distinct | neutral | unknown margin | neutral shift | strong |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for c in cases:
            p = c["p_collapse_action"]
            source_club = src.get(c["scenario_id"], {}).get("club", "?")
            lines.append(
                "| {sid} | {club} | {rec} | {ctrl} | {u} | {para} | {same} | {dist} | {neutral} | {margin} | {nshift} | {strong} |".format(
                    sid=c["scenario_id"],
                    club=source_club,
                    rec=int(c["recognition_gate"]),
                    ctrl=int(c["downstream_control_gate"]),
                    u=_fmt(p["unknown"]),
                    para=_fmt(p["paraphrase"]),
                    same=_fmt(p["same_explicit"]),
                    dist=_fmt(p["distinct_explicit"]),
                    neutral=_fmt(p["neutral_control"]),
                    margin=_fmt(c["unknown_margin"]),
                    nshift=_fmt(c["neutral_abs_shift"]),
                    strong=int(c["strong"]),
                )
            )

        eligible_domains = [
            info for info in summary["by_domain"].values() if info["gated"] >= 2
        ]
        positive_domains = [info for info in eligible_domains if info["mean_unknown_margin"] > 0]
        lines += [
            "",
            "### Frozen source-memory diagnostic",
            "",
            f"Eligible domains (>=2 gated): {len(eligible_domains)}; positive domains: {len(positive_domains)}.",
            "This is diagnostic only. Inspect whether apparent collapse is concentrated in a small set of historically recognizable country/season slices. Do not remove or reweight slices after seeing results.",
            "",
        ]

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
