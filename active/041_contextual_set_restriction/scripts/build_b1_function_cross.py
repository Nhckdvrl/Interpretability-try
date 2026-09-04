"""Build B1: referential relevance x explanatory relevance, crossed on the same content.

Frozen under tag B1_PREANALYSIS_FREEZE. Nothing below may change after any panel model has been
run on B1 or B0.

Inheritance. The twelve adjective-event pairings come from the critical materials of
Davies & Richardson (2021), J. Pragmatics 178:258-269 (AAM, White Rose eprints 172760): the
`+sem` verb of each quartet is the event the adjective bears on (`fed` / `hungry`,
`spat out` / `mouldy`), the `-sem` verb is the event it does not (`tickled`, `chewed`). Their
referential factor is a licensing manipulation (a contrast set is present or not) and is replaced
here by a denotational one whose gold is computed from the described properties, as in 041 S0.
The background fact `Z` and the four-entity worlds are ours; D&R needed no alternative cause because
their measure was reading time, whereas a forced-choice readout needs a defined competitor in both
cells.

World schema. Four entities, each described on two dimensions and carrying one background fact:

    A = P+ Q+   target, background fact Z
    B = P- Q+
    C = P+ Q-
    D = P+ Q-

    live {A,B,C}: drop P -> {A,B}   ambiguous  => P restricts
                  drop Q -> {A,C}   ambiguous  => Q restricts
    live {A,C,D}: drop P -> {A}     unique     => P does NOT restrict
                  drop Q -> {A,C,D} ambiguous  => Q restricts

`Q` therefore restricts in both R conditions, so the R manipulation is not a `P wins vs Q wins`
swap, and no competition between the two modifiers is built into the stimuli. World text is
identical across R conditions; only the clause naming the live entities differs.

`Z` is true of the target, stated in every cell, never part of the referring description, and never
an option in the referential readout. Matched background facts are stated for the non-targets so `Z`
creates no salience asymmetry. The E manipulation changes only the matrix verb phrase.
"""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path

SEED = 20260904

