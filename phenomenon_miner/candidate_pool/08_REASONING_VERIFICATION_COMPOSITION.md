# 领域 08：推理、验证、反例与组合

状态：`14 candidate cards — UNTESTED`
母问题：模型是否把“能构造理由、能识别局部关系、能验证规则、让否决证据控制最终结论”误当成同一个计算？

## 顶会边界

宽泛的 solve–verify gap 已被 [The Validation Gap](https://aclanthology.org/2025.emnlp-main.1495/)、[LLMs cannot spot math errors](https://aclanthology.org/2025.emnlp-main.553/) 与 [Confidence v.s. Critique](https://aclanthology.org/2025.acl-long.203/) 占位；前提顺序、可信内容污染逻辑、一般三段论错误也已有大量工作。因此这里不保留“会做不会检查”“换顺序掉点”“逻辑题做错”本身，只保留一个**局部判断已正确、但特定控制信号未进入特定结论 gate**的候选。

## 优先数据架

| 数据 | 自然/规范单元 | 适合轴 | 可得性 |
|---|---|---|---|
| [FOLIO](https://aclanthology.org/2022.emnlp-main.438/) | 人写一阶逻辑推理 | entailment、contradiction、unknown | 公开 |
| [ProofWriter](https://arxiv.org/abs/2012.13048) / RuleTaker | 可验证规则与证明 | proof、counterproof、depth | 公开 |
| [LogicBench](https://aclanthology.org/2024.acl-long.739/) | 25 类命题/一阶/非单调规则 | rule type、format | 公开 |
| [FoVer](https://aclanthology.org/2025.tacl-1.61/) / REVEAL | 自然语言推理链验证 | first-error、proof validity | 公开 |
| [PRM800K](https://github.com/openai/prm800k) / VtG | 数学逐步验证 | local error、global verdict | 公开 |
| ReClor / LogiQA / AR-LSAT | 自然考试论证 | sufficiency、necessity、exception | 公开 |
| ContractNLI / CaseHOLD | 合同条件与法律 holding | exception、scope、authority | 公开 |
| GSM8K / MATH / NumGLUE | 自然数学问题 | calculation、threshold、units | 公开 |

---

## RVC-01 — 自己给出的反例没有否决全称结论

**元数据。** `priority=A; naturalness=N3; collision_risk=MEDIUM; stage=LITERATURE-CHECKED`

**一句话矛盾。** 模型能亲自给出一个满足前提却违反结论的例子，下一问仍说“这个结论总是成立”。

**日常例子。** 它举出一个不参加培训也通过考试的人，却仍接受“只有参加培训的人才能通过”。

**数据与发现轴。** 从 FOLIO、LogicBench、ReClor、ContractNLI 中抽取带可读规则的 universal/conditional claims；先让模型产生或选择一个 countermodel，再保持同一上下文问 validity。对照 genuine supporting example、无效伪反例和由外部给出的同一反例。

**晋级 signature。** 反例的三个必要条件均判断正确，反例由模型生成和由用户提供时却至少一条路径不触发 veto；错误稳定落在原有 universal claim。若反例本身不成立或只是最终标签解析错，KILL。

**规模与机制。** 扩大规模会强化 example generation 与规则语言能力，不必自动建立 `witness → universal-veto` 路由。A：反例表示未与目标命题绑定；B：绑定存在，但 affirmation/prior conclusion 在晚层覆盖 veto。可做反例 token activation patch 与结论 logit 因果追踪。

**碰撞边界。** 不是再做 solve–verify gap；只有“有效 countermodel 已被内部/显式认证，却未否决对应量化命题”的定向现象才保留。

**最便宜证伪。** 30 个单句自然规则、先 forced-choice 检查 witness 条件；若强模型一旦承认反例便近乎 100% veto，立即 KILL。

## RVC-02 — 明确例外被承认，规则仍应用到该例外

**元数据。** `priority=A; naturalness=N3; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 模型知道 Lee 是规则列明的例外，给 Lee 做决定时仍套用一般规则。

**日常例子。** 政策说会员要付费，“学生会员除外”；模型正确说 Ana 是学生会员，却仍收费。

**数据与发现轴。** ContractNLI、RuleTaker/AbductionAndNegation、NormBank、真实政策 QA；比较 default rule、exception member、ordinary member，先问 exception membership，再问规则结论或选择动作。

**晋级 signature。** membership 与 exception scope 都正确，只有 rule application 把异常个体拉回默认类；姓名/内容交换后错误跟随 exception route。若模型不理解 exception，降为普通推理错误。

**规模与机制。** 默认规则在预训练中更强，显式例外是 late veto。A：exception feature未绑定个体；B：绑定正确但 default-rule circuit先行并控制答案。可与 RVC-01 比较“反例否决命题”与“例外阻断实例化”是否同路。

**碰撞边界。** 泛型过度推广、非单调推理已有；独特空位是 **exception report intact / same individual action wrong**。

**最便宜证伪。** 抽 40 条自然政策；若错误与基础 exception-membership accuracy 完全重合，KILL。

## RVC-03 — 找到第一处错误，仍接受整条证明

**元数据。** `priority=B; naturalness=N3; collision_risk=HIGH; stage=IDEA`

**一句话矛盾。** 模型准确指出证明第 4 步错了，却仍把该证明判为有效并采用其答案。

**日常例子。** 审核员标出账单里一笔加法错，但仍批准由该错误得到的总额。

**数据与发现轴。** PRM800K、VtG、REVEAL、FoVer；同一 trace 分别测 first-error location、valid/invalid verdict、是否采用 final answer。控制错误被后续独立修复与未修复。

**晋级 signature。** error localization正确，global verdict/answer稳定接受受污染后缀；若仅因最终答案碰巧正确，单独分层。规模增大令 localization上升但 veto不升尤其值钱。

**机制。** A：局部 critic 与 global verifier分离；B：verdict正确但 answer selector偏向最后答案。通过 patch error-state到 verdict/answer两个位置裁决。

**碰撞边界。** 与 EMNLP 2025 math-error论文高度相邻；只有论文未覆盖的 **localization→global-veto或answer adoption解离及机制** 才保留，否则 OCCUPIED。

**最便宜证伪。** 先精读最近论文实验变量；若已经联合报告同一三阶段 signature，文献阶段直接 KILL。

## RVC-04 — 两个“有人”被偷偷合成同一个人

**元数据。** `priority=A; naturalness=N3; collision_risk=LOW; stage=IDEA`

**一句话矛盾。** 模型知道“有人会法语”和“有人会日语”可以是两个人，推结论时却当成存在一个人两种都会。

**日常例子。** “团队里有人懂税务，也有人懂日语”不保证能找到同一个人处理日本税务。

**数据与发现轴。** FOLIO、LogicBench、真实团队/排班/数据库查询问题；`same explicit witness / two anonymous witnesses / explicitly different witnesses`，问可满足性、存在结论与人员分配。

**晋级 signature。** 模型能解释量词 scope 和不能合并 witness，行动/结论仍系统性选择 fused witness；反向拆分一个明确同一人的属性也可测试。若只在符号模板出现，KILL。

**规模与机制。** 强模型会更好抽取属性，但 discourse 中默认实体连续性可能更强。A：匿名 discourse referents在表示阶段合并；B：referents分开、composition readout用同一 salient slot。非常适合 entity-binding activation interchange。

**碰撞边界。** 不是泛化三段论；核心是 existential witness identity 与下游组合，需查 discourse representation / quantifier scope 邻近工作。

**最便宜证伪。** 20 个自然排班故事 + 显式同人/异人 controls；若仅含“someone”表面歧义导致，换为“not necessarily the same person”的自然澄清再测，仍消失则 KILL。

## RVC-05 — 局部约束全对，组合出的对象仍违反其中一个约束

**元数据。** `priority=B; naturalness=N3; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 模型逐条判断候选都正确，最后选择的候选却不满足它刚确认的一条硬约束。

**日常例子。** 它正确说航班 A 太晚、B 超预算、C 全满足，最后仍推荐 A。

**数据与发现轴。** NaturalPlan、TravelPlanner、AR-LSAT、constraint satisfaction QA；先对候选×约束矩阵做 deterministic judgement，再选择，交换候选顺序和软偏好。

**晋级 signature。** 矩阵近乎正确而选择稳定违反某一种约束，且错误有明确 dominance（最近提及、软偏好、即时收益）。若矩阵本身错，属于普通规划能力。

**规模与机制。** 逐项 verifier 与 argmax policy接受不同信号；更强偏好建模可能反而放大软偏好路径。A：约束聚合丢一维；B：硬约束表征存在但 utility writer覆盖。

**碰撞边界。** generic representation-use gap很近；必须有可复现的约束类别选择性或非线性，而非任意“不听自己分析”。

**最便宜证伪。** 30 个三候选自然问题，冻结矩阵；若最终错项无结构或只在长列表出现，HOLD/KILL。

## RVC-06 — “至少”在答案阶段收缩成“恰好”

**元数据。** `priority=B; naturalness=N3; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 模型正确解释“至少三人”允许四人，判断具体方案时却拒绝所有超过三人的方案。

**日常例子。** 餐厅要求至少三人起订，四人当然也符合。

**数据与发现轴。** NumGLUE、DROP、AR-LSAT、合同/政策文本；同一阈值下测 below/equal/above，先释义量词再做 eligibility/action。对照 at most/exactly/more than。

**晋级 signature。** 量词释义与数字比较均正确，仅 action/eligibility 在 `above threshold` 出现窄 collapse；若所有比较词都混乱则普通数理失败。

**规模与机制。** 指令数据里“满足最小数”常由边界例子示范，可能形成 equality prototype。A：quantifier decoder收缩；B：语义正确、资格 gate按边界模板匹配。

**碰撞边界。** 数量词推理已有；需保留 report/action双任务和 equality-attractor机制。

**最便宜证伪。** 真实政策句 20 条，逐一测阈值三点；强模型若曲线单调，KILL。

## RVC-07 — 计算结果正确，阈值决策取反

**元数据。** `priority=C; naturalness=N3; collision_risk=HIGH; stage=IDEA`

**一句话矛盾。** 模型算出 4.8% 高于 4.5%，却说没有超过阈值。

**数据与发现轴。** GSM8K、FinQA、TAT-QA、政策/风险阈值问题；分开 extraction、calculation、comparison、action，控制单位和等号边界。

**晋级 signature。** 前三层正确、只有固定决策方向错误，且单位/措辞 controls 后仍在。普通 arithmetic error 直接 KILL。

**机制与碰撞。** 很可能只是已知 Validation Gap 或 answer extraction，`collision_risk=HIGH`。只有出现稳定的 threshold-side、单位或风险方向特异 gate 才值得保留。

**最便宜证伪。** 文献 exact audit + 20 条无单位标量比较；若无选择性立即 KILL。

## RVC-08 — 能说明必要条件，却把它当充分条件使用

**元数据。** `priority=B; naturalness=N3; collision_risk=HIGH; stage=IDEA`

**一句话矛盾。** 模型会解释“有票是入场的必要条件，不保证能入场”，仍因某人有票断言其必能入场。

**数据与发现轴。** ReClor、LogiQA、AR-LSAT、ContractNLI；语义释义、counterexample、individual inference 三阶段，交换必要/充分条件和内容可信性。

**晋级 signature。** rule paraphrase 与反例均正确，same-item实例化仍做 converse inference；错误随 inference direction 而非词序。

**机制。** A：conditional方向在生成反例后丢失；B：方向编码正确但结论检索走共现路径。

**碰撞边界。** converse fallacy极拥挤；只有三阶段完整解离、反常 scaling或明确方向电路才晋级。

**最便宜证伪。** 先做严格论文审计；若已有同一“paraphrase correct/inference wrong”机制研究，OCCUPIED。

## RVC-09 — “不知道”在做决定时变成“不是”

**元数据。** `priority=B; naturalness=N3; collision_risk=HIGH; stage=IDEA`

**一句话矛盾。** 模型正确说记录里没有答案、因此未知，筛选候选时却把未知者当作不满足条件而永久排除。

**日常例子。** 病历没写过敏史不等于没有过敏；数据库没记录资质也不等于不具备。

**数据与发现轴。** ProofWriter open-world split、FOLIO、数据库/medical QA；true/false/unknown report 后做筛选、排序或询问下一步。对照明确否定与可补信息。

**晋级 signature。** 三值分类正确而 action 中 `unknown≈false`，在风险方向可出现 asymmetric destination；若任务规范本来要求保守排除，必须单列，不得混入。

**机制。** A：决策 writer只有二值接口；B：三值存在，但默认行动策略把未知映射为某一类。可测试不同损失不改变语义表示却翻转行为。

**碰撞边界。** OWA/CWA 与 abstention研究很多；独特性只可能来自 **known unknown + task-dependent action mapping**，并需明确规范。

**最便宜证伪。** 先选择 gold 明确要求“请求信息”的自然任务；若模型报告和动作同步，KILL。

## RVC-10 — 互相矛盾的前提被识别，结论仍像两者可同时使用

**元数据。** `priority=B; naturalness=N3; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 模型指出两条报告不能同时为真，后续解释却把两条都当事实拼成结论。

**日常例子。** 一份记录说车在东京，另一份同刻说在大阪；模型承认冲突后仍规划一条依赖“车同时在两地”的方案。

**数据与发现轴。** FOLIO contradiction、MultiNLI contradiction、fact-checking/多文档 QA；先定位冲突，再测 conclusion availability 与行动。对照可兼容信息和显式 source alternatives。

**晋级 signature。** conflict pair准确定位，但组合答案含来自两条互斥世界的属性，形成 hybrid world；若只是任选一源，不属于本卡。

**规模与机制。** 多文档整合能力越强，越可能把内容合并而不保留 mutual-exclusion gate。A：冲突标签不绑定 facts；B：source-world分别存在，summary writer做union。

**碰撞边界。** generic conflicting-context RAG拥挤；必须是 **conflict recognized / impossible conjunction constructed** 的世界融合。

**最便宜证伪。** 20 个双源自然案例，要求输出同时依赖两冲突事实；若错误只是随机选源，KILL。

## RVC-11 — 每一步都可能成立，不代表整条链是一条证明

**元数据。** `priority=B; naturalness=N2; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 模型逐句都说“这句话本身合理”，却没有发现相邻步骤根本接不上。

**数据与发现轴。** REVEAL、FoVer、EntailmentBank、e-SNLI explanations；从真实 proof 中替换一个中间结论为同主题真句，测 standalone truth、edge entailment、global validity。

**晋级 signature。** standalone truth高、明确 edge judgement也能判不蕴含，global verifier仍因主题连贯接受；错误随 semantic relatedness 增强而出现。

**机制。** A：global verifier聚合句真值而非边；B：边错误可见但 discourse coherence path覆盖。图边激活/attention transport可裁决。

**碰撞边界。** 属于 reasoning-chain verification，但“真句串 ≠ 证明”的 edge-vs-node 分解较具体；若近期论文已做同一替换则 KILL。

**最便宜证伪。** 30 条三步短链；若模型 edge 与 global verdict同步，KILL。

## RVC-12 — 多一条正确证明反而削弱正确答案

**元数据。** `priority=C; naturalness=N2; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 同一结论已有充分理由，再加入一条独立、同样正确的理由后模型反而改错。

**数据与发现轴。** EntailmentBank、FOLIO proof sets、HotpotQA supporting facts；`one sufficient proof / two independent proofs / duplicate proof / second irrelevant chain`，gold严格不变。

**晋级 signature。** 只接受独立正确 proof 时出现非单调下降或特定 cliff，且非长度、位置、实体引入解释；wrong destination应来自第二条 proof 的中间节点。平滑小跌 KILL。

**规模与机制。** 更强模型形成多条推理路径时可能有 winner arbitration，而非能力不足。A：proof paths互相抑制；B：answer router绑定最近 proof 的局部实体。

**碰撞边界。** redundancy/RAG distraction广泛；必须证明第二条是完整正确且效应由 proof composition 而非 context length/position造成。

**最便宜证伪。** 先对短样本做一/二 proof；若效应被位置 counterbalance 消除，KILL。

## RVC-13 — “可行”被误读成“必然成功”

**元数据。** `priority=B; naturalness=N3; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 模型知道一条计划只是存在可行执行，不保证所有执行成功，预测时却把可能性写成确定结果。

**日常例子。** “有一条路线能赶上飞机”不等于“随便走都会赶上”。

**数据与发现轴。** NaturalPlan、MATH existential constructions、科学实验计划；分开 `there exists a successful path / selected path is successful / all paths succeed`，要求模型先列 witness，再预测未指定执行。

**晋级 signature。** quantifier report正确，outcome writer把 existence路由为 certainty；与 AIC intention/actuality区分开。

**机制。** A：plan generator产生成功 witness后覆盖分布；B：modal表示存在，结果回答默认读 exemplar。可能连接“Experiments or Outcomes?”但 decisive contrast不同。

**最便宜证伪。** 真实旅行/实验方案 30 条；若限定问题措辞后消失，判 prompt artifact并 KILL。

## RVC-14 — 证明结论正确，却回答证明中最显眼的中间量

**元数据。** `priority=C; naturalness=N2; collision_risk=HIGH; stage=IDEA`

**一句话矛盾。** 模型完整推到目标结论，最终短答却复制了最后一个中间结果。

**数据与发现轴。** GSM8K/MATH、EntailmentBank、multi-hop QA；保留正确 rationale，交换中间量位置/类型，比较 rationale conclusion 与 final answer。

**晋级 signature。** reasoning terminal conclusion正确、final answer稳定落到特定邻接槽；规模或 answer-format出现 mode switch。随机格式错误 KILL。

**机制与碰撞。** 典型 answer-extraction/faithfulness问题，风险高。只有稳定“最后中间变量”路由及可因果分离才保留。

**最便宜证伪。** 先在公开生成日志做离线分析，无需新推理；若错误落点不集中，KILL。

## 本领域首轮排序

| 顺位 | 卡 | 主要价值 | 最大风险 |
|---:|---|---|---|
| 1 | RVC-01 counterexample without veto | 一句话惊讶、规范明确、机制接口干净 | solve–verify母现象 |
| 2 | RVC-04 existential witness fusion | 日常且是身份/组合问题，可能跨尺度 | 需避免简单模板 |
| 3 | RVC-02 exception known/rule applied | 政策应用自然、错误去向明确 | 非单调推理已有 |
| 4 | RVC-10 conflict-known/hybrid-world | 多文档真实应用、结构错误终点 | conflicting RAG拥挤 |
| 5 | RVC-05 constraints-correct/choice-invalid | 计划与决策方法口明显 | generic use gap |
| 6 | RVC-11 true nodes/broken edges | 可验证图结构、mechanistic route清楚 | proof verification相邻 |

RVC-03、RVC-07、RVC-08、RVC-14 先做文献审计，未证明独特 signature 前不应调用模型。

---

## Batch-2 脑暴死亡回填（2026-08-28）

完整账本：[`BATCH2_BRAINSTORM_LEDGER_2026-08-28.md`](BATCH2_BRAINSTORM_LEDGER_2026-08-28.md)。

| 本批主题 | 裁决 | 领域内理由 |
|---|---|---|
| **Explaining-away / collider（宽版本）** | `NOT-ADDED / MOTHER-OCCUPIED` | causal reasoning、selection/collider bias benchmark 已覆盖宽母题；仅做“LLM 不懂 collider”没有新 behavior operator。 |
| **Actual-causality preemption** | `NOT-ADDED` | actual causality / causal reasoning 邻域拥挤，且当前脑暴没有 components-intact 后独立 downstream 错误形状。 |
| **Ecological fallacy（宽版本）** | `NOT-ADDED / F6-RISK` | aggregation/statistical reasoning 本身拥挤；若只是 aggregate→individual conclusion，会被 F6 或普通 statistical reasoning 完整吸收。 |
| **Regression-to-the-mean neglect** | `NOT-ADDED` | 当前版本只能证明统计概念/计算不足，尚未形成“regression relation 已正确表示、某个独立 operator 仍错”的结构。 |
| **Optional stopping / p-hacking（宽版本）** | `NOT-ADDED` | 只问停止规则或显著性是统计规则应用，未形成不可被一般 verification/threshold 母题吸收的 computation。 |
| **Einstellung / mental set（宽版本）** | `KILL/OCCUPIED` | ACL 2026 MedEinst 已直接把典型先验/反事实证据下的 Einstellung 做成医疗 LLM 主现象；泛“旧策略固着”也落入 anchoring/plan inertia。 |

**禁止复活。** causal/statistical 老现象只有在模型已通过概念、局部关系与关键计算验收后，还出现一个具有明确 wrong destination、结构曲线和独立 operator 的 downstream failure，才可重新进入 N0；换 benchmark 或加 probe 不够。
