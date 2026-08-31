# V0 provenance audit

## Pinned public artifacts

- `Oxford-HAI-Lab/PyETR`: `bad96bc39cae746485acc095b1528366a6ec3a07`
- `Oxford-HAI-Lab/etr_case_generator`: `f6477b645df72b09b07fa81120bad24529f9a0ad`

## Blocking version discrepancy

The ICLR 2026 paper states that 400 items were initially generated and 17 were removed by pre-analysis integrity checks, leaving the reported 383-item population. The public generator history contains the 400-item `largeset` and its premise-reversed counterpart, but does not expose a stable 383-item ID manifest.

There are two additional provenance hazards:

- commit `c177357` explicitly marks the earlier datasets invalid after a `view_to_smt` bug was discovered;
- current HEAD contains a later 372-item `250524` set, which is not the paper's reported 383-item population.

Therefore V0 must not silently substitute either the 400-item pre-curation set or the later 372-item set. The next admissible step is to recover the exact 17 excluded IDs from a final-paper artifact or reproduce the integrity filter against the pinned historical generator/PyETR versions. Hidden-state work remains paused until that manifest is exact.
