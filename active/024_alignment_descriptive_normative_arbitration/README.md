# 024 — What Does Alignment Change: Descriptive Social Models or Normative Readout?

**Status:** `HOLD-INCONCLUSIVE-D0 / MECHANISM-NOT-AUTHORIZED`
**Created:** 2026-08-31  
**Selection route:** Hamdi-style mother-paper extension  
**Priority:** high new-candidate priority, behind established 014 and current 018 redesign until behavioral reproduction is frozen.

## 1. The question in plain language

> Aligned models often answer as people *should* behave rather than as people *actually do* behave. Did alignment make the model forget/distort how humans really behave, or does that descriptive human model remain inside while a normative signal wins at the output?

A simple example:

> In a repeated bargaining game, someone who was treated unfairly often retaliates. The model may know that retaliation is likely while also judging cooperation or fairness to be preferable. After instruction tuning / preference alignment, which internal object changed?

This question is meaningful without a benchmark, probe, SAE or intervention. The descriptive-vs-normative distinction is foundational in behavioral science; the AI-specific question is what post-training does to those two targets internally.

## 2. Why this is a Hamdi-style extension

The mother paper gives us a real, high-value behavioral object instead of asking us to gamble on a new failure.

**Alignment Makes Language Models Normative, Not Descriptive** (2026) reports a large base-vs-aligned reversal on real human decisions:

- 120 same-provider base/aligned model pairs;
- >10,000 real human decisions;
- multi-round bargaining, persuasion, negotiation and repeated games;
- base models frequently predict observed human actions better in complex strategic settings;
- aligned models do better where behavior is closer to simple normative predictions.

Reference: https://arxiv.org/abs/2603.17218

The paper establishes **what changes behaviorally**. We ask the adjacent mechanistic question:

> **What changed internally?**

That is the same productive shape as:

```text
behavioral mother object
→ internal scientific object
→ causal role
→ mechanism-predicted intervention
```

rather than inventing a new benchmark-specific failure.

## 3. Strongest neighbors and novelty boundary

### 3.1 A Theory of Response Sampling in LLMs: Part Descriptive and Part Prescriptive — ACL 2025 Main

This paper is the strongest collision neighbor. It already argues that model sampling is influenced by both:

- descriptive/statistical norms;
- prescriptive/ideal norms.

It tests pretrained and instruction-tuned Llama variants and reports stronger prescriptive influence for RLHF/instruction-tuned models.

Therefore **we cannot claim**:

- first evidence that LLMs combine descriptive and prescriptive information;
- first evidence that RLHF increases prescriptive influence;
- first descriptive-vs-normative behavioral distinction.

Reference: https://aclanthology.org/2025.acl-long.1454/

What remains open is the model-internal transformation responsible for the behavioral trade-off. The ACL paper itself leaves the origin/mechanism of the prescriptive component unresolved.

### 3.2 What Do Large Language Models Know About Opinions? — ICLR 2026

This work shows that models can internally encode human/group opinions better than their final answers reveal, identifies middle-layer social information and late bottlenecks, and uses causal steering.

Therefore **generic `the model knows social information but does not output it` is not novel**.

Our contribution must require two independently defined targets on the same situation:

```text
D(s) = descriptive target: what humans actually do
N(s) = normative target: what they should / ideally / equilibrium-rationally do
```

and paired base→aligned model comparison.

### 3.3 Moral-rightness / predicted-human / model-decision work

Recent relational moral-dilemma work explicitly separates moral rightness, predicted human behavior and the model's own decision. This strengthens the naturalness/existence prior but also means we cannot present the three-way behavioral distinction itself as new.

The novelty is what alignment does to the **internal representations and arbitration** of these targets.

## 4. Exact claim allowed after N0

Allowed working claim:

> **Post-training changes how descriptive human-behavior knowledge and normative policy signals are represented and/or arbitrated; we will distinguish descriptive-model degradation from dual-state retention and late normative readout.**

Not allowed:

- `LLMs contain descriptive and normative information`;
- `alignment makes models more normative`;
- `models know human opinions internally`;
- generic `knowledge exists but output ignores it`.

Those are mother/neighbor claims.

## 5. Competing mechanisms

The project is worthwhile because the mother behavior has at least three genuinely different internal explanations.

### H1 — Descriptive-model degradation

Alignment damages or distorts the internal model of observed human behavior.

Predictions:

- human-action information becomes less linearly/nonlinearly recoverable before the output layer;
- aligned representations move away from empirical human distributions even when the prompt explicitly asks for prediction;
- importing base-model descriptive state should improve prediction.

Interpretation:

> alignment changes stored/computed social knowledge itself.

### H2 — Descriptive model retained, normative state strengthened

The aligned model still represents likely human behavior but develops/strengthens a second normative signal.

Predictions:

- descriptive decodability remains similar across base/aligned models;
- normative target decodability grows or appears more strongly in aligned models;
- the two signals are at least partially separable.

Interpretation:

> alignment adds/reweights a second target rather than erasing the first.

### H3 — Late arbitration / readout change

Both descriptive and normative information are already present, but alignment changes which signal controls the answer.

