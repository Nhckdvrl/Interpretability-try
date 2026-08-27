# MTR / DPC 候选池残酷审计

审计日期：2026-08-28
范围：[04_MEMORY_TIME_REVISION.md](../04_MEMORY_TIME_REVISION.md) 的 MTR-01–14 与 [05_DISCOURSE_PRAGMATICS_COMMUNICATION.md](../05_DISCOURSE_PRAGMATICS_COMMUNICATION.md) 的 DPC-01–14。
方法：针对 ACL/EMNLP/NAACL、ICLR/ICML/NeurIPS 与 2024–2026 arXiv 做 exact-neighbor 检索，并以“行为成立后能否独立支撑机制论文”而非“能否跑出 accuracy drop”判定。**本轮未运行模型、未改动或关闭任何服务。**

## 判定语义

- `PROMOTE`：不是声称现象已成立；意思是若在自然数据、3/5 家族、至少两个尺寸上出现指定的决定性解离，它有一条不只是母现象换皮的论文主张，并且至少有两个可区分的机制假说。
- `HOLD`：有可读的一句话，但当前 novelty、gold、自然性或规模生存性至少一项不足。只能作为 PROMOTE 项的 control/辅现象，或在新证据出现后复审。
- `KILL`：exact/near-exact 已占、只是仓库内重复路由、构念无法给出确定 oracle，或预期只会得到提示/接口/能力不足效应。不要花模型预算。

严格计数：**4 PROMOTE / 6 HOLD / 18 KILL**。PROMOTE 项仍然只是“值得交给验证代理的行为假说”，不是研究结论。

## 28 项总表

