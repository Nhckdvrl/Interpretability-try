# Preregistration Addendum 1 — Metadata Stupid-Baseline Leak Audit

Frozen 2026-08-31, **after the panel began generating but before any model output
was inspected, scored, or loaded into an analysis**. Nothing below changes the
frozen sample, the prompts, the panel, or any S0 threshold. It adds mandatory
*reporting* obligations and records a limitation found by the audit.

Artifact: [`audit/metadata_leak_audit.json`](audit/metadata_leak_audit.json),
produced by [`scripts/metadata_leak_audit.py`](scripts/metadata_leak_audit.py).

## 1. What was run

On the frozen 2,149 role items, C-vs-F was predicted from feature blocks that
carry **no accident semantics**, scored with `GroupKFold(5)` clustered on `ev_id`
(no accident split across folds):

| block | grouped-CV balanced accuracy |
|---|---:|
| majority class | 0.500 |
| **META** — position in event, occurrence index, year, narrative length, Aircraft_Key, missingness patterns | **0.697** |
| **META+LEN** — META plus finding-text length/punctuation statistics | **0.797** |
| CODE — taxonomy codes (**never** rendered into any prompt) | 0.751 |

Single-feature grouped CV:

| feature | BA | in the model's evidence envelope? |
|---|---:|---|
| `finding_no / n_findings` (normalised position) | 0.693 | **no** |
| `finding_no` (raw position) | 0.672 | **no** |
| `len(finding_text)` in characters | 0.668 | **yes** |
| punctuation count in finding text | 0.626 | **yes** |
| `ev_year`, narrative length, missingness, Aircraft_Key, occurrence index | 0.50 | — |

Driver of the positional effect — NTSB coders list cause findings first:

| `finding_no` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8+ |
|---|---|---|---|---|---|---|---|---|
| P(CAUSE) | 0.83 | 0.61 | 0.39 | 0.39 | 0.37 | 0.31 | 0.23 | 0.24 |

## 2. Verdict: the audit FAILS its own bar, and this must be reported, not patched

Semantics-free metadata reaches 0.697–0.797, **above** the preregistered S0 role
ceiling of 0.62. Two consequences, which point in opposite directions and must
both be stated:

### 2.1 Ordering convention is *outside* the evidence envelope (limitation on interpreting a low B)

`finding_no` is never shown to any model: every item presents **one** finding in
isolation, with no ordering, index, or sibling findings. The positional
regularity therefore cannot inflate model role accuracy.

But it means a substantial part of the C/F gold is **coder bookkeeping
convention** that no model could recover from the evidence it is given. So a low
Task-B score cannot be attributed *entirely* to a causal-role reasoning failure:
some of the label variance is annotation order. **This is the single strongest
reviewer attack on the topic and it is now on the record before any result.**

### 2.2 Finding-text length is *inside* the envelope (limitation on interpreting a high B)

`len(finding_text)` alone reaches 0.668. The model sees the finding text, so this
non-semantic cue is available to it. Any Task-B score at or below ~0.67 is
therefore not evidence of causal-role competence.

## 3. Mandatory additional reporting (no threshold changed)

`g0_report.md` and `analyze_g0.py` must report, alongside every Task-B number:

1. the three metadata baselines above as reference lines — a role BA is only
   interpretable relative to 0.697 (META) and 0.797 (META+LEN), not to 0.5;
2. Task-B balanced accuracy stratified by finding-text length tercile — if role
   accuracy tracks length, the model is riding the in-envelope length cue;
3. Task-B balanced accuracy stratified by `finding_no` — the model cannot see
   position, so any strong monotone trend here means the model has *recovered*
   the coder convention from semantics, which is informative either way;
4. the explicit statement that C is **not** a unique "principal cause": NTSB
   determines "one or more probable causes", multiple `C` findings per event are
   normal, and the object is `cause vs contributing factor`, never root-cause
   analysis.

## 4. Not done, deliberately

- No item is dropped to break the position/length correlation (that would be
  subset rescue and would narrow the registered population).
- No S0 threshold is moved in either direction.
- The frozen sample, prompts and panel are untouched.

## 5. Evidence-envelope assertion (also verified here)

Task A and Task B render exactly the same two fields, `{narrative}` and
`{finding}`, for all 2,149 shared items; the only textual difference is the
framing sentence and the question. No probable-cause statement, conclusion,
`cm_inPc`, ordering position, C/F suffix, or legacy-only metadata reaches either
task. Verdict `PASS`.
