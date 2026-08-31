# Natural-Question Gate — Hamdi-style Topic Selection

Date: 2026-08-30  
Status: `AUTHORITATIVE P0 GATE; FOLLOWED IMMEDIATELY BY S0`

This file was added after the completed Top-6 audit exposed a systematic failure in topic selection. The main mistake was not that cheap D0 killed many ideas; it was that several ideas were selected because they admitted a clever experimental construction rather than because the underlying scientific question was naturally compelling and likely to exist.

This gate runs before novelty search, builder design, or full model calls. It does
**not** authorize a candidate. Every P0 survivor immediately enters the
type-specific [`SCIENTIFIC_SUBSTRATE_GATE.md`](SCIENTIFIC_SUBSTRATE_GATE.md),
which must complete before N0/N1 or registration.

---

## 1. Core principle

A good interpretability topic should already be interesting before mentioning:

- a dataset;
- a benchmark;
- a probe;
- an SAE;
- a head;
- activation patching;
- a capability gate;
- a matched-control construction.

The research question must survive deleting all of those nouns.

A useful lab standard is:

> **One ordinary example should make the reader immediately understand why the question is interesting.**

Examples of the desired shape:

- "Ask a model to pick a random digit. Why does it strongly prefer some digits if it understands that the request is arbitrary?"
- "A model can tell you many facts about dragons and Hogwarts. Does it separately represent that these entities do not exist in the real world?"

The phenomenon is not created by the measurement protocol. The protocol only reveals or isolates it.

---

## 2. P0 — Natural scientific object

Before any dataset search, write exactly three things:

```yaml
plain_question:
one_example:
why_a_non_specialist_should_care:
```

PASS requires all of the following:

1. The question is understandable without model-internal vocabulary.
2. The example is an ordinary use case or a stable conceptual distinction, not a benchmark-specific corner case.
3. The phenomenon would still make sense if the eventual dataset were replaced.
4. The phenomenon does not require a chain of researcher-invented conditions to define what it is.
5. There is a clear reason to expect the phenomenon or distinction to exist before running a large experiment.

If the question only becomes interesting after explaining a 2×2×2 design, a special gate, or a matched subset, reject it at P0.

---

## 3. P1 — Existence prior

We should stop treating "does this phenomenon exist at all?" as a 50/50 lottery.

A strong topic should normally have at least one of these anchors:

### A. Direct everyday behavioral anchor

The behavior is already obvious in casual interaction or trivial to demonstrate with a handful of prompts.

Example: arbitrary-choice prompts are visibly biased.

### B. Stable external conceptual distinction

The scientific object exists independently of model behavior.

Example: real vs fictional existence, knowledge vs ontology. The distinction
must still pass S0: both variables need independent objective labels and an
observed natural cross-population.

### C. Established mother phenomenon

A strong prior work establishes the broad behavioral object, and the new question is a genuinely natural next distinction rather than a hidden-state localization exercise.

Example: exact-token contextual entrainment naturally raises the question of whether salience transfers across another name for the same entity. For a failure
topic, the target effect must additionally be demonstrated on analyzable open
models before registration.

### Reject

Reject topics whose existence prior is mainly:

- "this benchmark lets us construct the contrast";
- "humans sometimes show a related bias";
- "if we filter to items satisfying five conditions, maybe a residual appears";
- "the mechanism would be interesting if the behavior happened".

---

## 4. P2 — Five-minute / ten-example sanity

Before building a dataset, try the phenomenon in the cheapest faithful form.

The purpose is not statistical evidence. It is to test whether the scientific object is visible at all without elaborate engineering.

PASS shape:

```text
5–20 ordinary examples
→ same qualitative question is visible
→ no special subset search
→ no post-hoc threshold
```

If the phenomenon cannot be expressed faithfully without first building a complex bank, that is a warning sign.

Exceptions are allowed only when the object is inherently population-level, but the burden of proof is high.

---

## 5. P3 — Dataset must be an instrument, not the source of the phenomenon

Ask:

> **Did we choose the dataset because it measures a question we already cared about, or did the dataset teach us what question to ask?**

Good:

```text
natural question
→ choose source that exposes it
→ controls isolate confounds
```

Bad:

```text
dataset has fields X/Y/Z
→ construct a rare subset
→ define the subset behavior as a new phenomenon
```

Controls are allowed to establish causal interpretation. They are not allowed to manufacture the headline scientific object.

---

## 6. P4 — Restriction budget

