# Next Agent Prompt — 2026-09-01

继续 GitHub 仓库 `Nhckdvrl/Interpretability-try` 的 ACL / EMNLP / NAACL 风格 **LLM mechanistic interpretability 工作**。

这是 fresh topic search 的直接 continuation，但 **authoritative register 已经完成 5/5**。不要从旧 prompt 的 `2/5` 状态重新 brainstorm，也不要为了凑更多题继续稀释 search。

## 第一步：先读当前 authority

必须先完整读取：

1. `README.md`
2. `phenomenon_miner/FINDING_RULES.md` — v2.1 唯一选题协议
3. `phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md` — 当前 authoritative handoff
4. `active/034_prospective_memory_retrieval_architecture/README.md`
5. `active/035_shared_dynamic_context_update/README.md`
6. `active/036_metaphor_processing_route_selection/README.md`
7. `active/038_unresolved_reference_representation_architecture/README.md`
8. `active/039_same_kind_vs_go_together_semantic_relation/README.md`
9. 本文件

只在语义重合或新 fatal evidence 出现时定向查 `rejected_candidates/` / `archive/`。

## 当前 authoritative register

```yaml
CURRENT_FRESH_PASS_REGISTER: 5
CURRENT_FRESH_ACTIVE_TOPICS: 5
target: 5
status: COMPLETE_AFTER_039_REGISTRATION
registered:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 036_metaphor_processing_route_selection
  - 038_unresolved_reference_representation_architecture
  - 039_same_kind_vs_go_together_semantic_relation
archived:
  - 037_generic_generalization_licensing
```

### 034 — Prospective Memory Retrieval Architecture

**PASS-REGISTER / GPU AUTHORIZED / FROZEN.**

> 当 agent 一边继续当前任务、一边要记住未来意图时，它依靠持续 strategic monitoring、cue-triggered spontaneous retrieval，还是动态切换？

不要修改 headline，除非发现新 fatal novelty collision。

### 035 — Shared Dynamic Context Update

**PASS-REGISTER / GPU AUTHORIZED / FROZEN.**

> anaphora accessibility 与 presupposition projection 是否复用一个动态更新的 local discourse context，还是各有独立/static computation？

不要缩回单独 anaphora / presupposition mechanism。

### 036 — Metaphor Processing Route Selection

**PASS-REGISTER / GPU AUTHORIZED — v2.1 RE-AUDIT PASSED.**

> metaphor comprehension 中 comparison vs categorization 的 route 由 conventionality、aptness，还是没有离散 route switch 来决定？

本轮 hard audit 没发现直接占掉 conventionality × aptness selector 的现代 open-LLM causal work。Jones–Estes human 2×2 substrate 与 frozen contract 保留。

### 038 — Unresolved Reference Representation

**PASS-REGISTER / GPU AUTHORIZED — v2.1 RE-AUDIT PASSED.**

> 指代还无法唯一确定时，模型是同时保留多个候选、保持 underspecified，还是过早 commit？

AmbiCoref + Correct-Detect + It Depends 提供 matched ambiguity substrate、modern open-model premise 与 deterministic candidate gold。没有发现 2025–2026 direct causal factorization collision。

### 039 — Same Kind or Go Together? Taxonomic vs Thematic Semantic Relations

**PASS-REGISTER / GPU AUTHORIZED / Route C.**

> 当两个概念都“有关”时，模型是否区分它们是 **same kind / taxonomic**，还是 **go together in an event/scenario / thematic**，并真正用这个 relation type 做决定？

为什么注册：

- human cognitive-semantic object 独立存在，不由 benchmark 创造；
- Landrigan & Mirman 公开 659 word pairs，每个 pair 同时有 taxonomic 与 thematic human ratings，以及 `Difference_Score`；
- 不需要 LLM judge；
- NAACL 2025 causal property-inference 工作研究 taxonomy vs categorical similarity，不是 taxonomic vs thematic；
- NeurIPS 2025 TaxonomiGQA 的 non-taxonomic negatives 只是“不在 WordNet hypernym chain”，不是 thematic controls；
- 2026 LLM taxonomic/thematic triad 工作的 object 是 cultural-surrogate fidelity，不是 relation-type internal causal use；
- hard search 没发现现代 open LLM 上 direct taxonomic-vs-thematic causal patching/steering collision。

