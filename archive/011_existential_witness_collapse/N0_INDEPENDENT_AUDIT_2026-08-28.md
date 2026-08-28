# 006 Independent N0 Audit — 2026-08-28

Status: `N0-PASS`

Auditor: `GPT-5.6 Sol (fresh adversarial audit role)`
Candidate: `Existential Witness Collapse`

## One-sentence claim

A model can correctly represent that two independently introduced existential witnesses are not known to be identical, yet still operationally reuse them as one joint witness in a downstream action that requires the same entity to satisfy both properties.

## Exact operator

```text
exists x: P(x)
exists y: Q(y)

recognition:
  P witness exists
  Q witness exists
  same witness is not established
  distinct witnesses are not established

downstream:
  action requires one entity satisfying P and Q
  model nevertheless chooses the joint-witness/collapse action
```

This is not ordinary quantifier accuracy. The target phenotype is `representation-correct -> illegal witness fusion`.

## Search passes

Fresh searches covered:

1. exact task/manipulation: existential witness identity, same-witness reasoning, existential conjunction, anonymous witness fusion;
2. ordinary-language anomaly: two people/resources each satisfy one condition but a system acts as though one satisfies both;
3. mother phenomenon: entity binding, entity resolution, coreference, variable binding, discourse referents, quantifier scope;
4. downstream/action setting: tool-agent entity binding, clarification under unresolved identity, planning/resource composition.

The audit refreshed 2024–2026 ACL/arXiv work and followed the strongest neighbors into their task definitions and experimental sections.

## Strongest neighbors

### 1. Entity Binding Failures in Tool-Augmented Agents (2026)

https://arxiv.org/abs/2606.30531

This is the strongest mother-level neighbor. It explicitly separates correct action/tool selection from wrong external-entity binding, and treats true ambiguity as requiring clarification/deferral rather than concrete action.

Why it does **not** absorb 006:

- its ambiguity unit is a natural-language mention with multiple candidate external entities;
- it studies choosing the wrong target entity, not fusing two independent existential witnesses into one joint witness;
- action-oriented baselines are evaluated under direct-execution policies and are not separately gated on a prior correct representation that identity is unresolved;
- there is no matched `same_explicit / distinct_explicit / unknown` identity-world operator;
- there is no requirement that the model first demonstrate `same not established` **and** `distinct not established`, then violate that representation downstream.

Therefore it occupies the broad `entity binding under ambiguity -> unsafe action` mother area, but not the exact `two existential referents -> illegal join after correct identity representation` phenotype.

### 2. Meaning Beyond Truth Conditions: Evaluating Discourse Level Understanding via Anaphora Accessibility (ACL 2025)

https://aclanthology.org/2025.acl-long.432/

This work tests discourse-level referent accessibility under dynamic-semantic manipulations. It is highly relevant to whether existential discourse referents are represented and accessible.

It does not test consequential reuse of two independent existential witnesses as one shared witness after an explicit identity-underdetermination gate.

### 3. Entity Binding Failures in Speech LLM Reasoning (2026)

https://arxiv.org/abs/2606.04474

This diagnoses failures to preserve entity-property associations in speech-to-text reasoning and shows recovery with explicit entity-aware CoT.

It is a modality-specific property-binding failure, not an anonymous-witness co-reference fusion operator and not a `knows-but-does-not-use` identity dissociation.

### 4. Semantic Capacity in Language Learners and LLMs: A Case Study of Quantifier Scope (LREC 2026)

https://aclanthology.org/people/yan-cong/

This occupies quantifier-scope interpretation. Scope competence/failure alone does not subsume 006 because 006 gates the relevant existential facts and then tests a downstream identity join.

## Mother-inclusion attack

The hardest compression is:

> 006 is just another entity-binding-under-ambiguity failure.

That compression is too broad for the registered claim. Existing entity-binding work asks which candidate entity a mention denotes. 006 instead has no uniquely intended hidden entity in the model-visible record: both the same-witness and distinct-witness worlds are logically live. The forbidden operation is not selecting the wrong candidate; it is collapsing two independent existential introductions into one witness without evidence, *after* correctly stating that identity is unresolved.

A second compression is:

> 006 is just quantifier reasoning.

That also fails because pure quantifier errors are excluded from the denominator. A case counts only after the model passes both existential-existence probes and both identity-underdetermination probes plus explicit same/distinct downstream controls.

## Why not a rename

The decisive contrast is the downstream joint-witness operator:

```text
identity-unknown record
vs
same-explicit record
vs
distinct-explicit record
```

with the model required to:

- preserve both identity worlds in recognition;
- collapse only in the explicit-same control;
- preserve in the explicit-distinct control;
- then be tested on an operational action in the unknown world.

No located paper implements that full dissociation.

## Hard kill retained for N1

Kill/route if smoke reveals that the observed destination is actually:

- generic action under ambiguity rather than joint-witness fusion;
- ordinary entity-resolution guessing;
- quantifier parsing failure;
- source-memory recall;
- wording/answer-order artifact;
- or if a refreshed search finds a paper with the full matched identity-world + downstream illegal-join signature.

## Independence note

This was rerun from scratch as a fresh adversarial audit and did not inherit the proposer-side survivor verdict as evidence. The auditor role is recorded explicitly because repository governance requires a separate N0 sign-off.

## Verdict

`PASS`

No exact or mother-complete collision was found as of 2026-08-28. The closest work occupies broader entity-binding and discourse-reference mothers but does not contain the registered component-correct existential-witness fusion operator.
