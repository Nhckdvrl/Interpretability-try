# Rejection Record — Impossible vs Improbable Modal Representation

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

Can a language model internally distinguish an event that is physically impossible from one that is merely very unlikely?

## Why it initially looked strong

- The question is fully natural and benchmark-independent.
- Findings ACL 2025 `Not quite Sherlock Holmes` established a strong behavioral window: Llama 3, Gemma 2, and Mistral NeMo can fail to rank merely improbable events above impossible ones.
- This is exactly the kind of simple top-down/model-biology phenomenon now prioritized by `FINDING_RULES.md` v2.1.

## Decisive kill evidence

ICLR 2026 `Is This Just Fantasy? Language Model Representations Reflect Human Judgments of Event Plausibility` directly studies the internal representation of modal categories. It identifies hidden-state modal difference vectors separating probable, improbable, impossible, and nonsensical events across multiple language models and explicitly reports strong internal discrimination for the difficult improbable-vs-impossible contrast.

Therefore the clean Route-C question `does the model internally distinguish impossibility from improbability even when output probabilities fail?` is already directly occupied at the representation level.

## Strongest-neighbor warning

Do not revive this by:

- changing to another plausibility dataset;
- swapping Llama/Gemma/Mistral versions;
- replacing linear directions with SAE/probes/patching;
- reframing as `where is impossibility encoded?`;
- adding causal steering unless the new scientific object is genuinely different from modal-category representation itself.

## Resurrection condition

Only reconsider if a future candidate asks a distinct natural modal question not answered by modal-category geometry—for example a genuinely new causal or compositional property whose headline is not simply `possible vs impossible representation`.
