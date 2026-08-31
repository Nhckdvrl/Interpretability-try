# Registered Frontier — NTSB Causal Relevance ≠ Causal-Role Selection

Date: 2026-08-31

Status: **TERMINAL — `KILL-S0 / RELEVANCE-ALSO-FAILS` (2026-08-31)**

> **This frontier is closed.** The delegated G0 was executed end to end. The data
> gate passed (3,506 natural mixed-role events) but the behavioural gate failed:
> Task-A causal-relevance balanced accuracy was 0.537–0.635 across four open
> families, far below the preregistered 0.75, while Task-B role selection sat at
> chance through degenerate class collapse. 0 of 4 families met the criterion.
>
> Terminal record: [`../rejected_candidates/ntsb_causal_relevance_vs_causal_role_selection_2026-08-31.md`](../rejected_candidates/ntsb_causal_relevance_vs_causal_role_selection_2026-08-31.md)
> Evidence: [`ntsb_causal_role_g0/results/g0_report.md`](ntsb_causal_role_g0/results/g0_report.md)
>
> Everything below is preserved as the original registration text. Do not treat
> it as a live frontier.

```yaml
PASS_REGISTER: false
counts_toward_target_five: false
stage: TERMINAL
death_code: KILL-S0 / RELEVANCE-ALSO-FAILS
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
