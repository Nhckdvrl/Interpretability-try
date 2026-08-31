# Prompt for the Next Topic-Search Agent

请继续我在 GitHub 仓库 `Nhckdvrl/Interpretability-try` 中进行的 **ACL / EMNLP / NAACL 风格 mechanistic interpretability 找题工作**。

这是前一轮的直接续接。**不要从零 brainstorm，不要让我重新解释背景，不要把任何 HOLD / PRE-S0 / REGISTERED-FRONTIER 算作 PASS，也不要为了凑五个降低标准。**

## 0. 第一件事：完整读取最新权威状态

严格按顺序读：

1. `README.md`
2. `phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md` —— 当前最高优先级 authoritative handoff
3. `phenomenon_miner/NEXT_AGENT_PROMPT_2026-08-31.md` —— 本文件
4. `rejected_candidates/continuation_terminal_addendum_9_2026-08-31.md` —— **最新 terminal negative memory**
5. `rejected_candidates/continuation_terminal_addendum_8_2026-08-31.md`
6. `rejected_candidates/continuation_terminal_addendum_7_2026-08-31.md`
7. `phenomenon_miner/NATURAL_QUESTION_GATE.md`
8. `phenomenon_miner/SCIENTIFIC_SUBSTRATE_GATE.md`
9. `phenomenon_miner/S0_FUNNEL_2026-08-31.md`
10. `phenomenon_miner/FAILED_TOPICS.md`
11. `archive/README.md`
12. `rejected_candidates/README.md`
13. 所有与任何新候选语义接近的 `rejected_candidates/*.md`

如果旧 chat、旧 candidate、旧 domain log、旧 frontier 中的 `lead / HOLD / PRE-CANDIDATE / PRE-S0 / survivor / under audit` 与最新 handoff 或 addendum 9 冲突，**以最新 handoff + addendum 9 为准**。

当前硬状态：

```yaml
PASS_REGISTER: 0
counts_toward_target_five: 0
MI_authorized_now: false
```

如果这一轮仍然没有题过门槛，就明确写：

`No candidate passes the current bar.`

然后继续扩大新的 mother families，不要降低 gate。

---

## 1. 新增硬规则：先做 semantic negative-memory audit，再搜论文

上一轮最大的浪费，是一些自然问题看起来很漂亮，但其实 2025–2026 已经把 title-level scientific object 直接占掉了。

因此任何新题在 P0 后，先做：

1. 用一句普通话/英文写 scientific object，不出现 dataset/benchmark/MI 方法；
2. 写 5–10 个语义别名/近邻说法；
3. 搜 `rejected_candidates/`, `archive/`, `FAILED_TOPICS.md`；
4. 如果同一个 scientific meaning 已经死掉，立即停止；
5. 只有没撞内部负知识，才做 strongest-neighbor 外部检索；
6. 只有 title-level object 看起来没被直接占，才值得做 S0。

**换 dataset、model、language、prompt、subset、CoT、MI tool、标题 adjective，不构成新题。**

---

## 2. 本轮刚刚死亡、绝对不要换名复活的题

完整死因看 `continuation_terminal_addendum_9_2026-08-31.md`。以下全部 terminal：

- affective validation / emotional support ≠ epistemic endorsement；
- feedback/update direction ≠ correction magnitude / step size；
- social-cue recognition ≠ accommodation / socially appropriate action；
- population mean / aggregate fit ≠ heterogeneity / dispersion / correlation structure；
- object identity / recognition ≠ state-dependent affordance / actionability；
- stated preference ≠ revealed preference / actual choice；
- study-design/evidence-boundary recognition ≠ causal-claim generation；
- likelihood/probability ≠ desirability/valence；
- geographic metric distance/reality ≠ semantic/cultural/landmark salience。

尤其注意：

`phenomenon_miner/frontier_social_state_routing_2026-08-31.md` 已经改成 **TERMINAL POINTER**。不要把 Social Agnosia / Enron / power-accommodation 再捡回来。

