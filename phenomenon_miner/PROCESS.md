# 现象发现、审计、验证与机制流程

版本：2026-08-29
状态：`FROZEN v3`。

## 唯一合法流水线

```text
母问题 / 自然现象 → 一句话 LLM 矛盾 + 日常例子
→ N0 前置新颖性审计（exact / near-exact LLM phenotype + decisive contrast）
→ D0 数据 / license / gold / 20例人工抽样
→ 冻结验证合同 → READY-TO-SMOKE
→ 30–50例 × 两个便宜家族
→ raw case / scorer / capability / artifact 审计
→ N1 按真实错误形状做二次新颖性审计
→ 3/5 家族与跨尺寸 → 强模型杀伤
→ 机制先决条件 → 白盒解释与机制导出方法
```

`candidate_pool` 是假设库存，不是实验队列。唯一有权调用模型的状态是注册表中的 `READY-TO-SMOKE`。

## N0 的范围

本仓库**允许并鼓励从已知的人类认知、决策、社会行为或经典自然现象出发**，再问 LLM 是否出现一个可复现、可机制化的 failure。因而：

- “人类中已有同名母现象”本身**不是 collision**；它通常是 natural mother / anchor。
- 真正的 discovery collision 是：已有 LLM 工作已经建立了同一 exact/near-exact phenotype，或一个更宽的 LLM 结果逻辑上完整包含本题 decisive contrast，或同一 LLM 机制已被直接做完。
- 换数据、领域、语言、payload、readout 不能制造新题；但“人类母现象 → 尚未报告的 LLM failure + 可证伪 controls”可以进入 discovery/mechanism lane。

若候选已经完成一轮足够深入、留有 strongest neighbor / why-not-a-rename / decisive contrast / hard-kill 的 adversarial N0，项目负责人可以直接接受该审计为 `N0-PASS`。**不得为了形式上的第二签名重复做一遍相同的大规模检索。** 只有当题目合同实质改变、审计明显过期、或出现具体 collision 争议时才重开 N0。

## N1

N1 在 smoke 后、扩模型前进行。它使用真实 wrong destination、曲线、scale 趋势和选择性 controls 再查 LLM 邻域，捕获 N0 时无法知道的 phenotype 词汇。N1 不能被提前的重复 N0 替代。

## D0 是独立硬门

N0 通过不代表可以跑模型。D0 必须解决：

1. 外部数据/实验材料的精确版本与 license；
2. gold 是否来自源数据/原作者 protocol，而不是为了 harness 人工拍脑袋；
3. manipulation 是否是最小变换，是否引入新的语义、utility、长度或 source confound；
4. calibration 与验证数据是否泄漏；
5. 至少 20 个随机样本的人工审计 ID 与结果；
6. statistical unit 是否真实独立，不能把 participant swap、prompt paraphrase、answer order 或同一 game 的重复条件冒充独立样本；
7. 数据不够硬时必须 `HOLD-D0`，不得为了让 harness 可运行而 synthetic 补齐。

## 杀题 / HOLD 规则

exact/near-exact LLM 行为已占、只是换表面包装、gold 不自然、只在弱模型或特殊提示存在、可由 artifact/能力地板解释、或需挑模板续命：`KILLED`。数据 license/gold/独立性不满足但科学问题仍成立：`HOLD-D0`。

```text
IDEA → N0-AUDITING → N0-PASS → D0-AUDITING → READY-TO-SMOKE
→ PILOT → N1-AUDITING → GENERALITY-CHECK → MECHANISM-READY → ADVANCE
任何节点 → HOLD / KILLED
```

权威状态只看 [`candidate_pool/AUDIT_REGISTRY.md`](candidate_pool/AUDIT_REGISTRY.md)。
