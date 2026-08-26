# 006 project progress

**Last updated:** 2026-08-27
**Current phase:** `D0 exploratory mechanism complete / V2 frozen / no confirmatory run started`
**Anchor model:** `Qwen/Qwen2.5-14B-Instruct`

This is the chronological project record. It connects the original topic, behavioral validation, code corrections, mechanism experiments, invalidated interpretations, current evidence, and the next approved work package.

## Status at a glance

| Track | Status | Current conclusion |
|---|---|---|
| Topic scope | Complete | Mother question is the transition from latent posterior estimation to downstream policy use |
| Behavioral G0 | Passed | Qwen2.5 shows the anchor formation/use/execution dissociation; Qwen3 and Gemma provide contrasting phenotypes |
| Mechanism design V1 | Complete | Formation, routing, comparator, and binding are competing explanations |
| Mechanism Phase 0 | Complete, exploratory | Expanded factorial preserves a substantial Qwen2.5 direct/bridge gap but exposes mapping sensitivity |
| Representation probes | Complete, exploratory | Literal serialized values and direct-task variables are decodable; abstract posterior identity is not established |
| Natural source interventions | Complete, exploratory | Whole serialized-number replacement is sufficient in bridge; final-token replacement is insufficient |
| Source-site layer trajectory | Complete, exploratory | Whole-span swap efficacy decays over layers 16–24 and is near zero after layer 25 |
| Receiver/path localization | Not started | Transport remains a hypothesis |
| Direct mechanism diagnosis | Not started | Formation versus routing versus comparator/binding remains unresolved |
| Selective repair | Not started | Reader-gated low-rank repair is a mechanism prediction only |
| Confirmatory D2-ID / D2-OOD / external transfer | Not started | All current white-box evidence remains D0 discovery |

## Milestone history

### M0 — Topic registration

**Status:** complete
**Commit:** `d66ed4f` — `Register 006 Bayesian latent inference-use gap`

The initial question was registered as:

> Why can a model report a sufficiently accurate posterior over a latent state, yet fail to apply that posterior to a minimal downstream policy?

The intended width was fixed early: one transition from belief to use, not a general theory of Bayesian reasoning.

### M1 — Minimal G0 scaffold

**Status:** complete, superseded
**Commit:** `5ddef7f` — `Add minimal G0 scaffold for 006`

The first scaffold established closed-form Bayesian cases and direct versus posterior-bridged policy prompts. Review found two invalid shortcuts:

1. a posterior estimate could be counted “good” even when its error crossed the policy threshold;
2. raw semantic answer candidates such as `INVEST/HOLD` could introduce lexical priors.

Decision: do not interpret the first scaffold; correct eligibility and surface-label scoring before any model judgment.

### M2 — Corrected behavioral G0

**Status:** passed
**Commit:** `1fe732c` — `Validate and refine G0 designs for projects 006-008`
**Artifacts:** `g0.py`, `tests/test_006_g0.py`, original `results/*_g0*`

Corrections:

- normalized likelihood over all `0.00…1.00` posterior continuations;
- inference-good only when the model’s reported posterior implies the correct action;
- threshold-boundary exclusions;
- minimal `posterior > threshold` policy;
- semantic ACT/WAIT counterbalanced over A/B labels;
- full candidate continuation scoring.

Headline G0:

| Model | Posterior MAE | Eligible | Direct error | Bridge error | Rescue |
|---|---:|---:|---:|---:|---:|
| Qwen2.5-14B-Instruct | `.105` | 42 | `33.3%` | `0%` | `14/14` |
| Gemma3-12B-IT | `.255` | 29 | `3.4%` | `0%` | `1/1` |
| Qwen3-8B | `.253` | 14 | `50.0%` | `42.9%` | `2/7` |

Decision: advance Qwen2.5 as the full-depth anchor. Retain Qwen3 as a posterior-estimation/report-poor behavioral contrast and Gemma as an action-good/bridge-sensitive contrast. Do not infer either internal formation failure or routing from behavior alone.

### M3 — Logic audit and narrative correction

**Status:** complete
**Artifact:** corrected project `README.md`

The bridge interpretation was narrowed:

- safe: the model can execute the comparison when a posterior is supplied;
- unsafe: bridge rescue by itself proves the direct model formed and failed to route the same posterior.

