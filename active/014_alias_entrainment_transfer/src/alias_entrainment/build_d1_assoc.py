"""D1 stage 3: same-type ASSOC candidates, across ALL strata and entity types.

ASSOC = a DIFFERENT referent with a strong, specific real-world tie to the
target. The tie must be SAME-TYPE (person<->person, org<->org, place<->place),
because a person-name alias contrasted against a city or a film would differ in
lexical neighbourhood, not just in referential identity.

`different_from` (P1889) is never a tie source: it is Wikidata's disambiguation
property, so it links NAME-SIMILAR entities and would hand ASSOC exactly the
lexical confound this design exists to remove. It is kept aside as CONFUSABLE.

The dataset is built BROAD and fully labelled. Strictness belongs to the
analysis (which cell is confirmatory), not to dataset construction.
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

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
    ap.add_argument("--cands", default="data/d1_candidates.json")
    ap.add_argument("--wikidata", default="data/d1_wikidata_all.json")
    ap.add_argument("--out", default="data/d1_assoc_candidates.json")
    args = ap.parse_args()

    W = json.load(open(args.wikidata))
    C = {c["subject_id"]: c for c in json.load(open(args.cands))}
    print(f"candidates: {len(C)} across all strata and types")

    # ---- second hop through groups / labels / works --------------------------
    hop = sorted({g for q, v in W.items() for t in SECOND_HOP
                  for g in v["ties"].get(t, [])})
    print(f"second-hop entities to expand: {len(hop)}")
    hents = fetch(hop, "claims")
    hop_members = {}
    for g, e in hents.items():
        cl = e.get("claims") or {}
        hop_members[g] = (eids(cl, "P527") + eids(cl, "P161") + eids(cl, "P175")
                          + eids(cl, "P54") + eids(cl, "P710"))

    # ---- gather candidates ----------------------------------------------------
    per_target = {}
    for q, v in W.items():
        if q not in C: continue
        cand = {}
        for t, xs in v["ties"].items():
            if t in EXCLUDED_TIES: continue
            if t in SECOND_HOP:
                for g in xs:
                    for m in hop_members.get(g, []):
                        if m != q: cand.setdefault(m, t + "_comember")
            else:
                for x in xs:
                    if x != q: cand.setdefault(x, t)
        if cand: per_target[q] = cand
    print(f"targets with >=1 tie candidate: {len(per_target)}")

    need = sorted({x for v in per_target.values() for x in v})
    print(f"resolving {len(need)} ASSOC candidate entities")
    ents = fetch(need, "labels|claims|sitelinks")
    info = {}
    for qid, e in ents.items():
        lab = ((e.get("labels") or {}).get("en") or {}).get("value")
        info[qid] = dict(label=lab, ctype=coarse(eids(e.get("claims") or {}, "P31")),
                         sitelinks=len(e.get("sitelinks") or {}))

    out, drop = {}, Counter()
    for tgt, cands in per_target.items():
        c = C[tgt]
        ttype = W[tgt]["coarse_type"]
        banned = {w.lower() for w in (c["seen_form"] + " " + c["target_form"]).split()}
        alias_lc = {a.lower() for a in c["aliases"]}
        rows = []
        for qid, rel in cands.items():
            i = info.get(qid) or {}
            lab = i.get("label")
            if not lab: continue
            if i.get("ctype") != ttype:            # SAME-TYPE requirement
                continue
            if set(lab.lower().split()) & banned:  # no character leakage
                continue
            if lab.lower() in alias_lc:            # not an alias of the target
                continue
            rows.append(dict(qid=qid, label=lab, relation=rel,
                             sitelinks=i.get("sitelinks", 0)))
        if rows:
            out[tgt] = dict(seen_form=c["seen_form"], target_form=c["target_form"],
                            cats=c["cats"], pageviews=c["pageviews"],
                            stratum=c["stratum"], entity_type=ttype,
                            aliases=c["aliases"], assoc=rows)
        else:
            drop[f"no same-type ASSOC ({ttype})"] += 1

    Path(args.out).write_text(json.dumps(out, indent=1))
    print(f"\nwrote {args.out}")
    print(f"targets with >=1 same-type ASSOC: {len(out)}")
    for k, n in drop.most_common(6): print(f"   dropped {n:>4}  {k}")
    print("by stratum:", dict(Counter(v["stratum"] for v in out.values())))
    print("by type   :", dict(Counter(v["entity_type"] for v in out.values())))
    n = sorted(len(v["assoc"]) for v in out.values())
    print(f"ASSOC candidates per target: median {n[len(n)//2]}, max {n[-1]}")


if __name__ == "__main__":
    main()
