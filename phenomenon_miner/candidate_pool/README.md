# Candidate Pool

这里是 **真正的选题工作区**。新题在这里完成：

```text
N0 breadth novelty
+ N1 depth novelty
+ D0 source feasibility
```

三者都 PASS 才叫 `DISCOVERY-PASS`，才允许 formal registration。这里不是模型实验队列。

## 当前批次

### Batch 3 — mother-paper extensions（当前优先）

- [`BATCH3_HAMDI_MOTHER_PAPER_N0_SURVIVORS_10_2026-08-29.md`](BATCH3_HAMDI_MOTHER_PAPER_N0_SURVIVORS_10_2026-08-29.md)
- [`BATCH3_HAMDI_MOTHER_PAPER_LEDGER_2026-08-29.md`](BATCH3_HAMDI_MOTHER_PAPER_LEDGER_2026-08-29.md)

这些 `reviewer-mode N0 survivor` **还不是确定题目**。下一步不是模型 smoke，而是把每个候选的 N1 depth audit 和 D0 source-feasibility 做透。

### Batch 2

- [`BATCH2_DEEP_N0_SURVIVORS_10_V2_2026-08-28.md`](BATCH2_DEEP_N0_SURVIVORS_10_V2_2026-08-28.md)
- [`BATCH2_BRAINSTORM_LEDGER_2026-08-28.md`](BATCH2_BRAINSTORM_LEDGER_2026-08-28.md)
- [`audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md`](audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md)

### Batch 1

- [`DEEP_N0_SURVIVORS_10_2026-08-28.md`](DEEP_N0_SURVIVORS_10_2026-08-28.md)
- [`audits/ADVERSARIAL_N0_TEN_2026-08-28.md`](audits/ADVERSARIAL_N0_TEN_2026-08-28.md)

旧 shortlist / survivor 只代表当时 discovery 进度，不能自动满足 v4 的完整 discovery package。

## D0 feasibility 在这里就要完成

每个准备晋级的候选必须在 candidate card 中写出：

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

不能写“之后从 Wikipedia / HF / 某 benchmark 找一些数据”。

若没有现成 paired set，必须已经有 public natural source + deterministic construction recipe + dry-run yield + independently provable gold。否则继续留在这里，不进入 active。

## 长期 idea inventory

`01_...`–`12_...` 保存领域化 idea cards、邻近文献、brainstorm 和死亡回填，用于找新题和防止 rename revival。

完整状态推进看 [`../PROCESS.md`](../PROCESS.md)。
