# Discovery-stage Novelty Gate

版本：2026-08-29  
状态：`v2 — N0/N1 均在 formal registration 之前完成`

## 原则

Novelty 不是模型实验后的补票。一个题目值得投入 GPU 之前，必须已经把“是否撞车”查到足够深。

```text
N0 = breadth screen
N1 = depth closure
N0 + N1 = registration 前的一套完整 novelty audit
```

没有常规的 post-smoke N1。

## N0 — breadth screen

冻结 candidate claim：

> 模型能正确完成 A；但在自然条件 B 下，会系统地把 C 写成 D。

N0 搜：

- exact task / relation / phenotype；
- 普通语言 anomaly；
- mother phenomenon + LLM；
- decisive contrast / wrong destination；
- repo death families / rename；
- mechanism vocabulary 的明显占位。

目标是快速淘汰 obvious collision / rename / mother inclusion。

## N1 — depth closure

N1 只对 N0 survivor 做，而且**必须在 project registration 前完成**。

必须检查：

- strongest 3–5 papers 的全文；
- appendix / supplement / limitations；
- public code / released prompts / dataset notes；
- predecessor / successor / citation chain；
- mother paper 是否已经顺手覆盖下一问；
- exact decisive contrast 是否已存在；
- 已有机制工作是否完整吸收我们的 causal question；
- 邻近现象是否已有 scale-disappearance 证据。

输出必须写清：

```text
strongest_neighbor
what_it_already_solves
our_decisive_difference
why_not_a_rename
mother_inclusion_test
mechanism_occupancy
scale_survival_risk
hard_kill
search_date
```

裁决：`PASS / HOLD / KILLED-COLLISION`。

## Discovery 之后不重复 novelty search

一旦 `N1-PASS` 并正式注册，novelty audit 视为 closed。模型输出不应该成为“现在再查一次文献”的理由。

只在以下情况做 `NOVELTY-REFRESH`：

1. core claim / decisive contrast / mechanism question 实质改变；
2. 审计日期以后出现具体新论文；
3. 外部 reviewer 指出此前漏掉的具体近邻。

Refresh 只检查受影响部分，不重新跑一整套 N0/N1 仪式。

## 与 D0 的关系

Novelty 通过还不够。formal registration 之前必须同时通过 `D0-SOURCE-FEASIBILITY`：具体 source/version/license/gold/unit/count/construction recipe 都要可落地。

完整要求见 [`PROCESS.md`](PROCESS.md) 与 [`REQUIREMENTS.md`](REQUIREMENTS.md)。

## 新候选审计模板

```yaml
candidate_id:
claim_sentence:
lane: discovery

n0:
  search_date:
  search_queries: []
  obvious_neighbors: []
  verdict: PASS | HOLD | KILLED-COLLISION

n1:
  strongest_papers: []
  full_text_checked: true
  appendix_checked: true
  code_or_supplement_checked: true
  citation_chain_checked: true
  mother_inclusion_test:
  why_not_a_rename:
  mechanism_occupancy:
  scale_survival_risk:
  verdict: PASS | HOLD | KILLED-COLLISION

novelty_refresh_trigger: null
```

只能写“截至 audit date 未检索到完整覆盖”，不能写绝对的 `first` / `nobody has studied`。
