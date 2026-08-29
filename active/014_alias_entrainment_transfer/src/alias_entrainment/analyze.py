"""Frozen analysis for 014 phase 1. Implements configs/contract_r1.yaml verbatim.

Statistical unit is the item (entity x direction); the bootstrap resamples
ENTITIES, because the two directions of one entity are not independent.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from analyze_common import (CONDS, N_BOOT, SEED, capability_gate,
                            cluster_boot_median, entity_of, load_items, per_item_deltas)


def fixed_effect_ols(rows, names=("sim", "orth", "n_tokens", "is_alias")):
    """delta ~ sim + orth + n_tokens + is_alias, with item fixed effects.

    Item fixed effects are absorbed by within-item demeaning, which is exactly
    equivalent to including an item dummy for every item.
    """
    by_item = defaultdict(list)
    for r in rows:
        by_item[r["item_id"]].append(r)
    X, y = [], []
    for _, rs in by_item.items():
        if len(rs) < 2:
            continue
        M = np.array([[float(r[n]) for n in names] for r in rs])
        v = np.array([r["delta"] for r in rs])
        X.append(M - M.mean(0))
        y.append(v - v.mean())
    X, y = np.vstack(X), np.concatenate(y)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = max(len(y) - X.shape[1] - len(by_item), 1)
    xtx_inv = np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.diag(xtx_inv) * (resid @ resid) / dof)
    return {n: dict(beta=float(b), se=float(s), t=float(b / s) if s else float("nan"))
            for n, b, s in zip(names, beta, se)}


def analyze_family(tag: str, res_dir: Path, d0, tok=None) -> dict:
    passed, gate_diag = capability_gate(res_dir / f"{tag}__probe.jsonl")
    deltas, base = per_item_deltas(res_dir / f"{tag}__main.jsonl")

    gated = [i for i in deltas if i in passed]
    rep = dict(tag=tag, gate=gate_diag, n_gated=len(gated))
    rep["capability_floor"] = len(gated) < 60

    def sub(pred=lambda it: True, items=None):
        return [i for i in (items or gated) if pred(d0[i])]

    def contrast(a, b, items):
        return cluster_boot_median({i: deltas[i][a] - deltas[i][b] for i in items})

    S = gated
    rep["H1_replication"] = dict(
        **cluster_boot_median({i: deltas[i]["EXACT"] for i in S}),
        frac_positive=float(np.mean([deltas[i]["EXACT"] > 0 for i in S])))
    rep["H1_pass"] = bool(rep["H1_replication"]["median"] >= 1.0
                          and rep["H1_replication"]["frac_positive"] >= 0.80)

    rep["H2_alias_vs_unrel"] = contrast("ALIAS", "UNREL", S)
    rep["H2_pass"] = bool(rep["H2_alias_vs_unrel"]["median"] > 0
                          and rep["H2_alias_vs_unrel"]["excludes_zero"])

    main3 = contrast("ALIAS", "SEMREL", S)
    matched = sub(lambda it: it["sim_matched"])
    strict = sub(lambda it: it["strict_stratum"] == "opaque_strict")
    rep["H3_alias_vs_semrel"] = main3
    rep["H3_sim_matched"] = contrast("ALIAS", "SEMREL", matched) if matched else None
    rep["H3_opaque_strict"] = contrast("ALIAS", "SEMREL", strict) if strict else None

    reg_rows = []
    for i in S:
        it = d0[i]
        for cond, mention, sim, orth in (
            ("ALIAS", it["seen_form"], it["sim_alias_target"], it["orth_alias_target"]),
            ("SEMREL", it["semrel"], it["sim_semrel_target"], it["orth_semrel_target"]),
            ("UNREL", it["unrel"], it["sim_unrel_target"], it["orth_unrel_target"]),
        ):
            reg_rows.append(dict(item_id=i, delta=deltas[i][cond], sim=sim, orth=orth,
                                 n_tokens=(len(tok.encode(mention, add_special_tokens=False))
                                           if tok else len(mention.split())),
                                 is_alias=(cond == "ALIAS")))
    rep["H3_regression"] = fixed_effect_ols(reg_rows)

    rep["H3_pass"] = bool(
        main3["median"] > 0 and main3["excludes_zero"]
        and rep["H3_sim_matched"] and rep["H3_sim_matched"]["median"] > 0
        and rep["H3_opaque_strict"] and rep["H3_opaque_strict"]["median"] > 0
        and rep["H3_regression"]["is_alias"]["beta"] > 0)

    num = np.median([deltas[i]["ALIAS"] - deltas[i]["SEMREL"] for i in S])
    den = np.median([deltas[i]["EXACT"] - deltas[i]["SEMREL"] for i in S])
    rep["transfer_ratio"] = float(num / den) if den else None
    rep["transfer_ratio_pass"] = bool(rep["transfer_ratio"] is not None
                                      and rep["transfer_ratio"] >= 0.15)

    rep["condition_medians"] = {c: float(np.median([deltas[i][c] for i in S]))
                                for c in CONDS}
    rep["baseline_logprob_median"] = float(np.median(list(base.values())))
    # ---- diagnostics (descriptive; they do not replace any frozen test) -------
    failed = [i for i in deltas if i not in passed]
    diag = {}
    if len(failed) >= 20:
        # The sharpest falsification available from data already collected: if the
        # residual ALIAS-SEMREL gap is just as large where the model CANNOT link
        # the two forms, the gap is not entity-mediated.
        diag["alias_minus_semrel_gate_failed"] = contrast("ALIAS", "SEMREL", failed)
        diag["alias_minus_semrel_gate_passed"] = main3
        strict_f = [i for i in failed if d0[i]["strict_stratum"] == "opaque_strict"]
        if len(strict_f) >= 15:
            diag["opaque_strict_gate_failed"] = contrast("ALIAS", "SEMREL", strict_f)
    for d in ("canon2alias", "alias2canon"):
        sel = sub(lambda it, d=d: it["direction"] == d)
        if len(sel) >= 20:
            diag[f"alias_minus_semrel_{d}"] = contrast("ALIAS", "SEMREL", sel)["median"]
            diag[f"exact_{d}"] = float(np.median([deltas[i]["EXACT"] for i in sel]))
    diag["transfer_ratio_opaque_strict"] = None
    if strict:
        num_s = np.median([deltas[i]["ALIAS"] - deltas[i]["SEMREL"] for i in strict])
        den_s = np.median([deltas[i]["EXACT"] - deltas[i]["SEMREL"] for i in strict])
        diag["transfer_ratio_opaque_strict"] = float(num_s / den_s) if den_s else None
    rep["diagnostics"] = diag

    # Interaction test: does the residual alias effect depend on whether THIS
    # model can actually link the two forms? If the residual were only
    # mis-measured semantic similarity, it would not.
    inter_rows = []
    for i in deltas:
        it = d0[i]
        gp = float(i in passed)
        for cond, mention, sim, orth in (
            ("ALIAS", it["seen_form"], it["sim_alias_target"], it["orth_alias_target"]),
            ("SEMREL", it["semrel"], it["sim_semrel_target"], it["orth_semrel_target"]),
            ("UNREL", it["unrel"], it["sim_unrel_target"], it["orth_unrel_target"]),
        ):
            ia = float(cond == "ALIAS")
            inter_rows.append(dict(item_id=i, delta=deltas[i][cond], sim=sim, orth=orth,
                                   n_tokens=(len(tok.encode(mention, add_special_tokens=False))
                                             if tok else len(mention.split())),
                                   is_alias=ia, alias_x_gate=ia * gp))
    # Secondary metric from the contract: mother-faithful first-token logit delta.
    d2, _ = per_item_deltas(res_dir / f"{tag}__main.jsonl", metric="first_token_logit")
    strict2 = [i for i in gated if d0[i]["strict_stratum"] == "opaque_strict"]
    rep["secondary_first_token_logit"] = dict(
        exact=float(np.median([d2[i]["EXACT"] for i in gated])),
        alias_minus_semrel=cluster_boot_median(
            {i: d2[i]["ALIAS"] - d2[i]["SEMREL"] for i in gated}),
        alias_minus_semrel_opaque_strict=cluster_boot_median(
            {i: d2[i]["ALIAS"] - d2[i]["SEMREL"] for i in strict2}) if strict2 else None)

    rep["gate_interaction"] = fixed_effect_ols(
        inter_rows, names=("sim", "orth", "n_tokens", "is_alias", "alias_x_gate"))

    # Frame locality: mention-initial (F1) vs mention-final, adjacent to the
    # query (F2). An effect confined to F2 would be recency, not entity state.
    rows_all = [json.loads(l) for l in open(res_dir / f"{tag}__main.jsonl", encoding="utf-8")]
    fbase, fcell = {}, defaultdict(list)
    for r in rows_all:
        if r["condition"] == "NOCTX":
            fbase[(r["item_id"], r["qid"])] = r["logprob_sum"]
    for r in rows_all:
        if r["condition"] != "NOCTX":
            fcell[(r["item_id"], r["frame"], r["condition"])].append(
                r["logprob_sum"] - fbase[(r["item_id"], r["qid"])])
    rep["by_frame"] = {}
    for fr in ("F1", "F2"):
        vals, ex = {}, {}
        for i in gated:
            a = fcell.get((i, fr, "ALIAS")); sr = fcell.get((i, fr, "SEMREL"))
            e = fcell.get((i, fr, "EXACT"))
            if a and sr and e:
                vals[i] = float(np.mean(a) - np.mean(sr))
                ex[i] = float(np.mean(e))
        if vals:
            rep["by_frame"][fr] = dict(alias_minus_semrel=cluster_boot_median(vals),
                                       exact=float(np.median(list(ex.values()))))

    rep["by_stratum"] = {}
    for st in ("opaque_strict", "opaque", "partial", "acronym"):
        sel = sub(lambda it, st=st: it["strict_stratum"] == st)
        if len(sel) >= 10:
            rep["by_stratum"][st] = dict(n=len(sel),
                                         alias_minus_semrel=contrast("ALIAS", "SEMREL", sel)["median"],
                                         exact=float(np.median([deltas[i]["EXACT"] for i in sel])))
    return rep


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--res-dir", default="results/phase1_r1")
    ap.add_argument("--d0", default="data/frozen_d0.jsonl")
    ap.add_argument("--tags", nargs="+", required=True)
    ap.add_argument("--tokenizers", nargs="*", default=[])
    args = ap.parse_args()

    d0 = load_items(args.d0)
    res_dir = Path(args.res_dir)
    toks = {}
    if args.tokenizers:
        from transformers import AutoTokenizer
        for tag, mid in zip(args.tags, args.tokenizers):
            toks[tag] = AutoTokenizer.from_pretrained(mid)

    reports = [analyze_family(t, res_dir, d0, toks.get(t)) for t in args.tags]
    (res_dir / "analysis_r1.json").write_text(json.dumps(reports, indent=2))

    for r in reports:
        print("=" * 78)
        print(f"{r['tag']}   gated {r['n_gated']}/{r['gate']['n_items']} items"
              f"   order gap {r['gate']['order_gap']:+.3f}"
              f"   {'CAPABILITY-FLOOR' if r['capability_floor'] else ''}")
        print(f"  condition medians (nats): " +
              "  ".join(f"{c}={r['condition_medians'][c]:+.3f}" for c in CONDS))
        h1 = r["H1_replication"]
        print(f"  H1 EXACT           median {h1['median']:+.3f} "
              f"[{h1['ci_lo']:+.3f},{h1['ci_hi']:+.3f}] frac>0 {h1['frac_positive']:.2f}"
              f"   {'PASS' if r['H1_pass'] else 'FAIL'}")
        for key, label in (("H2_alias_vs_unrel", "H2 ALIAS-UNREL "),
                           ("H3_alias_vs_semrel", "H3 ALIAS-SEMREL"),
                           ("H3_sim_matched", "   sim-matched "),
                           ("H3_opaque_strict", "   opaque-strict")):
            v = r[key]
            if v:
                print(f"  {label:<18} median {v['median']:+.3f} "
                      f"[{v['ci_lo']:+.3f},{v['ci_hi']:+.3f}] n={v['n_items']}"
                      f"  {'CI excludes 0' if v['excludes_zero'] else 'CI includes 0'}")
        reg = r["H3_regression"]
        print("  regression (item FE): " + "  ".join(
            f"{k}={v['beta']:+.3f}(t={v['t']:+.2f})" for k, v in reg.items()))
        print(f"  transfer ratio {r['transfer_ratio']}"
              f"   H1 {r['H1_pass']}  H2 {r['H2_pass']}  H3 {r['H3_pass']}")
        d = r.get("diagnostics", {})
        if "alias_minus_semrel_gate_failed" in d:
            g, b = d["alias_minus_semrel_gate_passed"], d["alias_minus_semrel_gate_failed"]
            print(f"  DIAG gate passed  ALIAS-SEMREL {g['median']:+.3f} (n={g['n_items']})"
                  f"   gate FAILED {b['median']:+.3f} (n={b['n_items']}) "
                  f"[{b['ci_lo']:+.3f},{b['ci_hi']:+.3f}]")
        if "opaque_strict_gate_failed" in d:
            v = d["opaque_strict_gate_failed"]
            print(f"  DIAG opaque-strict, gate FAILED {v['median']:+.3f} "
                  f"[{v['ci_lo']:+.3f},{v['ci_hi']:+.3f}] n={v['n_items']}")
        if "alias_minus_semrel_canon2alias" in d:
            print(f"  DIAG direction canon->alias {d['alias_minus_semrel_canon2alias']:+.3f}"
                  f"  alias->canon {d['alias_minus_semrel_alias2canon']:+.3f}"
                  f"  | transfer ratio (opaque_strict) {d['transfer_ratio_opaque_strict']}")
        s2 = r.get("secondary_first_token_logit")
        if s2:
            m, o = s2["alias_minus_semrel"], s2["alias_minus_semrel_opaque_strict"]
            print(f"  SECONDARY (first-token logit) EXACT {s2['exact']:+.3f}"
                  f"   ALIAS-SEMREL {m['median']:+.3f} [{m['ci_lo']:+.3f},{m['ci_hi']:+.3f}]"
                  + (f"   opaque-strict {o['median']:+.3f} [{o['ci_lo']:+.3f},{o['ci_hi']:+.3f}]"
                     if o else ""))
        gi = r.get("gate_interaction")
        if gi:
            print("  GATE-INTERACTION: " + "  ".join(
                f"{k}={v['beta']:+.3f}(t={v['t']:+.2f})" for k, v in gi.items()))
        for fr, v in r.get("by_frame", {}).items():
            m = v["alias_minus_semrel"]
            print(f"  FRAME {fr}  ALIAS-SEMREL {m['median']:+.3f} "
                  f"[{m['ci_lo']:+.3f},{m['ci_hi']:+.3f}]   EXACT {v['exact']:+.3f}")
        if r["by_stratum"]:
            print("  by stratum (ALIAS-SEMREL median): " + "  ".join(
                f"{k}={v['alias_minus_semrel']:+.3f}(n={v['n']})"
                for k, v in r["by_stratum"].items()))

    n_h3 = sum(r["H3_pass"] for r in reports if not r["capability_floor"])
    print("=" * 78)
    print(f"H4 consistency: H3 passes in {n_h3} / {len(reports)} families")


if __name__ == "__main__":
    main()
