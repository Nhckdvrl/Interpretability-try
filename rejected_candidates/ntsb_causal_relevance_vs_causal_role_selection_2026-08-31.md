# NTSB Causal Relevance ≠ Causal-Role Selection — TERMINAL

Date: 2026-08-31
Death code: **`KILL-S0 / RELEVANCE-ALSO-FAILS`**
Evidence: [`phenomenon_miner/ntsb_causal_role_g0/results/g0_report.md`](../phenomenon_miner/ntsb_causal_role_g0/results/g0_report.md)

## Natural question

> In a real accident, can a model correctly recognize which findings are causally
> relevant while still failing to distinguish findings investigators classify as
> **causes** from findings they classify as **contributing factors**?

Never "find the one true root cause": NTSB determines one or more probable causes
and multiple `C` findings per event are normal.

## Why it looked good

- Genuinely expert-grounded external substrate: NTSB publishes structured
  investigation data with a historical `Cause_Factor` `C`/`F` role label, produced
  by professional investigators, not by us and not by an LLM.
- The 2024 Release 3.0 note is explicit that the new `cm_inPC` merges the old
  C/F distinction, so restricting to legacy C/F is *necessary*, not a manufactured
  distinction.
- The data gate genuinely passed: 3,506 natural mixed-role events, 13,092 C/F
  rows, spread over 2008–2020, C:F = 56:44 inside mixed-role events.
- The 2025–2026 neighbourhood (NTSB/HFACS accident investigation, aviation RAG
  causal analysis, maritime RCA) studies *finding the cause from accident
  material*; some of it even feeds the official `Probable Cause` text in as
  prompt input. None of it established this narrower, leakage-free
  relevance-vs-role-selection dissociation.

## Kill evidence

Frozen before any model load: 600 year-stratified events, 2,390 relevance items,
2,149 role items, fixed prompts, deterministic decoding, event-grouped bootstrap.

Balanced accuracy, four open families:

| family | Task A relevance | Task B role | gap |
|---|---|---|---|
| Qwen3-8B | 0.562 [0.535, 0.590] | 0.544 | 0.018 |
| Gemma-3-12B-it | 0.537 [0.515, 0.561] | 0.546 | −0.010 |
| Llama-3.1-8B-Instruct | 0.635 [0.596, 0.671] | 0.503 | 0.131 |
| Phi-4-mini-instruct | 0.539 [0.505, 0.573] | 0.533 | 0.006 |

The preregistered criterion needed >=2 of 4 families with relevance >=0.75,
role <=0.62 and gap >=0.15. **0 of 4 qualify, and the failure is on the
relevance axis in 4 of 4** (trigger required >=3 of 4).

The premise of the frontier is false: relevance recognition is *not* strong.
There is no "relevance strong / role weak" dissociation — there is
"relevance weak / role at chance". Every family also collapses onto
CONTRIBUTING_FACTOR (predicted 72–99% of items against 56% CAUSE gold); Llama
predicts CAUSE 20 times out of 2,149.

Two further facts that would have to be answered even if the numbers had come out
the other way:

- **Semantics-free metadata beats every model.** Grouped-CV balanced accuracy is
  0.697 from bookkeeping alone and 0.797 with text-length statistics, against a
  best model score of 0.546. `finding_no` alone gives 0.693 because NTSB coders
  list cause findings first (P(CAUSE) 0.83 → 0.24 across positions). That ordering
  is outside the model's evidence envelope, so a meaningful part of the C/F gold
  is coder bookkeeping that no model could recover from one isolated finding.
- **The relevance axis has no valid negative class.** Task-A negatives are
  findings the investigation recorded but did not cite in the probable cause —
  they are not irrelevant to the accident. NTSB provides no natural "irrelevant
  finding" population, and only 241 negatives exist across 177 of 600 events.

Adding the accident narrative made role selection *worse* for Qwen (+0.074) and
Phi (+0.075) relative to finding-text-only, which is the opposite of what a
context-using causal-role computation would predict.

## Nearest-neighbor warning

Dead by meaning. Do **not** resurrect as:

- cause vs contributing factor on another accident/incident corpus — maritime,
  rail, NHTSA, medical incident reports, OSHA, mining, ASRS, aviation safety
  RAG, or non-US aviation authorities;
- `cm_inPC` relevance vs legacy C/F role, or any other pairing of a
  relevance/inclusion field with a role/severity field in an investigation DB;
- root-cause vs contributing-cause extraction, causal ranking, causal chain
  ordering, primary vs secondary cause, blame vs causation, necessity vs
  sufficiency, or "which cause matters most";
- the same dissociation renamed as causal detection vs causal weighting, causal
  set membership vs causal hierarchy, relevance filter vs role selector,
  admit-then-rank, or any reader/writer, gate/dial, state/selector vocabulary;
- rescuing it with bigger models, reasoning models, CoT, few-shot, per-model
  prompt tuning, a different aircraft/weather/fatality/year subset, or an
  LLM judge in place of the NTSB label.

Note also that the neighbouring object "LLM finds the cause from accident
material" is already occupied by 2025–2026 NTSB/HFACS and aviation-RAG work; this
candidate was only ever distinct because of the leakage-free role-*selection*
framing, which the data has now falsified on open models.

## Resurrection condition

All of the following, simultaneously:

1. an external, expert-produced substrate that supplies a **valid negative
   class** — findings genuinely established as *not* causally relevant, not merely
   "not cited in the summary";
2. a role label whose variance is **not** substantially predictable from
   annotation bookkeeping (position, length, coder convention) — the audit here
   reached 0.697/0.797 from semantics-free features alone;
3. current interpretable open models demonstrating **relevance BA >= 0.75** on
   that substrate before any role claim is made;
4. and the role gap surviving event-grouped bootstrap in >=2 genuinely different
   families under prompts fixed in advance.

Changing corpus, domain, model, language, prompt, or MI method satisfies none of
these.

## Status

`PASS_REGISTER` remains **0**. MI was never started and remains forbidden.