更早 Addenda 2–8 与 domain logs 里的死题也全部有效，包括 mass volume×density/material、generic perceptual constancy、belief-update gate/dial、privacy knowledge/action、recognition/recall、what/where、truth/popular-belief、prevalence/diagnosticity、assertion/presupposition、statistical significance/effect magnitude、ratio bias、preference transitivity、anchoring 等。

---

## 3. 当前只有四条 nonterminal execution frontier

**它们都不算 PASS。** 不要因为是 frontier 就美化成题目。

### A. Intervention Effect Direction ≠ Magnitude

状态：

```text
HOLD-FATAL-CONTROL / NOT REGISTERED / NO MI
```

先解决 user/persona-drift fatal control。

必须：

1. 获取 2026 Nature treatment-effect artifact/code；
2. 获取 `The Illusion of Intervention` drift artifact/code；
3. 在 current interpretable open models 上复现 sign mostly correct + magnitude inflated；
4. faithful 实现 drift/confounder correction；
5. residual 消失 → `KILL-ARTIFACT`，写 rejection，不准 subset rescue；
6. 只有 substantial residual 跨 open families 存在，才允许 N1，然后才可能 MI。

禁止 fatal control 前做 probes/SAE/patching/steering。

### B. Visual size → mass shortcut

状态：

```text
PRE-S0 / NOT REGISTERED / NO MI
```

已知真实 substrate：VisPhysQuant 221 real objects，true `weight_kg`，multi-view images，Record3D RGB-D，公开代码可算 metric size。

真正要验证的是：

> mass signed/residual error 是否系统性随 apparent/metric size 变化？

不是 generic mass error，也不是 `mass = volume × density/material`（后者已死）。

G0：>=3 current interpretable VLM families，ordinary identical prompt，真实对象，raw item-level outputs，pre-frozen controls；>=2/3 family broad effect 才活，否则 `KILL-S0`，不准挑 extreme subtype 救。

### C. Mass-specific cross-view instability

状态：

```text
HOLD-OPEN-MODEL-EXISTENCE / NOT REGISTERED / NO MI
```

验证同一真实物体只换视角时 mass estimate 是否仍大幅变化：

- >=4 views/object；
- identical prompt；
- deterministic decode；
- >=3 current open VLM families；
- within-object log-mass dispersion；
- identity/category stable control；
- resize/crop + same-view repeat controls；
- broad >=2/3-family effect 才活，否则 `KILL-S0`。

不要重新包装成 generic perceptual constancy。

### D. NTSB causal relevance ≠ causal-role selection

状态：

```text
REGISTERED-FRONTIER / DELEGATED-G0 / NOT PASS-REGISTER / NO MI
```

这是**执行追踪注册**，不计入五个题。

正确问题：

> 在真实事故中，模型是否能识别哪些 finding 是 causally relevant，却仍分不清调查员标为 cause 的 finding 和 contributing factor？

关键语义：

```text
cm_inPC = probable-cause statement 中被引用为 cause OR contributing factor
legacy cause_factor = C vs F role label
```

**绝对不要**把 `cm_inPC=TRUE` 当 principal cause，也不要假设每个事故只有一个 C。

本地执行由以下文件负责：

1. `phenomenon_miner/REGISTERED_FRONTIER_NTSB_CAUSAL_ROLE_2026-08-31.md`
2. `phenomenon_miner/NTSB_LOCAL_AGENT_HANDOFF_2026-08-31.md`
3. `phenomenon_miner/NTSB_LOCAL_AGENT_PROMPT_2026-08-31.md`

如果本地 agent 已经跑出结果，下一轮必须**先读它提交的 audit/results/rejection**，再决定 NTSB 是 KILL 还是继续 N0/N1；不要重复下载/重复定义任务。

---

## 4. 不要只处理这四条：继续找新的 scientific objects

目标仍然是找到真正的 5 个 `PASS-REGISTER`，但绝对不能为数量放水。

优先搜索 2025–2026：

- ACL / Findings ACL
- EMNLP / Findings EMNLP
- NAACL
- TACL / Computational Linguistics
- ICLR / ICML / NeurIPS
- Nature / Nature Machine Intelligence / Nature Computational Science

重点不是论文标题已经写出来的 gap，而是：

