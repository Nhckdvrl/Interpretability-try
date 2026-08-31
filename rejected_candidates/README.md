# Rejected Interpretability Candidates

这里记录**一开始确实值得认真考虑，但后来被硬证据砍掉或明确降级**的候选题。

它和 `archive/` 不同：

- `archive/`：已经正式建项目、写过 G0/代码/计划，后来终止；
- `rejected_candidates/`：多数还停留在搜题 / paper audit 阶段，就因为行为、artifact、novelty、naturalness、surprise 或 exact mechanism collision 被提前杀掉。

## Search organization: one domain at a time

后续搜题**不再横向混扫若干互不相关的题**，而是一次锁定一个现象领域，尽量把该领域的候选空间扫透：

1. 先定义当前 domain 及其自然现象边界；
2. 广搜该领域已有 behavior / benchmark / mechanism / method 工作；
3. 对每个最初看起来值得认真考虑的题做 collision audit；
4. 被 kill 的题全部写入该 domain 的 rejection log；
5. 只有仍然存活的题才进入跨领域最终候选池；
6. 以后重新进入该领域时，必须先读对应 rejection log，避免重新发明旧题。

这套目录的目标是逐渐形成一个**按领域组织的负知识库**：不仅记录“哪些题不行”，还记录“为什么不行、以后看到什么相似题应该立即警觉”。

## Mandatory rejection fields

每个值得记录的 rejected candidate 至少写：

- **Natural question**：不提解释工具也能成立的一句话问题；
- **Why it initially looked good**；
- **Kill evidence**：行为证据 / 论文 collision / artifact failure 等；
- **Death code**；
- **Nearest-neighbor warning**：以后哪些换名、换 benchmark、换模型的版本也不应复活；
- **Resurrection condition**：只有出现什么新的自然行为证据 / artifact / decisive contrast 才值得重开。

## Surprise test

在 README 的硬门槛之外，再做一个高阶筛选：

> **如果最终结果成立，它是否可能让读者产生“原来模型是这样坏掉的 / 原来直觉错了”的感觉？**

如果无论结果如何都高度符合默认直觉，例如“语义不同所以表示不同”“更灵活的方法比线性方法拟合更准”，即使 technically novel，也应显著降级。

这个标准来自实际选题反馈：研究问题本身必须有趣，结果最好能打破一个自然默认直觉，而不是做完后让人觉得理所当然。

## Death codes

- `NO_NATURAL_BEHAVIOR`
- `DIRECT_MECHANISM_COLLISION`
- `NARRATIVE_COLLISION`
- `ARTIFACT_FAILURE`
- `NATURALNESS_FAILURE`
- `METHOD_COLLISION`
- `LOW_SURPRISE`
- `KILL-S0`
- `KILL-N0`
- `KILL-N1`
- `KILL-DATA`
- `KILL-P0`
- `KILL-INTERNAL-HISTORY`

## Domain / terminal logs

