# Next-Chat Startup Prompt — Hamdi-Style MI Topic Search

Copy the text below into a new conversation.

---

请继续我在 GitHub 仓库 `Nhckdvrl/Interpretability-try` 中进行的 **ACL / EMNLP / NAACL 风格 mechanistic interpretability 找题工作**。不要重新从零 brainstorm，也不要让我重复前一轮背景。

## 第一步：先读取仓库最新权威状态

必须先仔细阅读：

1. `README.md`
2. `phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md` —— **最新、最高优先级跨对话 handoff**
3. `phenomenon_miner/NATURAL_QUESTION_GATE.md`
4. `phenomenon_miner/SCIENTIFIC_SUBSTRATE_GATE.md`
5. `phenomenon_miner/S0_FUNNEL_2026-08-31.md`
6. `phenomenon_miner/FAILED_TOPICS.md`
7. `archive/README.md`
8. `rejected_candidates/README.md`
9. 所有与新候选相关的 `rejected_candidates/*.md`，尤其最新四份：
   - `hamdi_search_addendum_2026-08-31.md`
   - `hamdi_search_terminal_addendum_2_2026-08-31.md`
   - `late_search_addendum_2026-08-31.md`
   - `final_convergence_addendum_2026-08-31.md`

如果旧 chat、旧 candidate 文件、旧 domain log 中的 `lead / HOLD / under audit / survivor` 与上述最新文件冲突，以**最新 terminal addendum + handoff** 为准。

## 当前权威状态

- 本轮新题：**0 个 PASS-REGISTER**。
- 不允许因为我要最终凑 5 个就降低标准；五个必须是真正完整通过 gate 的五个。
- 当前唯一非 terminal frontier：
  **Intervention Effect Direction ≠ Magnitude**，状态 `HOLD-FATAL-CONTROL / NOT REGISTERED`。
  它必须先排除 2026 `The Illusion of Intervention` 所揭示的 treatment-induced **user drift / latent-population confounding**：先在可解释 open models 上复现 `sign 基本正确 + magnitude 系统性放大`，再做 faithful negative-control/confounder correction。若 residual 消失，立即 `KILL-ARTIFACT`；在此之前禁止 probe/SAE/patching。
- `Statistical Evidence/Significance ≠ Effect Magnitude` 已经是 **KILL-MI-FIT**，不是活 lead。BEAR 只保留作 future infrastructure。
- `Prevalence ≠ Diagnosticity` 已经 **KILL-DATA**。
- `Truth ≠ Popular Belief` 已经 **KILL-N1**（KaBLE / belief-knowledge-fact object 已占）。
- `Assertion ≠ Presupposition` 已经 **KILL-DATA**。
- `Premise reversal blocks fallacies` 现在也 **KILL-S0**：ICLR 2026 的存在证据来自 PyETR 程序生成的 383 个形式逻辑问题，按当前 failure S0 synthetic-only 不够。

完整死亡列表一定先查 rejection logs；禁止换名字、换 dataset、换模型、换语言、换 prompt、换 MI 工具复活同一 scientific object。

## 我真正要的题目

不要给我“interpretability ideas”。我要 **scientific objects**。

优先两种 Hamdi-style 形状：

### A. Natural behavior → internal object → causal fork

像 arbitrary/random choice：普通 prompt 中行为异常先稳定存在，然后才问模型有没有 `choice mode`；因果实验最好能区分 `switch vs dial / reader vs writer / upstream gate vs downstream writer` 等真正 competing mechanism，而不是只证明某个 direction 可 decode。

### B. Mother axis A → 世界中天然正交的新 axis B

像 `knowledge ≠ ontology/existence`：两个变量在人类世界里本来就是两回事，有独立 external gold 和自然 cross-cells；即使模型最终分得很好，论文仍然有科学意义。

不要机械复制“reader/writer”或“X≠Y”的形式。问题本身必须先天然存在。

## 搜索策略必须调整

上一轮大量 `经典语言学/心理学变量 A ≠ B` 被 N0/N1 或 S0 打死。所以新一轮优先：

1. **2025–2026 strong mother anomaly**：系统扫 ACL / EMNLP / NAACL / ICLR / ICML / NeurIPS / TACL / CL / Nature / Nature MI / Nature Computational Science，找：
   - large、counterintuitive、cross-model behavior；
   - 有 modern open-weight models；
   - natural / externally grounded population；
   - row-level data/code 真公开；
   - mother 尚未完成 internal representation + causal explanation；
   - 最重要：我们能问一个**新的 scientific object**，而不是“解释 mother 的 headline”。
