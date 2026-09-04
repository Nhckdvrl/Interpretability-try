# 041 — Main-paper blueprint (2026-09-04, rev 5)

Supersedes the framing in `README.md` section A. The **scientific object is unchanged**; the
paper-level question is allowed to grow. Existing results are an evidence inventory, not a track.

Revision history:
- rev 2 — implicit-causality verbs removed from the E manipulation; Davies & Richardson (2021) made
  the human mother; sibling modifier `Q` and explanation competitor `Z` decoupled; behavioural object
  restated as a functional-selectivity matrix; C5 restated as branch-point localisation.
- rev 5 — the explanation readout became a scored fixed continuation and the authored background
  fact `Z` was removed from the design, so B1 relies on no causal gold we invented.
- rev 4 — execution order fixed as freeze -> B0 -> B1 and recorded in
  `B1_PREANALYSIS_FREEZE.md`; B1 worlds and analysis plan built and tagged.
- rev 3 — Davies & Richardson AAM obtained and read; their 2x2 is confirmed fully crossed and their
  12 critical quartets are inherited verbatim as **B0**; modifier surprisal promoted from a felicity
  check to the direct LM analogue of their dependent measure; **no model of any kind is used for item
  selection** and the four-family panel is preserved intact.

## 0. Paper question

> **When descriptive content is true, how does an LLM determine what that content is currently doing
> in the discourse — separately from what it says?**

Stage 1 studies exactly two theoretically clean functions:

- **referential relevance** — does this content narrow the live candidate set?
- **semantic / explanatory relevance** — does this content bear on why the matrix event happened?

There is deliberately **no third "pure extra description" category.** Leffel et al. (2014) argue that
a modifier that does not restrict normally still needs a discourse relation to be licensed
(`I visited my sick mother` vs `#I visited my tall mother`), so a "purely redundant" cell is a
felicity artifact waiting to happen, not a function. The two functions are **crossable**, not two
labels on one scale: `R+E+` is expected (Hoek et al. 2020 — restrictive material can simultaneously
enter causal/concessive coherence relations).

## 1. Human mother, and exactly where our delta starts

**Davies, C. & Richardson, A. (2021). "Semantic as well as referential relevance facilitates the
processing of referring expressions." *Journal of Pragmatics* 178, 258-269.
doi:10.1016/j.pragma.2021.03.024.** Author accepted manuscript: White Rose Research Online
eprints.whiterose.ac.uk/172760. Read in full.

Their design, verbatim from Methods: *"The experiment used a 2x2 design. Semantic relevance
(relevant; irrelevant) and referential relevance (1-referent; 2-referents) were fully crossed,
yielding four conditions. Both variables were manipulated within-participants and within-items."*
12 vignettes x 4 versions = 48 critical trials plus 72 fillers, N=31, self-paced reading, two
analysis windows: the noun phrase (critical) and the following phrase (wrap-up). The modified NP is
identical across a quartet; only the first sentence (referential context) and the verb (semantic
context) change — `Bob fed / tickled the hungry rabbit`, `He spat out / chewed the mouldy apple`.

Three facts from their results that shape this blueprint:

1. **Both main effects are significant and the interaction is not.** Overspecified NPs are read more
   slowly, and that penalty is mitigated when the adjective is semantically relevant. They predicted
   an additive effect and got one; the two-referent/relevant cell is fastest (666 ms) and the two
   non-relevant cells slowest (872 ms), but the interaction did not reach significance.
2. **The two relevances have different time courses.** Semantic relevance is significant only in the
   NP window; referential relevance persists into the wrap-up window. *"Semantic irrelevance is
   problematic only in the earlier stages of processing."*
3. **They interpret their own effect as surprisal** (Levy 2008): *"doubly-relevant adjectives are
   less surprising, more expected, and quicker to read."*

What this buys us, stated plainly rather than worked around:

> **The behavioural R x E factorization is owned by human psycholinguistics.** It is our denominator.

And what it does *not* settle — which is where the paper starts:

> A behavioural null interaction cannot distinguish "two independent functional computations" from
> "one undifferentiated relevance signal that both manipulations feed". Reading times cannot answer
> it; internal causal organisation can. Fact (2) — that the two relevances already differ in *when*
> they act in humans — is the human prior for asking **where in the model's computation the two
> functions separate.**

