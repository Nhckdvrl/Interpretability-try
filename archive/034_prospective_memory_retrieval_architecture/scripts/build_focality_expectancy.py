"""Build the frozen S0-2 focality x context-expectancy PM microscope."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


ITEMS = [
    ("passport", "renew the passport", "official identity document", "The passport lies beside the keyboard.", "The driver's license lies beside the keyboard.", "international travel planning"),
    ("invoice", "forward the invoice to accounting", "financial document", "The invoice is clipped to the memo.", "The receipt is clipped to the memo.", "bookkeeping and payments"),
    ("violin", "book the violin for tuning", "string instrument", "The violin is inside the black case.", "The cello is inside the black case.", "orchestra equipment"),
    ("aspirin", "record the aspirin dose", "pain reliever", "The aspirin is in the top drawer.", "The ibuprofen is in the top drawer.", "medication supplies"),
    ("oak tree", "schedule the oak tree inspection", "deciduous tree", "The oak tree shades the south fence.", "The maple tree shades the south fence.", "garden maintenance"),
    ("USB cable", "pack the USB cable", "electronic cable", "The USB cable is behind the monitor.", "The HDMI cable is behind the monitor.", "computer equipment"),
    ("thermometer", "calibrate the thermometer", "medical instrument", "The thermometer is on the steel tray.", "The blood-pressure cuff is on the steel tray.", "clinic equipment"),
    ("train ticket", "validate the train ticket", "transit ticket", "The train ticket is in the side pocket.", "The bus ticket is in the side pocket.", "public transportation"),
    ("bronze key", "copy the bronze key", "door key", "The bronze key is under the notepad.", "The silver key is under the notepad.", "building access"),
    ("coffee mug", "wash the coffee mug", "piece of drinkware", "The coffee mug is beside the sink.", "The tea cup is beside the sink.", "kitchen supplies"),
    ("blue folder", "archive the blue folder", "office filing item", "The blue folder is on the lower shelf.", "The red binder is on the lower shelf.", "office records"),
    ("bicycle helmet", "inspect the bicycle helmet", "protective helmet", "The bicycle helmet hangs near the door.", "The motorcycle helmet hangs near the door.", "protective equipment"),
    ("fire alarm", "test the fire alarm", "fire-safety device", "The fire alarm is above the exit sign.", "The smoke detector is above the exit sign.", "workplace fire safety"),
    ("red umbrella", "return the red umbrella", "piece of rain gear", "The red umbrella is in the front closet.", "The blue raincoat is in the front closet.", "wet-weather equipment"),
    ("kettle", "descale the kettle", "water-heating vessel", "The kettle is on the rear counter.", "The electric urn is on the rear counter.", "hot-drink preparation"),
    ("flashlight", "replace the flashlight batteries", "portable light source", "The flashlight is in the emergency box.", "The lantern is in the emergency box.", "emergency lighting"),
]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    labels = ["A", "B", "C"]
    semantic_options = ["REMINDER", "YES", "NO"]
    rows = []
    for item_index, (cue, action, category, cue_note, control_note, expected_topic) in enumerate(ITEMS):
        for cue_present, focality, expectancy, permutation in itertools.product(
            [False, True], ["focal", "nonfocal"], ["expected", "unexpected"], itertools.permutations(labels)
        ):
            mapping = dict(zip(semantic_options, permutation))
            note = cue_note if cue_present else control_note
            ongoing_answer = "YES" if focality == "focal" else "NO"
            correct_semantic = "REMINDER" if cue_present else ongoing_answer
            context = (
                f"The next batch is about {expected_topic}."
                if expectancy == "expected"
                else "The next batch is about routine room cleaning."
            )
            ongoing_rule = (
                f"Answer YES when a note mentions an item in this category: {category}; otherwise answer NO."
                if focality == "focal"
                else "Answer YES when a note explicitly praises or approves of something; otherwise answer NO."
            )
            rows.append({
                "stimulus_version": config["stimulus_version"],
                "semantic_id": f"pm_{item_index:02d}",
                "cue": cue,
                "action": action,
                "cue_present": cue_present,
                "focality": focality,
                "expectancy": expectancy,
                "critical_note": note,
                "label_map": mapping,
                "correct_semantic": correct_semantic,
                "correct_label": mapping[correct_semantic],
                "prompt_text": (
                    "Process the final incoming note under these rules.\n"
                    f"Ongoing task: {ongoing_rule}\n"
                    f"Future intention: If an incoming note contains the exact target phrase '{cue}', "
                    f"override the ongoing task and carry out this reminder: {action}.\n"
                    f"Current context: {context}\n"
                    "The prior two notes were 'A plain envelope is on the table.' and "
                    "'A wooden stool is near the wall.' Neither contained the target phrase.\n"
                    f"Final incoming note: {note}\n"
                    f"Response mapping: A={next(k for k,v in mapping.items() if v == 'A')}; "
                    f"B={next(k for k,v in mapping.items() if v == 'B')}; "
                    f"C={next(k for k,v in mapping.items() if v == 'C')}.\n"
                    "Reply with exactly A, B, or C."
                ),
            })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "n": len(rows), "semantic_items": len(ITEMS)}))


if __name__ == "__main__":
    main()
