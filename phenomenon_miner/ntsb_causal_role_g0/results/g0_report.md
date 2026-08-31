# G0 Report — NTSB Causal Relevance ≠ Causal-Role Selection

Date: 2026-08-31
Contract: [`../../NTSB_LOCAL_AGENT_HANDOFF_2026-08-31.md`](../../NTSB_LOCAL_AGENT_HANDOFF_2026-08-31.md)
Frozen design: [`../PREREGISTRATION.md`](../PREREGISTRATION.md) + [`../PREREGISTRATION_ADDENDUM_1.md`](../PREREGISTRATION_ADDENDUM_1.md)

**Outcome: `KILL-S0 / RELEVANCE-ALSO-FAILS`.** No MI was run and none is authorized.

---

## 1. Question tested

> In a real accident, can a model correctly recognize which findings are causally
> relevant while still failing to distinguish findings investigators classify as
> **causes** from findings they classify as **contributing factors**?

`C` is not a unique "principal cause": NTSB determines one or more probable
causes, multiple `C` findings per event are normal, and the object is
`cause vs contributing factor`, never root-cause analysis.

## 2. Data gate — PASSED

Official `avall.zip` (95,636,276 B, sha256 `0cf30a61…`, matching the official
directory listing), parsed with `mdbtools 1.0.1`.

- 72,381 findings across 24,262 events with findings.
- Crosstab confirms the handoff's semantic rule and refutes the tempting shortcut:
  `C→cm_inPc=T` (37,764/37,764), `F→cm_inPc=T` (5,758/5,758), **and 17,519 rows
  carry `cm_inPc=T` with a blank `Cause_Factor`.** `cm_inPc=TRUE` is therefore
  demonstrably not C-gold.
- **3,506 mixed-role events**, 13,092 C/F rows, 2008–2020, largest single year
  21.2%, ACC 3,366 / INC 140. Minimum viability gate (>=500 events, >=1000 rows,
  spread) **PASS**.
- Corpus-wide C:F is 87:13, but **inside mixed-role events it is 56:44** — the
  mixed-role restriction is what makes the role task well-posed.

Random-20 semantic audit (seed 20260831) answered all seven handoff questions
affirmatively; C/F labels are semantically real, with `narr_cause` consistently
mirroring `C` findings in the main clause and `F` findings after "Contributing to
the accident was/were…". The audit also found the dataset's largest leak: NTSB
appends the role letter to `finding_description` on 42,045 of 43,522 C/F rows.
Stripped before any model input.

Frozen sample: 600 year-stratified events, 2,390 relevance items (2,149 YES /
241 NO), 2,149 role items (1,204 C / 945 F).

## 3. Panel

| family | model | status |
|---|---|---|
| Qwen | `Qwen/Qwen3-8B` | complete |
| Gemma | `google/gemma-3-12b-it` | complete |
| Llama | `NousResearch/Meta-Llama-3.1-8B-Instruct` | complete |
| Phi | `microsoft/Phi-4-mini-instruct` | complete (documented substitute) |
| Mistral | `mistralai/Mistral-Small-24B-Instruct-2501` | **infrastructure hang, 0 items scored** — [`mistral_infrastructure_failure.md`](mistral_infrastructure_failure.md) |

Deterministic decoding (`temperature=0`, `max_tokens=8`), exact revisions and
framework versions in each `results/<family>/manifest.json`.

## 4. Headline result

Balanced accuracy; 95% CIs are **event-grouped** bootstrap (10,000 resamples,
clustered on `ev_id` — findings within one accident are not independent).

| family | Task A relevance | Task B role | gap | gap 95% CI |
|---|---|---|---|---|
| Qwen | 0.562 [0.535, 0.590] | 0.544 [0.525, 0.563] | 0.018 | [−0.015, 0.051] |
| Gemma | 0.537 [0.515, 0.561] | 0.546 [0.534, 0.559] | −0.010 | [−0.035, 0.016] |
| Llama | 0.635 [0.596, 0.671] | 0.503 [0.499, 0.507] | 0.131 | [0.093, 0.168] |
| Phi | 0.539 [0.505, 0.573] | 0.533 [0.520, 0.547] | 0.006 | [−0.030, 0.041] |

Preregistered criterion (>=2 of 4 families with A>=0.75 **and** B<=0.62 **and**
gap>=0.15): **0 of 4 families qualify.**

**The failure is on the relevance axis, not the role axis.** Task-A balanced
accuracy is 0.54–0.64 in every family, far below the 0.75 the design required.
The premise of the whole frontier — that relevance recognition is strong — is
false on these models and this substrate.

