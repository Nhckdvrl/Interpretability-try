# Rejection Record — Once-True vs Never-True Historical Validity

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

When two statements are false now, does a language model internally distinguish one that used to be true from one that was never true at all?

Semantic aliases:

- once true vs never true
- stale fact vs fabricated fact
- historical validity vs current falsehood
- outdated knowledge vs confabulation
- former truth vs invented falsehood

## Why it initially looked strong

- The question is simple, ordinary, and independent of any benchmark.
- It directly matters for stale knowledge and hallucination: `Boris Johnson is UK prime minister` is a different kind of false statement from `Taylor Swift is UK prime minister`.
- EvolveBench exposes deterministic validity intervals for historical subject-relation-object facts and public open-model outputs, so a clean non-LLM-generated substrate exists.
- A 2026 hallucination taxonomy independently distinguishes temporal outdated hallucination from fabricated hallucination, supporting the object as real rather than synthetic.

## Decisive kill evidence

`The Geometry of Forgetting: Temporal Knowledge Drift as an Independent Axis in LLM Representations` (arXiv:2605.09195, 2026) directly occupies the decisive contrast.

The paper constructs complete Wikidata holder timelines and defines:

- **Stale-Recall:** the model retrieves a past holder that was genuinely correct during training but is wrong now;
- **Confabulation:** the model produces a holder that appears nowhere in the historical timeline.

The authors explicitly state that these two outputs are both currently wrong but differ in temporal validity, then train a dedicated residual-stream probe to distinguish Stale-Recall from Confabulation. Reported AUROC is 0.89–0.99 across six instruction-tuned models. The paper further argues that temporal drift is an internal direction independent of correctness and uncertainty and adds activation patching / causal steering.

This is essentially the exact `once true vs never true` internal-representation question, not merely a neighboring temporal-QA benchmark.

## Strongest-neighbor warning

Do not revive by:

- using EvolveBench instead of the paper's Wikidata timeline;
- changing office-holder relations or domains;
- switching to newer Llama/Qwen checkpoints;
- replacing probes with SAE/patching/steering;
- reframing as `historical validity trace`;
- emphasizing current-false matched pairs.

Those are measurement/method refinements of an already occupied concept-level axis.

## Resurrection condition

Only reconsider a temporal-status topic if the new property is genuinely distinct from stale-vs-confabulated temporal validity—for example a different natural temporal concept whose causal role is not reducible to whether a fact has drifted or whether a retrieved answer ever appeared in the fact timeline.
