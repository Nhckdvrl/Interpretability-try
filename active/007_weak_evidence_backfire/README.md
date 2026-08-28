# 007 — Weak-Evidence Backfire

Status: `N0-PASS / D0-PASS / READY-TO-SMOKE / HARNESS-READY-r5-natural-d0`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #10**.

```yaml
formal_n0_verdict: PASS
n0_basis: 2026-08-28 adversarial N0 accepted by project resolution 2026-08-29
d0_verdict: PASS
d0_items: 25
manual_audit: 20/20 PASS
validation_authorized: true
```

The historical 2026-08-29 duplicate independent audit that marked this project `KILLED-COLLISION` is retained for provenance but is superseded by [`N0_RESOLUTION_2026-08-29.md`](N0_RESOLUTION_2026-08-29.md). A known human weak-evidence effect is the natural mother phenomenon, not by itself an LLM collision.

## Mother question

Can a model correctly recognize a cue as genuine positive evidence for a hypothesis, yet integrate it with the wrong sign in downstream belief and action?

```text
E supports H
but P_model(H | E) < P_model(H | same background, no E)
```

A valid case must pass support/likelihood gates, ordinary strong-evidence use, neutral non-diagnosticity, pragmatic-completeness, matched-length controls, both evidence directions, and both belief/action readouts. The two directions of one natural scenario are one statistical unit.

## Frozen natural D0

See [`D0_AUDIT.md`](D0_AUDIT.md). The exact signed JSONL is deterministically materialized by `data/materialize_frozen_d0.py` and checksum-verified before use.

- 25 natural feature-level scenarios;
- 15 from UCI Breast Cancer Wisconsin (Diagnostic), DOI `10.24432/C5DW2B`;
- 10 from UCI Wine, DOI `10.24432/C5PC7J`;
- both source datasets are CC BY 4.0;
- fixed stratified 60/40 calibration/held-out split, seed `20260829`;
- thresholds selected only on calibration rows;
- weak/strong direction and ordering must reproduce on held-out rows;
- fixed random manual audit: 20/20 PASS.

The r5 data contract fixes one important r4 problem: real finite data are not required to produce an empirical `neutral_lr` exactly equal to 1. A neutral cue must instead be a real cue from the same source data with LR in `[0.90, 1.10]` on both calibration and held-out partitions. The frozen data are substantially tighter than this bound.

## Execution

The runner is now authorized for the frozen smoke. Do not change thresholds, controls, prompts, D0 rows, or promotion criteria after seeing model output.

```bash
cd active/007_weak_evidence_backfire
python -m pip install -e '.[dev,run]'
pytest -q
python data/materialize_frozen_d0.py
weak-evidence-run validate-data --data data/frozen_d0.jsonl
# then run the frozen 30–50-case/two-family smoke using the existing CLI/config
```

A smoke result still requires raw-case audit and N1 before any generality or mechanism claim.