Formation, routing/alignment, comparator failure, and late A/B binding were retained as competing explanations.

### M4 — Mechanism Plan V1

**Status:** complete
**Artifact:** `INTERPRETABILITY_PLAN.md`

V1 defined:

- a causal abstraction from evidence to posterior, threshold, margin, semantic action, and mapping;
- behavioral refreeze before white-box work;
- named-position residual caches and grouped probes;
- natural activation interchange before subspace methods;
- exact component/path confirmation after attribution screening;
- selective rescue and one BayesBench transfer.

V1 remains the record of the original hypothesis space. V2 supersedes its execution order after observing D0 results.

### M5 — Mechanism Phase 0 refreeze

**Status:** complete, D0 exploratory
**Artifacts:** `mechanism/configs/phase0_behavior.json`, `mechanism/results/qwen25_14b_phase0_*`

New corpus:

- exact symmetric `0.8/0.2` family;
- priors `.2/.5/.8`, count differences `-2…2`, thresholds `.3/.5/.7`;
- 42 non-boundary cases, balanced 21 ACT / 21 WAIT;
- 16 surface variants and six belief conditions;
- 4,032 action rows over 15 unique evidence states.

Qwen2.5 results:

- posterior mean/argmax MAE `.1306/.1441`;
- direct accuracy `.570`;
- gold bridge `.932`;
- self-mean condition accuracy `.896`;
- self-argmax condition accuracy `.933`;
- counterfactual follow `.897`.

Important warning: aggregate mapping consistency is only `.551`. The selected ACT/WAIT + greater-than + high-first anchor is cleaner (`.738` mapping consistency; `36.7%` direct error; 22/22 gold and self bridge rescue), but this selection is discovery-only.

### M6 — Activation cache and representation timeline

**Status:** complete, D0 exploratory
**Artifacts:** `mechanism/src/activation_cache.py`, `probe_timeline.py`, `belief_span_cache.py`, `probe_belief_span.py`

Implemented named semantic anchors, BF16 residual caching, grouped ridge/logistic probes, and eight-token span pooling.

Observed:

- late direct query states strongly decode the task posterior/margin;
- bridge→direct probes on the same matched cases preserve rank but not calibration;
- pooled states decode serialized numeric values strongly;
- a final-token probe is inadequate for arbitrary six-digit self estimates.

Limitations recorded after audit:

- direct probes may reconstruct posterior from visible counts;
- bridge→direct analysis did not hold out evidence families;
- source-span rows repeat identical activations across later threshold/mapping variants;
- only 15 unique evidence states and a small set of numeric values exist;
- literal numeric decodability is not abstract posterior representation.

Decision: future probes require held-out evidence, values, formats, likelihood regimes, raw-token baselines, and dev-only layer selection.

### M7 — Numerical-intervention correction

**Status:** complete
**Artifacts:** corrected `mechanism/src/residual_interchange.py`

An initial interchange implementation exposed BF16 batch-shape drift and an FP16 cache conversion. The corrected implementation:

- preserves BF16 activations;
- captures receiver and donor states in one batch-local baseline forward;
- uses an identical padded batch for the patched forward;
- computes full A/B continuation likelihoods in semantic coordinates.

Invalidated outputs:

- `qwen25_14b_interchange_direct_query_shard*.jsonl` and its summary;
- old `qwen25_14b_activation_anchor.pt` FP16 cache.

They remain local, ignored, and excluded from every canonical summary.

### M8 — Single-position natural interchange

**Status:** complete, D0 exploratory negative result
**Canonical artifacts:** corrected `*_direct_local_*`, `*_gold_local_*`, and `*_gold_belief_*`

Across all layers, patches at the final query position did not transfer donor action in direct or gold bridge. A patch at the final posterior digit was also null. Coarse direct scans at evidence/rule/threshold/mapping end positions found no stable directionally aligned window.

Decision: reject final-digit/query-end carrier accounts at the tested sites. Do not infer that no other individual digit is sufficient, or that a multi-position state is necessarily distributed.

### M9 — Whole serialized-number intervention

**Status:** complete, D0 exploratory positive result
**Artifacts:** primary span shards and `qwen25_14b_phase2_span_summary.json`

