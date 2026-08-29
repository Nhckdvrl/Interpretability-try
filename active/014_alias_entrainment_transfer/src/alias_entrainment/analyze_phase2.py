"""Phase-2 analysis for 014. Implements the `phase2` block of contract_r1.yaml."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

N_BOOT = 10000
SEED = 20260829


def entity_of(item_id):
    return item_id.split("::")[0]


def unpack(d):
    out = defaultdict(dict)
    for key, v in d.items():
        iid, cond = key.split("|")
        out[iid][cond] = v
    return dict(out)


def ratios(clean, abl, items):
    """retain_exact, retain_alias for one item set."""
    e_c = np.median([clean[i]["EXACT"] for i in items])
    e_a = np.median([abl[i]["EXACT"] for i in items])
    a_c = np.median([clean[i]["ALIAS"] - clean[i]["SEMREL"] for i in items])
    a_a = np.median([abl[i]["ALIAS"] - abl[i]["SEMREL"] for i in items])
    return (e_a / e_c if e_c else np.nan), (a_a / a_c if a_c else np.nan)


def boot_selectivity(clean, abl, items, n_boot=N_BOOT, seed=SEED):
    by_ent = defaultdict(list)
    for i in items:
        by_ent[entity_of(i)].append(i)
    ents = sorted(by_ent)
    rng = np.random.default_rng(seed)
    re_o, ra_o = ratios(clean, abl, items)
    vals = np.empty(n_boot)
    idx = rng.integers(0, len(ents), size=(n_boot, len(ents)))
    pools = [by_ent[e] for e in ents]
    for b in range(n_boot):
        samp = [i for j in idx[b] for i in pools[j]]
        re_b, ra_b = ratios(clean, abl, samp)
        vals[b] = ra_b - re_b
    lo, hi = np.percentile(vals[np.isfinite(vals)], [2.5, 97.5])
    # separate CIs for each retained fraction, so it is visible which term is
    # imprecise when the selectivity interval is wide
    re_b = np.empty(n_boot); ra_b = np.empty(n_boot)
    for b in range(n_boot):
        samp = [i for j in idx[b] for i in pools[j]]
        re_b[b], ra_b[b] = ratios(clean, abl, samp)

    def ci(a):
        a = a[np.isfinite(a)]
        return [float(x) for x in np.percentile(a, [2.5, 97.5])]

    return dict(retain_exact=float(re_o), retain_alias=float(ra_o),
                selectivity=float(ra_o - re_o), ci_lo=float(lo), ci_hi=float(hi),
                excludes_zero=bool(lo > 0 or hi < 0),
                retain_exact_ci=ci(re_b), retain_alias_ci=ci(ra_b))


def verdict(sel):
    s, lo, hi = sel["selectivity"], sel["ci_lo"], sel["ci_hi"]
    if abs(s) <= 0.25 and lo <= 0 <= hi:
        return "mechanism_B_shared_entity_representation"
    if s > 0.25 and lo > 0:
        return "mechanism_C_two_pathways"
    if s < -0.25 and hi < 0:
        return "mechanism_A_prime_alias_downstream"
    return "INDETERMINATE"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--res-dir", default="results/phase2_r1")
    ap.add_argument("--tags", nargs="+", required=True)
    args = ap.parse_args()

    report = {}
    for tag in args.tags:
        blob = json.loads((Path(args.res_dir) / f"{tag}__ablate.json").read_text())
        D = {k: unpack(v) for k, v in blob["deltas"].items()}
        items = [i for i in blob.get("eval_items_strict", blob["eval_items"])
                 if i in D["clean"]]
        items_all = [i for i in blob["eval_items"] if i in D["clean"]]
        clean = D["clean"]
        total = blob["n_heads_total"]
        print("=" * 78)
        print(f"{tag}   {len(items)} evaluation items (opaque_strict x gate-passed), "
              f"{total} heads")
        print(f"  clean: EXACT {np.median([clean[i]['EXACT'] for i in items]):+.3f}   "
              f"ALIAS-SEMREL "
              f"{np.median([clean[i]['ALIAS'] - clean[i]['SEMREL'] for i in items]):+.3f}")
        rows = {}
        for frac in blob["topk_frac"]:
            k = max(1, round(total * frac))
            sel = boot_selectivity(clean, D[f"top{frac}"], items)
            rand = [ratios(clean, D[key], items)
                    for key in D if key.startswith(f"rand{frac}_")]
            r_ex = float(np.mean([r[0] for r in rand]))
            r_al = float(np.mean([r[1] for r in rand]))
            valid = sel["retain_exact"] <= 0.70 and sel["retain_exact"] < r_ex - 0.05
            rows[f"{frac}"] = dict(k=k, **sel, rand_retain_exact=r_ex,
                                   rand_retain_alias=r_al,
                                   validity_gate=bool(valid), verdict=verdict(sel))
            print(f"  k={k:>4} ({frac:>5.0%})  "
                  f"retain_EXACT {sel['retain_exact']:.3f} "
                  f"[{sel['retain_exact_ci'][0]:.2f},{sel['retain_exact_ci'][1]:.2f}] "
                  f"(rand {r_ex:.3f})   "
                  f"retain_ALIAS {sel['retain_alias']:.3f} "
                  f"[{sel['retain_alias_ci'][0]:.2f},{sel['retain_alias_ci'][1]:.2f}] "
                  f"(rand {r_al:.3f})")
            print(f"{'':>16}selectivity {sel['selectivity']:+.3f} "
                  f"[{sel['ci_lo']:+.3f},{sel['ci_hi']:+.3f}]   "
                  f"validity {'PASS' if valid else 'FAIL'}   -> {verdict(sel)}")
        # secondary, better powered, but not confound-free (amendment r2a)
        if len(items_all) > len(items):
            print(f"  -- secondary: all {len(items_all)} held-out gate-passed items --")
            for frac in blob["topk_frac"]:
                sel = boot_selectivity(clean, D[f"top{frac}"], items_all)
                rows[f"{frac}"]["secondary_all_items"] = sel
                print(f"  k={max(1, round(total * frac)):>4} ({frac:>5.0%})  "
                      f"retain_EXACT {sel['retain_exact']:.3f}  "
                      f"retain_ALIAS {sel['retain_alias']:.3f}  "
                      f"selectivity {sel['selectivity']:+.3f} "
                      f"[{sel['ci_lo']:+.3f},{sel['ci_hi']:+.3f}]")
        report[tag] = rows
    Path(args.res_dir, "analysis_phase2.json").write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
