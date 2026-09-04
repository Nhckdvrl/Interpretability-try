"""Build the final PM microscope without word counting or exact cue repetition."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_multi_intention_behavior import FILLERS, ITEMS, cyclic_maps


def members(text: str) -> list[str]:
    return [value.strip() for value in text.replace(", or ", ", ").split(",")]


def example_text(values: list[str], excluded: str) -> str:
    kept = [value for value in values if value != excluded]
    if len(kept) != 2:
        raise ValueError(f"Expected two non-cue examples after excluding {excluded}: {values}")
    return f"{kept[0]} or {kept[1]}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    rows = []
    for item_index, (target_category, target_cue, control, target_examples, _expected_topic,
                     other_category, other_examples) in enumerate(ITEMS):
        target_members = members(target_examples)
        other_members = members(other_examples)
        other_cue = other_members[0]
        target_example_text = example_text(target_members, target_cue)
        other_example_text = example_text(other_members, other_cue)
        cue_words = {"none": control, "target": target_cue, "other": other_cue}
        for cue_type, critical_word in cue_words.items():
            critical = f"The {critical_word} remained beside a window."
            for focality in ["focal", "nonfocal"]:
                if focality == "focal":
                    ongoing_rule = (
                        f"answer YES if the sentence names a {target_category} "
                        f"(for example, {target_example_text}); otherwise answer NO"
                    )
                    ongoing_answer = "YES" if cue_type == "target" else "NO"
                else:
                    ongoing_rule = "answer YES if the sentence begins with the word 'The'; otherwise answer NO"
                    ongoing_answer = "YES"
                for expectancy in ["expected", "unexpected"]:
                    expectancy_text = (
                        "A future-intention cue is likely to appear in this block."
                        if expectancy == "expected"
                        else "A future-intention cue is unlikely to appear in this block."
                    )
                    fillers = "\n".join(f"Earlier sentence {i + 1}: {sentence}" for i, sentence in enumerate(FILLERS))
                    for map_index, mapping in enumerate(cyclic_maps()):
                        correct_semantic = {
                            "target": "TARGET_ACTION", "other": "OTHER_ACTION", "none": ongoing_answer
                        }[cue_type]
                        inverse = {label: semantic for semantic, label in mapping.items()}
                        mapping_text = "; ".join(f"{label}={inverse[label]}" for label in ["A", "B", "C", "D"])
                        rows.append({
                            "stimulus_version": config["stimulus_version"],
                            "semantic_id": f"multi_pm_v2_{item_index:02d}",
                            "target_category": target_category, "other_category": other_category,
                            "target_cue": target_cue, "other_cue": other_cue, "control_word": control,
                            "cue_type": cue_type, "focality": focality, "expectancy": expectancy,
                            "mapping_index": map_index, "semantic_to_label": mapping,
                            "correct_semantic": correct_semantic, "correct_label": mapping[correct_semantic],
                            "critical_sentence": critical,
                            "prompt_text": (
                                "You are processing a stream of sentences while holding two future intentions.\n"
                                f"Future intention 1: if a later sentence names a {target_category} "
                                f"(for example, {target_example_text}), interrupt the ongoing task and perform TARGET_ACTION.\n"
                                f"Future intention 2: if a later sentence names a {other_category} "
                                f"(for example, {other_example_text}), interrupt and perform OTHER_ACTION.\n"
                                f"Ongoing task: {ongoing_rule}.\n"
                                f"Cue expectancy: {expectancy_text}\n"
                                f"{fillers}\nCurrent sentence: {critical}\n"
                                f"Response mapping: {mapping_text}.\n"
                                "Apply the future intentions first; if neither triggers, do the ongoing task. "
                                "Reply with exactly A, B, C, or D."
                            ),
                        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(rows), "semantic_items": len(ITEMS)}))


if __name__ == "__main__":
    main()
