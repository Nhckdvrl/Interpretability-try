# Rejection Record — Function vs Material / Appearance in Object Identity

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

When deciding what an object really is, does a language model care more about what it is for than what it looks like or what it is made of?

Semantic aliases:

- function vs appearance
- telos vs material
- artifact essentialism
- what something is for vs what it looks like
- transformation task in LLMs

## Why it initially looked strong

- The question is immediate and benchmark-independent.
- It comes from classic psychological work on essentialist categorization and artifact identity.
- It is exactly the sort of simple everyday distinction prioritized by `FINDING_RULES.md` v2.1.

## Decisive kill evidence

Cognitive Science 2023 `You are what you're for: Essentialist categorization in large language models` directly applies classic transformation-task logic to LLMs and compares function/telos, material, and appearance as determinants of categorization. Its central behavioral conclusion is that purpose/function is the strongest determinant, followed by material and appearance.

Therefore a project asking whether a model internally represents `function over appearance/material` would primarily convert an already-established headline interpretation into mechanistic evidence. Changing the model generation or MI technique would not widen the concept-level question.

## Do not revive by

- changing object categories;
- using newer Llama/Qwen/Gemma models;
- replacing behavior with probes/SAEs/activation patching;
- renaming the axis `artifact identity`, `telos`, or `functional essence`.

## Resurrection condition

Only reconsider if the new question concerns a distinct natural property of object representation that is not equivalent to the already studied function/material/appearance competition.