- [`agent_tool_use.md`](./agent_tool_use.md) — Agent / tool-use / execution failures
- [`cognitive_logical_reasoning.md`](./cognitive_logical_reasoning.md) — formal / conditional / logical reasoning phenomena; old `under audit` notes are superseded by newer terminal addenda
- [`cognitive_decision_making.md`](./cognitive_decision_making.md) — economic choice, legal judgment, anchoring, authority, risk, sunk cost
- [`factuality_information_conflict.md`](./factuality_information_conflict.md) — false premises, answerability, misinformation, source credibility, repetition
- [`multimodal_grounding.md`](./multimodal_grounding.md) — VLM perception–knowledge conflict and counterfactual visual grounding
- [`semantic_pragmatic_factorization.md`](./semantic_pragmatic_factorization.md) — semantic / pragmatic / discourse factorization kills
- [`risk_uncertainty_factorization.md`](./risk_uncertainty_factorization.md) — likelihood-vs-severity and epistemic-vs-aleatoric uncertainty collisions
- [`social_norm_factorization.md`](./social_norm_factorization.md) — social / moral norm factorization
- [`social_simulation_factorization.md`](./social_simulation_factorization.md) — social simulation and treatment-effect leads
- [`hamdi_search_addendum_2026-08-31.md`](./hamdi_search_addendum_2026-08-31.md) — early cross-domain hard kills
- [`hamdi_search_terminal_addendum_2_2026-08-31.md`](./hamdi_search_terminal_addendum_2_2026-08-31.md) — assertion/presupposition, prevalence/diagnosticity, significance/effect-size, etc.
- [`late_search_addendum_2026-08-31.md`](./late_search_addendum_2026-08-31.md) — late convergence kills and resurrection warnings
- [`final_convergence_addendum_2026-08-31.md`](./final_convergence_addendum_2026-08-31.md) — premise-reversal synthetic-only kill, off-trajectory robustness, multi-agent diversity, generation-vs-robustness
- [`continuation_mother_search_2026-08-31.md`](./continuation_mother_search_2026-08-31.md) — continuation mother-paper search kills including geographic direction/distance, forced-choice/indifference, ordinal/cardinal quantity and other direct-collision objects
- [`continuation_terminal_addendum_2_2026-08-31.md`](./continuation_terminal_addendum_2_2026-08-31.md) — popularity/quality, memory/control, rank/calibration, moral-ordering/intensity and related terminal objects
- [`continuation_terminal_addendum_3_2026-08-31.md`](./continuation_terminal_addendum_3_2026-08-31.md) — later terminal cleanup including recognition/recall, content/source, what/where and stale physical-cognition survivors
- [`continuation_terminal_addendum_4_2026-08-31.md`](./continuation_terminal_addendum_4_2026-08-31.md) — additional continuation hard kills; newer addenda supersede any remaining HOLD wording
- [`continuation_terminal_addendum_5_2026-08-31.md`](./continuation_terminal_addendum_5_2026-08-31.md) — belief-update gate/dial, species moral-status axes, implicit preference/inhibition, privacy knowledge/action, generic perceptual constancy, relational-property essentialization
- [`continuation_terminal_addendum_6_2026-08-31.md`](./continuation_terminal_addendum_6_2026-08-31.md) — numeric heaping, subliminal learner/reader, common/deadly, power/status, authorship/endorsement, mass volume×density, unit invariance, anchoring, astronomy/geophysics axes, ratio bias, preference transitivity, occupational income/prestige, manipulation detection/effect, inattentional blindness, legal authority, belief-expression framing, health/sustainability, institutional-role/prominence; also records blockers for the remaining frontiers
- [`continuation_terminal_addendum_7_2026-08-31.md`](./continuation_terminal_addendum_7_2026-08-31.md) — affective validation vs epistemic endorsement; feedback/update direction vs correction magnitude
- [`continuation_terminal_addendum_8_2026-08-31.md`](./continuation_terminal_addendum_8_2026-08-31.md) — no-resurrection alias lock; social cognition→action, population mean→heterogeneity, state-affordance, stated/revealed preference, causal overreach, probability/valence, geographic distortion families
- [`continuation_terminal_addendum_9_2026-08-31.md`](./continuation_terminal_addendum_9_2026-08-31.md) — **LATEST TERMINAL ADDENDUM / conversation closeout**; canonical summary of all serious deaths from the final continuation conversation plus the only four nonterminal execution frontiers
- [`001.md`](./001.md) — **legacy mixed-domain batch**，保留历史记录，不再继续追加。

## Authority rule

When statuses conflict, use this order:

1. `phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md` (newest contents)
2. newest `continuation_terminal_addendum_*_2026-08-31.md` — currently **Addendum 9**
3. other terminal addenda
4. domain logs
5. old chat / old `lead`, `PRE-CANDIDATE`, `HOLD`, `under audit` prose

A stale positive label is never evidence of survival.

## Mandatory pre-search check

任何新候选在进入 S0 前，除了 `phenomenon_miner/FAILED_TOPICS.md` 和 `archive/README.md`，还必须搜索本目录的 domain logs 与**最新 terminal addendum**。先把候选写成一句不含 dataset/MI 词的 scientific object，再写 5–10 个语义近邻/别名去搜负知识库。若 scientific object 已死亡，**换模型、换数据、换 prompt、换语言、换 MI 方法或换名字均不能自动复活**；只能满足该条目明确写出的 resurrection condition 后重新进入 P0/S0。