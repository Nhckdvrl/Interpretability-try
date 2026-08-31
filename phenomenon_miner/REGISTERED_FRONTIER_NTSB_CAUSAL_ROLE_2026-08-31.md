# Registered Frontier — NTSB Causal Relevance ≠ Causal-Role Selection

Date: 2026-08-31

Status: **REGISTERED-FRONTIER / DELEGATED-G0 / NOT PASS-REGISTER / NO MI AUTHORIZED**

```yaml
PASS_REGISTER: false
counts_toward_target_five: false
stage: delegated_artifact_audit_then_G0
owner: local_agent
MI_authorized: false
```

## Natural question

> In a real accident, a model may recognize which findings are causally relevant, yet still fail to distinguish findings investigators treat as causes from those treated as contributing factors. Does causal relevance come apart from causal-role selection?

This wording intentionally avoids claiming that every accident has one unique “principal cause.” NTSB records may contain multiple findings marked `C` (cause) and multiple findings marked `F` (factor).

## Why this frontier is registered

The external scientific substrate is real and expert-grounded rather than researcher-invented:

- NTSB publishes structured aviation investigation data in Microsoft Access MDB form.
- The `findings` table historically contains `cause_factor` values `C` / `F`.
- Since Release 3.0 (2024-03-01), NTSB added `cm_inPC`, indicating whether a finding was cited in the probable-cause statement as **a cause or contributing factor**.
- NTSB explicitly states that old records were back-filled with `cm_inPC = TRUE` whenever legacy `cause_factor` was `C` or `F`.

Therefore:

- `cm_inPC` can support **relevance/inclusion** (`in probable-cause explanation` vs not);
- `cause_factor=C/F` can support the historical **role distinction** (`cause` vs `factor`);
- **`cm_inPC` alone must never be treated as C-vs-F gold.**

Official sources:

- dataset directory: https://data.ntsb.gov/avdata
- release notes: https://data.ntsb.gov/avdata/FileDirectory/DownloadFile?fileID=C%3A%5Cavdata%5CMDB_Release_Notes.pdf
- NTSB accident data page: https://www.ntsb.gov/safety/data/pages/Data_Stats.aspx

## Exact registration boundary

This is **not** registered as:

- `LLMs do actual causation`;
- generic `root cause analysis`;
- generic `cause vs non-cause` classification;
- extracting causes from accident reports;
- a benchmark built from NTSB labels;
- an MI study of a pre-assumed cause/factor circuit.

It is registered only as the possible **behavioral dissociation**:

```text
causal-relevance recognition remains strong
BUT
cause-vs-contributing-factor role selection is substantially weaker
```

on the same natural expert investigations and current open model families.

If that dissociation does not exist, this frontier dies at S0.

## Mandatory next file

The full local execution contract is:

`phenomenon_miner/NTSB_LOCAL_AGENT_HANDOFF_2026-08-31.md`

The local agent must follow that file before any mechanistic analysis.
