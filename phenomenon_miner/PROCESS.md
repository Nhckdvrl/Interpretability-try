# 现象发现、审计、验证与机制流程

版本：2026-08-28
状态：`FROZEN v2`，与 `REQUIREMENTS.md` v2 对齐。

## 唯一合法流水线

```text
母问题 / 老问题 → 一句话自然矛盾 + 日常例子
→ N0 前置新颖性审计（exact phenotype + 母现象包含关系）
→ 独立对抗复核
→ D0 数据 / license / gold / 20例人工抽样
→ 冻结验证合同 → READY-TO-SMOKE
→ 30–50例 × 两个便宜家族
→ raw case / scorer / capability / artifact 审计
→ N1 按真实错误形状做二次新颖性审计
→ 3/5 家族与跨尺寸 → 强模型杀伤
→ 机制先决条件 → 白盒解释与机制导出方法
```

`candidate_pool` 是假设库存，不是实验队列。旧 Tier、首轮 `PROMOTE/ADVANCE` 都不能跳过 N0、独立复核和 D0。唯一有权调用模型的状态是注册表中的 `READY-TO-SMOKE`。

## 两次 novelty 审计

- **N0，运行模型前：** 查 exact behavior、decisive contrast、母现象包含和机制占位。exact behavior 已知时，discovery 线直接 KILL。只有用户明确选择机制续作，才能转 mechanism-followup 线，且不得宣称新行为。
- **N1，smoke 后、扩模型前：** 用真实错误目的地、曲线、scale 趋势和选择性 controls 再查。N1 捕获 N0 时未知的 phenotype 词汇，不是把检索推迟到实验后。

详见 [`NOVELTY_GATE.md`](NOVELTY_GATE.md)。

## N0 强制产物

1. 不依赖数据集名的一句话主张；
2. exact task × manipulation、普通语言 anomaly、母现象 × decisive property 四轮检索；
3. 2024–2026 顶会、arXiv 和引用链；
4. 最近 3–5 篇论文全文/appendix 比较；
5. `why_not_a_rename`；
6. 非候选提出者的独立 `PASS/HOLD/KILL`；
7. 数据路径、license、gold 与 20 个样例 ID；
8. 冻结 scorer、promotion signature、kill condition。

缺一项不得 `READY-TO-SMOKE`。审计冲突默认 `HOLD`。

## 杀题规则

exact/near-exact 已占、只是换数据/领域/语言/payload/readout、机制也已做完、gold 不自然、只在弱模型或特殊提示存在、可由 artifact/能力地板解释、或需挑模板续命：标记 `KILLED`，移出队列，永久保留审计。`HOLD/WATCH` 同样不得调度。

```text
IDEA → N0-AUDITING → N0-PASS → D0-AUDITING → READY-TO-SMOKE
→ PILOT → N1-AUDITING → GENERALITY-CHECK → MECHANISM-READY → ADVANCE
任何节点 → HOLD / KILLED
```

权威状态只看 [`candidate_pool/AUDIT_REGISTRY.md`](candidate_pool/AUDIT_REGISTRY.md)。
