"""Build the human norming instrument for the authored Z-event causal relations.

Davies & Richardson (2021) validated the P-event half of the E manipulation against 31 readers
(`hungry` bears on `fed`, not on `tickled`). The Z-event half is ours, so it is normed
independently, on humans, before any preregistered model is evaluated.

Design: 12 families x 2 events (E+ / E-) x 2 candidate reasons (P / Z) = 48 rating trials.
Each trial shows a minimal ONE-referent vignette — reference is deliberately not at stake here, so
the four-entity world is not used — in which both P and Z are stated, followed by the matrix event
and a single candidate reason, rated 1-7.

Presentation is a 4-list Latin square: each participant sees each family exactly once, three
families in each of the four conditions, so no participant ever compares two versions of the same
item. List assignment is deterministic (family index + condition index) mod 4.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path

SEED = 20260904
SCALE = "1 = does not explain it at all, 7 = explains it completely"
QUESTION = "How well does this reason explain why the event happened?"


def load_items():
    spec = importlib.util.spec_from_file_location(
        "b1", Path(__file__).resolve().parent.parent / "scripts" / "build_b1_function_cross.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ITEMS


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for family_index, item in enumerate(load_items()):
        (item_id, noun, plural, setting, p_pos, p_neg, q_values,
         event_p, event_z, z_fact, cause_p, cause_z, other_bg) = item
        article = "an" if noun[0] in "aeiou" else "a"
        for event_index, (event_label, event) in enumerate(
                (("E_plus", event_p), ("E_minus", event_z))):
            vp, wrapup, _ref_question, _exp_question = event
            vignette = (f"There is {article} {noun} in {setting}. "
                        f"The {noun} is {p_pos}. The {noun} {z_fact}. "
                        f"{vp} the {noun} {wrapup}")
            for reason_index, (reason_label, reason) in enumerate(
                    (("P", cause_p), ("Z", cause_z))):
                condition_index = event_index * 2 + reason_index
                rows.append({
                    "norm_version": "z_causal_norm_v1",
                    "trial_id": f"{item_id}__{event_label}__{reason_label}",
                    "family_index": family_index,
                    "item_id": item_id,
                    "event": event_label,
                    "reason": reason_label,
                    "list_index": (family_index + condition_index) % 4,
                    "vignette": vignette,
                    "candidate_reason": reason,
                    "question": QUESTION,
                    "scale": SCALE,
                })

    assert len(rows) == 48, len(rows)
    for list_index in range(4):
        subset = [r for r in rows if r["list_index"] == list_index]
        assert len(subset) == 12, (list_index, len(subset))
        assert len({r["item_id"] for r in subset}) == 12, list_index
        counts = {}
        for r in subset:
            counts[(r["event"], r["reason"])] = counts.get((r["event"], r["reason"]), 0) + 1
        assert set(counts.values()) == {3}, (list_index, counts)
    print("Latin square certified: 4 lists x 12 trials, each family once, 3 per condition")

    args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with args.output_jsonl.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")
    with args.output_csv.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} norming trials to {args.output_jsonl} and {args.output_csv}")


if __name__ == "__main__":
    main()
