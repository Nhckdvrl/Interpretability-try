"""Adjective-event families for B1.

Each family is one property `P` of one noun, paired with two events: one the property bears on
(`+sem`) and one it does not (`-sem`). Events are stored as (agent, past form, base form, wrap-up)
so the reference question ("Which N did AGENT BASE?") and the explanation question ("Why did AGENT
BASE that N?") are generated mechanically. Writing those questions by hand is what produced the
irregular-verb bug the certification caught (`fed` / `feed`), so they are never authored.

`source` marks provenance:

  davies_richardson -- the 12 critical quartets of Davies & Richardson (2021), J. Pragmatics
                       178:258-269, verbatim verbs. Their +sem/-sem contrast was validated on 31
                       readers and verb frequency was controlled within quartet to 1.2 Zipf.
  extended          -- 36 further families written to the same template. Revised once, on
                       linguistic grounds, after a per-item manipulation check showed 7 of the 48
                       failing: in each case either the `-sem` verb plausibly bore on the property
                       after all ("wiped a boiling kettle", "rotated a punctured tyre", "swept a
                       slippery floor") or the Q value did not sit with the noun ("wooden knife",
                       "wide lawn"). The 12 inherited families were never touched, so the core
                       analysis is unaffected by the revision to raise the number of
                       independent units, since the bootstrap resamples families and twelve is too
                       few for the causal claims. These are NOT frequency-controlled and were not
                       normed on humans; every result is therefore reported on the inherited core
                       and on the full set separately, so the human-validated subset stands alone.

Fields: item, noun, plural, explanation_noun, setting, P+, P-, (Q+, Q-), plus_sem event,
minus_sem event, source.
"""

from __future__ import annotations

DAVIES_RICHARDSON = [
    ("table", "table", "tables", "table", "the meeting room", "heavy", "light", ("brown", "white"),
     ("Mark", "helped Tom move", "help Tom move", "to the middle of the room."),
     ("Mark", "helped Tom sit at", "help Tom sit at", "at the end of the meeting.")),
    ("mirror", "mirror", "mirrors", "mirror", "the hallway", "broken", "intact", ("gold", "silver"),
     ("Ella", "stepped over", "step over", "on her way out."),
     ("Ella", "looked at", "look at", "on her way out.")),
    ("bird", "bird", "birds", "bird", "the garden", "noisy", "quiet", ("brown", "grey"),
     ("Sarah", "listened to", "listen to", "all afternoon."),
     ("Sarah", "painted", "paint", "all afternoon.")),
    ("rabbit", "rabbit", "rabbits", "rabbit", "the kitchen", "hungry", "well-fed", ("brown", "white"),
     ("Bob", "fed", "feed", "when he got home."),
     ("Bob", "tickled", "tickle", "when he got home.")),
    ("chandelier", "chandelier", "chandeliers", "chandelier", "the shop", "large", "small",
     ("brass", "crystal"),
     ("Nina", "helped them lift", "help them lift", "onto the counter."),
     ("Nina", "helped them choose", "help them choose", "for the dining room.")),
    ("apple", "apple", "apples", "apple", "the bowl", "mouldy", "fresh", ("red", "green"),
     ("Gregg", "spat out", "spit out", "straight away."),
     ("Gregg", "chewed", "chew", "straight away.")),
    ("scarf", "scarf", "scarves", "scarf", "the chair", "warm", "thin", ("red", "blue"),
     ("Josie", "put on", "put on", "before leaving the house."),
     ("Josie", "moved", "move", "before leaving the house.")),
    ("food", "bowl of food", "bowls of food", "food", "the kitchen floor", "tasty", "bland",
     ("tinned", "homemade"),
     ("the cat", "ate", "eat", "before having a nap."),
     ("the cat", "smelled", "smell", "before having a nap.")),
    ("bag", "bag", "bags", "bag", "the shop floor", "pretty", "plain", ("leather", "canvas"),
     ("Florence", "bought", "buy", "and left the store."),
     ("Florence", "moved", "move", "and left the store.")),
    ("spider", "spider", "spiders", "spider", "the desk", "scary", "harmless", ("black", "brown"),
     ("Penny", "screamed at", "scream at", "for a long time."),
     ("Penny", "stroked", "stroke", "for a long time.")),
    ("trampoline", "trampoline", "trampolines", "trampoline", "the garden", "bouncy", "flat",
     ("round", "square"),
     ("the dog", "jumped on", "jump on", "before his walk."),
     ("the dog", "looked at", "look at", "before his walk.")),
    ("painting", "painting", "paintings", "painting", "the studio", "weighty", "lightweight",
     ("framed", "unframed"),
     ("Susanne", "dropped", "drop", "in the living room."),
     ("Susanne", "displayed", "display", "in the living room.")),
]

