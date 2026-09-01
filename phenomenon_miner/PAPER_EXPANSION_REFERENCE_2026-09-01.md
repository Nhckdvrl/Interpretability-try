# Evidence-Based Paper Expansion Reference — 2026-09-01

Purpose: after a natural phenomenon / latent object survives topic selection, expand it toward ACL / EMNLP Main scale **by copying evidence patterns from strong papers rather than inventing elaborate mechanisms in advance**.

This is not a new gate. The scientific object stays primary.

## 1. ACL 2025 Outstanding — Llama See, Llama Do

Paper: `Llama See, Llama Do: A Mechanistic Perspective on Contextual Entrainment and Distraction in LLMs`.

Observed expansion pattern:

1. establish a novel phenomenon across many models and prompt settings;
2. show it persists even for random tokens, isolating a non-semantic core;
3. test semantic modulation (e.g. factual vs counterfactual context);
4. propose a mechanistic object (`entrainment heads`);
5. locate heads with a dedicated discovery method;
6. causally turn them off and show the phenomenon attenuates;
7. connect the mechanism to mitigation of distraction.

Lesson:

> A Route-C paper grows by broad characterization + causal localization + functional consequence/mitigation, not by adding theory jargon before the phenomenon is secure.

Source: ACL 2025 Outstanding, https://aclanthology.org/2025.acl-long.791/

## 2. NAACL 2025 — Racing Thoughts

Paper: `Racing Thoughts: Explaining Contextualization Errors in Large Language Models`.

Observed expansion pattern:

1. start from a recurring contextualization failure;
2. formulate one algorithmic hypothesis (race conditions / dependency timing);
3. derive mechanistic predictions;
4. provide both correlational and causal evidence;
5. use the hypothesis to motivate inference-time interventions that reduce the failure.

Lesson:

> One strong mechanistic hypothesis plus causal evidence and a consequence can be enough; no need for three prewritten architectures.

Source: https://aclanthology.org/2025.naacl-long.155/

## 3. ACL 2026 — Do LLMs Know Tool Irrelevance?

Observed expansion pattern:

1. identify a natural behavioral flaw: structural parameter alignment can override semantic irrelevance;
2. construct data that **decouples the two natural factors**;
3. establish broad behavioral impact;
4. identify two competing pathways (semantic checking vs structural matching);
5. show their relative strength explains invocation decisions;
6. rebalance the pathways;
7. verify mitigation without degrading generic tool-use capability.

Lesson:

> The most convincing causal story often includes a double dissociation, a decision-relevant internal competition, and a specificity control showing the intervention does not simply break the model.

Source: https://aclanthology.org/2026.acl-long.1473/

## 4. EMNLP 2025 Outstanding — Causal Interventions Reveal Shared Structure Across English Filler-Gap Constructions

Observed expansion pattern:

1. begin from an external linguistic theory about shared structure;
2. use Distributed Interchange Interventions to test whether causal internal representations transfer across constructions;
3. establish abstraction/shared structure rather than construction-specific decodability;
4. examine variation and discover previously overlooked factors involving frequency, filler type, and surrounding context;
5. use internal LM evidence to feed back into linguistic theory.

Lesson:

> Cross-context / cross-construction transfer is powerful evidence that a latent object is abstract and reusable. Mechanistic analysis can also generate new externally meaningful moderators, but only after the core object is established.

Source: https://aclanthology.org/2025.emnlp-main.1271/

## 5. ACL 2026 — Cell-Based Representation of Relational Binding

Observed expansion pattern:

1. decode a low-dimensional binding subspace;
2. characterize its geometry (entity × relation grid/cells);
3. test cross-context translation/transfer;
4. causally patch the subspace and systematically change predictions;
5. perturb the subspace and show performance degrades.

Lesson:

> `decodable` becomes paper-scale when accompanied by geometric organization, generalization/transfer, and causal use.

Source: https://aclanthology.org/2026.acl-long.2194/

## 6. ICML 2026 — Do Language Models Track Entities Across State Changes?

This paper is especially relevant to 040.

Observed expansion loop:

```text
behavioral evaluation
→ mechanistic hypothesis
→ operation-specific internal analysis
→ mechanism predicts a failure mode missing from the original evaluation
→ targeted behavioral test confirms it
→ mechanistic intervention partially fixes it
```

Key example: the model uses a fragile global suppression tag for REMOVE. Mechanistic analysis predicts failures when same-label objects appear in multiple boxes; targeted behavior confirms the prediction; nullifying the tag partially repairs the issue.

Lesson:

> A strong interpretability paper can be a closed scientific loop: behavior informs mechanism, and mechanism produces a new falsifiable behavioral prediction. This is stronger than `probe + patching` alone.

Source: https://arxiv.org/abs/2605.30233

---

# What this implies for 040

Frozen headline remains:

> Does a modern LLM represent and causally use **numerical identity** — being literally the same individual — separately from qualitative/type sameness?

Do **not** pre-register a long speculative circuit story. Instead, the paper-strengthening ladder, conditional on earlier stages succeeding, should follow reference-backed patterns:

## Stage 1 — phenomenon / object characterization

- same individual despite substantial qualitative/state change;
- different individual despite same type / near-identical properties;
- deterministic scoring, no LLM judge;
- replicate across primary Llama/Qwen families that pass S0.

## Stage 2 — abstraction / transfer

Following filler-gap and CBR examples, test whether the identity state transfers across:

- held-out lexical/surface cue family;
- held-out object/event domain;
- independent sameness formulation/window.

The purpose is to distinguish an abstract identity object from `the`/`another` or one event template.

## Stage 3 — causal functional specificity

Following tool-irrelevance / CBR patterns:

- intervene on identity state;
- measure token-specific history transfer;
- require preserved shared type/category knowledge;
- compare with lexical cue, recency, semantic similarity and generic binding/coreference controls.

This is the key `representation is used, not merely readable` step.

## Stage 4 — mechanism-derived new failure prediction

Only if Stage 3 reveals a stable mechanism, follow the ICML 2026 behavior↔mechanism loop:

1. derive a new failure case from the discovered identity mechanism;
2. construct the smallest targeted behavioral test needed to falsify that prediction;
3. confirm or reject it.

Examples must be derived from the observed mechanism, not chosen now to force a story.

Potential categories to inspect **only after mechanism evidence exists** include same-label duplicates, identity under large state transformation, and misleading qualitative similarity.

## Stage 5 — optional intervention / mitigation

Only if a real failure mode is predicted and verified, test whether a targeted intervention improves identity-sensitive inference while preserving generic entity tracking/type knowledge.

Mitigation is strengthening evidence, not required to define the topic.

## Stage 6 — architecture generalization

After primary AR-Transformer evidence is secure, optional architecture comparison may include:

- diffusion LM (LLaDA/Dream-family);
- linear/recurrent-like model (Mamba/RWKV-family).

The purpose is to ask whether numerical identity is an architecture-general computational solution or instantiated differently. Architecture comparison cannot rescue a failed primary identity claim.

---

# One-line paper-building rule

> **Phenomenon → abstraction/generalization → causal use → mechanism-derived prediction → behavioral confirmation → optional mitigation/architecture generalization. Stop at the last stage actually supported by evidence; do not invent downstream stages before the mechanism earns them.**
