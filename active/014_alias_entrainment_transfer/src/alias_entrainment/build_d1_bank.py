"""D1 r4 stage 5: match ASSOC controls and freeze the ordered evaluation bank.

This replaces the pre-r4 implementation that hard-coded every output row as
person/opaque_strict/alias2canon and claimed to add SEMREL/UNREL without doing
so.  r4 preserves each pair's true metadata, constructs every valid direction,
and selects both ASSOC_ANY (primary) and ASSOC_SAMETYPE (sensitivity).

The RAW source population is data/d1_surface_pairs_r4.json.  A pair/direction can
fail matching here without disappearing from that population; drop counts are
part of the build report.

Canonical contract: configs/contract_d1_r4.yaml
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import unicodedata
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

from build_d1_candidates import normu, tokens_u
from count_cooccurrence import COOC_VERSION

ALPHA, BETA = 1.0, 100.0
FRAMES = {
    "F1": "{M} was in the news last week.",
    "F2": "Yesterday's report briefly mentioned {M}.",
}


def load_counts(d):
    root = Path(d)
    meta = json.loads((root / "strings.json").read_text())
    if meta.get("version") != COOC_VERSION:
        raise RuntimeError(
            f"cooc version {meta.get('version')!r} != required {COOC_VERSION!r}; "
            "old pre-fix shards are forbidden"
        )
    patterns = meta["patterns"]
    single, pair = Counter(), Counter()
    shards = sorted(root.glob("shard*.json"))
    if not shards:
        raise RuntimeError(f"no cooccurrence shards in {root}")
    for f in shards:
        b = json.loads(f.read_text())
        if b.get("version") != COOC_VERSION:
            raise RuntimeError(f"stale/mixed shard {f}: {b.get('version')!r}")
        for k, v in b["single"].items():
            single[int(k)] += v
        for k, v in b["pair"].items():
            a, c = k.split("|")
            pair[(int(a), int(c))] += v
    return patterns, single, pair


def surface_occurs_in(needle: str, haystack: str) -> bool:
    """Would the scored target surface literally already occur in the mention?"""
    n = unicodedata.normalize("NFKC", needle).casefold().strip()
    h = unicodedata.normalize("NFKC", haystack).casefold()
    return bool(n) and n in h


def target_tokens(s: str) -> set[str]:
    # Exact scored-name tokens of length >=2.  If ASSOC contains one of these it
    # can receive direct lexical entrainment rather than serving as an association
    # control.  One-character particles are ignored.
    return {t for t in tokens_u(s) if len(t) >= 2}


def orth_sim_u(a: str, b: str) -> float:
    return SequenceMatcher(None, normu(a), normu(b)).ratio()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assoc", default="data/d1_assoc_candidates_r4.json")
    ap.add_argument("--cooc", default="results/d1_build/cooc_r4")
    ap.add_argument("--out", default="data/frozen_d1_r4.jsonl")
    args = ap.parse_args()

    A = json.load(open(args.assoc))
    patterns, single, pair = load_counts(args.cooc)
    sid = {s: i for i, s in enumerate(patterns)}
    print(f"{len(A)} raw surface pairs; {len(patterns)} counted strings; "
          f"{sum(single.values()):,} surface-sentence hits")

    def S(x, b):
        if x not in sid or b not in sid:
            return None
        return math.log((pair.get((sid[x], sid[b]), 0) + ALPHA)
                        / (single.get(sid[x], 0) + BETA))

    def choose_assoc(v, seen, target, same_type_only=False):
        s_seen = S(seen, target)
        if s_seen is None or single.get(sid.get(seen, -1), 0) == 0:
            return None, "seen surface never occurs in corpus"
        ttok = target_tokens(target)
        elig = []
        for r in v.get("assoc", []):
            if same_type_only and not r.get("same_type"):
                continue
            c = r["label"]
            if c not in sid or single.get(sid[c], 0) == 0:
                continue
            # Direction-specific leakage only.  Do NOT globally ban a relative's
            # overlap with the non-scored alias/canonical form.
            if ttok & target_tokens(c):
                continue
            s_c = S(c, target)
            joint_c_target = pair.get((sid[c], sid[target]), 0)
            # Smoothing prevents infinities; it must not turn two zero-joint
            # pairs into evidence for a strong learned association control.
            if s_c is None or joint_c_target < 1 or s_c < s_seen:
                continue
            elig.append(dict(
                **r,
                s_assoc=s_c,
                joint_assoc_target=joint_c_target,
                margin=s_c - s_seen,
                freq_mismatch=abs(math.log(single[sid[c]] + 1)
                                  - math.log(single[sid[seen]] + 1)),
                len_mismatch=abs(len(tokens_u(c)) - len(tokens_u(seen))),
                orth_mismatch=abs(orth_sim_u(c, target) - orth_sim_u(seen, target)),
            ))
        if not elig:
            return None, "no ASSOC reaches S(C,target) >= S(seen,target) without target-token leakage"
        elig.sort(key=lambda r: (
            r["margin"], r["freq_mismatch"], r["len_mismatch"],
            r["orth_mismatch"], r["qid"],
        ))
        return elig[0], None

    rows, drop = [], Counter()
    pair_survival = defaultdict(set)
    for v in A:
        alias, canon = v["seen_form"], v["target_form"]
        directions = [
            ("alias_to_canonical", alias, canon),
            ("canonical_to_alias", canon, alias),
        ]
        for direction, seen, target in directions:
            if surface_occurs_in(target, seen):
                drop[f"{direction}: target surface already occurs in seen surface"] += 1
                continue
            pick, why = choose_assoc(v, seen, target, same_type_only=False)
            if pick is None:
                drop[f"{direction}: {why}"] += 1
                continue
            pick_same, _ = choose_assoc(v, seen, target, same_type_only=True)
            s_seen = S(seen, target)
            row = dict(
                item_id=f"{v['pair_id']}::{direction}",
                pair_id=v["pair_id"],
                entity_uri=v["subject_id"],
                entity_type=v.get("entity_type", "other"),
                direction=direction,
                structural_stratum=v["structural_stratum"],
                redirect_high_types=v.get("redirect_high_types", []),
                cats=v.get("cats", []),
                confirmatory_intended_surface=v.get("confirmatory_intended_surface", False),
                typical_error_only=v.get("typical_error_only", False),
                seen_form=seen,
                target_form=target,
                source_alias_form=alias,
                source_canonical_form=canon,
                popularity=v.get("pageviews", 0),
                orth_seen_target=orth_sim_u(seen, target),
                s_seen_target=s_seen,
                joint_seen_target=pair.get((sid[seen], sid[target]), 0),
                c_seen=single[sid[seen]],
                assoc_any=pick["label"],
                assoc_any_qid=pick["qid"],
                assoc_any_type=pick.get("entity_type", "other"),
                assoc_any_relation=pick["relation"],
                s_assoc_any=pick["s_assoc"],
                joint_assoc_any_target=pick["joint_assoc_target"],
                assoc_any_margin=pick["margin"],
                c_assoc_any=single[sid[pick["label"]]],
                assoc_sametype=(pick_same or {}).get("label"),
                assoc_sametype_qid=(pick_same or {}).get("qid"),
                assoc_sametype_relation=(pick_same or {}).get("relation"),
                s_assoc_sametype=(pick_same or {}).get("s_assoc"),
                frames=FRAMES,
            )
            rows.append(row)
            pair_survival[v["pair_id"]].add(direction)

    if not rows:
        raise RuntimeError("No ordered item survived ASSOC_ANY matching")
    item_ids = [row["item_id"] for row in rows]
    if len(item_ids) != len(set(item_ids)):
        raise RuntimeError("item_id collision in frozen r4 evaluation bank")

    # Independent hard-identity probe foils. Using ASSOC_ANY itself as the foil
    # would select on the same pair later contrasted in Q2. Rotate over a large
    # different-entity pool, match coarse type/token length, and forbid lexical
    # overlap with every main-condition mention.
    foil_pool = sorted({
        (row["entity_uri"], row["entity_type"], row["target_form"])
        for row in rows
    })
    for row in rows:
        forbidden = (target_tokens(row["target_form"])
                     | target_tokens(row["seen_form"])
                     | target_tokens(row["assoc_any"]))
        eligible = []
        for entity_uri, entity_type, form in foil_pool:
            if entity_uri == row["entity_uri"] or entity_type != row["entity_type"]:
                continue
            if forbidden & target_tokens(form):
                continue
            eligible.append((
                abs(len(tokens_u(form)) - len(tokens_u(row["target_form"]))),
                hashlib.sha256((row["item_id"] + "\0" + entity_uri + "\0" + form).encode()).hexdigest(),
                entity_uri,
                form,
            ))
        if not eligible:
            raise RuntimeError(f"no independent identity-probe foil for {row['item_id']}")
        _, _, foil_entity, foil_form = min(eligible)
        row["identity_probe_foil"] = foil_form
        row["identity_probe_foil_entity"] = foil_entity
    Path(args.out).write_text("\n".join(
        json.dumps(r, sort_keys=True, ensure_ascii=False) for r in rows
    ) + "\n")

    print(f"\nmatched ordered items: {len(rows)} from {len(pair_survival)} surface pairs")
    print("directions:", dict(Counter(r["direction"] for r in rows)))
    print("strata:", dict(Counter(r["structural_stratum"] for r in rows)))
    print("entity types:", dict(Counter(r["entity_type"] for r in rows)))
    print("intended confirmatory ordered items:",
          sum(r["confirmatory_intended_surface"] for r in rows))
    print("with ASSOC_SAMETYPE sensitivity control:",
          sum(r["assoc_sametype"] is not None for r in rows))
    print("drop reasons:")
    for k, n in drop.most_common():
        print(f"  {n:>6}  {k}")
    print("ASSOC_ANY relations:",
          dict(Counter(r["assoc_any_relation"] for r in rows).most_common(20)))
    digest = hashlib.sha256(Path(args.out).read_bytes()).hexdigest()
    print(f"\nwrote {args.out}; sha256 {digest}")


if __name__ == "__main__":
    main()
