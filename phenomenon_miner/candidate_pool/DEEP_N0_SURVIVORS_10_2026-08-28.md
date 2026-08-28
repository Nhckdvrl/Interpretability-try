# 深度 N0 后的当前十题 shortlist（2026-08-28）

状态：`ADVERSARIAL-N0-SURVIVOR / AWAITING INDEPENDENT SIGN-OFF / NOT DISPATCHABLE`

```yaml
validation_authorized: false
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
```

本文件是当前十题 shortlist。详细的第二轮对抗式新颖性审计、最强邻居、`why_not_a_rename` 与 hard kill condition 见：

[`audits/ADVERSARIAL_N0_TEN_2026-08-28.md`](audits/ADVERSARIAL_N0_TEN_2026-08-28.md)

**这里的 `ADVERSARIAL-N0-SURVIVOR` 不等于 formal `N0-PASS`。** 本轮仍属于同一 proposer-side 审计链；仓库流程要求另一独立 auditor 做 citation chaining、全文/appendix 检查与时间戳 refresh。没有 independent N0 + D0 + 注册表授权，不得跑 smoke。

---

## 当前十题

| # | 题目 | 一句话 decisive contrast | 状态 |
|---:|---|---|---|
| 1 | **First-Negative-Evidence Harm** | fixed option set 中，一条真实 negative subtraction 先害、更多 negative 又救；必须区别于 mention、positive anchor 与 physical deletion | `ADVERSARIAL-N0-SURVIVOR` |
| 2 | **Packed–Unpacked Event Splitting** | 模型确认同一事件 = 互斥穷尽 partition，却仍因 unpacking 改变总 probability/decision weight | `ADVERSARIAL-N0-SURVIVOR` |
| 3 | **Publicness–Coordination Dissociation** | 每个人一阶知识严格匹配，只改变 private-to-each vs public observability，协调行为仍未体现 publicness | `ADVERSARIAL-N0-SURVIVOR` |
| 4 | **Existential Witness Collapse** | independent existential facts 的局部 binding 正确，downstream planner 却执行未经授权的 joint-witness join | `ADVERSARIAL-N0-SURVIVOR` |
| 5 | **Inadmissible-Evidence Persistence** | evidence 已正确判不可采/struck，verdict 却不能回到 `never-seen` counterfactual，并随其内容方向移动 | `ADVERSARIAL-N0-SURVIVOR` |
| 6 | **Habitual → Episode Actualization** | 已识别 habitual/generic 不蕴含具体发生，timeline/memory 却创建 dated/countable event token | `ADVERSARIAL-N0-SURVIVOR` |
| 7 | **Mixed-Status Event Attraction** | 两个 event factuality 分别判断正确，组合后却向邻接 event 的 status 定向 pooling/attraction | `ADVERSARIAL-N0-SURVIVOR` |
| 8 | **Dissent → Holding Role Swap** | majority/dissent 与双方 proposition 均识别正确，holding 却精确落到 dissent proposition | `ADVERSARIAL-N0-SURVIVOR` |
| 9 | **Source-Discount Recovery** | source identity 与低可信判断在 delay 后仍正确，但 source→message discount coupling 失效；source-cue reinstatement 应恢复折扣 | `ADVERSARIAL-N0-SURVIVOR` |
| 10 | **Weak-Evidence Backfire** | 模型独立判断 E 是 H 的正证据，却出现 `P(H|E) < P(H)` 的真正 sign reversal | `ADVERSARIAL-N0-SURVIVOR` |

---

## 本轮从十强永久移除

### SEC-06 / Provenance-Graph Retraction Leakage

`KILLED-COLLISION/ROUTE`。

[Grounded Continuation](https://arxiv.org/abs/2605.14175) 已把 dependency graph、retraction propagation 与 stale-premise continuation verifier 做成核心 operator。新闻转载/provenance 链可作为外部 setting，不再 standalone。

### UDH-03 / same-final-evidence abstention hysteresis

`KILLED-MOTHER-OCCUPIED`。

ACL 2026 Main [Mitigating Lost in Multi-turn Conversation via Curriculum RL with Verifiable Accuracy and Abstention Rewards](https://aclanthology.org/2026.acl-long.1540/) 已直接研究逐轮 instruction shards、solvability 与 abstention。partial→full 后仍拒答不足以从 LiC 母题独立出来。

### Sure-Thing / disjunction violation

`NOT-ADDED / DISCOVERY-OCCUPIED`。已有工作直接用 Savage sure-thing principle 评价 ChatGPT，不进入 discovery shortlist。

### 更早已移除

- Equivalent-Quantity Decision Split：quantity comparison / numeral-unit heuristic 近 exact；
- Generation–Reception Trace Asymmetry：self-conditioning/source-monitoring 母区过密；
- Part–Whole Double Counting：ROUTE 到 F6；
- Confidence-Conditioned Correction Relapse：confidence/self-correction 母区过密；
- Part-List Cue、Redundant-Constraint：保留历史 ideation，但不占十强。

---

## 下一道门

每题独立 reviewer 只需回答：

```text
exact phenotype 是否已在正文/appendix 做过？
更宽论文是否已经逻辑上包含 decisive contrast？
自然数据能否冻结 relation/gold？
why_not_a_rename 是否真的超出 F1–F9？
```

任一题失败就永久 KILL/ROUTE，再从新候选中补位；不得为了维持十题数量降低门槛。