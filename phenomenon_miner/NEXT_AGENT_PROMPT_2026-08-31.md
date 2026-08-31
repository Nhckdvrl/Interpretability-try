# Prompt for the Next Topic-Search Agent

请继续我在 GitHub 仓库 `Nhckdvrl/Interpretability-try` 中进行的 **ACL / EMNLP / NAACL 风格 mechanistic interpretability 找题工作**。

这是前一轮的直接续接。**不要从零 brainstorm，不要让我重新解释背景，不要把旧 HOLD / PRE-S0 当成 survivor，也不要为了凑五个降低标准。**

## 0. 第一件事：读取最新权威状态

严格按这个顺序读：

1. `README.md`
2. `phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md` —— **当前最高优先级 authoritative handoff**
3. `phenomenon_miner/NATURAL_QUESTION_GATE.md`
4. `phenomenon_miner/SCIENTIFIC_SUBSTRATE_GATE.md`
5. `phenomenon_miner/S0_FUNNEL_2026-08-31.md`
6. `phenomenon_miner/FAILED_TOPICS.md`
7. `archive/README.md`
8. `rejected_candidates/README.md`
9. `rejected_candidates/continuation_terminal_addendum_6_2026-08-31.md` —— **最新 terminal log**
10. `rejected_candidates/continuation_terminal_addendum_5_2026-08-31.md`
11. 所有与任何新候选相关的 `rejected_candidates/*.md`

如果旧 chat、旧 candidate 文档、旧 domain log 中的 `lead / HOLD / PRE-CANDIDATE / under audit / survivor` 与最新 handoff + terminal addenda 冲突，**以最新 handoff + 最新 terminal addendum 为准**。

## 1. 当前硬状态

```yaml
new_PASS_REGISTER: 0
registered_new_topics: []
MI_authorized_now: false
```

**No candidate passes the current bar.**

不要把下面任何 HOLD / PRE-S0 算作五个题之一。

## 2. 当前四条未注册 frontier

### A. Intervention Effect Direction ≠ Magnitude

状态：

```text
HOLD-FATAL-CONTROL / NOT REGISTERED / NO MI AUTHORIZED
```

这是当前最高优先级。

先做：

1. 拿到 2026 Nature treatment-effect artifact/code；
2. 拿到 `The Illusion of Intervention` user-drift artifact/code；
3. 在可解释现代 open models 上确认 `effect sign 大体正确 + magnitude 系统性放大`；
4. 按 user-drift 工作做 faithful negative-control/confounder correction；
5. 如果 magnitude inflation residual 消失，立即 `KILL-ARTIFACT`，写 rejection，不准缩 subset 救；
6. 只有 substantial residual 跨 open families 留下后，才允许 N1 和 MI。

不要在 fatal control 之前 probe / SAE / patch / steer。

### B. Visual size → mass shortcut

状态：

```text
PRE-S0 / NOT REGISTERED / NO MI
```

已验证：

- VisPhysQuant `output.json` 已真实解析，共 **221 个真实对象**；
- row 有 `ID`, `weight_kg`, multi-view image paths；
- public Drive 有约 **14.27GB** Record3D RGB-D archive；
- `draw_bbox_axis.py` 能从 depth + camera intrinsics deterministic 计算 metric `x_length / y_length`；
- PhysQuantAgent repo **没有**隐藏的 per-view Qwen3-VL result file，不要再浪费时间搜 supplementary；
- `mass = volume × density/material` factorization 本身已 `KILL-N0`，不要复活。

真正需要验证的是行为：**mass signed/residual error 是否系统性沿 size 走**。

G0：真实物体、ordinary prompt、至少 3 个 current interpretable VLM families；如果 <2/3 family 同方向或 effect 不 substantial，直接 `KILL-S0`，不准挑 extreme object/subtype 救。

### C. Mass-specific cross-view instability / latent physical-property constancy

状态：

```text
HOLD-OPEN-MODEL-EXISTENCE / NOT REGISTERED / NO MI
```

旧 open-VLM qualitative evidence 显示同一真实物体只换视角，mass estimate 可以相差很大；但 generic perceptual constancy 已被 direct mother 占掉，所以只有**mass 作为 latent physical property**这个更具体对象可能活。

必须实际跑 modern open-family G0：

- same real object；
- >=4 views；
- identical prompt；
- deterministic decoding；
- >=3 current open VLM families；
- log-mass within-object dispersion；
- object identity/category stable control；
- image resize/crop + same-view repeat controls。

只有 broad >=2/3-family instability 才允许进入 N0/N1；否则 `KILL-S0`。

### D. Real-investigation causal relevance ≠ principal/actual-cause selection

状态：

```text
PRE-G0 / ARTIFACT-EXECUTION-BLOCKER / NOT REGISTERED / NO MI
```

