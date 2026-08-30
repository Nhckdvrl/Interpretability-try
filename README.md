# Interpretability Topic Search

这个仓库用于寻找、快速证伪、再解释 **LLM / MLLM 的自然反直觉现象**。

当前核心流程：

```text
programmatic / source-grounded D0
-> diagnostic controls
-> scientific PASS / scientific FAIL / measurement-INCONCLUSIVE
-> only real positives enter mechanism
```

## 2026-08-30 Top-6 实验审查

前六个项目已全部完成第一轮实验，并重新按代码、数据、gate、fatal controls、统计与 claim 逐项独立审查。

完整报告：[`phenomenon_miner/TOP6_RESULT_REVIEW_2026-08-30.md`](phenomenon_miner/TOP6_RESULT_REVIEW_2026-08-30.md)

### 成立

**014 Alias Entrainment Transfer**

Broad cross-surface learned-relation spillover 很强：三家族、双 frame、双方向均稳定超过强 `ASSOC_ANY` different-referent control。真正没有成立的是 entity/reference-specific interpretation；`opaque_strict` Q2 未通过。

### 尚不能判真假

**018 Stock–Flow Correlation Intrusion**

D0 v1 的 ResOpsUS 数据设计是好的，但 net-recognition A/B gate 被极端 option-position bias 破坏，negative-net cells 没有合法 denominator。因此是 `INCONCLUSIVE / HOLD-D0-MEASUREMENT-FAILURE`，不是 scientific null。

### 已归档

以下四个 registered contracts 被诊断性实验终止：

- `015 Clarification Resolution Lag` — matched neutral history 解释 apparent lag；
- `016 Mixed-Status Event Attraction` — same-status context 解释 mixed-context shift；
- `017 Cross-Modal Resolution Inertia` — strongest effect 不需要旧 interpretation identity；
- `019 Abstention Hysteresis` — 三家族/两 source 强烈朝假设反方向，且 neutral history 解释 recovery。

完整项目、代码、数据合同、raw results 和报告均保存在 [`archive/`](archive/README.md)。

## 当前还在队列里的题

[`phenomenon_miner/CURRENT_TOPICS.md`](phenomenon_miner/CURRENT_TOPICS.md)

```text
paper synthesis: 014
measurement redesign: 018
next screening: 020 -> 023 -> 021 -> 022
```

020 必须先做内部 collision；021/022 必须超出强 mother work 的 headline behavior。

## 关键入口

- [`active/README.md`](active/README.md) — 当前项目。
- [`archive/README.md`](archive/README.md) — terminal 项目与完整 provenance。
- [`phenomenon_miner/AUDIT_REGISTRY.md`](phenomenon_miner/AUDIT_REGISTRY.md) — 唯一模型调用授权。
- [`phenomenon_miner/FAILED_TOPICS.md`](phenomenon_miner/FAILED_TOPICS.md) — anti-revival failure library。
- [`phenomenon_miner/DATASET_SCOPE_AUDIT.md`](phenomenon_miner/DATASET_SCOPE_AUDIT.md) — 数据 scope 纪律。
- [`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md) — finding / promotion 规则。

## 当前最重要的新增教训

> **`NO-PROMOTE` 不能自动翻译成“现象不存在”。**

如果 fatal control 解释掉目标效应，或者 well-powered diagnostic contrast 稳定为 null，当前 contract 可以 archive。

如果 capability / measurement instrument 本身导致关键 cell 没有合法 denominator，只能写 `INCONCLUSIVE / REDESIGN`。018 就是这种情况。

反过来，一个 clean negative 也不能通过换模型、subset、threshold、prompt 或 readout 继续搜 positive。

## 一句纪律

> **先确定你真的测到了那个科学对象，再讨论它存在不存在；一旦用正确的诊断对照把它否掉，就停。**