# item, noun, plural, setting, P+, P-, (Q+, Q-),
# (vp_p, wrap_p, ref_q_p, exp_q_p), (vp_z, wrap_z, ref_q_z, exp_q_z),
# z_fact, cause_p, cause_z, (bg_b, bg_c, bg_d)
ITEMS = [
    ("table", "table", "tables", "the meeting room", "heavy", "light", ("brown", "white"),
     ("Mark helped Tom move", "to the middle of the room.", "Which table did Mark help Tom move?",
      "Why did Mark help Tom move that table?"),
     ("Mark helped Tom sit at", "at the end of the meeting.", "Which table did Mark help Tom sit at?",
      "Why did Mark help Tom sit at that table?"),
     "was already laid out for the meeting",
     "Because the table was heavy.", "Because the table was already laid out for the meeting.",
     ("had a wobbly leg", "was covered in papers", "had just been polished")),

    ("mirror", "mirror", "mirrors", "the hallway", "broken", "intact", ("gold", "silver"),
     ("Ella stepped over", "on her way out.", "Which mirror did Ella step over?",
      "Why did Ella step over that mirror?"),
     ("Ella looked at", "on her way out.", "Which mirror did Ella look at?",
      "Why did Ella look at that mirror?"),
     "was hanging at eye level",
     "Because the mirror was broken.", "Because the mirror was hanging at eye level.",
     ("had just been delivered", "was wrapped in paper", "belonged to her aunt")),

    ("bird", "bird", "birds", "the garden", "noisy", "quiet", ("brown", "grey"),
     ("Sarah listened to", "all afternoon.", "Which bird did Sarah listen to?",
      "Why did Sarah listen to that bird?"),
     ("Sarah painted", "all afternoon.", "Which bird did Sarah paint?",
      "Why did Sarah paint that bird?"),
     "was perched in bright sunlight",
     "Because the bird was noisy.", "Because the bird was perched in bright sunlight.",
     ("had a broken wing", "had just landed", "was sitting near the fence")),

    ("rabbit", "rabbit", "rabbits", "the kitchen", "hungry", "well-fed", ("brown", "white"),
     ("Bob fed", "when he got home.", "Which rabbit did Bob feed?",
      "Why did Bob feed that rabbit?"),
     ("Bob tickled", "when he got home.", "Which rabbit did Bob tickle?",
      "Why did Bob tickle that rabbit?"),
     "had been very playful that evening",
     "Because the rabbit was hungry.", "Because the rabbit had been very playful that evening.",
     ("had just arrived", "was due at the vet", "had chewed through its hutch")),

    ("chandelier", "chandelier", "chandeliers", "the shop", "large", "small", ("brass", "crystal"),
     ("Nina helped them lift", "onto the counter.", "Which chandelier did Nina help them lift?",
      "Why did Nina help them lift that chandelier?"),
     ("Nina helped them choose", "for the dining room.", "Which chandelier did Nina help them choose?",
      "Why did Nina help them choose that chandelier?"),
     "matched the dining room",
     "Because the chandelier was large.", "Because the chandelier matched the dining room.",
     ("was on sale", "came with a warranty", "had been recommended online")),

    ("apple", "apple", "apples", "the bowl", "mouldy", "fresh", ("red", "green"),
     ("Gregg spat out", "straight away.", "Which apple did Gregg spit out?",
      "Why did Gregg spit out that apple?"),
     ("Gregg chewed", "straight away.", "Which apple did Gregg chew?",
      "Why did Gregg chew that apple?"),
     "was part of a tasting test",
     "Because the apple was mouldy.", "Because the apple was part of a tasting test.",
     ("had been washed", "came from the garden", "was still in its wrapper")),

    ("scarf", "scarf", "scarves", "the chair", "warm", "thin", ("red", "blue"),
     ("Josie put on", "before leaving the house.", "Which scarf did Josie put on?",
      "Why did Josie put on that scarf?"),
     ("Josie moved", "before leaving the house.", "Which scarf did Josie move?",
      "Why did Josie move that scarf?"),
     "was blocking the seat",
     "Because the scarf was warm.", "Because the scarf was blocking the seat.",
     ("had just been washed", "belonged to her sister", "was still in its bag")),

    ("food", "bowl of food", "bowls of food", "the kitchen floor", "tasty", "bland",
     ("tinned", "homemade"),
     ("The cat ate", "before having a nap.", "Which bowl of food did the cat eat?",
      "Why did the cat eat that bowl of food?"),
     ("The cat smelled", "before having a nap.", "Which bowl of food did the cat smell?",
      "Why did the cat smell that bowl of food?"),
     "was in an unfamiliar bowl",
     "Because the food was tasty.", "Because the food was in an unfamiliar bowl.",
     ("had been there since morning", "was in a chipped bowl", "had just been put down")),

    ("bag", "bag", "bags", "the shop floor", "pretty", "plain", ("leather", "canvas"),
     ("Florence bought", "and left the store.", "Which bag did Florence buy?",
      "Why did Florence buy that bag?"),
     ("Florence moved", "and left the store.", "Which bag did Florence move?",
      "Why did Florence move that bag?"),
     "was blocking the aisle",
     "Because the bag was pretty.", "Because the bag was blocking the aisle.",
     ("had a broken zip", "was on the top shelf", "had just been restocked")),

    ("spider", "spider", "spiders", "the desk", "scary", "harmless", ("black", "brown"),
     ("Penny screamed at", "for a long time.", "Which spider did Penny scream at?",
      "Why did Penny scream at that spider?"),
     ("Penny stroked", "for a long time.", "Which spider did Penny stroke?",
      "Why did Penny stroke that spider?"),
     "was part of her class project",
     "Because the spider was scary.", "Because the spider was part of her class project.",
     ("had escaped that morning", "was in a glass tank", "had just been fed")),

    ("trampoline", "trampoline", "trampolines", "the garden", "bouncy", "flat", ("round", "square"),
     ("The dog jumped on", "before his walk.", "Which trampoline did the dog jump on?",
      "Why did the dog jump on that trampoline?"),
     ("The dog looked at", "before his walk.", "Which trampoline did the dog look at?",
      "Why did the dog look at that trampoline?"),
     "had a torn cover",
     "Because the trampoline was bouncy.", "Because the trampoline had a torn cover.",
     ("had just been assembled", "was still in its box", "belonged to the neighbours")),

    ("painting", "painting", "paintings", "the studio", "weighty", "lightweight",
     ("framed", "unframed"),
     ("Susanne dropped", "in the living room.", "Which painting did Susanne drop?",
      "Why did Susanne drop that painting?"),
     ("Susanne displayed", "in the living room.", "Which painting did Susanne display?",
      "Why did Susanne display that painting?"),
     "had won a prize",
     "Because the painting was weighty.", "Because the painting had won a prize.",
     ("was still drying", "had been a gift", "came from the market")),
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
        (item_id, noun, plural, setting, p_pos, p_neg, q_values,
         event_p, event_z, z_fact, cause_p, cause_z, other_bg) = item
        q_pos, q_neg = q_values

        for target_index in range(4):
            # entity slots: 0 = A (target), 1 = B, 2 = C, 3 = D
            props = [(p_pos, q_pos), (p_neg, q_pos), (p_pos, q_neg), (p_pos, q_neg)]
            facts = [z_fact, other_bg[0], other_bg[1], other_bg[2]]
            # rotate which numbered entity is the target, keeping the schema fixed
            order = [(target_index + k) % 4 for k in range(4)]
            slot_of_number = {number: slot for slot, number in enumerate(order)}
            names = [f"{noun.split()[0].capitalize()} {n + 1}" for n in range(4)]
            entity_lines = []
            for number in range(4):
                slot = slot_of_number[number]
                p_val, q_val = props[slot]
                entity_lines.append(
                    f"{names[number]} is {p_val} and {q_val}; it {facts[slot]}."
                )
            number_of_slot = {slot: number for number, slot in slot_of_number.items()}
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
                                for mapping_index in range(3):
                                    ordered = (live_names[mapping_index:]
                                               + live_names[:mapping_index])
                                    options = "\n".join(
                                        f"{OPTION_LETTERS[i]}) {name}"
                                        for i, name in enumerate(ordered))
                                    gold = OPTION_LETTERS[ordered.index(target_name)]
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
                                        "p_explains": e_condition == "E_plus",
                                        "n_live_satisfying": len(satisfying),
                                        "surface_form": surface,
                                        "cue_index": cue_index,
                                        "mapping_index": mapping_index,
                                        "target_name": target_name,
                                        "gold_option": gold,
                                        "live_names": live_names,
                                        "prompt_text": (
                                            f"{scene}\n\n{cue_text}\n{critical}\n\n"
                                            f"{ref_question}\n{options}\n"
                                            f"Answer with exactly A, B or C."),
                                        "critical_sentence": critical,
                                        "modifier_span": p_pos,
                                        "np_span": phrase,
                                    })
                                # explanation readout: full and drop_p only, np surface only
                                if condition in {"full", "drop_p"} and surface == "np":
                                    for option_order in range(2):
                                        pair = ([cause_p, cause_z] if option_order == 0
                                                else [cause_z, cause_p])
                                        options = "\n".join(
                                            f"{OPTION_LETTERS[i]}) {text}"
                                            for i, text in enumerate(pair))
                                        explanation_rows.append({
                                            "stimulus_version": "b1_function_cross",
                                            "readout": "explanation",
                                            "world_id": f"b1_{world_index:04d}",
                                            "item_id": item_id,
                                            "r_condition": r_condition,
                                            "e_condition": e_condition,
                                            "description_condition": condition,
                                            "p_restricts": r_condition == "R_plus",
                                            "p_explains": e_condition == "E_plus",
                                            "cue_index": cue_index,
                                            "option_order": option_order,
                                            "p_cause_option": OPTION_LETTERS[pair.index(cause_p)],
                                            "z_cause_option": OPTION_LETTERS[pair.index(cause_z)],
                                            "prompt_text": (
                                                f"{scene}\n\n{cue_text}\n{critical}\n\n"
                                                f"{exp_question}\n{options}\n"
                                                f"Answer with exactly A or B."),
                                            "critical_sentence": critical,
                                            "verb_phrase": vp,
                                            "explanation_question": exp_question,
                                            "cause_p_text": cause_p,
                                            "cause_z_text": cause_z,
                                            "q_values": [q_pos, q_neg],
                                            "entity_names": names,
                                        })
            world_index += 1

    certify(reference_rows)
    certify_explanation(explanation_rows)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        for row in reference_rows + explanation_rows:
            handle.write(json.dumps(row) + "\n")
    print(f"wrote {len(reference_rows)} reference and {len(explanation_rows)} explanation rows "
          f"to {args.output}")