## 5. Why Task A failed

Qwen and Gemma answer YES to almost everything (YES recall 0.93/0.94, NO recall
0.19/0.13). Llama is more balanced (0.68/0.59) but still only 0.635.

The honest diagnosis is a **construct-validity limit of the substrate**: the
Task-A negatives are findings the investigation *did* record but did not cite in
the probable-cause statement. They are not irrelevant to the accident — they are
genuine findings about it. NTSB provides no natural "irrelevant finding"
population, so "was this finding causally relevant?" does not have a clean gold.
The negative class is also thin: 241 items across 177 of 600 events, exactly as
flagged before the run.

This diagnosis is recorded as a limitation. It is **not** used to rescue the
topic, relax a threshold, or redefine the population.

## 6. Task B is at chance in all four families

| family | B BA | pred CAUSE / CONTRIBUTING_FACTOR | CAUSE recall | CF recall |
|---|---|---|---|---|
| Qwen | 0.544 | 602 / 1547 | 0.319 | 0.769 |
| Gemma | 0.546 | 228 / 1921 | 0.147 | 0.946 |
| Llama | 0.503 | 20 / 2125 | 0.013 | 0.994 |
| Phi | 0.533 | 262 / 1861 | 0.156 | 0.910 |

Gold is 56% CAUSE; every family predicts CONTRIBUTING_FACTOR 72–99% of the time.
Llama is effectively degenerate. Under the fixed paraphrase, role BA is
0.510 / 0.602 / 0.499 / 0.500 — unchanged.

So there is no "relevance strong, role weak" dissociation. There is
"relevance weak, role at chance".

## 7. Controls

1. **Label prior** — majority class 0.560 accuracy, 0.500 balanced; stratified
   random 0.500.
2. **Finding-text-only** — Qwen 0.618, Gemma 0.551, Llama 0.500, Phi 0.608.
   Notably this is *higher* than full context for Qwen (+0.074) and Phi (+0.075):
   adding the accident narrative makes role selection **worse**. The preregistered
   `KILL-ARTIFACT / LEXICAL-LABEL-PREDICTION` trigger (finding-only >= full − 0.02
   **and** >= 0.62) does not fire, but only just.
3. **Narrative-only** — 0.498 / 0.499 / 0.027 / 0.501. No prompt artifact; Llama's
   0.027 reflects its near-constant CONTRIBUTING_FACTOR output.
4. **Code removal** — codes were never in any prompt. Dropping the
   "Contributed to outcome" modifier items changes role BA by <=0.003 in every family.
5. **Probable-cause leakage** — eligibility rule E4 excluded 152 units whose
   factual narrative contained accident-role wording; "cause of death" was
   correctly not treated as a match.
6. **Year/deprecation** — reported per year in `analysis.json`; no year carries
   the (absent) effect.

## 8. Metadata stupid-baselines (Addendum 1)

Semantics-free features predict C/F better than any model did:

| block | grouped-CV BA |
|---|---:|
| majority class | 0.500 |
| META (position, year, lengths, missingness) | **0.697** |
| META + finding-text length statistics | **0.797** |
| taxonomy codes (never shown to models) | 0.751 |
| **best model, Task B** | **0.546** |

`finding_no` alone reaches 0.693 because NTSB coders list cause findings first
(P(CAUSE) falls 0.83 → 0.24 across positions). That ordering is **outside** the
models' evidence envelope — each prompt shows one isolated finding — so part of
the C/F gold is coder bookkeeping no model could recover from what it is given.
Models did not recover it from semantics either: predicted P(CAUSE) by position
is flat and far below gold in every family.

`len(finding_text)` alone reaches 0.668 and **is** inside the envelope, yet role
BA is flat across length terciles (e.g. Qwen 0.496/0.581/0.561), so the models
are not riding the length cue — they are simply not doing the task.

Evidence-envelope assertion: Task A and Task B render exactly `{narrative}` and
`{finding}` for all 2,149 shared items. `PASS`.

## 9. Verdict

Preregistered hard kill, handoff §16:

> `KILL-S0 / RELEVANCE-ALSO-FAILS` — models that fail C/F selection are also bad
> at causal relevance. Then there is no relevance→selection dissociation.

Task-A BA < 0.75 in **4 of 4** families (trigger required >=3 of 4).

No subset rescue, no threshold change, no prompt re-tuning, no model swap, and no
MI. Per handoff §16, none of those are permitted to revive this result.

```text
KILL-S0 / RELEVANCE-ALSO-FAILS
```

`PASS_REGISTER` remains **0**.
