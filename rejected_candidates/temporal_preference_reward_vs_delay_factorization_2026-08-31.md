# Rejection — Temporal Preference → Reward Magnitude vs Delay

```yaml
question: Does an LLM compute intertemporal choice from separable reward-magnitude and delay representations that are integrated downstream, or from an already-compressed scalar subjective-value code?
mother: Temporal Preference Concepts and their Functions in a Large Language Model (2026)
semantic_aliases:
  - reward vs delay representation in intertemporal choice
  - amount-delay factorization
  - subjective value representation in LLM temporal choice
  - discounted utility code
  - magnitude vs temporal cost geometry
what_was_reviewed: mother full scope, parametric geometry, behavioral analysis, direct successor
kill_class: F2
kill_evidence: The mother explicitly defines intertemporal choice as options differing in reward and delay, states that the instrument separates reward from delay, and constructs a parametric activation grid over reward amounts, delay times, and time horizons specifically to disentangle their effects on internal representations. Its behavioral appendix separately measures reward sensitivity and finds reward magnitude largely inert for the focal Qwen model. The Aug-2026 successor Intertemporal Preference Steering in Qwen3 further tests steering on a monetary task varying reward size and delay. The proposed factorization is therefore inside the mother's/successor's scientific scope rather than an omitted adjacent axis.
nearest_neighbor_warning: Do not revive as amount vs time, magnitude effect, subjective value, discounted utility, reward sensitivity, indifference curves, or by changing discount function/model/steering method.
resurrection_condition: Reopen only if a different classical decision variable is identified that the temporal-preference work does not manipulate or characterize internally and that yields a distinct causal computation.
```
