from __future__ import annotations

import argparse
import collections
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


def _pair_score(pair) -> float:
    lc, hc, lv, hv = pair
    return (hc.accuracy - lc.accuracy) + (hv.accuracy - lv.accuracy)


def _cell_matching(ranked, free: set[str], limit: int) -> list:
    """Best vertex-disjoint set of at most `limit` pairs from one cell.

    Scanning a cell's ranked list and taking whatever fits is what wastes annotators:
    a strong annotator consumed by an easy pairing can be the only partner some other
    pairing had. Selecting a maximum-cardinality, maximum-weight matching instead lets
    the cell keep as many disjoint pairs as its candidate graph actually supports.
    """
    if limit <= 0:
        return []
    try:
        import networkx as nx
    except ModuleNotFoundError as exc:  # pragma: no cover - dependency guard
        raise RuntimeError("pair selection needs networkx; install the 'd0' extra") from exc
    graph = nx.Graph()
    for pair in sorted(ranked, key=lambda p: (-_pair_score(p), p[0].worker, p[1].worker)):
        low, high = pair[0].worker, pair[1].worker
        if low not in free or high not in free:
            continue
        if graph.has_edge(low, high):
            continue  # the ranked list is score-sorted, so the first orientation wins
        graph.add_edge(low, high, weight=_pair_score(pair), pair=pair)
    if graph.number_of_edges() == 0:
        return []
    matched = nx.max_weight_matching(graph, maxcardinality=True)
    chosen = [graph[u][v]["pair"] for u, v in matched]
    chosen.sort(key=lambda p: (-_pair_score(p), p[0].worker, p[1].worker))
    return chosen[:limit]


def select_global_pairs(cells: list[dict], *, pairs_per_cell: int,
                        target_total: int | None = None) -> None:
    """Choose globally annotator-disjoint pairs across cells, filling `cells[i]["chosen"]`.

    Two stages. First a balanced pass in which every cell is offered `pairs_per_cell`,
    scarcest cell first — a cell whose candidate graph supports only a handful of
    disjoint pairs must pick before a cell with hundreds of alternatives, or its few
    usable annotators get spent elsewhere. Then, if `target_total` is set and the
    balanced pass fell short, a top-up pass repeatedly gives one more pair to whichever
    cell currently holds the fewest, so the overflow lands as evenly as supply allows.
    """
    for cell in cells:
        cell["chosen"] = []
        cell["ceiling"] = len(_cell_matching(cell["ranked"], cell["vertices"], 10 ** 6))
    used: set[str] = set()

    for cell in sorted(cells, key=lambda c: (c["ceiling"], str(c["key"]))):
        free = cell["vertices"] - used
        cell["chosen"] = _cell_matching(cell["ranked"], free, pairs_per_cell)
        used.update(w.worker for pair in cell["chosen"] for w in pair[:2])

    if target_total is None:
        return
    exhausted: set = set()
    while sum(len(c["chosen"]) for c in cells) < target_total:
        order = sorted((c for c in cells if c["key"] not in exhausted),
                       key=lambda c: (len(c["chosen"]), c["ceiling"], str(c["key"])))
        if not order:
            return
        for cell in order:
            extra = _cell_matching(cell["ranked"], cell["vertices"] - used, 1)
            if not extra:
                exhausted.add(cell["key"])
                continue
            cell["chosen"].extend(extra)
            used.update(w.worker for w in extra[0][:2])
            break
        else:
            return


DEFAULT_OPTION_LETTERS = {"0": "A", "1": "B", "2": "C"}


def load_domain_specs(path: str | None) -> dict:
    """Load published per-domain task descriptions (optional).

    Keeping these out of the builder keeps it dataset-agnostic: without the file the
    records fall back to bare domain/label codes, which is correct but unnatural.
    """
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _option(specs: dict, domain_value, label: int) -> tuple[str, str]:
    """Return (letter, human phrase) for a raw label code in a domain."""
    letters = specs.get("option_letters", DEFAULT_OPTION_LETTERS)
    letter = letters.get(str(label), str(label))
    dom = specs.get("domains", {}).get(str(domain_value), {})
    phrase = dom.get("options", {}).get(str(label))
    return letter, (phrase or f"option {letter}")


