# Frozen natural D0

The authoritative D0 is a **deterministic 30-scenario byte specification**, not a hand-authored JSONL checked into Git. Materialize it locally as `frozen_d0.jsonl` immediately before the first smoke.

Sources:

- UCI Breast Cancer Wisconsin (Diagnostic), DOI `10.24432/C5DW2B`, CC BY 4.0;
- UCI Wine, DOI `10.24432/C5PC7J`, CC BY 4.0, restricted to cultivar 1 vs 2.

Frozen SHA-256:

```text
d3ef047882a49b05993f3c00c222e9d922faface3339c4161016594016c4877a
```

`build_frozen_d0.py` rebuilds the exact JSONL from the sklearn-packaged UCI arrays using the frozen source-array hashes, seed, split, threshold-selection and LR contract. `verify_frozen_d0.py` independently rebuilds all 30 rows and requires the materialized bytes to match the frozen SHA exactly. This is preferable to vendoring a derived copy that could silently drift away from the source-generation logic.

Before any smoke run:

```bash
python data/build_frozen_d0.py --out data/frozen_d0.jsonl
python data/verify_frozen_d0.py data/frozen_d0.jsonl
weak-evidence-run validate-data --data data/frozen_d0.jsonl
```

If the sklearn/UCI source-array hash, the generated SHA, or any loader contract differs, stop. Do not change thresholds or replace failed rows after seeing model output.