Theory lineage: Leffel et al. 2014 (non-restrictive modifiers need an explanation-type relation);
Hoek et al. 2020 (restriction and coherence are not mutually exclusive); Rohde et al. (coherence
expectations act in real time).

**Rohde's implicit-causality verbs are excluded from the E manipulation.** IC verbs shift discourse
focus, next-mention and reference expectations by themselves. If the E axis were built on them and we
later found `E manipulation -> ReferenceMargin`, we could not separate "the modifier's explanatory
role leaked into reference" from "the IC verb moved referential salience directly" — and that
off-diagonal is the whole experiment. We would be manufacturing an alternate explanation we cannot
remove. D&R's verbs are ordinary transitive verbs whose relation to the adjective is the manipulated
variable, which is exactly what we need.

## 2. Experiment ladder

Execution order is frozen in `B1_PREANALYSIS_FREEZE.md` (tag `B1_PREANALYSIS_FREEZE`) and is **not**
the order in which the experiments are presented: the B1 design and analysis plan are frozen first,
*then* the panel is opened, *then* B0 runs, *then* B1. B0 is explicitly not a gate for B1 — no family
is dropped or kept on its B0 result. B0 and B1 share the inherited D&R adjective-event families, so
the claim we make is not that their materials are disjoint, but that no B1 trial was evaluated and no
B0 outcome was used for item, family, model, window or analysis selection before the freeze.

```text
B0  direct replication of D&R in an LM
    their 48 items verbatim, their two windows, surprisal instead of reading time
    -> human-anchored denominator + the natural-language window
                    |
B1  041-ised worlds: denotational R x inherited E, two forced-choice readouts
    -> the functional-selectivity matrix
                    |
B2  mechanism: separability of internal states, causal double dissociation,
    branch-point localisation
```

### B0 — the replication (built, `stimuli/b0_dr_replication.jsonl`, 48 rows)

Materials verbatim from their Appendix; two transcription notes recorded in
`scripts/build_b0_dr_replication.py` rather than silently applied. Measure: mean token surprisal over
the **NP window** (adjective + noun) and the **wrap-up window** (the following phrase), which is the
measure they themselves invoke. No forced choice, no instruction following, no model-dependent
labels — this runs on base models unchanged.

Predictions inherited from the human data, so they are gates, not claims: main effect of referential
relevance and of semantic relevance on NP-window surprisal; referential relevance surviving into the
wrap-up window while semantic relevance does not. B0 costs almost nothing and does three jobs: it
anchors the whole project to a published human result, it supplies the natural-language window that
S4's metalinguistic readout failed to supply, and its window asymmetry is the first evidence bearing
on the branch-point question in C5.

**One honest limitation of their referential manipulation, and what we do about it.** `There were two
spiders` licenses the modifier by supplying a contrast set, but it does not make `the scary spider`
*denotationally* restricting — no properties are given for the second spider. Their referential
factor is therefore a **licensing** manipulation, weaker than 041's model-independent gold. We do not
patch their materials; we keep B0 as the faithful replication and put the denotational manipulation
in B1.

### B1 — the crossed worlds

```text
   WORLD (identical text in every cell; 4 entities, 2 described properties each)
     A = P+ Q+     target
     B = P- Q+
     C = P+ Q-
     D = P+ Q-
   description = "the P Q N"

   R axis — change only which entities are live (no world text changes)
     live {A,B,C} :  P restricts        Q restricts
     live {A,C,D} :  P does NOT restrict Q restricts        <- Q's role is held constant

   E axis — change only the matrix verb, inheriting D&R's adjective-verb pairings
     V+ : the event P bears on       (fed the hungry rabbit)
     V- : the event P does not       (tickled the hungry rabbit)

   readout R : ReferenceMargin(P), forced choice over the live entities, and its P-omission cost
   readout E : ExplanationSupport(P) = length-normalised log P of a FIXED continuation,
               "Because the rabbit was hungry.", identical across every condition,
               plus the same with P's contrasting value as a baseline
   readout S : modifier-span surprisal, the B0 measure carried into the crossed worlds
```

B1 assumes no alternative cause. The only causal gold is D&R's: `hungry` bears on `fed` and not on
`tickled`. Scoring a fixed continuation rather than a forced choice also removes option-order bias
and lets the readout run unchanged on base models.

Three structural hazards, three structural fixes.

**(a) `R-E-` must not be the odd cell.** The critical NP always carries two true modifiers; we study
only `P`. When `P` is `R-E-`, its sibling `Q` carries the referential load, so the utterance is never
odd — `P` is merely over-informative. This cell is also the one D&R's 31 participants read without
difficulty (slowest, not broken), which is a stronger guarantee than any check we could run.

