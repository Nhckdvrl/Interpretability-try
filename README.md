# Interpretability Topic Search

用于寻找、快速证伪、再解释 **LLM / VLM 的自然、反直觉、可机制化 scientific questions**。

```yaml
PASS_REGISTER: 5
counts_toward_target_five: 5
active_projects:
  - 029_etr_human_like_fallacy
  - 030_spatial_reference_frame_transformation
  - 031_spontaneous_deception_knowledge_action
  - 032_temporal_forgetting_mechanism
  - 033_contextual_entrainment_opposite_scaling
new_topic_MI_authorized:
  - ETR-human-like-fallacy
  - spatial-reference-frame
  - spontaneous-deception-knowledge-action
  - temporal-forgetting-mechanism
  - contextual-entrainment-opposite-scaling
latest_registration: contextual entrainment opposite-scaling mechanism
latest_terminal_execution: NTSB causal-role frontier KILL-S0
```

**Target reached: 5/5 true PASS-REGISTER. All five now have active execution plans.** HOLD / frontier / PRE-S0 不计入五题。

## 当前只认三份权威文件

1. [`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md) — 唯一选题协议
2. [`phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`](phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md) — 当前状态 / 下一步
3. 本 README — 仓库入口

执行入口：[`active/README.md`](active/README.md)。其它 gate/funnel/addendum/domain log 是冷证据；仅在新题语义接近时定向读取。一般失败经验见 [`phenomenon_miner/FAILED_TOPICS.md`](phenomenon_miner/FAILED_TOPICS.md)。

## 五个正式注册 + active 项目

### 01 Human-Like Fallacies: Alternative Filtering or Prior Contamination?

Mother: ICLR 2026 `Theory-Grounded Evaluation of Human-Like Fallacy Patterns in LLM Reasoning`。已知 open-model ETR fallacy + premise-reversal rescue；新机制：premature alternative filtering vs semantic/prior contamination vs late output imitation。核心：`alternative reinstatement patch`。

- Registration: [`REGISTERED_ETR_HUMAN_LIKE_FALLACY_MECHANISM_2026-08-31.md`](phenomenon_miner/REGISTERED_ETR_HUMAN_LIKE_FALLACY_MECHANISM_2026-08-31.md)
- Active plan: [`active/029_etr_human_like_fallacy/README.md`](active/029_etr_human_like_fallacy/README.md)

### 02 From Pixels to Perspectives: Reference-Frame Transformation in VLMs

Mechanistic mother: ICLR 2026 `Linear Mechanisms for Spatiotemporal Reasoning in Vision Language Models`; behavioral mother: ICLR 2025 Oral `COMFORT`。现成 image-plane x/y IDs + FoR behavior；新机制：late remap vs explicit coordinate transform vs multiple frame codes + selector。

- Registration: [`REGISTERED_SPATIAL_REFERENCE_FRAME_TRANSFORMATION_2026-08-31.md`](phenomenon_miner/REGISTERED_SPATIAL_REFERENCE_FRAME_TRANSFORMATION_2026-08-31.md)
- Active plan: [`active/030_spatial_reference_frame_transformation/README.md`](active/030_spatial_reference_frame_transformation/README.md)

### 03 Do Language Models Really Lie When They Fail?

Mother: ICLR 2026 Oral `Beyond Prompt-Induced Lies`。已知 benign hard-wrong/easy-follow-up-correct phenotype 与公开 Llama/Mistral/Qwen/Gemma outputs；新机制：genuine knowledge-action dissociation vs reasoning-state corruption vs competing trajectories。核心：`edge-state reinstatement`。

- Registration: [`REGISTERED_SPONTANEOUS_DECEPTION_KNOWLEDGE_ACTION_2026-08-31.md`](phenomenon_miner/REGISTERED_SPONTANEOUS_DECEPTION_KNOWLEDGE_ACTION_2026-08-31.md)
- Active plan: [`active/031_spontaneous_deception_knowledge_action/README.md`](active/031_spontaneous_deception_knowledge_action/README.md)

### 04 What Does Reasoning Training Forget?

Mother: ACL 2026 `Temporal Sampling for Forgotten Reasoning in LLMs`。同一 reasoning item 在真实训练 checkpoint 轨迹上 deterministic `correct -> wrong`，且总体能力仍上升；新机制：upstream capability erosion vs reasoning-circuit disruption vs persistent solution with changed control/readout vs diffuse interference。核心：**checkpoint layer transplantation**。

- Registration: [`REGISTERED_TEMPORAL_FORGETTING_MECHANISM_2026-08-31.md`](phenomenon_miner/REGISTERED_TEMPORAL_FORGETTING_MECHANISM_2026-08-31.md)
- Active plan: [`active/032_temporal_forgetting_mechanism/README.md`](active/032_temporal_forgetting_mechanism/README.md)

### 05 Why Bigger Models Ignore Lies but Copy Noise

Behavior mother: Findings ACL 2026 `Better and Worse with Scale`; mechanistic predecessor: ACL 2025 Outstanding `Llama See, Llama Do`。Pythia/Cerebras 已建立 semantic entrainment 随规模下降、non-semantic copying 随规模上升的反向 scaling；mother 明确没有 mechanistic decomposition。新机制：shared copying writer + semantic gate vs distinct scaling circuits vs late memory/context competition。核心：跨 scale causal head/pathway decomposition + semantic-filter ablation/patching。

- Registration: [`REGISTERED_CONTEXTUAL_ENTRAINMENT_OPPOSITE_SCALING_MECHANISM_2026-08-31.md`](phenomenon_miner/REGISTERED_CONTEXTUAL_ENTRAINMENT_OPPOSITE_SCALING_MECHANISM_2026-08-31.md)
- Active plan: [`active/033_contextual_entrainment_opposite_scaling/README.md`](active/033_contextual_entrainment_opposite_scaling/README.md)

## Active execution discipline

Each active README contains the background, exact mother object, competing hypotheses, inherited data/models/artifacts, detailed initial validation sequence, fatal controls, and promote/kill conditions.

Uniform execution order:

```text
mother artifact freeze
→ exact matched population
→ cheap faithful replay
→ validate measurement
→ causal intervention
→ replication
→ paper-scale expansion
```

Entering `active/` does **not** mean a preferred hypothesis must win. Strong nulls that falsify the mother interpretation are allowed; construct/measurement failures must still be terminated rather than rescued post hoc.

## Hamdi-style discipline

禁止：`想 phenomenon -> 造数据/机制 -> 花算力赌行为存在`。

只允许：`strong mother -> exact established object/anomaly -> same-object omitted real axis or unasked causal computation -> inherit artifact/recipe -> negative memory + strongest-neighbor -> cheap falsifier -> S0/N0/N1 -> PASS-REGISTER -> active validation -> MI`。

任何认真审过后死亡的候选必须立即进入 `rejected_candidates/`，带 semantic aliases；不得通过换模型、数据、prompt、语言、subset、MI method 复活。

## 其它状态

- `Individual belief lookbacks -> common ground`：高质量 HOLD；缺同 checkpoint capability bridge，不计数。
- `014 Alias Entrainment Transfer`：已有正式结果，继续 paper development，不属于本轮五题。
- `NTSB causal relevance vs causal-role selection`：TERMINAL `KILL-S0 / RELEVANCE-ALSO-FAILS`。

> **不再问“模型可能还有什么错”；问“强 mother 已建立的对象/异常，还缺哪个决定性 causal computation？”**
