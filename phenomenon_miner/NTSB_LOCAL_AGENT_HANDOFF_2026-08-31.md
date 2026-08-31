# NTSB Local-Agent Handoff — Causal Relevance ≠ Causal-Role Selection

Date: 2026-08-31

Status: **DELEGATED ARTIFACT AUDIT → G0 / NOT PASS-REGISTER / NO MI**

This document is intended to be handed directly to a local coding/research agent with normal network access and shell access.

Do **not** begin mechanistic interpretability. The only job is to determine whether the real NTSB substrate exists cleanly enough and whether current open models exhibit the preregistered behavioral dissociation.

---

# 0. One-sentence scientific question

> In a real accident, can a language model correctly recognize which findings are causally relevant while still failing to distinguish findings investigators classify as causes from findings they classify as contributing factors?

The desired scientific object is **causal relevance ≠ causal-role selection**.

Do not rewrite this into generic root-cause analysis, cause extraction, actual causation, or an NTSB benchmark.

---

# 1. Authority and non-negotiable repository rules

Before doing anything, read:

1. `README.md`
2. `phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`
3. `phenomenon_miner/NEXT_AGENT_PROMPT_2026-08-31.md`
4. newest `rejected_candidates/continuation_terminal_addendum_*_2026-08-31.md`
5. `phenomenon_miner/NATURAL_QUESTION_GATE.md`
6. `phenomenon_miner/SCIENTIFIC_SUBSTRATE_GATE.md`
7. `phenomenon_miner/S0_FUNNEL_2026-08-31.md`
8. `phenomenon_miner/FAILED_TOPICS.md`
9. `archive/README.md`
10. `rejected_candidates/README.md`
11. `phenomenon_miner/REGISTERED_FRONTIER_NTSB_CAUSAL_ROLE_2026-08-31.md`

Current global state remains:

```yaml
PASS_REGISTER: 0
```

This NTSB frontier is registered only for execution tracking. It does **not** count toward the target five unless it later passes S0, N0, N1, anti-narrowing and MI-fit.

---

# 2. Critical semantic correction: `cm_inPC` is NOT C-vs-F gold

This is the most important rule in the whole task.

NTSB Release 3.0 says:

- `cm_inPC` was added to the `findings` table;
- valid values are TRUE/FALSE;
- TRUE means the finding was cited in the accident probable-cause statement **as a cause or contributing factor**;
- the old `cause_factor` field is deprecated;
- for historical rows, NTSB back-filled `cm_inPC=TRUE` whenever `cause_factor='C'` **or** `cause_factor='F'`.

Therefore:

```text
cm_inPC = relevance/inclusion in probable-cause explanation
cause_factor = historical role label C vs F
```

Never infer:

```text
cm_inPC TRUE = principal cause
```

That is false.

Also do not assume there is exactly one `C` per event. Multiple cause findings are possible.

Use the scientific wording **cause vs contributing factor / causal-role selection**, not “find the one true root cause.”

Official sources:

- https://data.ntsb.gov/avdata
- https://data.ntsb.gov/avdata/FileDirectory/DownloadFile?fileID=C%3A%5Cavdata%5CMDB_Release_Notes.pdf
- https://www.ntsb.gov/safety/data/pages/Data_Stats.aspx

As of 2026-08-31, the official directory lists:

```text
avall.zip
created: 2026-08-01 06:52:48
size: 95,636,276 bytes
```

---

# 3. Phase A — download the official artifact

Use the official file, not a scraped reconstruction, as the authoritative data source.

Suggested Linux shell:

```bash
set -euo pipefail

mkdir -p phenomenon_miner/ntsb_causal_role_g0/{raw,export,audit,items,results,scripts}
cd phenomenon_miner/ntsb_causal_role_g0/raw

curl -fL \
  --retry 5 \
  --retry-delay 3 \
  --retry-all-errors \
  'https://data.ntsb.gov/avdata/FileDirectory/DownloadFile?fileID=C%3A%5Cavdata%5Cavall.zip' \
  -o avall.zip

ls -lh avall.zip
sha256sum avall.zip | tee SHA256SUMS.txt
unzip -l avall.zip | tee unzip_listing.txt
unzip -o avall.zip
```

