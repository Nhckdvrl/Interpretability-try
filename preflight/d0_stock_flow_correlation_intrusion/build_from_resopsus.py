#!/usr/bin/env python3
"""Build a data-first D0 bank for Stock-Flow Correlation Intrusion from ResOpsUS.

The script expects the official ResOpsUS archive to be downloaded/extracted
outside the repository. It does not invent tank stories. It scans natural daily
reservoir records and identifies windows where:

1) observed storage change has a clear sign;
2) cumulative inflow-outflow has the same sign as the observed storage change;
3) the *trend in inflow level* points in the opposite direction.

These are useful D0 windows because a model can correctly reason about net flow
while still being tempted to track the salient inflow series when predicting the
stock trajectory.

No model calls are made here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterator

import pandas as pd

SECONDS_PER_DAY = 86400.0
M3_PER_MCM = 1_000_000.0

ALIASES = {
    "date": ["date", "datetime", "time"],
    "storage": ["storage", "stor", "reservoir_storage"],
    "inflow": ["inflow", "in_flow", "inflow_cms", "inflow_cfs"],
    "outflow": ["outflow", "out_flow", "release", "discharge", "outflow_cms", "outflow_cfs"],
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True, help="Extracted ResOpsUS directory")
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--window-days", type=int, default=7)
    p.add_argument("--min-valid-days", type=int, default=5)
    p.add_argument("--closure-ratio-max", type=float, default=0.35)
    p.add_argument("--audit-n", type=int, default=40)
    return p.parse_args()


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(s).strip().lower()).strip("_")


def find_col(columns: list[str], kind: str) -> str | None:
    normalized = {norm(c): c for c in columns}
    for alias in ALIASES[kind]:
        if alias in normalized:
            return normalized[alias]
    # Conservative fuzzy fallback; ambiguous matches are rejected.
    hits = []
    for nc, original in normalized.items():
        if any(alias in nc for alias in ALIASES[kind]):
            hits.append(original)
    return hits[0] if len(hits) == 1 else None


def slope(values: pd.Series) -> float:
    y = values.astype(float).to_list()
    n = len(y)
    if n < 2:
        return float("nan")
    xbar = (n - 1) / 2.0
    ybar = sum(y) / n
    num = sum((i - xbar) * (v - ybar) for i, v in enumerate(y))
    den = sum((i - xbar) ** 2 for i in range(n))
    return num / den if den else 0.0


def sign(x: float, eps: float = 1e-12) -> int:
    if x > eps:
        return 1
    if x < -eps:
        return -1
    return 0


def stable_hash(parts: list[str]) -> str:
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def iter_csvs(root: Path) -> Iterator[Path]:
    # ResOpsUS releases use several layouts. We accept any CSV but only retain
    # files with an unambiguous date/storage/inflow/outflow schema.
    for path in sorted(root.rglob("*.csv")):
        if path.is_file():
            yield path


def read_candidate_file(path: Path) -> tuple[pd.DataFrame, dict[str, str]] | None:
    try:
        df = pd.read_csv(path, low_memory=False)
    except Exception:
        return None
    cols = list(map(str, df.columns))
    mapping = {kind: find_col(cols, kind) for kind in ("date", "storage", "inflow", "outflow")}
    if any(v is None for v in mapping.values()):
        return None

    use = pd.DataFrame(
        {
            "date": pd.to_datetime(df[mapping["date"]], errors="coerce"),
            "storage": pd.to_numeric(df[mapping["storage"]], errors="coerce"),
            "inflow": pd.to_numeric(df[mapping["inflow"]], errors="coerce"),
            "outflow": pd.to_numeric(df[mapping["outflow"]], errors="coerce"),
        }
    ).dropna()
    use = use.sort_values("date").drop_duplicates("date")
    if len(use) < 10:
        return None
    return use, {k: str(v) for k, v in mapping.items()}


def infer_flow_factor(df: pd.DataFrame) -> tuple[float, str]:
    """Infer whether flow columns are likely m3/s or cfs by closure scale.

    Official ResOpsUS documentation describes inflow/outflow as flow rates and
    storage as MCM. Releases/agency tables can vary, so we compare two plausible
    conversions against observed day-to-day storage changes and choose the one
    with lower median relative error. The chosen unit is recorded, never hidden.
    """
    sample = df.copy()
    sample["d_storage"] = sample["storage"].diff()
    sample["net_raw"] = sample["inflow"] - sample["outflow"]
    sample = sample.dropna().head(500)
    if len(sample) < 5:
        return SECONDS_PER_DAY / M3_PER_MCM, "m3/s_assumed"

    candidates = {
        "m3/s": SECONDS_PER_DAY / M3_PER_MCM,
        "cfs": 0.028316846592 * SECONDS_PER_DAY / M3_PER_MCM,
    }
    scores: dict[str, float] = {}
    for unit, factor in candidates.items():
        implied = sample["net_raw"] * factor
        denom = sample["d_storage"].abs() + implied.abs() + 1e-6
        scores[unit] = float(((sample["d_storage"] - implied).abs() / denom).median())
    unit = min(scores, key=scores.get)
    return candidates[unit], unit


def extract_windows(
    df: pd.DataFrame,
    source_file: Path,
    mapping: dict[str, str],
    window_days: int,
    min_valid_days: int,
    closure_ratio_max: float,
) -> list[dict[str, Any]]:
    factor, inferred_unit = infer_flow_factor(df)
    rows: list[dict[str, Any]] = []
    n = len(df)
    for start in range(0, n - window_days + 1):
        w = df.iloc[start : start + window_days].dropna()
        if len(w) < min_valid_days:
            continue
        if w["date"].iloc[-1] - w["date"].iloc[0] > pd.Timedelta(days=window_days + 2):
            continue

        observed_delta = float(w["storage"].iloc[-1] - w["storage"].iloc[0])
        implied_net = float(((w["inflow"] - w["outflow"]) * factor).sum())
        inflow_slope = float(slope(w["inflow"]))

        s_storage = sign(observed_delta)
        s_net = sign(implied_net)
        s_inflow_trend = sign(inflow_slope)
        if 0 in (s_storage, s_net, s_inflow_trend):
            continue
        if s_storage != s_net:
            continue
        if s_inflow_trend == s_storage:
            continue

        denom = max(abs(observed_delta), abs(implied_net), 1e-6)
        closure_ratio = abs(observed_delta - implied_net) / denom
        if closure_ratio > closure_ratio_max:
            continue

        source_id = source_file.stem
        start_date = str(w["date"].iloc[0].date())
        end_date = str(w["date"].iloc[-1].date())
        key = stable_hash([source_id, start_date, end_date])
        rows.append(
            {
                "stable_key": key,
                "source_file": str(source_file),
                "source_id": source_id,
                "start_date": start_date,
                "end_date": end_date,
                "n_days": int(len(w)),
                "storage_start": float(w["storage"].iloc[0]),
                "storage_end": float(w["storage"].iloc[-1]),
                "observed_storage_delta": observed_delta,
                "cumulative_inflow_minus_outflow_mcm": implied_net,
                "inflow_start": float(w["inflow"].iloc[0]),
                "inflow_end": float(w["inflow"].iloc[-1]),
                "inflow_slope": inflow_slope,
                "storage_direction": "up" if s_storage > 0 else "down",
                "net_flow_direction": "positive" if s_net > 0 else "negative",
                "inflow_trend_direction": "up" if s_inflow_trend > 0 else "down",
                "closure_ratio": closure_ratio,
                "inferred_flow_unit": inferred_unit,
                "column_mapping": mapping,
                "daily": [
                    {
                        "date": str(r.date.date()),
                        "storage": float(r.storage),
                        "inflow": float(r.inflow),
                        "outflow": float(r.outflow),
                    }
                    for r in w.itertuples(index=False)
                ],
            }
        )
    return rows


def main() -> None:
    args = parse_args()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict[str, Any]] = []
    inspected_files = 0
    usable_files = 0
    schema_fail = 0
    for csv_path in iter_csvs(args.root):
        inspected_files += 1
        loaded = read_candidate_file(csv_path)
        if loaded is None:
            schema_fail += 1
            continue
        usable_files += 1
        df, mapping = loaded
        all_rows.extend(
            extract_windows(
                df,
                csv_path,
                mapping,
                args.window_days,
                args.min_valid_days,
                args.closure_ratio_max,
            )
        )

    all_rows.sort(key=lambda r: r["stable_key"])
    with (out / "eligible_windows.jsonl").open("w", encoding="utf-8") as f:
        for row in all_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # Audit sample balances the two directions when possible.
    by_dir = {"up": [], "down": []}
    for row in all_rows:
        by_dir[row["storage_direction"]].append(row)
    selected: list[dict[str, Any]] = []
    target_each = max(1, args.audit_n // 2)
    selected.extend(by_dir["up"][:target_each])
    selected.extend(by_dir["down"][:target_each])
    seen = {r["stable_key"] for r in selected}
    for row in all_rows:
        if len(selected) >= args.audit_n:
            break
        if row["stable_key"] not in seen:
            selected.append(row)
            seen.add(row["stable_key"])

    with (out / "audit_sample.jsonl").open("w", encoding="utf-8") as f:
        for row in selected:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    source_counts = Counter(r["source_id"] for r in all_rows)
    direction_counts = Counter(r["storage_direction"] for r in all_rows)
    unit_counts = Counter(r["inferred_flow_unit"] for r in all_rows)
    summary = {
        "source": "ResOpsUS",
        "root": str(args.root),
        "csv_files_inspected": inspected_files,
        "csv_files_with_usable_schema": usable_files,
        "csv_files_rejected_or_non_timeseries": schema_fail,
        "eligible_natural_windows": len(all_rows),
        "unique_source_ids": len(source_counts),
        "storage_direction_counts": dict(direction_counts),
        "inferred_flow_unit_counts": dict(unit_counts),
        "window_days": args.window_days,
        "closure_ratio_max": args.closure_ratio_max,
        "audit_sample_n": len(selected),
        "scope_note": (
            "All qualifying natural windows from every usable reservoir file are retained. "
            "Reservoir identity, direction, inferred unit, and closure error stay as factors."
        ),
        "d0_status": "SOURCE-WINDOW-BANK-MATERIALIZED; HUMAN SOURCE AUDIT STILL REQUIRED",
    }
    (out / "scope_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    md = [
        "# ResOpsUS D0 source audit sample",
        "",
        "Generated before model calls. Verify source semantics and unit/closure assumptions.",
        "",
    ]
    for i, row in enumerate(selected, 1):
        md.extend(
            [
                f"## {i}. {row['source_id']} — {row['start_date']} to {row['end_date']}",
                f"- storage: {row['storage_direction']} (Δ={row['observed_storage_delta']:.4g})",
                f"- net inflow-outflow: {row['net_flow_direction']} ({row['cumulative_inflow_minus_outflow_mcm']:.4g} MCM implied)",
                f"- inflow trend: {row['inflow_trend_direction']} (slope={row['inflow_slope']:.4g})",
                f"- closure ratio: {row['closure_ratio']:.3f}; inferred flow unit: {row['inferred_flow_unit']}",
                "- audit: [ ] columns map correctly; [ ] no agency-specific unit mismatch; [ ] storage/net direction genuinely conflicts with inflow trend; [ ] no major missing-date artifact",
                "",
            ]
        )
    (out / "AUDIT_SAMPLE.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
