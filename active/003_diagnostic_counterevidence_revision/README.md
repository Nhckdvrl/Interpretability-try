# 003 — 决定性反证出现后，模型的结论修正在哪一步失败？

**Status:** `PRE-CANDIDATE / PAPER-AUDIT-PASSED / G0-NOT-RUN`  
**Created:** 2026-08-26  
**Primary testbed:** MedEinst (ACL 2026)

> 本目录当前只保存研究计划。行为 G0 通过前，禁止开始 probe、SAE、attention sweep 或 activation patching。

## 1. Mother question

一个模型已经能正确解决原始样本，但输入只改变少量决定性证据、正确标签因此翻转后，模型却仍坚持原标签。

本项目不研究“这种 failure 是否存在”；MedEinst 已经证明它存在。我们要回答的是：

> **模型的 revision pipeline 到底在哪一步断了？**

预注册三个竞争解释：

- **H1 证据表征失败**：新证据没有形成足以影响任务的内部表示。
- **H2 证据—先验仲裁失败**：新证据已经被正确表示，但旧标签先验在整合阶段继续占优。
- **H3 晚期回退**：中间层已经转向新标签，但后层 / 最终读出又回到旧标签。

三个结果必须导向不同的修复方法，否则机制分析没有价值。

## 2. 为什么值得实际验证

MedEinst 提供 5,383 组公开 control/trap 反事实 pair，覆盖 49 类标签。每个 pair 共享 `case_id`，trap 通过少量判别证据改变使正确标签翻转。

原论文已经在 open-weight 模型上报告稳定自然 failure：

- Qwen3-14B：Baseline Acc 44.12%，Bias Trap Rate 54.19%；
- Qwen3-32B：Baseline Acc 40.25%，Bias Trap Rate 43.46%；
- QwQ-32B：Bias Trap Rate 44.88%。

因此这里不是从 benchmark 总分猜一个细分错误；目标 failure 已由论文直接定义和计数。

公开资源：

- Paper: https://aclanthology.org/2026.acl-long.1847/
- Dataset: https://huggingface.co/datasets/zhui711/MedEinst
- Official repo: https://github.com/zhui711/MedEinst

## 3. Collision audit

### MedEinst — ACL 2026 Main

已经完成：

- control/trap counterfactual benchmark；
- Bias Trap Rate；
- 多模型评估；
- 类别级分析；
- 原标签回退、ranking / confidence 行为分析；
- 一个显式证据审计与因果推理 agent 方法。

没有完成：

- open-weight hidden-state failure localization；
- matched-pair activation interchange；
- changed-evidence → final decision 的 causal path；
- H1/H2/H3 三阶段裁决；
- 根据内部 failure location 设计 targeted repair。

因此不能声称“首次发现 anchoring / fixation”，也不能再做一个相似的外部 evidence-audit agent。

### mARC / flexible clinical reasoning work

2025–2026 的 mARC 工作证明熟悉模式可压过 decisive counterevidence，并研究更强 reasoning model 是否更灵活，但没有做上述内部 revision-stage causal analysis。

### Targeted mechanism search

截至 2026-08-26，针对以下组合进行检索：

- `Einstellung effect + mechanistic interpretability`
- `counterevidence + activation patching`
- `diagnostic anchoring + hidden states`
- `clinical evidence + causal tracing`
- `disease prior + causal intervention`

尚未发现已经系统裁决 H1/H2/H3 的直接工作。

### 最大叙事风险

原 MedEinst 已经提出“强统计先验压过低概率反证”的解释。

如果我们的结果只是“旧 prior 很强”或“某层能读出 evidence”，则没有新的 narrative package，直接 KILL。

我们的独立贡献必须是：

> **把 revision failure 分解为 evidence encoding、evidence–prior arbitration、late readout reversion，并用选择性因果干预裁决其主导位置和边界条件。**

## 4. Frozen behavioral G0

### G0-A：官方任务复现

优先：

- Discovery: Qwen3-14B
- Confirmation: Qwen3-32B

按官方 pair 定义记录：

```text
control_correct
trap_correct
trap_predicts_control_label
```

核心自然 failure：

```text
control 正确
AND trap 错误
AND trap 回到 control label
```

### G0-B：机制兼容的离散 readout

自由生成标签可能是多 token，也可能带长推理，不利于干净 causal analysis。

因此只额外建立一个**不修改原 narrative**的二选一视图：

```text
Case: <original narrative>
A: <control label>
B: <trap label>
Answer: A or B
```

约束：

- control/trap 使用完全相同的两个候选；
- A/B 映射随机平衡；
- 候选顺序对半翻转；
- gold 直接来自原数据；
- 不通过 prompt engineering 人为诱导 failure。

这个阶段只回答：原 benchmark 的自然 fixation 在一个可做因果分析的离散 readout 中是否仍存在。

### STOP gate

进入 mechanism 前至少要求：

```text
>= 200 个自然 fixation pairs
至少一个 pinned open-weight model 的 BTR >= 20%
A/B position balance 后效应仍然明显
至少两个类别组中成立
```

