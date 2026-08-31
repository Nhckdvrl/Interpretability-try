# Rejection Record — Stable Trait vs Temporary State Representation

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

Does a language model distinguish an enduring trait of a person from a temporary state they happen to be in right now?

Semantic aliases:
- stable trait vs transient state
- personality vs situation
- enduring disposition vs current condition
- state-trait representation

## Why it initially looked strong

The distinction is ordinary, psychologically mature, and directly relevant to personalization: `Alex is anxious today` should not automatically mean `Alex is an anxious person`.

## Decisive kill evidence

Findings ACL 2026 `Beyond Fixed Psychological Personas: State Beats Trait, but Language Models are State-Blind` directly makes state-vs-trait the headline object. It introduces Chameleon, decomposes within-person state and between-person trait variance, and concludes that LLMs focus on trait while being insensitive to state.

A follow-up that probes hidden states to explain the reported state-blindness would therefore be a direct behavior-to-mechanism continuation of the same axis rather than a new concept-level question.

## Do not revive by

- switching personality datasets;
- using newer Llama/Qwen checkpoints;
- replacing behavior analysis with probes/SAEs/patching;
- renaming the question `disposition vs situation`.

## Resurrection condition

Only reconsider if the new object is a distinct person-representation property not reducible to the state-trait distinction already claimed by the 2026 mother.
