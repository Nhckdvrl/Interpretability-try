# 领域 03：主体、意图、承诺与行动

状态：`12 candidate cards — UNTESTED`
母问题：模型是否把“想做、预计会做、答应做、获准做、能够做、已经做完”压成一个模糊的 future/action 表示？

## 顶会边界

普通 agent 失败、目标切换和 action-effect verification 已经不是空白：[AgentChangeBench](https://arxiv.org/abs/2510.18170)、ACL 2026 *Don't Act Blindly*、[Tool Irrelevance](https://aclanthology.org/2026.acl-long.1473/) 分别覆盖 goal shift、动作后果检查和结构匹配偏差。ACL 2026 的 [representation-use gap](https://aclanthology.org/2026.acl-long.676/) 还使“模型知道但不用”成为宽母现象。

因此本领域只保留具有**特定行动状态机**的裂缝：承诺≠完成、完成≠继续、许可≠义务、预计≠意图、撤销后状态≠从未授权。最强行为应同时满足：相关概念报告正确、目标/权限/后果 control 正确、最终 action 仍沿一个可命名的错误路径。

## 优先数据架

| 数据 | 自然单元 | 适合轴 | 可得性 |
|---|---|---|---|
| [PRESTO](https://aclanthology.org/2023.emnlp-main.667/) | 含修正、不流畅和多语言的 task dialogue | self-correction、slot replacement | 公开 |
| [AgentChangeBench](https://github.com/Maniktherana/AgentChangeBench) | 中途目标切换轨迹 | replace/add/cancel | 公开（NeurIPS 2025 workshop） |
| [τ-bench](https://github.com/sierra-research/tau-bench) | 航空/零售状态化 agent | goal、permission、side effect | 公开 |
| [BFCL](https://gorilla.cs.berkeley.edu/leaderboard) | 多轮 function calling | tool/argument/state | 公开 |
| ToolSandbox / AppWorld | 可执行状态环境 | revoke/rollback/termination | 公开 |
| ALFWorld / WebShop / AgentBench | 长程行动规划 | goal reached、dead end | 公开 |
| NaturalPlan / PlanBench | 自然规划与约束 | feasibility、order、irreversibility | 公开 |
| CommitmentBank / ATOMIC / SocialIQA / OpenToM | 态度、意图与行动后果 | intend/expect/promise/action | 公开 |
| NormBank / NeuBAROCO | 许可、义务与禁止 | may/should/must | 公开 |

---

## AIC-01 — 承诺被当成完成

**一句话矛盾。** 模型能解释“她答应提交报告”只是承诺，更新任务状态时却把报告标成已提交。

**自然例子。** “供应商承诺周五退款”不能用于回答“退款已经到账了吗？”

**数据与轴。** CommitmentBank、FactBank/MAVEN-Fact、真实客服/项目对话；`promised / intended / tried / managed / completed` 原生动词，分别问 speech-act、event actuality、current state 与 next action。

**晋级 signature。** commitment/actuality 分类正确，只有任务账本或行动把未来事件写成 completed；错误稳定落到 promised event，不是任意 hallucination。若直接 factuality 也错，降为普通语义失败。

**规模与机制。** 强模型会更好地提取计划 payload，但 event writer 可能在读取清晰 action content 时忽略 status gate。A：提及 action 即创建 completed event；B：status tag存在，planner只读 action payload。与 event actuality母现象的区别必须是**任务状态与行动后果**。

## AIC-02 — 意图和预期接到错误的下游问题

**一句话矛盾。** 模型分别知道一个人“打算做什么”和“认为会发生什么”，却用预期回答行动、用意图回答结果。

**自然例子。** “Sam 打算徒步，但预计暴风雨会迫使他放弃。”尝试动作来自意图，最可能结果来自预期。

**数据与轴。** OpenToM、ATOMIC、SocialIQA、CommitmentBank；同一主体同时持有冲突的 intention/expectation，交换两 proposition，测 attitude labels、attempt、prediction。

**晋级 signature。** 两个态度标签均正确，但 action/outcome 出现交叉双重分离，且交换内容后错误跟着 attitude route 而非词序移动。

**规模与机制。** 两种 future state 都会随规模变清晰，但 query router可能只有一个“未来事件”通道。A：态度在共享表示中混合；B：表示正交、query gate 选错。普通 ToM/action gap 不足，必须有这组交叉错误。

## AIC-03 — 明知目标已完成，仍继续执行计划

**一句话矛盾。** 模型正确报告任务已经完成，却继续执行缓存的剩余步骤，甚至破坏完成状态。

**自然例子。** 商品已经买到，agent 仍继续点击“加入购物车”和“付款”。

**数据与轴。** ALFWorld、WebShop、AppWorld、AgentBench；利用环境原生 early success，比较 `goal reached early / almost reached / explicit success message`，保存 state report、STOP probability和下一 action。

**晋级 signature。** goal-state probe正确，工具结果读取正确，只有 termination/action错误；错误动作对应原计划的下一步。若模型只是没检测成功，KILL。

**规模与机制。** 更强 planning能形成更持久的 plan representation，而 stop gate是独立计算。A：goal comparator未接 termination；B：STOP信号存在但 autoregressive plan completion path占优。可 patch goal state或 plan carrier。

## AIC-04 — 新目标已经接受，旧目标仍驱动动作

**一句话矛盾。** 模型完整复述替代目标 B，下一步却继续已经取消的目标 A。

**自然例子。** 用户先要求取消航班，随后改为只改座位；agent 说“好的，只改座位”，却调用 cancel_booking。

**数据与轴。** AgentChangeBench、τ-bench、BFCL multi-turn、PRESTO；`replace / add / postpone / cancel`，目标内容与说法自然来自原轨迹。问 current goal，再执行一步。

**晋级 signature。** current-goal report、priority和所需tool知识均正确，错误 action精确对应旧计划；goal swap 后错误等变。只统计恢复慢已被 AgentChangeBench覆盖。

**规模与机制。** 指令理解改善旧新目标识别，但 plan cache未必重编译。A：semantic goal slot已更新、action plan未invalidate；B：两者都更新，tool decoder受旧调用序列 induction牵引。

## AIC-05 — 权限撤销后，行动仍像权限存在

**一句话矛盾。** 模型正确说访问权已撤销，却仍调用受限工具或建议执行受限动作。

**自然例子。** 管理员先授权退款，随后明确撤销；最终状态应等同“从未授权”。

**数据与轴。** ToolSandbox、τ-bench、BFCL multi-turn；`never grant / grant / grant→revoke / revoke→grant`，最终权限集合有可执行 oracle。分别测 permission report、tool choice、argument和postcondition。

**晋级 signature。** grant→revoke 与 never-grant 的报告都正确，行为却不同；错误只在历史授权路径出现，形成真正 hysteresis。

**规模与机制。** 长程记忆强化会同时保存旧grant与revoke，canonical permission state是独立需要。A：append-only permission memory；B：current permission正确，但旧plan/tool affordance path未被veto。

**碰撞边界。** 普通 role/system prompt refusal不算；必须是同一自然任务中的可证明权限状态和matched path independence。

## AIC-06 — 会指出死路，选择时仍走死路

**一句话矛盾。** 模型逐项评估时准确说某一步会进入不可逆死路，最终动作却仍选那一步。

**自然例子。** 旅行计划明知错过末班车后无法到达，仍把这条路线排第一。

**数据与轴。** NaturalPlan、PlanBench、ALFWorld、Blocksworld；同一候选动作先做 consequence/feasibility probe，再自由选择；交换表面顺序与即时收益。

**晋级 signature。** consequence与irreversibility判断高，choice错误系统性偏向即时进展或默认动作；把已识别风险增强时仍不发生veto。若评估本身不稳定，属于planning能力不足。

**规模与机制。** verifier与policy接受不同训练信号，更强模型可同时拥有强评价器和强行动先验。A：risk representation未送入policy；B：送入但immediate-progress reward压过future veto。

## AIC-07 — 许可在计划中膨胀成义务

**一句话矛盾。** 模型会解释“可以线上提交，也可以邮寄”，生成计划后却说“必须线上提交”。

**自然例子。** 可选路径被选中，不意味着它是唯一允许路径。

**数据与轴。** NormBank、NeuBAROCO、真实政策文本、IFEval/agent tasks；`may / should / must / must not` 与同一action payload。先问modal force，再让模型规划并解释未选选项是否合法。

**晋级 signature。** modal分类与合法动作集合正确，plan writer把所选动作重写为necessary并拒绝同样合法的替代；作用随是否被迫选一路而打开。

**规模与机制。** 规划需commit一个动作，事后解释可能把commitment误写成necessity。A：constraint compiler丢modal强度；B：compiler正确，choice rationalizer做necessity backfill。

**碰撞边界。** deontic keyword bias已有；本卡必须是 **semantic set correct / selected action causes force inflation**。

## AIC-08 — 能做不等于应该做

**一句话矛盾。** 模型知道某工具能完成操作，也知道它在当前情境不获授权，却仍因“参数正好可填”而调用。

**自然例子。** 系统有删除账户API，但用户只要求查看账户状态。

**数据与轴。** BFCL、ToolSandbox、τ-bench；分别测 tool capability、semantic relevance、authorization和actual call。使用真实API语义，做 `can×relevant×authorized` 三因子。

**晋级 signature。** capability/relevance/authorization三项报告均正确，只有call route在 capability+parameter match 下压过authorization veto；若只是不懂工具相关性，已被 Tool Irrelevance完整覆盖。

**规模与机制。** 工具训练强化结构可填与成功调用，安全/权限gate独立。A：authorization没有进入tool logits；B：进入但强structural alignment晚层覆盖。

**碰撞边界。** 高风险；只有 authorization-specific veto failure 与因果路径独立于 Tool Irrelevance才保留。

## AIC-09 — 委托关系被误作亲自执行

**一句话矛盾。** 模型知道经理让 Lee 签署合同，却把“签字的身体动作”和“造成签署的责任”都归给经理。

**自然例子。** “主编让记者删除一段文字”：记者执行，主编发令，二者agency不同。

**数据与轴。** PropBank/QA-SRL/MAVEN-ARG 的 causative frames、新闻事件论元、SocialIQA；direct action、caused action、ordered-but-unrealized。分别问physical actor、causer、responsible party和event actuality。

**晋级 signature。** causative relation与两实体都识别正确，但某一种downstream读出选择性串槽；最好physical actor与responsibility形成双重分离。

**规模与机制。** 事件压缩倾向把causer与agent挂在同一action node，法律/社会责任又需要独立readout。A：角色槽合并；B：槽分开、query role selector失效。

**碰撞边界。** SRL/causative语义成熟；必须是 recognition-use + 自然责任/行动分离，而非句法解析题。

## AIC-10 — 条件承诺在条件失败后仍被执行

**一句话矛盾。** 模型能说承诺只在条件 P 成立时生效，P 已明确不成立，仍按承诺已触发制定行动。

**自然例子。** “如果包裹周五没到，我会退款”；包裹周四已到，不应退款。

**数据与轴。** τ-bench零售政策、ContractNLI、NaturalPlan、条件义务/承诺语料；四格 `condition true/false × promise present/absent`，先问条件与义务状态，再执行。

**晋级 signature。** condition truth、rule meaning和payload均正确，只在 action中把conditional promise当unconditional；反方向条件成立时正常执行。

**规模与机制。** action payload比condition gate更显著；强instruction training可能强化承诺执行。A：条件scope未绑定action；B：绑定正确但planner只检索action token。

**碰撞边界。** 普通conditional reasoning已有；独特性来自 **conditional commitment activation gate** 与实际tool action。

## AIC-11 — 修正被理解成追加任务而非替换任务

**一句话矛盾。** 模型能解释“周二——抱歉，是周四”是修正，最终却安排两场会议。

**自然例子。** 自我修正的规范语义是旧slot被替换，不是增加一个新事件。

**数据与轴。** PRESTO原生self-repair utterances；比较 `X—sorry Y`、直接Y、X and Y、X then cancel X and add Y。测repair type、current slot、event count与执行calls。

**晋级 signature。** repair识别正确、current value Y正确，但event count/tool calls仍包含X；距离/中间turn可形成残留曲线。若只答错Y，属于dialogue state tracking。

**规模与机制。** 对话理解强化repair detection，但append-only生成/记忆会保留旧event。A：旧slot未overwrite；B：state正确，tool compiler读取所有mentioned events。

**碰撞边界。** PRESTO已测解析，BlockWorld-Repairs测恢复；空位是 replacement-vs-accumulation 的状态机制。

## AIC-12 — 用户中断被当成背景文字，旧动作继续

**一句话矛盾。** agent正确复述用户“停下，不要执行”，当前step仍完成下一次外部写操作。

**自然例子。** 用户在付款确认前说“取消”，agent却因已生成计划而提交付款。

**数据与轴。** τ-bench/AppWorld/BFCL multi-turn 与 agent interruption tasks；在read-only、reversible、irreversible action前插入自然stop，比较 acknowledgment和实际call。控制同长度非stop消息。

**晋级 signature。** stop intent、target task和动作后果均报告正确，错误只在 action已被plan primed或接近commit边界时出现cliff；不是简单漏读最后一句。

**规模与机制。** 流式agent的计划可能在用户消息前已进入action representation，强planning增加inertia。A：interrupt gate太晚；B：gate正确但pending action未invalidate。

**碰撞边界。** goal shift和安全中断已有系统研究；需明确 **acknowledgment intact + commit-boundary phase transition** 才有会议尺度。

## 本领域首轮排序

| 顺位 | 卡 | 主要价值 | 主要风险 |
|---:|---|---|---|
| 1 | AIC-03 knows-done/keeps-acting | 日常、错误落点为下一计划、机制与方法直连 | agent运行成本 |
| 2 | AIC-11 repair-as-addition | PRESTO原生、自我修正自然、对象计数明确 | correction工作已有 |
| 3 | AIC-05 revoked permission | 同终态路径独立、真实安全语义 | 与access-control评测相邻 |
| 4 | AIC-02 intention/expectation cross-wire | 基本主体问题、交叉双解离 | ToM拥挤 |
| 5 | AIC-10 conditional commitment gate | 真实政策/交易、deterministic action | 可能只是conditional reasoning |
| 6 | AIC-06 evaluates-dead-end/chooses-it | verifier-policy机制很干净 | representation-use母现象过宽 |

AIC-08、AIC-12 只有观察到专属 veto/commit-boundary signature 才能摆脱已有工具和goal-shift论文。

---

## Batch-2 脑暴死亡回填（2026-08-28）

完整账本：[`BATCH2_BRAINSTORM_LEDGER_2026-08-28.md`](BATCH2_BRAINSTORM_LEDGER_2026-08-28.md)。

| 本批主题 | 裁决 | 领域内理由 |
|---|---|---|
| **Deontic / free-choice inference（宽版本）** | `NOT-ADDED / MOTHER-OCCUPIED` | may/should/must、许可→义务与条件义务已经是本文件 AIC-07/AIC-10 的母区；只搬一个经典 deontic/free-choice puzzle 不构成新的 operator。 |
| **Generic delegation confusion** | `ROUTE AIC-09 / F2` | physical actor、causer、responsible party 的分离已在 AIC-09；换成 manager/agent/tool 委托不另建题。 |
| **Prospective intention / reminder（若只是“以后记得做”）** | `NOT-ADDED` | 若没有独立 temporal trigger/operator，容易退化成 goal memory/state tracking；不占第二批十强。 |

**禁止复活。** 新 proposal 若只是把 `permission/obligation` 或 `delegation` 换成法律、工具、机器人 setting，继续 ROUTE；必须给出本文件现有卡无法预测的错误形状才可重开。
