"""D1 corpus sanity audit (contract d1-r3 `corpus_sanity_audit`).

The dataset card guarantees cleaned article text but does not state that every
redirect page is dropped. A surviving redirect stub titled with the alias would
hand `alias -> canonical` a fabricated co-occurrence that `ASSOC -> canonical`
can never get, which would bias the decisive test toward ALIAS.

Samples 50 alias surfaces, not one.
"""
from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path

from datasets import load_dataset


def norm_title(t: str) -> str:
    return re.sub(r"\s+", " ", (t or "").replace("_", " ")).strip().lower()


def main() -> None:
    A = json.load(open("data/d1_assoc_candidates.json"))
    ds = load_dataset("wikimedia/wikipedia", "20231101.en", split="train")
    print(f"corpus: {len(ds):,} articles")

    titles = {}
    for i, t in enumerate(ds["title"]):
        titles.setdefault(norm_title(t), i)
    print(f"unique normalised titles: {len(titles):,}")

    rng = random.Random(20260829)
    sample = rng.sample(sorted(A), min(50, len(A)))
    hits = []
    for tgt in sample:
        a = A[tgt]["seen_form"]
        idx = titles.get(norm_title(a))
        if idx is not None:
            hits.append((a, A[tgt]["target_form"], ds[idx]["title"],
                         len(ds[idx]["text"])))
    print(f"\nalias surfaces sampled: {len(sample)}")
    print(f"alias surfaces existing as their own article: {len(hits)}")
    for a, b, t, n in hits:
        print(f"   ALIAS {a!r} -> target {b!r} | article {t!r} ({n} chars)")

    # a canonical title SHOULD exist as an article; that is the control
    ctrl = sum(1 for tgt in sample
               if norm_title(A[tgt]["target_form"]) in titles)
    print(f"\ncontrol -- canonical targets present as articles: {ctrl}/{len(sample)}")
    print("\nVERDICT:", "PASS -- no alias redirect stubs in the corpus" if not hits
          else f"STRIP REQUIRED -- {len(hits)} alias-titled articles must be removed")
    Path("results/d1_build/corpus_audit.json").write_text(json.dumps(
        dict(n_articles=len(ds), sampled=len(sample),
             alias_titled_articles=[h[0] for h in hits],
             canonical_present=ctrl), indent=1))


if __name__ == "__main__":
    main()
