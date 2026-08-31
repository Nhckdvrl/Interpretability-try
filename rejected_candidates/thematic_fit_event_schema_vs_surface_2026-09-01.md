# Thematic fit: event-schema integration vs local/surface association

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Semantic aliases

- generalized event knowledge mechanism
- thematic-role prototype vs event schema
- verb-role association vs whole-event integration
- situation-model thematic fit
- local lexical fit vs global event plausibility

## Natural question

When deciding whether an entity is a plausible participant in an event, does a language model build a whole-event/situation representation, or mostly use local verb-role and surface associations?

This is a natural event-semantics question and initially had an unusually good modern substrate: CoNLL 2026 releases code/results for Llama-3.2 and Qwen2.5 thematic-fit evaluation.

## Decisive kill evidence

The concept-level interpretation predates the modern mother and is already directly occupied. *SEM 2021 *Did the Cat Drink the Coffee? Challenging Transformers with Generalized Event Knowledge* explicitly moves beyond isolated verb-argument typicality to the typicality of **entire events and situations**, compares Transformers with an event-integration model, and concludes that Transformer predictions often depend on surface features such as frequent words, collocations, and syntactic patterns rather than fully capturing generalized event knowledge.

Thus the proposed headline `whole-event schema vs local/surface association` is not a fresh scientific question opened by CoNLL 2026. A modern Llama/Qwen causal study would most naturally read as causal verification/localization of the existing GEK-vs-surface interpretation.

## Data note

This is not a substrate kill. Public thematic-fit artifacts are useful and modern. The failure is N2 delta width.

## Nearest-neighbor warning

Do not revive by renaming `event schema` as `situation model`, `role prototype`, `event representation`, or `generalized event knowledge`, or by switching from correlations/logprobs to SAE/probe/patching.

## Resurrection condition

Only reopen if a new, independently motivated semantic axis is identified that the GEK literature does not already frame, and thematic fit becomes merely a measurement window rather than the source of the headline.