def _background(specs: dict, domain_col: str, domain_value, target_letter: str, other_letter: str) -> str:
    dom = specs.get("domains", {}).get(str(domain_value))
    tail = (f"For the task at hand the audited gold answer is known to be "
            f"option {target_letter} or option {other_letter}.")
    if not dom:
        return (f"A new annotation task in {domain_col}-{domain_value} is known, for this binary "
                f"decision, to have true label {target_letter} or {other_letter}.")
    presentation = dom.get("presentation", "presents the task material")
    if dom.get("documented") and dom.get("question"):
        return (f"NetEaseCrowd task set for {domain_col} {domain_value} — {dom['title']}. "
                f"Each task {presentation}, and the annotator answers: \"{dom['question']}\" {tail}")
    return (f"NetEaseCrowd task set for {domain_col} {domain_value} — {dom['title']}. "
            f"Each task {presentation}; the public release records the annotations and audited gold "
            f"answers but not the question text. {tail}")


def make_record(*, dataset_name: str, license_name: str, source_url: str, domain: str,
                domain_col: str, domain_value, specs: dict,
                target_label: int, other_label: int, pair, scenario_index: int, seed: int,
                short_delay: str, long_delay: str) -> dict:
    low, high, low_val, high_val = pair
    t_letter, t_phrase = _option(specs, domain_value, target_label)
    o_letter, o_phrase = _option(specs, domain_value, other_label)
    def _hyp(letter: str, phrase: str) -> str:
        gloss = "" if phrase == f"option {letter}" else f" ({phrase})"
        return f"the audited gold answer for this task is option {letter}{gloss}"

    target_h = _hyp(t_letter, t_phrase)
    other_h = _hyp(o_letter, o_phrase)
    low_profile = (f"Annotator {low.worker} was correct on {low.accuracy:.1%} of the binary calibration records; "
                   f"report-{t_letter} LR={low.target_lr:.3f}, report-{o_letter} LR={low.other_lr:.3f}.")
    high_profile = (f"Annotator {high.worker} was correct on {high.accuracy:.1%} of the binary calibration records; "
                    f"report-{t_letter} LR={high.target_lr:.3f}, report-{o_letter} LR={high.other_lr:.3f}.")
    calibration = (
        "Source profiles were estimated from a fixed 60% task-disjoint calibration split before any model call. "
        "A separate 40% task split preserves the same source ordering in both report directions."
    )
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
    dom_spec = specs.get("domains", {}).get(str(domain_value), {})
    return {
        "scenario_id": f"{dataset_name}:{domain}:{target_label}v{other_label}:{scenario_index:03d}",
        "domain": domain,
        "cell_id": f"{domain}:{target_label}v{other_label}",
        "background": _background(specs, domain_col, domain_value, t_letter, o_letter),
        "calibration_text": calibration,
        "target_hypothesis": target_h, "other_hypothesis": other_h,
        "target_action": f"record option {t_letter} as the accepted answer for this task",
        "other_action": f"record option {o_letter} as the accepted answer for this task",
        "high_source": f"Annotator {high.worker}", "low_source": f"Annotator {low.worker}",
        "high_source_profile": high_profile, "low_source_profile": low_profile,
        "high_source_reliability": high.accuracy, "low_source_reliability": low.accuracy,
        "low_target_lr": low.target_lr, "high_target_lr": high.target_lr,
        "low_other_lr": low.other_lr, "high_other_lr": high.other_lr,
        "target_message": f"The annotator reports option {t_letter}.",
        "other_message": f"The annotator reports option {o_letter}.",
        "short_delay_text": short_delay, "long_delay_text": long_delay,
        "high_source_reinstatement": hi_re, "low_source_reinstatement": lo_re,
        "high_source_length_control": hi_ctrl, "low_source_length_control": lo_ctrl,
        "source": {
            "dataset": dataset_name, "record_id": f"workers={low.worker},{high.worker};labels={target_label},{other_label};seed={seed}",
            "license": license_name, "split": "task-disjoint-60/40", "provenance": "external-derived", "url": source_url,
            "raw_target_label": int(target_label), "raw_other_label": int(other_label),
            "option_letters": {str(target_label): t_letter, str(other_label): o_letter},
            "domain_documented": bool(dom_spec.get("documented", False)),
            "domain_description_url": specs.get("provenance", {}).get("url"),
            "calibration_low_n_target": low.n_target, "calibration_low_n_other": low.n_other,
            "calibration_high_n_target": high.n_target, "calibration_high_n_other": high.n_other,
            "validation_low_n_target": low_val.n_target, "validation_low_n_other": low_val.n_other,
            "validation_high_n_target": high_val.n_target, "validation_high_n_other": high_val.n_other,
            "validation_low_accuracy": low_val.accuracy, "validation_high_accuracy": high_val.accuracy,
            "validation_low_target_lr": low_val.target_lr, "validation_high_target_lr": high_val.target_lr,
            "validation_low_other_lr": low_val.other_lr, "validation_high_other_lr": high_val.other_lr,
        },
        **flags,
    }


