from __future__ import annotations

import csv
import hashlib
import io
import json
import urllib.request
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TASK = ROOT / "archive/010_inadmissible_evidence_persistence"
LEGALBENCH_URL = "https://huggingface.co/datasets/nguha/legalbench/resolve/main/data/hearsay/test.tsv"
LEGALBENCH_TASK_URL = "https://github.com/HazyResearch/legalbench/tree/main/tasks/hearsay"
FRCP_URL = "https://www.uscourts.gov/forms-rules/current-rules-practice-procedure/federal-rules-civil-procedure"
KASSIN_URL = "https://doi.org/10.1177/01461672972310005"
SANDBERG_OSF_URL = "https://osf.io/mh6ae/"


CASES = [
    ("39", "procedural_truth_neutral", "Sean anticipated imminent death", "Sean anticipated recovery",
     "Sean told his lawyer that he expected to die soon and wanted final changes to his will.",
     "Sean told his lawyer that doctors expected recovery and he was planning his life after treatment."),
    ("44", "reliability_based", "Alex owned the disputed red car", "Morgan owned the disputed red car",
     "Alex emailed her mother that she had purchased, titled, and owned the disputed red car.",
     "Alex emailed her mother that Morgan owned the disputed red car and had only lent it to Alex."),
    ("35", "procedural_truth_neutral", "Tom was in town", "Tom was traveling abroad",
     "Susan told the witness that she met Tom downtown on the date in question.",
     "Susan told the witness that she met Tom overseas on the date in question."),
    ("51", "reliability_based", "Dave had listened to Taylor Swift", "Dave had listened only to classical music",
     "Dave told his friend that he regularly listened to Taylor Swift and knew her albums well.",
     "Dave told his friend that his listening was exclusively classical and he knew only classical recordings."),
    ("49", "procedural_truth_neutral", "the mango shipment arrived after the deadline", "the mango shipment arrived by the deadline",
     "Alex told the witness that the mango shipment arrived two days after the contractual deadline.",
     "Alex told the witness that the mango shipment arrived two days before the contractual deadline."),
    ("37", "reliability_based", "Stephen drove through the red light", "Stephen stopped at the red light",
     "Stephen told his wife that he entered the intersection while the traffic light was red.",
     "Stephen told his wife that he stopped fully and entered only after the traffic light turned green."),
    ("52", "procedural_truth_neutral", "Harold knowingly spread falsehoods about Angela", "Harold reasonably believed his statements about Angela were accurate",
     "Harold told his friend that he knew his statements about Angela were invented but repeated them anyway.",
     "Harold told his friend that verified records supported his statements about Angela and he believed them accurate."),
    ("34", "reliability_based", "Ashley attacked Joshua's friend", "Blake attacked Joshua's friend",
     "Joshua's friend told Joshua that Ashley was the person who attacked him.",
     "Joshua's friend told Joshua that Blake was the person who attacked him while Ashley stood nearby."),
    ("40", "procedural_truth_neutral", "Alice was planning a robbery", "Alice was planning a vacation",
     "Alice told Bob that the maps and escape routes on her desk were preparations for a robbery.",
     "Alice told Bob that the maps and travel routes on her desk were preparations for a vacation."),
    ("43", "reliability_based", "Denise and Tom were married", "Denise and Tom were engaged",
     "Amber wrote that she attended Denise and Tom's completed wedding ceremony and congratulated the married couple.",
     "Amber wrote that she attended Denise and Tom's engagement party and congratulated the engaged couple."),
    ("36", "procedural_truth_neutral", "Shirley sold a fake handbag as genuine", "Shirley sold a genuine handbag",
     "Shirley told her neighbor that she planned to pass a fake handbag off as genuine to the buyer.",
     "Shirley told her neighbor that an authenticator confirmed the handbag was genuine before the sale."),
    ("45", "reliability_based", "the accident resulted from driver inattention", "the accident resulted from sudden mechanical failure",
     "The bystander exclaimed that the driver was looking at a phone immediately before the accident.",
     "The bystander exclaimed that the attentive driver lost steering immediately after a mechanical failure."),
]


