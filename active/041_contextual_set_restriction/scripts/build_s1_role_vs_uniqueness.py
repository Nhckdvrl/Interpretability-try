"""Cross modifier restriction with description uniqueness, which S0 could not separate.

In the S0 worlds a modifier restricts exactly when dropping it destroys the unique reference, so
`SetRestrictionRole` and `is the description still unique` are perfectly confounded. A role state
that is really just a uniqueness/ambiguity signal would pass S0 unchanged.

Here the live set has three objects and the readout is satisfier-vs-non-satisfier, which stays
well defined when two objects satisfy the description:

    unique world     T=(m1,m2)  N=(differs on the restricting dimension)  X=(differs on both)
    duplicate world  T=(m1,m2)  T'=(m1,m2)                                N=(as above)

    dropping the restricting modifier makes N a satisfier -> margin should collapse
    dropping the other modifier leaves N a non-satisfier  -> margin should survive

and this should hold identically in both worlds, because uniqueness of the description is
irrelevant to whether a modifier restricts. Which dimension restricts is swapped across worlds, so
the same lexical modifier appears in both roles.
"""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path

from build_s0_restriction_swap import FAMILIES, LABELS, describe

DESCRIPTION_CONDITIONS = ["full", "drop_dim1", "drop_dim2"]
SURFACE_FORMS = ["np", "relative_12", "relative_21"]


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
                    # N differs from the target on the restricting dimension only
                    n1, n2 = (other1, m2) if restricting == "dim1" else (m1, other2)
                    for uniqueness in ["unique", "duplicate"]:
                        offset = world_index % len(LABELS)
                        label_t, label_n, label_extra = (LABELS[(offset + i) % len(LABELS)] for i in range(3))
                        extra = (m1, m2) if uniqueness == "duplicate" else (other1, other2)
                        objects = [(label_t, m1, m2), (label_n, n1, n2), (label_extra, *extra)]
                        presentation = objects[world_index % 3 :] + objects[: world_index % 3]
                        scene = "\n".join(f"Object {label} is a {value1} {value2} {noun}."
                                          for label, value1, value2 in presentation)
                        for condition in DESCRIPTION_CONDITIONS:
                            keep1 = condition in {"full", "drop_dim2"}
                            keep2 = condition in {"full", "drop_dim1"}
                            satisfiers = [label for label, value1, value2 in objects
                                          if (not keep1 or value1 == m1) and (not keep2 or value2 == m2)]
                            dropped = {"full": None, "drop_dim1": "dim1", "drop_dim2": "dim2"}[condition]
                            for surface in SURFACE_FORMS:
                                phrase = describe(m1, m2, noun, surface, keep1, keep2)
                                for mapping_index in range(2):
                                    options = ([label_t, label_n] if mapping_index == 0
                                               else [label_n, label_t])
                                    option_text = "\n".join(f"{tag}) object {label}" for tag, label
                                                            in zip(["A", "B"], options))
                                    target_option = "A" if options[0] == label_t else "B"
                                    rows.append({
                                        "stimulus_version": config["stimulus_version"],
                                        "world_id": f"csr1_{world_index:03d}",
                                        "family": family, "noun": noun,
                                        "target_dim1": m1, "target_dim2": m2,
                                        "restricting_dimension": restricting,
                                        "uniqueness": uniqueness,
                                        "n_satisfiers_full": 2 if uniqueness == "duplicate" else 1,
                                        "description_condition": condition,
                                        "dropped_dimension": dropped,
                                        "dropped_modifier_is_restricting": (
                                            None if dropped is None else dropped == restricting),
                                        "n_satisfiers": len(satisfiers),
                                        "surface_form": surface, "mapping_index": mapping_index,
                                        "target_label": label_t, "distractor_label": label_n,
                                        "target_option": target_option,
                                        "distractor_option": "B" if target_option == "A" else "A",
                                        "description_phrase": phrase,
                                        "modifier_dim1": m1 if keep1 else None,
                                        "modifier_dim2": m2 if keep2 else None,
                                        "state_key": f"csr1_{world_index:03d}|{condition}|{surface}",
                                        "prompt_text": (
                                            "Scene: there are three objects on a table.\n"
                                            f"{scene}\n\n"
                                            f"Question: which of these objects do you mean?\n"
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
