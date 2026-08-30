"""Build a balanced 2x2 natural-window bank from official ResOpsUS v2."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

from .io import sha256, write_jsonl


FLOW_TO_MCM_DAY = 86_400 / 1_000_000
WINDOW_ROWS = 7
FLOW_DAYS = 6


def stable_hash(*parts: object) -> str:
    return hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()


def direction(value: float) -> str:
    return "up" if value > 0 else "down"


def load_attributes(path: Path) -> dict[str, dict]:
    frame = pd.read_csv(path, encoding="utf-8-sig")
    return {
        str(int(row.DAM_ID)): {
            "dam_name": str(row.DAM_NAME),
            "state": str(row.STATE),
            "agency_code": str(row.AGENCY_CODE),
            "inconsistencies_noted": None if pd.isna(row.INCONSISTENCIES_NOTED) else str(row.INCONSISTENCIES_NOTED),
        }
        for row in frame.itertuples(index=False)
    }


def extract_file(path: Path, attributes: dict[str, dict], closure_max: float,
                 min_flow_margin: float, min_inflow_correlation: float,
                 min_inflow_range_ratio: float) -> list[dict]:
    dam_id = path.stem.rsplit("_", 1)[-1]
    meta = attributes.get(dam_id, {})
    # The release explicitly flags a small set of reservoirs with known point errors.
    if meta.get("inconsistencies_noted"):
        return []
    raw = pd.read_csv(path, na_values="NA")
    required = {"date", "storage", "inflow", "outflow"}
    if not required.issubset(raw.columns):
        return []
    frame = pd.DataFrame({
        "date": pd.to_datetime(raw["date"], errors="coerce"),
        "storage": pd.to_numeric(raw["storage"], errors="coerce"),
        "inflow": pd.to_numeric(raw["inflow"], errors="coerce"),
        "outflow": pd.to_numeric(raw["outflow"], errors="coerce"),
    }).drop_duplicates("date").sort_values("date").reset_index(drop=True)
    if len(frame) < WINDOW_ROWS:
        return []

    dates = frame["date"].to_numpy()
    storage = frame["storage"].to_numpy(float)
    inflow = frame["inflow"].to_numpy(float)
    outflow = frame["outflow"].to_numpy(float)
    x = np.arange(FLOW_DAYS, dtype=float)
    x_centered = x - x.mean()
    x_ss = float(np.square(x_centered).sum())
    rows = []
    for end in range(WINDOW_ROWS - 1, len(frame)):
        start = end - (WINDOW_ROWS - 1)
        if np.isnat(dates[start]) or np.isnat(dates[end]):
            continue
        if (dates[end] - dates[start]) != np.timedelta64(WINDOW_ROWS - 1, "D"):
            continue
        stor = storage[[start, end]]
        incoming = inflow[start + 1:end + 1]
        outgoing = outflow[start + 1:end + 1]
        if not (np.isfinite(stor).all() and np.isfinite(incoming).all() and np.isfinite(outgoing).all()):
            continue
        if (incoming < 0).any() or (outgoing < 0).any():
            continue

        storage_delta = float(stor[1] - stor[0])
        exact_net = float((incoming - outgoing).sum() * FLOW_TO_MCM_DAY)
        rounded_in = np.round(incoming, 2)
        rounded_out = np.round(outgoing, 2)
        prompt_net = float((rounded_in - rounded_out).sum())
        if storage_delta == 0 or exact_net == 0 or prompt_net == 0:
            continue
        if np.sign(storage_delta) != np.sign(exact_net) or np.sign(exact_net) != np.sign(prompt_net):
            continue
        closure = abs(storage_delta - exact_net) / max(abs(storage_delta), abs(exact_net), 1e-9)
        if closure > closure_max:
            continue
        flow_margin = abs(float((incoming - outgoing).sum())) / max(float((incoming + outgoing).sum()), 1e-9)
        if flow_margin < min_flow_margin:
            continue

        y = incoming
        y_centered = y - y.mean()
        y_ss = float(np.square(y_centered).sum())
        if y_ss == 0:
            continue
        inflow_slope = float(np.dot(x_centered, y_centered) / x_ss)
        inflow_correlation = float(np.dot(x_centered, y_centered) / np.sqrt(x_ss * y_ss))
        inflow_range_ratio = float((y.max() - y.min()) / max(abs(y.mean()), 1e-9))
        if abs(inflow_correlation) < min_inflow_correlation or inflow_range_ratio < min_inflow_range_ratio:
            continue
        inflow_dir = direction(inflow_slope)
        storage_dir = direction(storage_delta)
        cell = f"net_{storage_dir}__inflow_{inflow_dir}"
        rows.append({
            "item_id": f"resops-{dam_id}-{pd.Timestamp(dates[start]).date()}-{pd.Timestamp(dates[end]).date()}",
            "stable_key": stable_hash(dam_id, dates[start], dates[end]),
            "dam_id": dam_id,
            **meta,
            "source_file": path.name,
            "start_date": str(pd.Timestamp(dates[start]).date()),
            "end_date": str(pd.Timestamp(dates[end]).date()),
            "initial_storage_mcm": round(float(stor[0]), 4),
            "observed_final_storage_mcm": round(float(stor[1]), 4),
            "observed_storage_delta_mcm": storage_delta,
            "cumulative_net_flow_mcm": exact_net,
            "prompt_net_flow_cumecs_sum": prompt_net,
            "net_direction": "positive" if exact_net > 0 else "negative",
            "storage_direction": storage_dir,
            "inflow_trend_direction": inflow_dir,
            "congruence": "aligned" if storage_dir == inflow_dir else "conflict",
            "cell": cell,
            "closure_ratio": closure,
            "flow_margin": flow_margin,
            "inflow_slope": inflow_slope,
            "inflow_time_correlation": inflow_correlation,
            "inflow_range_ratio": inflow_range_ratio,
            "daily_flows": [
                {"date": str(pd.Timestamp(dates[index]).date()),
                 "inflow_cumecs": float(round(inflow[index], 2)),
                 "outflow_cumecs": float(round(outflow[index], 2))}
                for index in range(start + 1, end + 1)
            ],
        })
    return rows


def balanced_select(eligible: list[dict], per_cell: int, separation_days: int,
                    max_per_dam_cell: int) -> list[dict]:
    selected: list[dict] = []
    dates_by_dam: dict[str, list[pd.Timestamp]] = defaultdict(list)
    counts: Counter = Counter()
    cells = ["net_up__inflow_up", "net_up__inflow_down",
             "net_down__inflow_up", "net_down__inflow_down"]
    for cell in cells:
        candidates = sorted((row for row in eligible if row["cell"] == cell),
                            key=lambda row: row["stable_key"])
        for row in candidates:
            if sum(item["cell"] == cell for item in selected) >= per_cell:
                break
            key = (row["dam_id"], cell)
            if counts[key] >= max_per_dam_cell:
                continue
            start = pd.Timestamp(row["start_date"])
            if any(abs((start - other).days) < separation_days for other in dates_by_dam[row["dam_id"]]):
                continue
            selected.append(row)
            counts[key] += 1
            dates_by_dam[row["dam_id"]].append(start)
    return sorted(selected, key=lambda row: row["stable_key"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--closure-max", type=float, default=0.10)
    ap.add_argument("--min-flow-margin", type=float, default=0.05)
    ap.add_argument("--min-inflow-correlation", type=float, default=0.60)
    ap.add_argument("--min-inflow-range-ratio", type=float, default=0.15)
    ap.add_argument("--per-cell", type=int, default=150)
    ap.add_argument("--separation-days", type=int, default=30)
    ap.add_argument("--max-per-dam-cell", type=int, default=2)
    ap.add_argument("--audit-n", type=int, default=40)
    args = ap.parse_args()

    source = args.root / "time_series_all"
    attributes_path = args.root / "attributes" / "reservoir_attributes.csv"
    attributes = load_attributes(attributes_path)
    eligible = []
    files = sorted(source.glob("ResOpsUS_*.csv"))
    for index, path in enumerate(files, 1):
        eligible.extend(extract_file(
            path, attributes, args.closure_max, args.min_flow_margin,
            args.min_inflow_correlation, args.min_inflow_range_ratio,
        ))
        if index % 100 == 0:
            print(json.dumps({"files": index, "eligible": len(eligible)}), flush=True)
    selected = balanced_select(
        eligible, args.per_cell, args.separation_days, args.max_per_dam_cell,
    )
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    write_jsonl(out / "d0_bank.jsonl", selected)
    audit = sorted(selected, key=lambda row: stable_hash(row["stable_key"], "audit"))[:args.audit_n]
    write_jsonl(out / "source_audit_sample.jsonl", audit)
    summary = {
        "contract_id": "018-d0-v1",
        "source": "ResOpsUS v2, Zenodo record 6612040",
        "source_archive_md5": "d0684cbacf6196c246c73b858ab5b752",
        "license": "CC-BY-4.0",
        "official_units": {"storage": "MCM", "inflow": "m3/s", "outflow": "m3/s"},
        "flow_alignment": "for storage[end]-storage[start], sum daily flows on dates start+1 through end",
        "files_scanned": len(files),
        "eligible_windows": len(eligible),
        "eligible_cells": dict(sorted(Counter(row["cell"] for row in eligible).items())),
        "eligible_dams": len({row["dam_id"] for row in eligible}),
        "selected_windows": len(selected),
        "selected_cells": dict(sorted(Counter(row["cell"] for row in selected).items())),
        "selected_dams": len({row["dam_id"] for row in selected}),
        "selection": {"per_cell": args.per_cell, "separation_days": args.separation_days,
                      "max_per_dam_cell": args.max_per_dam_cell},
        "filters": {"closure_max": args.closure_max, "min_flow_margin": args.min_flow_margin,
                    "min_inflow_correlation": args.min_inflow_correlation,
                    "min_inflow_range_ratio": args.min_inflow_range_ratio},
    }
    summary["bank_sha256"] = sha256(out / "d0_bank.jsonl")
    (out / "scope_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
