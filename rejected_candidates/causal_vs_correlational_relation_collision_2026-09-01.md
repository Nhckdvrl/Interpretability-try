# Rejection — Causal vs Correlational Relation

Date: 2026-09-01  
Verdict: **KILL-NOVELTY / KILL-BEHAVIOR**

## Natural question

Does a model distinguish **one thing causing another** from the two things merely **varying together / being correlated**?

## Semantic aliases

- causation vs correlation
- causal relation vs statistical association
- cause vs correlate
- causal structure vs co-occurrence

## Why it looked promising

The distinction is maximally natural, societally important, and seemingly amenable to controlled sentence pairs with the same entities/events. A reusable causal-relation state would also have a clear downstream-use question.

## Decisive kill evidence

William Lithgow-Serrano, Kanjirangat & Antonucci, **“Causal Understanding by LLMs: The Role of Uncertainty”** (UncertaiNLP 2025) directly makes causal-relation typing an LLM object. Seven models including Qwen-7B perform four-way classification over **direct causal / conditional causal / correlational / no relationship**, and the authors explicitly interpret the near-random behavior as evidence about structured causal representation.

Source: https://aclanthology.org/2025.uncertainlp-main.19/

Other contemporary Corr2Cause/generalization work also directly asks whether LLMs distinguish correlation from causation. Therefore a hidden-state/patching follow-up has too little N2 width. In addition, the published behavioral phenotype is weak enough that a Route-C claim of robust relation-type use would require rediscovering the phenomenon on a new substrate.

## Strongest-neighbor warning

Do not revive as:

- cause-vs-correlation direction;
- causal-relation SAE feature;
- correlation-to-causation patching;
- a different causal benchmark;
- “structured causal representation” with a stronger MI method only.

## Death code

`F2 + F1 — direct object ownership, plus weak established behavior for the intended causal-use story.`

## Resurrection condition

Only reconsider a genuinely different causal-semantic property not already part of causal-relation classification/generalization, with an independently established modern open-model phenomenon.
