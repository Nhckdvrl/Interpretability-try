# Top-6 completed experiment review — 2026-08-30

Status: `AUTHORITATIVE INDEPENDENT POST-RUN REVIEW`

This review re-audits the completed Top-6 projects independently of each project's own final verdict. The standard is not "did the report say NO-PROMOTE?" but:

1. did the implementation actually measure the registered scientific object;
2. was there a valid capability / recognition denominator;
3. did the preregistered fatal controls distinguish the intended phenomenon from simpler alternatives;
4. were statistical units and bootstrap clusters appropriate;
5. is a null strong enough to falsify the registered claim, or merely a measurement/capability failure;
6. does any positive result support the broad paper claim or only a post-hoc subset.

Only projects whose **registered scientific claim is cleanly rejected** are archived. A failed measurement is not treated as a scientific null.

---

## Executive verdict

| project | independent verdict | action |
|---|---|---|
| `014_alias_entrainment_transfer` | **ESTABLISHED, with narrowed claim** | **KEEP ACTIVE** |
| `015_clarification_resolution_lag` | **REGISTERED PHENOTYPE REJECTED** | **ARCHIVE** |
| `016_mixed_status_event_attraction` | **REGISTERED BROAD PHENOTYPE REJECTED** | **ARCHIVE** |
| `017_cross_modal_resolution_inertia` | **REGISTERED INTERPRETATION-SPECIFIC PHENOTYPE REJECTED** | **ARCHIVE** |
| `018_stock_flow_correlation_intrusion` | **INCONCLUSIVE — MEASUREMENT / RECOGNITION FLOOR** | **KEEP, HOLD-REDESIGN** |
| `019_abstention_hysteresis` | **STRONGLY REJECTED** | **ARCHIVE** |

The main scientific lesson is that `NO-PROMOTE` has two different meanings. 015/016/017/019 contain diagnostic negative evidence against their registered claims. 018 does not: its decisive estimand was never identifiable because the net-flow gate collapsed under an A/B presentation artifact.

---

# 014 — Alias Entrainment Transfer

## Verdict: ESTABLISHED, but not reference-specific

This is the only clearly positive project among the six.

### What is established

The corrected r4 bank contains 1,768 ordered items / 1,370 entities, with 1,220 confirmatory entities. `ASSOC_ANY` is a different-referent, externally grounded strong-association control whose Wikipedia sentence association is at least as strong as the alias-target association; target-token leakage is forbidden. Entity type, direction and surface structure are factors rather than convenience filters.

Broad `ALIAS - ASSOC_ANY` is large and stable in all three families and both frames:

- Qwen3-8B: +3.446 / +3.567 nats;
- Gemma-3-12B-IT: +4.117 / +4.079;
- Llama-3.1-8B-Instruct: +3.216 / +2.897;

all bootstrap CIs exclude zero. Same-type ASSOC sensitivity and both surface directions also survive.

Therefore the project has a real behavioral result beyond exact-string repetition:

> contextual entrainment / salience spills across learned or derivable relations between surface forms, even when the target surface itself never appeared and a strong different-referent association is controlled.

### What is rejected

The reference-specific Q2 does not pass. On hard-identity-gated `opaque_strict` pairs, all three families show a positive F2 estimate but every F1 CI crosses zero. On the ungated 323-entity opaque-strict population, all six family×frame CIs cross zero.

The structure gradient is instead very strong:

`compositional > partial > opaque >> opaque-strict≈0`.

Combined with Phase 3's direct-write result, this supports a lexical/derivational boundary much better than a special shared-referent state.

### Implementation audit

The strongest concern in this project was construct validity, and r4 handled it unusually well:

- the earlier population narrowing was explicitly reversed;
- zero-joint ASSOC matches were detected in source audit and removed before model calls;
- casefold ID collisions were detected, old outputs discarded, and all families rerun;
- the circular use of ASSOC as the identity foil was detected, replaced by an independent rotated foil, and all families rerun;
- final inference is entity-clustered and both directions/frames are preregistered.

