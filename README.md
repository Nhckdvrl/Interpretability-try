# Interpretability Topic Search

这个仓库用于寻找、快速证伪、再解释 **LLM / VLM 的自然、反直觉、可机制化 scientific questions**。

当前 continuation search：

```yaml
PASS_REGISTER: 2
counts_toward_target_five: 2
new_topic_MI_authorized: ETR-human-like-fallacy | spatial-reference-frame
latest_registration: spatial reference-frame transformation
latest_terminal_execution: NTSB causal-role frontier KILL-S0
```

当前已有 **2/5** 个正式 `PASS-REGISTER`；其它 survivor/HOLD 不计数。

---

## 当前只认三份权威文件

1. [`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md) — **唯一选题协议**
2. [`phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`](phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md) — 当前状态 / 下一步
3. 本 README — 仓库入口

一般失败经验：[`phenomenon_miner/FAILED_TOPICS.md`](phenomenon_miner/FAILED_TOPICS.md)。其它 gate、funnel、N0/N1、terminal addendum、domain log、old candidate 文件都是历史证据；只有新题语义接近时定向读取。

---

## 当前正式注册

### 01 Human-Like Fallacies: Alternative Filtering or Prior Contamination?

Mother：ICLR 2026 `Theory-Grounded Evaluation of Human-Like Fallacy Patterns in LLM Reasoning`。

已知行为：383 个 PyETR reasoning problems、38 个模型；能力越强，错误中 ETR-predicted human-like fallacy 的比例越高，而总体逻辑正确率与能力无关；仅反转 premise order 就会在多个 open models 上显著阻断 fallacy。Mother 明确不主张 causal mechanism。

新问题：这些 human-like fallacies 是否来自 **ETR-like premature alternative filtering**、**semantic/prior contamination**，还是 **late output imitation**？核心干预是 original-order fallacy 与 reversed-order rescue 之间的 `alternative reinstatement patch`。

正式 card：[`phenomenon_miner/REGISTERED_ETR_HUMAN_LIKE_FALLACY_MECHANISM_2026-08-31.md`](phenomenon_miner/REGISTERED_ETR_HUMAN_LIKE_FALLACY_MECHANISM_2026-08-31.md)。

### 02 From Pixels to Perspectives: Reference-Frame Transformation in VLMs

Mechanistic mother：ICLR 2026 `Linear Mechanisms for Spatiotemporal Reasoning in Vision Language Models`；behavioral mother：ICLR 2025 Oral `COMFORT`。

已知对象：mother 公开代码从 4×4 image grid 提取 causal spatial IDs，并显式保存 horizontal/vertical `x/y` spatial axes；COMFORT 已在重叠的 LLaVA-1.5-7B/13B checkpoints 上证明模型偏好 egocentric FoR、难以灵活采用 Camera/Addressee/Relatum alternative frames。

新问题：camera/image-plane spatial ID 遇到另一 perspective 时，是 **late linguistic remapping**、**explicit intermediate coordinate transform**，还是 **multiple frame-specific codes + selector**？核心干预是 analytic x/y ID transform + matched FoR selector patch。

正式 card：[`phenomenon_miner/REGISTERED_SPATIAL_REFERENCE_FRAME_TRANSFORMATION_2026-08-31.md`](phenomenon_miner/REGISTERED_SPATIAL_REFERENCE_FRAME_TRANSFORMATION_2026-08-31.md)。

---

## 现在怎样找题

禁止默认路线：

```text
想一个听起来合理的 phenomenon → 设计数据/机制 → 花算力赌模型会不会出现
```

只允许真正的 Hamdi-style：

```text
strong concrete mother
→ exact scientific object
→ same-object omitted real axis / already-established anomaly's unasked computation
→ inherit mother recipe
→ semantic negative-memory + strongest-neighbor
→ cheap artifact/output falsifier
→ S0/N0/N1
→ PASS-REGISTER
→ MI
```

详见唯一协议 `FINDING_RULES.md`。

---

## 失败纪律

任何候选只要已经进入 mother / neighbor / substrate / behavior / measurement / mechanism 中任一项认真审查，最后 KILL，就必须立即在 `rejected_candidates/` 留下短 record + semantic aliases。只有未形成 scientific question 的搜索噪声可不记。

统一死亡类：F1 behavior lottery；F2 ownership；F3 substrate/object mirage；F4 measurement artifact；F5 no common phenotype；F6 post-hoc rescue；F7 mechanistically weak。

近期已经在 0 GPU 条件下杀掉多条看似漂亮的题，包括 derivation、relation algebra、RAG causal reliance、tool necessity、island gating、truth-vs-confidence、provenance recency×reliability、Preference Heads×intensity 等；不得通过换模型/数据/prompt/MI method 复活。

---

## 其它状态

- `014 Alias Entrainment Transfer`：已有正式研究结果，继续 paper development，不属于本轮五题计数。
- `NTSB causal relevance vs causal-role selection`：TERMINAL `KILL-S0 / RELEVANCE-ALSO-FAILS`。
- 其它 legacy HOLD/frontier 都不计数，以 handoff 为准。

---

## One-line discipline

> **不要问“模型还可能有什么有趣的错？”；问“强 mother 已经测清的 object，还有哪个重要属性或 computation 它没有问？”**
