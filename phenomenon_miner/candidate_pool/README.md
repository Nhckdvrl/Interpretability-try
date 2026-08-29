# Candidate Pool

这里是 **真正的选题工作区**。新题在这里完成：

```text
N0 breadth novelty
+ N1 depth novelty
+ D0 source feasibility
```

三者都 PASS 才叫 `DISCOVERY-PASS`，才允许 formal registration。这里不是模型实验队列。

## 当前唯一 survivor queue

[`CURRENT_SURVIVORS_2026-08-29.md`](CURRENT_SURVIVORS_2026-08-29.md) 是 v4 原则下对 Batch 1 + Batch 2 V2 + Batch 3 共 30 个明确题目身份的重新 survival audit，也是当前唯一 discovery queue。

当前结论：

- 19 个题继续 discovery；
- 2 个旧题已经是 legacy active project，继续按各自 contract 处理；
- 9 个题 terminal / route out；
- **没有任何新题因为这次总审计自动获得 `DISCOVERY-PASS` 或模型调用权限。**

每个 retained candidate 还必须完成自己的 full-text/appendix/code N1 closure、exact source/version/license，以及 >=20 个真实 examples/pairs 的 feasibility audit。

## Batch 文件的角色

以下文件现在全部是 **provenance / prior-round audit**，不是当前 shortlist：

- Batch 3：[`BATCH3_HAMDI_MOTHER_PAPER_N0_SURVIVORS_10_2026-08-29.md`](BATCH3_HAMDI_MOTHER_PAPER_N0_SURVIVORS_10_2026-08-29.md) 与其 ledger；
- Batch 2：[`BATCH2_DEEP_N0_SURVIVORS_10_V2_2026-08-28.md`](BATCH2_DEEP_N0_SURVIVORS_10_V2_2026-08-28.md) 与 brainstorm/audit files；
- Batch 1：[`DEEP_N0_SURVIVORS_10_2026-08-28.md`](DEEP_N0_SURVIVORS_10_2026-08-28.md) 与 [`audits/ADVERSARIAL_N0_TEN_2026-08-28.md`](audits/ADVERSARIAL_N0_TEN_2026-08-28.md)。

旧 `SURVIVE` / `A+` 只说明当时没有被那一轮杀掉，不能覆盖当前 v4 verdict。

## D0 feasibility 在这里就要完成

每个准备晋级的候选必须写出：

```yaml
source:
version:
license:
statistical_unit:
gold_source:
extraction_or_construction_recipe:
estimated_eligible_count:
feasibility_audit_ids: []   # >=20 real examples
external_validation_anchor:
d0_source_feasibility_verdict:
```

不能写“之后从 Wikipedia / HF / 某 benchmark 找一些数据”。若没有现成 paired set，必须已经有 public natural source + deterministic construction recipe + dry-run yield + independently provable gold。

## 长期 idea inventory

`01_...`–`12_...` 保存领域化 idea cards、邻近文献、brainstorm 和死亡回填，用于找新题和防止 rename revival。它们不是 162 个 active candidates。

完整状态推进看 [`../PROCESS.md`](../PROCESS.md)；模型调用权限只看 [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md)。