> **strong mother paper 的 table / ablation / appendix 中存在稳定、反直觉、跨模型的 residual anomaly，但作者没有把它命名成 headline scientific object，也没有已经做掉明显的 MI successor。**

优先三类来源：

1. **Everyday deterministic/distributional behavior**：普通 prompt 就能看到，不依赖 benchmark 才成立。
2. **External-world grounded distinction**：两个量本来就在世界里不同，有 deterministic/expert/human gold，自然 cross-cells。
3. **Strong mother anomaly 的 lateral extension**：不是解释 mother 的主结论，而是从一个未命名 anomaly 横向长出新的 scientific object。

不要机械生成 `X ≠ Y`。

---

## 5. 严格 funnel

每个 serious candidate 必须走：

```text
P0 natural question
→ semantic negative-memory audit
→ strongest-neighbor/title collision attack
→ S0 real substrate
→ current-open-model existence/capability
→ N0 mother-inclusion attack
→ N1 strongest-neighbor/successor attack
→ anti-narrowing / narrative width
→ MI-fit / Hamdi-surprise
→ PASS-REGISTER
```

### Failure-mechanism 在注册前必须满足

- failure 在 current analyzable open checkpoints 上真实存在；
- 默认 >=2/3 genuinely different families 同方向；
- ordinary faithful prompts；
- no synthetic-only existence；
- no post-hoc subset rescue；
- effect scientifically substantial；
- item-level outputs/scorer/exact checkpoint revisions 保存；
- N0/N1 通过。

### Factorization/internal-object 在注册前必须满足

- A/B 在模型外独立定义；
- independent deterministic/expert/human gold；
- row-level artifact 已真实获得和解析；
- natural cross-cells 已计数；
- random-20 sanity audit；
- attrition/restriction budget；
- core axis 不由我们临时人工标；
- central gold 不用 LLM judge；
- 第二轴不是 proxy；
- 不允许 synthetic 2×2 制造现象。

---

## 6. N0/N1 不许放水

默认不是新题：

- mother behavior → mechanism；
- `representation exists` → `is it causal?`；
- 哪层/哪个 head；
- 换模型/dataset/language；
- generic `knows X but doesn't use X`；
- title 加 adjective；
- existing joint labels → probe disentanglement；
- hidden-state-defined phenomenon；
- central LLM judge；
- proxy second axis。

N1 是为了**杀题**。至少查 strongest neighbors，覆盖 arXiv / ACL Anthology / OpenReview / PMLR / relevant journals，主动搜 mechanism-adjacent 词：

`representation`, `latent`, `direction`, `feature`, `circuit`, `SAE`, `activation patching`, `causal intervention`, `steering`, `disentangle`, `factorization`, `mechanism`。

---

## 7. Hamdi-style surprise 标准

最终 MI 不是“找到表示”，而应有 competing causal mechanisms，并最好出现这种结果：

```text
natural intuitive mechanism
→ causal test says intuition is wrong/incomplete
→ decomposition predicts a simpler intervention
```

例如 switch vs dial、reader vs writer、upstream prior vs downstream selector、parallel states vs overwrite、shared scalar vs separate axes、content vs binding/index。

但这些只能在行为已经迫使区分后使用，**不能反过来为了想做 reader/writer 而编一个行为题。**

---

## 8. 负知识必须落仓库

任何认真审过但死亡的题，立即写进 `rejected_candidates/`，至少包含：

- Natural question
- Why it looked good
- Kill evidence
- Death code
- Nearest-neighbor warning
- Resurrection condition

重要的新死亡再追加到新的 `continuation_terminal_addendum_*`，并更新 `rejected_candidates/README.md` 的 latest pointer。

不要只在 chat 里说“不行”。

---

## 9. 这一轮的执行风格

不要长时间只汇报“还在搜”。尽快给出可判定动作：

- 找到候选 → 先 negative-memory/N0/N1 杀；
- 找到 real substrate → 真正解析/计数；
- 有现成 G0 scaffold → 直接跑或明确交给本地 agent；
- 死亡 → 立即写 rejection；
- 存活 → 明确它当前过到哪一 gate，不要提前叫 candidate/PASS。

最终目标仍是 5 个真正 `PASS-REGISTER`，但当前起点就是 **0**。
