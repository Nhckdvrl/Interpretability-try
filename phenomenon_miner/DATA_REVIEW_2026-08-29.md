# Data-first re-audit — 2026-08-29 evening

Status: `AUTHORITATIVE SUPPORTING REVIEW / CURRENT_TOPICS.md REMAINS THE QUEUE`

This review was triggered after the 014 dataset-scope failure made the selection problem explicit: novelty can be acceptable while the data path silently changes the scientific question. The purpose here is therefore not to generate more topics. It is to prune the current queue by asking whether each phenotype can be defined on a natural source population with hard gold **before** hidden-state evidence enters.

## Review rule

A topic stays in the current phenomenon queue only if all four are credible now:

1. **External phenotype first** — the new headline can be stated without naming a probe, neuron, head, representation, route, or causal patch.
2. **Natural source population** — there is a real source bank whose units instantiate the mother question; a synthetic mechanism control cannot serve as the only anchor.
3. **Hard or externally frozen gold** — the decisive label is deterministic, source-authored, or computable from reported quantities. Researcher intuition is not the gold.
4. **Low inferential distance** — the first D0 can be built with one main contrast and a small number of fatal controls. If the dataset requires many coupled assumptions, the topic is not ready.

`GREEN` means a concrete source path exists and should be audited next. `AMBER` means the scientific object is worth keeping but the source/gold linkage still needs manual feasibility work. `RED` means the current formulation should leave the phenomenon queue.

---

## Keep — phenomenon discovery

### 1. Mixed-Status Event Attraction — GREEN

**Phenotype:** event factuality is correct in isolation, but combining differently-statused events in the same discourse pulls one event toward the other's status.

**Primary source:** MAVEN-FACT (112,276 naturally occurring event mentions with factuality labels and supporting evidence for non-factual events), preserving the original document as the sampling unit.

**D0 recipe:**

- sample same-document event pairs with different gold factuality labels; never random-concatenate unrelated events;
- preserve the natural paragraph/sentence neighborhood and event IDs;
- require isolated recognition for both events before the joint condition is eligible;
- score directional attraction separately (`factual -> possible/impossible`, `nonfactual -> factual`) rather than pooling all labels;
- cluster inference by source document;
- retain event relation, distance, trigger type, polarity and modality as factors, not filters.

**Fatal data checks:** enough same-document mixed-status pairs after validity exclusions; no label leakage from an annotation-derived prompt; attraction must survive matched distance/order controls.

**Why it stays:** large natural bank, source-authored labels, same-discourse units, and a clean route to event-status representation/binding if the behavior exists.

### 2. Subgroup-Significance -> Interaction Promotion — GREEN/AMBER

**Phenotype:** one subgroup is statistically significant and another is not, while the interaction is not significant; the model nevertheless claims the treatment effect differs between subgroups.

**Primary source:** independent open-access randomized trials with explicit subgroup estimates and an explicit interaction test (`P for interaction`, interaction CI, or equivalent model coefficient). PubMed Central Open Access is the preferred source family.

**Gold:** `no sufficient evidence of subgroup-effect difference` when the frozen interaction test does not reject. This is **not** the stronger claim that subgroup effects are equal.

**D0 recipe:**

- 20+ independent trials, one endpoint/subgroup/timepoint unit per trial for the primary analysis;
- keep reported subgroup estimates, CIs/p-values and the interaction statistic; do not recreate them from prose if the paper reports them directly;
- require the tempting pattern `one subgroup significant / another not significant` while the interaction is non-significant;
- use exact trial provenance and a second-person audit of the extracted endpoint/subgroup/timepoint mapping;
- isolated controls ask the subgroup-specific conclusions and the interaction conclusion separately before the combined summary/action question.

**Fatal data checks:** if 20 independent open-access units with explicit interaction tests cannot be assembled without mixing endpoints/timepoints, move to HOLD-DATA.

**Why it stays:** the inferential error has a deterministic statistical oracle and a natural wrong destination; the mechanism can later distinguish thresholded subgroup-significance features from an interaction operator.

### 3. Stock-Flow Correlation Intrusion — GREEN/AMBER

**Phenotype:** the model correctly computes net flow but the predicted stock trajectory/peak still tracks a salient component flow, especially inflow.

**Natural sources already identified:**

- ResOpsUS: daily reservoir storage, inflow, outflow and evaporation across many U.S. reservoirs;
- official population-accounting time series (e.g. U.S. Census / Japan e-Stat) containing population stock plus births, deaths and migration components.

**D0 recipe:**

- use real time-series windows; the balance equation must be checkable from source quantities;
- first ask net-flow direction/amount, then ask stock direction/peak/time-to-peak;
- choose windows where inflow and net flow disagree in direction or peak timing so the wrong destination is diagnostic;
- use table/text rendering as the primary first shot; charts are a secondary modality factor, not the only source;
- cluster by reservoir/geography and report source family separately.

