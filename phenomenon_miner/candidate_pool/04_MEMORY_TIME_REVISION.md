# 领域 04：记忆、时间与修订

状态：`14 candidate cards — UNTESTED / BRUTALLY AUDITED (3 PROMOTE / 1 HOLD / 10 KILL)`
本文件只建立候选池；**未运行任何模型，也未触碰常驻服务**。
逐卡证据与裁决见 [AUDIT_MTR_DPC.md](audits/AUDIT_MTR_DPC.md)。`PROMOTE` 仅表示行为若跨家族成立便值得进入机制阶段，不表示已经验证。
母问题：模型是否把“曾经是真的、现在是真的、尚未确定、已被修正、被撤销、只是没有再提”压进同一个可检索但不可可靠更新的记忆槽？

## 领域边界与红线

“长对话记不住”“新证据来了不更新”“问过去比问现在容易”都已不足以构成新现象。[LongMemEval](https://openreview.net/forum?id=pZiyCaVuti) 已直接覆盖长期对话中的 knowledge update、temporal reasoning 与 abstention；[Belief-R](https://aclanthology.org/2024.emnlp-main.586/) 覆盖追加证据后的推断修订；ICLR 2026 的 [AGM-Bench](https://openreview.net/forum?id=2s1BujG84C) 更系统测试 belief inertia、minimal change、preservation 与 iterated revision。原仓库的 PI/RI 线还占据“同一历史中初始值优于最新值”的宽非对称。

因此本领域只保留以下更窄但可能长成机制论文的结构：

```text
当前答案本身正确，但特定旧线索会把旧状态复活
能说修正后的值，却在计数/行动/总结中保留两个版本
同一最终状态因 direct path 与 rollback path 而产生不同输出
能做时间计算，却把相对时间绑定到错误的说话时刻
能区分事件描述，却把同类的两次事件并成一个 token
```

所有候选都必须回答：**为什么这不是 AGM-Bench 的自然语言例子、LongMemEval 的一个错误类型，或泛化的 representation-use gap？** 若没有决定性 contrast，就不进入验证。

## 优先公共数据架

| 数据/来源 | 原生对象 | 适合候选 | 可得性 |
|---|---|---|---|
| [LongMemEval](https://github.com/xiaowu0162/LongMemEval)（ICLR 2025） | 带时间戳的多会话、知识更新、时间推理 | MTR-01/03/06/08/09/12 | 官方数据与评测公开 |
| [LoCoMo](https://aclanthology.org/2024.acl-long.747/) | 约 600-turn 长对话、事件图、QA/总结 | MTR-01/02/03/07/10/11 | 官方数据公开 |
| [LoCoMo-Plus](https://aclanthology.org/2026.acl-long.1150/) | cue–trigger 语义断连的长期约束 | MTR-02/03/13 | 官方代码公开 |
| [Belief-R](https://aclanthology.org/2024.emnlp-main.586/) | 追加前提导致结论维持或撤回 | 碰撞审计；MTR-12/13 control | Anthology data/software |
| [PRESTO](https://aclanthology.org/2023.emnlp-main.667/) / [REPAIR-QA](https://aclanthology.org/2023.sigdial-1.52/) | 自我修正与第三位置修复 | MTR-04/11 | 公开 |
| [TimeDial](https://aclanthology.org/2021.acl-long.549/) | 日常对话中的时间常识 | MTR-06/07 | 官方 GitHub 公开 |
| [TORQUE](https://aclanthology.org/2020.emnlp-main.88/) | 新闻事件先后关系 | MTR-07/08/14 | Anthology data 公开 |
| [MAVEN-ERE](https://aclanthology.org/2022.emnlp-main.60/) / [WEC](https://aclanthology.org/2021.naacl-main.198/) | 事件共指、时间、因果与跨文档事件身份 | MTR-07/14 | 官方仓库/附件公开 |
| [ComplexTempQA](https://aclanthology.org/2025.emnlp-main.463/) | 带时间范围的 Wikidata 时序 QA | MTR-08/10/14 | 论文数据公开 |
| [NewsEdits 2.0](https://openreview.net/forum?id=mqrylyUmZ3) | 真实新闻版本更新及 edit intention | MTR-11/14 | 官方论文/代码页；下载前复核许可 |
| τ-bench / AppWorld / ToolSandbox | 有状态任务、撤销与事务轨迹 | MTR-05/13 | 官方公开；只在后续应用域需要时使用 |

---

## MTR-01 — 不确定性已经消失，回答仍保留旧的候选集合

`stage: IDEA | audit: HOLD | priority: A | naturalness: N3 | source: LongMemEval/LoCoMo | collision: HIGH`

**一句话矛盾。** 模型能正确回答“最终选了首尔”，制定后续计划时却仍说“首尔或京都都有可能”。

**日常例子与数据。** 长期对话中先说“我在首尔和京都之间犹豫”，后来明确“已经订了首尔”；从 LongMemEval knowledge-update 与 LoCoMo 决策事件中抽取 `open alternatives → resolution`，gold 来自后续明确承诺或事件图。

**发现轴与晋级 signature。** 分别问 `最终选择`、`仍有哪些可能`、`据此安排下一步`。只有在最终值和 resolution status 都答对，但下游总结/行动稳定保留旧 alternative set 时晋级；错误落点必须是**原候选集合**，不是随意 hedge。

**规模与机制。** 更强模型会更完整保留讨论历史，未必会把“候选集记忆”和“当前单值状态”做 destructive update。A：resolution 只新增单值，旧 set 未关闭；B：状态已关闭，但 cautious writer 重新展开旧选项。可用 late-layer patch 或询问风险水平区分。

**最近工作与空位。** LongMemEval 测更新答案，AGM-Bench 测一般 revision；空位只可能是 **resolution report intact / possibility set remains behaviorally open**。若直接 current answer 也错，归入既有 memory update failure。

**最便宜的证伪。** 先人工抽 20 个原生 resolution 轨迹、做 direct-final 与 history 两条件。若错误不指向旧 alternatives，或一句中性“以最终决定为准”完全消除，则 KILL。

## MTR-02 — 总结里没写，不等于用户撤回了

`stage: IDEA | audit: KILL | priority: A | naturalness: N3 | source: LoCoMo/LoCoMo-Plus | collision: FATAL-CONSTRUCT`

**一句话矛盾。** 模型知道摘要只能压缩信息，却把摘要中被省略的长期约束当成已经失效。

**日常例子与数据。** 用户多次提到坚果过敏；一次会话摘要只写旅行安排，之后推荐含坚果餐厅。用 LoCoMo persona/event graph 与 LoCoMo-Plus latent constraint，比较原对话、忠实但省略该事实的摘要、明确撤销约束三条件。

**发现轴与晋级 signature。** 先问“摘要是否声称用户不过敏/过敏已结束”，再做约束相关建议。只有模型正确回答“摘要没有这样说”，行为却使 `omitted summary ≈ explicit revocation`，而 `full history` 正常，才晋级。

**规模与机制。** 摘要式记忆是实际系统入口；规模增强语义压缩，却不保证读者区分 `not stored` 与 `stored negative`。A：summary writer 删除约束；B：reader 把缺省槽解释为 false。用人工金摘要与模型自产摘要分开裁决。

**最近工作与空位。** LoCoMo-Plus 已研究 cue–trigger disconnect，TiMem 等研究 consolidation；本卡必须证明的是**absence-as-revocation semantics**，而非检索没召回或摘要质量差。

**最便宜的证伪。** 只用人工写的、经两人核验忠实摘要做 20 例。若模型回答“信息不足/需查原记录”而非假定撤销，或现象只在模型自产坏摘要出现，KILL。

## MTR-03 — 一个旧线索会把已经更新的值重新唤醒

`stage: IDEA | audit: KILL | priority: A | naturalness: N3 | source: LongMemEval/LoCoMo | collision: OCCUPIED`

**一句话矛盾。** 模型直接问“现在住哪”答对新地址，但先谈一句旧社区，再问同一问题就回到旧地址。

**日常例子与数据。** 用户从波士顿搬到西雅图；中性查询 current residence 正确，提到“你以前在波士顿常去的咖啡店”后，同一 current query 被旧值捕获。用 LongMemEval knowledge-update 与 LoCoMo relocation，旧线索来自真实历史而非随机 distractor。

**发现轴与晋级 signature。** `neutral cue / new-state cue / old-state cue / unrelated autobiographical cue`，查询 byte-identical。必须先证明旧事实的时间标签和当前值都能正确报告；错误随旧 cue 的**语义归属**而非 token overlap 走，并稳定落到旧值。

**规模与机制。** 更强 episodic retrieval 可能强化 cue-dependent reconstruction，故不必随规模消失。A：旧 cue 改变检索，current state 不再进入；B：新旧都进入，query readout 被局部 episode gate 选择。检索层与晚层 patch 预测不同。

**最近工作与空位。** 与 LongMemEval update、contextual entrainment 和 AGM inertia 都近。只有 **baseline current correct + old episodic cue selectively resurrects superseded value** 才保留；generic distractor drop 不算。

**最便宜的证伪。** 20 个自然更新样本，每例只加一句原历史线索；若同长度新线索/无关线索同样掉，或错误不落旧值，KILL。

## MTR-04 — 修正后的值答对，事件却被算了两次

`stage: ROUTE | audit: KILL-DUPLICATE | priority: B | naturalness: N3 | source: PRESTO/REPAIR-QA | collision: OCCUPIED`

**一句话矛盾。** 模型知道“周二——抱歉，是周四”最终是周四，却在日历或事件计数中保留周二和周四两场。

**日常例子与数据。** PRESTO 的自然 self-repair 与 REPAIR-QA 的第三位置修复；测 repair label、current slot、event count、结构化日历输出。

**晋级 signature。** `current value=Thursday` 正确但 `count=2` 或两个 tool calls；direct Thursday 与 “Tuesday and Thursday” 是关键 controls。错误必须是 replacement→accumulation，不是日期识别失败。

**规模与机制。** append-only turn encoding 可随能力增强仍存在。A：旧 event node 未删除；B：dialogue state 正确，结构化 writer 汇总所有 mentioned values。

**最近工作与空位。** 这是 [AIC-11](03_AGENCY_INTENTION_COMMITMENT.md#aic-11--修正被理解成追加任务而非替换任务) 的跨域路由，不应另起重复题。PRESTO 已做 repair parsing；只有 state-correct/count-wrong 机制可保留。

**最便宜的证伪。** 直接复用 30 个 PRESTO repairs 做值问答与计数；若两者同错同对，无 dissociation，KILL。

## MTR-05 — 回滚后终态相同，模型仍按失败路径留下的状态行动

`stage: IDEA | audit: KILL | priority: A | naturalness: N3 | source: stateful agent traces | collision: EXACT-OCCUPIED`

**一句话矛盾。** 操作已经完整撤销、终态与从未操作完全相同，模型却仍表现得像那次操作留下了结果。

**日常例子与数据。** 订单先应用优惠券后回滚，最终账单与未应用相同；模型仍说优惠已使用或不可再用。可从 τ-bench/AppWorld/ToolSandbox 的事务轨迹抽取 oracle-equivalent final states，先离线读轨迹，不要求首轮执行 agent。

**发现轴与晋级 signature。** `direct A / A→B→A / A→C→A`，最终 serialized state 相同；先问 current fields，再问下一合法动作。高价值形状是 current state 报告正确但 action 受 history 影响，或 path 类型决定不同残留。

**规模与机制。** 计划和工具训练倾向保留 action trace；canonical state 与 action history 有独立通道。A：event trace 被误作 current state；B：state 正确但 affordance cache 未 rollback。

**最近工作与空位。** AGM-Bench 已测 iterated revision，agent goal-change 也拥挤；空位是**真实事务回滚、可证明同终态、下一动作错误**，不是形式命题 revision。

**最便宜的证伪。** 先抽 12 条真实可逆轨迹，直接把最终状态表放入上下文。若显式 state table 可完全压过 path，或只在轨迹极长时错，降为普通长上下文失败。

## MTR-06 — “昨天”被绑定到提问时间，而不是原话时间

`stage: IDEA | audit: KILL | priority: A | naturalness: N3 | source: LongMemEval/TimeDial | collision: OCCUPIED`

**一句话矛盾。** 模型会做日期加减，也看得懂每轮时间戳，却把旧对话里的“昨天”按今天重新解释。

**日常例子与数据。** 5 月 10 日用户说“我昨天提交了申请”；6 月 1 日问提交日期，应是 5 月 9 日而非 5 月 31 日。LongMemEval 有 timestamped histories；TimeDial/PATE 提供自然 temporal expressions。

**发现轴与晋级 signature。** 先测 timestamp extraction、日期算术、绝对日期版本，再测原生 relative expression；平移整个时间轴应等变。只有组件都对但 deictic anchor 选择 query time 才晋级。

**规模与机制。** 这是 address/binding 问题而非算术难度，规模未必修复。A：relative expression 在写入时未 resolve；B：已保存 event date，查询时重新解析 surface phrase。遮去原措辞或 patch date slot可区分。

**最近工作与空位。** TimeDial 测时间常识，LongMemEval 测 temporal reasoning，RemeMo 测相对时间依赖；本卡的独特性是 **utterance-time vs query-time anchor swap**，不是一般日期计算。

**最便宜的证伪。** 20 个明确时间戳且只需一步换算的样本。若绝对日期改写仍同样错，或模型连时间戳都读错，KILL。

## MTR-07 — 同一类事件发生两次，模型把两次经历并成一次

`stage: IDEA | audit: PROMOTE-UNTESTED | priority: A | naturalness: N3 | source: LoCoMo/MAVEN-ERE/WEC | collision: HIGH-BUT-DISTINCT`

**一句话矛盾。** 模型能列出两次“搬家”的不同日期和参与者，问次数或后果时却把它们当作同一个事件。

**日常例子与数据。** 某人 2019 年搬到巴黎、2023 年又搬到里昂；新闻也常有同一公司两轮收购/诉讼。LoCoMo event graph、MAVEN-ERE 与 WEC 提供 event identity、arguments、time。

**发现轴与晋级 signature。** 同事件多 mention、同 type 不同 token、不同 type 三组；测 mention extraction、event coreference、count 与 token-specific consequence。必须出现“arguments/time 可报告，event count 或后果仍 token-collapse”的解离。

**规模与机制。** 大模型更擅长语义聚类，反而可能把 lexical-semantic 相同看得过重。A：事件 node 在中层即合并；B：nodes 分开，count/summary reader 按 event type 聚合过度。

**最近工作与空位。** 事件共指数据与模型很多；若只是 coreference accuracy 低，完全撞车。只有 **token attributes intact / downstream token identity collapsed** 才有机制空位。

**最便宜的证伪。** 从 gold 非共指、同 type 对中抽 30 组。若问“发生几次”与 event-coreference 判断完全同步，无 representation-use split，KILL。

## MTR-08 — 当前更新覆盖了历史真值

`stage: IDEA | audit: KILL | priority: B | naturalness: N3 | source: LongMemEval/ComplexTempQA | collision: OCCUPIED`

**一句话矛盾。** 模型知道公司现在的 CEO 是 B，却连问“2021 年是谁”也回答 B，仿佛更新会重写历史。

**日常例子与数据。** 地址、职位、价格、政策都具有有效时间；LongMemEval updates 与 ComplexTempQA/Wikidata qualifiers 可提供 `valid_from/valid_to` gold。

**发现轴与晋级 signature。** `current / at-time / first / immediately-before-change` 四种 query；实体和时间位置换。必须是 current 正确、past 稳定落到 current value，且不等同 PI/RI 的 latest retrieval failure。

**规模与机制。** 更强模型可能更偏好最新事实，这是更新成功的副作用。A：memory 做 destructive overwrite；B：历史仍在，query temporal role 被 current-default gate 覆盖。

**最近工作与空位。** Temporal QA 已广泛覆盖，PI/RI 又直接占领 initial/latest asymmetry。本卡仅作为**反向错误目的地**候选；若没有“current overwrites past”且跨 query 类型一致的独特结构，KILL。

**最便宜的证伪。** 只抽 gold 时段明确的 20 个真实更新。若 past/current 都是普通混错，或加年份即可解决，KILL。

## MTR-09 — 问过“以前”之后，下一问“现在”被锁在旧时间层

`stage: IDEA | audit: KILL | priority: B | naturalness: N3 | source: LongMemEval/LoCoMo | collision: FATAL-CONFOUND`

**一句话矛盾。** 单独问当前状态时模型答对；先正确回答一次过去状态，再问同一句当前问题，它却沿用旧答案。

**日常例子与数据。** 先问“你搬家前住哪”，再问“现在住哪”；两问单独都容易，连续问时第二问被旧 temporal mode 捕获。

**发现轴与晋级 signature。** `current-only / past→current / unrelated→current / current→past`；第二问 byte-identical。错误必须在第一问正确后出现，并落到刚读出的历史值；增加显式年份、换实体、插入 topic boundary 是 controls。

**规模与机制。** 强模型建立临时 discourse focus，可能使 temporal query mode 有惯性。A：answer token induction；B：temporal reference frame persists and rebinds query。换旧答案表面词但保持时间 frame可区分。

**最近工作与空位。** 极接近 PI/RI、multi-turn anchoring 与 generic conversational carryover。只有**两种单问都对、顺序产生可逆 temporal-mode hysteresis**才保留；否则不值得验证。

**最便宜的证伪。** 对 20 个 LongMemEval updates 只改变提问顺序。若 effect 由答案 token 重复/简单 recency 解释，或仅小模型出现，KILL。

## MTR-10 — 职位换人后，继任者继承了前任的个人记忆

`stage: ROUTE | audit: KILL-DUPLICATE | priority: B | naturalness: N3 | source: temporal QA/news | collision: OCCUPIED`

**一句话矛盾。** 模型知道“新 CEO 是 Lee”，却把旧 CEO 的出生地、承诺或行为一并转给 Lee。

**日常例子与数据。** “CEO”是随时间换人的 role，不是一个持续存在的 person。ComplexTempQA、Wikidata qualifiers、新闻事件论元可提供 succession 与 person-specific attributes。

**晋级 signature。** succession/current holder/两人的个人属性都能单独答对；只有以 role 为中介的下游问题发生 predecessor→successor property transfer。

**规模与机制。** role token 是稳定检索键，person binding 才需要更新；规模增强 role knowledge 不保证 versioned binding。A：role node 与属性错误常驻；B：person nodes 正确但 query 经 role address 取旧 cache。

**最近工作与空位。** 这是 [OIR-04](01_ONTOLOGY_IDENTITY_REFERENCE.md#oir-04--角色的继任者继承了前任的个人属性) 的时间实现，必须合并路由，不另立论文。

**最便宜的证伪。** 20 个公开 succession 例，问 direct-person 与 via-role 两种。若 direct 也错，属于知识缺失；若 via-role 无额外错，KILL。

## MTR-11 — 同一最终事实，经历过修正的版本在总结中留下不同痕迹

`stage: IDEA | audit: KILL | priority: B | naturalness: N3 | source: PRESTO/NewsEdits/LoCoMo | collision: OCCUPIED`

**一句话矛盾。** 两段对话最终都只确定“会议在周四”，但一段曾说周二再改成周四，模型给出的最终摘要或置信度不同。

**日常例子与数据。** `direct Thursday` 与 `Tuesday→correction→Thursday` 应有相同当前任务状态；PRESTO、新闻版本历史和 LoCoMo updates 提供自然 revision paths。

**发现轴与晋级 signature。** 比较 direct、correction、cancel-and-recreate、uncertainty-then-resolve 四条自然路径；最终 canonical state 相同。晋级需要结构性 path signature（旧值进入摘要、置信度下降、额外行动）而非任意措辞敏感。

**规模与机制。** 大模型更会编码 provenance，而问题是下游是否区分“历史记录”与“当前状态”。A：state 未 canonicalize；B：state 正确，provenance feature 错误进入 writer。

**最近工作与空位。** AGM-Bench 的 iterated revision、PRESTO repairs 与 path-independence 母现象高度接近。本卡必须依靠**自然修订轨迹 + current-state report intact + specific residual destination**；只看到 direct/path accuracy 差异就 OCCUPIED。

**最便宜的证伪。** 先做 12 组人工核验的自然 paraphrase pairs。若所有差异被长度、否定词或重复 mention controls解释，KILL。

## MTR-12 — “不再拥有”比“改成另一个”更难写入当前状态

`stage: IDEA | audit: KILL | priority: B | naturalness: N3 | source: LongMemEval/LoCoMo | collision: OCCUPIED`

**一句话矛盾。** 模型能把“我现在养猫”更新为新宠物，却在“我不再养宠物”后继续保留旧宠物。

**日常例子与数据。** 用户偏好、订阅、过敏、工作和所有权都有 `positive replacement`、`cessation/deletion`、`temporary suspension`。从 LongMemEval/LoCoMo 的自然更新抽取，再人工核验状态边界。

**发现轴与晋级 signature。** 匹配 `A→B / A→none / A→not-A-but-unknown / no update`，保持提及次数和时间距离。只有 deletion 特异地失败、且模型理解“不再”的语义时晋级。

**规模与机制。** 文本记忆天然善于存实体—属性 pair，absence/none 需要 gate 或 tombstone。A：没有负状态节点；B：negative node形成但 retrieval 仍偏向有 lexical payload 的旧值。

**最近工作与空位。** AGM-Bench 已测 contraction/preservation；ICML 2024 [Asymmetric Belief Updaters](https://openreview.net/forum?id=BNAvYSCrLD) 研究奖励反馈的正负更新。只有**自然实体状态的 delete-vs-replace、语义识别完好、旧值作为错误落点**才不被覆盖。

**最便宜的证伪。** 各 20 个 replacement/deletion 原生例；若控制 lexical payload 后差异消失，或删除句本身常被误解，KILL。

## MTR-13 — 已过期的信息被正确识别，却仍控制当前建议

`stage: IDEA | audit: PROMOTE-UNTESTED | priority: A | naturalness: N3 | source: policy/news/dialogue | collision: HIGH-BUT-DISTINCT`

**一句话矛盾。** 模型会说优惠券昨天已经过期，仍建议今天结账时使用它。

**日常例子与数据。** 促销、签证、药物处方、政策条款和访问许可都有自然有效期。可从 τ-bench 政策、带发布日期/有效期的政府 FAQ、LongMemEval timed preferences 中抽取；只用有明确 `valid_until` 与 query time 的样本。

**发现轴与晋级 signature。** 分别测 expiry extraction、日期比较、当前 applicability、action recommendation；`active / expires today / just expired / long expired` 是自然轴。只有前三项报告正确而 action 仍用 expired item 才晋级。

**规模与机制。** 时间理解和行动选择接受不同训练目标；较强模型甚至会更流畅地复述过期条款。A：validity gate 未接 planner；B：接入但 utility/tool affordance path 压过 gate。

**最近工作与空位。** 与 temporal QA、policy following、representation-use gap相邻；独特性是**期限状态正确、适用性判断正确、行动选择仍使用过期项**的三段解离。

**最便宜的证伪。** 20 条真实、无专业知识门槛的明示期限文本。若 applicability 判断也错，或只在日期算术复杂时错，KILL。

## MTR-14 — 把“报道更新的时间”当成“事件发生的时间”

`stage: IDEA | audit: PROMOTE-UNTESTED | priority: A | naturalness: N3 | source: NewsEdits/TORQUE/news | collision: MEDIUM-HIGH`

**一句话矛盾。** 模型能分别指出文章发布时间和事件日期，生成时间线时却把一次编辑当成事件又发生了一次。

**日常例子与数据。** 新闻 6 月 10 日更新一篇报道，补充说明事故发生于 6 月 8 日；“updated June 10”不是第二次事故。NewsEdits 2.0、TORQUE、MAVEN-ERE/WEC 可提供版本、event mentions 与 temporal relations。

**发现轴与晋级 signature。** `publication time / revision time / event time` 三槽；先做槽位抽取，再做 event count/timeline。晋级需要抽取都正确但 timeline 出现 revision-time phantom event，且错误随 update metadata 而非文档长度出现。

**规模与机制。** 新闻预训练强化 dateline 与事件显著性，两种时间常共现。A：revision metadata 被编码为 event mention；B：时间槽分开，timeline writer 将 document-time edge 误接 event node。

**最近工作与空位。** temporal QA 与 event coreference 已成熟，ACL 2026 的 temporal framing 也研究新闻中的时间语言；空位只在 **document-time/event-time routing dissociation**，不是一般日期抽取。

**最便宜的证伪。** 先抽 20 个单事件、一次版本更新的真实新闻对；若 event count 始终正确或只有复杂多事件文章出错，KILL。

## 审计后验证队列与停止清单

| 顺位 | 卡 | 裁决 | 只有什么结果才晋级 | 最大风险 |
|---:|---|---|---|---|
| 1 | MTR-07 event-token identity collapse | PROMOTE-UNTESTED | attributes、time、non-coreference 都对，计数与 token-specific consequence 仍合并 | EventRelBench/UERLens 已占事件关系与机制；不能只是 coref 错 |
| 2 | MTR-14 document-time→event-time routing | PROMOTE-UNTESTED | 三时间槽都对，revision time 精确地产生 phantom event | 新闻人工核验成本；不能是普通日期/计数错误 |
| 3 | MTR-13 expiry gate bypass | PROMOTE-UNTESTED | expiry 与 applicability 均对，free-text/structured action 都仍使用过期项 | STALE/When Facts Change 母现象很近 |
| 4 | MTR-01 resolved alternatives remain open | HOLD / control | 必须得到稳定的 set-valued closure 失败，而不是任意 stale answer | STALE 已测 state resolution 与 policy adaptation |

**停止投入：** MTR-02/03/04/05/06/08/09/10/11/12。MTR-05 已被 exact rollback-consistency 论文占据；MTR-06 已被 utterance-level temporal fidelity 工作占据；MTR-04/10 为仓库内重复路由。详见总审计。