Predictions:

- early/middle descriptive representations remain largely intact;
- base/aligned divergence is concentrated late;
- a selective late intervention can recover human-behavior prediction without globally undoing instruction following or safety.

Interpretation:

> the model still knows what people do; alignment changes policy/readout.

These mechanisms imply different scientific conclusions and different interventions, so MI is not decorative.

## 6. Data philosophy

**Do not invent synthetic social situations just because they produce clean labels.**

The first dataset should reuse real human-decision distributions from the mother paper or another public behavioral-science source with:

- real observed choices;
- the same decision state available to the model;
- a separately defined normative target where possible;
- repeated/strategic settings where descriptive and normative predictions naturally diverge.

The important population is not a rare filtered subset. It is the ordinary region of behavioral science where empirical behavior departs from normative theory.

Preferred source families:

- repeated matrix games;
- bargaining / ultimatum-like repeated interactions;
- persuasion / negotiation datasets with human next actions;
- other public experiments used by the mother paper, if licensing permits redistribution.

## 7. Behavioral reproduction before MI

Before any hidden-state experiment, reproduce a narrow version of the mother effect on at least one accessible open-weight base/aligned pair.

Required comparison:

```text
same state s
base model predicts human next action
aligned counterpart predicts human next action
```

and, where a normative target is available:

```text
model prediction distance to D_human(s)
model prediction distance to N(s)
```

### Minimum reproduction gate

Do not freeze exact numbers until source data and model pair are audited, but the gate must require:

1. base/aligned are truly paired or sufficiently architecture/training-matched to make the comparison meaningful;
2. the descriptive-vs-normative behavioral shift is visible without prompt shopping;
3. the effect holds on a substantial natural population, not a hand-selected scenario type;
4. the normative target is independently defined rather than generated by the same model being analyzed.

If this mother behavior cannot be reproduced on accessible open models, `HOLD_NO_OPEN_MODEL_OBJECT`; do not manufacture it with a synthetic game.

## 8. Mechanistic program

Only after the behavioral object passes.

### M1 — Separate target readouts

For the same states, construct readouts for:

- empirical human-action target;
- normative target.

The goal is not probe leaderboard performance. The goal is to establish whether base/aligned trajectories differ in **which target is represented where**.

### M2 — Base→aligned fate analysis

Track representational change across layers/checkpoints if paired artifacts exist:

```text
descriptive information fate
normative information fate
final action/logit trajectory
```

The decisive result is a qualitative distinction among H1/H2/H3, not a single layer with high AUC.

### M3 — Causal interchange

If a layer/subspace carrying descriptive or normative state is identified, perform selective interchange/steering:

- aligned ← base descriptive state;
- base/aligned normative-state interventions;
- unrelated-task controls;
- output-format / general-capability controls.

A valid intervention should shift human-behavior prediction in the predicted direction without merely making the model less aligned or more random.

### M4 — Mechanism-derived intervention

The best paper ending would be a mechanism-informed switch for simulation use:

> retain normal aligned assistant behavior by default, but when asked to forecast human behavior, route the retained descriptive social model rather than the normative policy.

This is scientifically meaningful only if the mechanism predicts the intervention.

## 9. Hard kill / route rules

- `KILL_MOTHER_NOT_REPRODUCED`: accessible paired models do not show the behavioral alignment trade-off.
- `KILL_GENERIC_SOCIAL_DECODABILITY`: only finding is internal human-behavior information > output accuracy.
- `ROUTE_ACL2025_SAMPLING`: result reduces to a descriptive/prescriptive output mixture coefficient.
- `KILL_NO_SEPARATE_TARGETS`: normative and descriptive targets cannot be independently defined on the same states.
- `KILL_NO_ALIGNMENT_FATE`: hidden-state differences do not explain the paired base/aligned behavioral shift.
- `KILL_CAUSAL_FAILURE`: a purported descriptive/normative representation is decodable but selective intervention has no predicted effect.
- `KILL_NO_GENERALIZATION`: mechanism appears only in one tiny game or one prompt wording.

## 10. N0 verdict

```yaml
natural_question_gate: PASS
mother_inclusion_n0: PASS_SHARPENED
behavioral_mother_exists: true
novelty_claim: alignment-induced internal fate/arbitration of descriptive vs normative social targets
screening_authorized: false
mechanism_authorized: false
```

The source/data audit and open-model mother-reproduction contract are now
frozen in [`SOURCE_AUDIT.md`](SOURCE_AUDIT.md),
[`D0_PREFLIGHT.md`](D0_PREFLIGHT.md), and
[`configs/d0_contract.json`](configs/d0_contract.json). Only deterministic D0
behavioral scoring has been completed and adjudicated in
[`D0_REPORT.md`](D0_REPORT.md). The frozen verdict is
`HOLD_INCONCLUSIVE_D0`: two of four families pass rather than the required
three. No further behavioral or mechanistic call is authorized under D0 v1.

Full N0: [`../../phenomenon_miner/HAMDI_AXIS_N0_2026-08-31.md`](../../phenomenon_miner/HAMDI_AXIS_N0_2026-08-31.md).
