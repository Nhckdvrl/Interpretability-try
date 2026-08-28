from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

ALPHA = 0.5


@dataclass(frozen=True)
class WorkerStats:
    worker: str
    n_target: int
    n_other: int
    accuracy: float
    target_lr: float
    other_lr: float


def _rate(k: int, n: int, alpha: float = ALPHA) -> float:
    return (k + alpha) / (n + 2 * alpha)


def worker_stats(df: pd.DataFrame, *, worker_col: str, truth_col: str, answer_col: str,
                 target_label: int, other_label: int, min_per_class: int) -> dict[str, WorkerStats]:
    """Estimate source-specific directional LRs on a binary truth slice.

    Responses outside {target_label, other_label} remain in the denominators. This is
    deliberate: in a multiclass source task, a third-label response is evidence that the
    worker did *not* emit the target/other message and must not be silently discarded.
    """
    subset = df[df[truth_col].isin([target_label, other_label])]
    out: dict[str, WorkerStats] = {}
    for worker, g in subset.groupby(worker_col, sort=False):
        gt = g[g[truth_col] == target_label]
        go = g[g[truth_col] == other_label]
        if len(gt) < min_per_class or len(go) < min_per_class:
            continue
        p_t_given_t = _rate(int((gt[answer_col] == target_label).sum()), len(gt))
        p_t_given_o = _rate(int((go[answer_col] == target_label).sum()), len(go))
        p_o_given_t = _rate(int((gt[answer_col] == other_label).sum()), len(gt))
        p_o_given_o = _rate(int((go[answer_col] == other_label).sum()), len(go))
        target_lr = p_t_given_t / p_t_given_o
        other_lr = p_o_given_t / p_o_given_o
        accuracy = float((g[answer_col] == g[truth_col]).mean())
        out[str(worker)] = WorkerStats(str(worker), len(gt), len(go), accuracy, target_lr, other_lr)
    return out


def stable_worker_pairs(cal: dict[str, WorkerStats], val: dict[str, WorkerStats], *,
                        min_low_accuracy: float = 0.55,
                        min_accuracy_gap: float = 0.08,
                        min_lr_margin: float = 1.15) -> list[tuple[WorkerStats, WorkerStats, WorkerStats, WorkerStats]]:
    """Return (low_cal, high_cal, low_val, high_val) pairs robust on held-out tasks."""
    ids = sorted(set(cal) & set(val))
    candidates = []
    for low_id in ids:
        lc, lv = cal[low_id], val[low_id]
        if min(lc.accuracy, lv.accuracy) <= min_low_accuracy:
            continue
        if not (lc.target_lr > 1 and lv.target_lr > 1 and 0 < lc.other_lr < 1 and 0 < lv.other_lr < 1):
            continue
        for high_id in ids:
            if high_id == low_id:
                continue
            hc, hv = cal[high_id], val[high_id]
            if min(hc.accuracy, hv.accuracy) <= min_low_accuracy:
                continue
            if min(hc.accuracy - lc.accuracy, hv.accuracy - lv.accuracy) < min_accuracy_gap:
                continue
            if not (hc.target_lr > lc.target_lr * min_lr_margin and hv.target_lr > lv.target_lr * min_lr_margin):
                continue
            if not (0 < hc.other_lr < lc.other_lr / min_lr_margin < 1 and 0 < hv.other_lr < lv.other_lr / min_lr_margin < 1):
                continue
            score = (hc.accuracy - lc.accuracy) + (hv.accuracy - lv.accuracy)
            candidates.append((score, lc, hc, lv, hv))
    candidates.sort(key=lambda x: x[0], reverse=True)
    return [(lc, hc, lv, hv) for _, lc, hc, lv, hv in candidates]


def split_by_task(df: pd.DataFrame, *, task_col: str, seed: int, calibration_fraction: float = 0.6):
    tasks = np.array(sorted(df[task_col].astype(str).unique()))
    rng = np.random.default_rng(seed)
    rng.shuffle(tasks)
    cut = int(round(len(tasks) * calibration_fraction))
    cal_tasks = set(tasks[:cut]); val_tasks = set(tasks[cut:])
    return df[df[task_col].astype(str).isin(cal_tasks)].copy(), df[df[task_col].astype(str).isin(val_tasks)].copy()


