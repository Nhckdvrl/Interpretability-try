# Hamdi-Style Topic Search — Current Handoff

Date: 2026-08-31  
Status: **AUTHORITATIVE CURRENT STATE**

```yaml
PASS_REGISTER: 5
counts_toward_target_five: 5
active_projects:
  - active/029_etr_human_like_fallacy
  - active/030_spatial_reference_frame_transformation
  - active/031_spontaneous_deception_knowledge_action
  - active/032_temporal_forgetting_mechanism
  - active/033_contextual_entrainment_opposite_scaling
MI_authorized_for_new_topics:
  - ETR-human-like-fallacy
  - spatial-reference-frame
  - spontaneous-deception-knowledge-action
  - temporal-forgetting-mechanism
  - contextual-entrainment-opposite-scaling
latest_registration: contextual entrainment opposite-scaling mechanism
latest_state_change: five PASS topics promoted into active execution plans
latest_terminal_execution: NTSB frontier KILL-S0 / RELEVANCE-ALSO-FAILS
```

**Target reached: 5/5 true PASS-REGISTER. All five now live in `active/` with detailed initial-validation plans.**

## Mandatory reads

Only:

1. root [`README.md`](../README.md)
2. [`FINDING_RULES.md`](FINDING_RULES.md)
3. this file

For execution, open [`../active/README.md`](../active/README.md) and then the chosen project's README. Historical gates/addenda/domain logs are cold evidence; search them only when a concrete semantic collision is relevant.

## Active 029 — Human-Like Fallacies

Execution plan: [`../active/029_etr_human_like_fallacy/README.md`](../active/029_etr_human_like_fallacy/README.md)

Mother: ICLR 2026 **Theory-Grounded Evaluation of Human-Like Fallacy Patterns in LLM Reasoning**.

Established object: 38-model ETR-predicted human-like fallacies plus a semantics-preserving premise-reversal rescue.

New causal question: **premature alternative filtering vs semantic/prior contamination vs late output imitation**.

Core validation sequence:

1. freeze formal PyETR/reversal pairs;
2. cheap mother phenotype replay on a confirmed open checkpoint;
3. derive alternative-state labels from the formal ETR state machine;
4. localize original-fallacy vs reversed-rescue divergence;
5. run **alternative reinstatement patch** with non-ETR wrong-answer controls.

## Active 030 — Spatial Reference-Frame Transformation

Execution plan: [`../active/030_spatial_reference_frame_transformation/README.md`](../active/030_spatial_reference_frame_transformation/README.md)

Mechanistic mother: ICLR 2026 **Linear Mechanisms for Spatiotemporal Reasoning in Vision Language Models**. Behavioral mother: ICLR 2025 Oral **COMFORT**.

Established object: explicit image-plane `x/y` spatial IDs + Camera/Addressee/Relatum FoR behavior on overlapping LLaVA checkpoints.

New causal question: **late linguistic remap vs explicit coordinate transform vs multiple frame codes + selector**.

Core validation sequence:

1. reproduce mother `x/y` spatial IDs;
2. replay COMFORT FoR phenotype on overlapping checkpoint;
3. trace frozen `x/y` geometry across FoR queries;
4. inject analytic geometry-derived FoR transforms;
5. patch query/selector state to distinguish transform from code selection.

## Active 031 — Spontaneous Deception: Knowledge or Corrupted Reasoning?

Execution plan: [`../active/031_spontaneous_deception_knowledge_action/README.md`](../active/031_spontaneous_deception_knowledge_action/README.md)

Mother: ICLR 2026 Oral **Beyond Prompt-Induced Lies**.

Established object: public Llama/Mistral/Qwen/Gemma hard-initial-wrong + matched-easy-follow-up-correct events on benign graph reasoning.

New causal question: **genuine knowledge-action dissociation vs reasoning-state corruption vs competing correct/fabricated trajectories**.

Core validation sequence:

1. reconstruct mother event population from official outputs with deterministic graph truth;
2. lock a stable local subset on one open checkpoint;
3. derive edge-existence/reachability state targets from the graph environment;
4. trace the first corrupted/fabricated state;
5. run **edge-state reinstatement** and separate upstream graph-state rescue from late answer-policy rescue.

## Active 032 — What Does Reasoning Training Forget?

Execution plan: [`../active/032_temporal_forgetting_mechanism/README.md`](../active/032_temporal_forgetting_mechanism/README.md)

Mother: ACL 2026 **Temporal Sampling for Forgotten Reasoning in LLMs**.

Established object: deterministic same-item `correct -> wrong` transitions across real reasoning-training checkpoints while aggregate performance improves.

New causal question: **upstream capability erosion vs reasoning-circuit disruption vs persistent solution with changed control/readout vs distributed interference**.

Core validation sequence:

1. reconstruct greedy per-item checkpoint trajectories on released Qwen2.5-7B checkpoints;
2. freeze `C->W`, `W->C`, `C->C`, `W->W` cells;
3. screen **checkpoint layer transplantation**;
4. localize minimal causal layer window and reverse transplant;
5. use same-prompt cross-checkpoint activation patching to identify what state was lost/rerouted.

## Active 033 — Why Bigger Models Ignore Lies but Copy Noise

Execution plan: [`../active/033_contextual_entrainment_opposite_scaling/README.md`](../active/033_contextual_entrainment_opposite_scaling/README.md)

Behavior mother: Findings ACL 2026 **Better and Worse with Scale**. Mechanistic predecessor: ACL 2025 Outstanding **Llama See, Llama Do**.

Established object: semantic contextual entrainment scales down with model size while non-semantic copying scales up, replicated on Pythia and Cerebras-GPT; generic entrainment heads are already known.

New causal question: **shared copying writer + scaling semantic gate vs distinct independently scaling circuits vs common upstream entrainment with late competition**.

Core validation sequence:

1. reproduce the exact mother `Delta_d` sign split;
2. reproduce generic ACL'25 entrainment causality on a reference Pythia size;
3. build normalized scale-conditioned causal profiles;
4. localize a semantic-selective gate with difference-in-differences intervention effects;
5. perform semantic-gate ablation + generic-writer ablation for a causal double dissociation / late-competition test.

## Shared execution rule

All five have passed topic selection, but none is allowed to skip validation.

```text
mother artifact freeze
→ exact matched population
→ cheap faithful replay
→ measurement validation
→ causal intervention
→ replication
→ paper-scale expansion
```

`ACTIVE` means **worth serious causal testing**, not “the preferred hypothesis is assumed true.” A strong null that changes the mother interpretation is acceptable. A construct or measurement failure must still be terminalized rather than rescued post hoc.

## Unregistered HOLD

### Individual belief lookbacks -> common ground

Mechanistic mother: ICLR 2026 **Language Models Use Lookbacks to Track Beliefs**; natural substrate: Findings ACL 2024 **Common-ToM**.

Still promising, but published same-checkpoint capability bridge is missing. It does **not** count toward five and must not be forced through with an expensive behavior-discovery G0.

## Negative-memory discipline

Every serious death remains logged in `rejected_candidates/` with semantic aliases. Do not revive dead ideas via dataset/model/language/prompt/subset/MI-method/title changes.

## What happens next

Discovery is complete. Do not generate more topics merely for quantity unless explicitly requested.

The next action is to choose an active project and execute its **V0/V1 only first**, freezing the exact mother population before any expensive causal work. Results must then determine whether to promote to deeper MI or stop.

## Hard constraints retained

- mother first;
- no central LLM judge for core phenotype when deterministic/formal scoring exists;
- no synthetic 2×2 manufactured for the title;
- no fresh expensive G0 whose purpose is merely discovering whether a guessed behavior exists;
- no post-hoc subset/threshold/prompt rescue;
- probe/readout evidence alone is never a mechanism claim;
- every serious death gets a short rejection record.

> **Five questions now pass the discovery bar; all five are active, but every one must still earn its mechanism through preregistered causal validation.**
