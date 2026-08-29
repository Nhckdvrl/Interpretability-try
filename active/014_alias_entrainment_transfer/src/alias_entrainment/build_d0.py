"""Build the frozen D0 item bank for 014 Alias Entrainment Transfer.

Source: PopQA (akariasai/PopQA, local HF cache). PopQA ships the Wikidata
aliases (CC0) and Wikipedia pageview popularity for every subject and object
entity it uses, so the whole bank is derived from one public artefact.

Nothing here is synthetic except the two semantically bleached insertion
frames, which are the minimal causal contrast and carry no effect size.

Contract: configs/contract_r1.yaml (2026-08-29-r1), frozen before any model call.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
from datasets import load_dataset

SEED = 20260829
ASCII_OK = re.compile(r"^[A-Za-z0-9 .&'\-]+$")

# Which relation-role a type can be read off from, unambiguously.
TYPE_VOTES = {
    "person": [("obj", "director"), ("obj", "screenwriter"), ("obj", "composer"),
               ("obj", "author"), ("obj", "father"), ("obj", "mother"),
               ("subj", "occupation"), ("subj", "place of birth"),
               ("subj", "father"), ("subj", "mother"), ("subj", "religion")],
    "city": [("obj", "capital"), ("subj", "capital of"), ("obj", "place of birth")],
    "country": [("subj", "capital"), ("obj", "country"), ("obj", "capital of")],
}
CARRIER_RELATIONS = {
    "person": ["director", "screenwriter", "composer", "author"],
    "city": ["capital", "place of birth"],
    "country": ["country", "capital of"],
}
FRAMES = {
    "F1": "{M} was in the news last week.",
    "F2": "Yesterday's report briefly mentioned {M}.",
}
TYPE_TEMPLATE = {"person": "the person {}", "city": "the city {}",
                 "country": "the place {}"}
POP_FLOOR_TARGET = 1000     # entity under test must be reasonably well attested
POP_FLOOR_POOL = 500        # control entities must also be attested


def norm(s) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def words(s) -> set[str]:
    return {w for w in re.sub(r"[^a-z0-9 ]", " ", (s or "").lower()).split() if w}


def is_acronym(short: str, long: str) -> bool:
    """True if `short` is the initial-letter sequence of `long`."""
    initials = "".join(w[0] for w in re.sub(r"[^A-Za-z ]", " ", long).split() if w)
    s = norm(short)
    if not s or len(s) > len(initials):
        return False
    # allow the acronym to skip lowercase function words (of, and, the, ...)
    caps = "".join(w[0] for w in re.sub(r"[^A-Za-z ]", " ", long).split()
                   if w and w[0].isupper())
    return s == initials.lower() or s == caps.lower()


def is_compositional(short: str, long: str) -> bool:
    """Catch forms DERIVABLE from the other, which `is_acronym` alone missed.

    The 2026-08-29 audit of the frozen bank found 39% of pairs compositional:
    ISO/postal codes (GBR, US-MA, Fla.), initials with a middle name (DJT),
    title-plus-numeral forms (QE2), and full legal names. `opaque_strict` was
    orthographically opaque, never conceptually opaque.
    """
    s, l = norm(short), norm(long)
    if len(s) > len(l):
        s, l = l, s
        short, long = long, short
    if len(s) <= 4:
        return True                       # country/postal codes and initialisms
    letters = re.sub(r"[^A-Za-z]", "", short)
    if letters.isupper() and len(letters) <= 6:
        return True                       # all-caps code form
    caps = "".join(w[0] for w in re.sub(r"[^A-Za-z ]", " ", long).split()
                   if w and w[0].isupper()).lower()
    core = re.sub(r"[^a-z]", "", s)
    if core and (core in caps or all(c in caps for c in core)):
        return True                       # initials, with or without middle names
    if words(short) < words(long) or words(long) < words(short):
        return True                       # one name is a subset of the other's words
    return False


def orth_sim(a, b) -> float:
    """Character-level overlap of the normalized strings (0..1).

    Guards the case where an alias transfers only because it looks like the
    target (`Italia` -> `Italy`) rather than because it denotes the same entity.
    """
    return SequenceMatcher(None, norm(a), norm(b)).ratio()


def stratum(a: str, b: str) -> str:
    if is_acronym(a, b) or is_acronym(b, a):
        return "acronym"
    if words(a) & words(b):
        return "partial"
    return "opaque"


ORTH_STRICT_MAX = 0.40


def strict_stratum(a: str, b: str) -> str:
    """`opaque_strict` = no shared word, not derivable, and low character overlap."""
    if stratum(a, b) == "opaque" and orth_sim(a, b) < ORTH_STRICT_MAX \
            and not is_compositional(a, b):
        return "opaque_strict"
    return "compositional" if is_compositional(a, b) else stratum(a, b)


def good_pair(a: str, b: str) -> bool:
    if not (ASCII_OK.match(a) and ASCII_OK.match(b)):
        return False
    na, nb = norm(a), norm(b)
    if len(na) < 3 or len(nb) < 3 or na == nb:
        return False
    if na in nb or nb in na:
        return False
    if len(a.split()) > 5 or len(b.split()) > 5:
        return False
    return True


def build_entities(ds):
    ents: dict[str, dict] = {}
    for r in ds:
        for role, name, al, uri, pop in (
            ("subj", r["subj"], r["s_aliases"], r["s_uri"], r["s_pop"]),
            ("obj", r["obj"], r["o_aliases"], r["o_uri"], r["o_pop"]),
        ):
            e = ents.setdefault(uri, dict(uri=uri, name=name, aliases=set(),
                                          pop=pop or 0, roles=set()))
            try:
                e["aliases"].update(json.loads(al))
            except Exception:
                pass
            e["roles"].add((role, r["prop"]))
            e["pop"] = max(e["pop"], pop or 0)
    for e in ents.values():
        types = {t for t, votes in TYPE_VOTES.items() if e["roles"] & set(votes)}
        e["type"] = types.pop() if len(types) == 1 else None   # unanimity required
    return ents


def pick_alias(e) -> tuple[str, str] | None:
    """One alias per entity: prefer the opaque stratum, then the shortest alias."""
    cands = [a for a in sorted(e["aliases"]) if good_pair(e["name"], a)]
    if not cands:
        return None
    order = {"opaque": 0, "partial": 1, "acronym": 2}
    cands.sort(key=lambda a: (order[stratum(e["name"], a)], len(a)))
    return e["name"], cands[0]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/frozen_d0.jsonl")
    ap.add_argument("--n-items", type=int, default=300)
    ap.add_argument("--carriers", type=int, default=3)
    ap.add_argument("--encoder", default="BAAI/bge-large-en-v1.5")
    args = ap.parse_args()

    rng = random.Random(SEED)
    ds = load_dataset("akariasai/PopQA", split="test")
    ents = build_entities(ds)

    # ---- candidate entities: typed, popular, with one usable alias -------------
    cands = []
    for e in ents.values():
        if e["type"] is None or e["pop"] < POP_FLOOR_TARGET:
            continue
        picked = pick_alias(e)
        if picked is None:
            continue
        canon, alias = picked
        cands.append(dict(uri=e["uri"], type=e["type"], pop=e["pop"],
                          canon=canon, alias=alias,
                          stratum=stratum(canon, alias),
                          all_aliases=sorted(e["aliases"]) + [canon]))
    cands.sort(key=lambda c: (-c["pop"], c["uri"]))

    # ---- control pools, per type ----------------------------------------------
    pools = defaultdict(list)
    for e in ents.values():
        if e["type"] and e["pop"] >= POP_FLOOR_POOL and ASCII_OK.match(e["name"]) \
                and len(e["name"].split()) <= 5 and len(norm(e["name"])) >= 4:
            pools[e["type"]].append(dict(uri=e["uri"], name=e["name"], pop=e["pop"],
                                         aliases=set(e["aliases"]) | {e["name"]}))
    for t in pools:
        pools[t].sort(key=lambda x: x["uri"])

    # ---- carrier questions, per type ------------------------------------------
    carriers = defaultdict(list)
    for r in ds:
        if not r["question"] or not r["obj"] or not r["subj"]:
            continue
        for t, rels in CARRIER_RELATIONS.items():
            if r["prop"] in rels:
                carriers[t].append(dict(qid=r["id"], question=r["question"],
                                        gold=r["obj"], subj=r["subj"],
                                        subj_uri=r["s_uri"], obj_uri=r["o_uri"],
                                        prop=r["prop"]))
    for t in carriers:
        carriers[t].sort(key=lambda x: x["qid"])

    # ---- embeddings for the control pools -------------------------------------
    from sentence_transformers import SentenceTransformer
    enc = SentenceTransformer(args.encoder, device="cuda")
    pool_emb = {}
    for t, pool in pools.items():
        names = [TYPE_TEMPLATE[t].format(p["name"]) for p in pool]
        pool_emb[t] = enc.encode(names, batch_size=256, normalize_embeddings=True,
                                 show_progress_bar=False)
        print(f"pool[{t}] = {len(names)} entities")

    # ---- assemble items --------------------------------------------------------
    items, n_ent = [], 0
    for c in cands:
        if n_ent * 2 >= args.n_items:
            break
        t = c["type"]
        pool, emb = pools[t], pool_emb[t]
        if len(pool) < 50 or len(carriers[t]) < 50:
            continue

        forms = [(c["canon"], c["alias"], "canon2alias"),   # seen -> target
                 (c["alias"], c["canon"], "alias2canon")]
        built = []
        for seen, target, direction in forms:
            tv = enc.encode([TYPE_TEMPLATE[t].format(target)],
                            normalize_embeddings=True)[0]
            sims = emb @ tv
            # SEMREL: most similar *non-coreferent* same-type entity sharing no
            # word with either form -> the strongest possible priming control.
            banned_uris = {c["uri"]}
            banned_words = words(target) | words(seen)
            alias_orth = orth_sim(seen, target)
            ok = [i for i, p in enumerate(pool)
                  if p["uri"] not in banned_uris and not (words(p["name"]) & banned_words)
                  and norm(p["name"]) not in {norm(x) for x in c["all_aliases"]}]
            if len(ok) < 20:
                break
            semrel_ok = [i for i in ok
                         if orth_sim(pool[i]["name"], target) <= max(alias_orth, 0.25)]
            if len(semrel_ok) < 20:
                break
            semrel_ok.sort(key=lambda i: -sims[i])
            semrel_i = semrel_ok[0]
            by_sim = sorted(ok, key=lambda i: -sims[i])   # BUG FIX 2026-08-29:
            # `ok` is in pool (URI) order. The old code sliced `ok` directly and
            # called it the bottom tercile, so UNREL was really a random
            # same-type entity (median sim 0.60 against SEMREL's 0.78). Sort
            # explicitly before slicing.
            lo = by_sim[int(len(by_sim) * 0.67):]
            unrel_i = lo[rng.randrange(len(lo))]

            sim_alias = float(enc.encode([TYPE_TEMPLATE[t].format(seen)],
                                           normalize_embeddings=True)[0] @ tv)
            # carriers: gold and subject must not touch either form
            cpool = [q for q in carriers[t]
                     if q["obj_uri"] != c["uri"] and q["subj_uri"] != c["uri"]
                     and not (words(q["gold"]) & banned_words)
                     and not (words(q["subj"]) & banned_words)
                     and norm(target) not in norm(q["question"])
                     and norm(seen) not in norm(q["question"])]
            if len(cpool) < args.carriers:
                break
            chosen = rng.sample(cpool, args.carriers)

            # Hard invariant: in the ALIAS condition the scored string must not
            # occur anywhere in the prompt, not even inside another word. Short
            # targets can hide in the frame ("NED" inside "mentioned").
            leak = any(norm(target) in norm(f"{tpl.format(M=seen)}\nQ: {q['question']}\nA:")
                       for tpl in FRAMES.values() for q in chosen)
            if leak:
                break

            built.append(dict(
                item_id=f"{c['uri'].rsplit('/', 1)[-1]}::{direction}",
                entity_uri=c["uri"], entity_type=t, popularity=c["pop"],
                direction=direction, stratum=c["stratum"],
                seen_form=seen, target_form=target,
                semrel=pool[semrel_i]["name"], unrel=pool[unrel_i]["name"],
                sim_alias_target=sim_alias,
                sim_semrel_target=float(sims[semrel_i]),
                sim_unrel_target=float(sims[unrel_i]),
                sim_matched=bool(sims[semrel_i] >= sim_alias),
                strict_stratum=strict_stratum(seen, target),
                orth_alias_target=orth_sim(seen, target),
                orth_semrel_target=orth_sim(pool[semrel_i]["name"], target),
                orth_unrel_target=orth_sim(pool[unrel_i]["name"], target),
                carriers=[dict(qid=q["qid"], question=q["question"], gold=q["gold"],
                               prop=q["prop"]) for q in chosen],
                frames=FRAMES,
            ))
        if len(built) == 2:          # keep an entity only if both directions exist
            items.extend(built)
            n_ent += 1

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False, sort_keys=True) + "\n")

    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    from collections import Counter
    print(f"\nwrote {len(items)} items ({n_ent} entities) -> {out}")
    print("sha256:", digest)
    print("type:", Counter(i["entity_type"] for i in items))
    print("stratum:", Counter(i["stratum"] for i in items))
    print("strict stratum:", Counter(i["strict_stratum"] for i in items))
    print("median orth_sim alias/semrel/unrel: %.3f %.3f %.3f" % tuple(
        float(np.median([i[k] for i in items])) for k in
        ("orth_alias_target", "orth_semrel_target", "orth_unrel_target")))
    print("sim-matched (sim(SEMREL,B) >= sim(ALIAS,B)):",
          sum(i["sim_matched"] for i in items), "/", len(items))


if __name__ == "__main__":
    main()
