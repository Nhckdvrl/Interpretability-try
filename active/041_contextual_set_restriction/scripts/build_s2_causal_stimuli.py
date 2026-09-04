"""Held-out-family worlds for the causal test, with a matched raw-property-truth probe.

Both probes share the identical prompt up to the final question, so the modifier tokens the
intervention edits sit at the same positions in both. `property_truth` is the preservation
denominator required by H3: the same edit must not destroy knowledge that an object has the
property, only which modifier the model leans on for reference.
"""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path

from build_s0_restriction_swap import FAMILIES, LABELS, describe

PROBES = ["reference", "property_truth"]
SURFACE_FORMS = ["np", "relative_21"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    rows = []
    world_index = 0
    for family, dim1_values, dim2_values, nouns in FAMILIES:
        for noun in nouns:
            for target1, target2 in product(range(2), range(2)):
                m1, m2 = dim1_values[target1], dim2_values[target2]
                other1, other2 = dim1_values[1 - target1], dim2_values[1 - target2]
                for restricting in ["dim1", "dim2"]:
                    n1, n2 = (other1, m2) if restricting == "dim1" else (m1, other2)
                    distinguishing = other1 if restricting == "dim1" else other2
                    for uniqueness in ["unique", "duplicate"]:
                        offset = world_index % len(LABELS)
                        label_t, label_n, label_extra = (LABELS[(offset + i) % len(LABELS)] for i in range(3))
                        extra = (m1, m2) if uniqueness == "duplicate" else (other1, other2)
                        objects = [(label_t, m1, m2), (label_n, n1, n2), (label_extra, *extra)]
                        presentation = objects[world_index % 3 :] + objects[: world_index % 3]
                        scene = "\n".join(f"Object {label} is a {value1} {value2} {noun}."
                                          for label, value1, value2 in presentation)
                        for surface, probe in ((surface, probe) for surface in SURFACE_FORMS
                                               for probe in PROBES):
                            phrase = describe(m1, m2, noun, surface, True, True)
                            question, gold_label = (
                                ("Which object does the reply mean?", label_t) if probe == "reference"
                                else (f"Which object is {distinguishing}?", label_n))
                            for mapping_index in range(2):
                                options = ([label_t, label_n] if mapping_index == 0
                                           else [label_n, label_t])
                                option_text = "\n".join(f"{tag}) object {label}" for tag, label
                                                        in zip(["A", "B"], options))
                                gold_option = "A" if options[0] == gold_label else "B"
                                rows.append({
                                    "stimulus_version": config["stimulus_version"],
                                    "world_id": f"csr2_{world_index:03d}",
                                    "family": family, "noun": noun, "probe": probe,
                                    "surface_form": surface,
                                    "restricting_dimension": restricting, "uniqueness": uniqueness,
                                    "mapping_index": mapping_index,
                                    "target_label": label_t, "distractor_label": label_n,
                                    "gold_option": gold_option,
                                    "other_option": "B" if gold_option == "A" else "A",
                                    "target_option": "A" if options[0] == label_t else "B",
                                    "distractor_option": "A" if options[0] == label_n else "B",
                                    "description_phrase": phrase,
                                    "modifier_dim1": m1, "modifier_dim2": m2,
                                    "prompt_text": (
                                        "Scene: there are three objects on a table.\n"
                                        f"{scene}\n\n"
                                        "Question: which of these objects do you mean?\n"
                                        f"Reply: I mean {phrase}.\n\n"
                                        f"{question}\n{option_text}\n"
                                        "Answer with exactly A or B."
                                    ),
                                })
                        world_index += 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(rows), "worlds": world_index}))


if __name__ == "__main__":
    main()
