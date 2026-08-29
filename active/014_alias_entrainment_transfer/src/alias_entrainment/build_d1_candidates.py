"""D1 r4 stage 1: extract the BROAD RedirectQA surface-pair bank.

The earlier r2 builder accidentally changed the research question by keeping
only four lexical-alias categories, dropping compositional/orthographic forms,
requiring ASCII, and selecting exactly one redirect per entity.  The project is
about cross-SURFACE entrainment, so those are analysis factors, not construction
filters.

r4 keeps every unique (subject_id, redirect surface), attaches RedirectQA's own
high-level category, and labels surface structure.  Typical_Errors are retained
for diagnostics; Aliases_and_Abbreviations + Spelling_variants form the intended
confirmatory surface population.  No model is called here.

Canonical contract: configs/contract_d1_r4.yaml
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

CONFIRMATORY_TYPES = {"Aliases_and_Abbreviations", "Spelling_variants"}


def clean_title(t: str) -> str:
    return re.sub(r"\s*\(.*?\)\s*$", "", (t or "").replace("_", " ")).strip()


def normu(s: str) -> str:
    """Unicode-aware comparison normalisation; D0's ASCII norm is not reused."""
    s = unicodedata.normalize("NFKC", s or "").casefold()
    return "".join(ch for ch in s if ch.isalnum())


def tokens_u(s: str) -> list[str]:
    # Python \w is Unicode-aware. Strip underscore because names do not use it as
    # a lexical identity cue here.
    return [x.casefold() for x in re.findall(r"[^\W_]+", unicodedata.normalize("NFKC", s or ""))]


def words_u(s: str) -> set[str]:
    return set(tokens_u(s))


def is_derivable(a: str, b: str) -> bool:
    """Surface-derivable, not 'short'.  This is a LABEL, never an exclusion."""
    wa, wb = tokens_u(a), tokens_u(b)
    if not wa or not wb:
        return False
    sa, sb = normu(a), normu(b)
    # Initialisms/acronyms in either direction.
    ia = "".join(w[0] for w in wa if w)
    ib = "".join(w[0] for w in wb if w)
    if (sa and sa == ib) or (sb and sb == ia):
        return True
    # One form is literally a subset of the other's words (short/full name).
    swa, swb = set(wa), set(wb)
    if swa < swb or swb < swa:
        return True
    # Aligned truncations: Rob/Robert, Steve/Steven, etc.
    if len(wa) == len(wb) and wa != wb and all(
            x.startswith(y) or y.startswith(x) for x, y in zip(wa, wb)):
        return True
    return False


def structural_stratum(a: str, b: str) -> str:
    if is_derivable(a, b):
        return "compositional"
    if words_u(a) & words_u(b):
        return "partial"
    sim = SequenceMatcher(None, normu(a), normu(b)).ratio()
    return "opaque_strict" if sim < 0.40 else "opaque"