def choose_disjoint_pairs(pairs, *, limit: int) -> list:
    """Avoid pseudo-replication by using each worker at most once in frozen scenarios."""
    out = []; used = set()
    for pair in pairs:
        low, high = pair[0], pair[1]
        if low.worker in used or high.worker in used:
            continue
        out.append(pair); used.update([low.worker, high.worker])
        if len(out) >= limit:
            break
    return out


def make_record(*, dataset_name: str, license_name: str, source_url: str, domain: str,
                target_label: int, other_label: int, pair, scenario_index: int, seed: int) -> dict:
    low, high, low_val, high_val = pair
    target_h = f"the task's true label is {target_label}"
    other_h = f"the task's true label is {other_label}"
    low_profile = (f"Annotator {low.worker} was correct on {low.accuracy:.1%} of the held-out binary calibration records; "
                   f"report-{target_label} LR={low.target_lr:.3f}, report-{other_label} LR={low.other_lr:.3f}.")
    high_profile = (f"Annotator {high.worker} was correct on {high.accuracy:.1%} of the held-out binary calibration records; "
                    f"report-{target_label} LR={high.target_lr:.3f}, report-{other_label} LR={high.other_lr:.3f}.")
    calibration = (
        "Source profiles were estimated from a fixed 60% task-disjoint calibration split before any model call. "
        "A separate 40% task split preserves the same source ordering in both report directions."
    )
    short_delay = "The record then lists two unrelated task identifiers and their completion timestamps; neither task shares this label decision or either source identity."
    long_delay = "The record then lists eight unrelated task identifiers, task-set identifiers, and completion timestamps from other annotators. None shares this label decision, message content, or either source identity."
    hi_re = f"Recall that the earlier report came from Annotator {high.worker}. Its audited calibration profile was: {high_profile}"
    lo_re = f"Recall that the earlier report came from Annotator {low.worker}. Its audited calibration profile was: {low_profile}"
    hi_ctrl = "Before deciding, recall that the earlier report remains part of the same annotation record and that the surrounding administrative metadata was generated under the fixed protocol."
    lo_ctrl = hi_ctrl
    flags = {
        "binary_hypotheses_exclusive_gold": True, "binary_hypotheses_exhaustive_gold": True,
        "message_direction_gold": True, "same_message_content_across_sources_gold": True,
        "source_reliability_above_chance_gold": True, "source_reliability_order_gold": True,
        "directional_likelihood_ratios_valid_gold": True, "calibration_matches_likelihood_ratios_gold": True,
        "source_profiles_hypothesis_neutral_gold": True, "source_identity_content_independent_gold": True,
        "delay_material_message_neutral_gold": True, "delay_material_source_neutral_gold": True,
        "short_and_long_delays_natural_gold": True, "reinstatement_does_not_repeat_message_gold": True,
        "reinstatement_only_restores_source_metadata_gold": True, "matched_length_control_semantically_inert_gold": True,
        "direction_pair_matched_gold": True, "actions_symmetric_gold": True, "natural_setting_gold": True,
    }
    return {
        "scenario_id": f"{dataset_name}:{domain}:{target_label}v{other_label}:{scenario_index:03d}",
        "domain": domain,
        "background": f"A new annotation task in {domain} is known, for this binary decision, to have true label {target_label} or {other_label}.",
        "calibration_text": calibration,
        "target_hypothesis": target_h, "other_hypothesis": other_h,
        "target_action": f"accept label {target_label} for the task", "other_action": f"accept label {other_label} for the task",
        "high_source": f"Annotator {high.worker}", "low_source": f"Annotator {low.worker}",
        "high_source_profile": high_profile, "low_source_profile": low_profile,
        "high_source_reliability": high.accuracy, "low_source_reliability": low.accuracy,
        "low_target_lr": low.target_lr, "high_target_lr": high.target_lr,
        "low_other_lr": low.other_lr, "high_other_lr": high.other_lr,
        "target_message": f"The annotator reports label {target_label}.",
        "other_message": f"The annotator reports label {other_label}.",
        "short_delay_text": short_delay, "long_delay_text": long_delay,
        "high_source_reinstatement": hi_re, "low_source_reinstatement": lo_re,
        "high_source_length_control": hi_ctrl, "low_source_length_control": lo_ctrl,
        "source": {
            "dataset": dataset_name, "record_id": f"workers={low.worker},{high.worker};labels={target_label},{other_label};seed={seed}",
            "license": license_name, "split": "task-disjoint-60/40", "provenance": "external-derived", "url": source_url,
            "validation_low_accuracy": low_val.accuracy, "validation_high_accuracy": high_val.accuracy,
            "validation_low_target_lr": low_val.target_lr, "validation_high_target_lr": high_val.target_lr,
            "validation_low_other_lr": low_val.other_lr, "validation_high_other_lr": high_val.other_lr,
        },
        **flags,
    }


