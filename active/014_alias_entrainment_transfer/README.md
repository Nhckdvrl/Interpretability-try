# 014 — Alias Entrainment Transfer：contextual entrainment 附着在**看见的表面形式**上，还是在**被激活的实体**上？

**Status:** `KEEP / HOLD-FOR-CONSTRUCT-VALIDATION` — phenotype 成立，**entity 解释尚未成立**；phase 4 被 `configs/contract_d1.yaml` 阻塞
**Created:** 2026-08-29
**Canonical shortlist:** Batch 3 Hamdi-mother-paper #1
**One-line question:** **Contextual entrainment attaches to the surface form that was seen, or to the entity that was activated?**

---

## 0. 授权状态

phase 1 / phase 2 运行于 2026-08-29，依据当时的 `candidate_pool/AUDIT_REGISTRY.md`；该文件其后在 v4 重构中被 `phenomenon_miner/AUDIT_REGISTRY.md` + `FINDING_RULES.md` 取代。

v4 的两项 discovery 前置——Tier S 要求的 20 对 alias conventionality / 歧义 / 频率分层人工审计，以及 N1 closure——**未执行**，由项目所有者于 2026-08-29 审阅后豁免。本项目据此在新注册表中登记为 `validation_authorized: true`。

记为豁免而非"已完成审计"，是为了让这一区别留在记录里。D0 构建期间实际做过的是两轮抽样检查，它们直接导致了 SEMREL 选择约束、正字法分层，以及 NED frame 泄漏的发现。

---

## 0b. 2026-08-29 external review — 现象成立，entity 解释不成立

外部 review 指出并经我逐条核实成立的三件事：

1. **`opaque_strict` 是正字法 opaque，不是概念 opaque。** 150 对全审计结果：
   `compositional` 39%、真正 `coref_conventional` 只有 **33%**、完全不同指 5%
   （`Mr Bean/Rowan Atkinson`、`Ashley O/Miley Cyrus`、`Davy Jones/David Bowie`、
   `Pink City/Los Angeles` 等）。见 [`data/D0_ALIAS_AUDIT_VERDICT.md`](data/D0_ALIAS_AUDIT_VERDICT.md)。
2. **UNREL 有真 bug**（我在修 SEMREL 时引入）：它取的是 URI 顺序后 1/3，不是相似度最低层。
   实际 median sim 0.60 vs SEMREL 0.78。所有 UNREL-based 结论（H2、Gemma `UNREL=+6.51`）作废。
3. **`ALIAS > SEMREL` 排除不了 pair-specific learned association。** knowledge gate 也不能——
   两种解释都预测"没学过 A–B 关系时 transfer 消失"。所以 gate interaction 证明的是
   *transfer 依赖已学到的关系*，不是 *该关系被表示为共享实体身份*。

**但现象没有死**：在审计后的干净子集上效应反而更强
（audit-clean ∧ `opaque_strict`：**+2.06 / +1.31 / +2.25 nats**，三家族 CI 均不含 0）。

因此 `mechanism_B_shared_entity_representation` 这个名字在解释上更正为 **shared upstream
cause**：phase 2 排除的是"完全独立的 alias 通路"，不是证明 head 内部有实体表征——phase 3 恰恰
否掉后者。

下一步不是 phase 4，而是 [`configs/contract_d1.yaml`](configs/contract_d1.yaml)：
独立的 RedirectQA confirmatory bank + 第五个条件 `ASSOC`（强关联但**不同指**），
决定性判据是 `ALIAS > ASSOC`。过不了就放弃 entity 解释。

---

## 1. Mother paper 与它确实解决了什么

