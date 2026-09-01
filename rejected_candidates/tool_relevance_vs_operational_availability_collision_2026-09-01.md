# Rejection Record — Tool Relevance vs Operational Availability

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

Does an LLM agent distinguish a tool that is semantically irrelevant from a tool that is exactly the right tool in principle but currently unavailable, inaccessible, or unsupported?

## Semantic aliases

- relevance vs availability
- right tool vs usable tool
- semantic suitability vs operational feasibility
- irrelevant tool vs inaccessible relevant tool
- capability availability vs semantic relevance

## Why it looked promising

The distinction is natural and practically important. ACL 2026 `Do LLMs Know Tool Irrelevance?` provides a strong mechanistic mother for semantic relevance, while real agents frequently face permission failures, missing tools, offline services, or unsupported capabilities. A clean conceptual 2×2 seems possible: relevant/irrelevant × available/unavailable.

## Decisive kill evidence

The second axis is not an omitted unexplored property.

- **FAIL-TaLMs / Benchmarking Failures in Tool-Augmented Language Models** explicitly contains 575 examples where necessary tools are deliberately unavailable/masked, separately analyzing human-replaceable and non-replaceable missing tools.
- **CAR-bench (ACL 2026 Long)** explicitly evaluates `capability awareness` under missing tools, unavailable information, and unsupported capabilities, and reports agents fabricating information or failing to acknowledge their limits.
- Adaptive-planning benchmarks such as **AdaPlanBench** also treat unavailable/nonfunctional tools as explicit world constraints.
- The first axis is already owned mechanistically by ACL 2026 `Do LLMs Know Tool Irrelevance?`, which isolates semantic relevance from structural parameter matching and identifies competing internal pathways.

Therefore `relevance × availability` would mostly combine two already-established tool-status dimensions and then apply mechanistic methods to their interaction. The 2×2 is useful engineering evaluation, but it does not create a new paper-scale scientific object under Route A/N2.

## Strongest-neighbor warning

Do not revive as:

- relevant but inaccessible vs irrelevant tool directions;
- permission-aware relevance;
- semantic suitability vs feasibility subspaces;
- missing-tool representation;
- `right but unavailable` tool steering;
- a 2×2 crossing SABEval with FAIL-TaLMs/CAR-bench.

A new factorial crossing is not enough when both conceptual axes are already independently owned.

## Death code

`F2 / N2 — two established tool-status objects combined into a new 2×2; remaining contribution is interaction/mechanization rather than a new scientific object.`

## Resurrection condition

Only reconsider if a distinct agent property is found whose scientific interpretation is not reducible to semantic relevance, tool necessity, capability awareness, or tool availability, and which has its own natural theory/substrate.
