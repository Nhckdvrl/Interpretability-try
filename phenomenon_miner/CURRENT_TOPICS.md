# Current Topics

日期：2026-08-30  
状态：`AUTHORITATIVE POST-TOP6 QUEUE`

Top-10 的前六个项目已经完成第一轮实跑并做了独立 post-run audit。完整审查：[`TOP6_RESULT_REVIEW_2026-08-30.md`](TOP6_RESULT_REVIEW_2026-08-30.md)。

现在不再把“跑过但失败的项目”继续列在当前 queue 中，也不把所有 `NO-PROMOTE` 机械视为 scientific null。

---

## A. 已经成立、值得进入论文整理

### 014 — Alias Entrainment Transfer

目录：[`../active/014_alias_entrainment_transfer/`](../active/014_alias_entrainment_transfer/)

**Verdict:** `ESTABLISHED / CROSS-SURFACE-BUT-NOT-REFERENCE-SPECIFIC`

已经站住的是：

> contextual entrainment / salience 会沿 learned or derivable surface-form relations 外溢；这种 spillover 明显超出强关联但不同 referent 的 `ASSOC_ANY` control，并在三家族、双 frame、双方向上稳定。

没有站住的是：

> shared referent 本身是特殊 causal unit / entity-level salience representation。

r4 的 `opaque_strict` reference-specific Q2 在三个家族都没有通过 both-frame criterion；ungated opaque-strict 也全部 null。结构梯度 `compositional > partial > opaque >> opaque-strict≈0` 与 phase-3 lexical direct-write 形成一致边界。

**下一步：** 不再找 reference-positive subset。直接围绕 broad spillover、structure gradient、phase-2 shared upstream cause、phase-3 lexical boundary 整理论文叙事。

---

## B. 暂时不能判真假的题：measurement redesign

### 018 — Stock–Flow Correlation Intrusion

目录：[`../active/018_stock_flow_correlation_intrusion/`](../active/018_stock_flow_correlation_intrusion/)

**Verdict:** `INCONCLUSIVE / HOLD-D0-MEASUREMENT-FAILURE`

ResOpsUS 数据 bank 和 2×2 natural design 本身没有问题。问题出在 net-flow recognition gate：A/B forced-choice 的 option-position bias 极端到让所有严格 gated items 都落在 positive-net cells。Llama 在 negative-net 上 canonical 近 100%、reversed 0%，因此不能把空 negative-net denominator 当作 scientific null。

**下一步如果继续：**

1. 冻结 D0 v2；
2. 用 semantic continuation (`positive` vs `negative`) 或 deterministic numeric net computation 取代 A/B letter gate；
3. 保留完整 `net direction × inflow trend` 四个 cell；
4. 保留 explicit-correct-net downstream control；
5. 禁止只跑 positive-net subset。

在新 contract 冻结前不继续模型调用。

---

## C. 尚未裁决、继续排队的四题

### 020 — Incremental Clue Backfire

> 已经答对以后，再增加一条 source-authored、同 gold 的真实 clue，模型是否反而改错？

Primary shape: Quiz Bowl ordered clue prefixes。

**先做 internal collision。** 若旧 Evidence-Induced Referent Displacement 已经覆盖同一 scientific object，直接 route/kill，不允许只因换数据集复活。

### 021 — Task-Switch Carryover

> 换任务后犯的错，是普通性能下降，还是仍然朝“旧任务规则预测的答案”移动？

Gupta et al. EMNLP 2024 已做 aggregate task-switch interference。只有 **old-rule-specific wrong destination / decay** 才是这里可能的新现象。

### 022 — Local Success, Global Composition Failure

> 所需中间事实已经全部正确、甚至显式摆在当前 context 中，最终组合仍然会不会错？

Press et al. 已定义 compositionality gap。普通“子问题对、总问题错”不是 novelty；必须测试更强的 externalized-intermediate-facts 条件。

### 023 — Description–Experience Gap

> 同一个 gamble，用概率描述或完全等价的 exact-frequency 历史呈现，选择是否系统不同？

必须用 deterministic exact frequencies 和 frequency/EV capability gates；sampling noise 不能承担主效应。

---

## D. 2026-08-30 已归档的四个 completed Top-6 项目

| project | terminal verdict | decisive reason |
|---|---|---|
| `015 Clarification Resolution Lag` | `ARCHIVED / REGISTERED PHENOTYPE REJECTED` | neutral matched history 产生与 ambiguity history 同量级影响；三个家族 `MATCHED-AMBIGUITY` CI 均跨 0 |
| `016 Mixed-Status Event Attraction` | `ARCHIVED / REGISTERED BROAD PHENOTYPE REJECTED` | `MIXED-LOCAL` 被 same-status context 解释；三家族 diagnostic `MIXED-SAME` 不成立，no-relation stratum 也 null |
| `017 Cross-Modal Resolution Inertia` | `ARCHIVED / INTERPRETATION-SPECIFIC CLAIM REJECTED` | strongest powered Llama effect 被 masked-choice history 几乎完全复制；不需要旧 interpretation identity |
| `019 Abstention Hysteresis` | `ARCHIVED / STRONGLY REJECTED` | 三家族、两 source、两类 readout 全部显著朝相反方向；neutral history 解释大部分 recovery |

完整项目已移入 `archive/`，不能在原 scientific identity 下用 prompt/subset/model/readout rescue。

---

## 当前实际顺序

```text
paper synthesis: 014
measurement redesign only: 018
next cheap screening: 020 -> 023 -> 021 -> 022
```

其中 020 collision-first；021/022 mother-collision 风险高。

---

## 判题纪律更新

这轮最重要的新规则：

> **`NO-PROMOTE` ≠ 自动 `KILL`。**

先问为什么没 promote：

- fatal control 把目标效应解释掉 / 三家族给出诊断性 null → 可以 archive；
- capability 或 measurement instrument 本身没有建立合法 denominator → `INCONCLUSIVE / REDESIGN`，不能声称现象不存在。

这一区分以后必须写进所有 D0 final report。
