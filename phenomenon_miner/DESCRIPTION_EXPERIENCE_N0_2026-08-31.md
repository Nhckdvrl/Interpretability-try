# 023 mother-inclusion N0 — inferring risk vs valuing risk

Date: 2026-08-31  
Status: `N0-PASS-SHARPENED / BEHAVIOR CONTRACT REQUIRED`

## Natural-question card

```yaml
P0_natural_question:
  plain_question: >
    When an LLM sees the same risk as explicit probabilities or as an exact
    history of outcomes, does it infer a different distribution, or apply a
    different value/choice policy to the same inferred distribution?
  one_example: >
    "10% win 50, otherwise 0" and a 20-event record containing exactly two
    50s and eighteen 0s carry the same empirical distribution. If choices
    differ, did the model misread the odds or value history-derived odds
    differently?
  why_care: >
    Decision-support and agent systems receive both summarized forecasts and
    raw histories. Equivalent evidence should not silently enter different
    risk policies.
  understandable_without_dataset_or_MI: true
P1_existence_prior:
  anchor: established_mother
  evidence: >
    Human description-experience research and ACL 2026 Mind the (DH) Gap both
    establish presentation-dependent risky choice; the unresolved object is
    inference versus valuation/routing.
  estimated_risk_that_phenomenon_is_absent: medium
P2_minimal_sanity:
  faithful_without_complex_builder: true
  examples_needed: 12 predeclared gambles
  expected_visible_signature: >
    correct frequency and expected-value judgments with a residual paired
    choice shift between exact histories and probability/count descriptions.
P3_dataset_role:
  question_preexists_dataset: true
  replacement_dataset_preserves_question: true
P4_restriction_budget:
  phenomenon_defining_conditions:
    - same payoff support and exact empirical distribution
    - representation as probability summary versus outcome history
  validity_exclusions: []
  controls:
    - count description
    - option order
    - sequence shuffle
    - amount scale
    - frequency and expected-value capability
    - stochastic dominance
  arbitrary_conjunctive_restrictions_count: 0
P5_mechanistic_forks:
  - history fails to form the same probability state
  - probability aligns but valuation or probability weighting differs
  - probability and value align but a representation-mode policy/readout differs
verdict: PASS_SHARPENED
```

## Mother inclusion

Ge, Zhang, and Vorobeychik, *Mind the (DH) Gap!* (ACL 2026 Outstanding
Paper), already owns:

- the existence and name of an LLM description-history gap;
- a 20-model behavioral comparison;
- reasoning-versus-conversational clustering;
- option order, gain/loss framing, explanation, and sample-size analyses;
- the claim that mathematical-reasoning training is a key differentiator.

The mother uses three base loss prospects. Its implicit condition samples 20
or 100 outcomes from the underlying distributions with four seeds, so realized
histories need not exactly match the explicit probabilities. It fits a
prospect-theoretic behavioral summary but explicitly warns that this is not a
definitive mechanism.

Therefore the old title-level claim “LLMs exhibit a description-experience
gap” is forbidden. Exact-frequency histories are also not a sufficient title:
they are a measurement control that removes sampling error.

## Surviving object

The independent conceptual question is:

> Does representation format change the inferred probability state, the
> transformation from probability to value, or only the final choice policy?

This is not a request to localize the mother's behavioral effect. The three
accounts disagree about what information the model possesses and what repair
would work. They make distinct behavioral prerequisites and, only after those
pass, distinct causal interchange predictions.

## Internal-history audit

Repository search found the same candidate only in the 023 README and the
decision-anomaly pre-candidate audit. That audit already stated the inference /
weighting / readout fork. No active or archived project owns this risk-specific
factorization. Generic representation-to-use projects do not establish the
same information-format manipulation or decision-theoretic object.

## Anti-narrowing and stop rules

- Do not claim first LLM DH/DE gap.
- Do not retell reasoning-versus-conversational differences.
- Do not promote an effect that disappears with exact frequencies.
- Do not condition the headline on a post-hoc gamble subset.
- Do not call a counting or EV failure a value-policy divergence.
- If exact histories and count descriptions agree after capability controls,
  stop rather than narrowing to one sequence order or gamble.
- N1 is intentionally not repeated per project instruction; this document is
  the previously required N0 mother-inclusion re-audit.

Mother: https://aclanthology.org/2026.acl-long.479/
