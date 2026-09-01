# Rejection Record — Relative vs Absolute Gradable Adjective Threshold Computation

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

Does a language model distinguish adjectives whose truth threshold must be set from context (for example `tall`) from adjectives whose lexical scale points toward a minimum or maximum endpoint (for example `wet`, `straight`, `full`)?

## Semantic aliases

- relative vs absolute gradable adjectives
- contextual threshold vs endpoint standard
- open-scale vs closed-scale adjective semantics
- minimum/maximum-standard adjective representation
- context-dependent vs lexically anchored degree standard

## Why it looked promising

The distinction is a classic formal-semantic object independent of benchmarks. `John is tall` can change truth value when the comparison class changes, while minimum/maximum-standard adjectives have endpoint-oriented lexical semantics whose apparent context sensitivity has a different theoretical source. Human work provides multiple independent diagnostics including negation/antonym entailments, comparative entailments, degree modifiers, comparison-class shifts, and visual-world processing.

The question initially looked like a strong Route-C candidate because current 2026 work on adjective representation mostly targets broader semantic class/gradability rather than this exact threshold distinction.

## Decisive kill evidence

AAAI 2023 **`Adjective Scale Probe: Can Language Models Encode Formal Semantics Information?`** already makes the exact relative/absolute distinction part of its central LLM scientific object.

The paper constructs a theory-driven formal-semantic probe for adjective degree semantics and explicitly states that:

- negation/antonym entailment patterns are used to probe the **context sensitivity of absolute adjectives (`bent`, `straight`) versus relative adjectives (`big`, `small`)**;
- comparative entailment tests distinguish **relative adjectives (`big`, `long`)**, **minimum-standard absolute adjectives (`bent`, `wet`)**, and **maximum-standard absolute adjectives (`straight`, `safe`)**;
- the tests probe the context-dependence of comparison thresholds and domain restrictions;
- the authors frame the study as asking whether transformer language models encode these abstract degree-semantic properties.

The study evaluates BERT, DeBERTa and T0 and finds substantial failures, while showing that ASP fine-tuning can generalize to untrained adjectives/tests. Separately, 2022 work on evaluativity implicatures already directly crosses relative and absolute adjective classes in pretrained LMs, and 2026 adjective-geometry work continues probing formal semantic properties in contextual Transformer representations.

Therefore a new Llama/Qwen project whose headline is `context-derived threshold vs lexical endpoint standard` would not introduce a fresh scientific object. The primary novelty would be replacing earlier behavioral/probing work with modern open-weight causal MI, which fails the current N2 standard.

## Strongest-neighbor warning

Do not revive as:

- relative-vs-absolute adjective direction;
- contextual-threshold vs endpoint-standard activation patching;
- minimum/maximum standard subspaces;
- `tall` vs `straight` causal circuits;
- open-scale vs closed-scale steering;
- modern-open-model replication of ASP with hidden-state methods.

The exact adjective-class distinction and its formal-semantic consequences are already direct language-model objects.

## Death code

`F2 / N0-N2 — exact relative/minimum-absolute/maximum-absolute degree-semantic distinction already explicitly probed in language models; remaining delta is stronger MI.`

## Resurrection condition

Only reconsider if a different adjective-semantic property is found whose scientific interpretation is independent of degree scale class, contextual threshold, scalar ordering, evaluativity, or the formal-semantic capabilities already covered by ASP, with a separate natural substrate and predictions.
