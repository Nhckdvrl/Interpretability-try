# NTSB G0 — Causal Relevance ≠ Causal-Role Selection

Execution of [`../NTSB_LOCAL_AGENT_HANDOFF_2026-08-31.md`](../NTSB_LOCAL_AGENT_HANDOFF_2026-08-31.md).

**Status: delegated artifact audit + G0 behavioural gate. NOT `PASS-REGISTER`. MI forbidden.**

## Question

> In a real accident, can a model correctly recognize which findings are causally
> relevant while still failing to distinguish findings investigators classify as
> **causes** from findings they classify as **contributing factors**?

## Semantic rule

```text
cm_inPc      = cited in the probable-cause statement as a cause OR contributing
               factor  ->  RELEVANCE. Never C-vs-F gold.
Cause_Factor = legacy role label C (cause) vs F (contributing factor).
```

Multiple `C` findings per event are normal. This is not root-cause analysis.

## Layout

| path | content |
|---|---|
| `PREREGISTRATION.md` | frozen sample rules, prompts, panel, thresholds, kills |
| `scripts/extract.sh` | official download + mdbtools schema/export |
| `scripts/audit_population.py` | Phase C data-only population audit |
| `scripts/random20_audit.py` | Phase D fixed-seed random-20 semantic/leakage audit |
| `scripts/build_g0_items.py` | frozen sample + item construction |
| `scripts/run_g0.py` | deterministic vLLM panel runner |
| `scripts/analyze_g0.py` | event-bootstrap analysis, controls, verdict |
| `audit/` | tables, schema, population/mixed-role summaries, random-20 |
| `items/` | frozen items + sampling manifest |
| `results/` | per-family raw item-level outputs, summary.csv, g0_report.md |

`raw/avall.zip` (95,636,276 B) and `raw/avall.mdb` (530 MB) are **not** committed;
their SHA256 and provenance are recorded in `PREREGISTRATION.md`. Re-fetch with
`scripts/extract.sh`.
