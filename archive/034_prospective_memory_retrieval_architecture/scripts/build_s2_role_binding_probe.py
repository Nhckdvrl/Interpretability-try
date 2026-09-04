"""Build the cue-role binding probe: what decides which intention a cue is routed to?

Behavioral finding this experiment explains: under a shallow (orthographic) ongoing task both
families misroute a second-intention cue into the *first* intention's action, and the null
cue-token transplant says the fix is not a single transportable retrieval state.

The design separates two accounts of that misrouting with a three-level ongoing task, holding the
two future intentions and the critical sentence fixed:

  nonfocal      -- orthographic ongoing task (does the sentence start with 'The');
  focal_target  -- semantic ongoing task keyed to intention 1's category;
  focal_other   -- semantic ongoing task keyed to intention 2's category.

  semantic-depth account   : any semantic ongoing task restores correct routing, symmetrically.
  monitoring-piggyback acct: routing follows whichever category the ongoing task itself checks, so
                             focal_target helps intention-1 cues and focal_other helps intention-2
                             cues -- a crossover interaction, not a main effect of depth.

At the cue token the same three conditions are decoded for two targets:
  DETECT : cue word vs matched non-cue control word (coarse binding to either intention set);
  ROLE   : intention-1 cue vs intention-2 cue (fine binding to a specific intention).

Category pairs are role-counterbalanced: every category appears once as intention 1 and once as
intention 2, so ROLE cannot be read off lexically. Held-out folds drop whole category pairs.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_multi_intention_behavior import FILLERS, cyclic_maps

# (category, three cue members, three non-cue control words)
CATEGORIES = [
    ("profession", ["doctor", "nurse", "pilot"], ["basket", "ribbon", "plaque"]),
    ("musical instrument", ["violin", "cello", "flute"], ["blanket", "satchel", "pebble"]),
    ("fruit", ["orange", "apple", "pear"], ["lantern", "bundle", "carton"]),
    ("vehicle", ["train", "bicycle", "truck"], ["cabinet", "tarp", "sack"]),
    ("bird", ["sparrow", "eagle", "robin"], ["notebook", "ribbon", "pebble"]),
    ("hand tool", ["hammer", "wrench", "saw"], ["curtain", "plaque", "carton"]),
    ("color word", ["purple", "yellow", "green"], ["bucket", "satchel", "bundle"]),
    ("emotion word", ["joy", "anger", "fear"], ["shelf", "tarp", "basket"]),
    ("sport", ["tennis", "hockey", "rugby"], ["pillow", "sack", "ribbon"]),
    ("city name", ["London", "Tokyo", "Cairo"], ["mirror", "plaque", "bundle"]),
    ("piece of clothing", ["jacket", "shirt", "scarf"], ["vase", "carton", "pebble"]),
    ("beverage", ["coffee", "tea", "juice"], ["folder", "tarp", "basket"]),
    ("animal", ["rabbit", "horse", "dolphin"], ["ticket", "satchel", "plaque"]),
    ("furniture item", ["table", "sofa", "chair"], ["wallet", "bundle", "sack"]),
    ("weather word", ["thunder", "rain", "snow"], ["parcel", "ribbon", "carton"]),
    ("body part", ["elbow", "ankle", "wrist"], ["marble", "pebble", "tarp"]),
    ("vegetable", ["carrot", "potato", "onion"], ["beacon", "basket", "satchel"]),
    ("metal", ["copper", "silver", "iron"], ["poster", "bundle", "ribbon"]),
    ("tree", ["maple", "birch", "willow"], ["ledger", "sack", "plaque"]),
    ("kitchen utensil", ["spoon", "ladle", "whisk"], ["banner", "carton", "pebble"]),
    ("insect", ["beetle", "moth", "wasp"], ["cushion", "tarp", "basket"]),
    ("building", ["castle", "cottage", "tower"], ["stamp", "satchel", "bundle"]),
    ("flower", ["tulip", "daisy", "orchid"], ["ladder", "ribbon", "sack"]),
    ("boat type", ["canoe", "ferry", "yacht"], ["candle", "plaque", "carton"]),
    ("gemstone", ["ruby", "pearl", "amber"], ["carpet", "hanger", "satchel"]),
    ("dance style", ["tango", "waltz", "ballet"], ["basin", "basket", "tarp"]),
    ("month name", ["April", "August", "October"], ["hanger", "bundle", "plaque"]),
    ("language name", ["Dutch", "Swedish", "Arabic"], ["stool", "sack", "ribbon"]),
    ("spice", ["pepper", "cinnamon", "ginger"], ["bottle", "carton", "satchel"]),
    ("office supply", ["stapler", "binder", "clipboard"], ["mattress", "pebble", "basket"]),
    ("planet", ["Venus", "Saturn", "Neptune"], ["helmet", "tarp", "bundle"]),
    ("music genre", ["jazz", "reggae", "opera"], ["kayak", "plaque", "sack"]),
]

# Each pair supplies two role-counterbalanced items, so every cue word is seen in both roles.
PAIRS = [(index, index + 1) for index in range(0, len(CATEGORIES), 2)]

FILLER_BLOCK = "\n".join(f"Earlier sentence {i + 1}: {text}" for i, text in enumerate(FILLERS))


def example_text(members: list[str], excluded: str) -> str:
    kept = [value for value in members if value != excluded]
    if len(kept) != 2:
        raise ValueError(f"Expected two remaining examples after excluding {excluded}: {members}")
    return f"{kept[0]} or {kept[1]}"


ONGOING_CONDITIONS = ["nonfocal", "focal_target", "focal_other"]


def ongoing_rule_for(condition: str, target_category: str, target_examples: str,
                     other_category: str, other_examples: str) -> str:
    if condition == "focal_target":
        return f"answer YES if the sentence names a {target_category} (for example, {target_examples}); otherwise answer NO"
    if condition == "focal_other":
        return f"answer YES if the sentence names a {other_category} (for example, {other_examples}); otherwise answer NO"
    return "answer YES if the sentence begins with the word 'The'; otherwise answer NO"


def ongoing_answer_for(condition: str, cue_type: str) -> str:
    if condition == "nonfocal":
        return "YES"
    if condition == "focal_target":
        return "YES" if cue_type == "target" else "NO"
    return "YES" if cue_type == "other" else "NO"


def prompt_for(target_category: str, target_examples: str, other_category: str, other_examples: str,
               focality: str, critical: str, mapping_text: str) -> str:
    ongoing_rule = ongoing_rule_for(focality, target_category, target_examples,
                                    other_category, other_examples)
    return (
        "You are processing a stream of sentences while holding two future intentions.\n"
        f"Future intention 1: if a later sentence names a {target_category} "
        f"(for example, {target_examples}), interrupt the ongoing task and perform TARGET_ACTION.\n"
        f"Future intention 2: if a later sentence names a {other_category} "
        f"(for example, {other_examples}), interrupt and perform OTHER_ACTION.\n"
        f"Ongoing task: {ongoing_rule}.\n"
        "Cue expectancy: A future-intention cue is likely to appear in this block.\n"
        f"{FILLER_BLOCK}\nCurrent sentence: {critical}\n"
        f"Response mapping: {mapping_text}.\n"
        "Apply the future intentions first; if neither triggers, do the ongoing task. "
        "Reply with exactly A, B, C, or D."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    mappings = [cyclic_maps()[index] for index in config["mapping_indices"]]
    rows = []
    for pair_index, (first, second) in enumerate(PAIRS):
        for order, (target_index, other_index) in enumerate([(first, second), (second, first)]):
            target_category, target_members, target_controls = CATEGORIES[target_index]
            other_category, other_members, _ = CATEGORIES[other_index]
            item_id = f"pm_role_{pair_index:02d}{'ab'[order]}"
            critical_words = (
                [("target", word) for word in target_members]
                + [("other", word) for word in other_members]
                + [("none", word) for word in target_controls]
            )
            for cue_type, critical_word in critical_words:
                target_cue = critical_word if cue_type == "target" else target_members[0]
                other_cue = critical_word if cue_type == "other" else other_members[0]
                target_examples = example_text(target_members, target_cue)
                other_examples = example_text(other_members, other_cue)
                critical = f"The {critical_word} remained beside a window."
                for focality in ONGOING_CONDITIONS:
                    ongoing_answer = ongoing_answer_for(focality, cue_type)
                    correct_semantic = {"target": "TARGET_ACTION", "other": "OTHER_ACTION",
                                        "none": ongoing_answer}[cue_type]
                    for map_index, mapping in zip(config["mapping_indices"], mappings):
                        inverse = {label: semantic for semantic, label in mapping.items()}
                        mapping_text = "; ".join(f"{label}={inverse[label]}" for label in ["A", "B", "C", "D"])
                        rows.append({
                            "stimulus_version": config["stimulus_version"],
                            "pair_index": pair_index, "role_order": order, "semantic_id": item_id,
                            "target_category": target_category, "other_category": other_category,
                            "cue_type": cue_type, "critical_word": critical_word,
                            "focality": focality, "mapping_index": map_index,
                            "semantic_to_label": mapping,
                            "correct_semantic": correct_semantic, "correct_label": mapping[correct_semantic],
                            "critical_sentence": critical,
                            "state_key": f"{item_id}|{cue_type}|{critical_word}|{focality}",
                            "prompt_text": prompt_for(target_category, target_examples, other_category,
                                                 other_examples, focality, critical, mapping_text),
                        })
    words = {row["critical_word"] for row in rows}
    filler_words = {word.strip(".").lower() for text in FILLERS for word in text.split()}
    overlap = {word for word in words if word.lower() in filler_words}
    if overlap:
        raise ValueError(f"Critical words collide with filler content: {sorted(overlap)}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(rows),
                      "items": len(PAIRS) * 2, "pairs": len(PAIRS),
                      "state_rows": len({row["state_key"] for row in rows})}))


if __name__ == "__main__":
    main()
