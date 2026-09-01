# Rejection — Cardinality vs Ordinality in Number Representation

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Natural question

Does a language model distinguish a number used as **quantity** (`three apples`) from the same numerical concept used as **position/order** (`the third runner`), or is both carried by one generic magnitude representation?

## Semantic aliases

- cardinal vs ordinal number
- quantity vs rank/order
- how many vs which position
- cardinality vs ordinality

## Why it looked promising

Cardinality and ordinality are distinct core concepts in human numerical cognition, and the same underlying numerical values can occur in both roles. The distinction is simple, natural, and supports cross-context controls.

## Decisive kill evidence

ACL 2026 Main `Language Models Learn Universal Representations of Numbers and Here’s Why You Should Care` directly studies the internal geometry of numerical representations across LLM families, explicitly emphasizing accurate encoding of numeric **and other ordinal information** and mechanistic manipulation of the shared sinusoidal structure. July-2026 `Geometry of Ordinal Representations in Language Models` further studies ordinal manifolds across multiple tasks in Gemma-2 and Qwen3 and uses activation patching/ablation to establish causal relevance.

The proposed cardinal-versus-ordinal project therefore sits inside an already heavily mechanized number/ordinal representation object. Even if no title phrases the exact binary factorization, the remaining delta would be a finer split of an occupied scientific object rather than a Hamdi-style independent new property.

## Strongest-neighbor warning

Do not revive as quantity-vs-rank direction, cardinal/ordinal steering, number-use subspace, or cross-context number patching.

## Death code

`F2 / N0-N1-N2 — direct modern-LLM mechanistic occupancy of numeric and ordinal representation geometry.`

## Resurrection condition

Only a numerical property demonstrably independent of magnitude/ordinal geometry and not a finer task split could reopen this area.