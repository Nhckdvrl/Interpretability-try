"""Scale axis for 014 (contract amendment r1c). Descriptive: no promote/kill power.

Capability grows with scale, so each rung gates a different item set and a naive
across-size comparison is confounded. The primary readout is therefore on the
COMMON GATED SET -- items every rung of the ladder passes -- with each model's
own gated set reported alongside.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from analyze_common import capability_gate, cluster_boot_median, load_items, per_item_deltas

LADDERS = {
    "qwen3": [("qwen3_0.6b", 0.6), ("qwen3_1.7b", 1.7), ("qwen3_4b", 4.0),
              ("qwen3_8b", 8.0), ("qwen3_14b", 14.0), ("qwen3_32b", 32.0)],
    "gemma3": [("gemma3_4b_it", 4.0), ("gemma3_12b_it", 12.0)],
}
FLOOR = 60


def spearman(x, y):
    def rank(v):
        order = np.argsort(v)
        r = np.empty(len(v), float)
        r[order] = np.arange(len(v), dtype=float)
        return r
    rx, ry = rank(np.asarray(x, float)), rank(np.asarray(y, float))
    rx, ry = rx - rx.mean(), ry - ry.mean()
    return float(rx @ ry / np.sqrt((rx @ rx) * (ry @ ry)))


def spearman_exact_p(x, y):
    """Exact two-sided permutation p. With 5-6 rungs the asymptotic p is useless."""
    from itertools import permutations
    obs = abs(spearman(x, y))
    perms = list(permutations(range(len(y))))
    hits = sum(1 for pm in perms if abs(spearman(x, [y[i] for i in pm])) >= obs - 1e-12)
    return hits / len(perms)


def rung_stats(tag, res_dir, d0, item_set=None):
    passed, diag = capability_gate(res_dir / f"{tag}__probe.jsonl")
    deltas, _ = per_item_deltas(res_dir / f"{tag}__main.jsonl")
    own = [i for i in deltas if i in passed]
    sel = [i for i in (item_set if item_set is not None else own) if i in deltas]
    strict = [i for i in sel if d0[i]["strict_stratum"] == "opaque_strict"]

    def med(items, f):
        return float(np.median([f(i) for i in items])) if items else float("nan")

    ams_strict = med(strict, lambda i: deltas[i]["ALIAS"] - deltas[i]["SEMREL"])
    den_strict = med(strict, lambda i: deltas[i]["EXACT"] - deltas[i]["SEMREL"])
    return dict(
        tag=tag, n_own_gated=len(own), n_used=len(sel), n_strict=len(strict),
        gate_rate=len(own) / max(diag["n_items"], 1), order_gap=diag["order_gap"],
        exact=med(sel, lambda i: deltas[i]["EXACT"]),
        alias_minus_semrel=med(sel, lambda i: deltas[i]["ALIAS"] - deltas[i]["SEMREL"]),
        alias_minus_semrel_strict=ams_strict,
        transfer_ratio_strict=(ams_strict / den_strict) if den_strict else float("nan"),
        ci_strict=cluster_boot_median(
            {i: deltas[i]["ALIAS"] - deltas[i]["SEMREL"] for i in strict}) if strict else None,
        _passed=passed,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--res-dir", default="results/phase1_r1")
    ap.add_argument("--d0", default="data/frozen_d0.jsonl")
    ap.add_argument("--ladder", default="qwen3")
    args = ap.parse_args()

    d0 = load_items(args.d0)
    res_dir = Path(args.res_dir)
    rungs = [(t, p) for t, p in LADDERS[args.ladder]
             if (res_dir / f"{t}__main.jsonl").exists()]

    own = [rung_stats(t, res_dir, d0) for t, _ in rungs]
    common = set.intersection(*[r["_passed"] for r in own])
    print(f"ladder {args.ladder}: {len(rungs)} rungs, common gated set = {len(common)} items")

    rows = [rung_stats(t, res_dir, d0, common) for t, _ in rungs]
    print("\nPRIMARY — common gated set")
    print(f"{'model':<14}{'params':>7}{'own_gate':>10}{'n_strict':>9}"
          f"{'EXACT':>9}{'A-S':>8}{'A-S(str)':>10}{'ratio(str)':>11}")
    for (t, p), r in zip(rungs, rows):
        print(f"{t:<14}{p:>7.1f}{r['gate_rate']:>10.2f}{r['n_strict']:>9}"
              f"{r['exact']:>9.2f}{r['alias_minus_semrel']:>8.2f}"
              f"{r['alias_minus_semrel_strict']:>10.2f}{r['transfer_ratio_strict']:>11.3f}")

    print("\nSECONDARY — each model's own gated set")
    print(f"{'model':<14}{'n_gated':>9}{'n_strict':>9}{'EXACT':>9}{'A-S(str)':>10}{'ratio(str)':>11}")
    for (t, p), r in zip(rungs, own):
        print(f"{t:<14}{r['n_own_gated']:>9}{r['n_strict']:>9}{r['exact']:>9.2f}"
              f"{r['alias_minus_semrel_strict']:>10.2f}{r['transfer_ratio_strict']:>11.3f}")

    ok = [(p, r) for (t, p), r in zip(rungs, own) if r["n_own_gated"] >= FLOOR]
    if len(ok) >= 4:
        lg = [np.log10(p) for p, _ in ok]
        idx = [t for (t, _), r in zip(rungs, own) if r["n_own_gated"] >= FLOOR]
        common_rows = {t: r for (t, _), r in zip(rungs, rows)}
        print(f"\nrungs clearing the capability floor ({FLOOR} items): {len(ok)} / {len(rungs)}")
        for name, series in (
            ("transfer_ratio_strict (common set)", [common_rows[t]["transfer_ratio_strict"] for t in idx]),
            ("A-S opaque_strict (common set)", [common_rows[t]["alias_minus_semrel_strict"] for t in idx]),
            ("EXACT (common set)", [common_rows[t]["exact"] for t in idx]),
            ("gate rate", [r["gate_rate"] for _, r in ok]),
            ("transfer_ratio_strict (OWN gated set)", [r["transfer_ratio_strict"] for _, r in ok]),
        ):
            rho = spearman(lg, series)
            pv = spearman_exact_p(lg, series)
            print(f"  spearman rho vs log10(params), {name:<38} = {rho:+.3f}"
                  f"   exact p = {pv:.3f}{'  *' if pv < 0.05 else ''}")
    else:
        print(f"\nfewer than 4 rungs clear the capability floor; rho not reported (contract r1c)")

    for r in rows + own:
        r.pop("_passed", None)
    (res_dir / f"scale_{args.ladder}.json").write_text(
        json.dumps(dict(common_set=sorted(common), common=rows, own=own), indent=2))


if __name__ == "__main__":
    main()
