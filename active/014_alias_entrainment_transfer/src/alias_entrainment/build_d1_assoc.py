"""D1 r4 stage 3: attach strong non-coreferent ASSOC candidates to every surface pair.

r3 made SAME-TYPE a construction requirement.  That was unnecessary estimand
narrowing: the association hypothesis is pair-specific and real-world, not
"same Wikidata coarse type".  r4 therefore builds:

  ASSOC_ANY      all strong related, different-referent candidates (primary)
  ASSOC_SAMETYPE the same list restricted by coarse type (sensitivity)

P1889 `different_from` remains forbidden: it encodes confusability, not a
real-world association.  No surface pair is deleted at this stage; missing
controls are a later matching outcome, not a reason to redefine the source bank.

Canonical contract: configs/contract_d1_r4.yaml
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

from build_d1_candidates import normu

API = "https://www.wikidata.org/w/api.php"
UA = ("Interpretability-research/014-alias-entrainment "
      "(academic use; contact xiang.ding.i8@s.mail.nagoya-u.ac.jp)")
EXCLUDED_TIES = {"different_from"}
SECOND_HOP = {"member_of", "record_label", "member_of_sports_team",
              "participant_in", "cast_member", "performer", "part_of"}
PERSON_TYPES = {"Q5"}
GROUP_TYPES = {"Q215380", "Q2088357", "Q9212979", "Q7623897"}
ORG_TYPES = {"Q43229", "Q4830453", "Q783794", "Q891723", "Q6881511", "Q2085381"}
PLACE_TYPES = {"Q486972", "Q515", "Q3957", "Q1549591", "Q56061", "Q532"}


def coarse(p31):
    s = set(p31)
    if PERSON_TYPES & s: return "person"
    if GROUP_TYPES & s: return "group"
    if ORG_TYPES & s: return "organization"
    if PLACE_TYPES & s: return "place"
    return "other"


def get(params):
    url = API + "?" + urllib.parse.urlencode({**params, "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for a in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())
        except Exception:
            if a == 4: raise
            time.sleep(2 * (a + 1))


def fetch(qids, props):
    out = {}
    qids = sorted(set(qids))
    for i in range(0, len(qids), 50):
        d = get(dict(action="wbgetentities", ids="|".join(qids[i:i + 50]),
                     props=props, languages="en"))
        out.update(d.get("entities") or {})
        if i and i % 2000 == 0:
            print(f"    {i}/{len(qids)}", flush=True)
        time.sleep(0.1)
    return out


def eids(claims, pid):
    v = []
    for c in claims.get(pid, []):
        dv = (c.get("mainsnak") or {}).get("datavalue") or {}
        if dv.get("type") == "wikibase-entityid":
            v.append(dv["value"]["id"])
    return v


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cands", default="data/d1_surface_pairs_r4.json")
    ap.add_argument("--wikidata", default="data/d1_wikidata_r4.json")
    ap.add_argument("--out", default="data/d1_assoc_candidates_r4.json")
    args = ap.parse_args()

    W = json.load(open(args.wikidata))
    C = json.load(open(args.cands))
    by_qid = {c["subject_id"] for c in C}
    print(f"surface pairs: {len(C)} across {len(by_qid)} entities")

    # Expand group/work/team relations to co-members, but retain the directly
    # related group/work itself too.  Cross-type relations are valid ASSOC_ANY.
    hop = sorted({g for q, v in W.items() if q in by_qid
                  for t in SECOND_HOP for g in v.get("ties", {}).get(t, [])})
    print(f"second-hop entities to expand: {len(hop)}")
    hents = fetch(hop, "claims")
    hop_members = {}
    for g, e in hents.items():
        cl = e.get("claims") or {}
        hop_members[g] = (eids(cl, "P527") + eids(cl, "P161") + eids(cl, "P175")
                          + eids(cl, "P54") + eids(cl, "P710"))

    per_entity: dict[str, dict[str, str]] = {}
    for q in sorted(by_qid):
        v = W.get(q) or {}
        cand: dict[str, str] = {}
        for t, xs in (v.get("ties") or {}).items():
            if t in EXCLUDED_TIES:
                continue
            for x in xs:
                if x == q:
                    continue
                cand.setdefault(x, t)  # direct relation is itself a valid ASSOC_ANY
                if t in SECOND_HOP:
                    for m in hop_members.get(x, []):
                        if m != q:
                            cand.setdefault(m, t + "_comember")
        per_entity[q] = cand

    need = sorted({x for v in per_entity.values() for x in v})
    print(f"resolving {len(need)} related entities")
    ents = fetch(need, "labels|claims|sitelinks")
    info = {}
    for qid, e in ents.items():
        lab = ((e.get("labels") or {}).get("en") or {}).get("value")
        info[qid] = dict(
            label=lab,
            ctype=coarse(eids(e.get("claims") or {}, "P31")),
            sitelinks=len(e.get("sitelinks") or {}),
        )

    out = []
    n_any, n_same = 0, 0
    type_counts, relation_counts = Counter(), Counter()
    for c in C:
        q = c["subject_id"]
        ttype = (W.get(q) or {}).get("coarse_type", "other")
        alias_closure = {normu(x) for x in c.get("aliases", []) if x}
        rows = []
        for qid, rel in per_entity.get(q, {}).items():
            i = info.get(qid) or {}
            lab = i.get("label")
            if not lab or qid == q:
                continue
            # Only true coreference is forbidden here.  Lexical overlap with the
            # SCORED target is direction-specific and is checked in stage 5.
            if normu(lab) in alias_closure:
                continue
            rows.append(dict(
                qid=qid,
                label=lab,
                relation=rel,
                entity_type=i.get("ctype", "other"),
                same_type=i.get("ctype") == ttype,
                sitelinks=i.get("sitelinks", 0),
            ))
            relation_counts[rel] += 1
        rows.sort(key=lambda r: (r["qid"], r["relation"]))
        if rows:
            n_any += 1
        if any(r["same_type"] for r in rows):
            n_same += 1
        type_counts[ttype] += 1
        out.append(dict(**c, entity_type=ttype, assoc=rows))

    Path(args.out).write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"\nwrote {args.out}")
    print(f"pairs with >=1 ASSOC_ANY candidate: {n_any}/{len(out)}")
    print(f"pairs with >=1 ASSOC_SAMETYPE candidate: {n_same}/{len(out)}")
    print("source entity types:", dict(type_counts))
    print("top relations:", dict(relation_counts.most_common(20)))


if __name__ == "__main__":
    main()
