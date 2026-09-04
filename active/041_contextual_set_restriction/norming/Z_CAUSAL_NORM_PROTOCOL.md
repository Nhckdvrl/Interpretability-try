# Z-event causal norming protocol — 041 Pilot B

## Why this exists

The E manipulation is a two-sided causal competitor manipulation:

```text
E+ : the matrix event is the one P bears on   -> P should win as the reason
E- : the matrix event is the one Z bears on   -> Z should win as the reason
```

Davies & Richardson (2021) validated the **P side** against 31 readers: `hungry` bears on `fed` and
not on `tickled`, `mouldy` on `spat out` and not on `chewed`. They validated nothing about `Z`,
because their design needed no alternative cause — their measure was reading time, ours is a forced
choice, which needs a defined competitor in both cells.

So `Z -> E-` is currently an experimenter-intended relation, not model-independent gold. That is
harmless for the reference readout and load-bearing for `ExplanationMargin(P)` and
`ExplanationConsequence(P)`. This protocol closes that gap on humans, before any preregistered model
is evaluated.

## Design

12 families x 2 events x 2 candidate reasons = 48 rating trials, built by
`build_z_causal_norm.py` from the same `ITEMS` table the B1 worlds are built from, so the two cannot
drift apart.

Each trial shows a **one-referent** vignette — the four-entity world is deliberately not used, since
reference is not what is being normed — in which both `P` and `Z` are stated, followed by the matrix
event and one candidate reason:

```text
There is a rabbit in the kitchen. The rabbit is hungry.
The rabbit had been very playful that evening. Bob tickled the rabbit when he got home.

Because the rabbit had been very playful that evening.

How well does this reason explain why the event happened?
1 = does not explain it at all ... 7 = explains it completely
```

**Presentation:** 4-list Latin square, deterministic assignment `(family_index + condition_index) mod
4`, certified in the builder. Each participant sees each family exactly once and three families in
each of the four conditions, so no participant ever compares two versions of the same item.
Recommended n = 32 (8 per list), matching the order of magnitude of D&R's own norming.

## Frozen pass criteria

Per family, on item means, all four must hold:

```text
P(E+) > Z(E+)      the intended reason wins when the event is the one P bears on
Z(E-) > P(E-)      the intended reason wins when the event is the one Z bears on
P(E+) > P(E-)      P's explanatory force is event-dependent
Z(E-) > Z(E+)      Z's explanatory force is event-dependent
```

Across the set, the two crossing contrasts must also hold by participant with bootstrap intervals
excluding zero (5,000 resamples over participants). Because a participant sees each family in only
one condition, the paired unit is the participant's mean per condition, not the item.

`scripts/analyze_z_causal_norm.py --ratings ratings.csv` applies exactly these criteria to a CSV of
`participant_id, trial_id, rating`.

## What happens on failure

A family that fails has its `Z` revised and is re-normed. This is permitted because it happens
before the panel is opened and is driven entirely by human judgements — no model, panel or
auxiliary, is consulted at any point. Once the panel is opened, nothing here may change.

## Constraints every authored Z satisfies by construction

1. contains no `P` and no `Q` content;
2. never appears in the referring description;
3. introduces no new discourse entity;
4. carries no uniqueness or salience marking (no "the only one", "the one that ...") that could give
   the referential readout a free signal;
5. is unrelated to the `E+` event.

Constraint 4 removed the first drafts of `table` ("was the only one with a free chair") and `spider`
("was the one from her class project"). Constraint 3 removed the first draft of `trampoline` ("had a
squirrel sitting on it"). Constraint 5 is why `trampoline` uses "had a torn cover" rather than "had
begun to wobble": wobbling is semantically adjacent to `bouncy` and would blur the E+/E- crossing
this protocol is meant to certify.
