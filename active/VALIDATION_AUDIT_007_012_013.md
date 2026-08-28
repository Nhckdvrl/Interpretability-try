# Pre-merge validation audit — active 007 / 012 / 013

Date: 2026-08-29  
Scope: `007_weak_evidence_backfire`, `012_source_discount_recovery`, `013_publicness_coordination_dissociation`  
Result: `HARNESS-READY / NOT READY-TO-SMOKE`

This is a scientific-design and implementation audit. It is **not** an independent N0 sign-off, D0 sign-off, or behavioral result. The authoritative registry therefore remains at `READY-TO-SMOKE: 0` and all three configs retain `validation_authorized: false`.

## Repository-level invariants

The three harnesses follow the frozen discovery process rather than treating implementation as scientific authorization:

- no LLM judge or API scorer; local causal LMs are scored by exact `A/B` continuation log probability;
- answer order and natural readout wording are counterbalanced;
- repeated identical prompt/candidate requests are lifetime-cached;
- external provenance is mandatory for formal D0; custom-only rows are rejected;
- model construction is blocked while `validation_authorized` is false;
- prompt variants, evidence directions, participant perspectives, and repeated measurements are not promoted to independent statistical samples;
- model-level bootstrap statistics use the natural scenario pair as the unit;
- capability-floor and artifact verdicts can never count toward panel promotion;
- mechanism experiments remain forbidden until behavior, N1, cross-family/scale, and strong-model gates survive.

## 007 — Weak-Evidence Backfire

The r4 contract was re-read against `PROCESS.md`, `REQUIREMENTS.md`, `NOVELTY_GATE.md`, the adversarial N0 record, and its existing pre-merge audit. No new code change is introduced here.

The important safeguards remain:

- the no-evidence baseline contains no statement such as “no cue was observed”;
- weak support, likelihood direction, support under completeness, strong support, strong>weak diagnosticity, and neutral non-diagnosticity are capability-gated;
- strong evidence must move belief and consequential action in the normatively correct direction;
- target-support and other-support reversals must both occur, with the natural bidirectional scenario treated as one unit;
- pragmatic-completeness and matched-length controls must preserve a true sign reversal;
- hypotheses must form an exclusive and exhaustive binary partition before normalized binary preference is used as a posterior-odds readout.

The existing `VALIDATION_AUDIT_006_007.md` remains the detailed r4 implementation record.

## 012 — Source-Discount Recovery

### Scientific bugs found during this audit

#### 1. Overall source accuracy is not sufficient evidence direction gold

An early design attempted to use an above-chance source reliability scalar to justify that a low-credibility message remained positive evidence. This is not generally valid when source errors are asymmetric.

The frozen r1 D0 schema now requires independently audited directional likelihood ratios:

```text
1 < low_target_lr < high_target_lr
0 < high_other_lr < low_other_lr < 1
```

The source reliability scalars remain credibility metadata only. The visible calibration must be manually audited against the stored LRs.

#### 2. Below-chance sources are invalid

A source with reliability below 0.5 can make discount or even reversal rational. D0 therefore rejects any record unless:

```text
0.5 < low_source_reliability < high_source_reliability < 1
```

This prevents a normatively correct response to an adversarial source from being mislabeled as the target phenomenon.

#### 3. The high-vs-low capability probe must not name the answer

An early probe called the alternatives “LOW-RELIABILITY VERSION” and “HIGH-RELIABILITY VERSION”. That leaks the relation being tested. The final prompt shows source identities and their audited profiles without those meta-labels, then asks the model to infer which version is more diagnostic.

#### 4. Delay recovery must not be ordinary forgetting

The final memory gate covers **both short and long delay** and both source conditions. Source identity, message direction, and relative source credibility all have to remain accessible. A long-delay result cannot enter the denominator if an intermediate memory checkpoint fails.

#### 5. Gap shrink alone is not enough

A shrinking high-vs-low gap could occur because the high-source signal degrades. The strong signature therefore also requires:

- both low- and high-source messages initially move belief/action in the correct direction;
- an immediate discount gap exists;
- low-source influence rebounds;
- high-source influence remains substantially retained;
- same-delay no-message baselines control generic context drift.

#### 6. Source-cue rescue must be selective

The long-delay source-metadata reminder may name the source and its credibility record but may not repeat the message. It is compared against an approximately length-matched, semantically inert reminder. A generic reminder effect cannot satisfy reinstatement.

