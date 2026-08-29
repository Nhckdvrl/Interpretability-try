# D0 materialization — Source-Discount Recovery

`frozen_d0.jsonl` is signed. The source is NetEaseCrowd (CC BY-SA 4.0); the builder expects the released CSV schema and performs task-ID-disjoint calibration/validation before selecting any worker pair.

## Files

| file | role |
|---|---|
| `raw/NetEaseCrowd_part_{1..15}.csv` | the release as downloaded (untracked; ~305 MB) |
| `raw/netease_normalized.csv` | the 15 parts concatenated, single header, no other transformation |
| `RAW_MANIFEST.md` | download provenance, licence and SHA256 of every raw file |
| `netease_capability_tasks.json` | the published per-capability task text, used to write natural backgrounds |
| `build_natural_d0.py` | the candidate builder |
| `audit_d0_candidates.py` | independent re-derivation audit + fixed-seed manual sample |
| `frozen_d0.jsonl` | the signed bank — 108 scenarios, sha256 `cde7f3fa9dfeb94645fa2e254507013c26cb2ffb01793b9bd889a86668af1c3a` |
| `D0_MANUAL_AUDIT.md`, `D0_MANUAL_AUDIT_PROMPTS.txt` | audit record and the prompts a human must read |

## Rebuild

```bash
python data/build_natural_d0.py \
  --csv data/raw/netease_normalized.csv \
  --dataset-name NetEaseCrowd \
  --license 'CC BY-SA 4.0' \
  --source-url 'https://github.com/fuxiAIlab/NetEaseCrowd-Dataset' \
  --domain-descriptions data/netease_capability_tasks.json \
  --domain-col capability \
  --task-col taskId \
  --taskset-col tasksetId \
  --worker-col workerId \
  --truth-col truth \
  --answer-col answer \
  --time-col completeTime \
  --min-per-class 20 \
  --pairs-per-cell 9 \
  --target-scenarios 108 \
  --lr-margin 2.0 \
  --exclude-domain 69 \
  --exclude-domain 126 \
  --seed 20260829 \
  --out data/frozen_d0.jsonl
```

`--pairs-per-cell` is the balanced quota every (capability, binary label pair) cell is offered, served scarcest cell first; `--target-scenarios` then tops up least-loaded cell first when supply is uneven. Selection is a maximum matching inside each cell, not a scan of the ranked list. One pair per cell caps the whole bank at 18 for NetEaseCrowd, below the frozen `>=20`; see `../D0_SOURCE_AUDIT.md` for why that ceiling is structural rather than a data-density limit. `--exclude-domain` drops a capability before selection, not after, so its annotators return to the pool for the remaining domains; capability 69 is excluded because its third option is "undecided", and capability 126 because the release does not publish its question text.

## Re-audit

```bash
python data/audit_d0_candidates.py \
  --candidates data/frozen_d0.jsonl \
  --csv data/raw/netease_normalized.csv \
  --manifest data/RAW_MANIFEST.md \
  --out data/D0_MANUAL_AUDIT.md \
  --prompts-out data/D0_MANUAL_AUDIT_PROMPTS.txt
```

`frozen_d0.jsonl` was signed on 2026-08-29 after a 20/20 human read of the stratified fixed-seed sample. The rebuild command above reproduces it byte for byte; it is kept for provenance, not because the bank is still open. Rebuilding with different flags produces a different bank and would invalidate the sign-off.