**(b) `Q`'s role must not mirror `P`'s.** If `Q` took over exactly when `P` gave up, the design would
encode `P wins vs Q wins` and any later "competition" finding would be built in rather than
discovered. Fix: **`Q` restricts in both R conditions.** With a fixed 4-entity world and a 3-entity
live set this is exact and changes no world text:

```text
live {A,B,C}:  drop P -> {A,B}   ambiguous  => P restricts
               drop Q -> {A,C}   ambiguous  => Q restricts
live {A,C,D}:  drop P -> {A}     unique     => P does not restrict
               drop Q -> {A,C,D} ambiguous  => Q restricts
```

Strictly better than changing entity facts between conditions: `R+` and `R-` prompts stay
byte-identical except for the clause naming the live entities, the property that made S0
interpretable.

**(c) The explanation readout must not smuggle in a cause we invented.** A forced choice needs a
defined competitor in both cells, and an authored background fact playing that role would have made
`Z bears on the E- event` an experimenter-intended gold requiring its own human norming. Fix: drop
the competitor. Score a **fixed continuation** — the same `P`-based explanation string under both
events — so the measured span is identical and the only causal claim in play is D&R's already-normed
one. The contrasting-value continuation is generated mechanically from the item table and separates
`P`-specific support from the `+sem` verb simply making explanations more likely.

### B2 — mechanism

Cross-classification (does the R direction classify E? — the S1 uniqueness statistic reused
verbatim), the causal double dissociation using the frozen S3 edit
`h' = h + alpha * (mu_opposite - h . d) * d` with property truth preserved, and branch-point
localisation across positions from the modifier token through the NP boundary to the wrap-up region.

## 3. The behavioural object: a functional-selectivity matrix

Not "the claims live in the off-diagonal" — under the orthogonal outcome the important off-diagonals
are two **nulls**, which cannot be the claim by themselves. The headline statistical object is the
structure of the whole matrix:

```text
                    Reference consequence   Explanation consequence
   R manipulation           dRR                      dRE
   E manipulation           dER                      dEE
```

Known denominators (predictable in advance, and in the human data already): `dRR > 0`, `dEE > 0`.

| structure | signature | reading |
|---|---|---|
| **orthogonal routing** | `dRR`, `dEE` large; `dRE`, `dER` ~ 0 | two independent functional computations |
| **generic relevance** | all four positive | one undifferentiated "this modifier matters" signal |
| **competition** | a directed negative cross-effect, e.g. `E+` raises explanation uptake while suppressing referential use | functions contend for the same content |

## 4. Claim ladder

| # | claim | evidence | status |
|---|---|---|---|
| gate | D&R's two main effects and window asymmetry reproduce as LM surprisal | **B0** | capability, one figure |
| **C1** | Descriptive content and referential function are separable: same lexicon, same truth, different function | existing **S1** (restriction ⊥ uniqueness, AUC .997-1.000, transfer .867-.929) + **S3** (causal specificity 4/4, property truth preserved) | **done, reused** |
| **C2** | Reference and explanation are distinct functions of the same content — which structure the selectivity matrix has | **B1** | to run |
| **C3** | The model carries separable internal functional states, not one relevance signal | cross-classification | to run |
| **C4** | **Headline.** The model routes the same content into distinct downstream computations by function | causal double dissociation | to run |
| **C5** | Where does functional routing branch? | see below | to run |

**C5 — branch-point localisation, not a pass/fail gate.** Requiring both functions to be independently
editable at the same token would discard a more interesting architecture. Three normal outcomes:

- **A. local multiplexing** — both functions independently editable at the modifier/NP state. Strongest.
- **B. shared-then-branch** — shared content early, functions separating at a later locus. Arguably
  *more* routing-shaped than A, and it is what D&R's human window asymmetry would predict.
- **C. entangled until output** — dissociation only at behaviour. Weaker; decide then whether to continue.

## 5. What the outcomes do to the story

Every branch has an ACL-scale narrative. None regresses to a restatement of S0.

