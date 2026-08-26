# 006 mechanism workspace

This directory contains the exploratory Qwen2.5-14B mechanism preflight and the frozen design for the next confirmatory round.

## Read first

- [`MECHANISM_LOG.md`](MECHANISM_LOG.md) — organized current results and interpretation limits.
- [`../INTERPRETABILITY_PLAN_V2.md`](../INTERPRETABILITY_PLAN_V2.md) — next study plan; no V2 experiment has been run.
- [`CLAIM_EVIDENCE_LEDGER.md`](CLAIM_EVIDENCE_LEDGER.md) — claim status and exact evidence mapping.

## Canonical committed outputs

The `results/` directory commits compact summaries and the primary raw JSONL needed to regenerate them. Large BF16 `.pt` activation caches, smoke runs, superseded FP16 outputs, and redundant shards remain local and ignored.

The primary compact summaries are:

- `qwen25_14b_phase0_summary.json`;
- `qwen25_14b_probe_timeline_summary.json`;
- `qwen25_14b_probe_belief_span_joint_summary.json`;
- `qwen25_14b_phase2_span_summary.json`.

## Reproduction boundary

The existing files are `D0 / exploratory`; they may motivate layer windows and hypotheses but are not final confirmatory evidence. V2 requires new family-level dev/test splits and manifests before another white-box run.

Current tests:

```bash
cd archive/006_bayesian_latent_inference_use_gap
/home/xiang/miniconda3/envs/pvlm/bin/python -m pytest -q
```

The runner scores full candidate continuations and the interchange code uses batch-local, identical-shape baseline/counterfactual forwards to avoid BF16 batch-shape drift.
