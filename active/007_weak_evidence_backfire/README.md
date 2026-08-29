# 007 — Weak-Evidence Backfire

Status: `N0-PASS / D0-PASS / READY-TO-SMOKE / HARNESS-READY-r5-natural-d0`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #10**.

```yaml
formal_n0_verdict: PASS
n0_basis: 2026-08-28 adversarial N0 accepted by project resolution 2026-08-29
d0_verdict: PASS
d0_items: 30
manual_audit: 20/20 PASS
frozen_data_sha256: d3ef047882a49b05993f3c00c222e9d922faface3339c4161016594016c4877a
validation_authorized: true
```

The historical 2026-08-29 duplicate N0 that killed this project because the human weak-evidence effect is known is retained for provenance but superseded by [`N0_RESOLUTION_2026-08-29.md`](N0_RESOLUTION_2026-08-29.md). In this project, a human/natural mother phenomenon is an anchor; collision means the same LLM phenotype/decisive contrast is already established.

## Target contradiction

```text
model recognizes E as genuine positive evidence for H
strong evidence is used in the correct direction
but adding weak E makes model preference for H fall below the matched no-evidence baseline
```

A valid case must survive both evidence directions, belief and consequential-action readouts, neutral control, pragmatic-completeness, length control, and scenario-level paired statistics.

## Frozen D0

See [`D0_AUDIT.md`](D0_AUDIT.md).

- 30 natural scenarios: 20 Breast Cancer Wisconsin Diagnostic + 10 Wine;
- external CC BY 4.0 sources with frozen DOI/provenance;
- fixed class-wise 60/40 calibration/validation split, seed `20260829`;
- exact model-visible thresholds reproduce source counts and Jeffreys-smoothed LR byte-for-byte;
- weak/strong ordering and a 20% diagnosticity margin survive held-out rows;
- real near-neutral controls are stable in both splits;
- fixed 20-row manual audit: 20/20 PASS.

The r5 audit also removes an answer leak in the old `strong_gt_weak` capability probe: model-visible alternatives are now `OBSERVATION 1/2`, not `WEAK/STRONG-CANDIDATE`.

## Historical smoke lineage

`results/smoke_r5/` is a valid historical run, but it belongs to an **older 25-case D0** (SHA `b1f6f889...`, execution commit `0ef5ee6...`). That run produced a two-family capability-floor hard kill.

Commit `3cbe5e2` later made a material D0 change: provenance, held-out LR verification and the deterministic builder were tightened, yielding the current **30-case D0** with SHA `d3ef0478...`. Therefore the old smoke verdict must not be inherited by the current contract. Any new smoke must use a new result directory and record the current D0 SHA, execution commit and model revisions.

## Execution

The runner is authorized only for this frozen D0/config. Do not tune cases, thresholds, prompts or gates after reading model output.

```bash
cd active/007_weak_evidence_backfire
python -m pip install -e '.[dev,run]'
python data/build_frozen_d0.py --out data/frozen_d0.jsonl
python data/verify_frozen_d0.py data/frozen_d0.jsonl
pytest -q
weak-evidence-run validate-data --data data/frozen_d0.jsonl
```

Then run the two-family smoke. A positive smoke still requires raw-case/scorer/capability/artifact audit and N1 before expansion or mechanism work.
