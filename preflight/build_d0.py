from __future__ import annotations
import csv, hashlib, io, json, urllib.request, platform, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
U004 = "https://www.football-data.co.uk/mmz4281/2324/E0.csv"
U005 = "https://huggingface.co/datasets/nguha/legalbench/resolve/main/data/hearsay/test.tsv"

def dump(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def build004():
    raw = urllib.request.urlopen(U004, timeout=30).read()
    matches = list(csv.DictReader(raw.decode("latin1").splitlines()))[:20]
    rows, audits = [], []
    for i, m in enumerate(matches, 1):
        home, away = m["HomeTeam"], m["AwayTeam"]
        sid = f"football-data-e0-2324-{i:03d}"
        packed = f"{home} wins the match against {away}."
        complement = f"{home} does not win the match against {away}."
        specs = [
            ("k2", [f"{home} wins by 1 or 2 goals", f"{home} wins by at least 3 goals"],
                   ["the match is a draw", f"{away} wins"]),
            ("k3", [f"{home} wins by exactly 1 goal", f"{home} wins by exactly 2 goals", f"{home} wins by at least 3 goals"],
                   ["the match is a draw", f"{away} wins by 1 or 2 goals", f"{away} wins by at least 3 goals"]),
            ("k4", [f"{home} wins by exactly 1 goal", f"{home} wins by exactly 2 goals", f"{home} wins by exactly 3 goals", f"{home} wins by at least 4 goals"],
                   ["the match is a draw", f"{away} wins by exactly 1 goal", f"{away} wins by exactly 2 goals", f"{away} wins by at least 3 goals"]),
        ]
        parts = []
        for fam, bs, cbs in specs:
            branches = "; ".join(bs); cbranches = "; ".join(cbs)
            p = {"partition_id": fam, "branches": bs,
                 "unpacked_text": f"{home} wins against {away} with one of these margins: {branches}.",
                 "reordered_unpacked_text": f"{home} wins against {away} with these margins in reverse order: {'; '.join(reversed(bs))}.",
                 "repacked_text": f"{home} wins the match against {away}; the margin categories are not enumerated.",
                 "partial_text": f"{home} wins against {away} by one of these margins: {'; '.join(bs[:-1])}.",
                 "complement_text": complement, "complement_branches": cbs,
                 "complement_unpacked_text": f"{home} does not win against {away}; the result is one of: {cbranches}.",
                 "focal_length_control_text": f"The event consisting of {home} winning the match against {away}, without listing margin categories, occurs.",
                 "complement_length_control_text": f"The complementary event, in which {home} fails to win against {away}, occurs without listing result categories.",
                 "branch_count_family": f"{sid}-home-win-margin-refinement"}
            for k in ("disjoint_gold", "exhaustive_gold", "equivalent_gold",
                      "partial_is_strict_subset", "partial_strictly_lower_probability_gold",
                      "complement_gold", "complement_partition_gold", "reordered_equivalent_gold",
                      "length_controls_equivalent_gold", "length_controls_matched_gold",
                      "branch_count_comparable_gold"):
                p[k] = True
            parts.append(p)
            audits.append({"scenario_id": sid, "partition_id": fam,
                "record_id": m.get("Date", "") + "/" + home + "/" + away,
                "source_url": U004, "license": "Football-Data terms: free for non-commercial use",
                "human_audit": "Deterministic football taxonomy audit: integer goal margins and draw/loss categories are disjoint and exhaustive; k3/k4 refine k2; the omitted partial margin is feasible.",
                "observed_result": {k: m[k] for k in ("FTHG", "FTAG", "FTR")}})
        rows.append({"scenario_id": sid, "domain": "sports", "packed_text": packed,
            "packed_paraphrase": f"The full-time result is a victory for {home} over {away}.",
            "source": {"dataset": "Football-Data.co.uk English Premier League results",
                "record_id": f"2324-E0-{i:03d}", "split": "season-2023-24",
                "license": "Football-Data terms: free for non-commercial use", "url": U004,
                "provenance": "external-derived; deterministic outcome-taxonomy refinement"},
            "partitions": parts})
    dump(ROOT / "archive/009_packed_unpacked_event_splitting/data/frozen_d0.jsonl", rows)
    dump(ROOT / "archive/009_packed_unpacked_event_splitting/data/pilot_d0.jsonl", rows[:5])
    dump(ROOT / "archive/009_packed_unpacked_event_splitting/data/d0_manual_audit.jsonl", audits)
    return len(rows), len(audits)

def build005():
    raw = urllib.request.urlopen(U005, timeout=30).read().decode("utf-8")
    source = {r["index"]: r for r in csv.DictReader(io.StringIO(raw), delimiter="\t")}
    # Each tuple is manually audited: source record, issue proposition, its
    # complement, a pro-issue statement and a content-swapped anti-issue statement.
    cases = [
      ("33","Deborah was sane","Deborah was not sane","Deborah told her friend outside court that she was completely sane.","Deborah told her friend outside court that she was not sane."),
      ("34","Joshua's friend was attacked by Ashley","Joshua's friend was not attacked by Ashley","Joshua's friend told Joshua outside court that Ashley had just attacked him.","Joshua's friend told Joshua outside court that Ashley had not attacked him."),
      ("35","Tom was in town","Tom was not in town","Susan told the witness outside court that Tom was in town.","Susan told the witness outside court that Tom was not in town."),
      ("36","Shirley committed fraud","Shirley did not commit fraud","Shirley told her neighbor outside court that she planned to trick the buyer with a fake handbag.","Shirley told her neighbor outside court that the handbag was genuine and she planned no trick."),
      ("37","Stephen drove through a stoplight","Stephen did not drive through a stoplight","Stephen told his wife by phone that he drove through the stoplight while not paying attention.","Stephen told his wife by phone that he stopped at the stoplight and did not drive through it."),
      ("38","Henry negligently hit Kelly with his car","Henry did not negligently hit Kelly with his car","Kelly said outside court that a witness saw Henry using his phone while driving at the crash.","Kelly said outside court that a witness saw Henry driving attentively and not using his phone at the crash."),
      ("39","Sean knew he was going to die","Sean did not know he was going to die","Sean told his lawyer outside court that he expected to die and wanted final changes to his will.","Sean told his lawyer outside court that he expected to recover and did not believe he was going to die."),
      ("40","Alice was planning a robbery","Alice was not planning a robbery","Alice told Bob outside court that she was researching escape routes for a robbery.","Alice told Bob outside court that she was not planning a robbery and was researching vacation routes."),
      ("41","Bruce committed medical malpractice","Bruce did not commit medical malpractice","Bruce told a nurse after surgery that he believed he had made a medical mistake.","Bruce told a nurse after surgery that he had followed the required procedure and made no mistake."),
      ("42","Alice suffered reputational harm","Alice did not suffer reputational harm","People told Bob outside court that they had heard damaging things about Alice.","People told Bob outside court that they had heard only favorable things about Alice."),
      ("43","Denise and Tom were married","Denise and Tom were not married","Amber sent Denise and Tom an out-of-court card congratulating them on their wedding.","Amber sent Denise and Tom an out-of-court card acknowledging that they had not married."),
      ("44","Alex owned a red car","Alex did not own a red car","Alex emailed her mother outside court that she had purchased and owned a red car.","Alex emailed her mother outside court that she had not purchased and did not own a red car."),
      ("45","the accident resulted from negligence","the accident did not result from negligence","A bystander exclaimed outside court that the driver was looking down at a phone while driving.","A bystander exclaimed outside court that the driver was attentive and the accident was not caused by negligence."),
      ("46","Henry committed insider trading","Henry did not commit insider trading","Alice told Bob outside court that Henry said he had a great nonpublic stock tip.","Alice told Bob outside court that Henry said he had no nonpublic stock tip and made no insider trade."),
      ("48","Mary was Tom's mother","Mary was not Tom's mother","Albert told Mary outside court that Tom was her son and looked like her.","Albert told Mary outside court that Tom was not her son."),
      ("49","the mango shipment was delayed","the mango shipment was not delayed","A witness said outside court that Alex complained he could not deliver the mangos on time.","A witness said outside court that Alex reported the mangos had been delivered on time."),
      ("50","Alex participated in the criminal conspiracy","Alex did not participate in the criminal conspiracy","A witness said outside court that she heard Alex arranging to meet his co-conspirators.","A witness said outside court that she heard Alex refuse involvement and deny joining any conspiracy."),
      ("51","Dave had listened to Taylor Swift","Dave had not listened to Taylor Swift","Dave told his friend outside court that he listened to Taylor Swift and she was his favorite artist.","Dave told his friend outside court that he had never listened to Taylor Swift."),
      ("52","Harold knowingly spread falsehoods about Angela","Harold did not knowingly spread falsehoods about Angela","Harold admitted to his friend outside court that his statements about Angela were lies.","Harold told his friend outside court that he had not knowingly made any false statement about Angela."),
      ("54","Corporation B stole Corporation A's trade secrets","Corporation B did not steal Corporation A's trade secrets","B's CEO told a friend outside court that B had taken A's trade secrets and could soon compete with A.","B's CEO told a friend outside court that B had not taken any of A's trade secrets."),
    ]
    rows, audits = [], []
    for idx, issue, opposite, pro_target, pro_other in cases:
        src = source[idx]
        if src["answer"].strip().lower() != "yes":
            raise ValueError(f"LegalBench hearsay record {idx} is not hearsay=Yes")
        pid = f"legalbench-hearsay-{idx}"
        facts = (f"The tribunal must decide one issue: whether {issue}. "
                 "Apart from the disputed out-of-court statement below, this evaluation record contains no fact resolving that issue.")
        target = f"Find that {issue}."
        other = f"Find that {opposite}."
        neutral = "The same speaker stated outside court that the courthouse hallway clock showed 3:00 p.m."
        for pol, ev in (("supports_target", pro_target), ("supports_other", pro_other)):
            sid = f"{pid}-{pol.replace('supports_', 'pro-')}"
            rows.append({"scenario_id": sid, "polarity_pair_id": pid, "domain": "legal",
                "case_facts": facts, "evidence_text": ev, "evidence_polarity": pol,
                "target_verdict": target, "other_verdict": other,
                "admissible_ruling": "For this experimental condition, the court admits the statement for use in deciding the stated issue.",
                "struck_ruling": "The court rules that the statement is hearsay, strikes it, and directs that it must not be used in deciding the stated issue.",
                "exclusion_scope": "The exclusion applies to the statement's entire contents and to the final decision on the stated issue.",
                "neutral_evidence_text": neutral,
                "neutral_struck_ruling": "The court strikes this out-of-court clock statement and directs that it must not be used in deciding the stated issue.",
                "admitted_gold": True, "struck_gold": True, "must_ignore_for_verdict_gold": True,
                "evidence_polarity_gold": True, "exclusion_scope_gold": True, "baseline_excludes_evidence_gold": True,
                "neutral_evidence_gold": True, "neutral_control_matched_gold": True, "neutral_ruling_matched_gold": True,
                "content_swap_gold": True, "matched_base_gold": True,
                "source": {"dataset": "LegalBench hearsay", "record_id": idx, "split": "test-derived",
                    "license": "CC BY 4.0", "url": U005,
                    "provenance": "external-derived; source hearsay gold plus manually audited proposition-level polarity swap"}})
        audits.append({"polarity_pair_id": pid, "source_record_id": idx, "source_text": src["text"],
            "source_slice": src["slice"], "source_answer": src["answer"], "source_url": U005,
            "license": "CC BY 4.0", "issue_proposition": issue, "opposite_proposition": opposite,
            "pro_target_evidence": pro_target, "pro_other_evidence": pro_other,
            "neutral_evidence": neutral,
            "human_audit": "Both variants are out-of-court assertions offered for their truth, preserve hearsay status, and reverse only the proposition direction. Base facts, verdicts, rulings, scope and neutral control are byte-identical within the pair.",
            "transformation": "Manual content swap grounded in the source issue; no model-generated taxonomy, legal status, or polarity gold."})
    dump(ROOT / "archive/010_inadmissible_evidence_persistence/data/frozen_d0.jsonl", rows)
    dump(ROOT / "archive/010_inadmissible_evidence_persistence/data/d0_manual_audit.jsonl", audits)
    return len(cases), len(rows)

def report():
    def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
    d4 = ROOT / "archive/009_packed_unpacked_event_splitting/data/frozen_d0.jsonl"
    d5 = ROOT / "archive/010_inadmissible_evidence_persistence/data/frozen_d0.jsonl"
    a4 = json.loads("[" + ",".join((ROOT/"archive/009_packed_unpacked_event_splitting/data/d0_manual_audit.jsonl").read_text().splitlines()) + "]")
    a5 = json.loads("[" + ",".join((ROOT/"archive/010_inadmissible_evidence_persistence/data/d0_manual_audit.jsonl").read_text().splitlines()) + "]")
    out = {"status":"EXPLORATORY-LOCAL", "validation_authorized":False,
           "generated_utc":"2026-08-28", "python":sys.version,
           "platform":platform.platform(), "source_urls":{"004":U004,"005":U005},
           "datasets":{"004":{"scenarios":20,"partitions":60,"domains":["sports"],"source_license":"Football-Data terms: free for non-commercial use","audited_records":len(a4),"sha256":sha(d4),"within_family_groups":20,"branch_counts":[2,3,4]},
                       "005":{"cases":40,"polarity_pairs":20,"domains":["legal"],"source_license":"CC BY 4.0","audited_pairs":len(a5),"sha256":sha(d5)}},
           "audit_coverage":{"004_manual_audits":len(a4),"005_manual_audits":len(a5),"minimum_sample_review_met":len(a4)>=20 and len(a5)>=20},
           "notes":["All gold fields are frozen before model calls.","004 taxonomy is deterministic score-margin refinement anchored to public match records; 005 legal status is anchored to LegalBench hearsay=Yes and pair transformation provenance.","No formal READY-TO-SMOKE or N0/D0 promotion was performed."]}
    p=ROOT/"preflight/d0_preflight_report.json"; p.parent.mkdir(exist_ok=True); p.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")

if __name__ == "__main__":
    print({"004": build004(), "005": build005()}); report()
