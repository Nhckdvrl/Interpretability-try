# D0 source audit — Source-Discount Recovery

Date: 2026-08-29  
Verdict: `D0-AUDITING` — **the release is materialized and a 22-scenario candidate bank passes every mechanical check; awaiting the human read of the re-drawn fixed-seed sample**.

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

## Materialization run — 2026-08-29

The release was downloaded, hashed (`RAW_MANIFEST.md`) and concatenated to 6,016,319 annotations, matching the published figure. Six capabilities are present: 50, 52, 53, 56, 69 and 126, each with truth labels {0, 1, 2}.

### The 18-scenario ceiling was structural, not a density limit

The first run produced exactly 18 scenarios and stopped. That was not the data: at the original 1.15 margin the 18 (capability, label-pair) cells hold 1,069 qualifying worker-disjoint pairs between them, and every cell yields candidates. The builder simply emitted at most one scenario per cell, so 6 capabilities x 3 label pairs bounded the bank at 18 — below the frozen `>=20`, and far below the `min_weighting_capable_pairs: 20` that `configs/frozen_g0.json` requires *after* the capability gate has removed rows.

The builder now takes `--max-pairs-per-cell` and allocates round-robin across cells: every cell contributes its best pair before any cell contributes a second. Workers remain globally unique. Relaxing `--min-per-class` was never considered, because density was never the constraint.

### Separation was raised from 1.15 to 2.0

At the original 1.15 margin the weakest frozen rows had a high/low report-LR ratio of 1.17 — mathematically ordered but far too small to ask whether the model later stops applying the difference. Measured headroom at several settings:

| LR margin | pairs/cell | scenarios | capabilities | smallest high/low target-LR ratio |
|---|---|---|---|---|
| 1.15 | 1 | 18 | 6 | 1.17 |
| 1.15 | 2 | 35 | 6 | 1.17 |
| 2.0 | 1 | 17 | 6 | 2.10 |
| **2.0** | **2** | **31** | **6** | **2.10** |
| 2.0 | 3 | 44 | 6 | 2.08 |
| 3.0 | 2 | 23 | 6 | 3.07 |

The setting is margin 2.0 with at most two pairs per cell. Over all six capabilities that yields 31 scenarios; capabilities 69 and 126 are then excluded (below), leaving **22 scenarios over 4 capabilities and 44 distinct annotators**, with no marginal rows.

### Capabilities 69 and 126 are excluded

Capability 69's third response option is literally "undecided", so its 0v2 and 1v2 cells ask whether the audited gold answer is a content option or a refusal to decide. That is faithful to the release, but it is a different kind of hypothesis from the capabilities where every option names a candidate answer, and the bootstrap unit is the scenario.

Capability 126 was dropped after the first human audit (below). The release marks it `documented: false` — it publishes the annotations and gold answers but not the question — so its background can only say that an internal task type offers three response options. That still supports a source-weighting test, but it is not a task a reader can recognise at a glance, and this project's `natural_setting_gold` means more than schema validity. The remaining four capabilities all carry a published question.

Both exclusions run before selection rather than by filtering the output, because annotators are unique across the whole bank and a dropped domain must release its workers back into the pool. For these two domains the released annotators turned out not to contend with the survivors — the 22 rows are identical to the corresponding rows of the 28-row bank — but that is an observed outcome, not a reason to filter instead of rebuild.

### First human audit — 2026-08-29

The 28-row bank's fixed-seed sample was read and returned **18/20 PASS, 2/20 HOLD-NATURALNESS**. Both holds were `126:0v1:002` and `126:1v2:002`, and both were held on `natural_setting` alone. The reader explicitly confirmed the two things this design is most exposed on: the intervening material carries only unrelated `task / task-set / completion-time` records with no case answer and no focal annotator, and the source reminder restores identity plus accuracy plus report-specific LRs **without** restating which option was reported — source calibration reinstated, message content not. The response was to drop capability 126 and re-freeze, not to relax the audit.

### Bug found and fixed: delay material could come from focal-source tasks

`_delay_blocks` filtered the focal annotators' *rows* and then deduplicated by task. A task both focal annotators had worked on survived that filter through some other worker's annotation, so 9 of the first 18 scenarios drew "unrelated administrative records" from tasks a focal source had in fact annotated. Nothing source-identifying was rendered — only task id, task-set id and completion time — but the delay material is supposed to be drawn from tasks the focal sources never touched, and the `delay_material_source_neutral_gold` flag asserts as much. The filter now excludes whole focal tasks. The builder tests carried the same blind spot: their fixture had every task annotated by both focal workers, so it could not have caught this.

### Backgrounds now carry the published task text

Scenarios previously read "A new annotation task in capability-50", with bare labels 0/1/2. The release documents the actual question for five of the six capabilities (50 expression-similarity filtering, 52 naturalness-of-expression judgment, 53 facial-similarity screening, 56 gesture-similarity filtering, 69 article-continuation classification); capability 126's question text is not published, and its background says so rather than inventing one. Label codes 0/1/2 are rendered in order as options A/B/C — a presentational relabelling recorded in `data/netease_capability_tasks.json`; all likelihood ratios are computed on the raw codes.

### Audit status

`data/audit_d0_candidates.py` re-derives every stored statistic from the raw release and checks it against the model-visible text. All ten checks pass on all 22 rows: global worker uniqueness, calibration/validation task disjointness, accuracy floor and ordering on both splits, both-direction LR ordering and margin on both splits, profile text matching the raw history, message text identical across sources, delay records drawn from unrelated tasks, delay material free of truths/answers/focal identities, reinstatement restoring source only, and complete provenance including the raw SHA256.

## Why D0 is not signed yet

A dataset card and a correct builder are not D0-PASS. The actual released NetEaseCrowd files must be materialized, hashed, passed through the builder, and produce at least 20 source-disjoint scenarios spanning at least two real capability domains. Then a fixed random sample of 20 generated rows must be manually checked for:

- worker histories and task-disjoint split;
- calibration/validation accuracy and both LR directions;
- global worker non-reuse;
- same message content across high/low source;
- delay rows containing only unrelated administrative metadata;
- reinstatement not repeating the message;
- license/provenance and prompt naturalness.

The concrete rows now exist and pass every mechanical check, and the first human audit is recorded above. What remains is the human read of the **re-drawn** 20-row sample for the 22-row bank, since dropping capability 126 changes which rows the fixed seed selects. The sample covers 20 of the 22 rows; the two outside it are `50:1v2:001` and `50:0v1:002`. Until that reading is recorded, `d0_verdict` stays `AUDITING` and `validation_authorized` remains `false`.
