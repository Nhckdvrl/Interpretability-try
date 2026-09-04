"""Build the frozen S0 misdescription crossover for referential vs attributive description use.

Every world is a Donnellan misdescription conflict: the speaker's independently established
target R does **not** satisfy the description F, while a second entity S does. The critical
description and every world fact are identical across contexts; only the speaker's relation to
the situation changes.

    referential          -- R is established as the speaker's attended/known target
    attributive_bare     -- no target is established at all
    attributive_matched  -- R is established with the *same* attention clause as referential,
                            but the speaker explicitly wants whoever actually satisfies F

v2 fixes two construction defects found by the first run. (1) The referential frame did not
actually instantiate Donnellan's referential use: it established an attended person and then had
the speaker request a description, which reads as two separate wants. Referential use requires the
speaker to *believe the description fits their target* and to use it to pick that person out, so
that belief is now stated -- it is constitutive of the use mode, not a hint. (2) The speaker-target
denominator asked one clumsy disjunctive question covering both establishment families and scored
below chance; each family now gets its own question. A downstream-action probe is also added so the
result does not rest on a single metalinguistic question.

`attributive_matched` is the control that matters: it equalises R's salience, mention count and
recency against the referential context while reversing the intended use, so a crossover that
survives it cannot be raw salience. It also drops the word `whoever`, so the use mode is not
carried by one lexical trigger.

Denominator probes reuse each scene verbatim and ask only for raw facts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

# (item, setting, role noun, description, F-predicate question form, R's own fact,
#  R fact predicate, S fact clause, description family)
ITEMS = [
    ("reception", "reception", "guest", "the guest drinking a martini", "is drinking a martini",
     "is drinking sparkling water", "is drinking sparkling water", "is drinking a martini", "participial"),
    ("gallery", "gallery opening", "visitor", "the visitor carrying the black folder",
     "is carrying the black folder", "is carrying a brown folder", "is carrying a brown folder",
     "is carrying the black folder", "participial"),
    ("clinic", "clinic waiting room", "patient", "the patient who came in with a fever",
     "came in with a fever", "came in with a sprained wrist", "came in with a sprained wrist",
     "came in with a fever", "relative_clause"),
    ("newsroom", "newsroom", "editor", "the editor who signs off on the front page",
     "signs off on the front page", "signs off on the culture pages", "signs off on the culture pages",
     "signs off on the front page", "role"),
    ("workshop", "workshop", "apprentice", "the apprentice wearing the safety goggles",
     "is wearing the safety goggles", "is wearing reading glasses", "is wearing reading glasses",
     "is wearing the safety goggles", "participial"),
    ("conference", "conference", "delegate", "the delegate who arrived with the minister",
     "arrived with the minister", "arrived alone", "arrived alone", "arrived with the minister",
     "relational"),
    ("library", "library", "volunteer", "the volunteer who keeps the donation ledger",
     "keeps the donation ledger", "keeps the event calendar", "keeps the event calendar",
     "keeps the donation ledger", "role"),
    ("kitchen", "kitchen", "cook", "the cook preparing the dessert", "is preparing the dessert",
     "is preparing the soup", "is preparing the soup", "is preparing the dessert", "participial"),
    ("station", "station office", "passenger", "the passenger who lost a suitcase", "lost a suitcase",
     "lost an umbrella", "lost an umbrella", "lost a suitcase", "relative_clause"),
    ("school", "school", "teacher", "the teacher who runs the chess club", "runs the chess club",
     "runs the choir", "runs the choir", "runs the chess club", "role"),
    ("depot", "depot", "driver", "the driver who signed for the sealed crate",
     "signed for the sealed crate", "signed for the open pallet", "signed for the open pallet",
     "signed for the sealed crate", "relational"),
    ("studio", "studio", "assistant", "the assistant holding the blue clipboard",
     "is holding the blue clipboard", "is holding a grey notebook", "is holding a grey notebook",
     "is holding the blue clipboard", "participial"),
]

NAME_PAIRS = [("Mr. Vale", "Mr. Reed"), ("Ms. Larkin", "Ms. Doyle"), ("Mr. Osei", "Mr. Novak")]
SPEAKERS = ["Ann", "Bea"]
PLACES = [("by the window", "by the door"), ("near the stairs", "near the desk")]
ESTABLISHMENT = {
    "perceptual": "{speaker} has been watching the {role} standing {place} for a while now and wants to talk to that person.",
    "acquaintance": "{speaker} met the {role} standing {place} last week and has been meaning to continue that conversation.",
}
TARGET_QUESTIONS = {
    "perceptual": "Which person has {speaker} been watching?",
    "acquaintance": "Which person did {speaker} meet last week?",
}
CONTEXTS = ["referential", "attributive_bare", "attributive_matched"]
PROBES = ["use_mode", "downstream_action", "description_truth", "speaker_target_fact", "entity_fact"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    rows = []
    counter = 0
    for (item, setting, role, description, f_predicate, r_fact_clause, r_predicate,
         s_fact_clause, family) in ITEMS:
        for name_index, (name_x, name_y) in enumerate(NAME_PAIRS):
            for target_is_first in [True, False]:
                target_name, satisfier_name = ((name_x, name_y) if target_is_first
                                               else (name_y, name_x))
                for place_index, (place_target, place_satisfier) in enumerate(PLACES):
                    for presentation_first_is_target in [True, False]:
                        entries = [(target_name, place_target, r_fact_clause),
                                   (satisfier_name, place_satisfier, s_fact_clause)]
                        if not presentation_first_is_target:
                            entries = list(reversed(entries))
                        scene = (f"Setting: at the {setting} there are two people.\n"
                                 + "\n".join(f"{name} is standing {place} and {fact}."
                                             for name, place, fact in entries))
                        speaker = SPEAKERS[counter % len(SPEAKERS)]
                        for establishment_name, establishment in ESTABLISHMENT.items():
                            attention = establishment.format(speaker=speaker, role=role,
                                                             place=place_target)
                            for context in CONTEXTS:
                                if context == "referential":
                                    frame = (f"{attention} {speaker} believes that this is the person "
                                             f"who {f_predicate}, and has that person in mind.")
                                elif context == "attributive_bare":
                                    frame = (f"{speaker} has not looked at anyone here and knows none of "
                                             f"them. {speaker} has only been told that exactly one "
                                             f"{role} here {f_predicate}, and wants to meet that person, "
                                             "whoever it is.")
                                else:
                                    frame = (f"{attention} In this case, however, {speaker} does not "
                                             f"care who that is and is interested only in the person "
                                             f"who {f_predicate}, whoever that turns out to be.")
                                for probe in PROBES:
                                    if probe == "speaker_target_fact" and context == "attributive_bare":
                                        continue
                                    if probe == "use_mode":
                                        question = f"Which person does {speaker} mean?"
                                        gold_name = (target_name if context == "referential"
                                                     else satisfier_name)
                                    elif probe == "downstream_action":
                                        question = (f"The host goes to fetch the person {speaker} "
                                                    "asked for. Which person should the host bring?")
                                        gold_name = (target_name if context == "referential"
                                                     else satisfier_name)
                                    elif probe == "description_truth":
                                        question = f"Which person {f_predicate}?"
                                        gold_name = satisfier_name
                                    elif probe == "speaker_target_fact":
                                        question = TARGET_QUESTIONS[establishment_name].format(
                                            speaker=speaker)
                                        gold_name = target_name
                                    else:
                                        question = f"Which person {r_predicate}?"
                                        gold_name = target_name
                                    for mapping_index in range(2):
                                        options = ([target_name, satisfier_name] if mapping_index == 0
                                                   else [satisfier_name, target_name])
                                        option_text = "\n".join(f"{tag}) {name}" for tag, name
                                                                in zip(["A", "B"], options))
                                        gold_option = "A" if options[0] == gold_name else "B"
                                        rows.append({
                                            "stimulus_version": config["stimulus_version"],
                                            "item": item, "description_family": family,
                                            "world_id": f"rva_{item}_{name_index}{int(target_is_first)}"
                                                        f"{place_index}{int(presentation_first_is_target)}",
                                            "context": context, "establishment": establishment_name,
                                            "probe": probe, "speaker": speaker,
                                            "target_name": target_name, "satisfier_name": satisfier_name,
                                            "gold_name": gold_name, "gold_option": gold_option,
                                            "other_option": "B" if gold_option == "A" else "A",
                                            "target_option": "A" if options[0] == target_name else "B",
                                            "satisfier_option": "A" if options[0] == satisfier_name else "B",
                                            "mapping_index": mapping_index,
                                            "prompt_text": (
                                                f"{scene}\n\n{frame}\n"
                                                f"{speaker} says: \"I need to speak with {description}.\"\n\n"
                                                f"{question}\n{option_text}\n"
                                                "Answer with exactly A or B."
                                            ),
                                        })
                        counter += 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(rows), "items": len(ITEMS),
                      "worlds": counter}))


if __name__ == "__main__":
    main()