def _delay_blocks(g: pd.DataFrame, *, task_col: str, worker_col: str, low_worker: str, high_worker: str,
                  seed: int, taskset_col: str | None, time_col: str | None) -> tuple[str, str]:
    # Exclude whole tasks either focal annotator touched, not merely their own rows: a
    # task survives row-level filtering through some other worker's annotation, which would
    # put a focal-source task into the supposedly unrelated administrative delay material.
    focal_tasks = set(g.loc[g[worker_col].astype(str).isin([low_worker, high_worker]), task_col])
    pool = g[~g[task_col].isin(focal_tasks)].copy()
    if len(pool.drop_duplicates(subset=[task_col])) < 8:
        raise ValueError("fewer than 8 unrelated administrative tasks available for delay controls")
    pool = pool.drop_duplicates(subset=[task_col]).sort_values(task_col, key=lambda x: x.astype(str))
    rng = np.random.default_rng(seed)
    take = min(8, len(pool))
    chosen = pool.iloc[rng.choice(len(pool), size=take, replace=False)]

    def render(row) -> str:
        bits = [f"task {row[task_col]}"]
        if taskset_col and taskset_col in row.index:
            bits.append(f"task-set {row[taskset_col]}")
        if time_col and time_col in row.index:
            bits.append(f"completion-time {row[time_col]}")
        return " / ".join(bits)

    items = [render(row) for _, row in chosen.iterrows()]
    short_items = items[:min(2, len(items))]
    prefix = "Unrelated administrative records from other tasks (no answers, truths, or focal-source identities): "
    return prefix + "; ".join(short_items) + ".", prefix + "; ".join(items) + "."


