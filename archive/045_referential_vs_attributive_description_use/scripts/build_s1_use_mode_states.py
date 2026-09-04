"""v3 worlds: trackable speaker target, paraphrased use-mode frames, description-token states.

Two changes from v2, both forced by its results rather than by the prediction it missed.

1. The speaker-target denominator failed in two of three families (Llama 0.506 with a pure A/B
   position fallback, Phi 0.649), because the target was established by description
   ("the guest standing by the window") and had to be resolved to a name. The target is now named
   directly. That does not reintroduce a salience confound: the confound control is the matched
   attributive frame, which contains the *identical* clause, not the absence of naming.
2. A single wording per use mode meant a probe could decode the frame's words rather than a use
   mode. Each mode now has three paraphrases so a direction can be trained on some and tested on
   held-out ones, which is what Lock B asks for.

States are captured at the last token of the critical description inside the utterance, which
precedes the question, so one state serves every probe and answer mapping.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_s0_use_mode_crossover import ITEMS, NAME_PAIRS, SPEAKERS

# v4: every frame opens with the identical target-establishing sentence, so the speaker's target
# has exactly the same salience, mention count and recency in both use modes and the denominator
# question is unambiguous. Referential frames now mark the speaker's belief as *false*, because in
# v3 the bare assertion "Ann believes X is the one who ..." was absorbed as a world fact and raw
# entity accuracy fell to 0.45 in referential contexts only.
COMMON_ESTABLISHMENT = "{speaker} has been watching {target} for a while now."
REFERENTIAL_FRAMES = [
    ("r1", "{speaker} mistakenly believes {target} is the one who {predicate}, and it is {target} "
           "that {speaker} is talking about."),
    ("r2", "Wrongly taking {target} to be the one who {predicate}, {speaker} is speaking about "
           "{target}."),
    ("r3", "{speaker} is under the false impression that {target} {predicate}, and is asking "
           "about {target}."),
]
# v6: the decisive contrast. v5's referential frames end by *stating* whom the speaker is talking
# about, so following them needs no inference. These frames give the same attention clause and the
# same false belief but never say who is meant, so the referential reading has to be derived. If
# accuracy collapses here while the explicit frames succeed, the models are following a stated
# referent rather than computing speaker reference.
INFERRED_FRAMES = [
    ("i1", "{speaker} mistakenly believes {target} is the one who {predicate}."),
    ("i2", "{speaker} has wrongly concluded that {target} {predicate}."),
    ("i3", "As it happens, {speaker} is under the false impression that {target} {predicate}."),
]
ATTRIBUTIVE_FRAMES = [
    ("a1", "In this case, however, {speaker} does not care who that is and wants only the person "
           "who {predicate}, whoever that turns out to be."),
    ("a2", "Setting that aside, {speaker} needs the person who {predicate}, and no one else, "
           "regardless of who it is."),
    ("a3", "What {speaker} needs now is simply the person who {predicate}, whichever person that "
           "is."),
]
BARE_FRAME = ("bare", "{speaker} has not looked at anyone here and knows none of them. {speaker} "
                      "has only been told that exactly one person here {predicate}, and wants to "
                      "meet that person, whoever it is.")
# v5 splits the action readout by whose information state the actor has. v4's single "the host
# goes to fetch..." question let a model legitimately answer from a third party's viewpoint, since
# the host never heard what the speaker believes; that ambiguity, not a representation-action gap,
# could explain why the action readout collapsed while `use_mode` did not.
PROBES = ["use_mode", "speaker_action", "informed_agent_action", "host_action",
          "description_truth", "speaker_target_fact", "entity_fact"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    frames = ([("referential", name, f"{COMMON_ESTABLISHMENT} {text}")
               for name, text in REFERENTIAL_FRAMES]
              + [("referential_inferred", name, f"{COMMON_ESTABLISHMENT} {text}")
                 for name, text in INFERRED_FRAMES]
              + [("attributive_matched", name, f"{COMMON_ESTABLISHMENT} {text}")
                 for name, text in ATTRIBUTIVE_FRAMES]
              + [("attributive_bare", BARE_FRAME[0], BARE_FRAME[1])])
    rows = []
    counter = 0
    for (item, setting, role, description, f_predicate, r_fact_clause, r_predicate,
         s_fact_clause, family) in ITEMS:
        for name_index, (name_x, name_y) in enumerate(NAME_PAIRS):
            for target_is_first in [True, False]:
                target_name, satisfier_name = ((name_x, name_y) if target_is_first
                                               else (name_y, name_x))
                entries = [(target_name, r_fact_clause), (satisfier_name, s_fact_clause)]
                if not target_is_first:
                    entries = list(reversed(entries))
                scene = (f"Setting: at the {setting} there are two people.\n"
                         + "\n".join(f"{name} {fact}." for name, fact in entries))
                speaker = SPEAKERS[counter % len(SPEAKERS)]
                world = f"rva3_{item}_{name_index}{int(target_is_first)}"
                for context, frame_name, template in frames:
                    frame = template.format(speaker=speaker, target=target_name,
                                            predicate=f_predicate)
                    for probe in PROBES:
                        if probe == "speaker_target_fact" and context == "attributive_bare":
                            continue
                        if probe == "use_mode":
                            question = f"Which person does {speaker} mean?"
                            gold_name = (target_name if context.startswith("referential") else satisfier_name)
                        elif probe == "speaker_action":
                            question = (f"{speaker} then walks over to the person {speaker} was "
                                        f"asking for. Which person does {speaker} walk over to?")
                            gold_name = (target_name if context.startswith("referential") else satisfier_name)
                        elif probe == "informed_agent_action":
                            question = (f"{speaker}'s assistant knows exactly whom {speaker} has "
                                        f"been watching and what {speaker} believes. The assistant "
                                        f"fetches the person {speaker} was asking for. Which person "
                                        "does the assistant bring?")
                            gold_name = (target_name if context.startswith("referential") else satisfier_name)
                        elif probe == "host_action":
                            question = (f"The host goes to fetch the person {speaker} asked for. "
                                        "Which person should the host bring?")
                            gold_name = (target_name if context.startswith("referential") else satisfier_name)
                        elif probe == "description_truth":
                            question = f"Which person {f_predicate}?"
                            gold_name = satisfier_name
                        elif probe == "speaker_target_fact":
                            question = f"Which person has {speaker} been watching?"
                            gold_name = target_name
                        else:
                            question = (f"According to the setting described at the start, which "
                                        f"person {r_predicate}?")
                            gold_name = target_name
                        for mapping_index in range(2):
                            options = ([target_name, satisfier_name] if mapping_index == 0
                                       else [satisfier_name, target_name])
                            option_text = "\n".join(f"{tag}) {name}" for tag, name
                                                    in zip(["A", "B"], options))
                            gold_option = "A" if options[0] == gold_name else "B"
                            rows.append({
                                "stimulus_version": config["stimulus_version"],
                                "item": item, "description_family": family, "world_id": world,
                                "context": context, "frame": frame_name, "probe": probe,
                                "speaker": speaker, "target_name": target_name,
                                "satisfier_name": satisfier_name, "gold_name": gold_name,
                                "gold_option": gold_option,
                                "other_option": "B" if gold_option == "A" else "A",
                                "target_option": "A" if options[0] == target_name else "B",
                                "satisfier_option": "A" if options[0] == satisfier_name else "B",
                                "mapping_index": mapping_index,
                                "critical_description": description,
                                "state_key": f"{world}|{context}|{frame_name}",
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
    print(json.dumps({"output": str(args.output), "rows": len(rows), "worlds": counter,
                      "state_rows": len({row["state_key"] for row in rows})}))


if __name__ == "__main__":
    main()
