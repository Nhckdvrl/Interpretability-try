# Rejection — Hard Constraint vs Soft Preference

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Natural question

Does a planning model distinguish **rules that must never be violated** from **preferences that should be satisfied when possible**?

## Semantic aliases

- hard vs soft constraints
- requirement vs preference
- feasibility vs utility
- must-have vs nice-to-have

## Why it looked promising

This is an excellent ordinary-language Route-C distinction with immediate agent relevance and clean conflict cases. A latent-state intervention could test whether the model uses constraint type when trade-offs arise.

## Decisive kill evidence

2026 work already makes the hard/soft distinction itself the central LLM-planning object. **U-Define: Designing User Workflows for Hard and Soft Constraints in LLM-Based Planning** explicitly separates hard rules that must not be violated from soft preferences that allow flexibility, and assigns different verification mechanisms to the two types.

Source: https://arxiv.org/abs/2605.02765

Additional 2026 constrained-planning work uses the same feasibility-vs-preference split. Thus an MI project would mainly ask how an already-explicit object is represented internally.

## Strongest-neighbor warning

Do not revive as requirement-vs-preference direction, must-vs-should latent state, constraint priority circuit, or compliance-vs-utility arbitration without a new independent scientific object.

## Death code

`F2 / N0-N2 — direct contemporary LLM planning object ownership.`

## Resurrection condition

Only reconsider a genuinely different semantic-status distinction whose scientific meaning is not reducible to hard/soft constraint typing.
