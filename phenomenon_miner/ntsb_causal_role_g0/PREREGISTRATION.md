# G0 Preregistration — NTSB Causal Relevance ≠ Causal-Role Selection

Frozen: 2026-08-31, **before any model was loaded or any model output was inspected.**

Execution contract: [`../NTSB_LOCAL_AGENT_HANDOFF_2026-08-31.md`](../NTSB_LOCAL_AGENT_HANDOFF_2026-08-31.md).
Everything below is fixed. No threshold may be relaxed after results. No subset rescue.

---

## 0. Semantic rule (handoff §2)

```text
cm_inPc      = finding was cited in the probable-cause statement as a cause OR a
               contributing factor  ->  RELEVANCE. Never C-vs-F gold.
Cause_Factor = legacy role label, C (cause) vs F (contributing factor).
```

Multiple `C` findings per event are normal and expected. The task is never
"find the one true root cause".

## 1. Artifact

| item | value |
|---|---|
| source | `https://data.ntsb.gov/avdata/FileDirectory/DownloadFile?fileID=C%3A%5Cavdata%5Cavall.zip` |
| downloaded (UTC) | see `raw/download_timestamp_utc.txt` |
| bytes | 95,636,276 (matches official directory listing) |
| SHA256 | `0cf30a610d18eb109035b83106c227b248f27c6cff794ce622548f44c455238a` |
| extracted | `avall.mdb`, 555,745,280 bytes, mtime 2026-08-01 06:52 |
| reader | `mdbtools v1.0.1` (conda-forge, `.conda-mdbtools/`) |
| tables | `Findings`, `events`, `narratives` (see `audit/tables.txt`, `audit/schema.sql`) |

Neither `avall.zip` nor `avall.mdb` is committed (repo `.gitignore` policy + size).

## 2. Statistical unit

The accident **event** (`ev_id`). Findings and narratives are attached per
`(ev_id, Aircraft_Key)`; a finding is always paired with **its own aircraft's**
factual narrative. All CIs are event-grouped bootstrap (10,000 resamples, seed 20260831).

## 3. Eligibility (measurement validity only — frozen)

An `(ev_id, Aircraft_Key)` unit is eligible iff:

- **E1** it has >= 1 finding with `Cause_Factor == 'C'` **and** >= 1 with `Cause_Factor == 'F'`;
- **E2** every C/F finding has a non-empty `finding_description` after role-suffix stripping;
- **E3** its `narratives.narr_accp` (NTSB *Factual narrative*) is non-empty and >= 60 words;
- **E4** that narrative contains **no** accident-role wording
  (`probable cause`, `contributing factor(s)`, `contributed to`, `contributing to`,
  `causal factor`, `was the cause`, `the cause of the accident`; `cause of death`
  and `contributing condition` in autopsy context are *not* matches) — leakage rule;
- **E5** no two C/F findings inside the unit share identical stripped text with
  conflicting roles (21 events / 48 rows corpus-wide; role is ill-posed there).

These remove invalid measurement. They do **not** subset by aircraft type,
weather, fatality, year range, pilot error, or any phenomenon-defining property.

## 4. Frozen sample

- `SEED = 20260831`.
- Draw **600 eligible events**, stratified proportionally by `ev_year`
  (largest-remainder allocation), one `Aircraft_Key` unit per event
  (the lowest eligible `Aircraft_Key`, deterministic).
- If fewer than 600 eligible events exist, take all of them and record it.
- Events are **not** selected on any pilot-model behaviour.

## 5. Items

Written to `items/g0_events.jsonl`, `items/g0_relevance.jsonl`, `items/g0_roles.jsonl`,
`items/sampling_manifest.json`.

- **Task A (relevance)** — one item per finding in the unit:
  - gold `YES` iff `Cause_Factor in {C,F}`;
  - gold `NO` iff `Cause_Factor` blank **and** `cm_inPc == 'F'`;
  - findings with blank `Cause_Factor` and `cm_inPc == 'T'` are **dropped**
    (relevance status not resolvable under the legacy schema).
- **Task B (role)** — one item per C/F finding; gold `CAUSE` / `CONTRIBUTING_FACTOR`.

## 6. Model input — what is allowed

Allowed: the factual narrative `narr_accp` (truncated to the first **1200
whitespace tokens**, truncation flagged per item) and the stripped
`finding_description`.

Forbidden and never rendered: `Cause_Factor`, `cm_inPc`, `narr_cause`
(probable-cause statement), `narr_accf` (final report summary), `finding_code`,
`category_no`/`subcategory_no`/`section_no`/`subsection_no`/`modifier_no`,
`ntsb_no`, and the ` - C` / ` - F` suffix that NTSB appends to
`finding_description` (present on 42,045 of 43,522 C/F rows — **the single
largest leak in this dataset**, stripped by regex `\s-\s[CF]\s*$`).

## 7. Frozen prompts

Identical for every family. No per-model tuning. No chain-of-thought. No NTSB
annotation-policy definitions.

**Task A (relevance):**
```text
You are given the factual description of an aviation accident and one investigation finding.

ACCIDENT:
{narrative}

FINDING:
{finding}

Question: Was this finding causally relevant to the accident according to the investigation?
Answer only YES or NO.
```