### Statistical contract

Target- and other-support directions are sign-normalized and must both pass. Belief/action are co-primary. The natural scenario, not the two directions or prompt variants, is the bootstrap unit.

### Offline verification

`14` tests pass. They include full result-matrix integration tests showing:

- an injected source-discount-recovery + selective-reinstatement signature reaches `PASS-TO-PANEL` under a one-case test config;
- normal stable source discount with no recovery yields `HARD-KILL-NO-SOURCE-DISCOUNT-RECOVERY`;
- short-delay source-memory failure yields `HARD-KILL-SOURCE-MEMORY-CAPABILITY-FLOOR`;
- below-chance reliability, invalid directional LR, message-repeating reinstatement, generic high-source decay, and non-selective matched-length rescue are rejected or held;
- authorization is checked before data/model construction.

These fixtures validate code paths only and are not behavioral evidence.

## 013 — Publicness–Coordination Dissociation

### Scientific bugs found during this audit

#### 1. Policy-gold leakage was removed

An early design risked placing `policy_gold_text` in the model-visible context. That would turn a natural coordination question into explicit rule following. In r1, `policy_gold_text` exists only for D0/manual audit and is never referenced by prompt construction. Tests enforce this separation.

#### 2. First-order knowledge is not enough to claim a use failure

If a model merely knows that both agents received the proposition but cannot derive public-event higher-order consequences, a coordination failure is ordinary ToM/public-announcement failure.

The capability gate now checks, from **both participant perspectives** and in both answer orders:

- self knows the proposition;
- the other participant knows it in the described world;
- whether the event was mutually observable;
- whether self can know the other received it;
- whether self can know the other knows self received it;
- one additional recursive receipt-knowledge level.

Only capability-correct cases can test representation-to-policy use.

#### 3. Explicit common knowledge is a bridge, not a policy instruction

`explicit_ck` states the epistemic consequence but never says which action is correct. A substantial coordination shift under this bridge is required before a weak natural-public shift can count as a dissociation. Otherwise the case is at a coordination-policy capability floor.

#### 4. Control baselines are triplet-matched

Primary, paraphrase, and length-control versions each contain their own matched:

```text
private / public / explicit_ck
```

triplet. This prevents a control from borrowing a different private baseline or a differently framed explicit-CK upper bound.

#### 5. Participant perspectives are correlated, not independent samples

Both participant roles must satisfy the signature, but their measurements are combined into one natural scenario. Material participant asymmetry is a hold condition, not extra sample size.

### Target statistic

For each participant and each control version:

```text
ck_gain      = P(coordinate | explicit_ck) - P(coordinate | private)
public_gain  = P(coordinate | public)      - P(coordinate | private)
dissociation = ck_gain - public_gain
public_use_ratio = public_gain / ck_gain
```

A target case requires a strong explicit-CK gain, a substantial dissociation, and a small public-use ratio after the recursive epistemic capability gate has passed.

### D0 validity requirement

The public event may only be used if the external task/information structure genuinely licenses the relevant common-knowledge operator. Public/private labels alone are not sufficient. D0 must also independently establish the relative coordination-policy direction and participant/payoff symmetry.

### Offline verification

`14` tests pass. Full-matrix integration tests show:

- an injected `publicness represented -> explicit CK used -> natural publicness underused` signature reaches `PASS-TO-PANEL` under a one-case test config;
- normal use of publicness close to the explicit-CK bridge yields `HARD-KILL-NO-PUBLICNESS-COORDINATION-DISSOCIATION`;
- recursive-ToM failure yields `HARD-KILL-PUBLICNESS-TOM-CAPABILITY-FLOOR`;
- an explicit-CK action floor, paraphrase/length artifact, policy-gold leakage, and length mismatch cannot produce a strong case;
- authorization is checked before data/model construction.

Again, these synthetic matrices test the harness, not the scientific phenomenon.

## What remains deliberately undone

All three projects still require the repository's scientific gates before a model call:

1. independent N0 reviewer and full-text/citation-chain refresh;
2. external data/version/license/gold resolution;
3. at least 20 randomly sampled D0 rows manually audited and recorded;
4. registry update to `n0_verdict: PASS`, `d0_verdict: PASS`, and `validation_authorized: true`;
5. only then a frozen 30–50 scenario × two-family smoke.

A failure at any earlier gate stops the project. Harness completeness is not a reason to authorize validation.
