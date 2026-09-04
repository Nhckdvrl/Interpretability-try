"""Build B1: referential relevance x explanatory relevance, crossed on the same content.

Frozen under tag B1_PREANALYSIS_FREEZE. Nothing below may change after any panel model has been run
on B0 or B1.

Inheritance. The twelve adjective-event pairings come from the critical materials of
Davies & Richardson (2021), J. Pragmatics 178:258-269 (AAM, White Rose eprints 172760): the `+sem`
verb of each quartet is the event the adjective bears on (`fed` / `hungry`, `spat out` / `mouldy`),
the `-sem` verb is the event it does not (`tickled`, `chewed`). Their referential factor is a
licensing manipulation (a contrast set is present or not) and is replaced here by a denotational one
whose gold is computed from the described properties, as in 041 S0.

B1 does not assume a uniquely correct alternative cause in the E- condition. It measures the model's
support for the same P-based explanation across the human-validated E+/E- property-event contrast,
so the only causal gold it relies on is the one Davies & Richardson already normed on 31 readers.

World schema. Four entities, each described on two dimensions:

    A = P+ Q+   target
    B = P- Q+
    C = P+ Q-
    D = P+ Q-

    live {A,B,C}: drop P -> {A,B}   ambiguous  => P restricts
                  drop Q -> {A,C}   ambiguous  => Q restricts
    live {A,C,D}: drop P -> {A}     unique     => P does NOT restrict
                  drop Q -> {A,C,D} ambiguous  => Q restricts

`Q` therefore restricts in both R conditions, so the R manipulation is not a `P wins vs Q wins`
swap, and no competition between the two modifiers is built into the stimuli. World text is
identical across R conditions; only the clause naming the live entities differs. The E manipulation
changes only the matrix verb phrase.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SEED = 20260904

# item, noun, plural, explanation_noun, setting, P+, P-, (Q+, Q-),
# (vp_p, wrap_p, ref_question_p, exp_question_p), (vp_z, wrap_z, ref_question_z, exp_question_z)
ITEMS = [
    ("table", "table", "tables", "table", "the meeting room", "heavy", "light", ("brown", "white"),
     ("Mark helped Tom move", "to the middle of the room.", "Which table did Mark help Tom move?",
      "Why did Mark help Tom move that table?"),
     ("Mark helped Tom sit at", "at the end of the meeting.", "Which table did Mark help Tom sit at?",
      "Why did Mark help Tom sit at that table?")),

    ("mirror", "mirror", "mirrors", "mirror", "the hallway", "broken", "intact", ("gold", "silver"),
     ("Ella stepped over", "on her way out.", "Which mirror did Ella step over?",
      "Why did Ella step over that mirror?"),
     ("Ella looked at", "on her way out.", "Which mirror did Ella look at?",
      "Why did Ella look at that mirror?")),

    ("bird", "bird", "birds", "bird", "the garden", "noisy", "quiet", ("brown", "grey"),
     ("Sarah listened to", "all afternoon.", "Which bird did Sarah listen to?",
      "Why did Sarah listen to that bird?"),
     ("Sarah painted", "all afternoon.", "Which bird did Sarah paint?",
      "Why did Sarah paint that bird?")),

    ("rabbit", "rabbit", "rabbits", "rabbit", "the kitchen", "hungry", "well-fed", ("brown", "white"),
     ("Bob fed", "when he got home.", "Which rabbit did Bob feed?",
      "Why did Bob feed that rabbit?"),
     ("Bob tickled", "when he got home.", "Which rabbit did Bob tickle?",
      "Why did Bob tickle that rabbit?")),

    ("chandelier", "chandelier", "chandeliers", "chandelier", "the shop", "large", "small",
     ("brass", "crystal"),
     ("Nina helped them lift", "onto the counter.", "Which chandelier did Nina help them lift?",
      "Why did Nina help them lift that chandelier?"),
     ("Nina helped them choose", "for the dining room.", "Which chandelier did Nina help them choose?",
      "Why did Nina help them choose that chandelier?")),

    ("apple", "apple", "apples", "apple", "the bowl", "mouldy", "fresh", ("red", "green"),
     ("Gregg spat out", "straight away.", "Which apple did Gregg spit out?",
      "Why did Gregg spit out that apple?"),
     ("Gregg chewed", "straight away.", "Which apple did Gregg chew?",
      "Why did Gregg chew that apple?")),

    ("scarf", "scarf", "scarves", "scarf", "the chair", "warm", "thin", ("red", "blue"),
     ("Josie put on", "before leaving the house.", "Which scarf did Josie put on?",
      "Why did Josie put on that scarf?"),
     ("Josie moved", "before leaving the house.", "Which scarf did Josie move?",
      "Why did Josie move that scarf?")),

    ("food", "bowl of food", "bowls of food", "food", "the kitchen floor", "tasty", "bland",
     ("tinned", "homemade"),
     ("The cat ate", "before having a nap.", "Which bowl of food did the cat eat?",
      "Why did the cat eat that bowl of food?"),
     ("The cat smelled", "before having a nap.", "Which bowl of food did the cat smell?",
      "Why did the cat smell that bowl of food?")),

    ("bag", "bag", "bags", "bag", "the shop floor", "pretty", "plain", ("leather", "canvas"),
     ("Florence bought", "and left the store.", "Which bag did Florence buy?",
      "Why did Florence buy that bag?"),
     ("Florence moved", "and left the store.", "Which bag did Florence move?",
      "Why did Florence move that bag?")),

    ("spider", "spider", "spiders", "spider", "the desk", "scary", "harmless", ("black", "brown"),
     ("Penny screamed at", "for a long time.", "Which spider did Penny scream at?",
      "Why did Penny scream at that spider?"),
     ("Penny stroked", "for a long time.", "Which spider did Penny stroke?",
      "Why did Penny stroke that spider?")),

    ("trampoline", "trampoline", "trampolines", "trampoline", "the garden", "bouncy", "flat",
     ("round", "square"),
     ("The dog jumped on", "before his walk.", "Which trampoline did the dog jump on?",
      "Why did the dog jump on that trampoline?"),
     ("The dog looked at", "before his walk.", "Which trampoline did the dog look at?",
      "Why did the dog look at that trampoline?")),

    ("painting", "painting", "paintings", "painting", "the studio", "weighty", "lightweight",
     ("framed", "unframed"),
     ("Susanne dropped", "in the living room.", "Which painting did Susanne drop?",
      "Why did Susanne drop that painting?"),
     ("Susanne displayed", "in the living room.", "Which painting did Susanne display?",
      "Why did Susanne display that painting?")),
]

DESCRIPTION_CONDITIONS = ["full", "drop_p", "drop_q", "bare"]
SURFACE_FORMS = ["np", "relative_pq", "relative_qp"]
LIVE_CUES = [
    "The choice was between {listing}.",
    "Only {listing} were under consideration.",
]
OPTION_LETTERS = ["A", "B", "C"]


def describe(noun: str, p_value: str, q_value: str, surface: str, keep_p: bool, keep_q: bool) -> str:
    kept = [v for v, keep in ((p_value, keep_p), (q_value, keep_q)) if keep]
    if not kept:
        return f"the {noun}"
    if surface == "np":
        return f"the {' '.join(kept)} {noun}"
    ordered = kept if surface == "relative_pq" else list(reversed(kept))
    if len(ordered) == 1:
        return f"the {noun} that is {ordered[0]}"
    return f"the {noun} that is {ordered[0]} and {ordered[1]}"


def listing(names: list[str]) -> str:
    return f"{', '.join(names[:-1])} and {names[-1]}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    reference_rows, explanation_rows = [], []
    world_index = 0

    for item in ITEMS:
        (item_id, noun, plural, explanation_noun, setting, p_pos, p_neg, q_values,
         event_p, event_z) = item
        q_pos, q_neg = q_values
        continuations = {
            "p": f"Because the {explanation_noun} was {p_pos}.",
            "p_contrast": f"Because the {explanation_noun} was {p_neg}.",
        }

        for target_index in range(4):
            props = [(p_pos, q_pos), (p_neg, q_pos), (p_pos, q_neg), (p_pos, q_neg)]
            order = [(target_index + k) % 4 for k in range(4)]
            slot_of_number = {number: slot for slot, number in enumerate(order)}
            number_of_slot = {slot: number for number, slot in slot_of_number.items()}
            names = [f"{noun.split()[0].capitalize()} {n + 1}" for n in range(4)]
            entity_lines = []
            for number in range(4):
                p_val, q_val = props[slot_of_number[number]]
                entity_lines.append(f"{names[number]} is {p_val} and {q_val}.")
            target_name = names[number_of_slot[0]]

            for r_condition, live_slots in (("R_plus", (0, 1, 2)), ("R_minus", (0, 2, 3))):
                live_numbers = sorted(number_of_slot[s] for s in live_slots)
                live_names = [names[n] for n in live_numbers]
                for e_condition, event in (("E_plus", event_p), ("E_minus", event_z)):
                    vp, wrapup, ref_question, exp_question = event
                    for cue_index, cue in enumerate(LIVE_CUES):
                        cue_text = cue.format(listing=listing(live_names))
                        scene = (f"Scene: there are four {plural} in {setting}.\n"
                                 + "\n".join(entity_lines))
                        for condition in DESCRIPTION_CONDITIONS:
                            keep_p = condition in {"full", "drop_q"}
                            keep_q = condition in {"full", "drop_p"}
                            satisfying = [
                                names[n] for n in live_numbers
                                if (not keep_p or props[slot_of_number[n]][0] == p_pos)
                                and (not keep_q or props[slot_of_number[n]][1] == q_pos)
                            ]
                            for surface in SURFACE_FORMS:
                                phrase = describe(noun, p_pos, q_pos, surface, keep_p, keep_q)
                                critical = f"{vp} {phrase} {wrapup}"
                                stem = f"{scene}\n\n{cue_text}\n{critical}"
                                for mapping_index in range(3):
                                    ordered = (live_names[mapping_index:]
                                               + live_names[:mapping_index])
                                    options = "\n".join(
                                        f"{OPTION_LETTERS[i]}) {name}"
                                        for i, name in enumerate(ordered))
                                    reference_rows.append({
                                        "stimulus_version": "b1_function_cross",
                                        "readout": "reference",
                                        "world_id": f"b1_{world_index:04d}",
                                        "item_id": item_id,
                                        "r_condition": r_condition,
                                        "e_condition": e_condition,
                                        "description_condition": condition,
                                        "p_restricts": r_condition == "R_plus",
                                        "q_restricts": True,
                                        "p_relevant_to_event": e_condition == "E_plus",
                                        "n_live_satisfying": len(satisfying),
                                        "surface_form": surface,
                                        "cue_index": cue_index,
                                        "mapping_index": mapping_index,
                                        "target_name": target_name,
                                        "gold_option": OPTION_LETTERS[ordered.index(target_name)],
                                        "live_names": live_names,
                                        "prompt_text": (f"{stem}\n\n{ref_question}\n{options}\n"
                                                        "Answer with exactly A, B or C."),
                                        "critical_sentence": critical,
                                        "modifier_span": p_pos,
                                        "np_span": phrase,
                                    })
                                # explanation readout: scored continuation, no forced choice.
                                if condition in {"full", "drop_p"} and surface == "np":
                                    for continuation_label, continuation in continuations.items():
                                        explanation_rows.append({
                                            "stimulus_version": "b1_function_cross",
                                            "readout": "explanation",
                                            "world_id": f"b1_{world_index:04d}",
                                            "item_id": item_id,
                                            "r_condition": r_condition,
                                            "e_condition": e_condition,
                                            "description_condition": condition,
                                            "p_restricts": r_condition == "R_plus",
                                            "p_relevant_to_event": e_condition == "E_plus",
                                            "cue_index": cue_index,
                                            "continuation_label": continuation_label,
                                            "prefix": f"{stem}\n\n{exp_question}\n",
                                            "continuation": continuation,
                                            "critical_sentence": critical,
                                            "verb_phrase": vp,
                                            "explanation_question": exp_question,
                                            "q_values": [q_pos, q_neg],
                                            "entity_names": names,
                                        })
            world_index += 1

    certify_reference(reference_rows)
    certify_explanation(explanation_rows)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        for row in reference_rows + explanation_rows:
            handle.write(json.dumps(row) + "\n")
    print(f"wrote {len(reference_rows)} reference and {len(explanation_rows)} explanation rows "
          f"to {args.output}")


def certify_reference(rows: list[dict]) -> None:
    """Deterministic structural validity. No model is consulted, at build time or ever."""
    for row in rows:
        cond, r = row["description_condition"], row["r_condition"]
        n = row["n_live_satisfying"]
        if cond == "full":
            assert n == 1, row
        elif cond == "drop_p":
            assert n == (2 if r == "R_plus" else 1), row
        elif cond == "drop_q":
            assert n == (2 if r == "R_plus" else 3), row
        else:
            assert n == 3, row
        assert len(row["live_names"]) == 3, row
        assert row["target_name"] in row["live_names"], row
        assert row["modifier_span"] in row["critical_sentence"] or cond in {"drop_p", "bare"}, row
    print(f"structural certification passed on {len(rows)} reference rows")


def certify_explanation(rows: list[dict]) -> None:
    """The scored continuation must be identical across the E manipulation, the question must belong
    to the event actually described, and the continuation must not leak the referent's identity."""
    expected = {}
    continuations = {}
    for item in ITEMS:
        item_id, explanation_noun, p_pos, p_neg = item[0], item[3], item[5], item[6]
        expected[(item_id, "E_plus")] = (item[8][0], item[8][3])
        expected[(item_id, "E_minus")] = (item[9][0], item[9][3])
        continuations[(item_id, "p")] = f"Because the {explanation_noun} was {p_pos}."
        continuations[(item_id, "p_contrast")] = f"Because the {explanation_noun} was {p_neg}."

    for row in rows:
        key = (row["item_id"], row["e_condition"])
        want_vp, want_question = expected[key]
        # exact verb synchronisation, checked against the source table rather than by stemming,
        # since irregular forms (fed / feed) defeat a lexical heuristic
        assert row["verb_phrase"] == want_vp, (key, row["verb_phrase"])
        assert row["explanation_question"] == want_question, (key, row["explanation_question"])
        other = "E_minus" if row["e_condition"] == "E_plus" else "E_plus"
        assert row["explanation_question"] != expected[(row["item_id"], other)][1], key
        assert row["verb_phrase"] in row["critical_sentence"], key
        # the scored span is identical across E+ and E-, so the contrast is a pure context swap
        assert row["continuation"] == continuations[(row["item_id"], row["continuation_label"])], key
        # no identity leakage in the scored span
        lowered = row["continuation"].lower()
        for q_value in row["q_values"]:
            assert q_value.lower() not in lowered, (key, row["continuation"], q_value)
        assert not re.search(r"\d", row["continuation"]), (key, row["continuation"])
        for name in row["entity_names"]:
            assert name.lower() not in lowered, (key, row["continuation"], name)
    print(f"explanation certification passed on {len(rows)} rows")


if __name__ == "__main__":
    main()