def certify(rows: list[dict]) -> None:
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
    """The explanation readout must ask about the event that was actually described, and neither
    answer option may leak the referent's identity."""
    import re

    # exact verb synchronisation: the question must be the one belonging to the event that was
    # actually described. A lexical heuristic would trip over irregular forms (fed / feed), so the
    # check is against the source table itself, and it also asserts the two events are not swapped.
    expected = {}
    for item in ITEMS:
        item_id, event_p, event_z = item[0], item[7], item[8]
        expected[(item_id, "E_plus")] = (event_p[0], event_p[3])
        expected[(item_id, "E_minus")] = (event_z[0], event_z[3])

    for row in rows:
        key = (row["item_id"], row["e_condition"])
        want_vp, want_question = expected[key]
        assert row["verb_phrase"] == want_vp, (key, row["verb_phrase"])
        assert row["explanation_question"] == want_question, (key, row["explanation_question"])
        other = "E_minus" if row["e_condition"] == "E_plus" else "E_plus"
        assert row["explanation_question"] != expected[(row["item_id"], other)][1], key
        assert row["verb_phrase"] in row["critical_sentence"], (key, row["critical_sentence"])

        # (2) neither answer option may carry Q, an entity label, or a digit
        for text in (row["cause_p_text"], row["cause_z_text"]):
            lowered = text.lower()
            for q_value in row["q_values"]:
                assert q_value.lower() not in lowered, (row["item_id"], text, q_value)
            assert not re.search(r"\d", text), (row["item_id"], text)
            for name in row["entity_names"]:
                assert name.lower() not in lowered, (row["item_id"], text, name)
    print(f"explanation certification passed on {len(rows)} rows")


if __name__ == "__main__":
    main()