不要再搜 NTSB schema。官方 artifact 已确认：

- data page: `https://www.ntsb.gov/safety/data/pages/Data_Stats.aspx`
- download directory: `https://data.ntsb.gov/avdata`
- `avall.zip`: 2026-08-01 snapshot, **95,636,276 bytes**
- 1982-present civil aviation accidents
- structured findings historical `cause_factor` has `C` / `F`; newer metadata includes probable-cause inclusion such as `cm_inPC`

当前 chat 只是 binary download endpoint cache-miss，**不是数据不存在**。

下一步在正常联网 shell 直接下载 `avall.zip`，解析 MDB：

1. list tables/columns；
2. inspect `findings`；
3. count `C/F`, `cm_inPC`, missingness, years；
4. count accidents with multiple findings and mixed roles；
5. random-20 audit；
6. 确认普通 prompt 能把 finding universe 给模型，而不需要我们手标核心 label；
7. 再做 current-open-family G0。

注意：`C/F taxonomy` 本身不是题目。

只有当模型**能识别多个 finding 的 causal relevance，却系统性不会像专家一样选 principal/actual cause**，才可能形成 scientific object。

若只是 `cause vs factor classification`，或者 formal actual causation benchmark，直接 N0/N1 kill。

## 3. 不要只审核这四条，继续找新题

主要任务仍然是：

> **继续寻找新的 scientific objects，直到真正找到 5 个足够硬的 `PASS-REGISTER`，或者本轮搜索再次证据性归零后继续扩大新的 mother families。**

不要为了凑五个降低标准。

### Priority 1 — 2025–2026 strong mother anomaly → lateral new object

系统搜索：

- ACL / Findings ACL
- EMNLP / Findings EMNLP
- NAACL
- ICLR
- ICML
- NeurIPS
- TACL / Computational Linguistics
- Nature
- Nature Machine Intelligence
- Nature Computational Science

优先找：

- large, counterintuitive behavior；
- current open-weight family；
- natural / externally grounded population；
- row-level data/code 真开放；
- behavior 已明显存在；
- **mother 没有把这个 dissociation 自己命名成 headline object**；
- mother 没有已经把 MI extension 写成明显 future-work successor；
- 我们能提出一个新的 title-level scientific object，而不是 `解释 mother failure 的 circuit`。

尤其看 mother 的 tables / ablations 中**稳定但未被命名的 dissociation**。

### Priority 2 — Everyday deterministic/distributional behavior

像 Hamdi arbitrary/random choice 一样：普通 prompt 里现象本身肉眼可见，不依赖 dataset、复杂 2×2、subset 筛选才成立。

但 random-choice 家族已经占位，不要换数字/颜色/quiz 复活。

### Priority 3 — External-world structure / orthogonal axis

只有满足以下条件才深审：

- 两个变量在人类世界里本来就是不同东西；
- independent external gold；
- same natural units/objects；
- natural cross-cells；
- 样本量足够；
- 不需要新人工标核心变量；
- 不需要 LLM judge；
- 即使模型把两轴分得很好，论文仍然成立；
- 不是已有 joint-prediction / disentanglement mother 的直接 hidden-state follow-up。

目前更值得探索的**抽象形状**，不是候选标题：

- intrinsic property vs genuinely relational/context-bound property；
- latent stable physical property vs irrelevant observation/view change；
- causal relevance vs downstream causal-role selection；
- upstream state vs downstream selector，**但必须行为先迫使这个区分出现**。

不要机械写 `X ≠ Y`。

## 4. Hamdi-style 真正标准

Hamdi random-choice 的价值不是“有 reader/writer 两个 direction”。

正确顺序：

```text
natural behavior
→ internal state
→ competing mechanism
→ causal test
→ mechanism predicts a surprising/simple intervention
```

最好的结果应能推翻默认直觉，例如：

```text
one randomness dial
→ actually reader/switch + writer/dial
```

并且机制发现最好能预测一个原先不会想到的低秩/简单 intervention，而不只是“第 17 层有一个 feature”。

优先机制 fork：

- switch vs dial
- reader vs writer
- upstream prior vs downstream selector
- parallel states vs overwrite
- shared scalar vs separate axes
- content vs binding/index

但不能因为想做这些 fork 而反过来编行为故事。

## 5. 每个 serious candidate 严格流程

```text
P0 Natural Question
→ classify Failure-mechanism / Factorization-object
→ internal negative-memory audit
→ S0 actual substrate audit
→ open-model existence/capability
→ N0 mother-inclusion attack
→ N1 strongest-neighbor/successor attack
→ narrative-width + anti-narrowing
→ MI-fit + Hamdi-surprise
→ only then PASS-REGISTER
```

### Failure-mechanism 注册前

