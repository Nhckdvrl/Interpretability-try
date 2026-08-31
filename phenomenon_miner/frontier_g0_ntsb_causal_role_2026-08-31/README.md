# Frozen G0 — NTSB causal relevance vs causal-role selection

Date: 2026-08-31
Status: **`S0 PASS / G0 AUTHORIZED / NOT REGISTERED / NO MI`**

The official artifact audit is frozen in
`../ntsb_avall_audit_2026-08-31/S0_RESULT.md`. This directory tests the only
behavior that could justify keeping the frontier alive.

## Natural question

> If a model can identify which facts mattered to an accident, can it distinguish
> what **caused** the accident from what merely **contributed** to it?

One ordinary example: an aircraft loses directional control in a crosswind. Both
the control failure and the wind matter. The investigation may call the control
failure a `Cause` and the crosswind a `Factor`. Merely detecting that both are
causally relevant is not the same computation as assigning their causal roles.

## Why the two stages are externally grounded

NTSB supplies two different official fields:

- `cm_inPC`: finding appears in the probable-cause statement as a **cause OR
  contributing factor** — relevance/inclusion;
- historical `Cause_Factor`: `C = Cause`, `F = Factor`, blank = other Finding —
  causal role.

Do not merge them. `cm_inPC` is not a principal-cause label.

## Frozen population

Use the deterministic, leak-clean 300-event manifest produced from official
`avall.zip` by `prepare_g0_population.py`.

Each event provides:

- NTSB Final Narrative (`narr_accf`), fallback Preliminary Narrative (`narr_accp`);
- candidate NTSB findings with legacy ` - C` / ` - F` suffix stripped;
- hidden `cm_inPC` relevance gold;
- hidden legacy C/F role gold;
- held-out NTSB Probable Cause Narrative (`narr_cause`) for an oracle control only.

No new human labels and no LLM judge.

## Frozen current-open-family panel

Run exactly one checkpoint per family:

- Qwen3 family: `Qwen/Qwen3-8B`
- Gemma 3 family: `google/gemma-3-12b-it`
- GPT-OSS family: `openai/gpt-oss-20b`

If a named checkpoint cannot be loaded for a hard technical/license reason,
document the substitution **before inspecting any G0 output**. Do not add a fourth
family to rescue 1/3.

Use deterministic decoding (`temperature=0`) and an OpenAI-compatible local text
endpoint. Save exact checkpoint revisions.

## Task R — causal relevance

Use only manifest events containing at least one official `cm_inPC=T` and at
least one official `cm_inPC=F` candidate. This is a validity restriction needed to
measure both classes, not a post-hoc subset.

Prompt presents the accident narrative and numbered candidate findings. Ask:

> Which findings were causally relevant enough to belong in the investigation's
> probable-cause statement, either as a cause or as a contributing factor? Return
> only the IDs.

Score each finding against `cm_inPC` with event-clustered:

- balanced accuracy;
- macro-F1;
- sensitivity/specificity;
- exact event set accuracy as a secondary metric.

Raw accuracy is never the primary metric because relevant findings are common.

## Task S — conditional causal-role selection

For the same event, present **only findings whose legacy gold is C or F**. Thus
all displayed findings are already known by construction to be causally relevant.
Ask the model to assign each finding one label:

- `cause`
- `contributing_factor`

Score against legacy NTSB `C/F` using balanced accuracy and macro-F1. This is the
primary behavioral stage. The model receives no `cm_inPC`, C/F suffix, or probable
cause narrative.

This conditional design deliberately gives relevance for free. If role selection
still fails, the result cannot be explained by the model simply overlooking an
irrelevant finding.

## Task O — oracle/interface control

Repeat Task S while additionally showing the held-out official `narr_cause`
Probable Cause Narrative. This is not a target behavior and is never used to claim
novelty. It tests whether the prompt/parser/model can map explicit NTSB causal-role
wording to the candidate findings.

If the oracle control does not reach high accuracy, the interface is too ambiguous
for the dissociation claim and G0 dies.

## Frozen phenotype gate per family

A family is a positive **only if all conditions hold**:

1. Task R parse coverage >= 95%;
2. Task S parse coverage >= 95%;
3. Task O parse coverage >= 95%;
4. Task R balanced accuracy >= 0.80;
5. Task R macro-F1 >= 0.75;
6. Task S balanced accuracy <= 0.65;
7. Task S macro-F1 <= 0.65;
8. `R_balanced_accuracy - S_balanced_accuracy >= 0.15`;
9. Task O balanced accuracy >= 0.90;
10. an event-cluster bootstrap 95% CI for the R-vs-S balanced-accuracy gap has
    lower bound > 0.05.

The candidate survives open-model existence only if >=2/3 families are positive.
Otherwise write a terminal rejection immediately.

The thresholds are intentionally asymmetric. A mild performance difference is
not enough; we need a visually obvious **relevance-good / role-selection-bad**
phenotype before MI is justified.

## Fatal interpretations / anti-rescue

Kill rather than rescue if:

- relevance itself is weak;
- cause/factor assignment is also strong;
- the gap appears in only one family;
- oracle role mapping is weak;
- the effect requires fatalities, weather cases, pilot-error cases, Part 91, one
  year range, long narratives, or another post-hoc subtype;
- chain-of-thought or an elaborate expert prompt is necessary to create the gap;
- the result reduces to generic extraction accuracy for `cause` vs `factor`.

Recent incident-analysis work already studies cause and contributing-factor
extraction. Therefore the only scientifically interesting phenotype here is the
**conditional two-stage dissociation**, not a new classifier benchmark.

## N0/N1 only after G0

If >=2/3 families pass, then attack at least these neighbors before registration:

1. 2025 NTSB/HFACS LLM accident-cause reasoning work;
2. AC-Reason / AC-Bench actual-causality reasoning;
3. 2026 healthcare incident-report LLM extraction of events, causes and
   contributing factors;
4. direct MI/representation/causal-intervention work on causal reasoning.

Do not start MI until that collision audit passes.

## Required committed outputs after execution

- frozen manifest SHA256;
- exact checkpoint revisions;
- raw per-event requests/responses for R/S/O;
- deterministic parser outputs;
- per-family item/event metrics;
- event-cluster bootstrap artifact;
- final G0 summary with hard-gate verdict.