Niu et al., ACL 2025 Main (**Outstanding Paper**),
[*Llama See, Llama Do: A Mechanistic Perspective on Contextual Entrainment and Distraction in LLMs*](https://aclanthology.org/2025.acl-long.791/) ([arXiv:2505.09338](https://arxiv.org/abs/2505.09338), [code](https://github.com/frankniujc/entrainment)).

Mother result（已解决，不可重述为我们的贡献）：

```text
只要 token t 在 context 里出现过，
后续 logit(t) 就系统性升高，
即使 t 与问题完全无关、甚至是 Brown corpus 随机 token；
一小批 attention head（entrainment heads）因果地承载了大部分效应。
```

Mother 的度量就是 `Δℓ(t) = ℓ(t | context+query) − ℓ(t | query)`，四种 context（related / irrelevant / random / counterfactual），LRE 数据集，Llama-2/3.1 + GPT-2 XL。

两个 successor（都必须一起算 collision）：

- [*Sentence-Level Contextual Entrainment in LLMs*](https://arxiv.org/abs/2606.24077)，26 模型 / 7 家族。但它明确定义 "the response y is **exactly the context c**" 或 context 的连续子串——**被打分的字符串仍然出现过**。
- [*Better and Worse with Scale*](https://arxiv.org/abs/2604.13275)，Cerebras-GPT / Pythia 上的 scale sign-split（semantic context 随规模减弱，non-semantic context 随规模增强）。同样只做 exact token 匹配。

三篇都没有测过**被打分的目标串从未在 prompt 中出现**的情况。

## 2. Mother question

> **上下文"感染"的因果单位，是出现过的词，还是被激活的实体？**

日常例子（一句话就能懂）：

```text
context 里只出现 "International Business Machines"
后面模型要写 "IBM"
"IBM" 这三个字符从头到尾没出现过
它会不会也被 entrain？
```

同类：`Bombay → Mumbai`、`Formosa → Taiwan`、`Lee Jun-fan → Bruce Lee`、`Britain → United Kingdom`。

## 3. Scientific fork（这是本题存在的理由）

```text
若 alias 完全不 transfer
  → mother phenomenon 本质上是 lexical reoccurrence / copy bias，
    semantic factor 只调 gain，不改变 causal unit。

若 unseen canonical alias 也被提升，且超出 semantic priming
  → context 中被激活的至少部分是 entity-level salience state，
    entrainment 先经过实体表征，再落到一个从未出现的词形上。
```

两个方向都是对 mother 理解的实质修正，因此这是一个 **decisive** 而不是 confirmatory 的实验。

## 4. Phase 1：四条件，不做 MI

按用户裁定，第一阶段**不碰 probe / patching / head ablation**。只看 target logit。

对每个实体 E 与它的两个名字 `A`（context 中出现的那个）、`B`（被打分、从未出现的那个）：

| 条件 | context 里插入的 mention | 含义 |
|---|---|---|
| `EXACT` | `B` 本身 | mother 复现，transfer 的上界 |
| `ALIAS` | `A`（`B` 串完全不出现） | **新条件** |
| `SEMREL` | `C` = 同类型、非同指、与 `B` 语义最相关的实体名 | **决定生死的对照** |
| `UNREL` | `D` = 同类型、与 `B` 低相关的实体名 | 一般 distractor 基线 |
| `NOCTX` | 无 context | Δ 的基准 |

度量（mother-faithful）：

```text
Δ_cond = log P(B | context_cond + query) − log P(B | query)
```

`B` 从来不是 query 的正确答案：query 是一条独立的、与 E 无关的 PopQA 问题，gold ≠ B。所以任何 Δ>0 都是 distraction，不是任务表现。

**关键判据一句话：`ALIAS > SEMREL` 必须先稳定出现。** 否则本题直接死成 semantic priming。

## 5. 为什么 SEMREL 不是随便挑的

这是本题唯一真正的杀点。因此：

1. `C` 由**模型外部**的 encoder（`BAAI/bge-large-en-v1.5`）在同类型实体池里选 **sim(C,B) 最大**的非同指实体——即最强可能的 semantic-priming 对照，而不是一个弱对照。
2. 主分析同时报告一个 **similarity-matched 子集**：只保留 `sim(C,B) ≥ sim(A,B)` 的 item。在这个子集上 alias 的表面语义相似度**更低**，若仍然 `ALIAS > SEMREL`，semantic priming 无法解释。
3. 主分析额外做回归 `Δ ~ sim(mention,B) + is_alias + n_tokens(mention) + (1|item)`：问 `is_alias` 是否在相似度的平滑函数之上仍有效应。

## 6. 正字法分层（第二个杀点）

`International Business Machines → IBM` 是**表面可推导**的（首字母）。如果 transfer 只出现在这类 pair 上，那它可能只是 acronym formation，仍然是 surface。因此每个 pair 打三种标签：

```text
acronym   B 是 A 的首字母缩写（或反之）
partial   共享至少一个完整词，但互不为子串
opaque    无共享词、非缩写、无字符派生关系   ← money stratum
```

`opaque` 层（`Bombay→Mumbai`、`Formosa→Taiwan`、`Lee Jun-fan→Bruce Lee`）必须单独成立。

## 7. Capability gate（012 的教训）

null 只有在模型确实知道 A 和 B 同指时才可解释。因此每个 ordered pair 先过一个**反平衡双内容选项** probe（012 r3 学到的形式，避免 yes/no 答案位置 artifact）：

```text
Q: Which of the following is another name for Bombay?
Options: (A) Mumbai  (B) Delhi
A: (
```

两种选项顺序都必须答对，item 才进入主分析集合。另有一个自由生成的次级 readout（`Bombay is another name for the city of` → 目标是否在 top-5）。

若某家族的 gated 分析集合 < 60 items，该家族判 `CAPABILITY-FLOOR`，其 alias 数字不解释。

## 8. Frozen 判据（运行前冻结，见 `configs/contract_r1.yaml`）

```text
H1 复现   median Δ_EXACT ≥ +1.0 nats，且 >0 的 item 比例 ≥ 0.80，三家族都成立
H2 必要   median(Δ_ALIAS − Δ_UNREL) > 0，bootstrap 95% CI 不含 0
H3 决定   median(Δ_ALIAS − Δ_SEMREL) > 0，bootstrap 95% CI 不含 0
            且在 similarity-matched 子集上同号
            且在 opaque 层上同号
            且回归中 is_alias 系数 > 0
H4 一致   H3 在 ≥2 / 3 家族同号
transfer  ratio = (Δ_ALIAS − Δ_SEMREL) / (Δ_EXACT − Δ_SEMREL) ≥ 0.15
```

**PROMOTE**（进入 phase 2 = entrainment-head ablation 是否专门消掉 alias-transfer 分量）当且仅当 H1–H4 与 transfer ratio 全部满足。

**KILL** 条件：

- H3 在任一形式上失败（尤其是 similarity-matched 子集或 opaque 层翻号）；
- transfer 只在 `acronym` 层存在；
- H1 都不成立（说明 harness 没测到 mother phenomenon，是实现问题，先修 harness 而不是解释结果）。

禁止的续命：换 frame、换 carrier、换模型直到显著、把 SEMREL 换成更弱的对照、把 gate 放宽。

## 9. D0 数据

- **来源**：[PopQA](https://huggingface.co/datasets/akariasai/PopQA)（Izacard/Asai et al., 2023），本地缓存，14,267 条，自带 Wikidata URI、`s_aliases`/`o_aliases`（Wikidata CC0）与 Wikipedia 月浏览量 popularity。
- **alias pair**：由 PopQA 自带的 Wikidata alias 字段生成，经 ASCII / 长度 / 互不为子串 / 非纯标点变体过滤。
- **entity type**：由实体在 PopQA 中承担的关系角色推断（`person` / `city` / `country`）。
- **carrier query**：同样取自 PopQA 的自然问题，类型匹配（person→`director`，city→`capital`，country→`country`），gold ≠ B，且 carrier 实体与 E 无重叠。
- **人工审计**：随机 20 条，按仓库 D0 规则记录 ID 与结论。

没有任何 synthetic 语料；插入 frame 是两条固定的语义漂白句，是最小因果对照，不承担 naturalness 或 effect size。

## 10. 如果 phase 1 通过，phase 2 是什么

只有此时才动 MI，而且是**解释一个已经发现的新行为**，不是靠 MI 造题：

用 mother 的 differentiable-masking 方法定位 entrainment heads（在 `EXACT` 条件上），然后问：

```text
把这批 head 置零，是否**选择性地**消掉 alias-transfer 分量
（Δ_ALIAS − Δ_SEMREL），而不是等比例地压掉所有条件？
```

- 若 alias 分量与 exact 分量被同一批 head 同等地消掉 → 机制 B：entrainment 作用在一个已经 canonicalize 的实体表征上。
- 若 head ablation 只消 exact 分量、alias 分量存活 → 机制 C：alias 效应走另一条通路，本题变成 "两种 entrainment"。
- 若 alias 分量本来就不存在 → phase 1 已 KILL，不进入这里。

## 11. Collision 边界（2026-08-29 复检）

| 邻居 | 它占了什么 | 为什么没占本题 |
|---|---|---|
| Llama See, Llama Do (ACL 2025) | token 级 reappearance + entrainment heads | 打分目标必须出现过 |
| Sentence-Level Entrainment (2026) | 整句 reappearance，26 模型 | 明确要求 y 是 context 的精确串/子串 |
| Better and Worse with Scale (2026) | entrainment 的规模符号分裂 | 仍是 exact token 匹配 |
| Semantic priming in LMs (Misra 2020; Michaelov 2021/2024) | 相关词提升目标概率 | 这正是我们的 SEMREL 对照，不是我们的 claim；本题问的是同指是否在相似度之上还有额外分量 |
| Entity linking / coreference with LLMs | 符号层别名归一化 | 与 next-token distraction 的因果单位无关 |

允许的最强 claim（若 phase 1 通过）只能是：

> Contextual entrainment transfers to canonical aliases that never appeared in the prompt, beyond what similarity-matched semantic priming predicts; the causal unit is therefore at least partly entity-level rather than purely lexical.

不得声称首次发现 entrainment、首次发现 semantic priming、或首次发现 LLM 会被无关上下文干扰。
