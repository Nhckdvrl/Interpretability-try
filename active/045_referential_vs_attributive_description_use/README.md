# 045 — Do We Follow the Person the Speaker Means, or Whoever Fits the Description?

Status: **STRICT-PASS-REGISTER / GPU AUTHORIZED**  
Date: 2026-09-01  
Route: **B/C — classic reference distinction + same-surface causal object**  
Protocol: `FINDING_RULES.md` v2.1 + `STRICT_EXTENSION_GATE_2026-09-01.md`

## A. Frozen natural question

> **When someone uses a description like “the man drinking a martini”, does an LLM know whether the speaker is talking about a particular person they already have in mind, or instead about whoever actually fits the description?**

Classic Donnellan distinction:

- **REFERENTIAL use** — the speaker has a particular target independently in mind and uses the description as a tool for directing attention to that target;
- **ATTRIBUTIVE use** — there is no independently selected target; the speaker intends to say something about whoever/whatever satisfies the description.

The same words can be used in both ways. The scientific object is therefore **reference mode / description essentiality**, not the lexical form of the definite description.

## B. Why this is a real scientific object

Donnellan's classic contrast keeps the description essentially identical while changing the discourse situation.

For `the man drinking a martini`:

- referential context: the speaker is looking at one particular man and uses the phrase to call attention to him;
- attributive context: the speaker merely knows that exactly one man at the party is drinking a martini and asks about whoever that is.

Likewise, `Smith's murderer is insane` can be used:

- referentially about a particular suspect already under discussion;
- attributively about whoever actually committed the murder.

The distinction remains actively discussed in philosophy of language. A 2026 analysis explicitly characterizes the referential use as expressing thought about a particular target independently of whether that target fits the descriptive content, while attributive use lacks such an independently selected target.

## C. Human/experimental anchors

### C1 — Ackerman 1979

Children and college adults were presented with short paragraphs that established referential versus attributive contexts before a definite description. Both children and adults interpreted the descriptions context-sensitively and inferred the speaker's intent.

This establishes that the distinction is behaviorally recoverable from discourse context rather than being only a philosopher's notation.

### C2 — Rostworowski & Pietrulewicz 2018/2019 misdescription experiment

This open experimental study tested ordinary speakers' judgments when a description is false of the contextually targeted object.

It crossed referential/attributive use with misdescription conditions and found systematic tolerance/partial truth intuitions. The paper includes the complete vignettes in its appendix.

Important limitation: each first-study condition is represented by only one vignette. Therefore this paper is a **natural human anchor**, not the sole scale substrate for 045.

### C3 — deterministic theory-licensed causal microscope

Because the referential/attributive distinction is defined independently, we can construct many matched discourse worlds with model-independent gold while holding the critical description constant.

No LLM judge is needed.

## D. Strongest-neighbor audit — N0 / N1 / N2

### D1 — definite-description semantics is obviously crowded

Prior work already owns:

- uniqueness/familiarity theories of definiteness;
- reference resolution;
- discourse salience and speaker intent;
- misdescription behavior in humans;
- philosophical analysis of speaker reference vs semantic reference;
- broad philosophical questions about whether language-model words refer.

045 may not claim novelty from any of these individually.

### D2 — no direct neural/LLM exact-object ownership found

Targeted searches across:

- `referential vs attributive` + BERT/GPT/LLM;
- `Donnellan` + language model;
- `speaker reference vs semantic reference` + LLM;
- `misdescription` + LLM;
- `speaker intent` + definite description + neural model;

found no work that:

1. keeps the same description while context switches referential vs attributive use;
2. identifies an abstract internal use-mode state in a pretrained neural LM;
3. causally changes whether downstream reference follows the speaker-target or the descriptive satisfier;
4. preserves the raw speaker-target and description-truth facts.

The 2024 Computational Linguistics paper `Do Language Models' Words Refer?` is a philosophical account of reference for LMs, not this empirical causal factorization.

### D3 — exact N2

> **Modern LLMs represent and causally use a context-conditioned `DescriptionUseMode` that determines whether a definite description follows an independently selected speaker-target or the object satisfying its descriptive content, while preserving both raw facts.**

If the result reduces to generic theory-of-mind, salience, coreference, or `does the description fit`, kill N2.

## E. Strict Extension Gate

### Lock A — same-surface role switch: PASS

