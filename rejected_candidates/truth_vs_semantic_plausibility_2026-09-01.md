# Rejection Record — Truth vs Semantic Plausibility

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

Does a language model internally distinguish whether a statement is actually true from whether it merely sounds likely or semantically plausible?

Semantic aliases:

- truth vs plausibility
- factual truth vs likely-sounding statement
- true-but-surprising vs false-but-plausible
- factuality independent of semantic likelihood

## Why it initially looked strong

- The distinction is ordinary and benchmark-independent: true statements can sound surprising, while false statements can sound perfectly plausible.
- It admits a clean conceptual 2×2 and connects naturally to hallucination and factual verification.
- Human truth-judgment work already separates truth from plausibility, so the scientific object is not invented for LLMs.
- It fits the v2.1 Route-C preference for a simple top-down/model-biology question.

## Decisive kill evidence

The remaining novelty delta is too narrow once the strongest neighbors are considered.

1. Marks & Tegmark, `The Geometry of Truth` (COLM 2024), explicitly introduced non-factual `likely` controls and truth/probability anti-correlation controls to test whether a truth direction is merely a text-probability / likelihood direction. Their central representational claim is already that a truth-related direction is not reducible to likely-sounding text.
2. ACL 2026 Findings `How Language Models Conflate Logical Validity with Plausibility` directly analyzes the geometry of validity and plausibility and uses steering interventions to show bidirectional causal contamination between the two.

A new experiment using human semantic-plausibility ratings instead of token likelihood would refine the control, but the conceptual question would still be `is correctness/truth separable from plausibility?`, which is already substantially occupied at both representational and causal levels.

Therefore the safest description of a new project would be an improved or more semantically faithful instantiation of an existing axis, not a new paper-scale scientific question.

## Strongest-neighbor warning

Do not revive this by:

- replacing LM probability with human plausibility ratings;
- changing the factual domain;
- swapping probe/SAE/activation patching methods;
- using newer Llama/Qwen models;
- renaming the axis `surprising truth vs plausible falsehood`.

Those changes improve measurement but do not widen N2.

## Resurrection condition

Only reconsider if the new object is an independently meaningful property not already reducible to likelihood/plausibility-versus-correctness—for example a distinct historical, social, modal, or source-status property with its own natural cross-cells and causal consequences.
