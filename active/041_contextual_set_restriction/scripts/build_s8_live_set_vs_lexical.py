"""Does the role state track the live candidate set, or just a lexical match somewhere in the scene?

Every earlier design makes these two extensionally identical: whenever a modifier restricts, the
scene also contains an object matching the description on every dimension but that one. So a shallow
feature — "is there another object here that differs from the description only on my dimension" —
would score exactly as well as a referential role state, at any scale.

Here the scene and the live candidate set come apart. The question names which objects are live; the
scene always describes more objects than that.

    A  live_match     the differing-on-my-dimension object IS live   -> restricts,     lexical cue present
    B  offstage_match that object is in the scene but NOT live       -> does not,      lexical cue present
    C  no_match       no such object exists anywhere                 -> does not,      no lexical cue

    live-set account : A > B, and B close to C
    lexical account  : A close to B, both above C

Condition B is the one no previous version of this topic has ever run.
"""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path

from build_s0_restriction_swap import FAMILIES, LABELS, describe

CONDITIONS = ["live_match", "offstage_match", "no_match"]
DESCRIPTION_CONDITIONS = ["full", "drop_dim1", "drop_dim2"]
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
                for condition in CONDITIONS:
                    offset = world_index % len(LABELS)
                    labels = [LABELS[(offset + i) % len(LABELS)] for i in range(4)]
                    target = (labels[0], m1, m2)
                    # the object that differs from the target only on dimension 2
                    sharer = (labels[1], m1, other2)
                    # never a satisfier under any single omission
                    filler_a = (labels[2], other1, other2)
                    filler_b = (labels[3], other1, other2)
                    if condition == "live_match":
                        scene_objects = [target, sharer, filler_a, filler_b]
                        live = [target, sharer]
                    elif condition == "offstage_match":
                        scene_objects = [target, sharer, filler_a, filler_b]
                        live = [target, filler_a]
                    else:
                        scene_objects = [target, filler_a, filler_b,
                                         (labels[1], other1, other2)]
                        live = [target, filler_a]
                    presentation = scene_objects[world_index % 4 :] + scene_objects[: world_index % 4]
                    scene = "\n".join(f"Object {label} is a {value1} {value2} {noun}."
                                      for label, value1, value2 in presentation)
                    distractor = live[1]
                    live_order = live if world_index % 2 == 0 else list(reversed(live))
                    for description_condition in DESCRIPTION_CONDITIONS:
                        keep1 = description_condition in {"full", "drop_dim2"}
                        keep2 = description_condition in {"full", "drop_dim1"}
                        satisfiers = [label for label, value1, value2 in live
                                      if (not keep1 or value1 == m1) and (not keep2 or value2 == m2)]
                        scene_satisfiers = [label for label, value1, value2 in scene_objects
                                            if (not keep1 or value1 == m1) and (not keep2 or value2 == m2)]
                        for surface in SURFACE_FORMS:
                            phrase = describe(m1, m2, noun, surface, keep1, keep2)
                            for mapping_index in range(2):
                                options = ([target[0], distractor[0]] if mapping_index == 0
                                           else [distractor[0], target[0]])
                                option_text = "\n".join(f"{tag}) object {label}" for tag, label
                                                        in zip(["A", "B"], options))
                                gold_option = "A" if options[0] == target[0] else "B"
                                rows.append({
                                    "stimulus_version": config["stimulus_version"],
                                    "world_id": f"csr8_{world_index:03d}",
                                    "family": family, "noun": noun,
                                    "scene_condition": condition,
                                    "dim2_restricts_live_set": condition == "live_match",
                                    "dim2_lexical_match_in_scene": condition != "no_match",
                                    "description_condition": description_condition,
                                    "dropped_dimension": {"full": None, "drop_dim1": "dim1",
                                                          "drop_dim2": "dim2"}[description_condition],
                                    "n_live_satisfiers": len(satisfiers),
                                    "n_scene_satisfiers": len(scene_satisfiers),
                                    "surface_form": surface, "mapping_index": mapping_index,
                                    "target_label": target[0], "distractor_label": distractor[0],
                                    "gold_option": gold_option,
                                    "other_option": "B" if gold_option == "A" else "A",
                                    "description_phrase": phrase,
                                    "modifier_dim1": m1 if keep1 else None,
                                    "modifier_dim2": m2 if keep2 else None,
                                    "state_key": f"csr8_{world_index:03d}|{description_condition}|{surface}",
                                    "prompt_text": (
                                        "Scene: there are four objects on a table.\n"
                                        f"{scene}\n\n"
                                        f"Question: should we take object {live_order[0][0]} or "
                                        f"object {live_order[1][0]}?\n"
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
    print(json.dumps({"output": str(args.output), "rows": len(rows), "worlds": world_index}))


if __name__ == "__main__":
    main()
