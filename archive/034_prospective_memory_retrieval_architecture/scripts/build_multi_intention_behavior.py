"""Build a delayed, two-intention prospective-memory focality experiment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ITEMS = [
    ("profession", "doctor", "basket", "doctor, nurse, or pilot", "workplaces and occupations", "musical instrument", "violin, cello, or flute"),
    ("musical instrument", "violin", "blanket", "violin, cello, or flute", "music rehearsals", "profession", "doctor, nurse, or pilot"),
    ("fruit", "orange", "lantern", "orange, apple, or pear", "grocery produce", "vehicle", "train, bicycle, or truck"),
    ("vehicle", "bicycle", "cabinet", "train, bicycle, or truck", "transportation", "fruit", "orange, apple, or pear"),
    ("bird", "sparrow", "notebook", "sparrow, eagle, or robin", "wildlife observations", "hand tool", "hammer, wrench, or saw"),
    ("hand tool", "hammer", "curtain", "hammer, wrench, or saw", "workshop equipment", "bird", "sparrow, eagle, or robin"),
    ("color word", "purple", "circle", "purple, yellow, or green", "paint selection", "emotion word", "joy, anger, or fear"),
    ("emotion word", "joy", "shelf", "joy, anger, or fear", "feelings and reactions", "color word", "purple, yellow, or green"),
    ("sport", "tennis", "pillow", "tennis, hockey, or cricket", "athletic events", "city name", "London, Tokyo, or Cairo"),
    ("city name", "Tokyo", "bucket", "London, Tokyo, or Cairo", "international travel", "sport", "tennis, hockey, or cricket"),
    ("piece of clothing", "jacket", "vase", "jacket, shirt, or scarf", "wardrobe planning", "beverage", "coffee, tea, or juice"),
    ("beverage", "coffee", "mirror", "coffee, tea, or juice", "cafe supplies", "piece of clothing", "jacket, shirt, or scarf"),
    ("animal", "rabbit", "folder", "rabbit, horse, or dolphin", "animal care", "furniture item", "table, sofa, or chair"),
    ("furniture item", "sofa", "ticket", "table, sofa, or chair", "home furnishings", "animal", "rabbit, horse, or dolphin"),
    ("weather word", "thunder", "wallet", "thunder, rain, or snow", "weather reports", "body part", "elbow, ankle, or wrist"),
    ("body part", "elbow", "parcel", "elbow, ankle, or wrist", "health examinations", "weather word", "thunder, rain, or snow"),
]

FILLERS = [
    "The wooden crate stayed near the wall.",
    "A small lamp rested on the desk.",
    "The plain envelope fell beside the door.",
    "A glass jar stood near the window.",
    "The empty box remained under the bench.",
    "A clean towel hung beside the sink.",
    "The paper note stayed inside the drawer.",
    "A metal tray rested near the cupboard.",
]


def cyclic_maps() -> list[dict[str, str]]:
    semantics = ["TARGET_ACTION", "OTHER_ACTION", "YES", "NO"]
    labels = ["A", "B", "C", "D"]
    return [dict(zip(semantics, labels[offset:] + labels[:offset])) for offset in range(4)]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    rows = []
    for item_index, (target_category, cue, control, target_examples, expected_topic,
                     other_category, other_examples) in enumerate(ITEMS):
        for cue_present in [False, True]:
            critical_word = cue if cue_present else control
            critical = f"The {critical_word} remained beside a window."
            if len(critical.rstrip(".").split()) != 6:
                raise ValueError(f"Critical sentence is not six words: {critical}")
            for focality in ["focal", "nonfocal"]:
                ongoing_rule = (
                    f"answer YES if the sentence names a {target_category} (for example, {target_examples}); otherwise answer NO"
                    if focality == "focal"
                    else "answer YES if the sentence contains exactly six words; otherwise answer NO"
                )
                no_cue_answer = "NO" if focality == "focal" else "YES"
                for expectancy in ["expected", "unexpected"]:
                    context = expected_topic if expectancy == "expected" else "routine household storage"
                    filler_records = "\n".join(
                        f"Earlier sentence {i + 1}: {sentence}" for i, sentence in enumerate(FILLERS)
                    )
                    for map_index, mapping in enumerate(cyclic_maps()):
                        correct_semantic = "TARGET_ACTION" if cue_present else no_cue_answer
                        inverse = {label: semantic for semantic, label in mapping.items()}
                        mapping_text = "; ".join(f"{label}={inverse[label]}" for label in ["A", "B", "C", "D"])
                        rows.append({
                            "stimulus_version": config["stimulus_version"], "semantic_id": f"multi_pm_{item_index:02d}",
                            "target_category": target_category, "other_category": other_category,
                            "cue": cue, "control_word": control, "cue_present": cue_present,
                            "focality": focality, "expectancy": expectancy, "mapping_index": map_index,
                            "semantic_to_label": mapping, "correct_semantic": correct_semantic,
                            "correct_label": mapping[correct_semantic], "critical_sentence": critical,
                            "prompt_text": (
                                "You are processing a stream of sentences while holding two future intentions.\n"
                                f"Future intention 1: if a later sentence names a {target_category} (for example, {target_examples}), "
                                "interrupt the ongoing task and perform TARGET_ACTION.\n"
                                f"Future intention 2: if a later sentence names a {other_category} (for example, {other_examples}), "
                                "interrupt and perform OTHER_ACTION.\n"
                                f"Ongoing task: {ongoing_rule}.\n"
                                f"Block context: the upcoming material is expected to concern {context}.\n"
                                f"{filler_records}\n"
                                f"Current sentence: {critical}\n"
                                f"Response mapping: {mapping_text}.\n"
                                "Apply the future intentions first; if neither triggers, do the ongoing task. Reply with exactly A, B, C, or D."
                            ),
                        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(rows), "semantic_items": len(ITEMS)}))


if __name__ == "__main__":
    main()