**Scope correction:** two independent natural source families are sufficient for D0 feasibility. A third domain is confirmatory, not a construction gate. Requiring three domains before the first behavioral shot would create avoidable source creep.

**Fatal data checks:** if source accounting does not close closely enough to provide a deterministic stock oracle, that source family is excluded for validity rather than corrected by hand.

**Why it stays:** strong natural mother phenomenon, deterministic dynamics, and data can stay external to the model rather than being invented as toy tanks.

### 4. Harmless-Error -> Remedy Collapse — GREEN/AMBER

**Phenotype:** the model correctly identifies a legal error and separately recognizes that the error was harmless/non-prejudicial, but still promotes the error into reversal/new-trial/remedy entitlement.

**Primary source:** public appellate opinions from CourtListener / public-domain U.S. case law. Candidate discovery can use exact phrases such as `harmless error`, `no prejudice`, `did not affect substantial rights`, combined with final dispositions such as `affirmed`.

**D0 recipe:**

- 20+ independent cases, preferably across circuits/case types;
- freeze three source spans per case: error finding, harmlessness/prejudice analysis, final disposition;
- gold comes from the court's disposition and harmlessness holding, not a researcher summary;
- isolated controls must establish that the model reads both the error and harmlessness correctly before the remedy question is eligible;
- do not pool constitutional and nonconstitutional harmless-error standards without a factor label.

**Fatal data checks:** if the final disposition depends on an independent reversible ground not represented in the chosen unit, the case is invalid for this contrast.

**Why it stays:** public natural text, externally authored role labels, and a clean `error finding != remedy entitlement` operator that is interpretable if a dissociation exists.

### 5. Noninferiority -> Equivalence Collapse — AMBER

**Phenotype:** a one-sided noninferiority result is read correctly but downstream language/action is symmetrized into equivalence.

**Primary source:** open-access noninferiority RCT reports with an explicit NI margin and reported CI for the treatment contrast.

**Gold:** compute the directional NI relation from the frozen margin/CI. Do not use authors' loose prose as the oracle, because papers sometimes use `equivalent/similar` imprecisely.

**D0 recipe:** 20+ independent trials; exact design/result provenance; isolated NI recognition; downstream questions that distinguish `not worse than margin` from `within a two-sided equivalence band` and from `no difference`.

**Fatal data checks:** if the NI margin or effect orientation cannot be unambiguously recovered, exclude the trial for measurement validity.

**Why it stays:** good scientific distinction and hard statistical gold are possible, but extraction burden is higher than the four topics above.

### 6. Surrogate -> Clinical-Outcome Promotion — AMBER

**Phenotype:** the model correctly identifies a measured surrogate/biomarker improvement and its regulatory/context status, yet promotes it into a claim of patient-centered clinical benefit that the evidence does not license.

**Primary sources:** FDA public surrogate-endpoint table + exact trial/approval documents for the same population, endpoint and context of use.

**D0 recipe:** create tuples `(trial result, surrogate endpoint, population/context, regulatory status, target clinical-outcome claim)` with source IDs on every link. At least 20 independently linked tuples are required.

**Fatal data checks:** do not label all surrogate endpoints as invalid clinical evidence. The gold must respect validated surrogate/context-of-use distinctions and approval type.

**Why it stays:** strong natural gate and authoritative public metadata, but source linking is expensive; it remains behind the GREEN topics until 20 exact tuples are demonstrated.

### 7. Dissent -> Holding Role Swap — AMBER

**Phenotype:** a proposition from a dissent is locally understood but is promoted into the controlling rule/holding when majority and dissent are jointly summarized.

**Primary source:** U.S. Supreme Court / appellate opinions with explicit opinion-role metadata. Prefer cases with a source-authored syllabus or clear `Held:` language for the controlling proposition; SCOTUS/CourtListener text and SCDB-style vote/opinion metadata can support role verification.

**D0 recipe:** 20+ independent cases where majority and dissent make genuinely conflicting propositions on the same issue; retain exact quoted/source spans and role metadata. The holding must be source-grounded, not researcher-authored.

**Fatal data checks:** if a case requires the researcher to infer the holding from a long opinion without an external anchor, it does not enter D0.

**Why it stays:** natural authority-role binding with interpretable wrong destination, but proposition-pair extraction remains manual.

---

## Move out of the phenomenon queue

### Task-Switch TR/TL Desynchronization — ROUTE -> MECH-FOLLOWUP

The mother task-switch paper already establishes the external behavior. The current headline (`TR switched, TL did not`, or vice versa) is defined in terms of an internal decomposition. The public mother repo makes task-switch data easy, but **easy data does not turn a hidden-state question into a new phenotype**.

It can return to phenomenon discovery only if a pre-hidden-state wrong-destination signature is frozen first, e.g. a systematic old-task mapping intrusion that can be scored from outputs alone under a counterbalanced mapping design.