def build_from_csv(path: str, *, dataset_name: str, license_name: str, source_url: str,
                   domain_col: str, task_col: str, worker_col: str, truth_col: str, answer_col: str,
                   seed: int, min_per_class: int, pairs_per_domain: int) -> list[dict]:
    df = pd.read_csv(path)
    records=[]
    for domain_value, g in df.groupby(domain_col, sort=True):
        labels = sorted(set(g[truth_col].dropna().astype(int).unique()))
        for target_label, other_label in [(a,b) for i,a in enumerate(labels) for b in labels[i+1:]]:
            binary = g[g[truth_col].isin([target_label, other_label])].copy()
            if binary[task_col].nunique() < 2 * min_per_class:
                continue
            cal_df, val_df = split_by_task(binary, task_col=task_col, seed=seed + int(target_label)*101 + int(other_label)*1009)
            cal = worker_stats(cal_df, worker_col=worker_col, truth_col=truth_col, answer_col=answer_col,
                               target_label=target_label, other_label=other_label, min_per_class=min_per_class)
            val = worker_stats(val_df, worker_col=worker_col, truth_col=truth_col, answer_col=answer_col,
                               target_label=target_label, other_label=other_label, min_per_class=max(5, min_per_class//2))
            chosen = choose_disjoint_pairs(stable_worker_pairs(cal,val), limit=pairs_per_domain)
            for i,pair in enumerate(chosen,1):
                records.append(make_record(dataset_name=dataset_name, license_name=license_name,
                    source_url=source_url, domain=f"{domain_col}-{domain_value}", target_label=int(target_label),
                    other_label=int(other_label), pair=pair, scenario_index=i, seed=seed))
    return records


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--csv', required=True); ap.add_argument('--dataset-name', required=True)
    ap.add_argument('--license', required=True); ap.add_argument('--source-url', required=True)
    ap.add_argument('--domain-col', required=True); ap.add_argument('--task-col', required=True)
    ap.add_argument('--worker-col', required=True); ap.add_argument('--truth-col', required=True); ap.add_argument('--answer-col', required=True)
    ap.add_argument('--out', required=True); ap.add_argument('--seed', type=int, default=20260829)
    ap.add_argument('--min-per-class', type=int, default=20); ap.add_argument('--pairs-per-domain', type=int, default=4)
    args=ap.parse_args()
    rows=build_from_csv(args.csv,dataset_name=args.dataset_name,license_name=args.license,source_url=args.source_url,
        domain_col=args.domain_col,task_col=args.task_col,worker_col=args.worker_col,truth_col=args.truth_col,answer_col=args.answer_col,
        seed=args.seed,min_per_class=args.min_per_class,pairs_per_domain=args.pairs_per_domain)
    Path(args.out).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
    print(json.dumps({'records':len(rows),'domains':len({r['domain'] for r in rows})},indent=2))

if __name__=='__main__': main()
