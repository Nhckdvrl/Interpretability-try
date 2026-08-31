# Copy-Paste Prompt — Local NTSB Validation Agent

Use this prompt verbatim with a local coding/research agent that has shell access and normal Internet access.

---

Continue the mechanistic-interpretability topic search in repository `Nhckdvrl/Interpretability-try`, but **do not search for new topics and do not do mechanistic interpretability in this task**.

Your only job is to execute the NTSB behavioral/data gate for the registered frontier:

> **causal relevance ≠ causal-role selection (cause vs contributing factor)**

First, read these files completely:

1. `phenomenon_miner/NTSB_LOCAL_AGENT_HANDOFF_2026-08-31.md` — authoritative execution contract
2. `phenomenon_miner/REGISTERED_FRONTIER_NTSB_CAUSAL_ROLE_2026-08-31.md`
3. `phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`
4. `rejected_candidates/continuation_terminal_addendum_9_2026-08-31.md`
5. `phenomenon_miner/NATURAL_QUESTION_GATE.md`
6. `phenomenon_miner/SCIENTIFIC_SUBSTRATE_GATE.md`
7. `phenomenon_miner/S0_FUNNEL_2026-08-31.md`

Then execute `NTSB_LOCAL_AGENT_HANDOFF_2026-08-31.md` exactly, end to end.

Critical semantic rule:

```text
cm_inPC = the finding was cited in the probable-cause statement as a cause OR contributing factor
legacy cause_factor = C vs F role label
```

**Never use `cm_inPC=TRUE` as principal-cause gold. Never assume one unique cause per event.** The role task is `CAUSE` vs `CONTRIBUTING_FACTOR` using legacy `cause_factor`, not “find the one true root cause.”

Required order:

1. Download the official NTSB `avall.zip` from `data.ntsb.gov`, record URL/timestamp/size/SHA256, and extract the MDB.
2. Use MDB tools to inspect the actual schema before assuming table/column names.
3. Export/parse `findings`, `events`, `narratives`, and any required lookup tables.
4. Produce a data-only population audit: total findings, `cause_factor` values/missingness, `cm_inPC` values/missingness, cross-tab, years, findings/event, C/F availability by year.
5. Count mixed-role events with `n_C>=1 AND n_F>=1` and report breadth across years/categories.
6. Enforce the preregistered minimum viability gate from the handoff. If it fails, write a terminal rejection with `KILL-DATA / INSUFFICIENT-NATURAL-MIXED-ROLE-POPULATION` and stop.
7. Make the fixed-seed random-20 mixed-role semantic/leakage audit. If labels are noisy, narratives leak conclusions, or the task is incoherent, write `KILL-DATA` and stop.
8. Freeze sample construction and prompts before looking at full model results.
9. Run the linked behavioral tasks on at least 3 genuinely different current interpretable open model families:
   - Task A: causal relevance (`C/F` vs non-C/F finding);
   - Task B: cause vs contributing factor (`C` vs `F`) among relevant findings.
10. Use deterministic decoding and save raw item-level outputs, parse failures, exact model IDs/revisions, tokenizer revisions, framework versions, prompts, and sampling manifest.
11. Apply the preregistered S0 promotion criterion from the handoff. Do not relax thresholds after seeing results and do not subset-rescue.
12. If the dissociation fails, write a rejection immediately with the appropriate `KILL-S0` reason.
13. If the dissociation survives, do **not** start MI. Instead write a concise G0 report with the exact behavioral evidence and blockers for N0/N1.

Repository-writing requirements:

- Create/use `phenomenon_miner/ntsb_causal_role_g0/` exactly as specified by the handoff.
- Commit scripts, manifests, small audits, reports and item-level results that are reasonable for Git.
- Do not commit the ~95MB official ZIP/MDB unless repository policy explicitly allows it.
- Every kill must also be recorded in `rejected_candidates/` with Natural question, Why it looked good, Kill evidence, Death code, Nearest-neighbor warning, Resurrection condition.
- Push all final code/report changes to `main`.

At the end, report exactly one of these outcomes:

```text
KILL-DATA: <reason>
```

or

```text
KILL-S0: <reason>
```

or

```text
G0-SURVIVES / NOT PASS-REGISTER / NO MI YET
```

Do not call it PASS-REGISTER in this task.