If the direct link changes, resolve it from the official directory page. Do not silently substitute a third-party CSV.

Record:

- download UTC timestamp;
- URL;
- byte size;
- SHA256;
- extracted MDB filename.

Commit only metadata/scripts/small audits, not the 95MB+ binary unless repository policy explicitly permits it.

---

# 4. Phase B — inspect the MDB before writing any experiment

Install MDB tools.

Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y mdbtools
```

macOS:

```bash
brew install mdbtools
```

Then:

```bash
MDB=$(find . -maxdepth 2 -iname '*.mdb' | head -n 1)
echo "$MDB"

mdb-tables -1 "$MDB" | tee ../audit/tables.txt
mdb-schema "$MDB" | tee ../audit/schema.sql
```

Do not assume capitalization or exact field names before inspecting the actual schema.

At minimum identify/export:

- `findings`
- `events`
- `narratives`

and any table needed to obtain a non-conclusion factual accident description.

Export example:

```bash
mdb-export "$MDB" findings > ../export/findings.csv
mdb-export "$MDB" events > ../export/events.csv
mdb-export "$MDB" narratives > ../export/narratives.csv
```

If table capitalization differs, use the actual names from `mdb-tables`.

Save exact commands in `scripts/extract.sh`.

---

# 5. Phase C — schema/label audit

Write a deterministic script, e.g.

```text
phenomenon_miner/ntsb_causal_role_g0/scripts/audit_population.py
```

The first run must produce **data facts only**, no LLM calls.

## 5.1 Findings-table audit

Print/save:

- total rows;
- column names/dtypes;
- unique values and missingness for `cause_factor`;
- unique values and missingness for `cm_inPC`;
- cross-tab `cause_factor × cm_inPC`;
- number of unique events;
- findings per event distribution;
- years covered after joining events;
- C/F availability by year.

Expected historical logic to verify, not assume:

```text
cause_factor in {C,F} -> cm_inPC TRUE
```

Because `cause_factor` stopped being populated for future cases after the deprecation, quantify exactly where it becomes sparse/absent.

## 5.2 Mixed-role population audit

For each event, compute:

```text
n_C
n_F
n_relevant = n_C + n_F
n_other_findings
```

Then count:

```text
mixed_role_event := n_C >= 1 AND n_F >= 1
```

Report:

- number of mixed-role events;
- number of C rows in mixed events;
- number of F rows in mixed events;
- median/mean C and F findings per mixed event;
- year distribution;
- event/investigation type distribution;
- whether mixed-role events are broad or concentrated in one narrow subtype.

Do **not** subset by aircraft type, weather, fatality, pilot error, etc. before seeing the global population.

## 5.3 Minimum viability rule

Do not run G0 if the natural population is tiny or pathologically narrow.

Initial conservative criterion:

```text
>= 500 mixed-role events
AND
>= 1,000 C/F labeled finding rows total inside mixed-role events
AND
reasonable spread across years and accident categories
```

If below this, do not lower the threshold after seeing the result. Write a rejection with:

```text
KILL-DATA / INSUFFICIENT-NATURAL-MIXED-ROLE-POPULATION
```

If counts are enormous, sample later; do not narrow the scientific object now.

---

# 6. Phase D — random-20 semantic audit

Before building prompts, create a **fixed random sample of 20 mixed-role events** using a recorded seed.

Example:

```python
SEED = 20260831
```

For each sampled event, save a human-readable audit containing:

- `ev_id` / NTSB accident number;
- date;
- factual narrative fields available to a model;
- all findings text;
- `cause_factor` C/F/blank;
- `cm_inPC`;
- probable-cause text **for audit only**;
- any codes used to generate finding text.

Output:

```text
phenomenon_miner/ntsb_causal_role_g0/audit/random20_mixed_role.md
```

Manually check all 20.

Questions to answer:

1. Are C and F labels semantically plausible distinctions, not database noise?
2. Are finding descriptions intelligible without proprietary code lookup?
3. Is there a factual narrative that can be supplied without leaking the final probable-cause wording?
4. Are C/F labels attached at event level or aircraft level in a way that requires preserving `Aircraft_Key`?
5. Do some events have duplicate/near-duplicate findings that make role prediction ill-posed?
6. Is the “F” category genuinely contributing-factor-like across cases?
7. Does the factual narrative already literally say “cause” / “contributing factor” for the target finding?

If the task leaks labels or is semantically incoherent, stop and write `KILL-DATA`.

---

# 7. Leakage rules — extremely important

The model must not see the conclusion it is supposed to predict.

Exclude from model input:

- `cause_factor`;
- `cm_inPC`;
- final probable-cause statement;
- fields that explicitly encode C/F status;
- finding codes if those codes trivially encode role;
- UI strings like `Cause:` / `Factor:`;
- post-investigation text that restates the official causal role verbatim.

The preferred evidence is the **factual accident narrative / synopsis before the final causal conclusion**, plus plain-language finding descriptions.

If the only available narrative is itself the probable-cause conclusion, the task is invalid.

---

# 8. The behavioral decomposition to test

The project only survives if the same model is good at **causal relevance** and clearly worse at **causal-role selection**.

This should be tested as two linked tasks on the same event distribution.

## Task A — causal relevance

Question shape:

> Given the factual accident description and this candidate finding, was this finding part of the official causal/contributing explanation of the accident?

Gold:

```text
positive: historical cause_factor in {C,F}
negative: finding not marked C/F
```

For historical rows, `cm_inPC` should agree with this inclusion logic; use the data audit to confirm.

Do not use LLM judging.

Score:

- balanced accuracy;
- macro-F1;
- AUROC only if a stable scalar score/logprob is available;
- positive/negative class counts;
- item-level predictions.

## Task B — causal-role selection

Only on findings already known to be causally relevant:

> Given the factual accident description and this causally relevant finding, did investigators classify this finding as a **cause** or a **contributing factor**?

Gold:

```text
C vs F from legacy cause_factor
```

Score:

- balanced accuracy;
- macro-F1;
- confusion matrix;
- per-event accuracy;
- item-level outputs.

Use exactly the same underlying mixed-role event population whenever possible.

---

# 9. Better paired formulation — preferred if feasible

A stronger test avoids comparing unrelated Task-A and Task-B items.

For every mixed-role event:

1. include at least one C finding;
2. include at least one F finding;
3. include one or more non-C/F findings if available;
4. ask the model to mark all causally relevant findings;
5. separately ask it to assign `CAUSE` vs `CONTRIBUTING_FACTOR` among the relevant findings.

Then compute within the same event:

```text
relevance_success
role_selection_success
```

This allows a direct dissociation count:

```text
relevance correct AND role wrong
```

The paper-level behavior, if real, is much stronger when this cell is common.

---

# 10. Prompt contract

Use ordinary, faithful prompts. No chain-of-thought requirement.

Freeze prompts before running the full panel.

A minimal format is preferable:

```text
You are given the factual description of an aviation accident and one investigation finding.