These corrections strengthen rather than select for the result. The surviving Q1 is therefore credible.

### Paper route

Keep 014 active. The paper-level claim should be **cross-surface learned-relation spillover and its lexical/reference boundary**, not "entity salience" or "shared referent circuit". No F2-only, person-only, direction-only, or alias-subtype rescue of Q2 is allowed.

---

# 015 — Clarification Resolution Lag

## Verdict: registered phenotype rejected

### Why the experiment is valid

CondAmbigQA provides source-authored ambiguous questions, multiple source-authored resolving conditions and their answers. The D0 uses 400 deterministic pairs across 376 independent questions. The crucial design is sound:

- `DIRECT`: Q + target resolving condition;
- `AMBIGUITY_HISTORY`: Q → explicit ambiguity clarification → the same target condition;
- `MATCHED_HISTORY`: Q → neutral extra conversational turn → the same target condition;
- `WRONG_CONDITION`: another source-valid condition whose gold answer must flip.

A/B answer order is counterbalanced. The gate requires both DIRECT and WRONG_CONDITION to be correct under both orders, which establishes that the model can use the resolving condition. Analysis averages the two answer orders and bootstraps at the source-question level, so multi-property questions are not treated as independent samples.

### Why the null is diagnostic

All three families show a small DIRECT-vs-AMBIGUITY difference, but the neutral MATCHED history produces essentially the same difference. The actual ambiguity-specific estimand is `MATCHED_HISTORY - AMBIGUITY_HISTORY`:

- Qwen: +0.092 pp, CI [-0.551,+0.735];
- Gemma: +0.289, [-0.289,+1.012];
- Llama: -0.213, [-1.064,+0.426].

The probability readout agrees. The broad ungated result is also not a stable ambiguity-history penalty.

This is exactly what the fatal matched-history control was designed to test. The registered claim was not "an extra conversation turn changes answers"; it was an **ambiguity-specific residual after clarification**. That residual is absent across three families with large capability-gated denominators.

### Limitation that does not rescue the project

D0 operationalizes the final decision as forced-choice A/B, not free generation of clarification/hedging language. A future project could ask specifically whether models continue to *verbally* request clarification after resolving evidence arrives. But that is a new behavioral contract/readout; it cannot be used to keep the current registered project alive after its diagnostic contrast failed.

### Action

Archive 015. Do not rescue via question subtype, PRACTIQ-only subset, alternative threshold, or mechanism work.

---

# 016 — Mixed-Status Event Attraction

## Verdict: registered broad phenotype rejected

### Why the experiment is valid

MAVEN-FACT supplies source event mentions and factuality labels. The builder preserves the natural same-document population and constructs 350,834 ordered mixed-status pairs, then a same-document same-target-status matched control bank. The 576-pair D0 is direction-balanced; event relation, sentence distance, event type and same-sentence status remain analysis factors rather than post-hoc filters.

The key improvement over a naive `MIXED - LOCAL` experiment is the **same-status context control**. Adding any second event can change local inference, attention allocation or discourse interpretation. Therefore factuality attraction requires:

`MIXED_STATUS - SAME_STATUS`,

not merely `MIXED_STATUS - TARGET_LOCAL`.

Analysis counterbalances label-option order, gates on target-local recognition under both orders, and clusters by source document.

### Result

`MIXED - LOCAL` is positive in all three families, but `SAME - LOCAL` is also positive. The diagnostic `MIXED - SAME` main-order CI crosses zero in all three families:

- Qwen +2.491 pp [-0.158,+5.523];
- Gemma +0.190 [-1.737,+2.316];
- Llama -0.136 [-0.588,+0.384].

Toward-neighbor discrete transitions are also unstable. The no-explicit-relation stratum is null in all three families. Qwen's large `PS+ -> CT+` cell is small-n and does not reproduce in Gemma or Llama.

