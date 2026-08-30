# Current Topics

日期：2026-08-30  
状态：`AUTHORITATIVE FOCUS QUEUE / NATURAL-QUESTION RESET`

Top-6 第一轮实跑和独立审查已经完成。结果不是简单的“运气不好”：015/016/017/019 暴露出此前找题流程过度奖励“可构造的 factorial experiment”，而没有把“科学问题本身是否自然、是否高概率存在”放在最前面。

新的 pre-discovery gate：[`NATURAL_QUESTION_GATE.md`](NATURAL_QUESTION_GATE.md)。

从现在开始，**当前资源只集中到 014 和 018。** 020–023 暂停 screening，必须先按 Natural-Question Gate 重新审计，不能因为之前已经注册就继续消耗模型调用。

---

## Priority 1 — 014 Alias Entrainment Transfer

目录：[`../active/014_alias_entrainment_transfer/`](../active/014_alias_entrainment_transfer/)

**Status:** `ESTABLISHED / PAPER-DEVELOPMENT PRIORITY`

自然问题：

> 一个 surface form 刚刚被看见后会被 contextual entrainment；那这种 salience 会不会自然扩散到同一对象或强 learned relation 的另一个 surface form？

为什么保留：

- mother phenomenon 已成立，不需要赌“entrainment 存不存在”；
- broad cross-surface spillover 已被三家族、双 frame、双方向稳定验证；
- `ASSOC_ANY` 控制说明 broad effect 不只是随便一个强关联 pair；
- r4 已把 scope narrowing、zero-joint association、casefold collision、circular identity foil 等 construct 风险逐项修正并全量重跑；
- negative boundary 也清楚：真正 `opaque_strict` reference-specific Q2 不成立。

允许的 paper-level claim：

> **Contextual entrainment spills across learned/derivable surface-form relations, with a strong lexical/derivational gradient and a clear boundary before reference-specific identity.**

下一步只做论文发展，不再做 reference-positive subset rescue：

1. 冻结 paper thesis；
2. 把 phase 1 / r4 broad behavior、phase 2 shared upstream cause、phase 3 lexical direct-write、r4 structure gradient 串成单一因果叙事；
3. 明确把 `opaque_strict≈0` 写成 boundary finding，而不是失败结果；
4. 做必要但不改变 claim 的 figure/table consolidation 和 robustness packaging；
5. 不新增 person-only / F2-only / direction-only / alias-subtype rescue。

---

## Priority 2 — 018 Stock–Flow Correlation Intrusion

目录：[`../active/018_stock_flow_correlation_intrusion/`](../active/018_stock_flow_correlation_intrusion/)

**Status:** `PRIMARY REDESIGN PROJECT / SCIENTIFIC STATUS UNKNOWN`

自然问题：

> 如果模型已经正确理解或算出 net flow，为什么下游判断 stock 涨跌时仍可能被更显眼的 inflow 走势带跑？

为什么保留：

- stock-flow confusion 是独立于任何 LLM benchmark 的自然 cognitive object；
- `stock(t+1)=stock(t)+inflow-outflow` 有 deterministic external semantics；
- ResOpsUS 的 600-window / 200-reservoir / full 2×2 bank 是自然数据，不是为了造 effect 写出来的 synthetic puzzle；
- D0 v1 的失败来自 A/B option-position recognition instrument，而不是 scientific null；
- 修 measurement 时不需要换问题、不需要换 population，也不需要删不利 cell。

### D0 v2 唯一允许的改动

替换 net-recognition measurement：

- semantic continuation：直接比较 `positive` vs `negative`；或
- numeric computation：让模型输出 cumulative inflow minus cumulative outflow，再 deterministic parse sign。

必须保持：

- 原 600 natural windows；
- `net direction × inflow trend` 四个 cell；
- reservoir clustering；
- explicit-correct-net downstream control；
- table/text 主呈现；
- 不允许 positive-net-only subset。

D0 v2 冻结后再恢复模型调用。

---

## Suspended — 020–023

以下项目**不判死，但停止排队**：

- `020 Incremental Clue Backfire`
- `021 Task-Switch Carryover`
- `022 Local Success, Global Composition Failure`
- `023 Description–Experience Gap`

原因不是实验结果，而是它们来自上一版 topic-generation process。必须先逐题通过：

```text
P0 natural question
P1 existence prior
P2 five-minute / ten-example sanity
P3 dataset-is-instrument test
P4 restriction budget
P5 natural mechanism unfolding
```

任何一题如果需要先解释复杂 benchmark construction 才显得有意思，或者 phenomenon 本身高度依赖特殊 denominator，直接移出，不再因为“代码已经写了一点”而继续。

在 re-audit 完成前：

```yaml
020_screening: false
021_screening: false
022_screening: false
023_screening: false
```

---

## Archived from completed Top-6

- `015 Clarification Resolution Lag` — matched neutral history explains apparent lag.
- `016 Mixed-Status Event Attraction` — same-status context explains mixed-context shift.
- `017 Cross-Modal Resolution Inertia` — strongest effect does not require prior interpretation identity.
- `019 Abstention Hysteresis` — strong reverse effect; neutral incomplete→complete history explains recovery.

完整审查：[`TOP6_RESULT_REVIEW_2026-08-30.md`](TOP6_RESULT_REVIEW_2026-08-30.md)。

---

## Current allocation

```text
paper development: 014
behavioral redesign: 018
new-topic screening: PAUSED
020–023: SUSPENDED-PENDING-NATURALNESS-REAUDIT
```

---

## One-line discipline

> **先问一个普通人一听就想知道答案的自然问题，再找数据测它；绝不再从“这个数据集能拼出什么 contrast”反推 scientific question。**
