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

**No frozen JSONL is signed yet.** As of 2026-08-29 the NetEaseCrowd release is materialized and hashed, and [`data/d0_candidates_netease.jsonl`](data/d0_candidates_netease.jsonl) holds **28 candidate scenarios over 5 capabilities and 56 distinct annotators**, at most two per (capability, label pair) cell, with a required high/low report-LR separation of 2.0 in both directions on both splits. Capability 69 is excluded because its third response option is "undecided", a different kind of hypothesis from the other capabilities. [`data/audit_d0_candidates.py`](data/audit_d0_candidates.py) re-derives every statistic from the raw release; all ten checks pass on all 28 rows ([`data/D0_MANUAL_AUDIT.md`](data/D0_MANUAL_AUDIT.md)).

What is still missing is the human read of the fixed-seed 20-row sample in `data/D0_MANUAL_AUDIT_PROMPTS.txt`. Until that reading is recorded, this stays a candidate: do not rename it `frozen_d0.jsonl` and do not set `validation_authorized` true.
