# Failed / Routed Topics

日期：2026-08-29  
用途：**防止旧题换名复活，提炼下一轮找题的 hard lessons。**

本文件不是 archive 的替代品。`archive/` 保存完整实验、代码、raw result 和正式 verdict；这里仅保存当前研究决策需要记住的**死亡原因**。

状态含义：

- `KILL`：scientific contract 已被证伪或不满足 discovery gate；不重开。
- `ROUTE`：问题本身可能真实，但已被更宽 mother work 吸收，不能 standalone。
- `HOLD-DATA`：问题仍有意义，但自然 source/gold 不成立；不能先注册再救。
- `LEGACY-OUT`：旧文档曾写 candidate/promoted，但不属于当前 v4 queue；旧标签无当前权威性。

---

## 1. v4 重审后明确移出的题

| topic | verdict | 为什么死 / 被 route | 以后不要怎么复活 |
|---|---|---|---|
| **First-Negative-Evidence Harm** | `KILL / ROUTE` | `Anchored Confabulation` 已占 partial-evidence non-monotonic harm；剩余“negative subtraction”需要在人为 MCQ prompt 中插入 verified-false option，再拼 mention/deletion factorial，scientific object 太依赖测试协议 | 不换 GPQA/MMLU/ARC，不靠更多 option template 把 subtype 包装成新 mother phenomenon |
| **Packed–Unpacked Event Splitting** | `TERMINAL` | 正式验证暴露 operationalization artifact：reorder、nested refinement、repacking recovery 等关键结构没有支持预期 splitting account | 不换 wording/branch taxonomy/概率接口寻找能出现 effect 的版本 |
| **Existential Witness Collapse** | `HARD KILL` | Qwen3-8B 在完整 capability denominator 上 40/40 通过 recognition/action controls，但 unknown 条件几乎没有 illegal witness join（`p_collapse≈9.4e-5`，0 strong cases） | 不换弱模型、阈值、自然域或 prompt 直到出现 fusion |
| **Inadmissible-Evidence Persistence** | `TERMINAL HOLD-D0` | D0 contract 无法形成足够硬、自然、独立且可冻结的 `never-seen / admissible / struck` counterfactual evidence chain | 不用 synthetic legal stories 或主观 legal gold 补数量 |
| **Source-Discount Recovery** | `HARD KILL` | 自然数据与 memory gate 可成立，但两模型在 108 对上都没有达到 source-weighting capability denominator；`0/108` weighting-capable pairs，目标 phenotype 无合法分母 | 不改 belief readout/threshold，不跑第四 shot 或扩大 panel 救 capability floor |
| **Burden-Placement Null-Case Reversal** | `KILL-DISCOVERY-DATA` | decisive contrast 要在同一 unresolved evidence 下只交换 burden holder；现实案件里 burden allocation 本身属于适用法律，不能自然自由交换，matched gold 会变成人工改写法律世界 | 不自造“同案只换 burden”故事，不把 doctrinal importance 当数据可行性 |
| **Short-Circuit Side-Effect Leakage** | `ROUTE → CoRE` | CoRE 已系统建立 `correct final output + wrong intermediate execution state` 的 Superficial Execution；value/effect gate 是漂亮 subtype，但不够独立成为 main-paper mother question | 可作为 CoRE-style diagnostic/control，不 standalone 重命名 |
| **SQL UNKNOWN Interface Collapse** | `ROUTE → Squirrel-Semantic` | Squirrel-Semantic 已显式覆盖 SQL NULL/3VL semantic error family；WHERE/CHECK designated-value pair 过窄 | 可作为 taxonomy item，不占独立 research slot |
| **Synonym-Saturation Escape in Semantic BM25** | `ROUTE-OUT-OF-SCOPE` | scientific question 可做，但 mother 是 cross-encoder IR circuit；剩余 saturation counting-unit 过窄，偏离当前 LLM/agent natural-phenomenon主线 | 不因已有 circuit 很方便解释就降低选题范围标准 |
| **GeoTemporal Binding Bottleneck** | `ROUTE → MOTHER-MECHANISM-FOLLOWUP` | GeoTemp mother 已经直接建立“geography/time components individually work but joint composition fails”的 headline；剩余 retrieval vs arithmetic vs binding 只是解释 mother failure 的 localization，不再有独立 phenotype budget | 不把 mother 已有的 component-good/joint-bad 重写成新现象；若以后做，只能明确作为 GeoTemp mechanism follow-up，并先冻结与 mother 不同的 causal question |
| **Causal Retrieval Schedule** | `ROUTE → TARGETED-MECH-FOLLOWUP` | mother 已有 hidden state 对 future retrieval-head schedule 的预测信号；剩余问题主要是 `predictive representation → causal plan?`。它没有独立 natural behavioral phenotype/D0，而且与 `candidate_topics` Topic 15 “predictive state formed but downstream action did not use it”属于同一高风险 identification pattern | 不因“如果 causal 会很酷”就把 correlation→causal validation 伪装成 phenomenon candidate；除非先出现一个独立行为 anomaly，需要该 schedule 才能解释 |
| **Dead-Branch Residue after Invalidation** | `KILL / ROUTE-STANDALONE` | Belief revision、stale premise propagation、stale memory→policy adaptation 已占据“新证据使旧 state 失效但 downstream 行为仍沿旧 state”的 mother question；把 stale state 换成 planning branch 尚不足以形成新 title-level conclusion | 不仅靠 ALFWorld/PDDL 或“branch”名词重开。只有出现 predecessor work 没覆盖的 branch-graph structural signature（例如 closure-descendant-specific attraction 且 sibling/shared-prefix 不受影响）时，才能以全新 claim 重新做 N0 |

