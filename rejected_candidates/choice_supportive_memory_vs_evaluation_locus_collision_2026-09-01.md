# Rejection Record — Choice-Supportive Bias: Memory Distortion vs Evaluative Reweighting

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

After an LLM makes a choice, does it later defend that choice because it has **distorted what it remembers about the options**, or because the factual memory remains intact but the model **reweights/evaluates the chosen option more favorably**?

## Semantic aliases

- memory distortion vs evaluation bias
- recall corruption vs post-choice rationalization
- choice-supportive memory vs judgment
- memory locus vs evaluative locus
- remembered facts vs later preference reweighting

## Why it looked promising

Choice-supportive bias has a mature human cognitive literature in which post-choice memory distortion, retrieval-time attribution, cognitive dissonance, and evaluative rationalization are theoretically separable. AAAI 2025 reports the bias across many LLMs, including open families, using paradigms adapted from human work. This initially looked like a legitimate Route-B mechanism question rather than a new benchmark.

## Decisive kill evidence

The AAAI 2025 mother already directly decomposes the phenomenon along the proposed axis.

`LLM Agents Can Be Choice-Supportive Biased Evaluators: An Empirical Study` does not merely report an aggregate post-choice bias. It explicitly runs:

1. **memory-based experiments** adapted from Henkel & Mather, where models choose between options and later recall/attribute old and distractor features; and
2. **evaluation-based experiments designed specifically to remove reliance on memory**, in which a separate evaluation agent receives the options and prior choice and evaluates neutral characteristics.

The paper explicitly motivates the second paradigm by asking whether choice-supportive bias persists **without contextual-memory effects**, and reports that the bias can remain even when contextual hallucination is not observable. Its stated contributions include both `memory-driven choice-supportive bias` and a `novel evaluation-based test ... without relying on the standard forgetting process`.

Thus the scientific distinction `memory distortion versus memory-independent evaluative bias` is already a core behavioral decomposition in the strongest LLM mother. A mechanistic double dissociation would primarily translate that mother decomposition into hidden-state/causal terms rather than introduce an independent scientific object.

## Strongest-neighbor warning

Do not revive as:

- recall-state vs evaluation-state circuits;
- memory corruption vs preference reweighting patching;
- choice-supportive retrieval vs judgment mechanisms;
- factual memory preserved but value changed;
- two-pathway choice-supportive bias in LLMs.

The mother already establishes and explicitly interprets the memory-dependent versus memory-independent distinction.

## Death code

`F2 / N2 — strongest mother already owns the proposed locus decomposition; remaining contribution is behavior-to-mechanism translation.`

## Resurrection condition

Only reconsider if a distinct post-choice cognitive property is found that is not equivalent to memory distortion, evaluation bias, perceived control, or choice-supportive attribution and has independent theory/substrate.
