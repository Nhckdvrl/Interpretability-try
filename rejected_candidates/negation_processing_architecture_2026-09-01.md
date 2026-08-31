# Rejection — Negation Processing Architecture

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Semantic aliases

- two-step negation vs direct negative representation
- suppression vs constructive negation
- literal positive simulation then negation
- negated-concept inhibition vs compositional construction
- delayed vs incremental negation processing

## Natural question considered

> Does an LLM process negation by first activating the positive/negated state and suppressing it, or by directly constructing a representation of the negative phrase/state?

This is a mature cognitive/psycholinguistic debate and has strong modern behavior, but the LLM mechanistic question is already directly occupied.

## Decisive kill evidence

Zhou, Zhou, Jia & May (2026), **`How Language Models Process Negation`** (arXiv:2605.03052), studies negation mechanistically in Mistral-7B and Llama-3.1-8B.

The paper explicitly compares two computational hypotheses:

1. an **attention-based suppression** mechanism that attends to the phrase being negated and suppresses related concepts;
2. a **constructive** mechanism that directly forms a representation of the entire negative phrase.

Using observational and causal interpretability methods, it reports that both mechanisms exist and that the constructive mechanism is more prominent. It additionally identifies late-layer shortcut-promoting attention behavior whose ablation improves negation accuracy.

This directly occupies both the natural object and the theory-level causal factorization. Human-inspired two-step simulation framing cannot create a new N2 delta because it maps closely onto the suppression-vs-construction alternatives already tested.

## Gate audit

```yaml
paper_scale: PASS
benchmark_removal: PASS
natural_object: PASS
scientific_lineage: PASS
modern_open_behavior: PASS
N0_object_ownership: FAIL
N1_causal_occupancy: FAIL
N2_delta_width: FAIL
verdict: KILL-NOVELTY
```

## Nearest-neighbor warning

Also nearby:

- 2026 human/LLM work explicitly testing the two-step simulation account of negation;
- Thunder-NUBench / Thunder-KoNUBench behavior resources;
- multiple negation-specific causal-tracing studies.

Do not revive by changing negation benchmark, model family, language, or MI method, or by renaming suppression/construction as two-step/one-step.

## Resurrection condition

Only reconsider if a genuinely distinct semantic or cognitive negation axis is identified that is not equivalent to suppression vs constructive representation or late shortcut interference, with an independent experiment-ready substrate.
