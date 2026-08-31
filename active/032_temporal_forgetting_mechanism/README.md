# 032 — What Does Reasoning Training Forget?

Status: **ACTIVE / PASS-REGISTER / V0 PROVENANCE PINNED — GREEDY OUTPUTS NOT YET INGESTED**

Route: **Hamdi Route B — established anomaly → unasked causal computation**  
Canonical registration: [`../../phenomenon_miner/REGISTERED_TEMPORAL_FORGETTING_MECHANISM_2026-08-31.md`](../../phenomenon_miner/REGISTERED_TEMPORAL_FORGETTING_MECHANISM_2026-08-31.md)

## 1. One-sentence question

When the same reasoning problem is solved correctly by one training checkpoint and incorrectly by a later checkpoint—even while aggregate benchmark performance improves—what exactly did training remove or reroute inside the model?

## 2. Background and mother result

Mother: **Temporal Sampling for Forgotten Reasoning in LLMs** (Li et al., ACL 2026 Long Paper).

The mother establishes **Temporal Forgetting**, an item-level, in-domain phenomenon distinct from classical catastrophic forgetting.

Key established facts:

- the same reasoning item can transition `correct -> wrong` at a later checkpoint;
- items can oscillate across a real training trajectory rather than degrade monotonically;
- the effect appears across model sizes, RL and SFT, and multiple reasoning benchmarks;
- core forgetting measurements use **greedy decoding**, reducing the chance that the effect is merely sampling noise;
- aggregate benchmark performance can still improve while individual problems are forgotten;
- the official repository releases eight Qwen2.5-7B RL checkpoints and per-checkpoint response artifacts, plus 64-sample response bundles for robustness analyses.

The mother proposes a behavioral **capability-shift hypothesis**: reasoning-oriented errors may decrease while understanding/knowledge-type errors increase. But that claim is based on output-level error categorization and does not identify which internal computation changes when a particular item flips from correct to wrong.

## 3. Scientific question and competing mechanisms

### H1 — Upstream capability erosion

Post-training corrupts problem understanding, retrieval or prerequisite knowledge. The later model never constructs the same useful problem state as the earlier correct checkpoint.

Prediction:
- early/middle checkpoint transplantation is needed for rescue;
- late answer-layer restoration alone is insufficient.

### H2 — Reasoning-circuit disruption

Problem representation survives, but the middle computation that transforms it into a solution is damaged or rerouted.

Prediction:
- early states remain similar across checkpoints;
- a localized middle-block transplant can restore the earlier solution.

### H3 — Persistent solution, changed control/readout

The later checkpoint still computes or stores the correct solution, but a changed control/readout process causes another trajectory to win.

Prediction:
- correct-answer / correct-solution information remains causally accessible late in the forgotten checkpoint;
- a late localized intervention rescues output without restoring the full earlier computation.

### H4 — Distributed parameter interference

There is no compact forgotten circuit. Many small parameter changes jointly reshape the trajectory.

Prediction:
- no localized block has a strong selective rescue effect;
- rescue grows diffusely with transplanted depth/parameter mass.

## 4. Data and artifacts

Official repository: `uw-nsl/Temporal_Forgetting`.

Primary inherited resources:

- eight Qwen2.5-7B RL checkpoints at regular training intervals;
- AIME24, AIME25 and AMC sampling/evaluation artifacts;
- lm-evaluation-harness integration for AIME/AMC/Olympiad/MATH-500-style tasks;
- greedy-decoding trajectory measurements reported by the mother;
- 64-response-per-checkpoint artifacts for secondary stochastic robustness analysis.

Primary statistical unit:

> **same reasoning item × two adjacent checkpoints of the same architecture**

Frozen transition cells:

- `C -> W`: correct at checkpoint `t`, wrong at `t+1` (**Forget**);
- `W -> C`: wrong then correct (**Improve**);
- `C -> C`: retained correct;
- `W -> W`: persistent wrong.

This matched design is unusually clean because prompt, tokenizer and architecture are fixed; the real training update is the treatment.

## 5. Initial validation model/data scope

Do **not** begin with new model families. The mother already establishes existence broadly.

Primary mechanism model:

- the released **Qwen2.5-7B RL checkpoint trajectory**.

Initial task order:

1. one benchmark with the cleanest deterministic scoring and enough `C -> W` transitions;
2. a second mother benchmark for replication;
3. only later test SFT or another model size if checkpoint artifacts are available.

Core correctness should use exact/rule-based math answer matching wherever possible. Do not make an LLM judge part of the primary transition definition.

## 6. Initial validation plan

### V0 — Reconstruct the checkpoint transition matrix

Goal: reproduce the mother's exact item-level object before any mechanistic analysis.

Steps:

1. Pin all eight released Qwen2.5-7B checkpoints by immutable revision/hash.
2. Pin task versions and prompts.
3. Re-run or ingest the mother's greedy-decoding outputs.
4. Compute per-item correctness for every checkpoint.
5. Build the full temporal sequence, e.g. `C C W W C ...`, for every item.
6. Extract adjacent transition tables `C->W`, `W->C`, `C->C`, `W->W`.
7. Verify the mother Temporal Forgetting rate on the chosen task.
8. Freeze matched item IDs before parameter/activation inspection.

**Stop condition:** if greedy transition labels cannot be reproduced from released checkpoints, resolve provenance before MI.

### V1 — Cheap parameter-delta audit

Goal: characterize training change without making a mechanistic claim.

For each adjacent checkpoint pair:

1. compute per-layer / module parameter-delta norms;
2. normalize by baseline parameter norm;
3. identify unusually changed blocks, attention modules, MLPs and output/readout components;
4. compare checkpoint pairs with high vs low forgetting counts.

This is only a prioritization tool. Large parameter change does not prove causal forgetting.

### V2 — Whole-block checkpoint transplantation screen

This is the central first causal experiment.

For each selected `C -> W` adjacent pair:

1. treat later wrong checkpoint `M_{t+1}` as recipient;
2. replace one full transformer block at a time with the corresponding block from earlier correct checkpoint `M_t`;
3. run the frozen `C->W` item set under greedy decoding;
4. measure selective rescue rate;
5. run the same hybrid models on `C->C`, `W->C` and `W->W` controls;
6. perform reverse transplantation (`M_{t+1}` block into `M_t`) and test whether it induces degradation;
7. normalize effects by transplanted parameter count and checkpoint delta norm.

A useful block should rescue forgotten items **more than retained-correct controls are perturbed**.

### V3 — Contiguous-window / binary-search localization

If single-block effects are weak or distributed:

1. transplant contiguous layer ranges;
2. binary-search the minimal window giving robust rescue;
3. compare early, middle and late windows with equal parameter mass;
4. repeat the reverse transplant;
5. test whether rescue is task-general or item-specific.

Interpretation:

- early window rescue → H1;
- middle localized rescue → H2;
- late window rescue → H3;
- only broad windows work → H4.

### V4 — Same-prompt activation patching across checkpoints

After locating a causal stage with weights:

1. run the identical forgotten prompt through earlier-correct and later-wrong checkpoints;
2. patch layer activations from early checkpoint into the later checkpoint at the localized stage;
3. compare token/position specificity;
4. reverse patch early checkpoint with late activations;
5. distinguish whether the transferred state corresponds to:
   - question representation;
   - retrieved knowledge;
   - intermediate reasoning state;
   - answer/control state.

Because the prompt is identical, cross-checkpoint activation patching avoids the alignment problems common in cross-example patching.

### V5 — Is the correct solution still latent?

To distinguish H3 from true capability loss:

1. measure correct-answer / intermediate-solution information in the later forgotten checkpoint using held-out, non-leaky readouts;
2. test whether that information is causally useful with targeted activation/route intervention;
3. compare forgotten `C->W` items against never-correct `W->W` controls.

The key distinction is not whether the correct answer is linearly decodable somewhere, but whether it can still **causally control** the output.

### V6 — Transition symmetry

A strong mechanism should explain both directions.

For the same localized block/pathway:

- does old→new transplantation rescue `C->W`?
- does new→old transplantation induce failure?
- on `W->C` transitions, does the newly learned component have the opposite causal effect?

This prevents us from mistaking generic checkpoint averaging for a forgetting mechanism.

## 7. Fatal controls

- Primary transition labels from greedy decoding / deterministic answer scoring.
- Same prompt and tokenizer across checkpoints.
- `C->C`, `W->C`, `W->W` matched controls.
- Reverse transplantation whenever feasible.
- Equal-size / equal-delta-norm transplant controls.
- Evaluate global regression: a hybrid model that simply becomes the old checkpoint everywhere is not a selective rescue.
- Do not interpret representation similarity or probe accuracy without behavioral intervention.
- Keep ordinary cross-task catastrophic forgetting literature separate from this in-domain item-level object.

## 8. Promote / kill criteria

### Promote if

- the mother deterministic transition population reproduces;
- a block/window/activation intervention selectively rescues `C->W` beyond control transitions;
- at least two causal hypotheses can be separated by stage-specific evidence.

### Strong outcomes even if H1 is false

- late rescue would show that apparently forgotten reasoning remains latent but loses control;
- distributed rescue would reveal that temporal forgetting is an optimization/interference phenomenon rather than a clean erased circuit.

### Kill / redesign if

- the `C->W` population is dominated by scoring/template instability;
- arbitrary old blocks rescue as well as candidate blocks after normalization;
- effects are explained entirely by global regression to the earlier checkpoint with no transition specificity.

## 9. Paper-level narrative

> **Does reasoning post-training actually erase capabilities, or does it continually re-route which capabilities control individual answers?**

This bears directly on RL/SFT stability, checkpoint selection, model merging, reasoning specialization, and the assumption that the final checkpoint monotonically contains everything earlier checkpoints knew how to do.
