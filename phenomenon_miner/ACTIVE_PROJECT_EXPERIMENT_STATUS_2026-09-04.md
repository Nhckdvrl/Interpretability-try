# Active-project experimental status — 2026-09-04

This document summarizes what the first information-gain experiments establish. A historical
registration does not protect a project from experimental archive. Exact predictions,
implementation, numbers, and limitations remain in each project's `EXPERIMENT_LOG.md`.

## 034 — Prospective-memory retrieval architecture

```yaml
behavior: established on released PMBench; controlled S0-2 panel failed
representation: not tested
causal_use: not_identifiable_yet
strongest_alternatives:
  - released heartbeat prompts can themselves retrieve the intention
  - controlled focality clone is confounded by Qwen ongoing-task category failure
  - cue trials are at or near ceiling
new_mechanistic_prediction: none licensed by the current clone
decision: stop patching; require a new preregistered non-ceiling behavioral microscope
```

Released baselines are non-floor/non-ceiling in three open families, and the released
monitoring-required partition is much harder than the no-monitoring partition. This is a real
prospective-memory denominator, not a retrieval-architecture result. In the controlled clone,
Qwen failed the no-cue focal comprehension control (6.25%) while Llama passed it; the families
also showed opposite focality effects on reminder margins. Layer or prompt search would not
repair this identifiability failure.

## 035 — Shared dynamic context update

```yaml
behavior: mixed; anaphora established, deterministic presupposition recipient failed
representation: not tested
causal_use: not_identifiable_yet
strongest_alternatives:
  - released presupposition ratings are modest and nonmonotone
  - corrected Llama readout collapses to high and Qwen is dominated by low
new_mechanistic_prediction: none licensed without a within-presupposition denominator
decision: ARCHIVE
```

The corrected full-data validation fails on both model families. Forced high-versus-low
accuracy is 0.500 for Llama and 0.550 for Qwen; Llama assigns all 90 items to high, whereas
Qwen assigns 68/90 to low. This exposes opposite checkpoint-specific response priors, not a
stable second phenomenon that could receive a cross-task intervention. Because the broad
claim requires both behavioral legs, and the failure does not expose another venue-scale
mechanistic object, 035 is physically archived rather than narrowed to a classifier study.

## 038 — Unresolved-reference representation architecture

```yaml
behavior: established in Llama-3.1-8B and Qwen3-32B
representation: asymmetric candidate/decision axis established; format remains ambiguous
causal_use: resolved-reference axis established, balanced candidate separability unsupported
strongest_alternatives:
  - direction is mention-position rather than entity-specific
  - AmbiCoref candidate labels are confounded with structural family
  - output competition may occur downstream of an underspecified state
new_mechanistic_prediction: an entity-specific commitment axis must survive mention-order swaps
decision: highest priority; build one independently balanced entity-specific causal calibration
```

Both families comprehend the reference task and keep both licensed candidates above a
distractor. Both also exhibit large candidate asymmetry and frequent permutation-dependent
preference reversals. A fixed middle-layer Llama direction causally changes held-out resolved
choices beyond random and shuffled controls, but on unresolved items candidate causal
separability is zero and effects are position-asymmetric. A structurally shared unresolved
state fails held-out-family transfer. Clean parallel alternatives (H1) are unsupported; a
single competition/commitment axis (H3-like) is currently most compatible, but not uniquely
identified. This is the closest project to a publishable mechanistic result and the one place
where another causal experiment has high expected information value.

## 040 — Numerical identity versus qualitative sameness

```yaml
behavior: direct cross-surface identity established in Qwen; Llama mixed
representation: not tested
causal_use: unsupported for arbitrary token-specific history
strongest_alternatives:
  - most recently established entity-to-code binding dominates retrieval
  - direct identity judgment need not control arbitrary property inheritance
new_mechanistic_prediction: weakening the last-binding trace should restore identity-governed history without harming type knowledge
decision: preserve as a strong dissociation; only continue with a binding-overwrite/rescue test
```

Qwen passes the natural direct-identity and type controls, avoiding the Davis–Altmann novelty
collapse. It nevertheless fails the frozen arbitrary-history contract: which entity-to-code
binding was established last produces a large crossover, even with a different-type
competitor, while type knowledge remains mostly intact. This is not evidence for a successful
identity circuit. It is a sharper negative result: locally available identity knowledge is
not robustly used to govern episodic history inheritance. A causal overwrite/rescue experiment
could turn the dissociation into a paper-scale explanation without narrowing the headline to
generic recency.

## Information-value ordering

1. **038:** one balanced entity-specific causal calibration can decide whether the replicated
   competition signature is commitment or position.
2. **040:** continue only if a clean intervention can dissociate binding overwrite from
   identity and preserve the type control.
3. **034:** redesign behavior before any activation work; released scaffolds are not mechanism.
4. **035:** completed and archived; no further compute.

Adding more layers, probes, model families, or post-hoc item subsets would not reduce the
current dominant uncertainty in 034/035. For 038/040, the remaining value lies in causal
specificity and mechanism-derived behavioral predictions, not broader method accumulation.
