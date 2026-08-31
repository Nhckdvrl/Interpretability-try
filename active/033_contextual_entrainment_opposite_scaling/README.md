# 033 — Why Bigger Models Ignore Lies but Copy Noise

Status: **ACTIVE / PASS-REGISTER / V0 AGGREGATE REPLAY COMPLETE — ITEM DATA NOT RELEASED**

Route: **Hamdi Route B — established scaling anomaly → unasked causal decomposition**  
Canonical registration: [`../../phenomenon_miner/REGISTERED_CONTEXTUAL_ENTRAINMENT_OPPOSITE_SCALING_MECHANISM_2026-08-31.md`](../../phenomenon_miner/REGISTERED_CONTEXTUAL_ENTRAINMENT_OPPOSITE_SCALING_MECHANISM_2026-08-31.md)

## 1. One-sentence question

Why does scaling make LLMs **more resistant to meaningful false context but more susceptible to mechanically copying meaningless context**?

Does scale strengthen one shared copying primitive plus a semantic gate, create two independently scaling circuits, or leave the same upstream entrainment mechanism while changing only late memory/context competition?

## 2. Background and mother lineage

### Behavioral mother

**Better and Worse with Scale: How Contextual Entrainment Diverges with Model Size** (Kukreja et al., Findings of ACL 2026).

The paper measures contextual entrainment on the same basic factual-query object across two open model scale families:

- Cerebras-GPT, from small models to 13B;
- Pythia, from 410M to 12B.

For a factual query with gold token `g` and distractor `d`, it measures the context-induced distractor advantage:

`Delta_d = logit(d | context) - logit(d | no context)`

The headline result is an **opposite-sign scaling law**:

- semantic contexts (`Counterfactual`, `Related`) show decreasing distractor entrainment as models get larger;
- non-semantic contexts (`Random`, `Irrelevant`) show increasing mechanical copying with scale.

The mother also performs no-context capability and distractor-salience controls, so the sign split is not explained by larger models simply knowing the gold answer better or liking the distractor token more at baseline.

Most importantly for us, the mother explicitly says it provides a **behavioral scaling analysis without mechanistic decomposition** and raises as future work whether copying and filtering arise from distinct circuits with different scaling properties.

### Mechanistic predecessor

**Llama See, Llama Do: A Mechanistic Perspective on Contextual Entrainment and Distraction in LLMs** (ACL 2025 Outstanding Paper).

This predecessor already establishes a sparse causal mechanism for generic contextual entrainment:

- differentiable masking identifies **entrainment heads**;
- ablating those heads attenuates the context-induced distractor effect;
- semantic properties modulate entrainment magnitude.

Therefore this project must **not** claim novelty for finding entrainment heads. The new object is why the same entrainment quantity scales in opposite directions depending on whether the context is semantically meaningful.

## 3. Competing causal mechanisms

### H1 — Shared copying writer + scaling semantic gate

A common copying/entrainment writer strengthens with scale in all contexts. Larger models additionally develop a stronger semantic-conflict / filtering pathway that suppresses the writer only when the context is meaningfully related to the query.

Predictions:

- the causal effect of entrainment heads grows with scale even in semantic conditions before filtering;
- large models recruit an additional semantic gate;
- ablating that gate should push Counterfactual/Related behavior toward the positive scaling profile of Random/Irrelevant context.

### H2 — Distinct copying and filtering circuits

Mechanical copying and semantic filtering are implemented by separable circuit families whose strengths scale independently.

Predictions:

- low overlap between non-semantic copying and semantic suppression components;
- double dissociation under ablation;
- copying-circuit strength increases with size while semantic-filter strength independently increases enough to reverse the net semantic effect.

### H3 — Common upstream entrainment, late memory/context competition

Early/middle entrainment is similar across conditions and scale. The sign split appears only late through competition between contextual token support and parametric-memory / answer pathways.

Predictions:

- early causal profiles remain similar;
- semantic/non-semantic divergence appears late;
- late residual/pathway patching can switch semantic behavior without changing earlier copying states.

## 4. Data and artifacts

Primary scientific substrate should be inherited from the ACL 2026 mother and ACL 2025 predecessor, not rebuilt as a new benchmark.

Required frozen artifacts:

- exact factual-query items used for contextual entrainment;
- four context conditions: `Counterfactual`, `Related`, `Random`, `Irrelevant`;
- gold token `g`, distractor token `d`, and no-context baseline for every item;
- mother model size ladders for Pythia and Cerebras-GPT;
- predecessor differentiable-mask / head-ablation recipe.

Primary statistical unit:

> **same factual query + same candidate distractor token + changed context semantics + model scale**

Whenever possible, preserve distractor identity when comparing semantic and non-semantic conditions so token frequency/baseline logit cannot masquerade as a semantic gate.

## 5. Initial model scope

Primary mechanistic ladder: **Pythia**, because the full size ladder is open and architectures are relatively standardized.

Do not start with every size.

Recommended staged design:

1. smallest / middle / largest mother-reported Pythia sizes for pipeline validation;
2. add intermediate sizes once the causal measurement is stable;
3. replicate the sign/mechanism on selected Cerebras-GPT endpoints only after the Pythia result is interpretable.

Cross-scale comparisons must use normalized causal effects. Raw head count is not meaningful across differently sized architectures.

## 6. Initial validation plan

### V0 — Exact mother-metric replay

