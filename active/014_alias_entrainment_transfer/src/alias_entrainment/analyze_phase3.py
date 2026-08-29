"""Phase-3 analysis for 014. Implements the `phase3` block of contract_r1.yaml."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from analyze_common import cluster_boot_median

CONDS = ("EXACT", "ALIAS", "SEMREL", "UNREL")


def per_item(keys, vals, items):
    """dDLA_cond = DLA(cond) - DLA(NOCTX), averaged over carriers x frames."""
    base, cells = {}, defaultdict(list)
    for (iid, qid, cond, frame), v in zip(keys, vals):
        if cond == "NOCTX":
            base[(iid, qid)] = v
    for (iid, qid, cond, frame), v in zip(keys, vals):
        if cond != "NOCTX":
            cells[(iid, cond)].append(v - base[(iid, qid)])
    keep = set(items)
    out = defaultdict(dict)
    for (iid, cond), vs in cells.items():
        if iid in keep:
            out[iid][cond] = float(np.mean(vs))
    return dict(out)


def boot_diff(a: dict, b: dict):
    common = sorted(set(a) & set(b))
    return cluster_boot_median({i: a[i] - b[i] for i in common})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--res-dir", default="results/phase3_r1")
    ap.add_argument("--sweep-dir", default="results/phase2_r1")
    ap.add_argument("--d0", default="data/frozen_d0.jsonl")
    ap.add_argument("--tags", nargs="+", required=True)
    args = ap.parse_args()

    d0 = {json.loads(l)["item_id"]: json.loads(l) for l in open(args.d0, encoding="utf-8")}
    report = {}
    for tag in args.tags:
        blob = json.loads((Path(args.res_dir) / f"{tag}__dla.json").read_text())
        keys = [tuple(k) for k in blob["keys"]]
        strict = blob["eval_items_strict"]
        allit = blob["eval_items"]
        sweep = json.loads((Path(args.sweep_dir) / f"{tag}__sweep.json").read_text())
        nl = max(h["layer"] for h in sweep["heads"]) + 1
        ranked = [(h["layer"], h["head"]) for h in sweep["heads"]]

        print("=" * 78)
        print(f"{tag}   {len(strict)} opaque_strict / {len(allit)} held-out items")
        rows = {}
        for frac in blob["topk_frac"]:
            ent = per_item(keys, blob["dla"][f"ent{frac}"], strict)
            rnd = [per_item(keys, blob["dla"][k], strict)
                   for k in blob["dla"] if k.startswith(f"rand{frac}_")]
            k = len(ranked[:max(1, round(blob["n_heads_total"] * frac))])
            late = sum(1 for l, _ in ranked[:k] if l >= 2 * nl / 3)

            ex = cluster_boot_median({i: ent[i]["EXACT"] for i in ent})
            ex_r = float(np.median([np.median([r[i]["EXACT"] for i in r]) for r in rnd]))
            valid = ex["median"] > 0 and ex["median"] > 2 * abs(ex_r)

            h3 = boot_diff({i: ent[i]["ALIAS"] for i in ent},
                           {i: ent[i]["SEMREL"] for i in ent})
            rnd_as = [float(np.median([r[i]["ALIAS"] - r[i]["SEMREL"] for i in r]))
                      for r in rnd]
            # selectivity vs the layer-matched random sets, paired per item
            mean_rnd = {i: float(np.mean([r[i]["ALIAS"] - r[i]["SEMREL"] for r in rnd]))
                        for i in ent}
            sel = cluster_boot_median(
                {i: (ent[i]["ALIAS"] - ent[i]["SEMREL"]) - mean_rnd[i] for i in ent})

            ent_all = per_item(keys, blob["dla"][f"ent{frac}"], allit)
            h3_all = boot_diff({i: ent_all[i]["ALIAS"] for i in ent_all},
                               {i: ent_all[i]["SEMREL"] for i in ent_all})

            print(f"  k={k} ({frac:.0%}), {late}/{k} heads in the late third")
            print(f"    dDLA medians   " + "  ".join(
                f"{c}={np.median([ent[i][c] for i in ent]):+.4f}" for c in CONDS))
            print(f"    validity: dDLA_EXACT {ex['median']:+.4f} "
                  f"[{ex['ci_lo']:+.4f},{ex['ci_hi']:+.4f}]  random {ex_r:+.4f}  "
                  f"{'PASS' if valid else 'FAIL'}")
            print(f"    H_repr    ALIAS-SEMREL {h3['median']:+.4f} "
                  f"[{h3['ci_lo']:+.4f},{h3['ci_hi']:+.4f}] "
                  f"{'CI excludes 0' if h3['excludes_zero'] else 'CI includes 0'}"
                  f"   random {np.median(rnd_as):+.4f}")
            print(f"    H_selectivity vs random {sel['median']:+.4f} "
                  f"[{sel['ci_lo']:+.4f},{sel['ci_hi']:+.4f}] "
                  f"{'CI excludes 0' if sel['excludes_zero'] else 'CI includes 0'}")
            print(f"    secondary (all {len(allit)} held-out) ALIAS-SEMREL "
                  f"{h3_all['median']:+.4f} [{h3_all['ci_lo']:+.4f},{h3_all['ci_hi']:+.4f}]")

            # alignment: cos(w_cond - w_NOCTX, w_EXACT - w_NOCTX)
            al = [r for r in blob["align"][f"ent{frac}"] if r["item_id"] in strict]
            byi = defaultdict(lambda: defaultdict(list))
            for r in al:
                for c in ("ALIAS", "SEMREL", "UNREL"):
                    if r[c] == r[c]:
                        byi[r["item_id"]][c].append(r[c])
            am = {c: {i: float(np.mean(v[c])) for i, v in byi.items() if v[c]}
                  for c in ("ALIAS", "SEMREL", "UNREL")}
            algn = boot_diff(am["ALIAS"], am["SEMREL"])
            print(f"    H_align   cos(ALIAS,EXACT) {np.median(list(am['ALIAS'].values())):+.4f}"
                  f"  cos(SEMREL,EXACT) {np.median(list(am['SEMREL'].values())):+.4f}"
                  f"  cos(UNREL,EXACT) {np.median(list(am['UNREL'].values())):+.4f}")
            print(f"              ALIAS-SEMREL {algn['median']:+.4f} "
                  f"[{algn['ci_lo']:+.4f},{algn['ci_hi']:+.4f}] "
                  f"{'CI excludes 0' if algn['excludes_zero'] else 'CI includes 0'}")

            verdict = ("ALIAS-INVARIANT-WRITE"
                       if (valid and h3["median"] > 0 and h3["excludes_zero"]
                           and sel["median"] > 0 and sel["excludes_zero"])
                       else "SEEN-FORM-ONLY-WRITE")
            print(f"    -> {verdict}")
            rows[str(frac)] = dict(k=k, late_heads=late, validity=valid,
                                   dDLA_EXACT=ex, H_repr=h3, H_selectivity=sel,
                                   H_repr_all_items=h3_all, H_align=algn,
                                   align_medians={c: float(np.median(list(v.values())))
                                                  for c, v in am.items()},
                                   verdict=verdict)
        report[tag] = rows
    Path(args.res_dir, "analysis_phase3.json").write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
