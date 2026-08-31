# Rejection — Reflexive Attraction: Structural Filter vs Cue-Based Retrieval

Date: 2026-09-01  
Verdict: **KILL-BEHAVIOR**

## Semantic aliases

- reflexive attraction in LLMs
- Principle A vs cue-based retrieval
- structural filtering vs feature matching for reflexives
- grammar-constrained retrieval vs similarity-based interference
- illicit antecedent attraction
- reflexive antecedent competition

## Natural question considered

> When an LLM resolves a reflexive, does grammar first restrict memory search to structurally legal antecedents, or do structural and feature cues jointly retrieve from a broader candidate set so that grammatically illicit distractors can compete?

This is a genuine sentence-processing question. Human psycholinguistics has long used reflexive attraction to distinguish memory architectures, and the distinction is independent of any benchmark.

## Scientific lineage

Human work provides strong theory:

- reflexive attraction is selectively weaker than agreement attraction under many configurations;
- this has motivated qualitatively different access mechanisms, strict structural filtering, and cue-based retrieval accounts;
- Parker & Phillips (2017) showed reflexive attraction can be induced under stronger feature mismatch and modeled both presence/absence using ACT-R cue-based retrieval;
- later work tests error-driven vs routine retrieval and representation updating.

Thus PAPER-SCALE itself is not the problem.

## Decisive kill evidence

The required **modern LLM behavioral premise is not frozen**.

The audit found:

- modern open models have strong evidence for general anaphor agreement / Principle-A / binding sensitivity (e.g. ACL 2026 evaluates anaphor agreement and binding in Llama-3.2, Mistral, Gemma-3 and other open models);
- a 2026 Turkish reflexive-binding paper reports locality preferences, but compares a Llama-2-derived Turkish model with a closed reasoning model and does not establish the required illicit-distractor attraction phenotype;
- no strong 2025–2026 source located in this audit establishes the **same reflexive-attraction interference signature** on at least two genuinely different modern open families using an executable row-level artifact.

General reflexive competence is not enough. The scientific question requires a distractor-competition effect diagnostic of retrieval architecture.

Continuing would require constructing distractor manipulations and running Llama/Qwen/Gemma first to discover whether attraction exists. Under the current protocol, that is behavior lottery, not an experiment-ready scientific premise.

## Gate audit

```yaml
paper_scale: PASS
benchmark_removal: PASS
scientific_lineage: PASS
N0_object_ownership: tentatively_clear
N1_causal_occupancy: tentatively_clear
exact_modern_open_family_attraction_phenotype: FAIL
requires_new_G0_to_discover_behavior: true
verdict: KILL-BEHAVIOR
```

## Nearest-neighbor warning

Do not confuse this with generic mechanistic entity binding. Recent work such as `Mixing Mechanisms: How Language Models Retrieve Bound Entities In-Context` studies positional/lexical/reflexive mechanisms in synthetic entity-binding tasks, which is a different object but makes generic `binding retrieval mechanism` language unsafe.

Likewise, ACL 2026 `Different types of syntactic agreement recruit the same units within large language models` already causally studies anaphor agreement as a syntactic functional category; a revived project must remain specifically about theory-diagnostic attraction/retrieval rather than generic anaphor units.

## Resurrection condition

Reconsider only if a public study/artifact establishes reflexive-attraction interference on >=2 modern open families (preferably Llama/Qwen/Gemma/Mistral) with exact row-level distractor manipulations and non-floor/non-ceiling effects. At that point the structural-filter vs cue-based-retrieval question can be re-audited without behavior discovery.
