# Rejection Record — Formal Authority vs Epistemic Expertise

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

When an LLM follows a person's advice, does it distinguish **having institutional authority** from **actually being knowledgeable or competent**?

Examples:

- a CEO can have high formal authority but low expertise on a narrow technical question;
- a specialist engineer can have high expertise but low organizational rank;
- a senior physician may have both;
- a novice with no office may have neither.

## Semantic aliases

- authority vs expertise
- rank vs competence
- institutional power vs epistemic credibility
- social status vs domain knowledge
- formal authority vs subject-matter expertise

## Why it looked promising

This initially had an unusually clean Hamdi-style shape. A 2026 mechanistic mother already establishes a graded authority hierarchy in open LLMs, while expertise/competence is an independently natural property that can in principle be crossed with formal rank. The ordinary question is immediate: `Does the model listen because someone has power, or because they know what they are talking about?`

## Decisive kill evidence

The strongest authority neighbor already explicitly owns the proposed distinction rather than merely happening to use expert personas.

`A Mechanistic View of Authority Hierarchy in LLM Sycophancy` (2026) studies graded persona authority in Llama-3.1-8B, Qwen3-8B, and Gemma-2-9B and analyzes the internal mechanism. Crucially, its appendix explicitly contrasts **competence-defined expertise levels** with **socially recognized institutional roles / authority**, noting that competence descriptions and institutional authority are different constructions.

A second direct neighbor, `When Truth Is Overridden` / related 2026 mechanistic sycophancy work, explicitly tests expertise-level framing and reports that expertise levels do not form the same stable internal clusters as the opinion/authority manipulation. Thus the exact question `is expertise represented separately from authority?` is already part of the current mechanistic literature, including a negative/weak-representation result.

Findings ACL 2026 `Sounding vs. Being an Expert: Disentangling Authority, Register and Cultural Impact in Sycophantic LLMs` further crowds the scientific space by explicitly disentangling explicit authority/credentials from other signals that make a source appear authoritative.

Therefore an `authority direction orthogonalized against expertise` project would not add a new scientific object. Its main delta would be a different factorial design or stronger causal intervention on an axis already explicitly contrasted in the strongest neighbors.

## Strongest-neighbor warning

Do not revive as:

- rank vs competence direction;
- authority vs expertise orthogonal subspaces;
- institutional power vs subject-matter knowledge;
- expert-low-rank vs novice-high-rank cross-cells;
- authority/expertise double dissociation;
- steering authority while holding competence fixed.

The conceptual distinction itself is already discussed and experimentally manipulated in the closest mechanistic literature.

## Death code

`F2 / N0-N2 — exact authority-versus-competence distinction already belongs to strongest mechanistic neighbors.`

## Resurrection condition

Only reconsider if the new object is genuinely different from competence/expertise/authority/source-credibility—for example, an independently motivated social-cognitive distinction whose predictions are not reducible to source rank or epistemic competence.