Goal: establish that our code reproduces the mother scaling object without introducing new evaluation choices.

Steps:

1. Pin the mother/predecessor data/code revisions or reconstruct the released item table exactly.
2. For each item/model/condition compute:
   - `logit(d | context)`;
   - `logit(d | no context)`;
   - `Delta_d`.
3. Reproduce the sign of the scaling trend for:
   - Counterfactual;
   - Related;
   - Random;
   - Irrelevant.
4. Re-run the no-context gold-token capability and distractor-baseline controls.
5. Freeze item IDs and preprocessing before any head discovery.

**Stop condition:** if the sign split cannot be reproduced on the exact mother setup, resolve provenance before MI. Do not substitute accuracy for the logit-shift object.

### V1 — Reproduce generic entrainment heads on a reference size

Goal: validate the ACL 2025 causal recipe, not claim novelty.

Steps:

1. Implement/adapt the predecessor differentiable-mask procedure on one reference Pythia model.
2. Recover a sparse component set whose ablation reduces contextual entrainment.
3. Confirm that random same-count head ablations do not match the effect.
4. Verify the effect on more than one context class.

If generic entrainment localization cannot be reproduced, do not invent an alternative head score solely for this project without auditing why.

### V2 — Scale-conditioned causal profiles

Goal: ask whether the same causal pathway changes strength with size.

For selected Pythia sizes:

1. derive normalized entrainment-head/pathway scores separately for semantic and non-semantic conditions;
2. measure:
   - causal effect size under ablation;
   - layer distribution;
   - cross-scale correspondence where architecture permits;
   - overlap between semantic and non-semantic causal sets;
3. normalize by residual/logit effect scale rather than compare raw head counts.

Key patterns:

- growing shared writer across all conditions supports H1;
- increasingly distinct component sets support H2;
- similar early profiles with late divergence support H3.

### V3 — Semantic-filter difference-in-differences localization

Generic entrainment is already owned. We specifically need a component whose effect is semantic-selective.

For matched items, estimate an intervention effect analogous to:

`[(semantic - no_context) effect] - [(nonsemantic - no_context) effect]`

Steps:

1. hold query and distractor identity fixed when possible;
2. patch/ablate individual components or pathways;
3. localize components that change semantic suppression substantially more than arbitrary copying;
4. test whether this semantic-selective causal effect increases with model size.

This provides a direct candidate **semantic gate** rather than another copying head.

### V4 — Decisive semantic-gate ablation

Core H1/H2 test.

On the largest Pythia model:

1. ablate the semantic-filter candidate while leaving generic entrainment heads intact;
2. measure Counterfactual/Related `Delta_d`;
3. ask whether semantic conditions move toward the Random/Irrelevant positive-copying regime;
4. restore/patch the component and test reversibility;
5. repeat on smaller scales where the gate is predicted to be weaker.

A strong result is not merely an accuracy drop; it is a **selective collapse of the opposite-sign semantic scaling behavior**.

### V5 — Writer ablation and double dissociation

1. ablate generic entrainment writer components;
2. measure whether positive Random/Irrelevant scaling collapses;
3. observe how much semantic entrainment remains;
4. combine writer and gate ablations.

Interpretation:

- writer affects both; gate selectively affects semantic contexts → H1;
- two selective component families → H2;
- neither explains early differences, but late pathway patching does → H3.

### V6 — Late competition test

To test H3:

1. compare early/middle residual contributions across context types;
2. inspect late parametric-memory/context-answer pathways;
3. patch semantic-condition late states toward matched non-semantic states while preserving earlier computation;
4. test whether the sign split can be switched late.

This guards against overinterpreting different head sets as separate circuits when the real effect is late readout competition.

## 7. Fatal controls

- Use the mother `Delta_d` logit-shift metric, not benchmark accuracy.
- Preserve no-context baselines.
- Control distractor identity, token frequency and baseline logit.
- Include **both** semantic conditions and **both** non-semantic conditions.
- Normalize causal effect across scale; raw head count is invalid.
- Generic entrainment-head discovery is predecessor replication, not novelty.
- Require causal ablation/patching; probe/head overlap alone cannot establish two circuits.
- Never infer mechanism from scaling correlation without intervention.

## 8. Promote / kill criteria

### Promote if

- exact mother opposite-sign scaling reproduces;
- generic predecessor entrainment causality reproduces;
- a semantic-selective causal component/pathway can be distinguished from mechanical copying;
- intervention effects across scale separate at least two of H1/H2/H3.

### Strong negative outcomes

- if one shared writer explains all early computation and the split emerges only late, that cleanly supports H3 and falsifies the natural distinct-circuit story;
- if semantic gate and copying writer double-dissociate, the result provides a mechanistic scaling law rather than merely a behavioral one.

### Kill / redesign if

- the mother sign split disappears under exact metric reproduction;
- apparent semantic components are driven by token identity/baseline logit;
- causal differences vanish after normalization across scale;
- the only result is “different sizes have different heads” with no explanation of the sign reversal.

## 9. Paper-level narrative

> **Does scaling make LLMs globally less distractible, or does it strengthen both a low-level copying reflex and a separate semantic control system?**

This connects mechanistic scaling laws to RAG, misinformation robustness, noisy/long context, contextual memory and the broader question of whether bigger models remove primitive heuristics or merely learn stronger control systems on top of them.