### 2026-08-29 re-audit lesson

这三条新移出题暴露了一个需要长期记住的选题偏差：

```text
mother behavior 已经成立
+ mother/neighbor 又给了一个漂亮 representation / decomposition
→ 很容易误把“下一步机制问题”当成“新的现象题”
```

v4 以后必须问：

1. **我们的 headline behavior 是否真的不是 mother 的 headline？**
2. **D0 是否能在不看 hidden state 的情况下定义一个独立、自然、可冻结的 phenotype？**
3. 如果答案是否定的，它应进入 `MECH-FOLLOWUP`，而不是占用 phenomenon discovery Tier S。

---

## 2. 正式 archive 的关键死亡经验

| archive project | terminal reason | 可复用教训 |
|---|---|---|
| `001_role_value_binding` | **STOP_NO_NATURAL_BINDING_FAILURE**：BFCL V4 `simple_python` 中 174 eligible samples，Qwen3-4B 与 Gemma3-4B 都是 `0/174` strict natural role-value binding failures | 不从 benchmark 总错误率猜细分 phenotype；先用公开 output 做零成本 natural preflight |
| `002_facts_vs_shortcuts_arbitration` | 宽行为已由 EACL 2026 mother paper直接建立，数值表示/输出 gap 等机制近邻也很强；作为旧 mechanism-followup snapshot 归档，不再作为独立 discovery 题 | 已知行为做 mechanism follow-up 必须明确授权；不能把 mother paper 的行为贡献重新包装成“新现象” |
| `003_decoy_dissociation` | 冻结 G0：Qwen `0/806` strong reversals，Gemma `71/4184=1.70%`，均达不到每模型 5% 且两模型通过的预注册 gate | 经典人类 bias 不保证现代 LLM 上存在同一 strict item-level phenotype；null 就停 |
| `004_deontic_facilitation` | 真 matched Wason modality swap 后 Qwen/Gemma 都远低于 effect gate，`0/32` strong pairs | 人类母现象的 dataset-level差异不能替代最小因果 contrast；matched manipulation 不成立就不做机制 |
| `005_anti_inference_discount` | Qwen/Gemma comprehension 大体可过，但 natural direct-vs-inference discount 极小，same-history bridged residual≈0 | “理解了却不用”的强 claim 必须建立 residual；如果显式 acknowledgement 后差距消失，就不能升级成 routing failure |
| `006_bayesian_latent_inference_use_gap` | custom task/interface 生成 apparent gap；跨模型不稳定；BayesBench 又占领宽 inference→use narrative | custom-only 不能承担 mother phenomenon；跨模型 G0 和 collision audit 必须先于 probe/patching |
| `007_choice_supportive_ownership_bias` | Qwen 是 own-specific suppression，Gemma 是 own/other 都 anchoring；同一 phenotype 未跨模型成立，第二公开任务也未闭合 | 不把不同家族的不同错误硬合成“普遍机制” |
| `008_reliability_weighted_cue_integration` | 文本显式数字 vs 图像读取成本不对称造成 artifact；同时已有 Bayesian cue-combination 工作覆盖宽 mother | stimulus modality/读数难度不对称可以制造假融合；artifact + collision 任一都足以停 |
| `009_packed_unpacked_event_splitting` | framing/operation controls 不支持预注册结构 | branch order、nested refinement、repacking 必须在模型调用前冻结为 fatal controls |
| `010_inadmissible_evidence_persistence` | terminal D0 contract：自然 source/gold/独立性无法满足，而不是靠 synthetic filler 解决 | D0 feasibility 属于选题；数据不硬就是选题没完成 |
| `011_existential_witness_collapse` | capability-gated clean null | 当强模型完整通过 denominator 并稳定保持规范行为，继续找 positive 是 rescue |
| `012_source_discount_recovery` | source-weighting capability floor | 目标 downstream operator 本身不会时，memory/recognition 再漂亮也不能定义 dissociation |

