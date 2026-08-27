# 小 agent 单卡交接模板

用途：把总池中的一张候选卡交给便宜 agent，避免它重开整个选题空间、擅自大规模跑模型，或把未验证假设写成发现。

## 纯文献与数据审计模板（默认使用）

复制下列文字并只替换 `{CARD_ID}`：

```text
你只负责 phenomenon_miner/candidate_pool 中的 {CARD_ID}，不要研究其他候选。

先完整阅读：
1. candidate_pool/AUDIT_REGISTRY.md
2. candidate_pool/CARD_SCHEMA.md
3. ../NOVELTY_GATE.md
4. candidate_pool/LITERATURE_PATTERNS.md
4. {CARD_ID} 所在领域文档中的完整卡片

当前阶段仅做 Phase 0 exact-collision audit 和 Phase 1 data audit：
- 不运行任何模型；
- 不访问、不重启、不关闭常驻模型服务；
- 不生成大规模合成数据；
- 不修改其他候选卡。

文献必须优先 ACL/EMNLP/NAACL 主会与正式 primary source；
ICLR/ICML/NeurIPS只作为额外灵感或机制邻近；PaperNotes只作索引，结论回到原论文。

检索四轮：
1. exact task + exact manipulation；
2. plain-language anomaly + LLM；
3. old philosophical/cognitive/software term + language model；
4. candidate mechanism vocabulary + target task。

必须回答：
- 最近工作是否已有同一 decisive contrast？
- 是否已有同一 reader-correct/use-wrong signature？
- 是否已有同一 wrong destination、scale law和机制问题？
- 为什么本卡不只是 ACL 2026 generic representation-use gap？
- 主数据能否真实下载、许可是否可用、gold是否独立于LLM？
- 人工读20例后，有多少例relation真的成立？列出sample IDs。

候选提出者不能独自签署通过；必须有独立对抗审计者，并明确回答 `why_not_a_rename`。只允许三种结论：
1. N0/D0-PASS：exact collision 未发现、全文/appendix 已查、数据可得且 20 例通过；随后由注册表管理员决定是否 `READY-TO-SMOKE`；
2. HOLD：有一个明确待解决条件；
3. KILL/OCCUPIED：说明证据，不用委婉保留。

把结果追加到原卡底部，包含日期、检索式、最近三篇工作比较表、数据路径、20例抽样摘要和结论。
不要声称“这是全新现象”。
```

## Smoke-test 模板（只有用户明确切到验证阶段后使用）

```text
你只验证 {CARD_ID}；它已经通过 Phase 0/1，冻结卡位于原领域文档底部。

先读冻结的：dataset、sample IDs、neutral prompt、reader metrics、use metrics、wrong destinations、controls、kill condition。

限制：
- 首轮仅30–50例×两个模型家族；
- 使用已经常驻的服务，不得关闭、重启或改变其他服务；
- 不得临时改prompt救效应；
- 原始输出、解析失败和每个wrong destination全部保存；
- 先报告reader地板，再报告use gap；
- 达到kill condition立即停止，不扩模型；
- 只有出现预注册signature才建议3/5家族验证。

输出写回原卡：命令、commit/数据版本、模型全名、样本数、逐条件结果、错误去向、controls和READY/HOLD/KILL。
未经3/5家族与尺寸验证，不得写“普遍现象”。
```

## 卡片领取规则

- 一次只领取一张；合并族（例如 `CSS-06/07/13`）算一张；
- 优先从总索引 Wave 1 开始；
- 已标 `ROUTE/OCCUPIED/HOLD` 的卡不得绕开边界自行跑；
- agent结束前必须把状态写回原卡，避免下一位重复劳动；
- 任何失败都保留：候选池也承担负结果记忆。
