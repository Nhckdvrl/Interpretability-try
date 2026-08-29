"""D1 r4 corpus sanity audit.

Checks that alias/redirect surfaces are not represented by redirect stub articles
in the pinned cleaned Wikipedia corpus.  The audit samples surface PAIRS across
the broad bank rather than assuming the old target-keyed person-only JSON shape.

Canonical contract: configs/contract_d1_r4.yaml
"""
from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path

from datasets import load_dataset


def norm_title(t: str) -> str:
    return re.sub(r"\s+", " ", (t or "").replace("_", " ")).strip().casefold()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cands", default="data/d1_surface_pairs_r4.json")
    ap.add_argument("--sample", type=int, default=50)
    ap.add_argument("--out", default="results/d1_build/corpus_audit_r4.json")
    args = ap.parse_args()

    A = json.load(open(args.cands))
    ds = load_dataset("wikimedia/wikipedia", "20231101.en", split="train")
    print(f"corpus: {len(ds):,} articles")

    titles = {}
    for i, t in enumerate(ds["title"]):
        titles.setdefault(norm_title(t), i)
    print(f"unique normalised titles: {len(titles):,}")

    rng = random.Random(20260829)
    sample = rng.sample(A, min(args.sample, len(A)))
    hits = []
    for rec in sample:
        a, b = rec["seen_form"], rec["target_form"]
        idx = titles.get(norm_title(a))
        if idx is not None:
            hits.append(dict(
                pair_id=rec["pair_id"], alias=a, target=b,
                article_title=ds[idx]["title"], text_chars=len(ds[idx]["text"]),
            ))
    print(f"\nalias surfaces sampled: {len(sample)}")
    print(f"alias surfaces existing as their own article: {len(hits)}")
    for h in hits:
        print(f"   ALIAS {h['alias']!r} -> {h['target']!r} | "
              f"article {h['article_title']!r} ({h['text_chars']} chars)")

    ctrl = sum(1 for rec in sample if norm_title(rec["target_form"]) in titles)
    print(f"\ncontrol -- canonical targets present as articles: {ctrl}/{len(sample)}")
    verdict = "PASS -- no alias redirect stubs in sample" if not hits \
        else f"STRIP/INVESTIGATE -- {len(hits)} alias-titled articles found"
    print("\nVERDICT:", verdict)
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(dict(
        version="d1-r4", n_articles=len(ds), sampled=len(sample),
        alias_titled_articles=hits, canonical_present=ctrl, verdict=verdict,
    ), indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
