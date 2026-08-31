#!/usr/bin/env python3
"""Stupid-baseline metadata leak audit — run BEFORE inspecting any model output.

Question: can C vs F be predicted on the FROZEN G0 role items from features that
carry no accident semantics at all — length, position within the event, occurrence
index, year, punctuation, missingness patterns, event-level shape?

If yes, `A high / B low` could not be read as role-selection failure, because the
role label would be recoverable from bookkeeping structure.

Three feature blocks, each scored separately with GroupKFold on ev_id
(event-grouped, so no accident is split across folds):

  META      semantics-free bookkeeping only              <- the dangerous one
  META+LEN  META plus finding-text *length* statistics
  CODE      finding_code / taxonomy path                 <- NOT model-visible,
                                                            reported as the
                                                            annotation-regularity
                                                            ceiling only

Also asserts that the Task-A and Task-B rendered prompts share an identical
evidence envelope for every shared item.
"""
from __future__ import annotations

import csv, json, re, string
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import GroupKFold

ROOT = Path(__file__).resolve().parents[1]
csv.field_size_limit(10_000_000)
SEED = 20260831
ROLE_SUFFIX = re.compile(r"\s-\s([CF])\s*$")


def load_jsonl(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> None:
    events = {e["ev_id"]: e for e in load_jsonl(ROOT / "items" / "g0_events.jsonl")}
    role_items = load_jsonl(ROOT / "items" / "g0_roles.jsonl")
    rel_items = load_jsonl(ROOT / "items" / "g0_relevance.jsonl")

    # ---- evidence-envelope assertion (user requirement 2) ------------------
    rel_by_id = {i["item_id"]: i for i in rel_items}
    envelope_mismatch = []
    for it in role_items:
        a = rel_by_id.get(it["item_id"])
        if a is None:
            envelope_mismatch.append((it["item_id"], "missing_in_taskA"))
        elif a["finding"] != it["finding"] or a["ev_id"] != it["ev_id"] \
                or a["aircraft_key"] != it["aircraft_key"]:
            envelope_mismatch.append((it["item_id"], "field_mismatch"))
    # both tasks render exactly {narrative, finding}; nothing else is passed
    with (ROOT / "scripts" / "run_g0.py").open(encoding="utf-8") as fh:
        src = fh.read()
    fields_a = set(re.findall(r"\{(\w+)\}", src.split("P_RELEVANCE = ")[1].split('"""')[1]))
    fields_b = set(re.findall(r"\{(\w+)\}", src.split("P_ROLE = ")[1].split('"""')[1]))

    # ---- raw Findings rows, for bookkeeping features -----------------------
    with (ROOT / "export" / "Findings.csv").open(newline="", encoding="utf-8", errors="replace") as fh:
        raw = list(csv.DictReader(fh))
    frow = {(r["ev_id"].strip(), int(r["Aircraft_Key"] or 0), int(r["finding_no"] or 0)): r
            for r in raw}
    file_order = {k: i for i, k in enumerate(frow)}
    unit_n = Counter((r["ev_id"].strip(), int(r["Aircraft_Key"] or 0)) for r in raw)

    X_meta, X_len, X_code, y, groups = [], [], [], [], []
    for it in role_items:
        eid, ak = it["ev_id"], it["aircraft_key"]
        fno = int(it["item_id"].rsplit(":", 1)[1])
        r = frow[(eid, ak, fno)]
        ev = events[eid]
        n_in_unit = unit_n[(eid, ak)]
        text = it["finding"]

        X_meta.append([
            fno,                                   # position within the unit
            fno / max(n_in_unit, 1),               # normalised position
            n_in_unit,                             # findings in the unit
            file_order[(eid, ak, fno)],            # occurrence index in the table
            int(ev["ev_year"]),                    # year
            ev["narrative_words"],                 # narrative length
            len(ev["narrative"]),
            int(ev["narrative_truncated"]),
            ak,                                    # Aircraft_Key
            int(ev["ev_type"] == "ACC"),
            int(not (r["lchg_userid"] or "").strip()),   # missingness patterns
            int(not (r["finding_code"] or "").strip()),
            int(not (r["modifier_no"] or "").strip()),
            len(ev["narrative"].split(".")),       # narrative sentence count
        ])
        X_len.append([
            len(text), len(text.split()), text.count("-"),
            sum(text.count(c) for c in string.punctuation),
            len(text.split("-")[-1]), len(text.split("-")[0]),
            sum(c.isdigit() for c in text), sum(c.isupper() for c in text),
        ])
        X_code.append([
            int(r["category_no"] or 0), int(r["subcategory_no"] or 0),
            int(r["section_no"] or 0), int(r["subsection_no"] or 0),
            int(r["modifier_no"] or 0), int(r["finding_code"] or 0),
        ])
        y.append(1 if it["gold"] == "CAUSE" else 0)
        groups.append(eid)

    y = np.array(y)
    groups = np.array(groups)
    blocks = {
        "META (semantics-free bookkeeping)": np.array(X_meta, float),
        "META+LEN (bookkeeping + text length stats)": np.hstack([X_meta, X_len]).astype(float),
        "CODE (taxonomy codes; NOT model-visible)": np.array(X_code, float),
    }

    gkf = GroupKFold(n_splits=5)
    report = {}
    for name, X in blocks.items():
        preds = np.zeros_like(y)
        for tr, te in gkf.split(X, y, groups):
            clf = GradientBoostingClassifier(random_state=SEED)
            clf.fit(X[tr], y[tr])
            preds[te] = clf.predict(X[te])
        report[name] = round(float(balanced_accuracy_score(y, preds)), 4)

    dummy = np.zeros_like(y)
    for tr, te in gkf.split(blocks["META (semantics-free bookkeeping)"], y, groups):
        d = DummyClassifier(strategy="most_frequent").fit(
            blocks["META (semantics-free bookkeeping)"][tr], y[tr])
        dummy[te] = d.predict(blocks["META (semantics-free bookkeeping)"][te])
    report["majority-class baseline"] = round(float(balanced_accuracy_score(y, dummy)), 4)

    # preregistered-style read: METADATA leak is a problem if semantics-free
    # features alone approach the S0 role ceiling of 0.62.
    meta_ba = report["META (semantics-free bookkeeping)"]
    metalen_ba = report["META+LEN (bookkeeping + text length stats)"]
    out = {
        "n_role_items": int(len(y)),
        "n_events": int(len(set(groups))),
        "gold_counts": {"CAUSE": int(y.sum()), "CONTRIBUTING_FACTOR": int((1 - y).sum())},
        "cv": "GroupKFold(5) clustered on ev_id",
        "balanced_accuracy": report,
        "S0_role_threshold_for_reference": 0.62,
        "metadata_leak_verdict": (
            "FAIL — semantics-free metadata alone reaches the S0 role ceiling"
            if max(meta_ba, metalen_ba) >= 0.62 else
            "PASS — semantics-free metadata cannot recover C/F"),
        "evidence_envelope_check": {
            "taskA_prompt_fields": sorted(fields_a),
            "taskB_prompt_fields": sorted(fields_b),
            "identical_fields": sorted(fields_a) == sorted(fields_b),
            "role_items_with_matching_taskA_item": len(role_items) - len(envelope_mismatch),
            "mismatches": envelope_mismatch[:20],
            "verdict": "PASS" if not envelope_mismatch and fields_a == fields_b else "FAIL",
        },
        "note": (
            "CODE is reported only as the annotation-regularity ceiling. finding_code, "
            "category_no, subcategory_no, section_no, subsection_no and modifier_no are "
            "never rendered into any model prompt (PREREGISTRATION.md sec. 6)."),
    }
    (ROOT / "audit" / "metadata_leak_audit.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
