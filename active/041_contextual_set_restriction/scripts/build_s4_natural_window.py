"""The Leffel et al. (2014) same-answer question-answer window, in natural language.

The synthetic worlds are the causal microscope; this is the published human paradigm that defines
the object. The critical answer phrase is held fixed and only the preceding question changes, so
the same modifier is contrastive in one context and merely descriptive in the other:

    Which chicken should the farmer slaughter?          -> "the fat chicken": fat restricts
    Should the farmer slaughter the chicken or the lamb? -> "the fat chicken": fat does not

A one-line scene makes both questions felicitous and holds the facts constant across contexts.
Two readouts, both natural: whether the modifier is needed to know which one is meant, and whether
the reduced answer already says which one is meant.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

# (agent, action, noun, modifier, contrast noun, plural of noun)
ITEMS = [
    ("farmer", "slaughter next", "chicken", "fat", "lamb", "chickens"),
    ("chef", "use for the stew", "onion", "red", "carrot", "onions"),
    ("curator", "hang in the main hall", "painting", "large", "tapestry", "paintings"),
    ("mechanic", "replace first", "tyre", "worn", "battery", "tyres"),
    ("librarian", "reshelve", "book", "torn", "magazine", "books"),
    ("gardener", "prune today", "rose", "tall", "hedge", "roses"),
    ("teacher", "collect", "notebook", "blue", "folder", "notebooks"),
    ("tailor", "mend first", "jacket", "grey", "scarf", "jackets"),
    ("carpenter", "sand down", "plank", "rough", "beam", "planks"),
    ("barista", "refill", "jug", "empty", "kettle", "jugs"),
    ("photographer", "print", "portrait", "blurred", "landscape", "portraits"),
    ("nurse", "restock", "cabinet", "lower", "trolley", "cabinets"),
    ("engineer", "inspect", "pipe", "cracked", "valve", "pipes"),
    ("baker", "glaze", "loaf", "dark", "pastry", "loaves"),
    ("archivist", "digitise", "letter", "faded", "diary", "letters"),
    ("cellist", "restring", "cello", "older", "violin", "cellos"),
    ("driver", "unload", "crate", "heavy", "sack", "crates"),
    ("editor", "revise", "chapter", "final", "preface", "chapters"),
    ("florist", "water", "orchid", "wilting", "fern", "orchids"),
    ("jeweller", "polish", "ring", "silver", "brooch", "rings"),
    ("vet", "examine", "puppy", "limping", "kitten", "puppies"),
    ("caretaker", "unlock", "gate", "rusty", "shed", "gates"),
    ("brewer", "bottle", "barrel", "older", "cask", "barrels"),
    ("printer", "reload", "tray", "lower", "cartridge", "trays"),
    ("sailor", "coil", "rope", "frayed", "chain", "ropes"),
    ("potter", "fire", "bowl", "glazed", "vase", "bowls"),
    ("cyclist", "pump up", "tube", "flat", "saddle", "tubes"),
    ("weaver", "finish", "rug", "narrow", "blanket", "rugs"),
    ("glazier", "replace", "pane", "cracked", "frame", "panes"),
    ("cook", "chop", "pepper", "green", "aubergine", "peppers"),
    ("pilot", "check", "gauge", "left", "lever", "gauges"),
    ("blacksmith", "reheat", "rod", "bent", "plate", "rods"),
    ("astronomer", "clean", "lens", "smudged", "mirror", "lenses"),
    ("miller", "open", "sack", "damp", "bin", "sacks"),
    ("dyer", "rinse", "cloth", "stained", "thread", "cloths"),
    ("sculptor", "move", "block", "cracked", "slab", "blocks"),
    ("beekeeper", "open", "hive", "quiet", "shed", "hives"),
    ("mason", "lay", "brick", "chipped", "tile", "bricks"),
    ("cobbler", "resole", "boot", "worn", "sandal", "boots"),
    ("vintner", "decant", "bottle", "dusty", "carafe", "bottles"),
]

CONTEXTS = ["restricting", "non_restricting"]
ANSWER_FORMS = ["full", "reduced"]
PROBES = ["modifier_needed", "answer_adequacy"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    rows = []
    for index, (agent, action, noun, modifier, contrast, plural) in enumerate(ITEMS):
        scene = f"The {agent} keeps several {plural} and one {contrast}."
        # Both questions are clefts so they stay parallel whatever the action phrase is; only the
        # set of live alternatives differs.
        questions = {
            "restricting": f"Which {noun} is it that the {agent} should {action}?",
            "non_restricting": f"Is it the {noun} or the {contrast} that the {agent} should {action}?",
        }
        for context in CONTEXTS:
            for answer_form in ANSWER_FORMS:
                answer = (f"The {modifier} {noun}." if answer_form == "full" else f"The {noun}.")
                for probe in PROBES:
                    if probe == "modifier_needed":
                        if answer_form == "reduced":
                            continue
                        question = (f"Is the word '{modifier}' needed here to know which one is "
                                    "meant?")
                        gold_yes = context == "restricting"
                    else:
                        question = "Does the reply already say which one is meant?"
                        gold_yes = not (context == "restricting" and answer_form == "reduced")
                    for mapping_index in range(2):
                        options = (["yes", "no"] if mapping_index == 0 else ["no", "yes"])
                        gold_option = "A" if options[0] == ("yes" if gold_yes else "no") else "B"
                        option_text = "\n".join(f"{tag}) {value}" for tag, value
                                                in zip(["A", "B"], options))
                        rows.append({
                            "stimulus_version": config["stimulus_version"],
                            "item_id": f"leffel_{index:02d}", "agent": agent, "noun": noun,
                            "modifier": modifier, "contrast_noun": contrast,
                            "context": context, "answer_form": answer_form, "probe": probe,
                            "gold_answer": "yes" if gold_yes else "no",
                            "gold_option": gold_option,
                            "other_option": "B" if gold_option == "A" else "A",
                            "mapping_index": mapping_index,
                            "prompt_text": (
                                f"{scene}\n"
                                f"Question: {questions[context]}\n"
                                f"Reply: {answer}\n\n"
                                f"{question}\n{option_text}\n"
                                "Answer with exactly A or B."
                            ),
                        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(rows), "items": len(ITEMS)}))


if __name__ == "__main__":
    main()
