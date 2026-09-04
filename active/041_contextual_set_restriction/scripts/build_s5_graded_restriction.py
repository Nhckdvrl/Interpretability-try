"""Is the state a binary role, or graded by how much the modifier actually narrows the set?

S0-S3 only ever contrast restricts / does not restrict. If the modifier-token state is really a
`SetRestrictionRole`, a natural next question is what quantity it carries: a binary flag, or the
size of the reduction the modifier is responsible for.

Each live set holds four objects with the described facts held constant:

    T  = (m1, m2)                      the target
    k  objects sharing m1, differing on dim2      -> dropping m2 admits k more satisfiers
    3-k objects differing on both dims            -> never satisfiers

so dimension 2 restricts with degree k in {0, 1, 2, 3} while dimension 1 never restricts and gives
the within-world k = 0 baseline. Candidate-set size, number of described objects and both lexical
modifiers are identical across all four degrees; only which objects fill the set changes.
"""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path

from build_s0_restriction_swap import FAMILIES, LABELS, describe

DEGREES = [0, 1, 2, 3]
SURFACE_FORMS = ["np", "relative_21"]
CONDITIONS = ["full", "drop_dim1", "drop_dim2"]


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
                for degree in DEGREES:
                    offset = world_index % len(LABELS)
                    labels = [LABELS[(offset + i) % len(LABELS)] for i in range(4)]
                    objects = [(labels[0], m1, m2)]
                    objects += [(labels[1 + i], m1, other2) for i in range(degree)]
                    objects += [(labels[1 + degree + i], other1, other2)
                                for i in range(3 - degree)]
                    presentation = objects[world_index % 4 :] + objects[: world_index % 4]
                    scene = "\n".join(f"Object {label} is a {value1} {value2} {noun}."
                                      for label, value1, value2 in presentation)
                    # the distractor is a sharer when one exists, otherwise a both-differ object
                    distractor = objects[1]
                    for condition in CONDITIONS:
                        keep1 = condition in {"full", "drop_dim2"}
                        keep2 = condition in {"full", "drop_dim1"}
                        satisfiers = [label for label, value1, value2 in objects
                                      if (not keep1 or value1 == m1) and (not keep2 or value2 == m2)]
                        for surface in SURFACE_FORMS:
                            phrase = describe(m1, m2, noun, surface, keep1, keep2)
                            for mapping_index in range(2):
                                options = ([labels[0], distractor[0]] if mapping_index == 0
                                           else [distractor[0], labels[0]])
                                option_text = "\n".join(f"{tag}) object {label}" for tag, label
                                                        in zip(["A", "B"], options))
                                gold_option = "A" if options[0] == labels[0] else "B"
                                rows.append({
                                    "stimulus_version": config["stimulus_version"],
                                    "world_id": f"csr5_{world_index:03d}",
                                    "family": family, "noun": noun,
                                    "restriction_degree": degree,
                                    "description_condition": condition,
                                    "dropped_dimension": {"full": None, "drop_dim1": "dim1",
                                                          "drop_dim2": "dim2"}[condition],
                                    "n_satisfiers": len(satisfiers),
                                    "surface_form": surface, "mapping_index": mapping_index,
                                    "target_label": labels[0], "distractor_label": distractor[0],
                                    "gold_option": gold_option,
                                    "other_option": "B" if gold_option == "A" else "A",
                                    "description_phrase": phrase,
                                    "modifier_dim1": m1 if keep1 else None,
                                    "modifier_dim2": m2 if keep2 else None,
                                    "state_key": f"csr5_{world_index:03d}|{condition}|{surface}",
                                    "prompt_text": (
                                        "Scene: there are four objects on a table.\n"
                                        f"{scene}\n\n"
                                        "Question: which of these objects do you mean?\n"
                                        f"Reply: I mean {phrase}.\n\n"
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
    print(json.dumps({"output": str(args.output), "rows": len(rows), "worlds": world_index}))


if __name__ == "__main__":
    main()