A topic is suspicious if the headline denominator itself needs many conjunctive restrictions.

Before model calls, separate:

```text
phenomenon-defining conditions
measurement-validity exclusions
analysis controls
moderators / strata
```

Target rule:

- headline phenomenon should normally need **one clean contrast**;
- hard exclusions should only remove invalid measurement;
- capability gates should not redefine the population;
- moderators remain factors;
- matched controls test explanations after the phenomenon is visible.

If three or more arbitrary conditions are needed merely to make the phenomenon describable, default to REJECT.

---

## 7. P5 — Natural mechanistic unfolding

Mechanism comes after the question, but a good question should naturally generate a small number of mechanistic forks.

Good examples:

```text
random-choice bias exists
→ does the model represent "choice mode"?
→ is that representation a switch or a distribution-shaping dial?
```

```text
model knows fictional entities very well yet denies their real-world existence
→ knowledge and ontology may be separable
→ where is ontology represented and is it causal?
```

```text
cross-surface entrainment exists
→ lexical derivation vs learned association vs reference identity
```

Bad:

```text
we found a head / feature
→ invent a behavioral story so the head has a paper
```

---

## 8. Why the completed Top-6 mostly failed this gate

### 015 Clarification Resolution Lag

The phenomenon required a very specific history construction and matched-history residual. Without explaining the protocol, the headline was not independently compelling enough. The matched-history control then removed the effect.

### 016 Mixed-Status Event Attraction

The dataset made same-document factuality pair construction convenient, but "neighbor event status attracts target status" was not an independently established natural phenomenon. Same-status context explained the shift.

### 017 Cross-Modal Resolution Inertia

The desired phenotype depended on sequentializing a particular MUCAR subset and conditioning on text-wrong/simultaneous-correct items. The strongest effect survived when prior-choice identity was masked, so the constructed interpretation-specific story collapsed.

### 019 Abstention Hysteresis

The same-question ablate/restore protocol was elegant, but refusal-specific stickiness was not a high-prior natural phenomenon. The experiment found the opposite: incomplete→complete history facilitated recovery, and neutral history explained most of it.

These are not merely unlucky nulls. They show that elegant factorial designs can seduce topic selection away from natural scientific objects.

---

## 9. Retrospective: why 014 survived and 018 did not

### 014 Alias Entrainment Transfer

The mother phenomenon is already real: contextual entrainment after seeing a token. The next question is immediate and natural: **if another surface form denotes or strongly relates to the same thing, does salience transfer there too?**

The later ASSOC/reference controls became complicated because they separate explanations of a real broad effect; they did not create the broad effect.

### 018 Stock–Flow Correlation Intrusion

The question is natural and the human mother phenomenon is classic, but that is
not an LLM existence substrate. After the bounded semantic-recognition repair,
0/4 open families promoted and the estimable effects were small, null, or
opposite. Under S0-first rules this failure topic would not have been registered.

---

## 10. Mandatory P0 card before S0

Every new topic must first fill this card:

```yaml
P0_natural_question:
  plain_question:
  one_example:
  why_care:
  understandable_without_dataset_or_MI: true|false

P1_existence_prior:
  anchor: everyday_behavior | external_concept | established_mother
  evidence:
  estimated_risk_that_phenomenon_is_absent: low | medium | high

P2_minimal_sanity:
  faithful_without_complex_builder: true|false
  examples_needed:
  expected_visible_signature:

P3_dataset_role:
  question_preexists_dataset: true|false
  replacement_dataset_preserves_question: true|false

P4_restriction_budget:
  phenomenon_defining_conditions: []
  validity_exclusions: []
  controls: []
  arbitrary_conjunctive_restrictions_count:

P5_mechanistic_forks:
  -
  -

verdict: PASS-TO-S0 | REJECT
```

A P0 pass is only permission to run S0. It is not a candidate registration,
novelty claim, data-feasibility assumption, or model-call authorization.

---

## 11. Current scheduling consequence

As of 2026-08-30:

- **014 Alias Entrainment Transfer** — primary paper-development project.
- **018 Stock–Flow Correlation Intrusion** — primary behavioral-redesign project.
- 020–023 are **suspended pending re-audit under this gate**. Existing directories preserve provenance, but no screening call is authorized merely because they were previously registered.

Do not generate another large batch of candidates until the candidate-generation process itself follows this gate.

---

## One-line discipline

> **Do not ask “what clever experiment can we build from this dataset?” Ask “what natural question would still be interesting if the dataset disappeared?”**