def load_category_map() -> dict[str, str]:
    """Use RedirectQA's metadata, never a hand-maintained four-label whitelist."""
    from huggingface_hub import hf_hub_download
    p = hf_hub_download(
        repo_id="naist-nlp/RedirectQA",
        repo_type="dataset",
        filename="metadata/redirect_category_to_type.csv",
    )
    with open(p, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames or []
        cat_key = next((k for k in fields if "category" in k.casefold()), None)
        type_key = next((k for k in fields if "type" in k.casefold() and k != cat_key), None)
        if not cat_key or not type_key:
            raise RuntimeError(f"Unexpected RedirectQA category metadata columns: {fields}")
        out = {}
        for r in rd:
            cat, typ = (r.get(cat_key) or "").strip(), (r.get(type_key) or "").strip()
            if cat:
                out[cat] = typ
    if not out:
        raise RuntimeError("RedirectQA category metadata was empty")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/d1_surface_pairs_r4.json")
    args = ap.parse_args()

    from datasets import load_dataset
    ds = load_dataset("naist-nlp/RedirectQA", split="test")
    cat2type = load_category_map()
    print(f"RedirectQA rows: {len(ds)}; category metadata: {len(cat2type)} labels")

    # Rows repeat surfaces across factual triples and two templates.  Preserve all
    # distinct redirect surfaces, but deduplicate those repeated realizations.
    surf: dict[tuple[str, str], dict] = {}
    canon: dict[str, str] = {}
    for r in ds:
        sid, s = r["subject_id"], r["subject_surface"]
        cats = list(r["subject_surface_category"] or [])
        if "__MAIN__" in cats:
            canon.setdefault(sid, clean_title(r["subject_wiki_title"]))
            continue
        key = (sid, s)
        rec = surf.setdefault(key, dict(
            subject_id=sid,
            surface=s,
            cats=set(),
            pageviews=r["subject_pageviews"],
            wiki_title=r["subject_wiki_title"],
            redirect_titles=set(),
            aliases=set(),
            triplet_ids=set(),
        ))
        rec["cats"].update(cats)
        if r.get("subject_redirect_wiki_title"):
            rec["redirect_titles"].add(r["subject_redirect_wiki_title"])
        rec["aliases"].update(r["subject_aliases"] or [])
        rec["triplet_ids"].add(int(r["triplet_id"]))
        rec["pageviews"] = max(rec["pageviews"] or 0, r["subject_pageviews"] or 0)

    print(f"unique (subject_id, redirect surface): {len(surf)}")

    rows, drop = [], Counter()
    unknown_cats = Counter()
    for (sid, s), rec in sorted(surf.items()):
        target = canon.get(sid) or clean_title(rec["wiki_title"])
        if not s or not target:
            drop["missing surface/title"] += 1
            continue
        if len(normu(s)) < 2 or len(normu(target)) < 2:
            drop["degenerate <2 alnum chars"] += 1
            continue
        if normu(s) == normu(target):
            drop["normalises to canonical"] += 1
            continue

        cats = sorted(rec["cats"])
        high_types = sorted({cat2type[c] for c in cats if c in cat2type and cat2type[c]})
        for c in cats:
            if c not in cat2type:
                unknown_cats[c] += 1
        intended = bool(set(high_types) & CONFIRMATORY_TYPES)
        error_only = bool(high_types) and set(high_types) <= {"Typical_Errors"}
        pair_hash = hashlib.sha1(
            (sid + "\0" + unicodedata.normalize("NFKC", s).casefold()).encode("utf-8")
        ).hexdigest()[:12]
        rows.append(dict(
            pair_id=f"{sid}::{pair_hash}",
            subject_id=sid,
            seen_form=s,
            target_form=target,
            cats=cats,
            redirect_high_types=high_types,
            confirmatory_intended_surface=intended,
            typical_error_only=error_only,
            pageviews=rec["pageviews"] or 0,
            structural_stratum=structural_stratum(s, target),
            orth_sim=SequenceMatcher(None, normu(s), normu(target)).ratio(),
            aliases=sorted(rec["aliases"] | {s, target}),
            redirect_titles=sorted(rec["redirect_titles"]),
            triplet_ids=sorted(rec["triplet_ids"]),
        ))

    Path(args.out).write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    print(f"\nwrote {args.out}")
    print(f"surface pairs: {len(rows)} across {len({r['subject_id'] for r in rows})} entities")
    print("by RedirectQA high-level type:",
          dict(Counter(t for r in rows for t in (r["redirect_high_types"] or ["UNKNOWN"])).most_common()))
    print("by structural stratum:", dict(Counter(r["structural_stratum"] for r in rows)))
    print("confirmatory intended surfaces:", sum(r["confirmatory_intended_surface"] for r in rows))
    print("Typical_Errors-only diagnostics:", sum(r["typical_error_only"] for r in rows))
    if unknown_cats:
        print("WARNING unknown categories:", dict(unknown_cats))
    for k, v in drop.most_common():
        print(f"dropped {v:>5} {k}")


if __name__ == "__main__":
    main()