**Task B (role):**
```text
You are given the factual description of an aviation accident and one finding that investigators considered causally relevant.

ACCIDENT:
{narrative}

FINDING:
{finding}

Question: Was this finding classified as a CAUSE or a CONTRIBUTING FACTOR?
Answer only CAUSE or CONTRIBUTING_FACTOR.
```

**Paraphrase of Task B (fixed in advance, §13 of the handoff):**
```text
Below is the factual description of an aviation accident, followed by one finding that
the investigation treated as causally relevant.

ACCIDENT:
{narrative}

FINDING:
{finding}

Did the investigators list this finding as a cause of the accident, or as a factor that
merely contributed to it?
Answer only CAUSE or CONTRIBUTING_FACTOR.
```

Decoding: `temperature=0`, `top_p=1`, `max_tokens=8`, chat template applied,
raw text saved including parse failures.

## 8. Panel (>= 3 genuinely different families)

| family | repo | role |
|---|---|---|
| Qwen | `Qwen/Qwen3-8B` | family 1 |
| Gemma | `google/gemma-3-12b-it` | family 2 |
| Llama | `NousResearch/Meta-Llama-3.1-8B-Instruct` | family 3 |
| Mistral | `mistralai/Mistral-Small-24B-Instruct-2501` | family 4 |

Exact revisions, tokenizer revisions, vLLM/transformers/torch versions and chat
templates are recorded in `results/<family>/manifest.json`.

## 9. Preregistered S0 promotion criterion (handoff §13)

For at least **2 of 4** families:

```text
Task-A relevance balanced accuracy      >= 0.75
AND Task-B C-vs-F balanced accuracy     <= 0.62
AND (relevance_BA - role_BA)            >= 0.15
```

plus all of:

- the gap survives event-grouped bootstrap (95% CI for the gap excludes 0);
- the gap is not produced by class imbalance (balanced accuracy is the headline;
  majority-class and stratified-random baselines reported);
- no single accident category or single year contributes most of the effect
  (diagnostic, not a rescue subset);
- the same qualitative gap holds under the fixed Task-B paraphrase of §7.

## 10. Preregistered controls

1. **Label-prior baseline** — majority-class and stratified-random C/F.
2. **Finding-text-only** — Task B without the narrative.
3. **Narrative-only** — Task B with the finding text removed.
4. **Code removal** — primary already excludes `finding_code`; a sensitivity
   analysis additionally drops items whose last taxonomy segment is
   `Contributed to outcome` (91.5% `F` within mixed events, 472/13,092 rows).
5. **Probable-cause leakage** — token-overlap of every model input against that
   unit's `narr_cause`; E4 already excludes role wording; high-overlap items inspected.
6. **Year / deprecation** — role BA reported by `ev_year` (mixed-role events span
   2008–2020).

## 11. Hard kill conditions (handoff §16 — no rescue permitted)

| code | trigger |
|---|---|
| `KILL-DATA / INSUFFICIENT-NATURAL-MIXED-ROLE-POPULATION` | < 500 mixed-role events or < 1000 C/F rows in them |
| `KILL-DATA / ROLE-GOLD-UNUSABLE` | C/F semantics incoherent or unpairable with a non-leaky narrative |
| `KILL-S0 / RELEVANCE-ALSO-FAILS` | Task-A BA < 0.75 in >= 3 of 4 families |
| `KILL-S0 / ROLE-SELECTION-IS-EASY` | Task-B BA > 0.62 in >= 3 of 4 families |
| `KILL-S0 / ONE-FAMILY-ONLY` | the full conjunction of §9 holds in <= 1 family |
| `KILL-ARTIFACT / LEXICAL-LABEL-PREDICTION` | finding-text-only Task-B BA >= full-context Task-B BA - 0.02 **and** >= 0.62 |
| `KILL-ARTIFACT / CONCLUSION-LEAKAGE` | model inputs found to carry probable-cause wording |

If S0 survives: write `g0_report.md`, **do not start MI**, and hand off to N0/N1.
MI (probes, SAEs, patching, tracing, steering, head/neuron search, linear
directions) is forbidden in this task under all outcomes.

## 12. Pre-model data facts already established (audit/, no LLM involved)

- 72,381 findings, 24,262 events with findings, `Cause_Factor` blank on 39.9%.
- Crosstab confirms the handoff: `C -> cm_inPc=T` (37,764/37,764),
  `F -> cm_inPc=T` (5,758/5,758), and 17,519 rows have `cm_inPc=T` with **blank**
  `Cause_Factor`. `cm_inPc=T` is therefore demonstrably not C-gold.
- Mixed-role events: **3,506**; C rows 7,383; F rows 5,709; years 2008–2020;
  largest single year 21.2%; ACC 3,366 / INC 140. Minimum viability gate **PASS**.
- Corpus-wide C:F is 87:13, but **inside mixed-role events it is 56:44** — this is
  what makes the role task well-posed, and it is the registered population.
- A leave-one-out finding-text lookup table (corpus annotation statistics the
  models do not have) reaches C/F balanced accuracy **0.758** inside mixed-role
  events. This is the data-side lexical ceiling; Control 2 is the model-side test.
