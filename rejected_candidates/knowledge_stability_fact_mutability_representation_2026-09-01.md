# Rejection Record — Knowledge Stability / Fact Mutability Representation

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

Do language models internally know which knowledge is likely to expire and which facts are effectively stable?

Semantic aliases:

- knowledge stability representation
- fact volatility representation
- mutable vs immutable facts
- evergreen vs time-sensitive knowledge
- which knowledge expires
- expected fact lifetime / temporal mutability

## Why it looked unusually strong

This was a high-quality Route-C candidate under `FINDING_RULES.md` v2.1:

- the question is ordinary and benchmark-independent;
- `drift` and `volatility` are naturally distinct: drift asks whether a fact has already changed, whereas volatility asks whether that kind of fact is inherently likely to change;
- EMNLP 2025 Main `Will It Still Be True Tomorrow?` gives a modern multilingual behavioral mother and public EverGreenQA rows;
- the property matters directly for retrieval freshness, RAG routing, hallucination, and model updating;
- the headline remains meaningful even without any MI method.

## Decisive kill evidence

NAACL 2024 Short `MuLan: A Study of Fact Mutability in Language Models` already occupies the central latent-property question.

The paper explicitly asks RQ2: whether LLMs represent time-contingent truths differently, making representations differentiable by mutability. It uses probe classifiers and reports that the representations do encode mutability. The authors conclude that time contingency may be hard to observe through prompting but is present in the models' representations.

MuLan is not a weak accidental neighbor. Its dataset is designed specifically to study mutable vs immutable relations and includes an `Immutable-N` control so that mutable relations are not trivially identified merely by having multiple possible objects. It studies six LLMs and reports differences in confidence, representations, and update behavior by mutability.

Therefore a 2026 project using EverGreenQA, newer Qwen/Llama checkpoints, stronger lexical controls, SAEs, activation patching, or steering would primarily upgrade the evidence/method/model generation for the same concept-level object rather than introduce a new scientific question.

## Additional neighbors

- EMNLP 2023 `Mitigating Temporal Misalignment by Discarding Outdated Facts` studies fact duration prediction.
- EMNLP 2025 Main `Will It Still Be True Tomorrow?` studies evergreen vs mutable question awareness and downstream retrieval/self-knowledge applications.
- Findings ACL 2026 `When Facts Change` studies how mutability affects temporal conflict resolution.
- 2026 temporal-drift representation work separately studies whether already-drifted facts form an internal direction.

Together these make the area scientifically important but too conceptually occupied for the current register.

## Do not revive by

- changing MuLan to EverGreenQA / RecencyQA;
- using human-curated multilingual queries instead of Wikidata triples;
- swapping LLaMA-2/Falcon for Qwen2.5/Llama-3.x/Gemma-3;
- replacing probes with SAE, activation patching, causal steering, or retrieval-tool decisions;
- reframing as `knowledge stability direction` or `does the model know which knowledge expires?`.

Those are useful follow-ups but fail the current N2 delta-width requirement.

## Resurrection condition

Only reconsider if the new question concerns a genuinely different natural temporal property that is not equivalent to fact mutability, expected lifetime, evergreenness, current drift, or stale-vs-confabulated historical validity.
