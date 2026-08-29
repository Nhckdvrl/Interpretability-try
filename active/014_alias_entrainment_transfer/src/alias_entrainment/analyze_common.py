"""Shared loaders and statistics for the 014 analyses."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np

CONDS = ("EXACT", "ALIAS", "SEMREL", "UNREL")
N_BOOT = 10000
SEED = 20260829


def load_items(path):
    return {json.loads(l)["item_id"]: json.loads(l) for l in open(path, encoding="utf-8")}


def entity_of(item_id: str) -> str:
    return item_id.split("::")[0]


def capability_gate(probe_path: Path) -> tuple[set[str], dict]:
    """Both option orders must prefer the co-referent alias over the SEMREL foil."""
    rows = [json.loads(l) for l in open(probe_path, encoding="utf-8")]
    lp = defaultdict(dict)
    free = {}
    for r in rows:
        if r["letter"] == "FREE":
            free[r["item_id"]] = r["free_hit"]
        else:
            lp[(r["item_id"], r["order"])][r["letter"]] = r["logprob_sum"]
    per_order = defaultdict(dict)
    for (iid, order), v in lp.items():
        gold = "A" if order == 0 else "B"
        foil = "B" if order == 0 else "A"
        per_order[iid][order] = v[gold] > v[foil]
    passed = {iid for iid, o in per_order.items() if all(o.values())}
    # order artifact diagnostic (the failure mode that invalidated 012 r2)
    acc0 = np.mean([o.get(0, False) for o in per_order.values()])
    acc1 = np.mean([o.get(1, False) for o in per_order.values()])
    diag = dict(n_items=len(per_order), n_passed=len(passed),
                acc_order0=float(acc0), acc_order1=float(acc1),
                order_gap=float(acc0 - acc1),
                free_probe_agreement=float(np.mean(
                    [free.get(i, False) for i in per_order])) if free else None)
    return passed, diag


def per_item_deltas(main_path: Path, metric="logprob_sum"):
    rows = [json.loads(l) for l in open(main_path, encoding="utf-8")]
    base, cells = {}, defaultdict(list)
    for r in rows:
        if r["condition"] == "NOCTX":
            base[(r["item_id"], r["qid"])] = r[metric]
    for r in rows:
        if r["condition"] != "NOCTX":
            b = base[(r["item_id"], r["qid"])]
            cells[(r["item_id"], r["condition"])].append(r[metric] - b)
    out = defaultdict(dict)
    for (iid, cond), vals in cells.items():
        out[iid][cond] = float(np.mean(vals))          # mean over 3 carriers x 2 frames
    return dict(out), base


def cluster_boot_median(values: dict[str, float], n_boot=N_BOOT, seed=SEED):
    """values: item_id -> value. Resamples entities, keeps both directions together."""
    by_ent = defaultdict(list)
    for iid, v in values.items():
        by_ent[entity_of(iid)].append(v)
    ents = sorted(by_ent)
    obs = float(np.median([v for vs in by_ent.values() for v in vs]))
    # ragged -> NaN-padded matrix so the whole bootstrap is one vectorized op
    width = max(len(v) for v in by_ent.values())
    mat = np.full((len(ents), width), np.nan)
    for i, e in enumerate(ents):
        mat[i, :len(by_ent[e])] = by_ent[e]
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(ents), size=(n_boot, len(ents)))
    boots = np.nanmedian(mat[idx].reshape(n_boot, -1), axis=1)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return dict(median=obs, ci_lo=float(lo), ci_hi=float(hi),
                excludes_zero=bool(lo > 0 or hi < 0), n_items=len(values),
                n_entities=len(ents))


