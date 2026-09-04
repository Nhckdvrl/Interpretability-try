"""Deconfound the intention-priority asymmetry: listing position vs action-name salience.

s2 established, in both families, that the intention-role binding is decoded essentially
perfectly at the cue token (mass-mean, pair-held-out, chance at layer 0 by counterbalanced
construction) -- including on the very trials whose action is misrouted -- while the action
executed is the *first* intention's roughly 20-73% of the time and the reverse error is
0.0-0.5%. s1 already showed the cue-token state carries no transportable fix.

s2 cannot say what defines "first", because intention 1 was always listed first *and* always
named TARGET_ACTION. This experiment crosses the two:

  listing order   -- which category is presented as Future intention 1;
  naming scheme   -- neutral (ALPHA/BETA carry no priority), semantic_forward (first-listed is
                     TARGET_ACTION, as in s2), semantic_reversed (first-listed is OTHER_ACTION).

  position account : the misroute goes to the first-listed intention under every naming scheme;
  name account     : the misroute follows the TARGET_ACTION label and flips under reversal.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_multi_intention_behavior import FILLERS, cyclic_maps
from build_s2_role_binding_probe import CATEGORIES, PAIRS, example_text

FILLER_BLOCK = "\n".join(f"Earlier sentence {i + 1}: {text}" for i, text in enumerate(FILLERS))
SCHEMES = {
    "neutral": ("ALPHA_ACTION", "BETA_ACTION"),
    "semantic_forward": ("TARGET_ACTION", "OTHER_ACTION"),
    "semantic_reversed": ("OTHER_ACTION", "TARGET_ACTION"),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    rows = []
    for pair_index, (left, right) in enumerate(PAIRS):
        for order, (first_index, second_index) in enumerate([(left, right), (right, left)]):
            first_category, first_members, first_controls = CATEGORIES[first_index]
            second_category, second_members, _ = CATEGORIES[second_index]
            item_id = f"pm_prio_{pair_index:02d}{'ab'[order]}"
            critical_words = ([("first", word) for word in first_members]
                              + [("second", word) for word in second_members]
                              + [("none", word) for word in first_controls])
            for cue_type, critical_word in critical_words:
                first_cue = critical_word if cue_type == "first" else first_members[0]
                second_cue = critical_word if cue_type == "second" else second_members[0]
                first_examples = example_text(first_members, first_cue)
                second_examples = example_text(second_members, second_cue)
                critical = f"The {critical_word} remained beside a window."
                for scheme, (first_action, second_action) in SCHEMES.items():
                    executed = {"first": first_action, "second": second_action, "none": "YES"}[cue_type]
                    misroute = {"first": second_action, "second": first_action, "none": None}[cue_type]
                    semantics = [first_action, second_action, "YES", "NO"]
                    for map_index, mapping in enumerate(cyclic_maps()):
                        if map_index not in config["mapping_indices"]:
                            continue
                        assignment = dict(zip(semantics, [mapping[key] for key in
                                                          ["TARGET_ACTION", "OTHER_ACTION", "YES", "NO"]]))
                        inverse = {label: semantic for semantic, label in assignment.items()}
                        mapping_text = "; ".join(f"{label}={inverse[label]}" for label in ["A", "B", "C", "D"])
                        rows.append({
                            "stimulus_version": config["stimulus_version"],
                            "pair_index": pair_index, "listing_order": order, "semantic_id": item_id,
                            "first_category": first_category, "second_category": second_category,
                            "naming_scheme": scheme, "first_action": first_action,
                            "second_action": second_action,
                            "cue_type": cue_type, "critical_word": critical_word,
                            "mapping_index": map_index, "semantic_to_label": assignment,
                            "correct_semantic": executed, "correct_label": assignment[executed],
                            "misroute_semantic": misroute,
                            "critical_sentence": critical,
                            "state_key": f"{item_id}|{cue_type}|{critical_word}|{scheme}",
                            "prompt_text": (
                                "You are processing a stream of sentences while holding two future intentions.\n"
                                f"Future intention 1: if a later sentence names a {first_category} "
                                f"(for example, {first_examples}), interrupt the ongoing task and perform "
                                f"{first_action}.\n"
                                f"Future intention 2: if a later sentence names a {second_category} "
                                f"(for example, {second_examples}), interrupt and perform {second_action}.\n"
                                "Ongoing task: answer YES if the sentence begins with the word 'The'; "
                                "otherwise answer NO.\n"
                                "Cue expectancy: A future-intention cue is likely to appear in this block.\n"
                                f"{FILLER_BLOCK}\nCurrent sentence: {critical}\n"
                                f"Response mapping: {mapping_text}.\n"
                                "Apply the future intentions first; if neither triggers, do the ongoing task. "
                                "Reply with exactly A, B, C, or D."
                            ),
                        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(rows),
                      "items": len(PAIRS) * 2, "schemes": list(SCHEMES)}))


if __name__ == "__main__":
    main()