The critical description is identical across paired contexts.

Canonical paired structure:

```text
critical phrase: "the man drinking a martini"

REFERENTIAL context:
  speaker is attending to a specific man R
  speaker uses the description to call attention to R

ATTRIBUTIVE context:
  speaker has no preselected man in mind
  speaker intends whoever uniquely satisfies MARTINI-DRINKER
```

The role switch is created by discourse intention/context, not lexical form.

### Lock B — cross-setting abstraction: PASS

Mandatory transfer across at least:

1. perceptual/attention-style target establishment;
2. prior-discourse acquaintance / named-suspect target establishment;
3. held-out description families (`the F`, relational descriptions, role descriptions);
4. held-out entity/domain families;
5. contexts with and without a competing real satisfier.

A state learned only from words like `look`, `suspect`, or one vignette family does not count.

### Lock C — TWO independent consequences: PASS

#### Consequence 1 — MisdescriptionTargetMargin

When the speaker-target `R` does **not** satisfy `F`, while another object `S` does:

```text
referential use:
  downstream reference should preferentially follow R

attributive use:
  downstream reference should preferentially follow S / whoever satisfies F
```

This is the decisive target-vs-satisfier crossover.

#### Consequence 2 — DescriptionEssentialityLogit

Change the descriptive content while preserving the independently selected speaker-target.

Prediction:

```text
referential use:
  target identity is relatively robust to replacing F with another audience-usable description of the same target

attributive use:
  changing the descriptive condition changes which object is licensed as the referent
```

The same internal `DescriptionUseMode` must causally affect both consequences.

## F. Deterministic substrate

### F1 — matched finite discourse worlds

Create worlds with two or three entities and explicit, auditable facts.

Example:

```text
R = Alex
  speaker is visibly attending to Alex
  Alex holds a water glass
  Alex is wearing a red jacket

S = Ben
  Ben is actually drinking a martini
  Ben is wearing a blue jacket

critical description = "the man drinking a martini"
```

REFERENTIAL condition:
- context establishes that the speaker is pointing/attending to Alex and uses the critical description to get the hearer to track Alex.

ATTRIBUTIVE condition:
- context removes any preselected target and establishes only the question about whoever is drinking a martini.

World facts, entity properties and critical description can remain identical; only the speaker-use context changes.

### F2 — model-independent gold

For every item we know separately:

```text
SpeakerTarget
DescriptionSatisfierSet
UseMode
```

These are explicit construction variables, not LLM labels.

### F3 — natural validation

Use published Donnellan/Ackerman/misdescription materials as naturalistic validation after the controlled microscope reproduces the frozen distinction.

## G. Frozen S0

Primary models:

- `meta-llama/Llama-3.1-8B-Instruct`
- `Qwen/Qwen3-8B`

### G1 — raw-fact denominators

Before any use-mode claim, require intact:

```text
SpeakerTargetFactLogit
  # which entity the discourse explicitly establishes as the speaker's independently attended/intended target

DescriptionTruthLogit
  # which entity actually satisfies F

EntityFactLogit
  # basic properties of R/S
```

### G2 — behavioral crossover

Define:

```text
TargetVsSatisfierMargin =
  log P(reference = SpeakerTarget)
  - log P(reference = DescriptionSatisfier)
```

On matched conflict worlds:

```text
REFERENTIAL: margin shifts toward SpeakerTarget
ATTRIBUTIVE: margin shifts toward DescriptionSatisfier
```

The model need not mirror any philosophical theory of sentence-level semantic reference; the behavioral readout asks which referent its downstream computation follows under the two contextually defined uses.

### G3 — second consequence

Test `DescriptionEssentialityLogit` on held-out items by replacing the descriptive route while holding speaker-target facts fixed.

### G4 — shortcut controls

Balance:

- target salience;
- entity order;
- names;
- speaker-target recency;
- description length/frequency;
- words such as `look`, `point`, `suspect`, `whoever`;
- satisfier position;
- truth of the predicated downstream property.

## H. Frozen causal-use contract

### H1 — estimate `DescriptionUseMode`

Estimate REFERENTIAL↔ATTRIBUTIVE state/subspace from balanced contexts with:

- identical critical descriptions crossed with use mode;
- speaker-target and satisfier identity balanced;
- held-out context-establishment families;
- held-out descriptions/entities.

No best-layer selection on final tests.

