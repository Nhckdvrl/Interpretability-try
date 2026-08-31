# Rejection — Idiom Literal–Figurative Processing Architecture

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Semantic aliases

- literal-first vs direct figurative access
- idiom lookup vs compositional processing
- figurative retrieval vs literal composition
- parallel literal/figurative competition
- idiom direct access vs context-guided selection
- literal suppression in idiom comprehension

## Natural question considered

> When an idiom can be interpreted literally or figuratively, does an LLM first compose the literal meaning and later override it, retrieve the figurative meaning directly, or maintain competing interpretations in parallel?

This is a legitimate psycholinguistic question, but the contemporary LLM causal mechanism space is already directly occupied.

## Decisive kill evidence

EACL 2026 Main, **`Tug-of-war between idioms' figurative and literal interpretations in LLMs`**, already uses causal tracing to study the internal competition between literal and figurative meanings.

The paper reports a mechanistic story in which:

- figurative information is retrieved early;
- figurative processing suppresses literal interpretation;
- contextual information is used from early layers and conflict is refined later;
- distinct/competing pathways carry figurative and literal information.

That directly occupies the natural direct-access / literal-composition / competition axis. EMNLP 2025 work on whether idiom understanding reflects memorization or reasoning further crowds the neighboring concept space.

## N0 / N1 / N2 audit

```yaml
N0_object_ownership: FAIL
reason: literal-vs-figurative competition is already the EACL 2026 paper's headline object

N1_causal_occupancy: FAIL
reason: causal tracing already investigates the internal literal/figurative pathways and suppression dynamics

N2_delta_width: FAIL
reason: another patching/SAE/circuit study would refine an already-owned mechanism rather than introduce a new scientific question
```

## Do not revive by

- changing idiom dataset;
- using another model family/language;
- replacing causal tracing with activation patching/SAE/probes;
- renaming the alternatives as lookup/composition, direct access/indirect access, or parallel competition;
- focusing on a different layer/token position.

## Resurrection condition

Only reconsider if an independent figurative-language theory axis is found that is conceptually distinct from literal-vs-figurative competition/access and is not already addressed by recent idiom mechanism work.
