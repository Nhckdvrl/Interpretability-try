# 012 — Source-Discount Recovery

Status: `ARCHIVED / TERMINAL-KILLED / HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #9**.

```yaml
formal_n0_verdict: PASS
d0_verdict: PASS
d0_items: 108
d0_primary_items: 101
d0_primary_cells: 8
d0_secondary_items: 7
d0_capabilities: 4
unique_annotators: 216
manual_audit: 20/20 PASS
r2_disposition: HOLD-INSTRUMENTATION-ARTIFACT
r3_disposition: TERMINAL-KILLED
behavioral_verdict: HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR
qwen_counterfactual_weighting_capable_pairs: 0/108
gemma_counterfactual_weighting_capable_pairs: 0/108
validation_authorized: false
```

See [`FINAL_VERDICT.md`](FINAL_VERDICT.md) for the terminal decision. All D0 material, harness code, raw audit records, and r2/r3 smoke records are retained in this archive.

## Why the project ended

The natural D0 itself passed: 108 NetEaseCrowd source pairs over four capabilities and 216 distinct annotators, with task-disjoint calibration/validation, a 2.0 high/low report-LR separation in both directions, 20/20 manual audit, and the pre-model 101-primary / 7-secondary cell-stratified analysis contract.

The r2 two-family first shot was not treated as a scientific kill because its `source_credibility` yes/no capability probe had an always-Yes gold and a decisive answer-position artifact. It is retained as `HOLD-INSTRUMENTATION-ARTIFACT`.

r3 changed exactly that instrumentation item to a counterbalanced two-content-option credibility probe and fully reran Qwen3-8B and Gemma-3-12B-IT. The summarizer still stopped at the memory gate, but the decisive terminal audit is independent of that probe: granting the memory gate outright while retaining the frozen support gate, immediate-influence floors and initial-gap thresholds leaves **0/108 weighting-capable source pairs in Qwen and 0/108 in Gemma**, against a frozen minimum of 20. The dominant blocker is `belief_initial_gap`; the untouched immediate readouts reproduced r2 bit-identically.

Therefore no further credibility-probe revision, belief readout replacement, threshold relaxation, model substitution, N1, generality panel, or mechanism work is allowed for this operationalization. The observed action-vs-belief weighting difference is preserved only as a failure-bank observation, not promoted into a replacement claim.

## Preserved records

- [`D0_SOURCE_AUDIT.md`](D0_SOURCE_AUDIT.md) — external source and D0 derivation audit.
- [`data/D0_MANUAL_AUDIT.md`](data/D0_MANUAL_AUDIT.md) — frozen-bank automated/manual audit record.
- [`results/smoke_r2/SMOKE_VERDICT.md`](results/smoke_r2/SMOKE_VERDICT.md) — instrumentation hold.
- [`results/smoke_r3/SMOKE_VERDICT.md`](results/smoke_r3/SMOKE_VERDICT.md) — full rerun and decisive counterfactual denominator audit.
- [`N0_RESOLUTION_2026-08-29.md`](N0_RESOLUTION_2026-08-29.md) — accepted novelty resolution.

D0 remains `PASS`; the project died at the behavioral capability denominator, not at data validity.