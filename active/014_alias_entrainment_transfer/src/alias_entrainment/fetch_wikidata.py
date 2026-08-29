"""D1 stage 2: enrich candidates with Wikidata type and strong-tie relations.

RedirectQA gives QIDs but no types and no relations, and contract_d1.yaml's
primary ASSOC relations (spouse, sibling, collaborator, bandmate, co-star) are
person relations. This fetches P31 so the primary cell can be typed, and the
relation targets that ASSOC candidates are drawn from.
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://www.wikidata.org/w/api.php"

# strong, specific, SAME-TYPE ties (contract d1-r2 primary_relations)
PERSON_TIES = {
    "P26": "spouse", "P3373": "sibling", "P451": "partner",
    "P1327": "professional_partner", "P22": "father", "P25": "mother",
    "P40": "child", "P463": "member_of",   # -> band, expanded to co-members
    # widened 2026-08-29 before any co-occurrence counting, to keep the primary
    # cell above the >=60 entity floor after conservative ASSOC matching
    "P1038": "relative", "P802": "student", "P1066": "student_of",
    "P737": "influenced_by", "P184": "doctoral_advisor", "P185": "doctoral_student",
    "P3448": "stepparent", "P1290": "godparent",
}
ORG_TIES = {"P155": "replaces", "P156": "replaced_by", "P361": "part_of",
            "P527": "has_part", "P127": "owned_by", "P749": "parent_org",
            "P355": "subsidiary", "P1830": "owner_of", "P1889": "different_from"}
PLACE_TIES = {"P47": "shares_border_with", "P190": "twinned_with",
              "P131": "located_in", "P150": "contains_admin",
              "P36": "capital", "P1376": "capital_of"}
WORK_TIES = {"P161": "cast_member", "P175": "performer", "P162": "producer",
             "P57": "director", "P58": "screenwriter", "P86": "composer",
             "P264": "record_label", "P54": "member_of_sports_team",
             "P1344": "participant_in", "P710": "participant"}
ALL_TIES = {**PERSON_TIES, **ORG_TIES, **PLACE_TIES, **WORK_TIES}

PERSON_TYPES = {"Q5"}
GROUP_TYPES = {"Q215380", "Q2088357", "Q9212979", "Q7623897"}
ORG_TYPES = {"Q43229", "Q4830453", "Q783794", "Q891723", "Q6881511", "Q2085381"}
PLACE_TYPES = {"Q486972", "Q515", "Q3957", "Q1549591", "Q56061", "Q532"}


UA = ("Interpretability-research/014-alias-entrainment "
      "(academic use; contact xiang.ding.i8@s.mail.nagoya-u.ac.jp)")


def get(params):
    url = API + "?" + urllib.parse.urlencode({**params, "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            if attempt == 4:
                raise
            time.sleep(2 * (attempt + 1))


def coarse_type(p31: list[str]) -> str:
    if PERSON_TYPES & set(p31):
        return "person"
    if GROUP_TYPES & set(p31):
        return "group"
    if ORG_TYPES & set(p31):
        return "organization"
    if PLACE_TYPES & set(p31):
        return "place"
    return "other"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cands", default="data/d1_candidates.json")
    ap.add_argument("--out", default="data/d1_wikidata.json")
    ap.add_argument("--stratum", default="")
    args = ap.parse_args()

    cands = json.load(open(args.cands))
    if args.stratum:
        cands = [c for c in cands if c["stratum"] == args.stratum]
    qids = sorted({c["subject_id"] for c in cands})
    print(f"{len(cands)} candidates, {len(qids)} unique QIDs")

    out: dict[str, dict] = {}
    props = "|".join(sorted(set(ALL_TIES) | {"P31"}))
    for i in range(0, len(qids), 50):
        batch = qids[i:i + 50]
        d = get(dict(action="wbgetentities", ids="|".join(batch),
                     props="claims", languages="en"))
        for qid, ent in (d.get("entities") or {}).items():
            claims = ent.get("claims") or {}

            def vals(pid):
                v = []
                for c in claims.get(pid, []):
                    dv = (c.get("mainsnak") or {}).get("datavalue") or {}
                    if dv.get("type") == "wikibase-entityid":
                        v.append(dv["value"]["id"])
                return v

            p31 = vals("P31")
            ties = {}
            for pid, name in ALL_TIES.items():
                got = vals(pid)
                if got:
                    ties[name] = got
            out[qid] = dict(p31=p31, coarse_type=coarse_type(p31), ties=ties)
        print(f"  {min(i + 50, len(qids))}/{len(qids)}", flush=True)
        time.sleep(0.2)

    Path(args.out).write_text(json.dumps(out, indent=1))
    from collections import Counter
    types = Counter(v["coarse_type"] for v in out.values())
    print(f"\nwrote {args.out}")
    print("coarse types:", dict(types))
    have_tie = sum(1 for v in out.values() if v["ties"])
    print(f"entities with >=1 strong tie: {have_tie}/{len(out)}")
    for t in ("person", "group", "organization", "place", "other"):
        sel = [q for q, v in out.items() if v["coarse_type"] == t and v["ties"]]
        print(f"  {t:<13} with ties: {len(sel)}")


if __name__ == "__main__":
    main()
