"""Push a capable model's *use* of the role down while its representation stays, within one model.

Parameter count is the wrong axis for this question. Sub-billion models are not what this work is
read against — interpretability results are read at 7B-27B — and a cross-scale "behaviour absent,
representation present" claim rests on thresholded accuracy, which is the artifact Schaeffer et al.
(NeurIPS 2023) identify behind apparent emergence. So the dissociation is looked for inside single
capable models and driven by task load instead. Restriction keeps its
definition — a modifier restricts iff dropping it admits more live candidates — and exactly one
modifier restricts in every world, so the readout and its gold never change. Only the amount of set
intersection changes, along two axes measured separately:

    modifier load    2, 3 or 4 adjectives in the description, live set fixed at 4
    candidate load   4, 7, 10 or 13 objects in the live set, description fixed at 4 adjectives

Dimensions are ternary rather than binary for a structural reason: any object differing from the
target on exactly one described slot becomes a satisfier when that slot is dropped, which would make
a second modifier restrict. Binary dimensions leave only 2^n - n - 1 usable fillers (just one at
n = 2), too few to build the larger sets; ternary leaves 3^n - 2n - 1.
"""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path

DIMENSIONS = [
    ("size", ("large", "medium", "small")),
    ("colour", ("red", "blue", "green")),
    ("texture", ("rough", "smooth", "ridged")),
    ("pattern", ("striped", "plain", "dotted")),
]
NOUNS = ["circle", "block", "tile", "panel", "disc", "plate", "ring", "bar"]
LABELS = ["P", "Q", "R", "S", "T", "V", "W", "Z", "F", "G", "H", "J", "K", "L"]
# the two load axes are measured separately rather than crossed, because the number of usable
# fillers depends on how many modifiers there are
AXES = ([("modifier_load", n, 4) for n in (2, 3, 4)]
        + [("candidate_load", 4, k) for k in (7, 10, 13)])


def describe(values: list[str], noun: str, dropped: int | None) -> str:
    kept = [value for index, value in enumerate(values) if index != dropped]
    return f"the {' '.join(kept + [noun])}" if kept else f"the {noun}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    rows = []
    world_index = 0
    for noun in NOUNS:
        for axis, n_modifiers, n_candidates in AXES:
            dims = DIMENSIONS[:n_modifiers]
            for restricting_slot in range(n_modifiers):
                for target_shift in range(2):
                    target = [values[(target_shift + i) % 3] for i, (_, values) in enumerate(dims)]
                    distractor = list(target)
                    distractor[restricting_slot] = next(
                        v for v in dims[restricting_slot][1] if v != target[restricting_slot])
                    # every other object must differ from the target on at least two described slots,
                    # otherwise dropping its single differing slot would make it a satisfier too
                    fillers = [list(combo) for combo in product(*[values for _, values in dims])
                               if sum(a != b for a, b in zip(combo, target)) >= 2]
                    fillers = [f for f in fillers if f != distractor]
                    needed = n_candidates - 2
                    if len(fillers) < needed:
                        continue
                    stride = max(1, len(fillers) // needed)
                    chosen = fillers[::stride][:needed]
                    objects = [("target", target), ("distractor", distractor)]
                    objects += [(f"filler{i}", values) for i, values in enumerate(chosen)]
                    offset = world_index % len(LABELS)
                    named = [(LABELS[(offset + i) % len(LABELS)], role, values)
                             for i, (role, values) in enumerate(objects)]
                    presentation = named[world_index % len(named):] + named[: world_index % len(named)]
                    scene = "\n".join(f"Object {label} is a {' '.join(values)} {noun}."
                                      for label, _, values in presentation)
                    target_label = next(l for l, r, _ in named if r == "target")
                    distractor_label = next(l for l, r, _ in named if r == "distractor")
                    for dropped in [None] + list(range(n_modifiers)):
                        text = describe(target, noun, dropped)
                        satisfiers = [
                            label for label, _, values in named
                            if all(values[i] == target[i]
                                   for i in range(n_modifiers) if i != dropped)]
                        for mapping_index in range(2):
                            options = ([target_label, distractor_label] if mapping_index == 0
                                       else [distractor_label, target_label])
                            option_text = "\n".join(f"{tag}) object {label}"
                                                    for tag, label in zip(["A", "B"], options))
                            gold_option = "A" if options[0] == target_label else "B"
                            rows.append({
                                "stimulus_version": config["stimulus_version"],
                                "world_id": f"csr8_{world_index:04d}",
                                "load_axis": axis, "noun": noun,
                                "n_modifiers": n_modifiers, "n_candidates": n_candidates,
                                "restricting_slot": restricting_slot, "dropped_slot": dropped,
                                "dropped_is_restricting": (None if dropped is None
                                                           else dropped == restricting_slot),
                                "description_condition": ("full" if dropped is None
                                                          else f"drop_{dropped}"),
                                "n_satisfiers": len(satisfiers),
                                "mapping_index": mapping_index,
                                "target_label": target_label, "distractor_label": distractor_label,
                                "gold_option": gold_option,
                                "other_option": "B" if gold_option == "A" else "A",
                                "description_phrase": text,
                                "modifier_words": list(target),
                                "restricting_word": target[restricting_slot],
                                "dropped_word": None if dropped is None else target[dropped],
                                "state_key": f"csr8_{world_index:04d}|{dropped}",
                                "prompt_text": (
                                    f"Scene: there are {n_candidates} objects on a table.\n"
                                    f"{scene}\n\n"
                                    "Question: which of these objects do you mean?\n"
                                    f"Reply: I mean {text}.\n\n"
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
