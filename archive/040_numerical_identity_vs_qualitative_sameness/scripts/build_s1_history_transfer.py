"""Build the arbitrary-history causal recipient from all released event frames."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

import openpyxl


def rows(path: Path) -> list[tuple[str, str]]:
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True).active
    return [(str(a).strip(), str(b).strip()) for a, b in ws.iter_rows(min_row=2, max_col=2, values_only=True) if a and b]


def object_type(different_second_sentence: str) -> str:
    match = re.search(r"\banother\s+(.+?)\.$", different_second_sentence, flags=re.I)
    if not match:
        raise ValueError(f"Cannot recover object type from: {different_second_sentence}")
    return match.group(1)


def replace_final_np(sentence: str, replacement: str) -> str:
    match = re.match(r"^(.*)\b(?:the|another|some other|his|her)\b[^.]*\.?$", sentence, flags=re.I)
    changed = f"{match.group(1)}{replacement}." if match else sentence
    if changed == sentence:
        raise ValueError(f"Cannot replace final NP: {sentence}")
    return changed


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source-root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    source = args.source_root / "experimentnorming"
    same = rows(source / "stimuli" / "multi_sent.xlsx")
    different = rows(source / "stimuli" / "multi_sent_another.xlsx")
    if len(same) != 62 or len(different) != 62:
        raise ValueError("Released event rows are incomplete")
    released_types = [object_type(second) for _, second in different]
    commit = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    records = []
    for row_index, ((first, same_second), (_, different_second)) in enumerate(zip(same, different)):
        noun = object_type(different_second)
        different_noun = released_types[(row_index + 2) % len(released_types)]
        if different_noun == noun:
            raise ValueError(f"Different-type control failed for row {row_index}: {noun}")
        frame = row_index // 2
        state_change = "minimal" if row_index % 2 == 0 else "substantial"
        first_event = replace_final_np(first, "Object Alpha")
        for competitor_relation in ["same_type", "different_type"]:
            beta_noun = noun if competitor_relation == "same_type" else different_noun
            for object_order in ["alpha_first", "beta_first"]:
                introductions = (
                    f"Object Alpha is an item of type '{noun}' carrying the episode code DAX. "
                    f"Object Beta is a different item of type '{beta_noun}' carrying the episode code VEK. "
                    if object_order == "alpha_first"
                    else f"Object Beta is an item of type '{beta_noun}' carrying the episode code VEK. "
                    f"Object Alpha is a different item of type '{noun}' carrying the episode code DAX. "
                )
                for identity in ["same_token", "different_token"]:
                    target_object_type = noun if identity == "same_token" else beta_noun
                    relation_clause = "which is of the same kind" if competitor_relation == "same_type" else "which is of a different kind"
                    for cue_family in ["explicit_object_label", "continuity_description"]:
                        if cue_family == "explicit_object_label":
                            target = "Object Alpha" if identity == "same_token" else "Object Beta"
                            second_event = replace_final_np(same_second, target)
                            bridge = ""
                        else:
                            if identity == "same_token":
                                bridge = "The item from the first event remains present and continues into the next event. "
                                target = "that continuing item"
                            else:
                                bridge = f"The item from the first event is set aside, and the other item, {relation_clause}, takes its place. "
                                target = "that replacement item"
                            second_event = replace_final_np(same_second, target)
                        passage = f"{introductions}{first_event} {bridge}{second_event}"
                        base = {
                            "item_id": f"s1_row{row_index:02d}_{competitor_relation}_{object_order}_{identity}_{cue_family}",
                            "source_row": row_index,
                            "frame": frame,
                            "state_change": state_change,
                            "identity": identity,
                            "cue_family": cue_family,
                            "object_order": object_order,
                            "competitor_relation": competitor_relation,
                            "object_type": noun,
                            "target_object_type": target_object_type,
                            "passage": passage,
                            "source_commit": commit,
                            "stimulus_version": "s1_v3_competitor_type_control",
                        }
                        for label_order in ["target_first", "target_second"]:
                            target_label, foil_label = ("A", "B") if label_order == "target_first" else ("B", "A")
                            gold_code = "DAX" if identity == "same_token" else "VEK"
                            foil_code = "VEK" if gold_code == "DAX" else "DAX"
                            records.append({
                                **base, "item_id": f"{base['item_id']}_history_{label_order}", "readout": "history_transfer",
                                "label_order": label_order, "target_label": target_label, "foil_label": foil_label,
                                "question": (
                                    "Which episode code belongs to the item in the second event?\n"
                                    f"{target_label}: {gold_code}\n{foil_label}: {foil_code}"
                                ),
                            })
                            records.append({
                                **base, "item_id": f"{base['item_id']}_type_{label_order}", "readout": "type_knowledge",
                                "label_order": label_order, "target_label": target_label, "foil_label": foil_label,
                                "question": (
                                    "What kind of object is involved in the second event?\n"
                                    f"{target_label}: {target_object_type}\n{foil_label}: a completely unrelated kind of object"
                                ),
                            })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps({"records": len(records), "source_rows": len(same), "source_commit": commit}))


if __name__ == "__main__":
    main()
