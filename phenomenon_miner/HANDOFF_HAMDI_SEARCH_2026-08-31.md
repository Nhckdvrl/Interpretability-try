# Hamdi-Style Topic Search — Current Handoff

Date: 2026-08-31  
Status: **AUTHORITATIVE CURRENT STATE**

```yaml
PASS_REGISTER: 3
counts_toward_target_five: 3
MI_authorized_for_new_topics:
  - ETR-human-like-fallacy
  - spatial-reference-frame
  - spontaneous-deception-knowledge-action
latest_registration: spontaneous deception knowledge-action audit
latest_execution_fact: NTSB frontier KILL-S0 / RELEVANCE-ALSO-FAILS
```

Current target progress: **3/5 true PASS-REGISTER**.

## Mandatory reads

Only:
1. root [`README.md`](../README.md)
2. [`FINDING_RULES.md`](FINDING_RULES.md)
3. this file

Old gates/addenda/domain logs are cold evidence. Search `rejected_candidates/` semantically only after a concrete mother-card exists.

## Registered 01 — Human-Like Fallacies

Card: [`REGISTERED_ETR_HUMAN_LIKE_FALLACY_MECHANISM_2026-08-31.md`](REGISTERED_ETR_HUMAN_LIKE_FALLACY_MECHANISM_2026-08-31.md)

Mother: ICLR 2026 **Theory-Grounded Evaluation of Human-Like Fallacy Patterns in LLM Reasoning**. Existing open-model phenotype + premise-reversal rescue; mother leaves mechanism open. Competing mechanisms: premature alternative filtering vs semantic/prior contamination vs late output imitation. Core test: **alternative reinstatement patch**.

## Registered 02 — Spatial Reference-Frame Transformation

Card: [`REGISTERED_SPATIAL_REFERENCE_FRAME_TRANSFORMATION_2026-08-31.md`](REGISTERED_SPATIAL_REFERENCE_FRAME_TRANSFORMATION_2026-08-31.md)

Mechanistic mother: ICLR 2026 **Linear Mechanisms for Spatiotemporal Reasoning in Vision Language Models**. Behavioral mother: ICLR 2025 Oral **COMFORT**. Existing image-plane x/y IDs + existing FoR gap on overlapping LLaVA checkpoints. Competing mechanisms: late linguistic remap vs explicit coordinate transform vs multiple frame codes + selector.

## Registered 03 — Spontaneous Deception: Knowledge or Corrupted Reasoning?

Card: [`REGISTERED_SPONTANEOUS_DECEPTION_KNOWLEDGE_ACTION_2026-08-31.md`](REGISTERED_SPONTANEOUS_DECEPTION_KNOWLEDGE_ACTION_2026-08-31.md)

Mother: ICLR 2026 Oral **Beyond Prompt-Induced Lies: Investigating LLM Deception on Benign Prompts**.

Why registered:
- exact benign hard-wrong/easy-follow-up-correct phenotype is already established;
- official repo exposes item-level outputs for Llama, Mistral, Qwen, Gemma and local hidden-state extraction tooling;
- the mother interprets matched behavior as evidence of what the model internally believes, but does not causally establish that the hard deceptive run contains the correct belief;
- competing causal accounts are genuine knowledge-action dissociation vs reasoning-state corruption vs competing correct/fabricated trajectories;
- decisive interventions are missing-edge/reachability-state tracing, matched easy/truthful→hard-deceptive patching, and **edge-state reinstatement**;
- a negative result is scientifically strong because it would reclassify a central ICLR Oral deception construct rather than merely fail to find a feature.

This is Route B: no new behavior-discovery G0.

## Current unregistered survivor

### Individual belief lookbacks -> common ground

Mechanistic mother: ICLR 2026 **Language Models Use Lookbacks to Track Beliefs**. Natural substrate: Findings ACL 2024 **Common-ToM**.

Private belief and common-ground labels coexist naturally on the same dialogue events; no direct causal work found on distinct public-state code vs recursive individual-belief retrieval. Blocker: Lookbacks circuit is on Llama-3-70B/405B while published Common-ToM does not report those checkpoints. Keep HOLD until a cheap/public same-checkpoint capability bridge exists. Do not launch expensive multi-family behavior-discovery G0.

## Current priority mother audits for 04/05

### Temporal forgetting of reasoning

Mother: ACL 2026 **Temporal Sampling for Forgotten Reasoning in LLMs**.

Established anomaly: during reasoning fine-tuning, the same problem can transition from correct at an earlier checkpoint to wrong later; phenomenon is reported across model sizes, RL/SFT, and multiple reasoning benchmarks. Official repo releases Qwen2.5-7B training checkpoints and 64-response-per-checkpoint artifacts.

Allowed question is NOT generic catastrophic forgetting. Audit whether the same-item correct→wrong transition reflects **circuit/representation erasure**, **persistent computation with changed readout/control**, or **coexisting solution trajectories whose competition shifts during training**. Must survive direct collision with 2026 mechanistic catastrophic-forgetting and reasoning-circuit work.

### Opposite-scaling contextual entrainment

Behavior mother: Findings ACL 2026 **Better and Worse with Scale: How Contextual Entrainment Diverges with Model Size**. Mechanistic predecessor: ACL 2025 Outstanding Paper **Llama See, Llama Do**.

Established anomaly: increasing scale makes models more resistant to semantic misinformation while more prone to mechanical copying of arbitrary/nonsemantic context. A 2025 mechanistic paper already identifies entrainment heads, so generic entrainment localization is F2.

Only viable new question: what causal decomposition makes semantic filtering and mechanical copying scale in opposite directions — a shared entrainment writer plus a scaling semantic gate, two distinct circuits, or changing competition with memory/context heads? Must survive direct head-overlap/scaling-neighbor audit before registration.

## Recent serious deaths

All have individual rejection records. In addition to prior F1–F7 deaths:
- Preference Heads -> preference intensity — F3 exact-object mismatch;
- training recency × source reliability — F3 manufactured factorial substrate;
- The Reasoning Trap -> tool-hallucination mechanism — F2 because mother already performs internal representation-collapse analysis.

Every new serious death must be logged immediately with semantic aliases.

## Search constraints

- Remaining topics should preferably be **LLM, not VLM**.
- Mother first; no free-association `X != Y` axes.
- Prioritize established open-model anomalies whose causal explanation is unresolved.
- No central LLM judge.
- No synthetic 2×2 manufactured for the title.
- No fresh expensive G0 merely to discover whether a guessed behavior exists.
- No resurrection via dataset/model/language/prompt/subset/MI-method rename.
- HOLD/PRE-S0/frontier/under-audit do not count toward five.

> **Find two more unanswered causal computations of already-established LLM scientific objects.**
