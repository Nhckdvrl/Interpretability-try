# 045 Hard Re-Audit — 2026-09-01

Verdict: **STRICT-PASS-REGISTER / GPU AUTHORIZED — HARD RE-AUDIT PASSED**

## Frozen question

> When a speaker uses the same definite description, does the model know whether reference should follow a particular person the speaker independently has in mind or instead whoever actually satisfies the description?

Frozen functional object:

> **DescriptionUseMode: REFERENTIAL vs ATTRIBUTIVE use of a definite description.**

This is deliberately theory-neutral about whether Donnellan's contrast is a semantic ambiguity, a pragmatic distinction, or a speaker-reference phenomenon. 045 does **not** claim to settle that philosophical issue. It asks whether modern LMs implement a reusable context-conditioned functional state with the behavioral consequences associated with the distinction.

## Why this audit was needed

The surrounding reference space is crowded:

- definite-description semantics;
- coreference/reference resolution;
- discourse salience;
- speaker intention / theory of mind;
- misdescription judgments;
- philosophical work on speaker reference vs semantic reference;
- recent work asking whether LM words refer at all.

A paper that merely shows that LMs use context or speaker intention would therefore fail N2.

## External scientific and behavioral anchors

### Donnellan's classic same-description contrast

The same phrase, e.g. `the man drinking a martini`, can be used:

- **referentially**: the speaker is independently attending to one particular person and uses the description as a tool for directing the hearer to that target;
- **attributively**: the speaker has no independently selected target and intends whoever in fact satisfies the description.

This supplies a genuine same-surface role shift.

### Ackerman 1979

Children and adults interpreted definite descriptions differently after contexts designed to establish referential versus attributive use. This establishes that the distinction is recoverable from ordinary discourse context.

### Rostworowski & Pietrulewicz misdescription experiment

Human judgments under false/misdescribed descriptions provide a natural consequence of the distinction: referential uses can remain target-directed even when the descriptive content fails of that target.

The released/open article includes full vignettes, but the first study has only one vignette per condition. Thus it is a natural anchor and validation source, not the sole scale substrate.

## Strongest computational-neural audit

Targeted searches covered:

```text
referential vs attributive + BERT/GPT/LLM
Donnellan + language model
speaker reference vs semantic reference + LLM
misdescription + language model
speaker intent + definite description + neural model
```

No direct neural/LLM work was found that jointly:

1. keeps the critical description fixed while discourse changes REFERENTIAL vs ATTRIBUTIVE use;
2. identifies a transferable internal use-mode state;
3. causally changes whether downstream reference follows the speaker-target or descriptive satisfier;
4. preserves both underlying raw facts.

The closest modern philosophical work, `Do Language Models' Words Refer?`, asks a broader foundational question about reference for LM tokens/words and does not occupy this empirical causal factorization.

## N0 / N1 / N2 conclusion

### N0

Generic reference behavior, speaker-intent reasoning, and definite descriptions are occupied. The exact same-description use-mode object was not found in neural/LLM work.

### N1

No prior causal intervention was found that edits a REFERENTIAL↔ATTRIBUTIVE state while preserving target and descriptive facts.

### N2

The acceptable contribution is strictly:

> **a reusable context-conditioned DescriptionUseMode state that controls whether reference follows an independently established speaker-target or the descriptive satisfier, with cross-setting transfer and raw-fact preservation.**

If 045 becomes generic ToM, salience, coreference, or description-truth reasoning, kill it.

## Strict-extension locks

### Lock A — same-surface role switch: PASS

Keep the critical definite description identical while changing only the use context.

In conflict worlds:

```text
R = independently established speaker-target
S = actual satisfier of description F
R does not satisfy F
S does satisfy F
```

REFERENTIAL context should make downstream reference relatively target-directed; ATTRIBUTIVE context should make it satisfier-directed.

### Lock B — cross-setting abstraction: PASS

Mandatory held-out transfer across:

- perceptual/attention target establishment;
- prior-discourse acquaintance / suspect-type target establishment;
- lexical description families;
- entity/domain families;
- real-satisfier-present and satisfier-absent cases.

### Lock C — two exact consequences: PASS

