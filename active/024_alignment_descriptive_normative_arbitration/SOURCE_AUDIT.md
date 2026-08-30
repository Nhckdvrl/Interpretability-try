# 024 D0 Source Audit

## Frozen source

- Upstream: `https://github.com/eliaka/repeatedgames`
- Commit: `224a605a21127cac69763f990e077f7b05abd422`
- File: `human_experiment/analysis/repgames.csv`
- SHA-256: `f3c3d46a2e34f85f950bfdffd0d04d6c6fc748268c14e5700646e44b2d42d11a`
- License: MIT

The source contains 3,900 published decisions: 195 participants, two games, and
exactly ten ordered rounds per participant-game. PD and BoS each contribute
1,950 decisions. Each participant experienced one of two precomputed GPT-4
opponent policies (`Base` or `Prompted`); these are source strata, not model
families in our evaluation.

## Field reconstruction audit

The experiment implementation fixes `action=0 -> F` and `action=1 -> J`.
The cleaned CSV contains the human action and payoff, but not the opponent
action directly. The field named `coordination` is an analysis variable and is
not a reliable same-action record (in particular for PD), so the builder does
not use it to reconstruct history. Because every valid human-action/payoff pair
maps to exactly one opponent action under the published binary payoff tables,
the opponent action is recovered by inverting those tables:

```text
game + human action + observed payoff -> unique opponent action
```

Four rows have an action/payoff combination outside the published payoff table:
two rows in participant 17/BoS, one in 38/BoS, and one in 153/PD. The exclusion
unit is frozen conservatively as the complete participant-game trajectory,
because a missing opponent action would contaminate every later history in that
trajectory. Thus 30 decisions are removed before model calls, leaving 3,870
decisions and 387 complete ten-round trajectories. No row is removed based on
the human choice or any model outcome. The builder fails closed on any other
schema, payoff, or trajectory-length violation.

## Independent targets

- Descriptive target: the observed human action in the source row.
- PD normative target: `F`. Under the published payoff matrix, `F` strictly
  dominates `J` in the stage game (10>8 against J; 5>0 against F), and finite
  ten-round backward induction therefore selects F at every round.
- BoS has multiple pure equilibria. Its unique fully mixed equilibrium assigns
  human `p(F)=10/17`; this is reported as a scalar reference, not mislabeled as
  a unique action-level normative gold.

## Population and limitations

The primary mother-reproduction population is all round 2-10 decisions from
the 387 audited trajectories in both games (3,483 rows). Apart from the frozen
source-integrity exclusion above, nothing is filtered by action, history,
participant, opponent policy, or apparent model success. Round 1 is a
predeclared boundary control rather than a primary estimand because it contains
only the two initial game states.

The human participants played against precomputed LLM policies and were told
they could be facing a human or an artificial agent. This is a limitation of
the mother source, not a post-hoc selection introduced here. The source is
nevertheless real participant behavior and is the same repeated-game family
used in the mother paper.