### H2 — first causal consequence

On held-out conflict worlds:

```text
steer toward REFERENTIAL
→ increase TargetVsSatisfierMargin toward SpeakerTarget

steer toward ATTRIBUTIVE
→ shift toward DescriptionSatisfier
```

while preserving:

```text
SpeakerTargetFactLogit
DescriptionTruthLogit
EntityFactLogit
```

If the intervention merely makes the model forget who the speaker was looking at, or who actually satisfies F, the claim fails.

### H3 — independent second consequence

The same intervention must shift `DescriptionEssentialityLogit` in the predicted direction on held-out description-substitution examples.

No replacement diagnostic may be chosen after seeing results.

### H4 — mandatory controls

- generic speaker-intention / ToM direction;
- generic salience direction;
- coreference/entity-binding direction;
- description-truth direction;
- speaker-target-fact direction;
- random/shuffled subspaces;
- lexical context-cue directions.

## I. Story invariance

### Result A — abstract use mode

The model knows both raw facts and maintains a reusable state controlling whether reference follows speaker-target or descriptive satisfaction.

### Result B — referential-target dominance

Models understand the description facts but default to the salient/intended target even in attributive contexts; this identifies a systematic speaker-target bias.

### Result C — descriptive dominance

Models understand speaker-target facts but reference remains tied to who satisfies the description, even in clear referential-use contexts.

### Result D — superficial context heuristic

Any apparent use-mode signal reduces to salience, lexical cues or generic ToM and fails held-out transfer/specificity.

All outcomes answer the same frozen question.

## J. Hard kills

1. Direct neural/LLM referential-vs-attributive causal factorization found -> `KILL-NOVELTY`.
2. Result is generic ToM / speaker intent only -> `KILL-N2`.
3. Result is generic coreference/salience -> `KILL-N2`.
4. Same critical description does not switch role across contexts -> `KILL-IDENTIFIABILITY`.
5. Intervention damages `SpeakerTargetFactLogit` -> `KILL-SPECIFICITY`.
6. Intervention damages `DescriptionTruthLogit` -> `KILL-SPECIFICITY`.
7. Only misdescription behavior works but DescriptionEssentiality does not -> `KILL-UNIFIED-OBJECT` under Lock C.
8. No cross-context/description-family transfer -> no abstract state claim.
9. Probe/best-layer only -> `KILL-SCALE`.
10. Failed S0 cannot be rescued through prompt/subset search.

## K. Relationship to active topics

### vs 042 uniqueness vs familiarity

042 asks **what licenses a definite description as definite** when uniqueness and strong familiarity conflict.

045 assumes a definite description is being used and asks **what determines its referential mode**: an independently intended target or whoever satisfies its descriptive content.

### vs 038 unresolved reference

038 asks the representational format of a reference that remains unresolved.

045 uses contexts in which the relevant speaker-target and/or satisfier facts are explicit and asks which source the model follows. It is not an ambiguity-representation paper.

### vs 040 numerical identity

040 asks whether two mentions concern the same individual despite qualitative similarity/change.

045 keeps individual identities explicit and manipulates description use.

## L. Strict verdict

```yaml
base_v2_1: PASS
natural_object: PASS
human_behavioral_anchor: PASS
model_independent_controlled_gold: PASS
old_neural_exact_object_ownership: CLEAR_IN_TARGETED_SEARCH
recent_LLM_exact_object_ownership: CLEAR_IN_TARGETED_SEARCH
Lock_A_same_surface_role_switch: PASS
Lock_B_cross_setting_abstraction: PASS
Lock_C_two_exact_consequences:
  - MisdescriptionTargetMargin
  - DescriptionEssentialityLogit
  status: PASS
specificity_denominators:
  - SpeakerTargetFactLogit
  - DescriptionTruthLogit
  - EntityFactLogit
central_confound:
  - salience
  - generic_ToM
  - coreference
identifiable_with_hard_kills: true
story_invariance: PASS
behavior_lottery: false
verdict: STRICT-PASS-REGISTER
GPU_AUTHORIZED: true
```

## One-line freeze

> **045 asks whether an LLM knows when a definite description is merely a tool for picking out a person the speaker already has in mind versus when the description itself determines whoever is being talked about. Same-surface context switches, target-vs-satisfier crossover, description-essentiality, and preservation of both speaker-target and description-truth facts are mandatory.**