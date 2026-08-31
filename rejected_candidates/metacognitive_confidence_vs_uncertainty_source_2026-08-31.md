question: Does an LLM's metacognitive confidence signal distinguish epistemic ignorance from aleatoric/input ambiguity, rather than representing only a scalar confidence level?
mother: ICLR 2026 Evidence for Limited Metacognition in LLMs
semantic_aliases:
  - confidence source decomposition
  - epistemic vs aleatoric internal uncertainty
  - ignorance vs ambiguity metacognition
  - uncertainty type representation
what_was_reviewed: mother scope + strongest-neighbor / mechanism ownership
kill_class: F2
kill_evidence: ACL 2026 'Quantifying Aleatoric Uncertainty of In-Context Learning for Robust Measure of LLM Prediction Confidence' explicitly decomposes aleatoric and epistemic uncertainty using internal model representations/self-function vectors, and related 2026 uncertainty work treats the same distinction as the headline object. Reframing the question as whether uncertainty source selects different actions (delegate/retrieve vs clarify) would no longer inherit an established behavior from the mother and would require a fresh behavior-discovery experiment, creating F1 behavior-lottery risk.
nearest_neighbor_warning: Do not revive by changing uncertainty benchmark, using entropy/probes/SAEs, moving from ICL to QA, or renaming aleatoric uncertainty as ambiguity/noise. Do not rescue with action routing unless differential action selection is already independently established on analyzable open models.
resurrection_condition: Reopen only if an already-established open-model behavior shows distinct adaptive actions for matched-confidence uncertainty sources, leaving an unoccupied causal controller question beyond existing epistemic/aleatoric representation work.
