"""D1 stage 1: select candidate entities and alias forms from RedirectQA.

Implements contract_d1.yaml + amendment d1-r2. No model is called here and no
ASSOC is chosen yet -- this only fixes WHICH entities and WHICH single redirect
form per entity enter the primary cell, so the corpus co-occurrence pass has a
bounded string set to count.

Statistical unit: subject_id x ONE selected redirect form.
Primary direction: seen = redirect alias -> target = canonical wiki title.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_d0 import ASCII_OK, good_pair, is_compositional, norm, strict_stratum  # noqa

PRIMARY_ALLOWED = [
    "Redirects_from_birth_names",
    "Redirects_from_pseudonyms",
    "Redirects_from_former_names",
    "Redirects_from_alternative_names",
]
# everything else that is a real category is excluded; `__MAIN__` marks the
# canonical surface and is not a redirect at all
EXCLUDED = {
    "Redirects_from_abbreviations", "Redirects_from_initialisms",
    "Redirects_from_acronyms", "Redirects_to_initialisms", "Redirects_to_acronyms",
    "Redirects_from_letter–word_combinations", "Redirects_from_numerals",
    "Redirects_from_short_names", "Redirects_from_long_names",
    "Redirects_from_surnames", "Redirects_from_given_names",
    "Redirects_from_personal_names", "Redirects_from_married_names",
    "Redirects_from_titles_with_diacritics", "Redirects_from_titles_without_diacritics",
    "Redirects_from_titles_without_ligatures", "Redirects_from_ASCII-only_titles",
    "Redirects_to_ASCII-only_titles", "Redirects_from_alternative_spellings",
    "Redirects_from_misspellings", "Redirects_from_incorrect_names",
    "Redirects_from_miscapitalisations", "Redirects_from_other_capitalisations",
    "Redirects_from_stylizations", "Redirects_from_modifications",
    "Redirects_from_technical_names", "Redirects_from_plurals",
    "Redirects_to_plurals", "Redirects_from_synonyms",
}
CATEGORY_PRIORITY = {c: i for i, c in enumerate(PRIMARY_ALLOWED)}


def clean_title(t: str) -> str:
    return re.sub(r"\s*\(.*?\)\s*$", "", (t or "").replace("_", " ")).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/d1_candidates.json")
    ap.add_argument("--min-pageviews", type=int, default=5000)
    args = ap.parse_args()

    from datasets import load_dataset
    ds = load_dataset("naist-nlp/RedirectQA", split="test")
    print(f"RedirectQA rows: {len(ds)}")

    # one record per (subject_id, redirect surface); rows repeat it across
    # triples and the two question templates
    surf: dict[tuple[str, str], dict] = {}
    canon: dict[str, str] = {}
    for r in ds:
        sid, s = r["subject_id"], r["subject_surface"]
        cats = list(r["subject_surface_category"] or [])
        if "__MAIN__" in cats:
            canon.setdefault(sid, r["subject_wiki_title"])
            continue
        key = (sid, s)
        if key not in surf:
            surf[key] = dict(subject_id=sid, surface=s, cats=set(),
                             pageviews=r["subject_pageviews"],
                             wiki_title=r["subject_wiki_title"],
                             redirect_title=r["subject_redirect_wiki_title"],
                             aliases=set(r["subject_aliases"] or []))
        surf[key]["cats"].update(cats)
    print(f"unique (subject_id, redirect surface): {len(surf)}  "
          f"subjects with a canonical row: {len(canon)}")

    # multi-label rule: >=1 allowed primary label AND no excluded label
    kept = defaultdict(list)
    reasons = defaultdict(int)
    for (sid, s), rec in surf.items():
        cats = rec["cats"]
        target = clean_title(canon.get(sid) or rec["wiki_title"])
        if not (cats & set(PRIMARY_ALLOWED)):
            reasons["no allowed primary label"] += 1; continue
        if cats & EXCLUDED:
            reasons["carries an excluded label"] += 1; continue
        if not target or not s:
            reasons["missing surface or title"] += 1; continue
        if (rec["pageviews"] or 0) < args.min_pageviews:
            reasons["below pageview floor"] += 1; continue
        if not (ASCII_OK.match(s) and ASCII_OK.match(target)):
            reasons["non-ascii"] += 1; continue
        if not good_pair(s, target):
            reasons["substring / too short / too long"] += 1; continue
        if is_compositional(s, target):
            reasons["compositional (derivable)"] += 1; continue
        kept[sid].append(dict(subject_id=sid, seen_form=s, target_form=target,
                              cats=sorted(cats), pageviews=rec["pageviews"],
                              stratum=strict_stratum(s, target),
                              aliases=sorted(rec["aliases"] | {s, target})))
    print("\nfiltered out:")
    for k, v in sorted(reasons.items(), key=lambda x: -x[1]):
        print(f"  {v:>6}  {k}")

    # exactly ONE redirect form per entity: category priority, then deterministic
    final = []
    for sid, cands in sorted(kept.items()):
        cands.sort(key=lambda c: (min(CATEGORY_PRIORITY[x] for x in c["cats"]
                                      if x in CATEGORY_PRIORITY),
                                  len(c["seen_form"]), c["seen_form"]))
        final.append(cands[0])
    print(f"\nentities with >=1 usable redirect: {len(kept)}")
    print(f"D1 primary candidates (one per entity): {len(final)}")
    from collections import Counter
    print("  by primary category:",
          dict(Counter(c["cats"][0] for c in final).most_common()))
    print("  by stratum:", dict(Counter(c["stratum"] for c in final)))

    Path(args.out).write_text(json.dumps(final, indent=1))
    print(f"\nwrote {args.out}")
    for c in final[:12]:
        print(f"   {c['seen_form']!r:<32} -> {c['target_form']!r:<28} "
              f"{[x.replace('Redirects_from_','') for x in c['cats']]}")


if __name__ == "__main__":
    main()
