# D0 source audit — Source-Discount Recovery

Date: 2026-08-29  
Verdict: `D0-AUDITING` — **source pool is valid; no frozen scenario set is signed yet**.

The purpose of this audit is to prevent a shortcut in which a prompt merely calls one source “high reliability” and another “low reliability.” Formal D0 requires real source histories from which report-specific likelihood ratios can be recomputed on disjoint tasks.

## Primary source candidate: NetEaseCrowd

The released NetEaseCrowd data are especially suitable:

- 2,413 anonymized workers;
- 999,799 tasks and 6,016,319 annotations;
- fields include `taskId`, `tasksetId`, `workerId`, `answer`, `completeTime`, `truth`, and `capability`;
- multiple real task/capability families;
- license: **CC BY-SA 4.0**.

The formal builder is [`data/build_natural_d0.py`](data/build_natural_d0.py).

### Frozen extraction contract

For each capability and binary truth-label pair:

1. split by **task ID**, never annotation row, into fixed 60% calibration / 40% validation tasks;
2. estimate each worker's report-specific LRs with Jeffreys 0.5-cell smoothing;
3. responses outside the selected binary labels remain in denominators rather than being silently discarded;
4. require both workers to be above chance on both splits;
5. require the same source ordering in both message directions on both splits:

```text
1 < low_target_lr < high_target_lr
0 < high_other_lr < low_other_lr < 1
```

6. require a nontrivial high/low accuracy gap and LR margin;
7. use each selected worker in **at most one frozen scenario globally**, not once per capability or label pair;
8. never expose the target task's truth to the model.

The builder stores calibration and validation source-history sample sizes and validation LR/accuracy metadata for later manual auditing.

## Delay material

Delay cannot be arbitrary filler and cannot repeat the focal message. When the real NetEase columns are supplied, the builder deterministically samples unrelated administrative rows from other tasks and exposes only task ID, task-set ID and completion time. It explicitly excludes the focal high/low worker identities and does not expose answers or truths.

Short and long delay conditions differ by the number of unrelated administrative records. Source reinstatement restores the focal source identity plus its calibration profile without repeating the earlier message. The matched-length control restores only record/protocol context.

## Second source candidate: CIFAR-10H

CIFAR-10H supplies raw annotator-level labels for CIFAR-10 test images and can provide a genuinely different source domain. Its raw release contains anonymized annotator IDs, true/chosen categories and image IDs; the published data are CC BY-NC-SA 4.0. Binary class-pair slices can use the same task/image-disjoint LR derivation.

It should not enter a frozen D0 merely because the dataset exists: selected annotator pairs must independently satisfy the same two-direction LR ordering on calibration and validation.

## Rejected / lower-priority sources

- **Toloka Relevance-2** is statistically attractive, but this audit did not establish a sufficiently clear redistributable dataset license for the formal frozen bank.
- public **RTE crowd** reprocessings expose worker/response/gold data, but their redistribution chain is less clean than NetEaseCrowd/CIFAR-10H.

## Why D0 is not signed yet

A dataset card and a correct builder are not D0-PASS. The actual released NetEaseCrowd files must be materialized, hashed, passed through the builder, and produce at least 20 source-disjoint scenarios spanning at least two real capability domains. Then a fixed random sample of 20 generated rows must be manually checked for:

- worker histories and task-disjoint split;
- calibration/validation accuracy and both LR directions;
- global worker non-reuse;
- same message content across high/low source;
- delay rows containing only unrelated administrative metadata;
- reinstatement not repeating the message;
- license/provenance and prompt naturalness.

Until those concrete rows exist, `validation_authorized` remains `false`.
