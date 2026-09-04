"""Build the frozen S0 role-swap microscope for contextual set restriction.

Each world holds three fully described objects and one fixed target description. Only the live
candidate set changes, so the same lexical modifier switches between restricting and
non-restricting with every object fact, the target phrase and the world size held constant.

    A = large red circle   (target)
    B = large blue circle  (differs from A on dimension 2)
    C = small red circle   (differs from A on dimension 1)

    live {A, B}: dimension-2 modifier restricts, dimension-1 modifier does not
    live {A, C}: dimension-1 modifier restricts, dimension-2 modifier does not

Gold is computed from denotations, never from a model or a hand label: a modifier restricts iff
dropping it increases the number of live candidates satisfying the description.
"""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path

# (family, dimension-1 values, dimension-2 values, nouns)
FAMILIES = [
    ("size_color", ("large", "small"), ("red", "blue"), ("circle", "square", "triangle", "block")),
    ("material_color", ("wooden", "plastic"), ("green", "yellow"), ("box", "tray", "handle", "frame")),
    ("texture_color", ("rough", "smooth"), ("black", "white"), ("stone", "tile", "panel", "sheet")),
    ("pattern_length", ("striped", "spotted"), ("long", "short"), ("ribbon", "scarf", "band", "strap")),
    ("fill_height", ("full", "empty"), ("tall", "flat"), ("bottle", "jar", "glass", "flask")),
    ("color_curvature", ("orange", "purple"), ("curved", "straight"), ("rod", "wire", "pipe", "bar")),
]

LABELS = ["P", "Q", "R", "S", "T", "V", "W", "Z"]
DESCRIPTION_CONDITIONS = ["full", "drop_dim1", "drop_dim2", "bare"]
SURFACE_FORMS = ["np", "relative_12", "relative_21"]
QUESTION_FORMS = [
    "Should we take object {first} or object {second}?",
    "Are you asking about object {first} or about object {second}?",
]


def describe(dim1: str, dim2: str, noun: str, surface: str, keep1: bool, keep2: bool) -> str:
    kept = [value for value, keep in ((dim1, keep1), (dim2, keep2)) if keep]
    if surface == "np":
        return f"the {' '.join(kept + [noun])}" if kept else f"the {noun}"
    ordered = kept if surface == "relative_12" else list(reversed(kept))
    if not ordered:
        return f"the {noun}"
    if len(ordered) == 1:
        return f"the {noun} that is {ordered[0]}"
    return f"the {noun} that is {ordered[0]} and {ordered[1]}"


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
                a1, a2 = dim1_values[target1], dim2_values[target2]
                b1, b2 = a1, dim2_values[1 - target2]          # shares dim1, differs on dim2
                c1, c2 = dim1_values[1 - target1], a2          # differs on dim1, shares dim2
                offset = world_index % len(LABELS)
                label_a, label_b, label_c = (LABELS[(offset + i) % len(LABELS)] for i in range(3))
                objects = [(label_a, a1, a2), (label_b, b1, b2), (label_c, c1, c2)]
                presentation = objects[world_index % 3 :] + objects[: world_index % 3]
                scene = "\n".join(f"Object {label} is a {value1} {value2} {noun}."
                                  for label, value1, value2 in presentation)
                for context, distractor in [("AB", (label_b, b1, b2)), ("AC", (label_c, c1, c2))]:
                    live = [(label_a, a1, a2), distractor]
                    ordered_live = live if world_index % 2 == 0 else list(reversed(live))
                    for condition in DESCRIPTION_CONDITIONS:
                        keep1 = condition in {"full", "drop_dim2"}
                        keep2 = condition in {"full", "drop_dim1"}
                        satisfying = [label for label, value1, value2 in live
                                      if (not keep1 or value1 == a1) and (not keep2 or value2 == a2)]
                        for surface in SURFACE_FORMS:
                            phrase = describe(a1, a2, noun, surface, keep1, keep2)
                            for question_index, question in enumerate(QUESTION_FORMS):
                                for mapping_index in range(2):
                                    option_labels = ["A", "B"]
                                    options = (ordered_live if mapping_index == 0
                                               else list(reversed(ordered_live)))
                                    option_text = "\n".join(
                                        f"{tag}) object {entry[0]}"
                                        for tag, entry in zip(option_labels, options))
                                    target_option = option_labels[[entry[0] for entry in options].index(label_a)]
                                    rows.append({
                                        "stimulus_version": config["stimulus_version"],
                                        "world_id": f"csr_{world_index:03d}",
                                        "family": family, "noun": noun,
                                        "target_dim1": a1, "target_dim2": a2,
                                        "context": context,
                                        "restricting_dimension": "dim2" if context == "AB" else "dim1",
                                        "description_condition": condition,
                                        "dropped_dimension": {"full": None, "bare": "both",
                                                              "drop_dim1": "dim1",
                                                              "drop_dim2": "dim2"}[condition],
                                        "dropped_modifier_is_restricting": (
                                            None if condition in {"full", "bare"} else
                                            ({"drop_dim1": "dim1", "drop_dim2": "dim2"}[condition]
                                             == ("dim2" if context == "AB" else "dim1"))),
                                        "n_live_satisfying": len(satisfying),
                                        "unique_in_live_set": len(satisfying) == 1,
                                        "surface_form": surface, "question_form": question_index,
                                        "mapping_index": mapping_index,
                                        "target_label": label_a, "distractor_label": distractor[0],
                                        "target_option": target_option,
                                        "distractor_option": "B" if target_option == "A" else "A",
                                        "prompt_text": (
                                            "Scene: there are three objects on a table.\n"
                                            f"{scene}\n\n"
                                            f"Question: {question.format(first=ordered_live[0][0], second=ordered_live[1][0])}\n"
                                            f"Reply: Take {phrase}.\n\n"
                                            "Which object does the reply mean?\n"
                                            f"{option_text}\n"
                                            "Answer with exactly A or B."
                                        ),
                                    })
                world_index += 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(rows),
                      "worlds": world_index, "families": len(FAMILIES)}))


if __name__ == "__main__":
    main()
