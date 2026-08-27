# RVC novelty-first 淘汰审计

日期：2026-08-28。范围 14 张卡。

| 卡 | 裁决 | 决定性理由 |
|---|---|---|
| RVC-01 | **ADVANCE** | certified countermodel 已成立却未否决对应 universal 的 exact gate failure 尚未找到 |
| RVC-02 | OCCUPIED | exception/non-monotonic reasoning 是 LogicBench 等既有核心轴 |
| RVC-03 | OCCUPIED | first-error localization 与 global verification 已被 Validation Gap、Hard2Verify 覆盖 |
| RVC-04 | **WATCH** | exact downstream witness fusion 可能有空位，但量词与 entity-slot 母工作很近 |
| RVC-05 | KILL | constraint matrix 正确但选择错误是 generic representation-use / planning gap |
| RVC-06 | KILL | at-least→exactly 是基础数量词能力 |
| RVC-07 | OCCUPIED | computation correct / threshold decision wrong 被 Validation Gap 包含 |
| RVC-08 | OCCUPIED | necessary/sufficient converse fallacy 已有大量行为与机制研究 |
| RVC-09 | OCCUPIED | unknown→false 是 open-world/closed-world 与 abstention 核心问题 |
| RVC-10 | OCCUPIED | conflict recognized / hybrid answer 落入 conflicting-context RAG |
| RVC-11 | OCCUPIED | node truth vs proof-edge validity 属于 reasoning-chain verifier 中心任务 |
| RVC-12 | OCCUPIED | 多一条 proof 伤害答案与 redundancy/detrimental context 太近 |
| RVC-13 | KILL | feasible→inevitable 是一般 existential/modal reasoning |
| RVC-14 | OCCUPIED | rationale correct / intermediate copied 是 answer extraction/faithfulness |

## ADVANCE：已认证反例未触发全称否决

> 模型亲自确认了一个反例满足前提并违反结论，却仍说原来的“所有……”成立。

[COUNTERMATH](https://openreview.net/forum?id=A31Ep22iQ7) 与 [Learning to Disprove](https://arxiv.org/abs/2603.19514) 研究反例生成，[The Validation Gap](https://aclanthology.org/2025.emnlp-main.1495/) 研究 solve/verify 解离；本轮没有找到“同一 valid countermodel 已被模型或形式工具逐条件认证，却没有获得对应 universal 的 veto 权”的跨模型 phenotype 与机制研究。

自然主数据应来自 ReClor/LogiQA/ContractNLI 的 universal、only、necessary claims，加上 FOLIO 的形式 backing。primary 叙事用自然政策、合同和论证；形式题只负责保证 countermodel 有效。

决定性四条件：

```text
valid counterexample, self-generated
valid counterexample, externally supplied
invalid near-counterexample
supporting example
```

只有三个必要判断都正确、conclusion verdict 仍保留 universal 才算；反例生成错不计。`countermodel-target binding failure` 与 `late affirmation overrides veto` 对 activation patch 的层/位置给出相反预测。

主要风险是强模型一旦承认 valid counterexample 就近乎 100% 否决。它只因低成本证伪和 exact 空位进入候选，不能预先宣称存在。

## WATCH：匿名存在见证的下游融合

> 模型会解释“有人懂税务、有人懂日语”不保证同一个人，排班时却仍安排一个未被证明存在的“双技能者”。

必须用真实 team roster / database query / scheduling 任务，不得用批量 `someone A; someone B` 玩具模板。本轮未找到 exact report-correct/action-fused 研究；但量词 benchmark、discourse referent 与 [Slot Machines](https://arxiv.org/abs/2604.21139) 已很近。只有跨家族下游 fusion 且错误稳定落在虚构 joint witness，才升级。
