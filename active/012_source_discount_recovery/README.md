# 012 — Source-Discount Recovery

Status: `N0-PASS / D0-AUDITING / ACTIVE-PREFLIGHT / HARNESS-READY-r1 / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #9**.

```yaml
formal_n0_verdict: PASS
n0_basis: 2026-08-28 adversarial N0 accepted by project resolution 2026-08-29
d0_verdict: AUDITING
validation_authorized: false
```

The historical duplicate N0 that killed this project as a sleeper-effect collision is superseded by [`N0_RESOLUTION_2026-08-29.md`](N0_RESOLUTION_2026-08-29.md). The sleeper effect/source-message dissociation is the natural human mother phenomenon; the LLM target is the stricter source-memory-intact, weighting-use dissociation with selective cue reinstatement.

## Data status

See [`D0_SOURCE_AUDIT.md`](D0_SOURCE_AUDIT.md). Two strong external source families were identified:

- **NetEaseCrowd**: real production crowdsourcing history, worker/task/truth/timestamp records, CC BY-SA 4.0;
- **CIFAR-10H**: raw annotator-level image decisions, CC BY-NC-SA 4.0.

The reproducible extractor [`data/build_natural_d0.py`](data/build_natural_d0.py) uses a task-ID-disjoint 60/40 split and report-specific worker likelihood ratios. Formal D0 requires, in both calibration and held-out tasks:

```text
1 < low_target_lr < high_target_lr
0 < high_other_lr < low_other_lr < 1
```

Workers must be above chance, the same message content must be paired across sources, target-task gold is never exposed, each selected worker is used at most once, and delay/reinstatement controls may not leak the message.

**No frozen JSONL is signed yet.** As of 2026-08-29 the NetEaseCrowd release is materialized and hashed, and [`data/d0_candidates_netease.jsonl`](data/d0_candidates_netease.jsonl) holds **108 candidate scenarios over 4 capabilities and 216 distinct annotators**, with a required high/low report-LR separation of 2.0 in both directions on both splits. Capability 69 is excluded because its third response option is "undecided", and capability 126 because the release does not publish its question text; every remaining capability carries a published question. [`data/audit_d0_candidates.py`](data/audit_d0_candidates.py) re-derives every statistic from the raw release; all ten checks pass on all 108 rows ([`data/D0_MANUAL_AUDIT.md`](data/D0_MANUAL_AUDIT.md)).

Pairs are chosen by a global matching rather than a scan: contract-valid pairs are enumerated per cell, then selected with a maximum matching inside each cell and scarcest-cell-first across cells, so annotators are never spent where alternatives existed. The bank is not balanced across capabilities and cannot be — capability 52 holds only 28 annotators in the whole release and 53 has few that clear the 2.0 separation — so 45/4/14/45 is the ceiling shape at this target. The first human audit, on the earlier 28-row bank, returned 18/20 PASS with 2 holds on capability 126's naturalness; that is what removed 126. What is still missing is the human read of the re-drawn 20-row sample in `data/D0_MANUAL_AUDIT_PROMPTS.txt`. Until that reading is recorded, this stays a candidate: do not rename it `frozen_d0.jsonl` and do not set `validation_authorized` true.

## Statistical contract (frozen `2026-08-29-r2`, before any model call)

108 source pairs are not 108 independent natural tasks. They sit inside 12 `(capability, binary label pair)` cells, and four of those cells hold between one and three scenarios each. Averaging over pairs would let capability 50 and 56's fifteen-scenario cells outvote everything else; weighting all twelve cells equally would hand a third of the headline to seven scenarios. The contract therefore splits the bank:

- **Primary inferential set** — the 8 cells the frozen bank sized at `min_primary_cell_size >= 5`: **101 scenarios across capabilities 50, 53 and 56**. The headline effect is the mean of the eligible cells' scenario means, every eligible cell weighted equally. The interval comes from a bootstrap that resamples eligible cells and then scenarios within each resampled cell.
- **Secondary set** — the 4 undersized cells (`52:0v1`, `52:0v2`, `52:1v2`, `53:0v2`), **7 scenarios**. They are executed and reported and they cannot move `PASS` / `HOLD` / `KILL`.

Capability is not a third bootstrap level. The primary set's three capabilities contribute three, two and three eligible cells; resampling capabilities first would give capability 53 the same third of the weight as the two that carry more cells, replacing one arbitrary weighting with another. Per-capability cell means are reported as `capability_cell_means` for heterogeneity, and gate nothing.

Membership is fixed by the frozen bank, never by the results: `min_primary_cell_size` is `5` in `configs/frozen_g0.json` and an undersized cell can never be promoted into the primary set after the model has run. Strong-pair fractions are reported twice — `strong_pair_fraction` over the whole executed bank, and `primary_strong_pair_fraction` over the inferential set, which is the one the promotion threshold reads. Capability floors (`support` / `memory` / `weighting`) are still read over all 108, since whether the model can do the task at all is not a question about stratification.
