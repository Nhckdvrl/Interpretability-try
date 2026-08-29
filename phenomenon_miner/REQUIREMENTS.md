# 现象筛选要求

版本：2026-08-29  
状态：`FROZEN v3 — discovery package 前置`

## 一句话目标

寻找一个**自然、普通人能理解、具有结构性反直觉、在有能力模型上仍值得解释、数据可真实落地、并且在投入实验前已经完成深度 novelty 审计**的 LLM 现象。

## 0. 新题正式注册的必要条件

新项目进入正式注册前必须同时满足：

```text
N0 breadth PASS
+ N1 depth PASS
+ D0 source-feasibility PASS
```

也就是说，在“确定题目”之前必须已经知道：

- strongest neighbor 是谁；
- 为什么不是 rename / mother inclusion；
- 数据从哪里来；
- license 是否允许；
- gold 如何得到；
- 独立 statistical unit 是什么；
- 大约能拿到多少 eligible cases；
- 如果需要构造，具体 deterministic recipe 是什么；
- 至少 20 个真实 source examples / candidate pairs 已人工看过。

这些问题答不清，不是 active project，只是 candidate。

---

## A. 问题本身

1. **自然。** 不依赖任意符号、特殊标签或长篇自定义规则才成立。
2. **一句话能讲清。** 最好能写成“模型明明 A，却仍然 B”。
3. **母问题够大。** 指向知识、信念、实体、现实性、因果、记忆、推理、交流、行动或社会认知等基本问题。
4. **有结构。** 优先 dissociation、sign reversal、cliff、U-shape、path dependence，而不是泛化的低准确率。
5. **不是 prompt artifact。** 简短客观问法、paraphrase、answer-order 等控制后性质仍在。
6. **先题后法。** 不从 SAE / head / probe / patching 工具反推故事。

## B. 数据与 D0 feasibility 必须前置

7. **不是“以后再找数据”。** candidate 阶段就要锁定具体 source/version。
8. **license 先解决。** 公开可访问不等于允许 adaptation/redistribution；条件不清则 HOLD。
9. **gold 必须独立。** 来自 source、正式 protocol、可执行语义或数学/程序 oracle，不由研究者看模型输出后决定。
10. **数量要预估。** 在注册前通过 source statistics 或 dry-run 证明有足够独立 eligible units。
11. **statistical unit 要真实独立。** participant swap、answer order、paraphrase、同一 game 的多个条件不能冒充样本量。
12. **20 例 feasibility audit。** 从真实 source / candidate pairs 中随机抽至少 20 个，检查 naturalness、gold、confound 和转换有效性。
13. **构造方法也要前置。** 若没有现成 paired data，注册前必须已有 executable deterministic recipe、seed、过滤规则、gold proof 和预计 yield。
14. **构造必须锚定自然 source。** pure synthetic toy bank 不能独立承担 paper-level naturalness/generalization；至少要有公开自然 source 和 external validation anchor。
15. **注册后不得找数据救题。** 若 frozen materialization 发现 source 根本不够或必须换 recipe，退回 discovery，不在 active 中继续搜数据。

## C. Novelty 必须在选题阶段做透

16. **母现象可以已有。** 人类 literature 是 anchor，不自动构成 LLM collision。
17. **N0 做广搜。** exact/near-exact phenotype、mother inclusion、wrong destination、同义词与 repo death family。
18. **N1 做深审。** strongest 3–5 papers 全文、appendix、supplement/code、citation chain、successor、mechanism occupancy、scale survival。
19. **N0/N1 都在 formal registration 之前。** 不允许把决定性 novelty search 推迟到 smoke 后。
20. **没有 routine post-smoke N1。** 只有 claim 实质改变、出现新论文或 reviewer 指出具体漏项时做 targeted novelty refresh。
21. **生成者与审计者分离。** 至少一个独立 reviewer 负责主动找杀题证据。
22. **不能靠换模型/数据/领域维持 novelty。** decisive contrast 已被完整做过就 KILL。
23. **只写截至日期未检索到覆盖。** 不写绝对 `first`。

## D. Behavior first 与一般性

24. **D0 freeze 后才模型调用。** discovery feasibility PASS 不等于立刻运行；最终 rows/IDs/hash/config 仍需冻结。
25. **先行为，后机制。** behavior prerequisite 没过，不靠 hidden-state evidence 续命。
26. **能力 gate。** 模型必须在 matched control 上理解任务、关系和输出接口。
27. **两家族 smoke。** 先用便宜、独立的两个模型家族做 fatal test。
28. **3/5 家族确认。** 正式 generality 至少三个独立家族同方向。
29. **至少一个三尺寸序列。** 用于判断 scaling survival，而不是单 checkpoint 奇观。
30. **强模型 kill test。** 更强模型若几乎消除现象，应优先停止而非机制化弱模型错误。
31. **paired raw cases 优先。** 保存单样本轨迹、错误落点和恢复，不只看 aggregate。
32. **deterministic scoring 优先。** 不依赖昂贵 LLM judge；自由生成必须保存原文并审计。
33. **nuisance controls。** 长度、格式、标签位置、措辞、提示难度必须闭环。

## E. Mechanism 与方法口

34. **至少两个竞争机制。** 它们必须对 layer/position/path/intervention/scaling 给出不同预测。
35. **机制不能是行为换句话说。** “更关注 X”不够，必须能局部化与因果干预。
36. **适合 matched comparison。** 优先最小自然对照和 causal interchange。
37. **机制应影响方法。** H1/H2 若最后都只导向 generic SFT，机制价值不足。
38. **机制前不铺大预算。** behavior/generality 未过，不扫大量层/头/SAE/模型。

## F. Stop-loss

39. exact collision、mother inclusion、数据路径不成立、gold 不稳、能力地板、artifact、强模型消失、只在单模型成立：直接 KILL/HOLD。
40. 不因 sunk cost 换弱模型、挑 subset、改 readout、改阈值、换名字续命。
41. terminal project 进入 archive；失败原因要能阻止未来 rename revival。

## “确定好的题目”是什么

在本仓库里，**题目本身确定**与**现象行为已经验证**是两回事。

### 题目确定（可正式注册）

```text
自然 mother question
+ decisive contrast
+ N0 PASS
+ N1 PASS
+ D0 source-feasibility PASS
+ mechanism fork
+ hard kill
```

### 现象确定（可进入机制）

还必须额外满足：

```text
frozen D0
+ behavioral smoke
+ artifact audit
+ cross-family / cross-size generality
+ strong-model survival
```

完整状态机见 [`PROCESS.md`](PROCESS.md)。
