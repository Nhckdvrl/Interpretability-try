# Rejection — Shared Monotonicity Across Logical Inference and NPI Licensing

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Semantic aliases

- reusable downward-entailing context representation
- shared monotonicity computation
- monotonicity across NPI licensing and natural-logic inference
- DM/UM semantic state reuse
- negative-polarity licensing via monotonicity
- shared natural-logic context representation

## Natural question considered

> Do language models implement a reusable semantic monotonicity operation that supports both entailment reasoning and negative-polarity-item licensing, or do the two behaviors rely on separate lexical/syntactic shortcuts?

This is a natural formal-semantic question and would otherwise resemble a strong cross-phenomenon Route A. However, the key relation between monotonicity and NPI processing is already directly owned by prior LM interpretability work.

## Decisive kill evidence

Jumelet, Denić, Szymanik, Hupkes & Steinert-Threlkeld, Findings ACL 2021, **`Language Models Use Monotonicity to Assess NPI Licensing`**, explicitly asks:

1. whether LMs create semantic categories of linguistic environments based on monotonicity; and
2. whether those categories play the same functional role in LM language understanding, using NPI licensing as the case study.

The paper goes beyond a surface correlation:

- it probes downward- vs upward-monotone environments;
- demonstrates NPI licensing behavior;
- introduces a diagnostic-classifier ranking method linking monotonicity information to the information used for NPI predictions;
- reports significant overlap between monotonicity representations and NPI processing;
- removes NPI-containing training examples and still finds monotonicity representations;
- removes NPIs from specific environments and shows generalization to unseen licensing environments, arguing against simple co-occurrence.

Its explicit conclusion is that LMs acquire a **general notion of monotonicity that is employed for NPI licensing**.

Therefore adding a modern natural-logic inference window and causal cross-task patching does not start from an unasked scientific object. It principally strengthens an already-owned representational/functional claim from probe/generalization evidence to causal intervention.

## Gate audit

```yaml
paper_scale: PASS
benchmark_removal: PASS
natural_object: PASS
formal_lineage: PASS
N0_object_ownership: FAIL
N1_causal_occupancy: partially_open_but_insufficient
N2_delta_width: FAIL
reason: prior LM work already claims a general monotonicity representation functionally used for NPI licensing; causal cross-task transfer would refine rather than introduce the core concept
verdict: KILL-NOVELTY
```

## Nearest-neighbor warning

Also nearby:

- causal-effect studies of natural-logic/monotonicity features in Transformer NLI;
- neuro-symbolic natural-logic models;
- modern monotonicity-focused architectural work.

Do not revive by simply replacing the old LMs with Llama/Qwen/Gemma or replacing diagnostic classifiers with activation patching/SAEs.

## Resurrection condition

Only reconsider if a **different formal semantic operation** is identified whose cross-phenomenon reuse has not already been functionally linked in LM work, with independent modern behavioral windows and an unoccupied causal factorization.
