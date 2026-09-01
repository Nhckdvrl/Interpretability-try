# Rejected Candidates — Evidence Library

这个目录是**逐题负证据库**，不是当前选题协议，也不是下一轮必须从头通读的清单。

当前协议只看：

- `../phenomenon_miner/FINDING_RULES.md`
- `../phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`
- `../phenomenon_miner/CURRENT_SEARCH_FLOW_2026-09-01.md` — 当前 v2.1 实际执行顺序，尤其明确 Route C 不再机械要求 exact modern-open published phenotype。

一般失败规律只看：

- `../phenomenon_miner/FAILED_TOPICS.md`

**语义去重第一入口：**

- [`CANONICAL_FAILURE_INDEX_2026-09-01.md`](CANONICAL_FAILURE_INDEX_2026-09-01.md) — 按 scientific object / semantic aliases 聚类的 canonical failure index。任何新 serious candidate 进入 HARD AUDIT 前必须先查这里，防止换标题、dataset、model、prompt、language、subset 或 MI method 后重复审同一个死题。

### Live-audit override rule

Canonical failure index 是快速 dedupe 层，不高于当前 live HARD AUDIT。若某个旧 index 条目后来因为更好的 scientific object / substrate 被重新定性，必须以**明确命名的最新 HARD AUDIT 文件**为准，并最终回写 index。

当前明确 override：

- `numerical identity / same token vs qualitative sameness` 不再视为 terminal `entity tracking` 近义题；当前状态见 `../phenomenon_miner/HARD_AUDIT_NUMERICAL_IDENTITY_VS_QUALITATIVE_SAMENESS_2026-09-01.md`。它仍未注册，但应继续做 N2 hard audit，而不是在 dedupe 阶段自动 kill。

---

## Mandatory logging boundary

**所有被认真审查过但最终排除的问题都必须在本目录留下短记录。** 目的不是写研究日记，而是建立 semantic dedupe memory，防止未来因为换标题、dataset、model、prompt、language、subset 或 MI method 又重新花文献时间或 GPU 排查同一个死题。

判定边界：

- 仅仅出现在搜索结果里、没有形成 scientific question / mother-extension card 的噪声，不建文件；
- 一旦对一个问题认真检查过 mother ownership、strongest neighbor、substrate、existing behavior、measurement 或 mechanism 中任一项，并据此决定 KILL，**必须立即建 rejection record**；
- pre-S0 / N0 / cheap-falsifier 阶段死亡同样必须记录，不以“还没跑模型”为理由省略；
- 同一 scientific meaning 的别名应合并到一个 canonical rejection，不为 rename 建重复文件；
- 如果一次死亡新增了一个未来很容易被换名复活的 alias family，**同时更新 `CANONICAL_FAILURE_INDEX_2026-09-01.md`**。

---

## 正确使用方式

当一个具体 mother-extension card 已经形成后：

1. 把新 scientific object 写成一句话；
2. 生成 5–10 个 semantic aliases / nearest-neighbor formulations；
3. **先查 `CANONICAL_FAILURE_INDEX_2026-09-01.md`**；
4. 再查是否存在明确的 live HARD AUDIT override；
5. 再在本目录和 `../archive/` 定向搜索；
6. 命中相同 scientific meaning 时，再读对应详细 rejection；
7. 只有满足该 rejection 的 resurrection condition 或已有明确 live override 才允许重开。

不要每轮完整通读所有 addendum。不要因为换 dataset、model、language、prompt、subset 或 MI method 就视为新题。

尤其禁止：

```text
旧死题 X
→ 换一个更学术的名字 X'
→ 找一个新 benchmark
→ 换成 SAE / steering / patching
→ 重新当 fresh candidate
```

如果 scientific object 没变，就仍然属于同一个 terminal cluster。

---

## 新 rejection 的最小格式

以后保持短，不复制整套 protocol：

```yaml
question:
mother:
semantic_aliases: []
what_was_reviewed:
kill_class: F1|F2|F3|F4|F5|F6|F7
kill_evidence:
nearest_neighbor_warning:
resurrection_condition:
```

其中 `kill_evidence` 必须写**决定性证据**，而不是“感觉不够好”。`nearest_neighbor_warning` 要尽量覆盖未来最可能的改名复活方式。

F1–F7 定义见 `phenomenon_miner/FAILED_TOPICS.md`。

只有当一次死亡产生了**新的通用失败模式**，才更新 `FAILED_TOPICS.md`。否则只写本目录的局部证据；如果只是新增 alias/dedupe family，则更新 canonical failure index。

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

> **认真审过就留短负记录；新题先查 canonical semantic failure index；scientific object 相同就禁止靠改名/换数据/换模型/换 MI 方法复活；但 Route C 的 deterministic natural axis 也不能因为缺 exact published modern-open phenotype 被旧规则误杀。**
