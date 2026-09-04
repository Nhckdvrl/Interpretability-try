"""Build B0: a direct LM replication of Davies & Richardson (2021).

Davies, C. & Richardson, A. (2021). Semantic as well as referential relevance facilitates the
processing of referring expressions. Journal of Pragmatics 178, 258-269.
doi:10.1016/j.pragma.2021.03.024
Materials transcribed from the author accepted manuscript deposited at White Rose Research Online
(eprints.whiterose.ac.uk/172760), Appendix "Stimulus items", critical items only.

Their design: 12 vignettes x 2 (semantic relevance: +sem / -sem) x 2 (referential relevance:
1-referent / 2-referents), fully crossed, within-participants and within-items; 48 critical trials.
The first sentence sets the referential context, the verb of the second sentence sets whether the
prenominal adjective is semantically relevant to the event, and the modified NP is identical in all
four cells of a quartet. Dependent measure: self-paced reading time in two windows, the noun phrase
(critical) and the following phrase (wrap-up).

Our LM analogue keeps the materials verbatim and replaces reading time with token surprisal over the
same two windows, which is the measure Davies & Richardson themselves appeal to when interpreting
their result (Levy 2008 surprisal theory: "doubly-relevant adjectives are less surprising, more
expected, and quicker to read"). No forced choice, no instruction following, no model-dependent
labels.

Two transcription notes, both recorded rather than silently applied:
  * item `bird`, cell -semR2, reads "There was two birds" in the appendix; the other R2 cell reads
    "There were two birds". Since this segment precedes the critical window it would perturb the
    surprisal measure, so it is normalised to "were" and flagged with `source_correction`.
  * items `table` and `chandelier` use slightly different wrap-up prepositions across the +sem/-sem
    members of a quartet. These follow the critical window, so they are kept verbatim and flagged
    with `wrapup_varies_within_quartet`.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

# item_id, (singular context, plural context), (+sem verb phrase, -sem verb phrase),
# adjective, noun, (+sem wrap-up, -sem wrap-up)
VIGNETTES = [
    ("table",
     ("In the room there was a table.", "In the room there were two tables."),
     ("The man helped his colleague move", "The man helped his colleague sit at"),
     "heavy", "table",
     ("to the middle of the room.", "in the middle of the room.")),
    ("mirror",
     ("There was a mirror on the floor.", "There were two mirrors on the floor."),
     ("The girl stepped over", "The girl looked at"),
     "broken", "mirror",
     ("when she entered the room.", "when she entered the room.")),
    ("bird",
     ("There was a bird at the side of the garden.", "There were two birds at the side of the garden."),
     ("Sarah listened to", "Sarah painted"),
     "noisy", "bird",
     ("all day long.", "all day long.")),
    ("rabbit",
     ("The rabbit was waiting in the kitchen.", "The rabbits were waiting in the kitchen."),
     ("Bob fed", "Bob tickled"),
     "hungry", "rabbit",
     ("when he got home.", "when he got home.")),
    ("chandelier",
     ("The parents bought a chandelier.", "The parents bought two chandeliers."),
     ("Their friends helped them lift", "Their friends helped them choose"),
     "large", "chandelier",
     ("in the shop.", "from the shop.")),
    ("apple",
     ("Gregg took a bite from an apple.", "Gregg took a bite from two apples."),
     ("He spat out", "He chewed"),
     "mouldy", "apple",
     ("straight away.", "straight away.")),
    ("scarf",
     ("There was a scarf on the chair.", "There were two scarves on the chair."),
     ("Josie put on", "Josie moved"),
     "warm", "scarf",
     ("before leaving the house.", "before leaving the house.")),
    ("food",
     ("There was a bowl of food next to the fridge.", "There were two bowls of food next to the fridge."),
     ("The cat ate", "The cat smelled"),
     "tasty", "food",
     ("before having a nap.", "before having a nap.")),
    ("bag",
     ("Florence noticed a bag on the shop floor.", "Florence noticed two bags on the shop floor."),
     ("She bought", "She moved"),
     "pretty", "bag",
     ("and left the store.", "and left the store.")),
    ("spider",
     ("There was a spider on Penny's book.", "There were two spiders on Penny's book."),
     ("She screamed at", "She stroked"),
     "scary", "spider",
     ("for a long time.", "for a long time.")),
    ("trampoline",
     ("Jack bought a trampoline early that morning.", "Jack bought two trampolines early that morning."),
     ("His dog jumped on", "His dog looked at"),
     "bouncy", "trampoline",
     ("before his walk.", "before his walk.")),
    ("painting",
     ("Susanne bought herself a new painting.", "Susanne bought herself two new paintings."),
     ("She dropped", "She displayed"),
     "weighty", "painting",
     ("in the living room.", "in the living room.")),
]

SOURCE_CORRECTIONS = {"bird": "appendix reads 'There was two birds' in the -semR2 cell; normalised to 'were'"}
WRAPUP_VARIES = {"table", "chandelier"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for item_id, contexts, verbs, adjective, noun, wrapups in VIGNETTES:
        for sem_index, sem_label in enumerate(("plus_sem", "minus_sem")):
            for ref_index, ref_label in enumerate(("one_referent", "two_referents")):
                context = contexts[ref_index]
                verb_phrase = verbs[sem_index]
                wrapup = wrapups[sem_index]
                prefix = f"{context} {verb_phrase} the"
                critical_window = f" {adjective} {noun}"
                wrapup_window = f" {wrapup}"
                rows.append({
                    "stimulus_version": "b0_dr_replication",
                    "source": "Davies & Richardson 2021, J. Pragmatics 178:258-269, Appendix",
                    "item_id": item_id,
                    "condition": f"{sem_label}__{ref_label}",
                    "semantic_relevance": sem_label,
                    "referential_relevance": ref_label,
                    "adjective": adjective,
                    "noun": noun,
                    "prefix": prefix,
                    "critical_window": critical_window,
                    "wrapup_window": wrapup_window,
                    "full_text": prefix + critical_window + wrapup_window,
                    "source_correction": SOURCE_CORRECTIONS.get(item_id),
                    "wrapup_varies_within_quartet": item_id in WRAPUP_VARIES,
                })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")
    print(f"wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
