# Active Projects

`active/` 是已经有明确科学投入理由、允许进入**预注册式初步验证 / causal MI** 的项目目录。

当前发现协议与状态只认：

1. [`../README.md`](../README.md)
2. [`../phenomenon_miner/FINDING_RULES.md`](../phenomenon_miner/FINDING_RULES.md)
3. [`../phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`](../phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md)

旧 `AUDIT_REGISTRY`、gate、funnel、addendum、历史 active 目录只保留 provenance，不再与上述三份文件并列作为权限源。

## 当前主线

| project | status | first execution target |
|---|---|---|
| [`029_etr_human_like_fallacy`](029_etr_human_like_fallacy/) | **ACTIVE / PASS-REGISTER** | 冻结 mother reversal-rescue pairs → formal ETR-state measurement → alternative reinstatement patch |
| [`030_spatial_reference_frame_transformation`](030_spatial_reference_frame_transformation/) | **ACTIVE / PASS-REGISTER** | 复现 mother x/y spatial IDs + COMFORT overlap → analytic FoR transform / selector patch |
| [`031_spontaneous_deception_knowledge_action`](031_spontaneous_deception_knowledge_action/) | **ACTIVE / PASS-REGISTER** | 从官方 outputs 重建 deceptive events → graph-state measurement → edge-state reinstatement |
| [`032_temporal_forgetting_mechanism`](032_temporal_forgetting_mechanism/) | **ACTIVE / PASS-REGISTER** | 重建 greedy checkpoint transitions → checkpoint layer transplantation |
| [`033_contextual_entrainment_opposite_scaling`](033_contextual_entrainment_opposite_scaling/) | **ACTIVE / PASS-REGISTER** | 复现 mother sign split + ACL'25 entrainment causality → semantic-gate / writer decomposition |
| [`014_alias_entrainment_transfer`](014_alias_entrainment_transfer/) | **ESTABLISHED / PAPER DEVELOPMENT** | 已有正式结果；继续 paper development |

五个新项目的 README 都同时承担：

- 背景与 mother object；
- 新 scientific question；
- competing causal hypotheses；
- 可复用数据 / 模型 / artifact；
- 初步验证 V0→Vn；
- fatal controls；
- promote / kill 条件。

在真正产生代码和结果前，**不要为每个项目再拆多份 planning 文档**。实验开始后再按需添加 `scripts/`、`data/manifest`、`results/`、`PREFLIGHT.md` / `REPORT.md`。

## 五题的一句话

### 029 — Human-Like Fallacies

> LLM 与人类犯同一个 ETR-predicted fallacy，是因为内部也过早过滤了必要 alternative，还是语义 prior / late readout 恰好产生同样输出？

核心：**premise reversal + alternative reinstatement patch**。

### 030 — Spatial Reference Frames

> VLM 从 camera/image-plane spatial ID 回答另一个视角时，真的变换内部坐标，还是选择另一套 code / 最后才翻译？

核心：**mother x/y ID 的解析几何变换 + FoR selector patch**。

### 031 — Spontaneous Deception

> hard question 答错、easy follow-up 答对时，hard run 内部真的知道真相但没说，还是 reasoning state 本身已经错了？

核心：**ground-truth graph-state tracing + edge-state reinstatement**。

### 032 — Temporal Forgetting

> reasoning training 让同一道题 `correct -> wrong` 时，是擦掉能力、破坏推理 circuit，还是只改变哪个 latent solution 控制输出？

核心：**同架构相邻 checkpoint layer transplantation + reverse transplant**。

### 033 — Opposite-Scaling Contextual Entrainment

> 为什么模型越大越抗 semantic misinformation，却越容易机械复制 meaningless context？

核心：**shared copying writer + semantic gate vs distinct circuits vs late competition** 的跨 scale causal decomposition。

## 执行纪律

这些项目已经通过选题 gate，但 **ACTIVE 不等于允许跳过验证**。

统一执行顺序：

```text
mother artifact freeze
→ exact matched population
→ cheap faithful replay
→ measurement validation
→ causal intervention
→ replication
→ paper-scale expansion
```

禁止：

- 重新发明一个更容易跑的数据集替代 mother object；
- fresh expensive G0 只是为了重新确认已知行为；
- 看到结果后换 subset / threshold / prompt 救 hypothesis；
- probe 有信号就直接写 mechanism；
- 用 LLM judge 取代已有确定性 formal / graph / exact-answer gold；
- 把 generic head localization 当作论文贡献。

如果 initial validation 暴露 construct、measurement 或 causal-identification 致命问题，应立即降级/终止并留下 evidence，而不是因为已经进 `active/` 就强行保题。

## Legacy / provenance directories

`003`、`013`、`018`、`023`–`028` 等旧目录仍保留历史材料，但它们的目录存在**不表示当前 ACTIVE**。其最新状态以 root README / handoff 与各自 terminal evidence 为准。

> **active 的意义是：问题已经值得认真验证；不是问题已经被证明，更不是 hypothesis 必须成功。**
