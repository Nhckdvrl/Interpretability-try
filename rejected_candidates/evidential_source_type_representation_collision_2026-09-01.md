# Rejection — Evidential Source Type Representation

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Natural question

Does a model distinguish information known from direct evidence, hearsay/report, and inference, separately from how certain the proposition is?

## Semantic aliases

- evidentiality
- direct vs indirect evidence
- reported/hearsay vs inferred
- source-sensitive reasoning
- evidential source vs epistemic confidence

## Why it looked promising

Source type and certainty are naturally distinct: a report can be certain while a direct observation can be uncertain. This suggested Hamdi-style cross-cells and a simple latent semantic axis.

## Decisive kill evidence

ACL 2026 Main `It's Not What You Say, It's How You Say It: Evaluating LLM Responses to Expressions of Belief` explicitly separates evidentiality from epistemic stance and evaluates Llama3, Qwen3, and Gemma3 across evidential/stance expression types. Independent 2026 work on Turkish evidentials directly evaluates source-sensitive reasoning under direct versus indirect evidential morphology and source trust manipulations.

Under the post-039 rule, the object is already owned even if no paper has used exactly our preferred causal patching method. A direct/hearsay/inferred hidden-state direction would largely be behavior/semantic-factorization -> stronger MI.

## Strongest-neighbor warning

Do not revive as evidentiality vector, direct-vs-hearsay steering, source-type circuit, or source-confidence orthogonalization merely by switching language or model.

## Death code

`F2 / N0-N2 — explicit modern-LLM ownership of evidentiality as a source-sensitive semantic dimension.`

## Resurrection condition

Only reconsider if the new object is independently distinct from evidentiality/source-sensitive reasoning, not a mechanistic refinement of the same axis.