EXTENDED = [
    ("kettle", "kettle", "kettles", "kettle", "the office kitchen", "empty", "full",
     ("steel", "plastic"),
     ("Ana", "filled", "fill", "before the meeting."),
     ("Ana", "labelled", "label", "before the meeting.")),
    ("window", "window", "windows", "window", "the stairwell", "cracked", "intact",
     ("wide", "narrow"),
     ("Ravi", "taped up", "tape up", "that afternoon."),
     ("Ravi", "measured", "measure", "that afternoon.")),
    ("shirt", "shirt", "shirts", "shirt", "the laundry room", "stained", "clean", ("linen", "cotton"),
     ("Omar", "soaked", "soak", "in the sink."),
     ("Omar", "folded", "fold", "by the sink.")),
    ("dog", "dog", "dogs", "dog", "the yard", "muddy", "dry", ("black", "tan"),
     ("Lena", "hosed down", "hose down", "after the walk."),
     ("Lena", "photographed", "photograph", "after the walk.")),
    ("knife", "knife", "knives", "knife", "the workshop", "blunt", "sharp", ("kitchen", "carving"),
     ("Theo", "sharpened", "sharpen", "before dinner."),
     ("Theo", "rinsed", "rinse", "before dinner.")),
    ("bread", "loaf", "loaves", "loaf", "the pantry", "stale", "fresh", ("brown", "white"),
     ("Mira", "toasted", "toast", "for breakfast."),
     ("Mira", "sliced", "slice", "for breakfast.")),
    ("battery", "battery", "batteries", "battery", "the drawer", "flat", "charged",
     ("black", "silver"),
     ("Ines", "replaced", "replace", "that evening."),
     ("Ines", "labelled", "label", "that evening.")),
    ("path", "path", "paths", "path", "the courtyard", "icy", "dry", ("gravel", "brick"),
     ("Karl", "gritted", "grit", "before dawn."),
     ("Karl", "photographed", "photograph", "before dawn.")),
    ("plant", "plant", "plants", "plant", "the conservatory", "wilting", "thriving",
     ("tall", "short"),
     ("Dora", "watered", "water", "that morning."),
     ("Dora", "moved", "move", "that morning.")),
    ("letter", "letter", "letters", "letter", "the post room", "urgent", "routine",
     ("sealed", "open"),
     ("Sam", "posted", "post", "the same day."),
     ("Sam", "signed", "sign", "the same day.")),
    ("tyre", "tyre", "tyres", "tyre", "the garage", "punctured", "sound", ("front", "rear"),
     ("Nils", "patched", "patch", "before the trip."),
     ("Nils", "measured", "measure", "before the trip.")),
    ("lamp", "lamp", "lamps", "lamp", "the hallway", "dusty", "spotless", ("brass", "ceramic"),
     ("Rosa", "cleaned", "clean", "over the weekend."),
     ("Rosa", "moved", "move", "over the weekend.")),
    ("cat", "cat", "cats", "cat", "the clinic", "limping", "healthy", ("grey", "ginger"),
     ("Ilse", "examined", "examine", "that afternoon."),
     ("Ilse", "brushed", "brush", "that afternoon.")),
    ("box", "box", "boxes", "box", "the loading bay", "fragile", "sturdy", ("wooden", "cardboard"),
     ("Hugo", "padded", "pad", "before the van arrived."),
     ("Hugo", "labelled", "label", "before the van arrived.")),
    ("soup", "soup", "soups", "soup", "the canteen", "cold", "hot",
     ("tomato", "chicken"),
     ("Yara", "heated", "heat", "before serving."),
     ("Yara", "stirred", "stir", "before serving.")),
    ("door", "door", "doors", "door", "the corridor", "squeaky", "silent", ("oak", "pine"),
     ("Piet", "oiled", "oil", "on Monday."),
     ("Piet", "painted", "paint", "on Monday.")),
    ("photo", "photo", "photos", "photo", "the album", "blurry", "sharp", ("colour", "digital"),
     ("Nina", "deleted", "delete", "the next day."),
     ("Nina", "printed", "print", "the next day.")),
    ("suitcase", "suitcase", "suitcases", "suitcase", "the hallway", "heavy", "light",
     ("blue", "grey"),
     ("Rafi", "wheeled", "wheel", "to the taxi."),
     ("Rafi", "zipped", "zip", "by the taxi.")),
    ("cup", "cup", "cups", "cup", "the cupboard", "chipped", "whole", ("china", "paper"),
     ("Elsa", "discarded", "discard", "after breakfast."),
     ("Elsa", "washed", "wash", "after breakfast.")),
    ("hedge", "hedge", "hedges", "hedge", "the front garden", "overgrown", "trim",
     ("long", "short"),
     ("Bram", "cut back", "cut back", "on Saturday."),
     ("Bram", "photographed", "photograph", "on Saturday.")),
    ("floor", "floor", "floors", "floor", "the lobby", "wet", "dry", ("wooden", "concrete"),
     ("Tess", "dried", "dry", "before opening."),
     ("Tess", "measured", "measure", "before opening.")),
    ("clock", "clock", "clocks", "clock", "the classroom", "slow", "accurate", ("round", "square"),
     ("Jonas", "reset", "reset", "after the holiday."),
     ("Jonas", "mounted", "mount", "after the holiday.")),
    ("jacket", "jacket", "jackets", "jacket", "the cloakroom", "torn", "intact",
     ("denim", "leather"),
     ("Anya", "repaired", "repair", "that evening."),
     ("Anya", "folded", "fold", "that evening.")),
    ("fish", "fish", "fish", "fish", "the cold room", "spoiled", "fresh", ("large", "small"),
     ("Kito", "binned", "bin", "before service."),
     ("Kito", "weighed", "weigh", "before service.")),
    ("road", "road", "roads", "road", "the valley", "flooded", "clear", ("main", "back"),
     ("Pia", "avoided", "avoid", "on the way north."),
     ("Pia", "photographed", "photograph", "on the way north.")),
    ("book", "book", "books", "book", "the archive", "damaged", "pristine", ("thick", "thin"),
     ("Ovi", "repaired", "repair", "over the summer."),
     ("Ovi", "catalogued", "catalogue", "over the summer.")),
    ("rope", "rope", "ropes", "rope", "the boathouse", "frayed", "sound", ("thick", "thin"),
     ("Vera", "replaced", "replace", "before the race."),
     ("Vera", "coiled", "coil", "before the race.")),
    ("seat", "seat", "seats", "seat", "the workshop", "wobbly", "firm", ("front", "back"),
     ("Milo", "tightened", "tighten", "on Friday."),
     ("Milo", "measured", "measure", "on Friday.")),
    ("milk", "carton of milk", "cartons of milk", "milk", "the fridge", "sour", "fresh",
     ("open", "sealed"),
     ("Rina", "poured away", "pour away", "before lunch."),
     ("Rina", "labelled", "label", "before lunch.")),
    ("gate", "gate", "gates", "gate", "the back lane", "rusty", "new", ("iron", "timber"),
     ("Sana", "sanded", "sand", "that weekend."),
     ("Sana", "photographed", "photograph", "that weekend.")),
    ("lawn", "lawn", "lawns", "lawn", "the park", "parched", "lush", ("front", "back"),
     ("Emil", "sprinkled", "sprinkle", "at sunset."),
     ("Emil", "mowed", "mow", "at sunset.")),
    ("cable", "cable", "cables", "cable", "the server room", "exposed", "insulated",
     ("orange", "black"),
     ("Ida", "taped", "tape", "before the inspection."),
     ("Ida", "labelled", "label", "before the inspection.")),
    ("room", "room", "rooms", "room", "the guest wing", "stuffy", "airy", ("upstairs", "downstairs"),
     ("Otto", "aired out", "air out", "before the guests came."),
     ("Otto", "measured", "measure", "before the guests came.")),
    ("scooter", "scooter", "scooters", "scooter", "the bike rack", "unlocked", "secured",
     ("red", "silver"),
     ("Ruth", "chained up", "chain up", "before her shift."),
     ("Ruth", "polished", "polish", "before her shift.")),
    ("mattress", "mattress", "mattresses", "mattress", "the spare room", "lumpy", "even",
     ("double", "single"),
     ("Iris", "replaced", "replace", "before the weekend."),
     ("Iris", "measured", "measure", "before the weekend.")),
    ("coat", "coat", "coats", "coat", "the porch", "damp", "dry", ("long", "short"),
     ("Bo", "dried", "dry", "after the walk."),
     ("Bo", "buttoned", "button", "after the walk.")),
]

ITEMS = ([tuple(list(item) + ["davies_richardson"]) for item in DAVIES_RICHARDSON]
         + [tuple(list(item) + ["extended"]) for item in EXTENDED])

assert len({item[0] for item in ITEMS}) == len(ITEMS), "duplicate item id"
assert len(ITEMS) == 48, len(ITEMS)

# The critical sentence is VERB PHRASE + NOUN PHRASE + wrap-up, so a verb phrase carrying its own
# article-bearing complement strands the object: "Bo hung by the fire the damp long coat".
for _item in ITEMS:
    for _event in (_item[8], _item[9]):
        for _form in (_event[1], _event[2]):
            assert " the " not in f" {_form} ", (_item[0], _form)
            assert " a " not in f" {_form} ", (_item[0], _form)
