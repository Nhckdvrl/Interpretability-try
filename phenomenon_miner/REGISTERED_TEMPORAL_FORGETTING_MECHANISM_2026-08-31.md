# PASS-REGISTER 04 — What Does Reasoning Training Forget?

Date: 2026-08-31  
Status: **PASS-REGISTER**  
Route: **B — established anomaly -> unasked causal computation**

## Natural question

When a reasoning model solves the same problem correctly at one training checkpoint and incorrectly at a later checkpoint, **what was actually lost?**

Did fine-tuning destroy an upstream comprehension/knowledge representation, damage the reasoning computation itself, or leave the correct computation available while changing which trajectory/readout controls the answer?

## Mother

Li et al., **Temporal Sampling for Forgotten Reasoning in LLMs**, ACL 2026 Long Paper.

The mother establishes **Temporal Forgetting**: during RL/SFT reasoning post-training, individual benchmark questions frequently transition from correct to incorrect even while aggregate benchmark performance improves. It explicitly distinguishes this from conventional catastrophic forgetting, which concerns cross-domain/global capability degradation.

The mother reports Temporal Forgetting Scores of 6.4%–56.1% across Qwen2.5 sizes, GRPO/SFT, and multiple reasoning benchmarks; free-form TheoremQA also shows >20% temporal forgetting. It uses greedy decoding for the core forgetting measurements to minimize random sampling fluctuations.

The mother proposes a behavioral **capability-shift hypothesis**: reasoning-oriented errors decrease while understanding/knowledge-type errors increase after RL. That analysis is output-level and uses an automated error-type judge; it does not establish which internal computation changes when a specific item flips from correct to wrong.

## Why this is not a behavior lottery

- The exact same-item `correct -> wrong` transitions are already the mother’s primary measured object.
- Core measurements use greedy decoding, so registration is not based on a one-off stochastic sample.
- The mother shows repeated oscillations across adjacent checkpoints and distinguishes them from ordinary cross-task catastrophic forgetting.
- The official repository releases eight Qwen2.5-7B RL checkpoints and per-checkpoint response artifacts; 64-response checkpoint artifacts are also available for additional robustness analyses.

No fresh multi-family G0 is needed to discover the phenomenon.

## Exact scientific object

The statistical unit is a **single reasoning item tracked through an ordered sequence of checkpoints of the same model architecture**.

This gives unusually clean matched causal pairs:

- `C -> W`: correct at checkpoint t, wrong at t+1 (Forget)
- `W -> C`: wrong at t, correct at t+1 (Improve)
- `C -> C`: retained-correct control
- `W -> W`: persistent-wrong control

The same prompt/tokenization and architecture are held fixed; only learned parameters change along the real training trajectory.

## Competing causal hypotheses

### H1 — Upstream capability erosion

Reasoning post-training corrupts a representation needed to understand the question or retrieve required knowledge. The later model therefore never constructs the same usable problem state as the earlier correct checkpoint.

Prediction: rescue should require transplanting early/middle computation from the previous correct checkpoint; late answer-layer restoration alone should fail.

### H2 — Reasoning-circuit disruption

Problem understanding remains intact, but a middle reasoning computation / algorithmic trajectory is changed or lost.

Prediction: early states remain equivalent while a localized middle-stage checkpoint transplant restores the solution.

### H3 — Persistent solution, changed control/readout

The later checkpoint still computes or retains the correct solution state, but post-training changes competition, control, or answer writing so a different trajectory wins.

Prediction: correct-answer information remains causally available late in the forgotten model; a late localized transplant or control intervention can restore output without reinstating the earlier full reasoning computation.

### H4 — Distributed parameter interference

There is no compact forgotten component: many small changes jointly alter the trajectory.

Prediction: no localized transplant produces selective rescue, and rescue scales diffusely with swapped depth/parameter mass.

## Core causal primitive — checkpoint layer transplantation

Because adjacent checkpoints share the exact architecture, use **hybrid checkpoint interventions** rather than relying only on probes.

For each matched `C -> W` item:

1. Take later wrong checkpoint `M_{t+1}` as recipient.
2. Replace a layer/block or contiguous block range with the corresponding weights from earlier correct checkpoint `M_t`.
3. Binary-search / path-localize the minimum transplanted component that restores the exact deterministic answer.
4. Perform the reverse transplant (`M_{t+1}` -> `M_t`) to test whether the same component causally induces forgetting.
5. Compare against `C -> C`, `W -> C`, `W -> W`, random-layer, and equal-norm weight-delta controls.

After locating a causal stage, activation patching on the same prompt can distinguish whether the restored object is question state, intermediate reasoning state, or answer/readout state.

## Strong fatal controls

- Use deterministic answer scoring on math/reasoning tasks; do not use a central LLM judge to define the core phenotype.
- Use greedy-decoding mother trajectories for primary `C/W` labels.
- Require bidirectional causal evidence where feasible: early->late rescue plus late->early degradation.
- Control checkpoint transplant size and parameter-delta norm; arbitrary old layers should not rescue selectively.
- Measure effects on retained-correct items so a transplant that merely makes the model more like an old checkpoint globally is not mistaken for a forgetting mechanism.
- Treat activation similarity/probe accuracy as descriptive until a transplant or intervention changes behavior.

## Strongest-neighbor audit

Mechanistic catastrophic-forgetting work in 2026 studies retention of **previous tasks/base capabilities after adaptation to a new task**, including circuit preservation and representational drift under RL vs SFT. That is an important neighbor but not the same scientific object.

The ACL mother explicitly separates Temporal Forgetting from catastrophic forgetting: Temporal Forgetting is **in-domain, item-level, and occurs despite improving aggregate performance**.

Generic reasoning-circuit and correct-vs-error-head papers likewise do not study how the same item’s causal computation changes across real adjacent training checkpoints.

Therefore the topic must stay focused on the mother-defined temporal transition, not be renamed as generic catastrophic forgetting.

## Anti-narrowing / paper narrative

The wide question is:

> **Does reasoning post-training actually erase capabilities, or does it continually re-route which capabilities control individual answers?**

This matters for RL/SFT stability, checkpoint selection, reasoning specialization, model merging, capability evaluation, and why a final checkpoint is not necessarily a monotonic improvement over its own training history.

A null/localized/distributed result is still informative:
- early/mid erosion would mechanistically validate the mother’s capability-shift story;
- late control/readout change would show “forgotten” reasoning remains latent in the final model;
- diffuse interference would connect item-level temporal forgetting to distributed optimization dynamics while preserving its distinct in-domain formulation.

## Registration decision

**PASS-REGISTER.**

Reason: strong ACL mother + deterministic pre-established within-item anomaly + public real training checkpoints + direct mother-stated but unverified causal explanation + uniquely clean matched checkpoint intervention + strongest neighbors address a different cross-task forgetting object.