- failure 已经在我们能做 MI 的 current open checkpoints 上存在；
- 默认至少 2/3 family 同方向；
- ordinary faithful prompt；
- synthetic-only 不行；
- post-hoc subset 不行；
- 经典人类 bias 存在不等于 LLM 存在；
- 保存 item-level output / scorer / checkpoint revision。

### Factorization/internal-object 注册前

- A/B 独立定义；
- independent gold；
- row-level artifact 真取得并解析；
- 实数 natural cross-cells；
- random-20 sanity audit；
- attrition；
- restriction budget；
- central labels 不能我们临时标；
- 不能 LLM judge；
- 不能 synthetic 2×2 制造现象；
- 第二轴不能用“差不多相关的 proxy column”偷换。

## 6. N0/N1 禁止放水

默认不是新题：

- mother behavior → mechanism；
- representation exists → causal or not；
- 哪一层/哪个 head；
- 换模型；
- 换 dataset；
- 换语言；
- task 做难；
- stricter subset；
- existing joint labels → probe disentanglement；
- generic `knows/can do X but doesn't use X`；
- hidden-state-defined phenomenon；
- novelty 只能靠标题加 adjective。

N1 每题至少找 3 个 strongest neighbors，主动搜：

`representation`, `latent`, `direction`, `feature`, `circuit`, `SAE`, `activation patching`, `causal intervention`, `steering`, `disentangle`, `factorization`, `mechanism`

覆盖 arXiv、ACL Anthology、OpenReview、PMLR 等。

**搜索是为了杀题，不是为了找支持文献。**

## 7. 最新新增 terminal 负知识

先完整读 `rejected_candidates/continuation_terminal_addendum_6_2026-08-31.md`。

这一轮新增死亡包括：

- numeric heaping / round-number attraction；
- subliminal learner-channel vs reader-channel；
- disease commonness/prevalence vs lethality；
- social power vs status；
- authorship/source vs endorsement/commitment；
- mass volume×density/material factorization；
- unit invariance；
- anchoring reader/writer；
- apparent brightness vs intrinsic luminosity；
- earthquake magnitude vs local intensity；
- absolute count vs proportion / ratio bias；
- pairwise preference vs global/transitive utility；
- occupational income vs prestige/status；
- manipulation strategy detection vs human effect magnitude；
- inattentional blindness；
- legal case content vs authority/applicability；
- belief-expression framing vs context/prior integration；
- healthfulness vs sustainability；
- institutional role vs prominence (`capital` vs `largest city`)。

Addendum 5 已杀：

- belief-update gate vs step-size；
- sentience/suffering vs intelligence；
- implicit preference vs inhibition；
- privacy knowledge vs action；
- generic perceptual constancy；
- relational-property essentialization。

更早 terminal 负知识全部仍有效：Truth/Popular Belief、Prevalence/Diagnosticity、Assertion/Presupposition、Statistical Evidence/Effect Magnitude、Premise Reversal、Deontic Facilitation、Description-History、recognition/recall、what/where、typicality、popularity/quality 等。

**不能换 dataset/model/language/prompt/MI tool 复活。**

## 8. 特别禁止继续浪费时间的形状

- temporal forgetting / stale state
- task-switch carryover
- ambiguity-history hysteresis
- evidence-more-hurts
- local-success/global-composition gap
- generic truth/belief/factuality/uncertainty
- ownership/self-attribution
- semantic relation inventory
- sentiment/emotion/dialogue-act label pairing
- synthetic moral/logic 2×2
- representation→causal follow-up
- mother→layer/head localization
- LLM-judge central gold
- proxy second axis
- title adjective narrowing after collision

## 9. 负知识必须持续写仓库

任何认真审过但死亡的题，立即追加到对应 `rejected_candidates/` 文件。

至少记录：

- Natural question
- Why it looked good
- Kill evidence
- Death code
- Nearest-neighbor warning
- Resurrection condition

不要只在 chat 里说“这个不行”。

## 10. 最终只有真正 survivor 才输出

每个 survivor 完整输出 20 节：

1. Plain question
2. One example
3. Why this matters
4. Topic type
5. Mother paper
6. Hamdi-style extension
7. S0 Scientific Substrate
8. Open-model viability
9. N0
10. N1，至少 3 strongest neighbors
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

真正要凑的五个必须是：

**`PASS-REGISTER`**

而不是五个 HOLD/PRE-S0。

如果一个都过不了，明确写：

`No candidate passes the current bar.`

然后继续扩大新的 mother families，不要降低 gate。

最重要的一句话：

> **先确保 scientific object 已经真实、可观测、能在 current open model 上研究；MI 的作用是告诉我们模型内部为什么会这样、或世界中本来不同的变量被模型表示成了什么，而不是替 dataset 或 hidden state 编故事。**