Frozen first causal test：

1. 用 neutral word-pair carriers + continuous human ratings 学 `RelationType` state；
2. residualize `OverallRelatedness` + lexical/frequency/concreteness/static-similarity/co-occurrence controls；
3. 在独立 unlabeled taxonomic-vs-thematic triad choice 中做 ± relation steering；
4. taxonomic steering 必须提高 taxonomic-vs-thematic choice logit，thematic steering 必须反向改变；
5. random/shuffled/generic-relatedness controls 不能复现；
6. 不允许 best-layer cherry-pick。

## 037 — 已撤销，禁止复活

Former `037_generic_generalization_licensing` 已 **KILL-NOVELTY / ARCHIVED**。

Hu, van Paridon & Lupyan (2026), arXiv:2607.04523 已直接研究 principled-vs-statistical generic-property distinction，并控制 prevalence / cue validity。再做 open-weight causal MI 只剩 behavior/factorization -> mechanism，违反 N2。

## v2.1 最重要纪律

Route C 合法：

```text
simple natural object / surprising phenomenon
→ benchmark-removal
→ N0/N1/N2
→ exact auditable substrate
→ obvious confounds
→ minimal causal-use question
→ mechanism 在执行中长出来
```

仍然绝对禁止：

- 用 GPU lottery 决定现象是否存在再改题；
- behavior paper -> patching/SAE 而没有新 object；
- probe-only / best-layer paper；
- null 后换 headline；
- 为了显得学术把简单题包装成多阶段 architecture；
- 为保护 5/5 而忽略 fatal collision。

## 本轮 broad Route-C search 已完成的 serious audit

至少 12 个 serious simple candidates 被真正推进到 strongest-neighbor / substrate 级别；只有 039 通过。已写入 failure library 的本轮 deaths 包括：

1. use vs mention / asserted vs quoted — **KILL-NOVELTY**；
2. speaker commitment / factivity — **KILL-NOVELTY**；
3. typicality vs frequency/commonness — **KILL-NOVELTY**；
4. action precondition vs effect — **KILL-NOVELTY**；
5. hard constraint vs soft preference — **KILL-NOVELTY**；
6. cause vs enabling condition — **KILL-NOVELTY**；
7. epistemic vs deontic modality — **KILL-NOVELTY**；
8. final goal vs subgoal status — **KILL-SCALE / KILL-BEHAVIOR**；
9. concrete vs abstract representation — **KILL-NOVELTY**；
10. causal vs correlational relation — **KILL-NOVELTY / KILL-BEHAVIOR**；
11. intentional lie vs honest error — **KILL-NOVELTY**, direct 2026 RIFT mechanistic collision.

Survivor #12 is 039 taxonomic vs thematic semantic relation.

Do not revive deaths by changing model/dataset/language/SAE/probe/patching method.

## 当前工作优先级

**默认不再 broad-search。** 现在从 topic discovery 转向 frozen execution：

1. **039 S0 first** — 成本最低、gold 最干净、最符合 Route C；
2. 038 ambiguity matched-pair S0 / causal calibration；
3. 036 Jones–Estes frozen behavior + causal microscope；
4. 034/035 按 implementation readiness 排期。

对 039，先做 obvious experiment，不要一上来扫 SAE/head：

```text
human RelationType axis 是否在 held-out lexical pairs 可测
+ 是否超过 generic relatedness/co-occurrence confounds
+ independent triad behavior 是否可用
→ 才进入 causal steering/patching
```

如果 frozen S0 失败，按 hard kill 结束/限制 claim，不得改成另一个 semantic relation paper。

## 失败记录纪律继续有效

任何执行中新发现的 fatal novelty/substrate/behavior 问题：

- 立即写 `rejected_candidates/` 或 archive record；
- 更新 root README / active register / handoff；
- count 不保护题目。

## 最终一句执行指令

> **Fresh register 已真正完成 5/5。不要从旧 2/5 prompt 重启找题；保持 034/035 headline 冻结，036/038 re-audit 已通过，039 是新的 Route-C simple-object 项目。下一步优先执行 039 frozen S0，只有出现 fatal collision 或用户明确要求时才重新 broad-search。**