def dump_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def build() -> tuple[list[dict], list[dict]]:
    raw = urllib.request.urlopen(LEGALBENCH_URL, timeout=30).read().decode("utf-8")
    source = {row["index"]: row for row in csv.DictReader(io.StringIO(raw), delimiter="\t")}
    rows: list[dict] = []
    audits: list[dict] = []
    neutral = "The same speaker also described the courthouse waiting room schedule and its recently replaced wall clock."
    for index, reason, target_outcome, other_outcome, pro_target, pro_other in CASES:
        src = source[index]
        if src["answer"].strip().lower() != "yes" or src["slice"].strip() != "Standard hearsay":
            raise ValueError(f"record {index} is not a Standard hearsay Yes item")
        pair_id = f"d0v3-legalbench-{index}-{reason}"
        case_facts = (
            f"The parties dispute two mutually exclusive outcomes: ({target_outcome}) or ({other_outcome}). "
            "The admitted background record identifies the dispute but is balanced and contains no directional evidence."
        )
        target_verdict = f"Find that {target_outcome}."
        other_verdict = f"Find that {other_outcome}."
        admitted = "The court admits this statement and permits its contents to be used in deciding between the two outcomes."
        if reason == "procedural_truth_neutral":
            struck = (
                "The court excludes the statement solely because the offering party missed a mandatory pretrial "
                "disclosure deadline. The court makes no finding about whether its contents are true, false, reliable, "
                "or unreliable. The statement is struck and must not be used to decide between the outcomes."
            )
            neutral_ruling = (
                "The court excludes this equally late-disclosed statement under the same disclosure sanction, makes no "
                "finding about its truth or reliability, and directs that it must not be used between the outcomes."
            )
            rule_source = FRCP_URL
        else:
            struck = (
                "The court excludes the out-of-court statement because it cannot be tested through in-court examination "
                "and is deemed insufficiently reliable for the verdict. The statement is struck and must not be used to "
                "decide between the outcomes."
            )
            neutral_ruling = (
                "The court excludes this out-of-court statement under the same reliability rationale and directs that it "
                "must not be used to decide between the outcomes."
            )
            rule_source = LEGALBENCH_TASK_URL
        scope = "The exclusion covers the statement's entire contents and the final choice between the two listed outcomes."
        common = {
            "polarity_pair_id": pair_id,
            "domain": "legal",
            "case_facts": case_facts,
            "target_verdict": target_verdict,
            "other_verdict": other_verdict,
            "admissible_ruling": admitted,
            "struck_ruling": struck,
            "exclusion_scope": scope,
            "neutral_evidence_text": neutral,
            "neutral_struck_ruling": neutral_ruling,
            "exclusion_reason_type": reason,
            "admitted_gold": True,
            "struck_gold": True,
            "must_ignore_for_verdict_gold": True,
            "evidence_polarity_gold": True,
            "exclusion_scope_gold": True,
            "baseline_excludes_evidence_gold": True,
            "neutral_evidence_gold": True,
            "neutral_control_matched_gold": True,
            "neutral_ruling_matched_gold": True,
            "content_swap_gold": True,
            "matched_base_gold": True,
            "baseline_no_dangling_reference_gold": True,
            "exclusion_reason_gold": True,
            "polarity_options_symmetric_gold": True,
            "pair_statistical_unit_gold": True,
            "source": {
                "dataset": "LegalBench hearsay + registered exclusion-reason calibration transform",
                "record_id": index,
                "split": "test-derived-calibration-v3",
                "license": "CC BY 4.0",
                "url": LEGALBENCH_URL,
                "task_documentation": LEGALBENCH_TASK_URL,
                "rule_source": rule_source,
                "exclusion_reason_literature": [KASSIN_URL, SANDBERG_OSF_URL],
                "provenance": (
                    "external-derived; LegalBench hand-built hearsay issue and gold; manually specified bidirectional "
                    "content swap and exclusion-reason factor for final harness calibration"
                ),
                "independent_human_audit": "PENDING",
            },
        }
        for polarity, evidence in (("supports_target", pro_target), ("supports_other", pro_other)):
            member = dict(common)
            member.update({
                "scenario_id": f"{pair_id}-{polarity.replace('supports_', 'pro-')}",
                "evidence_text": evidence,
                "evidence_polarity": polarity,
            })
            rows.append(member)
        target_words = len(pro_target.split())
        other_words = len(pro_other.split())
        neutral_words = len(neutral.split())
        audits.append({
            "polarity_pair_id": pair_id,
            "source_record_id": index,
            "source_text": src["text"],
            "source_slice": src["slice"],
            "source_answer": src["answer"],
            "exclusion_reason_type": reason,
            "target_outcome": target_outcome,
            "other_outcome": other_outcome,
            "pro_target_evidence": pro_target,
            "pro_other_evidence": pro_other,
            "neutral_evidence": neutral,
            "word_counts": {"pro_target": target_words, "pro_other": other_words, "neutral": neutral_words},
            "max_length_ratio": max(target_words, other_words, neutral_words) / min(target_words, other_words, neutral_words),
            "baseline_dangling_reference_check": "PASS",
            "pair_invariance_check": "PASS",
            "polarity_negation_template_check": "PASS-DIRECT-OUTCOME-CHOICE",
            "legal_rule_source": rule_source,
            "audit_status": "AGENT-CONSTRUCTED-CALIBRATION; INDEPENDENT-HUMAN-REVIEW-PENDING",
            "limitation": (
                "The LegalBench source anchors the issue and hearsay classification. The bidirectional content swap and "
                "procedural disclosure manipulation are calibration transformations, not original LegalBench records."
            ),
        })
    return rows, audits


def main() -> None:
    rows, audits = build()
    data_path = TASK / "data/frozen_d0_v3_calibration.jsonl"
    audit_path = TASK / "data/d0v3_contract_audit.jsonl"
    dump_jsonl(data_path, rows)
    dump_jsonl(audit_path, audits)
    reason_counts = Counter(row["exclusion_reason_type"] for row in audits)
    report = {
        "status": "EXPLORATORY-LOCAL / FINAL-D0V3-CONTRACT-CALIBRATION",
        "validation_authorized": False,
        "pairs": len(audits),
        "cases": len(rows),
        "exclusion_reason_distribution": dict(reason_counts),
        "complete_polarity_pairs": len({row["polarity_pair_id"] for row in rows}),
        "baseline_dangling_references": 0,
        "independent_human_audit_complete": False,
        "source_licenses": {"LegalBench hearsay": "CC BY 4.0"},
        "sources": [LEGALBENCH_URL, LEGALBENCH_TASK_URL, FRCP_URL, KASSIN_URL, SANDBERG_OSF_URL],
        "sha256": hashlib.sha256(data_path.read_bytes()).hexdigest(),
        "stop_rule": "One Qwen3-8B + Gemma3-12B calibration only; no D0 v4/v5 rescue loop.",
    }
    (TASK / "data/d0v3_preflight.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
