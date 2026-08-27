# 前置新颖性门：先杀撞车题，再花模型预算

版本：2026-08-28

## 两条路线

- **Discovery lane：** exact behavior 尚未被报道。
- **Mechanism-followup lane：** 行为已知但机制未解；只有用户明确授权才进入，不能冒充新现象。

默认只允许 discovery lane。

## N0：模型前全文审计

主张必须冻结成：“模型能正确完成 A；但在自然条件 B 下，会系统地把 C 写成 D。”

检索四轮：exact task + relation；普通语言 anomaly；mother phenomenon + decisive contrast/wrong destination；mechanism vocabulary + downstream interface。覆盖近义词、旧术语、2024–2026 ACL/EMNLP/NAACL、ICLR/ICML/NeurIPS、arXiv 和引用链。

最近 3–5 篇邻近论文必须检查主文、appendix、limitations、引用/被引链和后续版本。只看标题/摘要不能签署通过。

## 包含测试

去掉数据集、语言、领域和对象名后主张相同，默认按 rename KILL。必须判断：exact behavior 是否已有；是否只是母现象切片；是否只换 payload 或加 readout；既有 probe/patch/intervention 是否已回答机制；邻近工作是否显示随规模消失。

## 独立复核

候选提出者不得是唯一签署者。第二位审计者只负责找杀题证据。裁决：`N0-PASS`、`HOLD`、`KILLED-COLLISION`。

## D0 数据门

N0 后才检查公开路径/版本/license、独立 gold、relation 有效性、至少 20 个随机原例和 IDs。N0/D0 均过，才能 `validation_authorized: true`。

## N1

Smoke 后按真实错误目的地、形状、reader/use 解离、scale law 和 controls 再检索。N1 撞车立即 KILL，不得因 sunk cost 压窄续命。

```yaml
candidate_id:
claim_sentence:
lane: discovery
search_date:
search_queries: []
closest_papers: []
full_text_checked: false
mother_inclusion_test:
why_not_a_rename:
mechanism_occupancy:
scale_survival_evidence:
proposer:
independent_auditor:
n0_verdict: PASS | HOLD | KILLED-COLLISION
data_path:
license:
gold_source:
sample_audit_ids: []
d0_verdict: PASS | HOLD | KILLED-DATA
validation_authorized: false
```

只能写“截至某日未检索到完整覆盖”，不能写“没人做过”或 `first`。
