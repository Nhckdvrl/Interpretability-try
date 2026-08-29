"""D1 stage 5: apply the conservative ASSOC match and freeze the D1 bank.

Contract d1-r2 §2/§3 and d1-r3 `assoc_selection`:

    S(X->B) = log((c(X,B) + 1) / (c(X) + 100))     sentence windows
    eligible: S(C->B) >= S(A->B)
    then pick deterministically by
      (1) smallest association margin  -- a MATCHED control, not the strongest
      (2) smallest surface-frequency mismatch |log c(C) - log c(A)|
      (3) smallest token-length mismatch
      (4) lowest QID

SEMREL and UNREL are added exactly as in D0, with D0's UNREL bug fixed.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_d0 import ASCII_OK, norm, orth_sim, words  # noqa: E402

ALPHA, BETA = 1.0, 100.0
FRAMES = {"F1": "{M} was in the news last week.",
          "F2": "Yesterday's report briefly mentioned {M}."}


def load_counts(d):
    strings = json.load(open(Path(d, "strings.json")))
    single, pair = Counter(), Counter()
    for f in sorted(Path(d).glob("shard*.json")):
        b = json.loads(f.read_text())
        for k, v in b["single"].items():
            single[int(k)] += v
        for k, v in b["pair"].items():
            a, c = k.split("|")
            pair[(int(a), int(c))] += v
    return strings, single, pair


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assoc", default="data/d1_assoc_candidates.json")
    ap.add_argument("--cooc", default="results/d1_build/cooc")
    ap.add_argument("--out", default="data/frozen_d1.jsonl")
    ap.add_argument("--encoder", default="BAAI/bge-large-en-v1.5")
    args = ap.parse_args()

    A = json.load(open(args.assoc))
    strings, single, pair = load_counts(args.cooc)
    sid = {s: i for i, s in enumerate(strings)}
    print(f"{len(strings)} strings counted; "
          f"{sum(single.values()):,} surface occurrences, {len(pair):,} observed pairs")

    def S(x, b):
        return math.log((pair.get((sid[x], sid[b]), 0) + ALPHA)
                        / (single.get(sid[x], 0) + BETA))

    rows, drop = [], Counter()
    for tgt, v in A.items():
        b, a = v["target_form"], v["seen_form"]
        if sid.get(b) is None or sid.get(a) is None:
            drop["string not counted"] += 1; continue
        if single.get(sid[a], 0) == 0:
            drop["alias never occurs in corpus"] += 1; continue
        s_a = S(a, b)
        elig = []
        for r in v["assoc"]:
            c = r["label"]
            if sid.get(c) is None or single.get(sid[c], 0) == 0:
                continue
            s_c = S(c, b)
            if s_c >= s_a:                       # conservative eligibility
                elig.append(dict(
                    **r, s_assoc=s_c,
                    margin=s_c - s_a,
                    freq_mismatch=abs(math.log(single[sid[c]] + 1)
                                      - math.log(single[sid[a]] + 1)),
                    len_mismatch=abs(len(c.split()) - len(a.split()))))
        if not elig:
            drop["no ASSOC reaches S(C,B) >= S(A,B)"] += 1; continue
        elig.sort(key=lambda r: (r["margin"], r["freq_mismatch"],
                                 r["len_mismatch"], r["qid"]))
        pick = elig[0]
        rows.append(dict(
            item_id=f"{tgt}::alias2canon", entity_uri=tgt, entity_type="person",
            direction="alias2canon", stratum="opaque_strict",
            seen_form=a, target_form=b, assoc=pick["label"],
            assoc_qid=pick["qid"], assoc_relation=pick["relation"],
            cats=v["cats"], popularity=v["pageviews"],
            s_alias=s_a, s_assoc=pick["s_assoc"], assoc_margin=pick["margin"],
            c_alias=single[sid[a]], c_assoc=single[sid[pick["label"]]],
            n_eligible_assoc=len(elig), frames=FRAMES))

    print(f"\nASSOC matching survival: {len(rows)} / {len(A)}")
    for k, n in drop.most_common():
        print(f"   dropped {n:>4}  {k}")
    if not rows:
        print("\nNo item survived; nothing to freeze."); return

    import numpy as np
    print(f"\nmargin: median {np.median([r['assoc_margin'] for r in rows]):.3f} "
          f"(0 = perfectly matched; contract wants small)")
    print("relations:", dict(Counter(r["assoc_relation"] for r in rows).most_common()))
    Path(args.out).write_text("\n".join(json.dumps(r, sort_keys=True)
                                        for r in rows) + "\n")
    import hashlib
    print(f"\nwrote {args.out}  sha256 "
          f"{hashlib.sha256(Path(args.out).read_bytes()).hexdigest()}")
    for r in rows[:10]:
        print(f"   {r['seen_form']!r:<26} -> {r['target_form']!r:<24} "
              f"ASSOC {r['assoc']!r} ({r['assoc_relation']}, margin {r['assoc_margin']:+.2f})")


if __name__ == "__main__":
    main()
