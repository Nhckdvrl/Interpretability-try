# Rejection Record — Memorized vs Inferred Answer Source

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

Does a language model internally know whether an answer came from memory or was derived by reasoning?

Semantic aliases:

- memorized vs inferred answer
- recall vs reasoning source
- memory-derived vs reasoning-derived knowledge
- remembered vs worked-out answer

## Why it looked strong

- The distinction is immediate and non-technical: people distinguish `I remember this` from `I worked this out`.
- It matters for confidence, verification, retrieval, and reasoning reliability.
- It fits the Route-C simplicity prior: identify a simple latent property first, then characterize/causally test it.

## Decisive kill evidence

Findings ACL 2025 `The Reasoning-Memorization Interplay in Language Models Is Mediated by a Single Direction` already directly occupies the mechanistic object. The paper identifies linear features in the residual stream that distinguish reasoning tasks from memory-intensive tasks and causally manipulates those features to shift the balance between reasoning and memory recall.

Additional nearby work further crowds the distinction:

- ACL 2025 Findings `Memorization vs. Reasoning: Updating LLMs with New Knowledge` explicitly separates direct memorization probes from indirect reasoning probes.
- 2024 work on memorization in logical reasoning uses internal probing and per-sample memorization scores to study when models switch between reasoning and memorization.
- EACL 2026 extends memorization-constrained reasoning to story understanding.

Thus moving the same question to factual QA or newer open models would not create a new concept-level scientific object.

## Do not revive by

- replacing reasoning benchmarks with factual QA;
- changing models to Qwen3/Llama-3.x/Gemma-3;
- using SAE instead of linear residual directions;
- reframing as `does the model know where its answer came from?`;
- adding a retrieval-routing application.

## Resurrection condition

Only reconsider if the source distinction is genuinely different from memory recall vs reasoning—for example an independently meaningful origin property not reducible to memorization, inference, context retrieval, or source attribution.
