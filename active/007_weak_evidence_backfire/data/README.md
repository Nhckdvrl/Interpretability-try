# Frozen natural D0

`materialize_frozen_d0.py` contains the compressed exact bytes of the signed D0 and reconstructs `frozen_d0.jsonl` after verifying its SHA-256. See `../D0_AUDIT.md`.

Sources:

- UCI Breast Cancer Wisconsin (Diagnostic), DOI `10.24432/C5DW2B`, CC BY 4.0;
- UCI Wine, DOI `10.24432/C5PC7J`, CC BY 4.0.

The file contains 25 scenarios derived with a fixed stratified 60/40 calibration/validation split and seed `20260829`. Model-visible calibration frequencies come only from the 60% partition; all evidence-direction, weak/strong-ordering, and near-neutral controls must independently survive the held-out 40% partition.

Exact source-array SHA-256 hashes and held-out LR/count metadata are stored inside each record. Frozen file SHA-256:

`b1f6f88983b68e2764ff99964debd71a307dc0209c2cb9d2bb8f6d7484fd9792`