完整证据仍看 [`../archive/README.md`](../archive/README.md) 及各项目 `FINAL_VERDICT.md` / README。

---

## 3. 从当前树移除的 legacy 状态文档

这些文件过去曾叫 `candidate`、`phenomenon` 或 `promoted`，但标签来自 v4 之前，继续留在当前树会误导状态，因此只保留在 Git history。

### Redundant-Converse Composition Collapse — `LEGACY-OUT`

旧 `promoted/001` 后来已经自我降级为 `DOWNGRADED/HOLD`：现象依赖人工空间 relation world 与 direct-choice interface，自由生成中效应基本不稳。可记住的教训是：**structured-output/interface-specific anomaly 不能因为 effect 大就自动成为自然现象。**

### Evidence-Induced Referent Displacement — `LEGACY-OUT / NOT CURRENTLY ADJUDICATED`

旧 `promoted/002` 有很有趣的 quizbowl incremental clue trajectory，但它没有进入 2026-08-29 的 v4 30-topic re-audit，因此当前树不再保留一个带“PROMOTE”字样的孤立状态文件。若未来重开，必须从 `FINDING_RULES.md` 的完整 N0+N1+D0 feasibility 重新审计，而不是继承旧 promoted 标签。

### Lineage–Weight Dissociation — `LEGACY-OUT / MOTHER CROWDED`

行为本身有强 pilot，但宽母现象已被 source repetition、GroupQA、Memory Correlation Bias 等工作占领。潜在 novelty 只剩 recognition→weighting routing mechanism；旧 `candidates/` 与 `phenomena/` 两份重复长文从当前树移除。

### Event Actuality Gate / Mental Simulations Become History — `LEGACY-OUT`

早期 event factuality G0 受 sentence-vs-document annotation scope 影响，宽行为又有 CogNarr/event factuality work占位。若未来研究 kind/status→downstream reuse，应以当前 **Habitual→Episode Actualization** 或 **Mixed-Status Event Attraction** 的更严格 contract 为准，不复活旧名。

---

## 4. 最常见的死亡模式

以后新 candidate 在 N0/N1/D0 阶段优先检查这些：

1. **不存在**：自然数据上 strict phenotype 为零/极少。
2. **不是同一个现象**：不同模型各错各的，却被平均成一个 story。
3. **能力地板**：模型连 downstream operator 都不会，无法定义 recognition-use dissociation。
4. **构造 artifact**：接口、label、长度、显式数字、选项顺序或 synthetic world 制造 effect。
5. **数据不成立**：license、gold、independence、eligible count 不能在选题阶段锁死。
6. **mother collision**：剩余所谓 novelty 只是 subtype / domain swap / readout swap。
7. **强模型消失**：只有弱 checkpoint 存在，没有重要 scaling transition。
8. **post-hoc rescue**：看结果后换 subset、threshold、prompt、readout、模型或名字。
9. **mechanism masquerading as phenomenon**：mother behavior 已经成立，只剩 `representation exists → is it causal / where does it route?`，却仍占 phenomenon shortlist。

### 一句 stop-loss

> **如果一个题需要“再换个设置也许会有”才能继续，它已经不是当前 contract 的 survivor。**
