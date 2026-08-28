# 领域 09：Agent、工具语义与工作流状态

状态：`15 candidate cards — UNTESTED`
母问题：模型能否把“调用了工具、工具返回了什么、状态是否改变、这次调用属于哪一次任务、结果能否安全地驱动下一步”维持成不同变量？

## 顶会边界

普通 function selection、参数填写、缺工具/缺信息与长程成功率已有 [BFCL](https://gorilla.cs.berkeley.edu/leaderboard)、[ACEBench](https://aclanthology.org/2025.findings-emnlp.697/)、[FAIL-TaLMs](https://aclanthology.org/2025.naacl-long.149/) 和 [ToolSandbox](https://aclanthology.org/2025.findings-naacl.65/)；普通 stateful tool-use 失败也被 [Stateful Tool Use](https://aclanthology.org/2025.findings-acl.284/) 覆盖。这里不能写“agent 不会用工具”，而要发现一个可命名的**事务、来源或调用身份错误**，且最好满足“状态报告正确、下一动作错误”。

## 优先数据架

| 数据/环境 | 自然单元 | 适合轴 | 可得性 |
|---|---|---|---|
| [ToolSandbox](https://github.com/apple/ToolSandbox) | 手机工具、隐含状态依赖 | canonicalization、state dependency | 公开 |
| [AppWorld](https://aclanthology.org/2024.acl-long.850/) | 9 个日常 app、457 APIs | side effect、collateral damage | 公开 |
| [τ-bench](https://arxiv.org/abs/2406.12045) | 航空/零售对话与政策 | state transition、authorization | 公开 |
| [BFCL V4](https://gorilla.cs.berkeley.edu/leaderboard) | 多轮、memory、error recovery | call identity、argument state | 公开 |
| [ACEBench](https://aclanthology.org/2025.findings-emnlp.697/) | Normal/Special/Agent | incomplete、ambiguous、multi-agent | 公开 |
| [FAIL-TaLMs](https://aclanthology.org/2025.naacl-long.149/) | 工具不可用与信息不足 | failure handling | 公开 |
| API-Bank / ToolBench / ToolTalk | API dialogue/trajectories | selection、return parsing | 公开 |
| WebArena / AgentBench / ALFWorld | 交互式环境 | retry、termination、rollback | 公开 |

---

## ATW-01 — 工具明确失败，计划仍按成功推进

**元数据。** `priority=A; naturalness=N3; collision_risk=MEDIUM; stage=LITERATURE-CHECKED`

**一句话矛盾。** 模型能准确复述工具的失败原因，下一步却像操作已经成功一样继续。

**日常例子。** 转账 API 返回“余额不足，未执行”；agent 说“转账失败”，随后通知收款人钱已到账。

**数据与轴。** FAIL-TaLMs、ToolSandbox、τ-bench、AppWorld；利用原生 success/failure returns，分别测 result report、post-state、next action，控制同长度成功消息与 failure-before-side-effect/partial-side-effect。

**晋级 signature。** failure和current state报告正确，动作稳定对应成功分支；随 plan priming/步骤位置出现 cliff 更强。若模型没读懂 return，属于普通 parsing failure。

**规模与机制。** 更强模型会更好解释错误，也可能形成更强的预生成计划。A：result state未更新 plan；B：更新正确但 plan continuation在 action decoder覆盖。可 patch failure representation 到 planner step。

**碰撞边界。** FAIL-TaLMs已证工具坏时表现差；只有 **failure recognized / success branch executed** 的定向解离和机制才新。

**最便宜证伪。** 30 个短二步任务；若错误完全由 failure recognition解释，KILL。

## ATW-02 — 第二次失败借用了第一次的成功结果

**元数据。** `priority=A; naturalness=N3; collision_risk=LOW; stage=IDEA`

**一句话矛盾。** 同一工具第一次成功、第二次失败，模型却把旧成功当成本次结果。

**日常例子。** 第一次查 Alice 余额成功，第二次查 Bob 超时；模型把 Alice 的余额报给 Bob。

**数据与轴。** BFCL multi-turn、ToolSandbox、API-Bank；`success→failure`、`failure→success`、两个 success、不同工具 failure，实体和数值交换。记录 return attribution 与 answer destination。

**晋级 signature。** 第二次 failure识别正确，答案仍精确复制最近同 schema 的成功 payload；错误随工具/schema identity而非纯 recency移动。

**规模与机制。** 工具结果缓存与调用实例 binding是架构性接口，规模不保证解决。A：同名调用共享 result slot；B：调用分开，但 answer router在 empty/failure时回退最近成功。

**碰撞边界。** stateful benchmark通常统计最终错，不研究 stale-success substitution 的调用身份机制。

**最便宜证伪。** 20 对两个实体的查询；若 failure时只是拒答/猜测而不复制旧 payload，KILL。

## ATW-03 — 省略可选参数，被旧值自动补回

**元数据。** `priority=A; naturalness=N3; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 新一轮没有提供可选参数、API 规定使用默认值，模型仍沿用上一轮的旧值。

**日常例子。** 上次订酒店说“两间”，这次只说“订周五的同一家”，agent 又订了两间而非默认一间。

**数据与轴。** BFCL multi-turn、PRESTO、ToolSandbox；`explicit same / explicit new / omitted-default / omitted-inherit`，必须由 API schema 明确 omission语义。测 schema explanation、current slot 与 call。

**晋级 signature。** 模型准确说 omission means default，call中仍复活旧argument；仅在 schema/name相同时出现。若任务本身允许 conversational inheritance，样本无效。

**规模与机制。** 对话记忆提升使旧slot更易检索，反而可能加剧。A：slot state append-only；B：state正确，function-call decoder做格式级自补全。

**碰撞边界。** DST carryover已有；独特性是 **schema default known / call argument resurrected** 与可干预的 compiler路径。

**最便宜证伪。** 先人工审计 20 个 schema，确保默认规范无歧义；若效应依赖含糊对话，KILL。

## ATW-04 — 读的是一个对象，写到同名另一个对象

**元数据。** `priority=A; naturalness=N3; collision_risk=LOW; stage=IDEA`

**一句话矛盾。** agent 正确读取目标记录，写操作却落到名字相同但 ID 不同的记录。

**日常例子。** 两个联系人都叫 Alex；模型读对了订单 Alex-17，却更新 Alex-31 的地址。

**数据与轴。** AppWorld、τ-bench、ToolSandbox、BFCL enterprise functions；真实对象具 display name 与 stable ID。比较唯一名、同名异 ID、alias、重命名，测 read target、write argument、post-state。

**晋级 signature。** read/description都锁定正确 ID，write call稳定换到同名/近邻 ID；错误 destination能由 display-name salience预测。若 lookup最初已错，属于 entity resolution。

**规模与机制。** 自然语言 reader偏名字，structured writer需精确ID binding；两接口训练分离。A：ID token在跨阶段丢失；B：ID仍在，write decoder按名称重新检索。

**碰撞边界。** 普通 entity linking不够；本卡要求 read→write interface identity split。

**最便宜证伪。** 20 个 AppWorld 原生多对象任务；若模型始终复制明确ID，KILL。

## ATW-05 — 自己的猜测被检索回来后，升级成“独立证据”

**元数据。** `priority=A; naturalness=N3; collision_risk=LOW; stage=IDEA`

**一句话矛盾。** 模型先把自己的未经证实猜测写进记忆，稍后检索到它，便把它当成外部来源对原猜测进行佐证。

**日常例子。** agent 猜“会议可能周三”，把摘要存档；下一轮读到该摘要后说“记录也显示周三，因此很确定”。

**数据与轴。** BFCL V4 memory、LongMemEval、LOCOMO、AppWorld notes/mail；自然流程 `guess→write→retrieve→decide`，对照 external note、self-authored note带/不带 provenance、未写回。gold由原始记录决定。

**晋级 signature。** 模型能正确回答“这条笔记是我刚才写的、没有独立来源”，confidence或action仍像获得第二来源；原猜测错误时形成稳定自我放大。若只是在上下文重复导致，需 provenance controls 后仍在。

**规模与机制。** 更强 agent更常总结/写记忆，风险不会随参数自然消失。A：memory encoder丢 provenance；B：provenance可读，evidence aggregator只计 mention count。可做 source-lineage patch，机制可导出 provenance-aware memory。

**碰撞边界。** 与重复证据/来源谱系母现象相邻，但这里的独特性质是 **agent自身输出经过工具边界后获得虚假外部性**；不是 Hamdi 的实体现实性问题。

**最便宜证伪。** 20 个自然 memory任务，显式问 provenance 后再决策；若 self/external weighting相同且只是原答案复读，需进一步区分，否则 HOLD。

## ATW-06 — HTTP 成功状态压过了失败语义

**元数据。** `priority=A; naturalness=N3; collision_risk=LOW; stage=IDEA`

**一句话矛盾。** 返回码是 200、正文明确说业务失败，模型也读懂正文，却仍把操作记为成功。

**日常例子。** API 请求成功送达服务器，但票务正文说“无座，未出票”。

**数据与轴。** API-Bank、BFCL live、ToolSandbox；正交 `transport status × semantic outcome`，使用真实 API 包装语义，测两层状态解释、ledger与next action。

**晋级 signature。** transport和business status均报告正确，只有任务状态随 `200/success` token走；四格中产生 status-over-payload interaction。

**规模与机制。** 工具训练常把 `200` 强化为完成标志，业务语义需要另一路 gate。A：success token触发硬终止；B：payload failure形成但晚层被 schema-level status覆盖。

**碰撞边界。** 不等于普通 return parsing；它是 two-level success ontology 的冲突。

**最便宜证伪。** 真实 API 风格短响应 24 个；若强模型总按业务结果，KILL。

## ATW-07 — 部分成功被压成全部成功

**元数据。** `priority=A; naturalness=N3; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 批量工具说 5 项中 4 项成功、1 项失败，模型正确复述比例，却把整个任务标成完成。

**日常例子。** 给五位客户发邮件，一封退信；“批处理成功”不等于任务全部完成。

**数据与轴。** AppWorld、BFCL parallel calls、ACEBench；原生 batch/parallel results，扫失败项位置与重要性，测 item status、global completion和repair action。

**晋级 signature。** item-level状态全对，global status或follow-up忽略少数失败；可出现 majority threshold/cliff。若只是漏读长列表，长度/位置 controls 必须排除。

**规模与机制。** 多工具并发只会更普遍；聚合 operator与语义抽取分离。A：global reducer默认为 any-success；B：all-success规范存在但 majority success token覆盖。

**碰撞边界。** 普通 parallel function accuracy不覆盖部分结果到全局完成态的 reducer机制。

**最便宜证伪。** 1–5项短 batch，保持响应很短；若global completion严格遵守 all，KILL。

## ATW-08 — 重试被当成无害，重复副作用却真实发生

**元数据。** `priority=B; naturalness=N3; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 模型知道工具不是幂等的、第一次可能已执行但回包丢失，仍直接重试并造成重复操作。

**日常例子。** 支付请求超时不表示未扣款；盲目重试可能扣两次。

**数据与轴。** AppWorld/τ-bench/ToolSandbox 中写工具；`definite failure / ambiguous timeout / success` × `idempotent / non-idempotent`，先问可能状态，再选 retry/check/idempotency key。

**晋级 signature。** 模型正确列出“双重执行”风险与工具幂等性，action仍在 ambiguous+non-idempotent格直接 retry；明确失败和幂等 control正常。

**规模与机制。** retry是强通用策略，事务不确定性需要 veto；知识提升甚至更会解释风险但不保证 policy使用。A：outcome-set不进入planner；B：进入但 progress heuristic覆盖。

**碰撞边界。** error recovery benchmark拥挤；只有 **ambiguity×idempotency特异 interaction + risk-known/action-wrong** 才保留。

**最便宜证伪。** 24 个短自然API情境；若模型稳定先查状态，KILL。

## ATW-09 — 回滚后仍相信写入保留

**元数据。** `priority=A; naturalness=N3; collision_risk=LOW; stage=IDEA`

**一句话矛盾。** 工作流明确回滚了事务，模型也说“已回滚”，后续仍把中途写入当作当前状态。

**日常例子。** 银行事务先改余额、后因错误整体撤销；最终余额应等于开始前。

**数据与轴。** AppWorld state snapshots、数据库/API sandbox；`commit / rollback / partial compensation / no transaction`，最终 state相同的两条路径做 path-independence，问 state并继续行动。

**晋级 signature。** rollback含义和日志顺序正确，只有曾经写过的路径留下 ghost state；direct-original与write→rollback终态行为不同。

**规模与机制。** 长轨迹记忆保留事件历史，但 current state需canonicalization。A：event log被当state；B：state正确，downstream retriever优先最近write。可解释且能导出 transaction-aware compaction。

**碰撞边界。** ToolSandbox canonicalization相邻，但 rollback hysteresis及内部 current/history分离可能未覆盖；先 exact audit。

**最便宜证伪。** 20 个两字段事务，不必真执行外部工具，用环境原生日志离线评测；若无路径差，KILL。

## ATW-10 — dry run / preview 被当成真实执行

**元数据。** `priority=A; naturalness=N3; collision_risk=LOW; stage=IDEA`

**一句话矛盾。** 模型知道工具只是预览会发生什么，更新账本时却把预览结果当成已发生。

**日常例子。** “预览删除 34 个文件”不等于文件已删除。

**数据与轴。** AppWorld、CLI/API tasks、BFCL tool schemas；同 payload 的 `preview/dry-run/execute`，先问 tool mode，再问 state和next action。可选真实开源命令的 `--dry-run` 日志。

**晋级 signature。** mode classification正确，state writer只因 payload像结果而更新；execute正常，preview错误精确落到 simulated post-state。

**规模与机制。** 模型更懂 preview语义，但 rich simulated output会强激活结果写入路径。A：mode gate未绑定 payload；B：mode正确、state updater忽略非actual tag。

**碰撞边界。** 与 event actuality相邻，独特性是工具执行接口中的 simulation→state commit机制。

**最便宜证伪。** 20 个真实 dry-run outputs；若模型state判断稳定，KILL。

## ATW-11 — 取消 pending call 后，旧结果仍被接纳

**元数据。** `priority=B; naturalness=N3; collision_risk=LOW; stage=IDEA`

**一句话矛盾。** 用户取消了一个尚未完成的请求，迟到的返回到达后，模型仍把它写入当前任务。

**日常例子。** 已取消的旧地址查询晚到，不应覆盖随后成功的新地址查询。

**数据与轴。** 可在 ToolSandbox/BFCL async-style trajectory 上原则性扩展；`request A→cancel A→request B→return A/B`，call IDs与实体来自自然任务。

**晋级 signature。** 模型正确追踪 cancel和call ID，仍接受 canceled result；错误随arrival order呈 race，而非不会读ID。

**规模与机制。** 异步结果绑定是接口问题，不由语言能力自动解决。A：cancellation未invalidate result slot；B：slot无效但 recency/result salience路由覆盖。

**碰撞边界。** 需要构造异步轨迹，`naturalness=N3`但 source并非现成 benchmark；只有使用真实 async API规范且人工抽样通过才测。

**最便宜证伪。** 先查 BFCL/AppWorld 是否已有 call IDs和cancel；若只能靠不自然文本模拟，HOLD。

## ATW-12 — 查询空结果被当成世界中的否定事实

**元数据。** `priority=B; naturalness=N3; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 工具因过滤器过严返回空列表，模型知道查询覆盖不全，却断言现实中不存在该对象。

**日常例子。** 一个商店搜索不到药品，不代表这种药不存在；一次数据库查询为空也可能是条件错。

**数据与轴。** ToolSandbox、AppWorld、RAG/search tasks；`complete successful empty / incomplete empty / failed empty / nonempty`，先问 query coverage/status，再回答存在性和下一查询。

**晋级 signature。** coverage局限报告正确，世界结论仍 `empty→false`；complete-empty control应正常。错误若只是工具失败未识别，属于 FAIL-TaLMs。

**规模与机制。** 检索/数据库接口常用空结果作为负证据，source completeness是独立元数据。A：empty token触发否定；B：coverage可读但 answer writer忽略。

**碰撞边界。** RAG absence/knowledge boundaries相邻；这里需工具状态与 world-state ontology 的定向混淆。

**最便宜证伪。** 24 个真实 search/API风格响应；若模型总要求扩大检索，KILL。

## ATW-13 — 只读工具被误记为改变了世界

**元数据。** `priority=B; naturalness=N3; collision_risk=LOW; stage=IDEA`

**一句话矛盾。** 模型知道某 API 只是查询，却把返回的“建议状态”当成写操作后的新状态。

**日常例子。** 运费估算显示“预计周五送达”，并没有创建订单。

**数据与轴。** BFCL/AppWorld/API-Bank；成对 `quote/create`、`preview/commit`、`search/book` 工具，同 payload字段。测 affordance report、world state与follow-up。

**晋级 signature。** read/write属性解释正确，只有state更新受 result richness影响；错误落到工具描述的 hypothetical post-state。

**规模与机制。** 工具名知识改善不保证状态writer区分 observational与interventional results。A：result event默认actualize；B：tool affordance正确但未传到state updater。

**碰撞边界。** Tool Irrelevance/selection不覆盖 observation-action ontology。

**最便宜证伪。** 从真实 API schema抽20组 search/create；若无混淆，KILL。

## ATW-14 — 补偿动作成功，却仍按原失败状态行动

**元数据。** `priority=B; naturalness=N3; collision_risk=LOW; stage=IDEA`

**一句话矛盾。** 一个失败操作已被补偿动作恢复，模型能说系统恢复了，计划仍走故障分支。

**日常例子。** 库存预留失败后重新补货并预留成功，agent仍取消订单。

**数据与轴。** AppWorld/τ-bench；`fail→compensate→success` 与 direct success 终态matched，另有 fail-only。测 state report、next action与path independence。

**晋级 signature。** 终态报告相同，经历失败路径的 action仍不同；错误精确对应缓存的failure contingency。

**规模与机制。** 更强agent保留完整历史，也可能保留旧contingency。A：失败状态未清除；B：current state正确但 plan branch未rejoin。

**碰撞边界。** generic goal-change/path dependence相邻；独特性是 compensating transaction 和 failure-branch hysteresis。

**最便宜证伪。** 20 个三步工作流；若direct/compensated paths一致，KILL。

## ATW-15 — 同一最终状态因调用路径不同而被赋予不同可信度

**元数据。** `priority=C; naturalness=N2; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 两条工具路径得到字节相同的最终记录，模型只因其中一条经过“搜索→复制”就更相信它。

**数据与轴。** BFCL memory、AppWorld notes；`direct authoritative read / equivalent cached read / self-written then read`，final payload相同但 provenance不同。这里不是要求 invariant；规范权重由独立性与authority决定。

**晋级 signature。** 权重与真实provenance方向相反、尤其 self-written > external authoritative，才保留；合理来源偏好不算 anomaly。

**机制。** A：工具边界本身赋予 epistemic authority；B：retrieval familiarity/重复导致confidence提升。

**碰撞边界。** 与 ATW-05重叠，若没有更广的“tool-mediated authority”梯度则并入 ATW-05。

**最便宜证伪。** 只做 provenance判断与置信排序；无反常排序即 KILL。

## 本领域首轮排序

| 顺位 | 卡 | 主要价值 | 最大风险 |
|---:|---|---|---|
| 1 | ATW-05 self-corroboration after memory | 极自然、惊讶、来源与工具边界机制新 | 需与重复证据严格分离 |
| 2 | ATW-02 stale-success substitution | 错误终点精确、无需大规模agent跑 | 可能只在弱模型 |
| 3 | ATW-09 rollback ghost state | 路径独立、事务语义、机制和方法都强 | ToolSandbox canonicalization相邻 |
| 4 | ATW-06 transport-success/payload-failure | 两层成功本体清楚、真实API | 需真实样本而非模板 |
| 5 | ATW-08 unsafe retry despite known ambiguity | 高价值实际场景、interaction干净 | error-recovery文献拥挤 |
| 6 | ATW-04 read/write entity split | identity接口、可精确patch | entity resolution混淆 |
| 7 | ATW-10 dry-run actualization | 一句话自然、错误状态明确 | event factuality母现象 |

ATW-05、ATW-09、ATW-06 最像“行为先于名字”的候选；ATW-01 若没有 recognition/action 解离则已被 FAIL-TaLMs 完整包含。

---

## Batch-2 脑暴死亡回填与历史卡 override（2026-08-28）

完整账本：[`BATCH2_BRAINSTORM_LEDGER_2026-08-28.md`](BATCH2_BRAINSTORM_LEDGER_2026-08-28.md)。本节的 override 优先级高于上面的历史“首轮排序”。

### ATW-08 override — `KILL-EXACT / MECHANISM-FOLLOWUP-ONLY`

本轮发现 2026 ARR-under-review 的 **IdempotencyBench / “Do LLM Agents Act Exactly Once? Measuring Idempotency Violations Under Retries”** 已直接把 retry 下 duplicate side effects、idempotent/non-idempotent actions、retry modes、idempotency keys/receipts 做成系统 benchmark（320 deterministic tasks）。因此 ATW-08 的**行为发现线关闭**：

```text
ambiguous outcome
× idempotent/non-idempotent
→ retry
→ duplicate side effect
```

不能再以换 AppWorld/τ-bench、换支付/邮件 API 或加入“模型知道风险”作为新的 behavior paper。只有用户明确授权做该现象的 mechanism follow-up 时可复用历史卡，而且必须承认 behavior prior art。

### 其他 Batch-2 死亡/路由

| 本批主题 | 裁决 | 领域内理由 |
|---|---|---|
| **Generic idempotent retry / duplicate side effects** | `KILL-EXACT` | 同上，IdempotencyBench 正面占位。 |
| **Generic concurrency/race confusion** | `NOT-ADDED / F3-RISK` | 若只是 arrival order、race 或 eventual-state 错误，容易退化成 state tracking；路径残留又已有 ATW-09/11/14 与 F3。没有独立 operator 不新开。 |
| **Generic delegation** | `ROUTE AIC-09 / F2` | physical actor / causer / responsible party 已在 AIC-09；agent/tool setting 不构成新题。 |
| **Generic error-recovery retry** | `NOT-ADDED` | FAIL-TaLMs、stateful tool-use、IdempotencyBench 已使宽 error recovery 母区过密；必须有新的 call-identity/transaction operator 才重开。 |

**禁止复活。** 任何“超时→重试→重复扣款/重复发送”新名字先判为 ATW-08/IdempotencyBench 已占；不得因为增加 `knows-risk` probe 就重新宣称新行为。
