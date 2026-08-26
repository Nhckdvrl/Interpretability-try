# Search Round — 2026-08-27 — Natural-Phenomenon-First

**Status:** IN PROGRESS  
**Purpose:** preserve both surviving selections and killed paths so later rounds do not rediscover the same ideas.

## Round gate

A topic is not eligible merely because an LLM benchmark shows a large failure. It must begin from an independently meaningful natural/formal phenomenon. Apply the **delete-LLM test**: after removing LLM/prompt/tool/CoT/instruction vocabulary, the mother question must still make sense as a question about probability, causality, memory, belief, ontology, decision, perception, language, etc.

Additional promotion requirements:

1. Exact behavioral contrast already has substantial evidence on modern open-weight models; prefer two model families.
2. Effect size must be visibly large, not a 2–5 pp statistical curiosity.
3. Operationalization in prior evidence must match the proposed mother question; no broad→strict extrapolation.
4. G0 must be runnable locally without commercial LLM judges; deterministic / programmatic gold preferred.
5. Collision audit must leave an unoccupied causal-mechanism question and a mechanism-dependent method opening.

## Already killed in this round

- LLM-native operational anomalies (multilingual tool serialization, thinking-mode scope collapse, reasoning-vs-response instruction following, reasoning-persuaded LLM judge): `MOTHER_QUESTION_NOT_NATURAL`; see `agent_tool_use.md`.
- Generic false-belief / Theory-of-Mind failure: `MECHANISM_COLLISION`; see `cognitive_decision_making.md`.
- Generic working-memory interference / recency: `MECHANISM_COLLISION`; see `cognitive_decision_making.md`.
- Minimal-edit belief-revision inertia: `INSUFFICIENT_EXACT_CROSS_FAMILY_EVIDENCE`; see `cognitive_decision_making.md`.
- Parametric hindsight: `NARRATIVE_COLLISION`; see `temporal_hindsight.md`.

## Current survivors under audit

### S1 — Bayesian sequential evidence accumulation: latent inference vs downstream use

Natural mother phenomenon: how should beliefs change as probabilistic evidence arrives sequentially, and how should an inferred latent state be used in a later decision?

Current reason to investigate: BayesBench reports a recurring dissociation across open-weight Llama/Qwen models: scale improves inference of the latent source, but this does not reliably produce calibrated downstream predictions; some models over-update toward extremes. Exact per-model effect sizes and collision status are still being audited.

### S2 — Causal hierarchy: observation vs intervention vs counterfactual worlds

Natural mother phenomenon: observing X, intervening to set X, and imagining what would have happened under a contrary intervention are three distinct levels of causal reasoning.

Current reason to investigate: METER reports a large monotonic performance drop across these rungs on modern open models, including Qwen3 and Llama. Exact paired evidence, public scorer availability, and mechanism collision are still being audited.

### S3 — OPEN SLOT

Candidates being audited include reliability-weighted multi-cue integration and formal invariance/equivalence phenomena. No candidate will be promoted without exact modern open-family evidence.
