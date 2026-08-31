# Rejected Candidates — Evidence Library

这个目录是**逐题负证据库**，不是当前选题协议，也不是下一轮必须从头通读的清单。

当前协议只看：

- `../phenomenon_miner/FINDING_RULES.md`
- `../phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`

一般失败规律只看：

- `../phenomenon_miner/FAILED_TOPICS.md`

---

## 正确使用方式

当一个具体 mother-extension card 已经形成后：

1. 把新 scientific object 写成一句话；
2. 生成 5–10 个 semantic aliases / nearest-neighbor formulations；
3. 在本目录和 `../archive/` 定向搜索；
4. 命中相同 scientific meaning 时，再读对应详细 rejection；
5. 只有满足该 rejection 的 resurrection condition 才允许重开。

不要每轮完整通读所有 addendum。不要因为换 dataset、model、language、prompt、subset 或 MI method 就视为新题。

---

## 新 rejection 的最小格式

以后保持短，不复制整套 protocol：

```yaml
question:
mother:
kill_class: F1|F2|F3|F4|F5|F6|F7
kill_evidence:
nearest_neighbor_warning:
resurrection_condition:
```

F1–F7 定义见 `phenomenon_miner/FAILED_TOPICS.md`。

只有当一次死亡产生了**新的通用失败模式**，才更新 `FAILED_TOPICS.md`。否则只写本目录的局部证据。

---

## Domain logs

这些文件用于语义检索，不是并列 authority：

- `agent_tool_use.md`
- `cognitive_decision_making.md`
- `cognitive_flexibility.md`
- `cognitive_logical_reasoning.md`
- `factuality_information_conflict.md`
- `multimodal_grounding.md`
- `risk_uncertainty_factorization.md`
- `semantic_pragmatic_factorization.md`
- `social_norm_factorization.md`
- `social_simulation_factorization.md`

日期型 `continuation_*`, `hamdi_*`, `*_addendum_*` 文件保留历史 provenance，但不再要求维护“latest addendum” authority chain。当前状态统一由 handoff 决定。

---

## Canonical recent terminal example

`ntsb_causal_relevance_vs_causal_role_selection_2026-08-31.md`：完整数据门通过后，四家族 behavior premise 仍失败，并暴露 metadata/construct 问题。它现在主要作为 F1/F3/F4 的 evidence case，而不是一条 live frontier。

---

## One-line rule

> **先有 mother-extension，再查负知识；不要从负知识长清单反向生成下一批 `X != Y`。**