### Important limitation

Recognition rates are low (15–23%), especially for rare factuality labels. This lowers power. The same-status control is distance-matched but not a perfect event-semantic match, which adds noise. These limitations make the negative conclusion slightly less decisive than 019.

However, they do not provide positive evidence for the registered broad claim: the only broad effect is explained by adding another event, the diagnostic controlled estimand is null in every family, the no-relation stratum is null, and the apparent strongest direction fails replication. Under the repository's anti-subset-rescue rule, the current broad phenotype is finished.

### Action

Archive 016. A future substantially different benchmark with much higher factuality capability could instantiate a new contract, but the current MAVEN-FACT D0 must not be revived by selecting `PS+ -> CT+`, one model, or one presentation order.

---

# 017 — Cross-Modal Resolution Inertia

## Verdict: registered interpretation-specific phenotype rejected

### What the design correctly isolates

The static MUCAR phenomenon is not our novelty. D0 gates on the stronger condition:

`text-only wrong AND simultaneous image+text correct`.

Only then does it test whether a text-first history makes the same image less able to correct the answer.

The experiment includes several unusually useful controls:

- actual initial wrong A/B label in history;
- ordinal restatement of the same wrong option;
- **masked prior choice** where the identity is hidden;
- matched neutral history;
- image-first history;
- canonical/reversed option order;
- source `pair_id` cluster bootstrap.

The released MUCAR mapping defect was handled correctly: only the 186 rows whose annotation IDs deterministically identify one released image were used; the remaining 186 ambiguous suffix mappings were not guessed from the gold.

### Why the intended phenomenon fails

No family passes the full frozen gate.

- Qwen has a strong ordinal-vs-matched effect, but actual-label persistence is not above matched history and the valid pair-cluster count is below floor.
- Gemma has a sizeable point estimate for actual-label persistence but insufficient denominator and control CIs cross zero.
- Llama is adequately powered and has a very large text-first effect, but **masked history reproduces almost all of it**: actual/ordinal persistence ≈.687, masked ≈.672; ordinal-minus-masked is ≈.015.

The strongest powered signal therefore does not require knowing which interpretation was previously chosen. It is much better described as a sequential-format / late-image integration cost than as persistence of a particular old interpretation.

### Limitation

The official release defect leaves only 39 `pair_id` clusters and the Llama checkpoint is a released 4-bit conversion. A larger corrected source could increase power. But current evidence still rejects the **registered cross-family, interpretation-identity-specific** claim: the strongest family fails the identity control, while the other families show different/non-replicating response forms.

### Action

Archive 017. Reopening after an upstream corrected mapping or a new benchmark should be a new contract and must retain the masked-choice control as fatal.

---

# 018 — Stock–Flow Correlation Intrusion

## Verdict: INCONCLUSIVE — do not archive as a scientific null

This project is the important exception.

### Data construction is good

The source design is strong: 600 real ResOpsUS windows from 200 reservoirs, exactly 150 per 2×2 cell (`net direction × inflow trend`), with spacing, closure and unit checks. The natural-data bank is not the failure.

### The recognition measurement failed

The contract gates on four A/B presentations of the net-flow sign: two column orders × two answer orders. Every gated item in every family has **positive** net flow. Negative-net cells have zero strictly gated items.

This is visibly a presentation artifact rather than evidence that the models cannot determine a negative net:

- Llama negative-net recognition is ~99–100% when the correct answer is in the canonical position and 0% after option reversal;
- Qwen and Gemma also show large canonical/reversed and column-order swings.

Thus the denominator required for `local net computation correct -> downstream stock follows inflow` never exists across both net directions.

The analyzer correctly returns the controlled estimand as non-estimable. The code is faithful to the frozen contract; the problem is that the **contract's forced-choice recognition instrument is too position-sensitive**.

### Why positive-net diagnostics do not establish the claim