def build_from_csv(path: str, *, dataset_name: str, license_name: str, source_url: str,
                   domain_col: str, task_col: str, worker_col: str, truth_col: str, answer_col: str,
                   seed: int, min_per_class: int, pairs_per_cell: int = 9,
                   target_scenarios: int | None = None,
                   lr_margin: float = 2.0, domain_specs: dict | None = None,
                   exclude_domains: Iterable[str] = (),
                   taskset_col: str | None = None, time_col: str | None = None) -> list[dict]:
    """Freeze source pairs cell-by-cell, where a cell is one (domain, binary label pair).

    Enumeration and selection are separate. Every contract-valid pair a cell can offer is
    enumerated first; only then are pairs chosen globally, so that a cell with few usable
    annotators is not starved by a cell that had hundreds of alternatives. Annotators stay
    unique across the whole bank, which is what makes each scenario an independent
    source-pair unit rather than a re-use of a strong annotator.
    """
    specs = domain_specs or {}
    excluded = {str(d) for d in exclude_domains}
    df = pd.read_csv(path)
    groups: dict = {}
    cells: list = []
    for domain_value, g in df.groupby(domain_col, sort=True):
        # Excluding a domain has to happen before selection, not after: annotators are
        # unique across the whole bank, so a dropped domain releases its workers back to
        # the domains that remain.
        if str(domain_value) in excluded:
            continue
        groups[domain_value] = g
        labels = sorted(set(g[truth_col].dropna().astype(int).unique()))
        for target_label, other_label in [(a, b) for i, a in enumerate(labels) for b in labels[i + 1:]]:
            binary = g[g[truth_col].isin([target_label, other_label])].copy()
            if binary[task_col].nunique() < 2 * min_per_class:
                continue
            cal_df, val_df = split_by_task(binary, task_col=task_col,
                                           seed=seed + int(target_label) * 101 + int(other_label) * 1009)
            cal = worker_stats(cal_df, worker_col=worker_col, truth_col=truth_col, answer_col=answer_col,
                               target_label=target_label, other_label=other_label, min_per_class=min_per_class)
            val = worker_stats(val_df, worker_col=worker_col, truth_col=truth_col, answer_col=answer_col,
                               target_label=target_label, other_label=other_label,
                               min_per_class=max(5, min_per_class // 2))
            ranked = stable_worker_pairs(cal, val, min_lr_margin=lr_margin)
            if ranked:
                cells.append({"key": (domain_value, int(target_label), int(other_label)),
                              "domain_value": domain_value, "target": int(target_label),
                              "other": int(other_label), "ranked": ranked,
                              "vertices": {w.worker for pair in ranked for w in pair[:2]}})

    select_global_pairs(cells, pairs_per_cell=pairs_per_cell, target_total=target_scenarios)

    records: list[dict] = []
    scenario_counter = 0
    for cell in cells:
        for index, pair in enumerate(cell["chosen"], start=1):
            scenario_counter += 1
            short_delay, long_delay = _delay_blocks(
                groups[cell["domain_value"]], task_col=task_col, worker_col=worker_col,
                low_worker=pair[0].worker, high_worker=pair[1].worker,
                seed=seed + scenario_counter * 7919, taskset_col=taskset_col, time_col=time_col,
            )
            records.append(make_record(
                dataset_name=dataset_name, license_name=license_name, source_url=source_url,
                domain=f"{domain_col}-{cell['domain_value']}", domain_col=domain_col,
                domain_value=cell["domain_value"], specs=specs,
                target_label=cell["target"], other_label=cell["other"],
                pair=pair, scenario_index=index, seed=seed,
                short_delay=short_delay, long_delay=long_delay,
            ))
    return records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', required=True); ap.add_argument('--dataset-name', required=True)
    ap.add_argument('--license', required=True); ap.add_argument('--source-url', required=True)
    ap.add_argument('--domain-col', required=True); ap.add_argument('--task-col', required=True)
    ap.add_argument('--worker-col', required=True); ap.add_argument('--truth-col', required=True)
    ap.add_argument('--answer-col', required=True)
    ap.add_argument('--out', required=True); ap.add_argument('--seed', type=int, default=20260829)
    ap.add_argument('--min-per-class', type=int, default=20)
    ap.add_argument('--pairs-per-cell', type=int, default=9,
                    help='balanced quota offered to every (domain, label pair) cell, scarcest cell first')
    ap.add_argument('--target-scenarios', type=int,
                    help='if the balanced pass falls short, top up least-loaded cell first until this total')
    ap.add_argument('--lr-margin', type=float, default=2.0,
                    help='required high/low separation in both report directions, on both splits')
    ap.add_argument('--domain-descriptions', help='optional JSON of published per-domain task text')
    ap.add_argument('--exclude-domain', action='append', default=[],
                    help='drop a domain value entirely; repeatable')
    ap.add_argument('--taskset-col'); ap.add_argument('--time-col')
    args = ap.parse_args()
    rows = build_from_csv(
        args.csv, dataset_name=args.dataset_name, license_name=args.license, source_url=args.source_url,
        domain_col=args.domain_col, task_col=args.task_col, worker_col=args.worker_col,
        truth_col=args.truth_col, answer_col=args.answer_col, seed=args.seed,
        min_per_class=args.min_per_class, pairs_per_cell=args.pairs_per_cell,
        target_scenarios=args.target_scenarios,
        lr_margin=args.lr_margin, domain_specs=load_domain_specs(args.domain_descriptions),
        exclude_domains=args.exclude_domain,
        taskset_col=args.taskset_col, time_col=args.time_col)
    Path(args.out).write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf-8')
    domains = sorted({r['domain'] for r in rows})
    cells = collections.Counter((r['domain'], r['scenario_id'].split(':')[2]) for r in rows)
    print(json.dumps({'records': len(rows), 'domains': len(domains),
                      'unique_workers': len({w for r in rows for w in (r['high_source'], r['low_source'])}),
                      'cells': len(cells), 'per_domain': {d: sum(1 for r in rows if r['domain'] == d) for d in domains},
                      'per_cell': {f'{d}:{lp}': n for (d, lp), n in sorted(cells.items())}}, indent=2))


if __name__ == '__main__':
    main()
