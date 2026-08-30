# 023 D0 frozen preflight

## What is tested

The mother already establishes an LLM description-history gap. D0 does not
retest that claim. It asks whether a residual presentation effect survives when
the empirical distribution is identical and models can report both frequencies
and expected values. That prerequisite is necessary before inference,
valuation, and policy-routing mechanisms can be distinguished.

## Design

- 12 predeclared gambles across rare gain, rare loss, mixed, equal-EV variance,
  stochastic dominance, and sign-flip families;
- payoff scales ×1 and ×10;
- both option orders;
- three deterministic shuffles of an exact 20-outcome multiset;
- probability description, count description, and raw exact sequence;
- separate choice, EV comparison, and two frequency queries.

Every probability is a multiple of 0.05, so a 20-event history represents it
exactly. No sampled-frequency deviation exists. The count condition has the
same empirical semantics without sequence length/order.

## Frozen decision rule

Choice effects are eligible only when frequency, EV, dominance, and option-order
gates pass. Human-direction normalization is predeclared only for the six rare
gain/loss and sign-flip gambles. Promotion requires an effect against both
probability and count descriptions, bootstrap intervals above zero, at least
four of six directed gambles positive, at least two family passes, and positive
aggregate direction in at least three families.

No per-item capability filtering, post-hoc gamble selection, or hidden-state
call is allowed. Full constants are frozen in `configs/d0_contract.json`.