ACCIDENT:
{factual_narrative}

FINDING:
{finding_text}

Question: Was this finding causally relevant to the accident according to the investigation?
Answer only YES or NO.
```

Role task:

```text
You are given the factual description of an aviation accident and one finding that investigators considered causally relevant.

ACCIDENT:
{factual_narrative}

FINDING:
{finding_text}

Question: Was this finding classified as a CAUSE or a CONTRIBUTING FACTOR?
Answer only CAUSE or CONTRIBUTING_FACTOR.
```

Do not add definitions that simply reveal NTSB annotation policy unless a small preregistered instruction-control condition is run separately.

Do not optimize the prompt per model.

---

# 11. Current-open-model G0 panel

Use at least **3 genuinely different open model families** with accessible activations/weights.

Reasonable examples, subject to local availability and repository conventions:

- Qwen family (e.g. Qwen3 instruct checkpoint);
- Gemma family (e.g. Gemma 3 instruct checkpoint);
- Mistral family (e.g. current Mistral open instruct checkpoint).

Do not count two sizes of Qwen as two families.

Freeze:

- exact Hugging Face repo/model id;
- exact revision/commit;
- tokenizer revision;
- inference framework version;
- chat template;
- decoding settings.

Recommended G0 decoding:

```text
temperature = 0
max_new_tokens small
single deterministic answer
```

Save raw text even when parsing fails.

---

# 12. Freeze sample construction before model results

After the population/random-20 audit passes, build one frozen G0 sample.

Suggested target:

```text
300-600 mixed-role events
```

with broad time/category coverage.

Do not choose events based on which ones a pilot model gets wrong.

Suggested item construction:

- all C and F findings for sampled mixed-role events, capped only by a preregistered per-event rule if necessary;
- matched non-C/F findings from the same event for Task A when available;
- preserve event grouping for bootstrap/statistics.

Save:

```text
items/g0_events.jsonl
items/g0_relevance.jsonl
items/g0_roles.jsonl
items/sampling_manifest.json
```

Manifest must include seed and all filters.

---

# 13. S0 promotion criterion

Do not choose exact thresholds after seeing model outputs.

Recommended preregistered criterion:

For at least **2 of 3 model families**:

```text
Task-A causal-relevance balanced accuracy >= 0.75
AND
Task-B C-vs-F balanced accuracy <= 0.62
AND
(relevance_BA - role_BA) >= 0.15
```

Plus:

- the gap is not explained by an extreme class imbalance;
- the gap persists in event-grouped bootstrap CIs;
- no single accident subtype contributes most of the effect;
- the same qualitative gap appears under one minimal wording paraphrase fixed in advance.

These are suggested thresholds. If the local agent changes them, do it **before any full-model result is inspected**, document the reason, and never relax them post hoc.

A stronger promotion signal is:

```text
many individual events where relevance is correct for C/F findings,
but C and F are systematically confused
```

---

# 14. Required controls

## Control 1 — label-prior baseline

Report majority-class and stratified-random baselines for C/F.

## Control 2 — finding-text-only

Run the role task with only the finding description and no accident narrative.

Purpose:

- if role accuracy is already high from lexical/categorical cues alone, the task may be annotation-style prediction rather than causal reasoning;
- compare full-context gain over this baseline.

## Control 3 — narrative-only

Remove the target finding text and ask whether a candidate role can be inferred. It should not be possible in any meaningful way; this checks prompt leakage/artifacts.

## Control 4 — code removal

Primary result must use plain finding text without finding codes.

If codes improve performance drastically, treat that as dataset-artifact evidence, not scientific success.

## Control 5 — probable-cause leakage check

Search all model input text for exact/near-exact overlap with probable-cause text.

At minimum report string overlap diagnostics; manually inspect high-overlap cases.

## Control 6 — year/deprecation check

Because C/F is historical/deprecated, show that the result is not driven by one narrow early period or a schema-transition artifact.

---

# 15. Statistical analysis

Unit of dependence is the accident/event, not the individual finding row.

Use event-grouped bootstrap confidence intervals.

Recommended outputs per model:

```text
N events
N relevance items
N C items
N F items
Task A balanced accuracy / macro-F1
Task B balanced accuracy / macro-F1
A-B gap
95% event-bootstrap CI for gap
confusion matrices
fraction of events with relevance-correct / role-wrong dissociation
```

Also plot or tabulate role accuracy as a function of:

- number of C/F findings per event;
- year;
- narrative length;
- finding category only if category is a pre-existing field and this is diagnostic, not a rescue subset.

Do not search many subgroups for one that makes the title work.

---

# 16. Hard kill conditions

Immediately stop and write a rejection file if any of these occurs.

## `KILL-DATA / NO-MIXED-ROLE-POPULATION`

Mixed C/F events are too rare or too narrow.

## `KILL-DATA / ROLE-GOLD-UNUSABLE`

C/F semantics are inconsistent, duplicated, inaccessible, or cannot be paired with non-leaky factual narratives.

## `KILL-S0 / RELEVANCE-ALSO-FAILS`

Models that fail C/F selection are also bad at causal relevance. Then there is no relevance→selection dissociation.

## `KILL-S0 / ROLE-SELECTION-IS-EASY`

Models perform strongly on both relevance and C/F role selection. Then the claimed failure does not exist.

## `KILL-S0 / ONE-FAMILY-ONLY`

Only one model family shows the gap.

## `KILL-ARTIFACT / LEXICAL-LABEL-PREDICTION`

Finding-text-only or codes explain nearly all role accuracy/error structure.

## `KILL-ARTIFACT / CONCLUSION-LEAKAGE`

Inputs leak the probable-cause statement or explicit role wording.

Do not rescue a killed result by changing aircraft subtype, year range, prompt style, model size, language, or MI method.

---

# 17. N0/N1 audit only after S0 survives

Do not spend major time on mechanistic novelty before existence is established.

Known collision threats:

- formal actual-causation reasoning (`AC-Reason` and related work);
- generic cause-vs-contributing-factor extraction;
- medical incident root/contributing-factor extraction;
- root-cause analysis benchmarks;
- causal chain / event causality reasoning;
- generic “LLMs know but cannot select” mechanisms.

The title-level claim must remain:

> **Natural expert investigations reveal a dissociation between recognizing causal relevance and assigning causal role.**

If strongest-neighbor search finds this exact behavioral object already established, write `KILL-N1` even if nobody has done SAE/probing on it.

---

# 18. MI is forbidden until explicit promotion

Do not run:

- probes;
- SAEs;
- activation patching;
- causal tracing;
- steering;
- representation similarity;
- head/neuron search;
- linear direction discovery.

until all of the following are true:

```text
artifact audit PASS
random-20 PASS
current-open-family G0 PASS
N0 PASS
N1 PASS
anti-narrowing PASS
```

Only then write a separate MI preregistration.

---

# 19. If it survives: competing mechanisms worth testing later

These are hypotheses, not current claims.

1. **Single causal-strength scalar**
   - relevance and C/F role are thresholds/ranges on one scalar.

2. **Relevance detector + causal-role selector**
   - a finding is first admitted into a causal set, then a separate computation assigns cause vs contributing factor.

3. **Normality/responsibility/necessity selector**
   - all C/F findings are represented as causal, while a later selection operation weights abnormality, necessity, responsibility, temporal proximity, or explanatory centrality.

4. **Binding failure**
   - the model represents which roles exist in the event but binds C/F roles to the wrong findings.

5. **Narrative salience shortcut**
   - role selection follows mention order/prominence rather than causal structure.

A Hamdi-quality result would need to falsify a natural intuitive mechanism or predict a simple intervention, not merely show that C and F are linearly decodable.

---

# 20. Required local-agent deliverables

Create/commit these small artifacts:

```text
phenomenon_miner/ntsb_causal_role_g0/
  README.md
  scripts/
    extract.sh
    audit_population.py
    build_g0_items.py
    run_g0.py
    analyze_g0.py
  audit/
    tables.txt
    schema.sql
    population_summary.json
    cause_factor_cm_inPC_crosstab.csv
    mixed_role_summary.json
    random20_mixed_role.md
  items/
    sampling_manifest.json
    g0_events.jsonl
    g0_relevance.jsonl
    g0_roles.jsonl
  results/
    <model-family>/raw.jsonl
    summary.csv
    g0_report.md
```

Do not commit giant raw MDB/ZIP files unless explicitly intended.

`g0_report.md` must end with exactly one of:

```text
S0-PASS — proceed to N0/N1 audit; MI still forbidden.
```

or a specific kill code, e.g.

```text
KILL-S0 / RELEVANCE-ALSO-FAILS
```

If killed, immediately add a terminal entry under `rejected_candidates/` containing:

- Natural question;
- Why it looked good;
- Kill evidence;
- Death code;
- Nearest-neighbor warning;
- Resurrection condition.

---

# 21. Short execution order

Do this in exactly this order:

```text
1. download official avall.zip
2. hash + extract MDB
3. enumerate schema
4. export findings/events/narratives
5. audit cause_factor / cm_inPC / missingness / years
6. count mixed C/F events
7. fixed random-20 semantic/leakage audit
8. freeze factual non-conclusion input fields
9. freeze G0 sample + prompts + thresholds
10. run >=3 current open model families
11. compute relevance-vs-role dissociation with event bootstrap
12. PASS or KILL
13. only if PASS: N0/N1 exact-neighbor audit
14. only after N0/N1: consider MI
```

Do not spend time re-searching the NTSB schema on the web. The next useful action is local artifact execution.