No post-hoc metric choice.

1. **MisdescriptionTargetMargin** / `TargetVsSatisfierMargin`
   - whether downstream reference follows independent target R or actual satisfier S when they conflict.

2. **DescriptionEssentialityLogit**
   - whether changing the descriptive content while preserving the independently selected target changes reference.

The same causal state must affect both.

## Deterministic causal microscope

For every constructed item, central gold is explicit:

```text
SpeakerTarget
DescriptionSatisfierSet
DescriptionUseMode
```

World facts and the critical description can be identical across use-mode pairs. Only discourse establishes whether the description is functioning as a target-directing tool or as the condition that determines the referent.

No LLM judge.

## Raw-fact preservation

Before any use-mode claim, require intact:

```text
SpeakerTargetFactLogit
DescriptionTruthLogit
EntityFactLogit
```

A valid intervention must change use-mode-sensitive reference behavior **without** erasing:

- which entity the discourse establishes as the independently intended/attended target;
- which entity actually satisfies the description;
- ordinary entity properties.

This is the central identifiability gate.

## Causal signature

Estimate `DescriptionUseMode` from balanced training contexts with same-description crossings and held-out context families.

On held-out conflict worlds:

```text
steer toward REFERENTIAL
→ increase reference preference for SpeakerTarget

steer toward ATTRIBUTIVE
→ increase reference preference for DescriptionSatisfier
```

The same intervention must also shift `DescriptionEssentialityLogit` in the predicted direction.

Mandatory controls:

- speaker-intention / generic ToM direction;
- salience direction;
- coreference/entity-binding direction;
- description-truth direction;
- speaker-target-fact direction;
- lexical cue directions;
- random/shuffled subspaces.

## Relationship to active topics

### vs 042

042 asks what **licenses definiteness**: uniqueness vs strong discourse familiarity.

045 assumes a definite description is used and asks **which source determines its referent under that use**: independently selected speaker-target vs descriptive satisfaction.

### vs 038

038 asks how genuinely unresolved reference is represented. 045 uses explicit target/satisfier facts and asks which source is followed; it is not an ambiguity-format question.

### vs 040

040 asks numerical identity vs qualitative sameness. 045 keeps identities explicit and manipulates description use.

## Hard kills

1. A direct prior neural/LLM causal Donnellan-style factorization is found -> `KILL-NOVELTY`.
2. Generic speaker-intent/ToM direction explains the effect -> `KILL-N2`.
3. Generic salience/coreference explains the effect -> `KILL-N2`.
4. Same critical description does not switch role in held-out contexts -> `KILL-IDENTIFIABILITY`.
5. Intervention damages `SpeakerTargetFactLogit` -> `KILL-SPECIFICITY`.
6. Intervention damages `DescriptionTruthLogit` -> `KILL-SPECIFICITY`.
7. Only target-vs-satisfier crossover works but `DescriptionEssentialityLogit` does not -> `KILL-UNIFIED-OBJECT`.
8. Cross-context/description-family transfer fails -> no abstract state claim.
9. Probe/best-layer only -> `KILL-SCALE`.
10. Failed frozen S0 cannot be rescued by prompt/subset fishing.

## Final verdict

```yaml
natural_object: PASS
same_surface_role_shift: PASS
human_behavioral_anchor: PASS
model_independent_gold: PASS
N0_object_ownership: PASS_AFTER_TARGETED_SEARCH
N1_causal_occupancy: PASS
N2_delta_width: PASS_FOR_FUNCTIONAL_USE_MODE
Lock_A: PASS
Lock_B: PASS
Lock_C:
  - MisdescriptionTargetMargin
  - DescriptionEssentialityLogit
  status: PASS
specificity_denominators:
  - SpeakerTargetFactLogit
  - DescriptionTruthLogit
  - EntityFactLogit
story_invariance: PASS
PASS_REGISTER: true
GPU_AUTHORIZED: true
```

> **045 remains registered only as a functional description-use-mode paper. It does not claim to resolve the philosophical semantics/pragmatics debate over Donnellan; it tests whether a reusable causal state determines whether model reference follows an independent speaker-target or descriptive satisfaction.**