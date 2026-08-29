"""D1 r4 stage 2: enrich the broad surface bank with Wikidata type/relations.

Types are ANALYSIS LABELS, not eligibility filters.  Relations supply candidate
non-coreferent real-world associates for ASSOC_ANY and ASSOC_SAMETYPE.  The
relation inventory was fixed before any D1 model outcome; P1889 is fetched only
for optional CONFUSABLE diagnostics and is forbidden from ASSOC in stage 3.

Canonical contract: configs/contract_d1_r4.yaml
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://www.wikidata.org/w/api.php"

PERSON_TIES = {
    "P26": "spouse", "P3373": "sibling", "P451": "partner",
    "P1327": "professional_partner", "P22": "father", "P25": "mother",
    "P40": "child", "P463": "member_of",
    "P1038": "relative", "P802": "student", "P1066": "student_of",
    "P737": "influenced_by", "P184": "doctoral_advisor", "P185": "doctoral_student",
    "P3448": "stepparent", "P1290": "godparent",
}
ORG_TIES = {
    "P155": "replaces", "P156": "replaced_by", "P361": "part_of",
    "P527": "has_part", "P127": "owned_by", "P749": "parent_org",
    "P355": "subsidiary", "P1830": "owner_of", "P1889": "different_from",
}
PLACE_TIES = {
    "P47": "shares_border_with", "P190": "twinned_with",
    "P131": "located_in", "P150": "contains_admin",
    "P36": "capital", "P1376": "capital_of",
}
WORK_TIES = {
    "P161": "cast_member", "P175": "performer", "P162": "producer",
    "P57": "director", "P58": "screenwriter", "P86": "composer",
    "P264": "record_label", "P54": "member_of_sports_team",
    "P1344": "participant_in", "P710": "participant",
}
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
        except Exception:
            if attempt == 4:
                raise
            time.sleep(2 * (attempt + 1))


def coarse_type(p31: list[str]) -> str:
    s = set(p31)
    if PERSON_TYPES & s:
        return "person"
    if GROUP_TYPES & s:
        return "group"
    if ORG_TYPES & s:
        return "organization"
    if PLACE_TYPES & s:
        return "place"
    return "other"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cands", default="data/d1_surface_pairs_r4.json")
    ap.add_argument("--out", default="data/d1_wikidata_r4.json")
    args = ap.parse_args()

    cands = json.load(open(args.cands))
    qids = sorted({c["subject_id"] for c in cands})
    print(f"{len(cands)} surface pairs, {len(qids)} unique QIDs")

    out: dict[str, dict] = {}
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
    print("coarse types (labels only; nothing is filtered):", dict(types))
    have_tie = sum(1 for v in out.values() if any(
        k != "different_from" for k in v["ties"]))
    print(f"entities with >=1 usable real-world tie: {have_tie}/{len(out)}")


if __name__ == "__main__":
    main()
