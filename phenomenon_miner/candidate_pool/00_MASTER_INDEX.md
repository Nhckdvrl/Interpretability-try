# 现象候选池总索引、去重地图与分发顺序

版本：2026-08-28
状态：`HISTORICAL IDEATION INVENTORY — NOT A DISPATCH QUEUE`
权威裁决：[`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md)。旧 Tier 和“当前首选”全部失去调度权；审计已杀掉的卡不得换名重跑。

## 2026-08-28 找题批次入口

### 第一批深度 N0

- [`DEEP_N0_SURVIVORS_10_2026-08-28.md`](DEEP_N0_SURVIVORS_10_2026-08-28.md)：第一批十题 shortlist。
- [`audits/ADVERSARIAL_N0_TEN_2026-08-28.md`](audits/ADVERSARIAL_N0_TEN_2026-08-28.md)：第一批逐题 adversarial N0。

### 第二批新十题（进行中）

- [`BATCH2_BRAINSTORM_LEDGER_2026-08-28.md`](BATCH2_BRAINSTORM_LEDGER_2026-08-28.md)：本批**完整找题目录 + 死亡库**；大量脑暴、current survivors、exact collision、mother-inclusion、ROUTE/KILL 都必须落在这里。
- [`audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md`](audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md)：当前 9 个第二批 survivor 的 N0 工作稿；第十槽仍 OPEN。
- 第二批在凑齐并重新攻击通过 10 个之前，**不得**创建或声称 `FINAL 10`；当前 9 个也不授权 smoke。
- 本批淘汰主题除了中央 ledger，还必须回填到相应 `01_...`–`12_...` 领域文档的 Batch-2 death-ledger 区。重新提出旧主题时先查两处，禁止换名复活。

## 先说明这 162 个数字意味着什么

这不是“我们发现了 162 个现象”，而是 162 个可以被证伪的候选卡。每张卡已经具有：

```text
自然生活原型
+ 公开数据或自然来源
+ 明确的 reader/report → use/action 裂缝
+ 值得晋级的结构 signature
+ 至少两个可区分机制
+ 最近母现象与碰撞边界
+ 最便宜的停止条件
```

候选数量的用途是增加发现异常的机会；真正的论文起点仍必须经过：

```text
N0 exact + mother-inclusion audit
→ independent adversarial review
→ D0 data/license/20-case audit
→ explicit READY-TO-SMOKE authorization
→ two-family smoke
→ N1 actual-signature audit
→ cross-family/size confirmation
→ mechanism
```

任何候选在前四步前都不得被叙述成真实、普遍或新颖的模型现象。

## 一、领域总览

| 领域 | 卡数 | 最自然的母问题 | 优先公开数据 | 当前首选 |
|---|---:|---|---|---|
| [01 本体/身份/指称](01_ONTOLOGY_IDENTITY_REFERENCE.md) | 12 | 相同、相似、同名、同类是不是同一个对象？ | FraCaS, AmbER, EntityQuestions, BookCoref | OIR-01 / OIR-03 / OIR-09 |
| [02 信念/世界/态度](02_BELIEF_WORLDS_ATTITUDES.md) | 12 | 被想象、引用、相信的内容何时进入现实世界？ | CommitmentBank, FactBank, FANToM, NOPE | BWA-01 / BWA-03 / BWA-02 |
| [03 主体/意图/承诺](03_AGENCY_INTENTION_COMMITMENT.md) | 12 | 想做、答应、获准、已完成如何控制行动？ | PRESTO, τ-bench, BFCL, AppWorld | AIC-03 / AIC-05 / AIC-11 |
| [04 记忆/时间/修订](04_MEMORY_TIME_REVISION.md) | 14 | 旧事实、当前事实与更新路径是否被规范化？ | LongMemEval, LoCoMo, TimeDial, TORQUE | MTR-06 / MTR-01 / MTR-05 |
| [05 话语/语用/沟通](05_DISCOURSE_PRAGMATICS_COMMUNICATION.md) | 14 | 听到一句话与接受、同意、承诺它有何不同？ | CIRCA, NOPE, REPAIR-QA, CMV/SAD | DPC-08 / DPC-11 / DPC-07 |
| [06 社会证据/集体](06_SOCIAL_EVIDENCE_COLLECTIVE.md) | 12 | 人人知道、共同知识、群体立场与独立证据是否分开？ | FANToM, RumourEval, QuoteBank, NormBank | SEC-01 / SEC-04 / SEC-06 |
| [07 知识/RAG/证据](07_KNOWLEDGE_RAG_EVIDENCE.md) | 14 | 检索、支持、充分、引用与回答是否是不同阶段？ | NoMIRACL, HotpotQA, PrimeFacts, ALCE | KRE-07 / KRE-01 / KRE-05 |
| [08 推理/验证/组合](08_REASONING_VERIFICATION_COMPOSITION.md) | 14 | 会构造理由与让理由否决结论是否同一能力？ | FOLIO, ProofWriter, LogicBench, REVEAL | RVC-01 / RVC-04 / RVC-02 |
| [09 Agent/工具/工作流](09_AGENTS_TOOLS_WORKFLOWS.md) | 15 | 调用结果、调用身份、当前状态与工具权威是否分开？ | ToolSandbox, AppWorld, τ-bench, BFCL | ATW-05 / ATW-02 / ATW-09 |
| [10 代码/结构化状态](10_CODE_STRUCTURED_STATE.md) | 15 | 注释、测试、名字与真实执行语义谁控制模型？ | SWE-bench, CRUXEval, DS-1000, RepoBench | CSS-02 / CSS-06–07–13 / CSS-01 |
| [11 不确定/高风险决策](11_UNCERTAINTY_DECISION_HIGH_STAKES.md) | 14 | 证据强度、禁忌、规则地位是否真正进入决策 gate？ | ContractNLI, LegalBench, CaseHOLD, PubMedQA | UDH-13 / UDH-09 / UDH-11 |
| [12 多语/跨文化](12_MULTILINGUAL_CROSS_CULTURAL.md) | 14 | 跨语言后同一命题、来源、实体和更新是否仍为同一个？ | MKQA, MIRACL, Multi3WOZ, MERLIN | MCC-01 / MCC-03 / MCC-10 |

## 二、162 张卡实际收敛成的九个机制母族

这张表用于防止把同一机制在不同数据集上包装成多篇“小现象”。跨领域复现应该成为一篇论文的外部验证，而不是重复选题。

| 机制母族 | 基本裂缝 | 代表卡 | 合并纪律 |
|---|---|---|---|
| F1 内容与状态分离 | proposition被正确提取，actual/asserted/quoted/simulated/withdrawn状态丢失 | BWA-01, DPC-14, KRE-07, ATW-10, MCC-07 | 若共享同一 commitment/status gate，合成一条主线 |
| F2 对象与身份绑定 | 属性、名字或调用内容正确，identity token/role绑定错 | OIR-03/05/08, RVC-04, ATW-04, CSS-06/07/13, MCC-05/06 | 只有不同错误目的地或不同内部算子才拆开 |
| F3 当前状态与历史路径 | current state正确，旧update/撤销/rollback路径仍驱动行为 | OIR-09, AIC-05, MTR-05, ATW-09/14, CSS-09, UDH-13, MCC-03/10 | 优先寻找跨setting共同机制，不做七个窄题 |
| F4 来源身份与证据独立性 | 来源谱系可识别，aggregator仍按mention/document/tool数加权 | SEC-04/05/06/11, KRE-12, ATW-05, MCC-01 | SEC-11/KRE-12已路由现有lineage；ATW-05/MCC-01必须证明独特边界 |
| F5 被认证的否决信号没有 veto | exception/counterexample/failure/contraindication被识别却不阻断结论或动作 | RVC-01/02, ATW-01/08, UDH-05/08/11, MCC-09 | 必须指明哪种veto、错误落到哪里；generic use gap不够 |
| F6 局部状态到全局归约算子错 | item都读对，global all/any/count/scope/commitment算错 | DPC-11, SEC-12, RVC-04/05/06, ATW-07, CSS-14 | 优先找稳定错误算子，而非平均组合掉点 |
| F7 两层authority冲突 | 表面成功/标题/测试/多数/日常词义压过语义正文或正式规则 | KRE-03, ATW-06, CSS-01/02/11, UDH-09/10 | 要求低层与高层均可报告，最终选择才错 |
| F8 信息可得与世界真假混淆 | 没看到、没检索到、未读、未知被写成false/known | SEC-02, KRE-01, ATW-12, RVC-09 | 必须排除任务本身要求closed-world或保守行动 |
| F9 分区状态未合并 | language/channel/world/scope各自正确，跨分区更新或join失败 | BWA-02/10, SEC-01/03, MCC-03/06/10 | 静态跨语/ToM accuracy不够，需matched final state或join signature |

## 三、首批 24 张分发卡

排序依据不是预测 effect size，而是四个预实验属性：

1. 普通人一句话能理解；
2. 大模型不一定因知识更多而自然消失；
3. 数据与 gold 能在不依赖主观 prompt 的情况下冻结；
4. 若成立，内部解释能裁决不同 computation，而非只做 probe。

### Tier A0：先做文献与数据审计

以下 12 张最值得先交给 12 个小 agent；这里的“先”仍然不是授权直接跑模型。

| 顺位 | 卡 | 一句话研究问题 | 为什么有机会跨规模 | 首个非模型任务 | 最大否决风险 |
|---:|---|---|---|---|---|
| 1 | **ATW-05** | agent把自己的猜测写入记忆，再读回来时会不会把它当独立外证？ | 强agent更常自动总结和写记忆 | 审计BFCL/LongMemEval是否保留author与provenance；找30条自然轨迹 | 只是文本重复/自我一致性 |
| 2 | **UDH-13** | 模型明知条款已修订，为何当前义务仍由旧条款决定？ | 法律文本理解与state update接受不同信号 | 在ContractNLI/SEC contracts找真实amendment链及current-clause gold | 普通知识更新或长上下文遗漏 |
| 3 | **DPC-08** | “我听到了/我明白”为什么会被总结成“我同意”？ | acknowledgment和agreement在训练语料长期共现 | 在AMI/ICSI/CMV中找人工dialogue-act+stance双标签 | stance gold不够确定 |
| 4 | **MCC-01** | 同一报道的原文和翻译会不会被算成两名证人？ | 多语能力增强不保证source aggregator去重 | 找canonical source/translation pairs；与同语副本严格区分 | 退化为一般重复证据 |
| 5 | **RVC-01** | 模型亲自认证一个反例后，是否仍接受被推翻的全称命题？ | 反例生成会随规模增强，veto路由未必同步 | 审计FOLIO/LogicBench自然规则与solve–verify exact coverage | 已被validation gap完整包含 |
| 6 | **CSS-02** | 模型知道测试没覆盖需求，却会不会因全绿就宣布正确？ | agent/RL训练把green tests强化成终止信号 | 用HumanEval+/MBPP+和SWE-bench筛known coverage gaps | 代码judge已有同一contrast |
| 7 | **KRE-07** | 模型知道文章在反驳谣言，抽取时会不会复活被引的谣言？ | 更强抽取能恢复claim payload，不保证保留stance sign | 检查PrimeFacts/PolitiFact是否有quote+verdict span级gold | negation/quotation现象已覆盖 |
| 8 | **MTR-06** | 旧消息里的“昨天”会不会被错绑到今天的提问时间？ | 时间算术增强不保证utterance-event anchor绑定 | 从TimeDial/LongMemEval筛原生timestamp+relative-time样本 | 已是temporal QA错误子类且无独特机制 |
| 9 | **SEC-01** | 私发给每个人与公开宣布，一阶知识相同但协调是否被模型混同？ | 个体ToM增强不自动产生common-knowledge operator | 审计FANToM/Reflect是否有public/private matched cases | 普通二阶ToM或已有common-ground工作 |
| 10 | **ATW-09** | 工具事务回滚后，模型行为是否仍残留中途写入？ | 保留更完整历史可能反而加强ghost state | 在AppWorld/ToolSandbox筛真实rollback/compensation轨迹 | benchmark canonicalization已同样覆盖 |
| 11 | **RVC-04** | 两个“有人”会不会被偷偷合成同一个人？ | 实体连续性先验可与量词知识共同增强 | 从FOLIO/真实排班数据库题筛anonymous-witness joins | 简单量词模板、强模型完全解决 |
| 12 | **BWA-01** | 会正确归因引语，却会不会把引语当作者承诺的事实？ | quote attribution与commitment writer可分离 | 在QuoteBank+fact-check文档找speaker/author/verdict三层gold | 引文事实性已有exact论文 |

### Tier A1：A0 审计并行后接续

| 顺位 | 卡 | 核心价值 | 与 A0 的关系 |
|---:|---|---|---|
| 13 | **MTR-01** | 已决定却仍把旧候选集当开放，wrong destination清楚 | F3 current/history；比普通old-value error多一个set closure |
| 14 | **SEC-06** | 源头撤回后，下游转载仍获证据权重 | F4 provenance graph invalidation；可连接ATW-05但不是重复 |
| 15 | **DPC-11** | 同意一个局部观点被扩成同意整套立场 | F6 scope reducer；CMV/SAD自然规模大 |
| 16 | **KRE-01** | “没搜到”被当成“不存在” | F8 search-state/world-state；gold要避开closed-world规范 |
| 17 | **ATW-06** | HTTP 200压过正文“业务失败” | F7 two-level success ontology；API场景极自然 |
| 18 | **CSS-06/07/13** | equality、alias、shallow-copy被压成单一身份位 | F2 identity graph；应作为一个候选族验证 |
| 19 | **UDH-09** | 明知哪段是dissent，却把它提升成controlling holding | F7 authority binding；真实判决文档天然 |
| 20 | **MCC-03** | 外语修正已理解，却没有commit到另一语言的state | F9 language-partition update；Multi3WOZ/PRESTO可用 |
| 21 | **AIC-03** | 明知任务完成却继续缓存计划的下一步 | F3 termination/plan；错误目的地为next planned action |
| 22 | **OIR-09** | 被删除对象继续参与关系 | F3 entity existence；可与代码deleted API交叉确认 |
| 23 | **SEC-04** | 问句/围观评论被正确识别后，聚合时仍算支持 | F4 proposition-without-stance；RumourEval有人工gold |
| 24 | **KRE-05** | 一要求引用，正确答案反而改成易照抄的错误答案 | answer/citation writer竞争；需先审计ALCE后续工作 |

## 四、明确合并、路由或暂不分发的卡

| 卡 | 处理 | 原因 |
|---|---|---|
| OIR-06 / KRE-13 | 路由到现有 EIRD | 已有行为档案，不再作为新候选重复跑 |
| SEC-11 / KRE-12 | 路由到 lineage–weight dissociation | 同源去重母现象已有本地路线 |
| DPC-02 | 合并 SEC-01 | public vs private / common knowledge是同一 decisive contrast |
| SEC-12 | 与 OIR-07 合并 | group decision→unanimity/member attribution同族 |
| BWA-04 | 路由现有 event actuality 线 | 只有新的reuse/action signature才可重开 |
| MTR-05 / ATW-09 / CSS-09 | 作为一个跨setting候选族 | rollback residue不应拆成三篇 |
| BWA-01 / DPC-14 / MCC-07 | 作为 commitment-carrier 候选族 | 区别只在同语/跨语/摘要接口；先找共同机制 |
| BWA-09 / DPC-12 | 合并 | canceled presupposition residue |
| RVC-02 / UDH-08 / MCC-09 | 先做 exception-veto 母族审计 | 若只是setting不同，不拆题 |
| CSS-06 / CSS-07 / CSS-13 | 合并 | equality / alias / shallow-copy共同诊断identity graph压缩 |
| KRE-14 | HOLD | 本地已有boundary-only负证据，除非新自然setting出现 |
| RVC-03/07/08/14 | 文献优先，暂不跑 | 与validation gap、converse fallacy、answer extraction过近 |
| DPC-05/06 | 文献优先，暂不跑 | 2026 sarcasm/rhetorical-question工作已高度占位 |
| UDH-04/07 | 文献优先，暂不跑 | ConfuseBench/MedEinst相邻，需先证明新的decision destination |
| MCC-08 | 文献优先，暂不跑 | ACL 2026 mRAG language-bias占位很近 |

## 五、每个小 agent 的固定任务合同

小 agent 一次只能领取一张卡或一个已合并候选族，输出写回原卡底部，不另建散乱备忘。

### Phase 0 — exact collision（不调用模型）

必须检索四轮：

```text
exact task + exact manipulation
plain-language anomaly + LLM
old philosophical/cognitive/software term + language model
candidate mechanism vocabulary + target task
```

逐篇填表：

| 比较项 | 最近工作 | 本卡 |
|---|---|---|
| mother question |  |  |
| decisive contrast |  |  |
| reader/report control |  |  |
| downstream error destination |  |  |
| cross-family/scale result |  |  |
| internal mechanism |  |  |
| causal intervention |  |  |
| method/prediction |  |  |

如果最近工作已覆盖同一 `contrast + signature + mechanism question`，标 `OCCUPIED`；不得以换数据集或换措辞继续。

### Phase 1 — data audit（仍不调用模型）

必须确认：

- 资源能实际下载，license允许研究使用；
- gold来自原标注、执行器、数据库状态或明确规范，不来自另一个LLM；
- 抽样读至少20例，并保留原始样本ID；
- relation在每例上真的规范成立；
- target和controls在长度、位置、答案形式、实体数上没有明显泄漏；
- 若要构造，先写构造原理，再人工逐例确认，不从一个玩具模板扩5000条。

### Phase 2 — frozen smoke card（到这里才允许调用模型）

固定后才写：

```yaml
candidate_id: ATW-05
primary_dataset: ...
sample_ids: ...
prompt_policy: neutral, task-native
reader_metrics: ...
use_metrics: ...
wrong_destinations: ...
controls: ...
kill_condition: ...
```

首轮只需 `30–50 examples × 2 families`。目的不是证明论文，而是便宜否定：

- 基础reader地板 → KILL/HOLD；
- 无特定错误终点 → KILL；
- 只有一个模型/尺寸 → HOLD；
- 一句提示即可完全改掉且任务本无客观接口 → prompt artifact；
- signature出现 → 才扩到3/5家族与尺寸序列。

### Phase 3 — generality and novelty

通过 smoke 后再要求：

- 至少 3/5 家族方向成立；
- 至少一个家族覆盖三个尺寸；
- 两个自然setting，或一个自然数据分布+一个原则性sandbox；
- effect不设硬阈值，但必须有结构：错误目的地、interaction、迟滞、cliff、双解离或反常scale；
- exact novelty审计更新到实验完成日期。

### Phase 4 — mechanism opening

只有行为通过后才进入：

```text
content absent?
content present but wrong carrier/source/entity?
state update failed?
state correct but wrong reader/router?
veto reached writer but lost competition?
```

线性probe只作为定位证据；至少要有 activation patching/causal tracing/targeted ablation/steering 中一条能区分卡片预写机制。方法必须由机制推出选择性预测，不做通用“加一句提示”的mitigation。

## 六、任何候选都必须回答的“母现象包含”质询

### 为什么不是 ACL 2026 representation–use gap？

合格答案必须指出：

```text
哪一个representation被正确读取？
哪一个自然接口之后失效？
错误稳定去了哪一个邻接状态？
哪两个机制对新control给出相反预测？
为什么普通“知道但不用”无法预测该selectivity/shape？
```

只说“我们的数据不同”“我们的应用重要”“我们做mechanism”均不合格。

### 为什么不是 prompt sensitivity？

任务规范必须由原benchmark、程序语义、事件日志、来源谱系或明确规则决定；prompt只应承载任务，而不是创造现象。最少包含一个简短中性版本和一个任务原生版本，signature需方向一致。

### 为什么不会被大模型直接解决？

候选无需预言一定随规模存活，但必须有训练信号分离理由，例如：

- reader受语义/知识训练增强，writer受模板/行动成功奖励增强；
- 更强模型保留更多历史，却不一定canonicalize current state；
- 更强多语映射不保证source/entity去重；
- 更强反例生成不保证counterexample获得veto权；
- 更强代码执行不保证green-test completion gate读取spec coverage。

没有这种理由的卡可以保留在大池，但不进入前24。

## 七、建议的最省钱分发顺序

```text
Wave 1（12个agent，纯文献/数据）：ATW-05 UDH-13 DPC-08 MCC-01
                                      RVC-01 CSS-02 KRE-07 MTR-06
                                      SEC-01 ATW-09 RVC-04 BWA-01

Wave 2（只接替Wave 1被OCCUPIED/KILL的槽）：
                                      MTR-01 SEC-06 DPC-11 KRE-01
                                      ATW-06 CSS-06/07/13 UDH-09 MCC-03
                                      AIC-03 OIR-09 SEC-04 KRE-05

Wave 3（只有Phase 0/1通过者）：30–50例×2家族 smoke

Wave 4（只有结构signature出现者）：3/5家族 + 三尺寸 + 外部分布
```

每个wave都先止损再扩展。四个常驻模型服务是验证资源，不是候选生成器；在用户明确切换到验证阶段前，本目录的工作不应调用它们。

### Wave-1 discovery (2026-08-28)

**First-Negative-Evidence Harm (FNEH).** On 40 GPQA Diamond items, one externally verified elimination of a wrong option caused baseline-correct→wrong flips in six of seven tested runs (Qwen3-4/8/14/32B, Gemma3-12B, Phi4-mini, Llama3.1-8B; Qwen3-8B is the exception); two/three eliminations generally recovered accuracy. Raw outputs and required controls are archived in [`phenomena/002_first_negative_evidence_harm.md`](../phenomena/002_first_negative_evidence_harm.md). Candidate only; pending fresh-split, surface-matched, and manual audits.