| B1 outcome | headline becomes |
|---|---|
| **Orthogonal** | *LLMs separate what content means from what it is for, and route it accordingly* — C1→C5 as written |
| **Generic relevance** | *LLMs do not factor discourse function: one relevance signal governs both.* Then derive the failure it predicts — content made explanatory should wrongly gain referential pull — and test it directly. Behaviour→mechanism→new falsifiable prediction→confirmation is the ICML-2026 entity-tracking shape and is a strong paper |
| **Competition** | *Discourse functions contend for the same content.* **S7 moves into the main text**: its 4/4 result that two modifiers are coded against each other is the same phenomenon on a second axis. Strongest of the three |
| Behaviour dissociates, internal states do not | *behaviourally dissociable, internally entangled*; push causal via cue-patching (patch the live-entity clause vs the verb phrase) to localise where the paths diverge |
| B0 itself does not replicate | a real result about LM/human divergence on a published effect, and a reason to run B1 anyway, since B1's readouts are behavioural rather than surprisal-based |

**Floor.** If B and A both fail, the submittable paper is the current 041 (content vs referential
role, uniqueness dissociation, causal specificity, graded relative coding). That floor is not
improved by more models or a scaling series, so neither will be run.

## 6. Pilot A (backup)

Not four constructions at once. A structure ladder, and a **new** mechanistic site, because the S3
intervention site is the adjective token and there is no corresponding token across constructions.

```text
A1   the red cup              <->  the cup that is red
A2   the cup beside the plate <->  the cup that is beside the plate
A3   (only if A1-A2 transfer)      PP / participial
```

Representation site moves to the **NP-completion boundary**. Cheap prerequisite, no new stimuli:
confirm the referential role is present at the NP boundary in the existing S0/S1 worlds first.

## 7. Disposition of existing results

| result | disposition |
|---|---|
| S0 | introduction / denominator; never a claim |
| S1 | **C1**, main text; its cross-classification statistic is reused for C3 |
| S3 | **C1** causal half, main text; its edit is reused verbatim for C4 |
| S4 | superseded as the natural-language window by **B0**; the metalinguistic null is one sentence motivating why B0 uses surprisal and B1 uses world-directed forced choice |
| S6 scaling | dropped |
| S7 | **undecided by design** — main text only if the competition branch fires; otherwise appendix |
| S8 | dropped (negative, and a defensive experiment in origin) |

## 8. Item validity without model-based selection

**No model of any kind is used to select items, and no analysis family is spent on screening.**
The full four-family panel — Qwen3-8B, Llama-3.1-8B, Gemma-3-12B, Mistral-Small-24B — stays untouched
until the item set is frozen, because cross-family generality of the R/E organisation is a selling
point of the paper and a two-family panel would not carry it.

- **Structural validity is certified deterministically, in code**: 4-entity world well-formed; live
  set of the specified shape; the full description uniquely satisfied in every live set; `drop P` and
  `drop Q` set cardinalities exactly as the R condition requires; `Z` true of the target, stated, and
  absent from the referring description and from the referential competitor set; matched background
  facts present for non-targets; lexical/positional counterbalancing complete.
- **Lexical and event-property plausibility is inherited, not judged by us**: the twelve
  adjective-verb pairings come from D&R's human-normed materials, where the `+sem`/`-sem` contrast is
  already validated against 31 readers, and where verb frequency was controlled within each quartet
  to within 1.2 Zipf (SUBTLEX-UK). Where B1 needs more items than twelve, new pairings are normed
  independently rather than screened by a model.
- **If a smoke test is ever needed** it uses auxiliary families excluded from all confirmatory
  analyses, and its criteria are restricted to task validity — does the model parse the format, is
  the target recoverable, is the readout off floor/ceiling. It may never depend on the size or sign
  of the predicted R/E effect; outcome-conditioned selection is outcome-conditioned selection
  whichever model performs it.

Paper text: *Critical items were frozen before any evaluation on the four preregistered model
families. Structural validity was certified deterministically; adjective-verb plausibility was
inherited from previously normed human materials. Any model-based screening used auxiliary families
excluded from all confirmatory analyses, with criteria restricted to task validity rather than the
predicted experimental effect.*

## 9. Scope discipline

Calibrated against the venues targeted (measured 2026-09-04): EMNLP 2025 Outstanding filler-gap uses
pythia 1.4/2.8/6.9B; ACL 2025 Outstanding *Llama See, Llama Do* uses four Llama checkpoints with the
mechanism on one; NAACL 2025 *Racing Thoughts* is primarily one Gemma model. 041 already has five
families and five scales — **over-covered**. No models will be added, and the scaling series will not
be extended.