若不满足：`STOP_NO_MECHANISM_SCALE`。

如果只有官方自由生成会错、二选一格式几乎不再出现 fixation：`HOLD_NO_CLEAN_CAUSAL_READOUT`。

禁止换更弱模型、修改样本或调 prompt 来制造错误。

## 5. Mechanism prerequisites

### 5.1 changed-evidence span

control/trap 是 paired minimal edits。优先通过 token/sentence diff 自动定位变化 span，不新增人工标注。

如果大量 pair 是全局重写而非局部判别证据，`HOLD_BAD_MATCHED_PAIRS`。

### 5.2 明确决策变量

二选一输出定义：

```text
Δ = logit(correct trap label) - logit(old control label)
```

A/B 随机化后，可用于 layerwise readout、activation patching、path patching 和 targeted ablation。

### 5.3 选择性 causal control

合格干预应改变“新标签 vs 旧标签”的相对偏好，同时尽量不改变：

- A/B 位置偏置；
- unrelated pairs；
- control baseline；
- 一般输出能力。

如果 intervention 只是整体推向 A/B、整体降低置信度或造成一般退化，不算机制证据。

## 6. Mechanism ladder

### M1 — revision trajectory

比较：

- control success
- trap robust success
- trap fixation failure
- non-fixation stochastic failure

追踪各层 A/B preference。

H3 的关键预测是：fixation 样本在中间层曾偏向新标签，随后后层重新翻回旧标签。

### M2 — 反证是否真正进入计算

使用 control/trap matched pair 做 changed-evidence-span activation interchange。

双向测试：

- trap evidence → control
- control evidence → trap

若新证据的 causal signal 很弱，支持 H1 或说明 intervention unit 不成立；若 evidence signal 明显但完整 trap 仍停留旧标签，更支持 H2；若中间已翻转而后层逆转，更支持 H3。

### M3 — 找到 revision 被削弱 / 反转的位置

沿 changed evidence → final decision position 做 causal mediation / path patching。

目标不是找一个“Einstellung head”，而是判断 failure 首次发生于：

```text
evidence encoding
→ evidence-to-label integration
→ late decision/readout
```

### M4 — generalization

Discovery: Qwen3-14B。  
Confirmation: Qwen3-32B。

至少跨多个高/低 Bias Trap Rate 类别验证计算级结论。单类别、单模型漂亮 circuit 不足以支持一般 claim。

## 7. Mechanism → method

### 若支持 H1

做 **Counterevidence-Sensitive Representation Training**：

- 使用公开 train control/trap pairs；
- 对 changed evidence 做局部对比目标；
- 要求最小证据翻转产生 diagnosis-relevant representation shift。

### 若支持 H2

做 **Evidence–Prior Arbitration Tuning**：

- 只针对定位到的 mediator layers/modules；
- 训练 paired ranking margin；
- 新证据出现后新标签应超过旧标签；
- 同时保持 control 性能，避免简单反先验化。

### 若支持 H3

做 **Anti-Reversion Late-Layer Repair**：

- 只调晚层/readout；
- 约束正确的中层 preference 不得在后层翻回；
- 或设计轻量 inference-time late-layer gating。

如果 H1/H2/H3 最后都只能导向同一个 generic SFT，说明机制分析没有真正影响方法设计，项目应降级。

## 8. 论文尺度

成功叙事应是：

```text
稳定自然 fixation
→ 三阶段 revision hypothesis
→ matched-pair causal localization
→ robust vs failure trajectory
→ 跨类别/模型边界
→ mechanism-specific repair
```

而不是：

> “MedEinst 上找到一个 layer。”

理想 abstract 至少有四条 headline finding：

1. fixation 的主导 failure stage；
2. robust vs fixation 的内部 trajectory 差异；
3. 选择性因果干预；
4. mechanism-guided repair 与普通准确率的 trade-off。

## 9. Hard KILL rules

- `KILL_BEHAVIOR_GONE`：当前 pinned open model 不复现自然 trap。
- `HOLD_NO_CLEAN_CAUSAL_READOUT`：二选一视图不保留 failure。
- `HOLD_BAD_MATCHED_PAIRS`：pair diff 不能形成干净 evidence contrast。
- `KILL_NO_CAUSAL_MECHANISM`：只有 decodability，没有选择性因果证据。
- `KILL_NO_NEW_NARRATIVE`：结论只能复述“prior 压过 evidence”。
- `KILL_METHOD_COLLISION`：最终方法只是 MedEinst ECR-Agent / generic evidence audit 的轻微变体。
- `KILL_NO_GENERALIZATION`：只在单类别或单模型成立。

## 10. Current verdict

```text
PRE-CANDIDATE
PAPER-AUDIT-PASSED
PUBLIC-DATA-AVAILABLE
NATURAL-FAILURE-REPORTED
G0-NOT-RUN
```

下一步仅允许先实现行为 G0；在用户确认前，不进入机制实验代码。
