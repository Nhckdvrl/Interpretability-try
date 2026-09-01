# Rejection — Cause vs Enabling Condition

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Natural question

Does a model distinguish something that **causes an outcome** from something that merely **makes the outcome possible**?

## Semantic aliases

- cause vs enable
- cause vs enabling condition
- trigger vs background condition
- causal production vs causal permission

## Why it looked promising

Humans make this distinction even when necessity/sufficiency alone does not separate the roles. The classic psychology literature supplies matched scenarios and competing explanations, so the question is natural and mechanistically tempting.

## Decisive kill evidence

The distinction has already been imported directly into NLP causal reasoning. Yang et al., **“Towards Fine-grained Causal Reasoning and QA”** introduce human-annotated fine-grained causal relations with explicit labels **Cause / Enable / Prevent**, plus causality detection, extraction, and QA tasks. The released artifact contains 25K annotated event pairs and 24K QA pairs.

Artifact: https://github.com/YangLinyi/Fine-grained-Causal-Reasoning  
Paper: https://arxiv.org/abs/2204.07408

Classic independent lineage: Cheng & Novick (1991), **“Causes versus enabling conditions.”**

Because `enable` is already an explicit LM/NLP causal-reasoning object, an open-weight MI follow-up would mostly be behavior/object -> internal mechanism.

## Strongest-neighbor warning

Do not revive as trigger-vs-background cause, enabling-state direction, cause/enable patching, or a `Cause/Enable/Prevent` circuit.

## Death code

`F2 / N0-N2 — the exact fine-grained causal role is already an explicit NLP object.`

## Resurrection condition

Only reconsider if a distinct causal-semantic axis is found that is not one of the already-labelled fine-grained causal relations and has independent scientific value.
