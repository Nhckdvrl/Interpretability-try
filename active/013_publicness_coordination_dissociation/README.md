# 013 — Publicness–Coordination Dissociation

Status: `N0-PASS / HOLD-D0 / ACTIVE-PREFLIGHT / HARNESS-READY-r1 / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #3**.

```yaml
formal_n0_verdict: PASS
d0_verdict: HOLD
validation_authorized: false
```

## Mother question

With proposition, recipients and first-order knowledge matched, can a model correctly recognize the higher-order consequences of a public event and use explicitly stated common knowledge, yet underuse natural publicness in a coordination policy?

The harness retains recursive public/private capability gates, the explicit-common-knowledge action bridge, participant symmetry, paraphrase controls, and matched-length triplets. `policy_gold_text` is audit metadata and never enters a model prompt.

## D0 disposition

See [`D0_AUDIT.md`](D0_AUDIT.md).

Thomas et al.'s human common-knowledge coordination paradigm is an excellent natural anchor: messenger/private/shared knowledge versus publicly audible common knowledge, with explicit coordination payoffs. However the accessible materials do **not** currently yield the frozen requirement of at least 20 independent natural scenario pairs under a clean adaptation/redistribution path.

Counting participant swaps, answer orders, paraphrases or multiple payoff conditions from the same game as separate scenarios would be pseudoreplication. Nearby games have different equilibrium structures and cannot be pooled without a game-by-game audit. Therefore this project remains `HOLD-D0`; do not manufacture a synthetic Alice/Bob button-game bank just to make the harness runnable.
