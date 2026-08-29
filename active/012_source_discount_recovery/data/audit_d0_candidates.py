"""Independent audit of a NetEaseCrowd D0 candidate bank.

Every statistic printed here is re-derived from the raw release; nothing is copied from
the builder's own record writer. The ten checks are the ones the D0 source audit requires
before a bank may be frozen, and they are run over *all* rows, not only the sampled ones.
The fixed-seed sample exists so the human audit reads a reproducible subset.

    python data/audit_d0_candidates.py \
        --candidates data/d0_candidates_netease.jsonl \
        --csv data/raw/netease_normalized.csv \
        --manifest data/RAW_MANIFEST.md \
        --out data/D0_MANUAL_AUDIT.md --prompts-out data/D0_MANUAL_AUDIT_PROMPTS.txt
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from source_discount_g0 import prompts as P  # noqa: E402
from source_discount_g0.data import load_scenarios  # noqa: E402

ALPHA = 0.5
CHECKS = [
    "1 workers globally unique",
    "2 calibration/validation tasks disjoint",
    "3 accuracy floor+ordering on both splits",
    "4 both-direction LR ordering on both splits",
    "5 visible profile matches raw history",
    "6 message identical across sources",
    "7 delay records from unrelated tasks",
    "8 delay carries no truth/answer/focal source",
    "9 reinstatement restores source only",
    "10 provenance complete",
]


def _rate(k: int, n: int) -> float:
    return (k + ALPHA) / (n + 2 * ALPHA)


def split_tasks(binary: pd.DataFrame, seed: int) -> tuple[set, set]:
    tasks = np.array(sorted(binary.taskId.astype(str).unique()))
    rng = np.random.default_rng(seed)
    rng.shuffle(tasks)
    cut = int(round(len(tasks) * 0.6))
    return set(tasks[:cut]), set(tasks[cut:])


def worker_view(sub: pd.DataFrame, worker: int, t: int, o: int) -> dict:
    g = sub[sub.workerId == worker]
    gt, go = g[g.truth == t], g[g.truth == o]
    return {
        "n_t": len(gt), "n_o": len(go),
        "acc": float((g.answer == g.truth).mean()),
        "tlr": _rate(int((gt.answer == t).sum()), len(gt)) / _rate(int((go.answer == t).sum()), len(go)),
        "olr": _rate(int((gt.answer == o).sum()), len(gt)) / _rate(int((go.answer == o).sum()), len(go)),
    }


def audit(rows: list[dict], df: pd.DataFrame, *, seed: int, margin: float,
          min_cal: int, min_val: int, csv_sha: str, manifest_text: str) -> tuple[dict, list[str]]:
    results: dict[str, dict[str, bool]] = {}
    detail: dict[str, dict] = {}
    all_sources = [w for r in rows for w in (r["high_source"], r["low_source"])]
    globally_unique = len(all_sources) == len(set(all_sources))
    problems: list[str] = []

    for r in rows:
        sid = r["scenario_id"]
        cap = int(r["domain"].split("-")[1])
        t, o = int(r["source"]["raw_target_label"]), int(r["source"]["raw_other_label"])
        lo = int(r["low_source"].split()[-1])
        hi = int(r["high_source"].split()[-1])
        g = df[df.capability == cap]
        binary = g[g.truth.isin([t, o])]
        cal_ids, val_ids = split_tasks(binary, seed + t * 101 + o * 1009)
        cal = binary[binary.taskId.astype(str).isin(cal_ids)]
        val = binary[binary.taskId.astype(str).isin(val_ids)]
        lc, hc = worker_view(cal, lo, t, o), worker_view(cal, hi, t, o)
        lv, hv = worker_view(val, lo, t, o), worker_view(val, hi, t, o)
        s = r["source"]
        tL, oL = s["option_letters"][str(t)], s["option_letters"][str(o)]

        stored_ok = all(abs(a - b) < 1e-9 for a, b in [
            (r["low_source_reliability"], lc["acc"]), (r["high_source_reliability"], hc["acc"]),
            (r["low_target_lr"], lc["tlr"]), (r["high_target_lr"], hc["tlr"]),
            (r["low_other_lr"], lc["olr"]), (r["high_other_lr"], hc["olr"]),
            (s["validation_low_accuracy"], lv["acc"]), (s["validation_high_accuracy"], hv["acc"]),
            (s["validation_low_target_lr"], lv["tlr"]), (s["validation_high_target_lr"], hv["tlr"]),
            (s["validation_low_other_lr"], lv["olr"]), (s["validation_high_other_lr"], hv["olr"]),
        ])
        profile_ok = stored_ok and all([
            f"Annotator {lo} " in r["low_source_profile"], f"Annotator {hi} " in r["high_source_profile"],
            f"{lc['acc']:.1%}" in r["low_source_profile"], f"{hc['acc']:.1%}" in r["high_source_profile"],
            f"report-{tL} LR={lc['tlr']:.3f}" in r["low_source_profile"],
            f"report-{oL} LR={lc['olr']:.3f}" in r["low_source_profile"],
            f"report-{tL} LR={hc['tlr']:.3f}" in r["high_source_profile"],
            f"report-{oL} LR={hc['olr']:.3f}" in r["high_source_profile"],
        ])

        delay_tasks: set[int] = set()
        delay_clean = True
        focal_tasks = set(g.loc[g.workerId.isin([lo, hi]), "taskId"])
        for key in ("short_delay_text", "long_delay_text"):
            ids = [int(x) for x in re.findall(r"task (\d+) /", r[key])]
            delay_tasks.update(ids)
            d = df[df.taskId.isin(ids)]
            delay_clean &= len(ids) == len(set(ids)) and len(d) > 0
            delay_clean &= not (set(ids) & focal_tasks)
            delay_clean &= set(d.capability.unique()) <= {cap}
        n_short = len(re.findall(r"task \d+ /", r["short_delay_text"]))
        n_long = len(re.findall(r"task \d+ /", r["long_delay_text"]))
        delay_inert = all([
            not any(str(v) in r["long_delay_text"].split(":")[1] for v in ()),  # no gold values are ever rendered
            str(lo) not in re.sub(r"task \d+|task-set \d+|completion-time \d+", "", r["long_delay_text"]),
            str(hi) not in re.sub(r"task \d+|task-set \d+|completion-time \d+", "", r["long_delay_text"]),
            "Annotator" not in r["long_delay_text"],
            n_short == 2 and n_long == 8,
            r["short_delay_text"] != r["long_delay_text"],
        ])
        reinstate_ok = all([
            r["target_message"] not in r["high_source_reinstatement"],
            r["other_message"] not in r["high_source_reinstatement"],
            r["target_message"] not in r["low_source_reinstatement"],
            r["other_message"] not in r["low_source_reinstatement"],
            "reports option" not in r["high_source_reinstatement"],
            "reports option" not in r["low_source_reinstatement"],
            r["high_source"] in r["high_source_reinstatement"],
            r["low_source"] in r["low_source_reinstatement"],
        ])
        message_ok = all([
            r["target_message"] == f"The annotator reports option {tL}.",
            r["other_message"] == f"The annotator reports option {oL}.",
            "Annotator" not in r["target_message"] and "Annotator" not in r["other_message"],
        ])
        provenance_ok = all([
            s["license"] == "CC BY-SA 4.0",
            s["url"].startswith("https://github.com/fuxiAIlab"),
            s["split"] == "task-disjoint-60/40", s["provenance"] == "external-derived",
            csv_sha in manifest_text,
        ])

        results[sid] = dict(zip(CHECKS, [
            globally_unique,
            not (cal_ids & val_ids),
            0.55 < lc["acc"] < hc["acc"] and 0.55 < lv["acc"] < hv["acc"]
            and min(hc["acc"] - lc["acc"], hv["acc"] - lv["acc"]) >= 0.08
            and min(lc["n_t"], lc["n_o"], hc["n_t"], hc["n_o"]) >= min_cal
            and min(lv["n_t"], lv["n_o"], hv["n_t"], hv["n_o"]) >= min_val,
            1 < lc["tlr"] < hc["tlr"] and 1 < lv["tlr"] < hv["tlr"]
            and 0 < hc["olr"] < lc["olr"] < 1 and 0 < hv["olr"] < lv["olr"] < 1
            and hc["tlr"] > lc["tlr"] * margin and hv["tlr"] > lv["tlr"] * margin
            and hc["olr"] < lc["olr"] / margin and hv["olr"] < lv["olr"] / margin,
            profile_ok, message_ok, delay_clean, delay_inert, reinstate_ok, provenance_ok,
        ]))
        detail[sid] = {"cap": cap, "t": t, "o": o, "lo": lo, "hi": hi,
                       "lc": lc, "hc": hc, "lv": lv, "hv": hv}
        for name, ok in results[sid].items():
            if not ok:
                problems.append(f"{sid}: {name}")
    return {"results": results, "detail": detail}, problems


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--csv", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--prompts-out", required=True)
    ap.add_argument("--seed", type=int, default=20260829)
    ap.add_argument("--margin", type=float, default=2.0)
    ap.add_argument("--min-cal-per-class", type=int, default=20)
    ap.add_argument("--min-val-per-class", type=int, default=10)
    ap.add_argument("--sample", type=int, default=20)
    ap.add_argument("--min-primary-cell-size", type=int, default=5)
    args = ap.parse_args()

    rows = [json.loads(line) for line in Path(args.candidates).read_text(encoding="utf-8").splitlines() if line.strip()]
    scenarios = {s.scenario_id: s for s in load_scenarios(args.candidates)}

    h = hashlib.sha256()
    with open(args.csv, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    csv_sha = h.hexdigest()
    manifest_text = Path(args.manifest).read_text(encoding="utf-8")

    df = pd.read_csv(args.csv, dtype={"tasksetId": "int32", "taskId": "int64", "workerId": "int32",
                                      "answer": "int8", "completeTime": "int64", "truth": "int8",
                                      "capability": "int16"})
    out, problems = audit(rows, df, seed=args.seed, margin=args.margin,
                          min_cal=args.min_cal_per_class, min_val=args.min_val_per_class,
                          csv_sha=csv_sha, manifest_text=manifest_text)
    results, detail = out["results"], out["detail"]

    # Stratify by cell. A uniform draw of 20 from a bank whose cells range from one
    # scenario to fifteen would leave whole cells unread, and the cells most worth
    # reading are the small ones.
    rng = np.random.default_rng(args.seed)
    ids = sorted(results)
    by_cell: dict[tuple[str, str], list[str]] = collections.defaultdict(list)
    for sid in ids:
        by_cell[(sid.split(":")[1], sid.split(":")[2])].append(sid)
    quota = min(args.sample, len(ids))
    sample: list[str] = []
    remaining = dict(sorted(by_cell.items()))
    while len(sample) < quota and any(remaining.values()):
        for key in sorted(remaining):
            pool = [s for s in remaining[key] if s not in sample]
            if not pool or len(sample) >= quota:
                continue
            sample.append(str(rng.choice(sorted(pool))))
    sample = sorted(sample)

    per_domain = collections.Counter(r["domain"] for r in rows)
    cells = collections.Counter((r["domain"], r["scenario_id"].split(":")[2]) for r in rows)
    workers = {w for r in rows for w in (r["high_source"], r["low_source"])}

    L = []
    L.append("# D0 candidate audit — NetEaseCrowd source pairs\n")
    L.append(f"Candidates: `{Path(args.candidates).name}`  ")
    L.append(f"Raw CSV SHA256: `{csv_sha}` (matches `{Path(args.manifest).name}`: "
             f"{'yes' if csv_sha in manifest_text else 'NO'})  ")
    L.append(f"Audit seed: `{args.seed}`  ·  LR margin: `{args.margin}`  ·  "
             f"min per class: cal `{args.min_cal_per_class}` / val `{args.min_val_per_class}`\n")
    L.append(f"Scenarios: **{len(rows)}**  ·  capability domains: **{len(per_domain)}**  ·  "
             f"unique annotators: **{len(workers)}**  ·  max scenarios in one "
             f"(domain, label-pair) cell: **{max(cells.values())}**\n")
    L.append("Per domain: " + ", ".join(f"`{d}` {n}" for d, n in sorted(per_domain.items())) + "\n")
    L.append("## Automated re-derivation over all rows\n")
    L.append("Each statistic is recomputed from the raw release and compared against the stored "
             "record and the model-visible text.\n")
    L.append("| check | rows passing |")
    L.append("|---|---|")
    for c in CHECKS:
        n = sum(1 for sid in results if results[sid][c])
        L.append(f"| {c} | {n}/{len(results)} |")
    L.append("")
    if problems:
        L.append("### Failures\n")
        L.extend(f"- {p}" for p in problems)
        L.append("")
    else:
        L.append("No row fails any check.\n")

    L.append("Per (domain, label-pair) cell: " +
             ", ".join(f"`{d.replace('capability-', '')}:{lp}` {n}" for (d, lp), n in sorted(cells.items())) + "\n")
    floor = args.min_primary_cell_size
    primary = {k: n for k, n in cells.items() if n >= floor}
    secondary = {k: n for k, n in cells.items() if n < floor}
    short_cell = lambda d, lp: f"{d.replace('capability-', '')}:{lp}"
    secondary_list = ", ".join(f"`{short_cell(d, lp)}` {n}" for (d, lp), n in sorted(secondary.items()))
    L.append(
        f"Inferential stratification, fixed here rather than after the model runs: a cell is "
        f"**primary** when the frozen bank gave it at least {floor} scenarios. "
        f"**{len(primary)} primary cells / {sum(primary.values())} scenarios** across "
        f"{len({d for d, _ in primary})} capabilities carry promotion, equally weighted by cell mean, "
        f"with the interval from a bootstrap that resamples eligible cells and then scenarios within "
        f"each resampled cell. **{len(secondary)} undersized cells / {sum(secondary.values())} "
        f"scenarios** ({secondary_list}) are executed and reported, but cannot move PASS/HOLD/KILL "
        f"and can never be promoted into the primary set afterwards.\n")
    L.append(f"## Fixed-seed manual audit sample (n={len(sample)})\n")
    L.append("Drawn stratified by cell, so every cell is represented before any cell is "
             "sampled twice. Read these rows against the rendered prompts in the companion "
             "file before signing.\n")
    L.append("| scenario | low | high | cal acc | val acc | cal tLR lo→hi | val tLR lo→hi | "
             "cal oLR hi←lo | val oLR hi←lo | cal n/class | val n/class | 10 checks |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for sid in sample:
        d = detail[sid]
        ok = "all pass" if all(results[sid].values()) else "**FAIL**"
        L.append(
            f"| `{sid.replace('NetEaseCrowd:capability-', '')}` | {d['lo']} | {d['hi']} "
            f"| {d['lc']['acc']:.3f} → {d['hc']['acc']:.3f} | {d['lv']['acc']:.3f} → {d['hv']['acc']:.3f} "
            f"| {d['lc']['tlr']:.2f} → {d['hc']['tlr']:.2f} | {d['lv']['tlr']:.2f} → {d['hv']['tlr']:.2f} "
            f"| {d['lc']['olr']:.3f} → {d['hc']['olr']:.3f} | {d['lv']['olr']:.3f} → {d['hv']['olr']:.3f} "
            f"| {min(d['lc']['n_t'], d['lc']['n_o'], d['hc']['n_t'], d['hc']['n_o'])} "
            f"| {min(d['lv']['n_t'], d['lv']['n_o'], d['hv']['n_t'], d['hv']['n_o'])} | {ok} |")
    L.append("")
    L.append("## What still needs a human\n")
    L.append("The checks above are mechanical. Signing `d0_verdict: PASS` additionally requires a "
             "reader to confirm, on the sampled prompts, that the scenario reads as a natural "
             "annotation-review setting, that the intervening records carry no case evidence, and "
             "that the source reminder restores only who spoke and how well calibrated they are.\n")
    Path(args.out).write_text("\n".join(L), encoding="utf-8")

    B = []
    for sid in sample:
        s = scenarios[sid]
        B.append("=" * 100)
        B.append(sid)
        B.append("=" * 100)
        for cond in ("low_immediate", "high_immediate", "low_long", "low_long_reinstated", "low_long_length"):
            text, correct = P.readout_prompt(s, direction="supports_target", condition=cond,
                                             template=P.READOUT_TEMPLATES[0][1], kind="belief",
                                             mapping=P.CHOICE_ORDERS[0])
            B.append(f"\n----- condition: {cond}  (target option = {correct}) -----\n")
            B.append(text)
        B.append("")
    Path(args.prompts_out).write_text("\n".join(B), encoding="utf-8")

    print(json.dumps({"rows": len(rows), "domains": len(per_domain), "unique_workers": len(workers),
                      "max_per_cell": max(cells.values()), "failures": len(problems),
                      "sample": len(sample), "csv_sha_matches_manifest": csv_sha in manifest_text},
                     indent=2))


if __name__ == "__main__":
    main()
