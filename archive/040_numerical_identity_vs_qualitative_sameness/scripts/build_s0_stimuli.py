"""Build the frozen 040 S0 panel from the released Davis–Altmann carrier."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

import openpyxl


def rows(path: Path) -> list[tuple[str, str]]:
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True).active
    out = []
    for sent1, sent2 in ws.iter_rows(min_row=2, max_col=2, values_only=True):
        if sent1 and sent2:
            out.append((str(sent1).strip(), str(sent2).strip()))
    return out


def replace_final_referent_with_that_item(sentence: str) -> str:
    """Remove the released determiner cue while preserving the event predicate."""
    replaced = re.sub(
        r"\b(?:the|another|some other|his|her)\b[^.]*\.$",
        "that item.",
        sentence,
        count=1,
        flags=re.I,
    )
    if replaced == sentence:
        raise ValueError(f"Could not replace final referent in: {sentence}")
    return replaced


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source-root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()

    source_dir = args.source_root / "experimentnorming"
    same = rows(source_dir / "stimuli" / "multi_sent.xlsx")
    different = rows(source_dir / "stimuli" / "multi_sent_another.xlsx")
    if len(same) != 62 or len(different) != 62:
        raise ValueError(f"Expected 62 rows per identity condition, got {len(same)}, {len(different)}")
    commit = subprocess.check_output(["git", "-C", str(source_dir), "rev-parse", "HEAD"], text=True).strip()

    records = []
    for row_index, ((same_s1, same_s2), (diff_s1, diff_s2)) in enumerate(zip(same, different)):
        if same_s1 != diff_s1:
            raise ValueError(f"First-sentence mismatch at row {row_index}")
        frame = row_index // 2
        state_change = "minimal" if row_index % 2 == 0 else "substantial"
        for identity, released_s2 in [("same_token", same_s2), ("different_token_same_type", diff_s2)]:
            for cue_family in ["released_determiner", "continuity_description"]:
                if cue_family == "released_determiner":
                    passage = f"{same_s1} {released_s2}"
                else:
                    bridge = (
                        "The very same physical item remains present for the next event."
                        if identity == "same_token"
                        else "The original item is set aside, and a distinct physical item of the same kind takes its place for the next event."
                    )
                    passage = f"{same_s1} {bridge} {replace_final_referent_with_that_item(same_s2)}"
                base = {
                    "item_id": f"frame{frame:02d}_row{row_index:02d}_{identity}_{cue_family}",
                    "frame": frame,
                    "source_row": row_index,
                    "state_change": state_change,
                    "identity": identity,
                    "cue_family": cue_family,
                    "passage": passage,
                    "source_commit": commit,
                    "stimulus_version": "s0_v3_label_counterbalanced_clean_continuity",
                }
                for label_order in ["same_first", "different_first"]:
                    same_label, different_label = ("A", "B") if label_order == "same_first" else ("B", "A")
                    labeled_base = {**base, "item_id": f"{base['item_id']}_{label_order}", "label_order": label_order}
                    records.append(
                        {
                            **labeled_base,
                            "readout": "history_transfer",
                            "question": (
                                "Which statement correctly describes the two events?\n"
                                f"{same_label}: The same physical item participates in both events.\n"
                                f"{different_label}: Different physical items participate in the two events."
                            ),
                            "same_label": same_label,
                            "different_label": different_label,
                            "gold_semantic": "same" if identity == "same_token" else "different",
                        }
                    )
                    records.append(
                        {
                            **labeled_base,
                            "readout": "type_knowledge",
                            "question": (
                                "Which statement correctly describes the kinds of items in the two events?\n"
                                f"{same_label}: The items are the same kind of thing.\n"
                                f"{different_label}: The items are different kinds of things."
                            ),
                            "same_label": same_label,
                            "different_label": different_label,
                            "gold_semantic": "same",
                        }
                    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps({"records": len(records), "frames": 31, "source_commit": commit, "output": str(args.output)}))


if __name__ == "__main__":
    main()