### Resolved-Ambiguity Neuron Persistence — ROUTE -> MECH-FOLLOWUP

AmbigQA/AmbigNQ provides excellent ambiguous questions and semi-oracle evidence, so source availability is not the problem. The current headline, however, asks what ambiguity neurons encode after resolution. That is a mechanism lifecycle question.

A future phenotype candidate would need an external `resolution lag` first: after a natural context uniquely fixes the intended interpretation and the model can state that interpretation, it still clarifies/hedges/answers multiple senses. Until such behavior is shown, keep this as a mother-paper mechanism follow-up.

### Action-Boundary State Routing — ROUTE -> MECH-FOLLOWUP

Already correctly identified as a mechanism follow-up: mother behavior exists; the question is whether EBP reads or creates a boundary state.

### Predicate-Revision Eager-Flag Staleness — ROUTE/HOLD-DATA

The interesting object is an implementation switch in the filter-head mother paper. The currently proposed D0 relies on constructed list/predicate-revision conversations and does not yet have a natural behavioral source. Do not keep it in the phenomenon queue just because the eager-flag/late-filter fork is elegant.

### Training-Recency Conflict Arbitration — ROUTE/HOLD-DATA

The current question is `metadata causal?` and the required exposure-balanced conflict set is not naturally observable at sufficient precision. This is exactly the kind of hidden-state-first identification problem that the `candidate_topics` archive warns about.

### Correlation -> Agreement / Interchangeability Promotion — HOLD-DATA

The statistical distinction is real, but `interchangeable` requires a domain-specific acceptable-difference margin or an equivalent external agreement standard. High correlation + wide Bland-Altman limits alone does not create a universal hard gold. Without 20+ units with source-declared agreement criteria or paired raw data plus predeclared margins, keep this out of the live queue.

### Habitual -> Episode Actualization — HOLD-DATA

Natural habitual/generic corpora exist, but the downstream dated-event gold is not directly annotated. Constructing a date query can itself induce the pragmatic inference under study. Until a source provides independently annotated habitual/generic status plus episode actuality, this is not a clean D0.

### Competing-Event -> Censoring Collapse — HOLD-DATA/CAPABILITY-RISK

The operator has a deterministic statistical meaning, but the current data path is either specialist-methodology text or a constructed survival-analysis exercise. Before re-entering the queue it needs a natural source population where event type and risk-set transition are both source-grounded, plus evidence that the model has the base competing-risk/censoring competence.

### Publicness-Coordination Dissociation (legacy 013) — PARKED-HOLD-DATA

N0 remains interesting, but the existing audit already established that the accessible human paradigm does not yield 20 independent natural matched scenarios under a clean adaptation/license path. Do not count participant swaps, paraphrases or payoff variants as new units. Keep the project files as provenance, but remove it from near-term discovery scheduling unless a genuinely new source family appears.

---

## Active 014 Alias Entrainment Transfer — keep the phenotype, simplify the decision

014 is not a new candidate. The cross-surface phenotype is already strong; the only unresolved issue is the **construct** behind it. The current evidence supports `learned cross-surface relation transfer`, not yet `entity-level salience`.

The r4 correction is directionally right: preserve the broad RedirectQA surface population and treat surface structure/type/direction as factors rather than filters. But the next step must remain data-first.

Before any new D1 model call:

1. materialize the broad r4 raw bank and publish the scope/attrition table;
2. run a source-only ASSOC coverage audit before spending more effort on model gates;
3. manually inspect random source units, random ASSOC matches, and the high-attrition strata;
4. explicitly estimate whether the hard identity/opaque stratum can plausibly support the preregistered 60-entity model gate;
5. if the source bank cannot support Q2 without another cascade of convenience filters, **drop the entity/reference-specific claim** and keep the result as cross-surface learned-relation entrainment rather than narrowing the population again.

No phase-4 mechanism story is allowed to rescue a failed D1 construct.

---

## Terminal/stale status correction

`007_weak_evidence_backfire` already has a merged smoke verdict: **HARD KILL**. Qwen3-8B produced no recognition-gated denominator; Gemma3-12B-IT produced one gated pair with the opposite sign and failed the survival controls. It must no longer be shown as `READY-TO-SMOKE` or authorized.

The raw results remain valuable failure evidence; terminal status is not a reason to delete provenance.

---

## Scheduling after this review

Recommended discovery order by expected information gained per unit data effort:

1. Mixed-Status Event Attraction
2. Subgroup-Significance -> Interaction Promotion
3. Stock-Flow Correlation Intrusion
4. Harmless-Error -> Remedy Collapse
5. Noninferiority -> Equivalence Collapse
6. Surrogate -> Clinical-Outcome Promotion
7. Dissent -> Holding Role Swap

The first four are the only topics that should receive near-term D0 construction effort. The last three first need a 20-unit manual source-yield audit. Mechanism follow-ups remain useful research ideas, but they do not compete with these seven for phenomenon-discovery slots.
