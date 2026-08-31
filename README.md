# Interpretability Topic Search

这个仓库用于寻找、快速证伪、再解释 **LLM / VLM 的自然、反直觉、可机制化 scientific questions**。

```yaml
PASS_REGISTER: 3
counts_toward_target_five: 3
new_topic_MI_authorized:
  - ETR-human-like-fallacy
  - spatial-reference-frame
  - spontaneous-deception-knowledge-action
latest_registration: spontaneous deception knowledge-action audit
latest_terminal_execution: NTSB causal-role frontier KILL-S0
```

当前已有 **3/5** 个正式 `PASS-REGISTER`；其它 survivor/HOLD 不计数。

## 当前只认三份权威文件

1. [`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md) — 唯一选题协议
2. [`phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`](phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md) — 当前状态 / 下一步
3. 本 README — 仓库入口

一般失败经验见 [`phenomenon_miner/FAILED_TOPICS.md`](phenomenon_miner/FAILED_TOPICS.md)。其它 gate/funnel/addendum/domain log 是冷证据；只有新题语义接近时定向读取。

## 当前正式注册

### 01 Human-Like Fallacies: Alternative Filtering or Prior Contamination?

Mother：ICLR 2026 `Theory-Grounded Evaluation of Human-Like Fallacy Patterns in LLM Reasoning`。行为已在 383 个 PyETR problems、38 个模型上建立；premise reversal 已是现成 causal manipulation。新问题是 ETR-like premature alternative filtering、semantic/prior contamination、还是 late output imitation。核心干预：`alternative reinstatement patch`。

Card: [`REGISTERED_ETR_HUMAN_LIKE_FALLACY_MECHANISM_2026-08-31.md`](phenomenon_miner/REGISTERED_ETR_HUMAN_LIKE_FALLACY_MECHANISM_2026-08-31.md)

### 02 From Pixels to Perspectives: Reference-Frame Transformation in VLMs

Mechanistic mother：ICLR 2026 `Linear Mechanisms for Spatiotemporal Reasoning in Vision Language Models`；behavioral mother：ICLR 2025 Oral `COMFORT`。现成 image-plane x/y spatial IDs 与 Camera/Addressee/Relatum FoR gap 有 checkpoint overlap。新问题：late linguistic remap、explicit coordinate transform、还是 multiple frame-specific codes + selector。核心干预：analytic x/y ID transform + FoR selector patch。

Card: [`REGISTERED_SPATIAL_REFERENCE_FRAME_TRANSFORMATION_2026-08-31.md`](phenomenon_miner/REGISTERED_SPATIAL_REFERENCE_FRAME_TRANSFORMATION_2026-08-31.md)

### 03 Do Language Models Really Lie When They Fail?

Mother：ICLR 2026 Oral `Beyond Prompt-Induced Lies: Investigating LLM Deception on Benign Prompts`。Mother 已在 benign graph reasoning 上建立“hard initial wrong + matched easier follow-up correct”的 spontaneous-deception phenotype，并公开 Llama/Mistral/Qwen/Gemma item-level outputs；但它用 easier follow-up behavior 代理“internal belief”，没有证明 hard deceptive run 内部真的保留正确答案。

新问题：是 **genuine knowledge-action dissociation**、**reasoning-state corruption**，还是 **competing correct/fabricated trajectories**？核心干预：missing-edge/reachability state tracing + easy/truthful→hard-deceptive causal patch + `edge-state reinstatement`。若 hard run 根本没有正确 state，结果会直接修正 mother 的 deception 解释，仍是 paper-level finding。

Card: [`REGISTERED_SPONTANEOUS_DECEPTION_KNOWLEDGE_ACTION_2026-08-31.md`](phenomenon_miner/REGISTERED_SPONTANEOUS_DECEPTION_KNOWLEDGE_ACTION_2026-08-31.md)

## Hamdi-style discipline

禁止：

```text
想一个合理 phenomenon -> 造数据/机制 -> 花算力赌行为存在
```

只允许：

```text
strong concrete mother
-> exact scientific object / established anomaly
-> same-object omitted real axis OR unasked causal computation
-> inherit mother recipe/artifact
-> semantic negative-memory + strongest-neighbor attack
-> cheap falsifier
-> S0/N0/N1
-> PASS-REGISTER
-> MI
```

任何候选只要认真进入 mother/neighbor/substrate/behavior/measurement/mechanism 审查后死亡，必须立即在 `rejected_candidates/` 留短 record + semantic aliases。不得通过换模型、数据、prompt、语言、subset、MI method 复活。

## 其它状态

- `Individual belief lookbacks -> common ground`：高质量 HOLD；缺同 checkpoint capability bridge，不计数。
- `014 Alias Entrainment Transfer`：已有正式结果，不属于本轮五题。
- `NTSB causal relevance vs causal-role selection`：TERMINAL `KILL-S0 / RELEVANCE-ALSO-FAILS`。
- 其它 legacy HOLD/frontier 不计数，以 handoff 为准。

> **不要问“模型还可能有什么有趣的错？”；问“强 mother 已经建立了什么对象/异常，而它还没有问哪个重要的 causal computation？”**
