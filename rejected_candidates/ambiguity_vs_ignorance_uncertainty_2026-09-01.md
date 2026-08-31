# Rejection Record — Ambiguity vs Ignorance Uncertainty

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

Does a language model distinguish `I do not know the answer` from `the question itself does not have one uniquely determined answer`?

Semantic aliases:

- ignorance vs ambiguity
- epistemic vs aleatoric uncertainty
- knowledge gap vs input ambiguity
- reducible vs irreducible uncertainty
- unknown answer vs inherently ambiguous question

## Why it initially looked strong

- The distinction is intuitive and important for reliable assistants: ignorance should trigger retrieval or learning, while ambiguity should trigger clarification.
- It is a mature uncertainty distinction outside LLMs.
- It fits the v2.1 preference for simple natural objects.

## Decisive kill evidence

The concept-level axis is already crowded and substantially occupied:

1. ICML 2024 `Decomposing Uncertainty for Large Language Models through Input Clarification Ensembling` explicitly separates aleatoric uncertainty caused by ambiguity/underspecification from epistemic uncertainty caused by missing model knowledge.
2. AAAI 2026 `Fine-grained Uncertainty Decomposition in Large Language Models: A Spectral Approach` again directly targets aleatoric-vs-epistemic decomposition in LLMs.
3. ACL 2026 `Quantifying Aleatoric Uncertainty of In-Context Learning for Robust Measure of LLM Prediction Confidence` connects the distinction to internal/mechanistic representations through self-function vectors.
4. 2026 `The Anatomy of Uncertainty in LLMs` explicitly decomposes uncertainty into input ambiguity, knowledge gaps, and decoding randomness.

A native activation-probe/patching project could still add method detail, but the headline scientific question `does the model distinguish ambiguity from ignorance?` is no longer a fresh paper-scale object.

## Strongest-neighbor warning

Do not revive by changing the ambiguity dataset, using newer Llama/Qwen models, replacing uncertainty estimators with SAE/probes, or narrowing to a single QA task.

## Resurrection condition

Only reconsider if a different uncertainty distinction has independent scientific meaning and is not a relabeling of aleatoric/input ambiguity vs epistemic/knowledge-gap uncertainty.
