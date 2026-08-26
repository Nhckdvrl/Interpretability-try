# Search Round — 2026-08-27 — Natural-Phenomenon-First (Final)

**Status:** ROUND COMPLETE — 3 PRE-CANDIDATES SELECTED

## Gate

A topic must survive the delete-LLM test, have strong modern open-weight behavioral evidence, use exact/local scoring where possible, avoid broad→strict extrapolation, and retain an unoccupied causal-mechanism question with a mechanism-dependent method opening.

## Killed in this round

- LLM-native operational anomalies: `MOTHER_QUESTION_NOT_NATURAL`; see `agent_tool_use.md`.
- Generic false-belief / Theory-of-Mind failure: `MECHANISM_COLLISION`; see `cognitive_decision_making.md`.
- Generic working-memory interference / recency: `MECHANISM_COLLISION`; see `cognitive_decision_making.md`.
- Minimal-edit belief-revision inertia: `INSUFFICIENT_EXACT_CROSS_FAMILY_EVIDENCE`; see `cognitive_decision_making.md`.
- Parametric hindsight: `NARRATIVE_COLLISION`; see `temporal_hindsight.md`.
- Causal-ladder degradation (observation → intervention → counterfactual): behavior is strong, but METER already performs information-flow tracing, attention masking and evidence-flow intervention, hence `MECHANISM_COLLISION`.
- Generic order effects / primacy-recency: interesting but weaker exact modern-open-family support than the final survivors; published work also already proposes mitigation. `LOWER_PRIORITY / INSUFFICIENT_MODERN_EXACT_COVERAGE`.

## PRE-CANDIDATE 1 — Latent inference without rational downstream use

**Natural phenomenon.** Bayesian evidence accumulation: infer the latent state generating sequential evidence, then use that posterior consistently in downstream prediction/decision.

**Behavioral foundation.** `BayesBench: Evaluating LLM Belief Trajectories Under Multi-Turn Evidence Accumulation` evaluates seven open-weight Llama 3 / Qwen 2.5 models from 3B to 70B and reports a recurring dissociation: scale improves latent-state inference but downstream prediction does not improve in lockstep; explicitly conditioning on the inferred latent helps but does not close the gap. In medical triage, Qwen-14B, Qwen-32B and Llama-70B reach roughly 0.80 probability on the true communication profile mid-conversation while urgency prediction remains much weaker and middle urgency labels collapse toward extremes.

**Mechanism split.** (A) no calibrated posterior representation; (B) posterior exists but is not routed into target computation; (C) posterior is routed but distorted at categorical readout.

**Cheap G0.** Start with closed-form/symbolically scored coin-flip and recommender tasks; use local Qwen/Llama checkpoints and token log-probabilities. Require strong latent discrimination plus large downstream Bayes error on the same cases. No LLM judge.

**Collision.** No direct white-box paper was found that explains this inference→use dissociation; BayesBench remains behavioral and leaves representational underpinnings open.

**Method opening.** Representation correction vs posterior routing vs late readout calibration, depending on the mechanism.

**Status:** PRE-CANDIDATE — strongest survivor.

## PRE-CANDIDATE 2 — Ownership-specific choice-supportive bias

**Natural phenomenon.** Choice-supportive bias / post-decision commitment: making a choice can itself increase confidence in it and make later revision harder without new evidence.

**Behavioral foundation.** Nature Machine Intelligence 2026 reports Gemma-3-12B change-of-mind 34.0% when the initial answer is hidden versus 13.1% when shown. Across Gemma-3-27B, Llama-70B, DeepSeek and additional datasets, the Shown-vs-Hidden gap is 14–25 percentage points. The effect disappears when the identical visible answer is attributed to another model (~31.3% vs ~33.2%) and persists when all relevant facts are in context (17.2% vs 33.2%), ruling out simple copying and generic in-context dominance.

**Mechanism split.** (A) self-authorship/ownership representation gates evidence weighting; (B) self-generation creates a generic commitment state; (C) evidence stays intact and only late confidence/readout is boosted.

**Cheap G0.** Binary factual/numerical choices with scripted advice. Compare Hidden / Own-Shown / Other-Shown using exact A/B logits, balanced by initial correctness/confidence. No external judge or advice model required.

**Collision.** Behavioral literature is established, but no white-box mechanism for the ownership-specific matched contrast was found. `When Agents Commit Too Soon` studies long-horizon hidden-state convergence, not own-vs-other attribution of an identical prior choice.

**Method opening.** Selectively suppress self-commitment only when new evidence conflicts, rather than globally increasing answer-changing.

**Status:** PRE-CANDIDATE — strong behavior, medium collision risk.

## PRE-CANDIDATE 3 — Reliability-weighted cue combination under uncertainty

**Natural phenomenon.** Multisensory/multi-cue integration: two noisy measurements of one quantity should be weighted by reliability.

**Behavioral foundation.** `Emergent Bayesian Behaviour and Optimal Cue Combination in LLMs` adapts classic psychophysics tasks and evaluates nine models. Open-model overall BayesBench scores show substantial headroom: Qwen2.5-VL-32B 0.60, Phi-4 Multimodal 0.51, Gemma-3-4B-it 0.43, Mistral-24B 0.66, versus Llama-4 Maverick 0.85. The paper shows that accuracy and cue-integration efficiency can dissociate and explicitly states that its analysis is behavioral; a causal/mechanistic account remains future work.

**Mechanism split.** (A) cue reliability is represented but ignored; (B) reliability is not represented; (C) cue combination is internally correct but final magnitude readout is distorted.

**Cheap G0.** Locally recreate only deterministic line-ratio / marker-location tasks with controlled noise. Measure unimodal error variance, derive normative reliability weights, then test multimodal shifts on Gemma-3 and Qwen2.5-VL. No judge or external generator.

**Collision.** No direct white-box mechanism paper for reliability-weighted multimodal cue integration was found.

**Method opening.** Reliability-aware activation gating vs uncertainty representation training vs late readout correction.

**Status:** PRE-CANDIDATE — conceptually strong but needs local confirmation because failure magnitude varies by model.

## Ranking

1. Bayesian latent inference → downstream-use dissociation.
2. Ownership-specific choice-supportive bias.
3. Reliability-weighted cue combination.

No candidate is ACTIVE yet; all require a frozen local G0 before promotion.
