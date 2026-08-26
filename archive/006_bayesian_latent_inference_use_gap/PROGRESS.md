# 006 project progress

**Last updated:** 2026-08-27
**Current phase:** `KILLED / ARCHIVED`
**Anchor model:** `Qwen/Qwen2.5-14B-Instruct`

This is the chronological project record. It connects the original topic, behavioral validation, code corrections, mechanism experiments, invalidated interpretations, current evidence, and the next approved work package.

## Status at a glance

| Track | Status | Current conclusion |
|---|---|---|
| Topic scope | At risk | BayesBench already makes the broad latent-inference/downstream-prediction gap claim |
| Behavioral G0 | Synthetic development result only | Qwen2.5 has an anchor phenotype, but Qwen3/Gemma differ and prompt/label artifacts are not excluded |
| Mechanism design V1 | Complete | Formation, routing, comparator, and binding are competing explanations |
| Mechanism Phase 0 | Complete, exploratory | Expanded factorial preserves a substantial Qwen2.5 direct/bridge gap but exposes mapping sensitivity |
| Representation probes | Complete, exploratory | Literal serialized values and direct-task variables are decodable; abstract posterior identity is not established |
| Natural source interventions | Complete, exploratory | Whole serialized-number replacement is sufficient in bridge; final-token replacement is insufficient |
| Source-site layer trajectory | Complete, exploratory | Whole-span swap efficacy decays over layers 16–24 and is near zero after layer 25 |
| Receiver/path localization | Not started | Transport remains a hypothesis |
| Direct mechanism diagnosis | Not started | Formation versus routing versus comparator/binding remains unresolved |
| Selective repair | Not started | Reader-gated low-rank repair is a mechanism prediction only |
| Confirmatory D2-ID / D2-OOD | Paused | Do not spend more compute before official-benchmark transfer |
| Official external transfer | Required next | Reproduce with unmodified BayesBench code on public-data environments or archive 006 |

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

**Status:** passed as a synthetic development check; demoted after external-validity audit
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

Historical decision: advance Qwen2.5 as the full-depth anchor. This decision is no longer sufficient for paper-level work because the other models do not reproduce the phenotype and all cases were custom-generated. Do not infer either internal formation failure or routing from behavior alone.

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

### M12 — V2 data and control freeze

**Status:** complete; retained but not approved for execution
**Commits:** `5d1aa41`, `6f36e5c`, `4f94a16`

The planned D1/D2 datasets, distance-matched donor controls, intervention lattice, manifests, checksums, and report schemas were generated and frozen. This improves reproducibility but does not repair the external-validity problem: every V2 case is still derived from our custom task. These artifacts are preserved as development infrastructure and must not be run as the next scientific milestone.

### M13 — Generality and external-validity audit

**Status:** failed current evidence standard; project paused
**Date:** 2026-08-27

The attempted meta-G0 does not rescue generality. Qwen3-8B collapsed to one answer label across the action rows, while Gemma had weak mapping consistency; these are prompt/evaluation preflight failures, not interpretable evidence for or against report/use dissociation. The Qwen2.5-7B smoke was stopped before completion. No meta-G0 result may be cited as scientific evidence.

The audit changed two conclusions:

1. the custom closed-form corpus is a mechanism sandbox, not an external validation dataset;
2. BayesBench already reports across seven 3B–70B models that improved latent inference does not reliably carry over to downstream prediction, using public MovieLens, AITA, and medical-triage sources as well as a synthetic coin environment.

The broad behavioral narrative is therefore neither established by our data nor clearly novel. The only defensible salvage is a mechanism-and-repair extension anchored entirely in an official BayesBench reproduction. New V2 mechanism runs are suspended until an unmodified official-task transfer passes on at least two public-data environments and more than one open-weight model/model size. Failure triggers archival without threshold or prompt rescue.

## Current claim boundary

The project has established an externalized-source sufficiency effect inside one custom Qwen2.5 prompt family. It has not established a general behavioral phenomenon, external validity, or an explanation of the original direct use gap.

The next decisive binary question is:

> Does the direct computation contain a posterior representation that generalizes across values, formats, and evidence decompositions, but has weaker causal gain into the semantic-action writer than the matched bridge computation?

Possible answers remain formation failure, role-gated transport, coordinate mismatch, comparator failure, or late binding failure. V2 is designed so each outcome yields a different evidence-backed narrative rather than a threshold-based forced kill.

## Next approved milestone

**M14 — proposed official-benchmark transfer smoke (cancelled on archival)** superseded the previous V2 execution plan but was not run:

1. use the upstream BayesBench revision and its unmodified evaluation code;
2. run public-data MovieLens recommender and medical-triage smoke subsets;
3. test at least Qwen2.5-14B and one non-Qwen family before any full run;
4. predeclare the inference and downstream-use metrics from upstream outputs;
5. archive 006 if the same phenotype is not present across two environments and more than one model/model size;
6. only after a pass, redesign the mechanism experiment around the official task rather than retrofitting the custom corpus.

The already-frozen V2 data and controls remain reproducibility artifacts, not an approved run queue.

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