| ID | 结论 | 决定性理由 | 最近边界或阻断证据 |
|---|---|---|---|
| MTR-01 | HOLD | “最终值答对但旧候选集仍开放”有特异错误目的地；但 STALE 已同时测 state resolution、premise resistance 和 downstream policy adaptation，独立论文空间很窄。 | [STALE](https://arxiv.org/abs/2605.06527)、[Mem2ActBench](https://aclanthology.org/2026.acl-long.370/) |
| MTR-02 | KILL | 构念不闭合：只给摘要时，省略事实对读者并无可恢复 oracle；同时给原历史时，效应又退化成检索/注意。 | 摘要压缩系统问题，不是干净的模型本体 invariant |
| MTR-03 | KILL | “旧线索复活旧状态”已是 STALE 的 stale-premise resistance 与 Supersede 的 current-vs-stale gap 的直接实例。 | [STALE](https://arxiv.org/abs/2605.06527)、[Supersede](https://arxiv.org/abs/2606.27472) |
| MTR-04 | KILL / ROUTE | 与 AIC-11 是同一个 replacement→accumulation 命题；另立名称只会重复计数。 | 路由至 `AIC-11` |
| MTR-05 | KILL | 2026 年已有同终态/回滚路径残留的 exact 工作，并已经做到 same-token/different-cache、跨七家族、机制与修复。 | [Aborted but Not Forgotten](https://arxiv.org/abs/2608.15939)、[Rollback Is Not Undo](https://doi.org/10.1109/INFOCOM59046.2026.11571400) |
| MTR-06 | KILL | utterance-time 与 query-time 的时间锚定已经被 Memory-T1/Time-Dialog 明确建模到 session 与 utterance 两级 chronological fidelity。 | [Memory-T1](https://arxiv.org/abs/2512.20092)、[TReMu](https://aclanthology.org/2025.findings-acl.972/) |
| MTR-07 | **PROMOTE** | 若模型能正确列出两个事件的不同属性、正确判断非共指，却在计数/后果中把两个 event tokens 合并，这不是 event-coreference accuracy，而是“身份表示存在、下游用途丢失”的本体解离。 | 高风险近邻：[EventRelBench](https://aclanthology.org/2025.findings-emnlp.482/)、[UERLens](https://aclanthology.org/2026.acl-short.38/) |
| MTR-08 | KILL | current/past 真值与版本解析已被 PI/RI、TIDE、temporal conflict resolution 大面积覆盖；没有新的错误形状。 | [TIDE](https://arxiv.org/abs/2608.08512)、[When Facts Change](https://aclanthology.org/2026.findings-acl.103/) |
| MTR-09 | KILL | 两问顺序造成旧答案延续很难排除 token priming、recency 和 conversational carryover；即使成立也不足以自然支撑一个独立机制题。 | 与 PI/RI、multi-turn anchoring 重叠；缺少独立自然变量 |
| MTR-10 | KILL / ROUTE | 与 OIR-04 的 role-holder/property transfer 完全同构。 | 路由至 `OIR-04` |
| MTR-11 | KILL | direct path 与 correction path 的 path dependence 已被 iterated revision 与 rollback consistency 占据；“摘要痕迹不同”还混入长度与 provenance 的合理差异。 | [AGM-Bench](https://openreview.net/forum?id=2s1BujG84C)、[Aborted but Not Forgotten](https://arxiv.org/abs/2608.15939) |
| MTR-12 | KILL | deletion/contraction/forgetting 已成为显式 lifecycle operation，且已有 operation-level traces；不是未命名的新轴。 | [MemOps](https://arxiv.org/abs/2607.12893)、[AGM-Bench](https://openreview.net/forum?id=2s1BujG84C) |
| MTR-13 | **PROMOTE** | 只有在 `expiry extracted correctly → current applicability explicitly false → action nevertheless uses item` 三段同时成立时保留。expiry 是具有硬边界的 validity gate，不只是“知道新事实却不使用”。 | 最大威胁：[When Facts Change](https://aclanthology.org/2026.findings-acl.103/)、[STALE](https://arxiv.org/abs/2605.06527)、[TIDE](https://arxiv.org/abs/2608.08512) |
| MTR-14 | **PROMOTE** | `publication/revision time` 被写到 event node，产生 phantom recurrence；前提是三个时间槽均能正确抽取。该“文档时间→事件时间错误路由”不等同一般 temporal QA。 | [TimeSET](https://arxiv.org/abs/2403.00990)、[EventRelBench](https://aclanthology.org/2025.findings-emnlp.482/)、[UERLens](https://aclanthology.org/2026.acl-short.38/) |
| DPC-01 | HOLD | rejection-act intact / rejected proposition enters common ground 很清楚，但共同知识建立与使用已经有直接 benchmark；需先证明不是一般 negation/reference failure。 | [Grounding Gaps](https://aclanthology.org/2024.naacl-long.348/)、[Frame of Reference](https://aclanthology.org/2026.findings-acl.1645/) |
| DPC-02 | KILL / ROUTE | public announcement 与分别私信的一阶/高阶知识差异属于 ToM/common-knowledge 主域，在本文件不是独立候选。 | 路由 social/collective；[MindDial](https://aclanthology.org/2024.sigdial-1.63/) |
| DPC-03 | HOLD | indirect answer 理解正确但 RSVP/action 错仍可能有 bridge 价值；但现有工作已覆盖理解，若效应仅在 JSON/schema 出现就是接口伪影。 | [CIRCA](https://aclanthology.org/2020.emnlp-main.601/)、[PragmatiCQA](https://aclanthology.org/2023.findings-acl.385/)、[pragmatic representation shift](https://aclanthology.org/2026.lrec-1.390/) |
| DPC-04 | KILL | 间接请求从句法表面到语用意图的跨家族/跨尺寸内部重组已有 2026 representation paper；再加 action readout 太薄。 | [The Emergence of the Pragmatic Dimension](https://aclanthology.org/2026.lrec-1.390/) |
| DPC-05 | KILL | holistic irony 与 subsidiary inference 的解离、内部 representation 已被 ACL 2026 直接研究。 | [Decision Biases and Intent–Irony Decoupling](https://aclanthology.org/2026.findings-acl.962/) |
| DPC-06 | KILL | 修辞问句识别和内部 representation 都已占；QUD 输出只是一个窄 readout。 | [SRAQ](https://aclanthology.org/2025.emnlp-main.1553/)、[Rhetorical Questions in LLM Representations](https://aclanthology.org/2026.acl-long.5/) |
| DPC-07 | KILL | 2026-07 已有第一套专家标注的自然 implicature cancellation 数据，直接研究 recognition 与 belief update/cancellation。 | [Evaluating Communicative Belief Updates](https://arxiv.org/abs/2607.25094) |
| DPC-08 | HOLD / MERGE | acknowledgment→agreement 很自然，但裸 acknowledgment 的 gold 语用上可含部分接纳；作为 DPC-11 的 act-level contrast 很强，单独做论文不够稳。 | [Grounding Gaps](https://aclanthology.org/2024.naacl-long.348/)、[Dialogue Acts](https://aclanthology.org/2025.acl-long.1271/) |
| DPC-09 | HOLD | rebuttal 正确但 causal frame 残留有独特错误目的地；然而 false-premise 工作拥挤，下游后果常需人为补写，容易变成构造出来的 representation-use gap。 | [CREPE](https://aclanthology.org/2023.acl-long.583/)、[FalseQA](https://aclanthology.org/2023.acl-long.309/)、[PCBENCH](https://aclanthology.org/2025.findings-emnlp.44/) |
| DPC-10 | KILL | “虽然 P 但是 Q”通常同时承诺 P/Q，现实行动允许 trade-off；除非引入人为硬 veto，否则 gold 不唯一。 | discourse relation/nucleus classification 已成熟；核心阻断是 construct validity |
| DPC-11 | **PROMOTE** | `agreement target` 与全局立场均能正确抽取，最终总结却把局部 agreement 广播成 speaker-level stance flip；这是明确的 scope/commitment routing 解离。 | 近邻只覆盖 concession、stance 或 dialogue acts：[CMV Concessions](https://aclanthology.org/2018.dnd-9.4/)、[Dialogue Acts](https://aclanthology.org/2025.acl-long.1271/) |
| DPC-12 | KILL / ROUTE | 与 BWA-09 完全重复，且 presupposition cancellation 已是成熟母题。 | 路由至 `BWA-09` |
| DPC-13 | HOLD | conditional yes→unconditional state 很自然，但 CIRCA 已定义该标签；若只在 binary schema 中出现，就是设计者主动抹掉三值信息。 | [CIRCA](https://aclanthology.org/2020.emnlp-main.601/) |
| DPC-14 | KILL / ROUTE | 与 BWA-01 的 quote attribution/commitment 分离完全重复。 | 路由至 `BWA-01` |

## 真正进入验证队列的四项

### P1 — MTR-07：事件属性保留，但事件 token 身份在下游合并

**论文级一句话。** 模型知道两次同类事件在不同时间、涉及不同对象，也知道它们不是同一个事件；但一旦需要计数、追踪各自后果或生成时间线，两个事件变成一个。

**为什么尚未被 event coreference 母现象吞掉。** [EventRelBench](https://aclanthology.org/2025.findings-emnlp.482/) 已用 35K 问题覆盖 coreference/temporal/causal/super-sub 关系，[UERLens](https://aclanthology.org/2026.acl-short.38/) 已对事件关系特征做干预。因此仅仅“同类事件被判成共指”必须 KILL。唯一可保留的 headline 是：

```text
attributes/time correct
pairwise non-coreference judgment correct
yet downstream count or token-specific consequence collapses
```

**可区分机制。** H1：中层建立的是 type-centric event node，属性通过 mention 局部残留；H2：event nodes 本身分开，只有 count/timeline reader 以 event type 聚合。对 pairwise identity、token-specific consequence 与 count readout 做 matched activation patch，两个假说的因果层位预测不同。

**自然数据。** LoCoMo 的重复生活事件、MAVEN-ERE/WEC 的 gold 非共指同类型事件、EventRelBench 的 coreference 部分。优先直接筛出真实同 type / non-coreferent pairs，不生成玩具故事。

**必须通过的最小门。** 同一 item 内三项 component judgment 都正确；collapse 至少出现在 count 和一种非计数后果中；同一事件多 mention control 不得产生相同效应；3/5 家族且至少两档尺寸同方向。否则降级为 event-coreference error 并 KILL。

### P2 — MTR-13：过期状态已知，但 validity gate 没有约束行动

**论文级一句话。** 模型能准确说一条信息已经过期、现在不适用，却仍用它决定今天的行动。

**独特边界。** [When Facts Change](https://aclanthology.org/2026.findings-acl.103/) 已证明大模型可检测 temporal conflict/mutability 却不把判断传到最终预测；[STALE](https://arxiv.org/abs/2605.06527) 已测 implicit policy adaptation。因此不能把“知道旧、仍用旧”当 novelty。MTR-13 只有在以下额外结构稳定存在时才独立：

```text
hard validity boundary (valid_until/query_time)
explicit applicability=false
expired item remains selected as an affordance/action
active→boundary→expired 呈结构性形状
```

**可区分机制。** H1：planner 没有读取 validity bit；H2：validity bit 被读取，但高 utility/熟悉 action pathway 在晚层压过 veto。对 applicability token/expiry span 做 patch 与 utility-balanced controls 可分。

**自然数据。** 公开政策、活动/票券/访问许可、软件或 API 版本支持期；首轮只用明示日期、无医学法律知识门槛且动作 gold 唯一的材料。τ-bench 政策可作 application replication，但不能成为唯一数据源。

**必须通过的最小门。** active/expired 只改变有效时间；模型对日期、有效性、适用性均正确；free-text recommendation 与 structured action 都出现同一错误；revoked/superseded/unknown controls 显示 expiry-specific signature。若只是 [When Facts Change](https://aclanthology.org/2026.findings-acl.103/) 的一般 judge–prediction gap，降 HOLD。

### P3 — MTR-14：文档时间被误接成事件时间

**论文级一句话。** 模型能分别读出“新闻在 6 月 10 日更新”和“事故发生在 6 月 8 日”，却在时间线中凭空生成 6 月 10 日的第二次事故。

**为什么不是 temporal QA。** headline 不是日期抽取错，而是所有时间槽都正确后，`document/revision-time edge` 被路由到 `event node`。这给出可判定的 phantom-event destination，并与一般时间计算、日期位置、事件共指都有正交 controls。

**可区分机制。** H1：metadata 在中层被 eventify，形成额外 event mention；H2：document/event slots 分开，timeline writer 在晚层把 provenance edge 接错。比较 slot probes、event-count probes、metadata masking 与 late-layer interchange 可分。

**自然数据。** NewsEdits 2.0 的版本链、TimeSET 的真实新闻时间信息、TORQUE/MAVEN-ERE 的 event-time annotations。需要人工核验“更新没有报告第二次事件”；不能靠程序把任意 dateline 拼上文章。

**必须通过的最小门。** 单事件更新新闻上，publication/revision/event 三槽全对；phantom event 精确落在 revision time；仅移动 metadata 位置不改变方向；普通额外日期不产生同等错误；跨家族/尺寸。若只是长文事件计数错误，KILL。

### P4 — DPC-11：局部同意被广播成全局立场

**论文级一句话。** 模型能指出“我同意成本会上升”只同意一个局部前提，也能抽取说话者仍反对总体结论，却在总结、代理决策或人物状态中把他写成已经改变态度。

**为什么不是 stance detection。** [CMV concession work](https://aclanthology.org/2018.dnd-9.4/) 研究 concession 与说服，[Dialogue Acts](https://aclanthology.org/2025.acl-long.1271/) 研究 act classification；它们没有覆盖 `target binding correct + global stance correct + downstream commitment broadcast`。DPC-08 的 acknowledgment 可以作为 dialogue-act control，但二者应放在一项“commitment scope”研究中，不能拆成两篇。

**可区分机制。** H1：agreement scope 在表征中已经丢失；H2：scope/target 表征完整，summary/state writer 把 positive act 广播到 speaker-level stance。target/span patch、去掉词面 `agree` 的自然 paraphrase、局部 agree×全局 stance 四格能分。

**自然数据。** ChangeMyView/SAD 中带后续明确重申总体立场的真实回合；gold 必须由后文立场或原生标注确定，而非研究者猜测“听起来大概不同意”。

**必须通过的最小门。** agreement target、local proposition、global stance 三项都正确；错误在自由总结与至少一种 consequential readout 同时出现；不依赖单词 `agree`；bare acknowledgment、explicit global agreement、local disagreement 为 controls；跨家族/尺寸。否则降为普通 stance error。

## HOLD 项如何使用

- **MTR-01** 只作为 MTR-13 的“resolution without hard expiry”对照。若旧候选集合保留呈现独特 set-valued representation，而不是任意 stale behavior，才复审。
- **DPC-01** 可作为 DPC-11 的 negative update/control：rejection、acknowledgment、local agreement 是否共享一个有符号 commitment writer。
- **DPC-03** 只在自由文本、三值状态、真实行动三个接口都出现同一 literal-route failure 时复审；否则是 schema/interface 问题。
- **DPC-08** 合并到 DPC-11，不独立立题。优先使用带后续明确 disagreement 的 acknowledgment，消除语用歧义。
- **DPC-09** 只有真实语料自带可判定后果时再看；不要为了证明 residue 手写因果问题。
- **DPC-13** 只有 free text 也把 condition 删除、且不是任务要求 binary label 时复审。

## 立即停止投入的碰撞簇

1. **修订/旧值复活簇（MTR-03/08/11/12）**：STALE、Supersede、MemOps、AGM-Bench、TIDE 与 When Facts Change 已覆盖行为、结构化 operation、scale pattern 或 intervention/training 入口。
2. **回滚簇（MTR-05）**：同 token/different cache 的 exact 机制论文已经出现；任何普通文本 rollback 都更弱。
3. **时间指示词簇（MTR-06）**：utterance-level chronological fidelity 已明确成为 benchmark/training object。
4. **单项语用理解簇（DPC-04/05/06/07）**：indirect speech act、irony decoupling、rhetorical-question representation、implicature cancellation 均已有 2025–2026 direct work。
5. **仓库重复路由（MTR-04/10、DPC-02/12/14）**：合并到已有母卡，不人为扩大候选数。

## Novelty 声明纪律

这次检索支持的表述只能是“截至 2026-08-28 未找到完整覆盖该决定性解离的工作”，不能写 “first”。尤其 MTR-07、MTR-13 与 DPC-11 都邻近 2026 工作；行为 smoke test 通过后必须再做一次全文级 citation chaining，并把最强邻近方法直接复现为 control。任何 PROMOTE 项如果只得到整体 accuracy drop、component judgment 也同步失败、仅一两个小模型成立，立即 KILL，不进入机制阶段。

## Final-pass overwrite（第二轮对抗审计）

首轮 `4 PROMOTE` 已被更强的近邻检索推翻，**以 [SECOND_PASS_MTR_DPC.md](SECOND_PASS_MTR_DPC.md) 为最终判定**：

| 首轮候选 | 最终结论 | 覆写理由 |
|---|---|---|
| MTR-07 | **HOLD** | 自然 event identity gold 有粒度歧义；硬化样本后预期随规模消失；representation→wrong count 的机制又已被 [Repeated-Token Counting](https://arxiv.org/abs/2605.09239) 直接占领。 |
| MTR-13 | **KILL** | [ContractBench](https://arxiv.org/abs/2605.17281) 已 exact 覆盖 expiry 后使用、跨 38 模型、scaling cliff 与 intervention；[TicToc](https://aclanthology.org/2026.findings-acl.1848/) 覆盖 stale context→tool action。 |
| MTR-14 | **KILL** | DCT/event time 是经典母区分，TimeSET/ETRQA/EventRelBench/UERLens 已拥挤；自然 revision time 还不总是语义无关，干净 oracle 需要不自然重筛。 |
| DPC-11 | **FINALIST-CONDITIONAL / UNTESTED** | 仅保留 `target + local stance + global stance 均正确，downstream receiver 仍 scope-broadcast`；PSV、P3Sum、ambivalence 与 concession 是必须复现的强 controls。 |

第二轮另外从文献未打通的接口提出三个 `FINALIST-UNTESTED`：NG-01 habit→episode、NG-02 mixed-event factuality attraction、NG-03 partial-answer QUD closure。它们的 exact-collision、自然公开数据、强模型生存论证与两机制预测均记录在第二轮文档的 `NEW-GAP-GROWN` 章节。**本轮仍未运行任何模型或改动服务。**