2. **Everyday deterministic behavior**：普通聊天/选择/回答里肉眼可见的稳定 bias，类似 arbitrary choice，不依赖 benchmark 或复杂 builder。
3. **External-world orthogonal axes**：只有在两个 axis 都有 independent objective/source/human gold、same natural units、足够 cross-cells、无需新人工标注时才进入 S0。

## 每个候选的硬流程

对内部生成的每个 idea：

```text
P0 Natural Question
→ classify Failure-mechanism / Factorization-object
→ 先查 internal negative memory
→ S0 actual artifact/effect audit
→ open-model capability/existence gate
→ N0 mother inclusion
→ N1 strongest-neighbor / successor attack
→ anti-narrowing
→ MI-fit + Hamdi-surprise
→ only then PASS-REGISTER
```

### Failure-mechanism S0

必须在 current analyzable open checkpoints 上已经存在 broad natural failure；默认至少 2/3 family 同方向；普通 faithful prompt；不能 synthetic-only；不能 post-hoc 筛 subset；保存 item-level output / scorer / revision。

### Factorization S0

必须：

- 两轴 independent external definition；
- 两轴 independent gold；
- row-level artifact 实际取得并解析；
- 实际数 cross-cells / matched units；
- random 20 source-row sanity audit；
- attrition / restriction budget；
- central gold 不能由我们新标或 LLM judge 提供；
- 不能为了四格造 synthetic examples。

如果 artifact 下载不了、字段只是 proxy、四格缺失、或必须连续限制 domain/language/subtype，立即 KILL，不要 PARK 来占位。

## N0 / N1 最容易犯的错误

以下默认拒绝：

- mother behavior → 我们做 mechanism；
- representation exists → 问是否 causal；
- 换模型 / dataset / language；
- mother 的 task 做更难；
- 只剩一个 subtype；
- 已有 joint two-label task → 我们 probe 是否 factorize；
- generic `knows/can do X but doesn't use X`；
- hidden-state-defined phenomenon；
- novelty 只能靠标题不断加 adjective。

N1 每个 serious candidate 至少主动找 3 个最危险 neighbor，尤其搜 2025–2026、arXiv、ACL Anthology、OpenReview、PMLR，并组合关键词：`representation / latent / direction / feature / circuit / SAE / activation patching / causal intervention / steering / disentangle / factorization`。

## MI 必须真正必要

只有 naturalness + S0 + N0 + N1 都过后，才问机制。

至少要有 2–3 个真的 competing mechanisms，例如：

- shared scalar vs independent axes；
- parallel representations vs overwrite；
- upstream prior vs downstream selector；
- content vs index/binding；
- reader/switch vs writer/gain。

因果实验必须能让这些机制给出不同结果，而不是“patch 后 accuracy 掉多少”。

## 继续找，不要停在当前 0 survivor

你的任务是继续扩大 **新的 mother families / natural phenomena**，死一个就把 death evidence 写进相应 `rejected_candidates/` 文档，然后继续找替补。

目标最终是 **5 个真正 PASS-REGISTER**；但任何时点都不准用 HOLD 或弱题凑数。若这一轮仍为 0，就明确写 0，并继续新的搜索空间，而不是降低 gate。

## 真 survivor 的最终输出格式

只有完整 survivor 才按以下 20 节给我：

1. Plain question
2. One example
3. Why this matters
4. Topic type
5. Mother paper
6. Hamdi-style extension
7. S0 Scientific Substrate：actual dataset/artifact、exact URL/repo、schema、objective gold、total N、label counts、2×2、matched count、20-row audit、attrition、restriction budget、是否需人工 annotation
8. Open-model viability
9. N0
10. N1：至少 3 strongest neighbors
11. Internal-history audit
12. Exact novelty
13. Forbidden claims
14. Mechanistic forks
15. Decisive causal experiment
16. Fatal controls
17. ACL/EMNLP title
18. Four-sentence abstract skeleton
19. Anti-narrowing verdict
20. Final verdict

最终 verdict 只允许：
`PASS-REGISTER / HOLD-SUBSTRATE / KILL-NOVELTY / KILL-NATURALNESS / KILL-CAPABILITY / KILL-DATA / KILL-INTERNAL-COLLISION`。

**最重要的一句话：**

> 在做 MI 之前，先确保 scientific object 已经真实、可观测、能在 open model 上研究；MI 的作用是告诉我们模型内部为什么会这样，或者它究竟把哪两个世界中本来不同的变量当成什么，而不是替一个 dataset 或 hidden state 编故事。