On the surviving positive-net subset, the direct stock question does show inflow-aligned differences (+11.72/+5.43/+9.13 pp). But after the correct semantic net direction is placed in history, Qwen becomes approximately null, Gemma reverses, and Llama is only +1.67 pp, below the frozen threshold. These are useful diagnostics, not a valid substitute for the missing 2×2 estimand.

### Correct next status

Do **not** say the scientific phenomenon is false. Set 018 to `HOLD-D0-MEASUREMENT-FAILURE / REDESIGN-REQUIRED`.

A legitimate D0 v2 must be frozen before new outcomes and should replace the letter-sensitive net gate with a semantic/numeric recognition instrument, e.g.:

- directly score `positive` vs `negative` semantic continuations rather than A/B labels;
- or require open numeric cumulative-net computation with deterministic parsing;
- retain wording/order counterbalances as diagnostics rather than requiring four letter positions all to be correct;
- keep the full 2×2 net-direction × inflow-trend population and the explicit-correct-net stock control.

No positive-net-only rescue is allowed.

---

# 019 — Abstention Hysteresis

## Verdict: strongly rejected

This is the cleanest negative result among the six.

### Design quality

HotpotQA and MuSiQue provide source-grounded supporting evidence. The builder removes every supporting paragraph to create the incomplete turn, verifies answer/alias strings are absent, then restores the exact full evidence. Every final condition ends with the **byte-identical complete final payload**.

The gate is exactly appropriate: the model must answer correctly with full evidence and must genuinely abstain on the incomplete evidence.

Controls separate refusal identity from conversational transition:

- self-generated abstention;
- teacher abstention;
- nonliteral paraphrased abstention;
- neutral assistant response after the same incomplete user turn;
- unrelated answered history.

Both generated abstention and an independent ANSWER-vs-ABSTAIN continuation-probability readout are analyzed with paired bootstrap.

### Result is opposite to the hypothesis

Prior abstention sharply **reduces**, rather than increases, final abstention:

- Qwen: -40.7 pp [-50.5,-30.8];
- Gemma: -11.0 [-16.9,-5.1];
- Llama: -23.7 [-34.2,-14.5].

The continuous probability readout points the same way. Both datasets show the same direction. Final correctness generally improves.

More importantly, teacher/paraphrase/neutral histories show nearly the same recovery. The self-vs-neutral residual is tiny and changes sign across families. Therefore this is not a refusal-specific reverse phenomenon either; it is mainly an incomplete→complete conversational-transition facilitation effect.

Although the preregistered per-source gate count is slightly under floor for some family/source cells, the substantive failure is not underpowering: the primary effect is large, cross-family, cross-source and strongly opposite to the hypothesis.

### Action

Archive 019. Do not post-hoc rename it to "evidence-update history helps QA"; the current design was built to test refusal-specific stickiness, not to identify the causal source of the reverse facilitation.

---

# Final routing

## Keep / develop

### 014 Alias Entrainment Transfer

Scientific status: **positive**.

Paper story should integrate:

1. broad cross-surface spillover beyond a strong association control;
2. compositional→partial→opaque→opaque-strict structure gradient;
3. phase-2 shared upstream causal machinery;
4. phase-3 lexical direct-write boundary;
5. explicit negative result for reference-specific residue.

## Hold, redesign measurement

### 018 Stock–Flow Correlation Intrusion

Scientific status: **unknown**. Current D0 is not sufficient to reject it.

No new model call until a semantic/numeric recognition contract is frozen. Preserve the four-cell natural source population.

## Archive as failed registered contracts

- 015 Clarification Resolution Lag;
- 016 Mixed-Status Event Attraction;
- 017 Cross-Modal Resolution Inertia;
- 019 Abstention Hysteresis.

Archive means the **current scientific contract cannot be revived by prompt/subset/readout/model changes**. A genuinely new scientific object may of course be proposed later, but it must be registered as a new contract rather than inheriting the old project's identity or positive-looking subcells.
