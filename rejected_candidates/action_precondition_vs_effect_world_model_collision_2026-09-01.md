# Rejection — Action Preconditions vs Effects

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Natural question

When reasoning about an action, does a model distinguish **what must already be true for the action to be possible** from **what becomes true because the action happens**?

## Semantic aliases

- precondition vs effect
- applicability vs consequence
- action prerequisites vs outcomes
- world-model transition roles

## Why it looked promising

The distinction is simple, useful for agents, and gives matched event/action content with two natural relational roles. It also offers an obvious causal-use test in planning.

## Decisive kill evidence

Xie, Yang, Gunerli & Riedl, **“Making Large Language Models into World Models with Precondition and Effect Knowledge”** (COLING 2025 Main) directly defines these as two critical world-model functions: determining action applicability from preconditions and predicting the resulting world state from effects. The paper trains separate LLMs for the two knowledge types, validates them with humans, and tests planning-relevant action chains.

Source: https://aclanthology.org/2025.coling-main.503/

The natural axis is therefore already explicit in LLM research. Asking whether residual streams contain separable precondition/effect states would primarily mechanize the same object.

## Strongest-neighbor warning

Do not revive as applicability-vs-consequence, prerequisite-vs-result, STRIPS role representation, or precondition/effect causal directions.

## Death code

`F2 / N0-N2 — direct LLM scientific-object ownership.`

## Resurrection condition

A new topic would need a different independent action-semantic property, not a mechanistic re-expression of the precondition/effect split.