At post-layer 0, 12 crossing pairs produced:

- gold number span: recovery `.9809`, pair-bootstrap CI `[.9441, 1.0141]`, IIA `12/12`;
- gold full belief statement: recovery `.9834`, IIA `12/12`;
- self-mean number span: recovery `.9808`, IIA `12/12`;
- gold same-posterior effect `0.29` versus crossing effect `49.64` semantic-logit units.

The whole-span effect remains near complete through layer 15, decays over 16–24, and is approximately zero after layer 25.

Safe conclusion:

> In the selected explicit-belief bridge surface, early-layer replacement of the complete serialized number is sufficient to transfer semantic action; source-site replacement efficacy decays over layers 16–24 while the literal value remains decodable there.

Not yet supported:

- that every token contributes or the representation is distributed;
- that a receiver/path has been found;
- that the code is format-invariant or abstract;
- that this mechanism explains direct errors.

### M10 — Independent result audit and evidence freeze

**Status:** complete
**Artifacts:** `mechanism/MECHANISM_LOG.md`, `mechanism/CLAIM_EVIDENCE_LEDGER.md`, `mechanism/results/README.md`

The audit verified headline numbers and identified the following required corrections:

- call layers 16–24 a source-site decay window, not a handoff;
- call whole-span replacement sufficient and last-token replacement insufficient, not “distributed over eight tokens”;
- treat current probe maxima as literal-value exploratory results;
- disclose shared donors, baseline-correct selection, and pair rather than family bootstrap;
- distance-match crossing and same-action controls;
- topology-match posterior-role and irrelevant-role prompts;
- report effective unique evidence/value counts;
- separate invalidated and canonical output versions.

These corrections are now reflected across the log, ledger, result index, and V2 plan.

### M11 — Plan V2

**Status:** written and frozen; no V2 experiment run
**Artifact:** `INTERPRETABILITY_PLAN_V2.md`

V2 learns from Hamdi’s research loop without presupposing his reader–writer answer:

```text
anomalous source decay with rising decodability
→ role-gated transport hypothesis
→ subspan/content-role/receiver/path tests
→ direct formation-vs-routing diagnosis
→ mechanism-predicted gated repair
→ low-rank method only if natural path geometry predicts it
```

All present data are permanently D0 discovery. The next run cannot begin until D1, D2-ID, and one-factor D2-OOD causal-family splits, fixed-topology controls, manifests, and automatic report schemas are frozen.

## Current claim boundary

The project has established an externalized-source sufficiency phenomenon. It has not yet explained the original direct use gap.

The next decisive binary question is:

> Does the direct computation contain a posterior representation that generalizes across values, formats, and evidence decompositions, but has weaker causal gain into the semantic-action writer than the matched bridge computation?

Possible answers remain formation failure, role-gated transport, coordinate mismatch, comparator failure, or late binding failure. V2 is designed so each outcome yields a different evidence-backed narrative rather than a threshold-based forced kill.

## Next approved milestone

**M12 — V2 data/control freeze** is pending. It contains no white-box model run:

1. generate and checksum D1, D2-ID, and one-factor D2-OOD causal families;
2. fix the identical-topology content × role factorial;
3. register the eight-position/prefix/suffix/leave-one-out intervention lattice;
4. freeze distance-matched crossing/non-crossing donors;
5. define effective sample units and family-clustered inference;
6. create run manifests and automatic result tables;
7. review the freeze before any GPU experiment.

## Document map

- `README.md` — concise topic and G0 status;
- `PROGRESS.md` — this chronological record;
- `INTERPRETABILITY_PLAN.md` — original complete mechanism design;
- `INTERPRETABILITY_PLAN_V2.md` — result-driven next plan;
- `mechanism/MECHANISM_LOG.md` — detailed D0 result interpretation;
- `mechanism/CLAIM_EVIDENCE_LEDGER.md` — claim-to-artifact status;
- `mechanism/results/README.md` — canonical, local-only, and invalidated result index.

## Update rule

After every future milestone, append:

- date and Git commit;
- question tested;
- split and model revision;
- exact config/raw/summary artifacts;
- result including nulls;
- interpretation change;
- claim-ledger updates;
- next permitted decision.

No historical result is silently rewritten. Corrections are recorded as superseding decisions.
