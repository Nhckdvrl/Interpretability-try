# 044 — A Property of the Person, or Only of This Stage? Stage-Level vs Individual-Level Predication

Status: **STRICT-PASS-REGISTER / GPU AUTHORIZED / HARD RE-AUDIT PASSED**  
Date: 2026-09-01  
Route: **B/C — mature semantic distinction + context-conditioned latent object**  
Protocol: `FINDING_RULES.md` v2.1 + `STRICT_EXTENSION_GATE_2026-09-01.md`

## A. Frozen natural question

> **When a property is true of someone, does an LLM know whether it characterizes the individual as such, or only a particular temporal/situational stage of that individual?**

- **individual-level (IL)**: characterizes the individual without requiring one particular spatiotemporal stage;
- **stage-level (SL)**: applies to a particular situation/stage and carries situation/event dependence.

044 is **not** a temporary-vs-permanent adjective classifier.

## B. Why duration is not the object

Theoretical work repeatedly warns that IL/SL cannot be reduced to `permanent vs temporary`.

Mandatory anti-shortcut examples include:

- long-lasting/permanent-looking properties that nevertheless receive stage-level treatment, including Spanish `estar muerto` (`dead`);
- temporary descriptions that can appear in individual-level/`ser` configurations, including `reina por un día` (`queen for a day`);
- same lexical adjective with IL-like vs SL-like construal according to copula/context.

Recent work on the stage/individual distinction explicitly argues that the traditional transitory-vs-inherent characterization is insufficient.

## C. Same-lexical shift

Spanish provides a calibration family:

```text
Julia es feliz.       # characterizing / IL-like
Julia está feliz.     # current-situation / SL-like
```

English provides the crucial held-out context-only family:

```text
Trait context: across years and settings Maya is consistently cheerful...
Critical: Maya is happy.

Stage context: Maya has just received unexpected good news...
Critical: Maya is happy.
```

The critical sentence and adjective are identical. An abstract claim requires transfer beyond the Spanish copula tokens.

## D. Strongest-neighbor audit

Older corpus/formal computational work already uses IL/SL situation-aspect classes. Neural work on tense/aspect, event/state representations and habituality is nearby, and generic habitual-vs-episodic topics are already terminal in the failure library.

Targeted searches across BERT/Transformer/LLM, `ser/estar`, and IL/SL terminology did **not** find prior neural work that causally factorizes a same-lexical context-conditioned IL/SL predication state and transfers it across realization families.

Thus novelty cannot be `we classify stage-level adjectives`; it is:

> **a context-conditioned predication-level state, distinct from duration/property truth/copula identity, that causally transfers across surfaces and jointly controls two independent stage-sensitive consequences.**

A newly found direct neural collision remains fatal.

## E. Strict extension locks

### Lock A — same lexical + anti-duration: PASS

Required:

1. same adjective in both readings;
2. permanent-but-stage counterexamples;
3. temporary-but-individual counterexamples;
4. duration-matched controls.

### Lock B — cross-setting abstraction: PASS

Mandatory transfer across:

- Spanish same-adjective `ser/estar` calibration;
- English context-only same-critical-sentence shift;
- held-out adjective families;
- held-out subject/domain families.

No abstract claim if only `ser` vs `estar` is learned.

### Lock C — TWO EXACT DIAGNOSTICS FROZEN: PASS

The previous README was too loose because it left the second diagnostic to be chosen later. That is now repaired.

#### Diagnostic 1 — SituationBoundLogit

Does the predication support a continuation explicitly tying the property to the current/relevant situation rather than characterizing the individual across situations?

#### Diagnostic 2 — DepictiveCompatibilityLogit

Use **depictive secondary predication** as the fixed independent grammatical diagnostic.

Classic formal literature treats depictive secondary predicates as strongly stage-level: clear SL predicates are naturally licensed as depictives, while clear IL predicates are degraded unless coerced to an SL reading.

Examples of the diagnostic family:

```text
John sat in the car drunk.          # clear stage-compatible depictive
?? John sat in the car French.      # clear IL predicate degraded as depictive
```

The causal test uses only **consensus-clear items / context-induced readings** whose depictive interpretation is independently justified. Known coercible/borderline cases are excluded by a preregistered linguistic rule, never by model performance.

If SituationBound and DepictiveCompatibility systematically dissociate, the unified `PredicationLevel` claim dies; we do not choose whichever metric works.

## F. Substrate

### F1 — theory-grounded natural calibration

Use published `ser/estar`, IL/SL and depictive examples/materials, prioritizing same-adjective alternations and anti-duration counterexamples.

### F2 — deterministic context-shift microscope

Construct matched discourse pairs with identical final predication and only preceding context changing the intended interpretation:

```text
INDIVIDUAL-AS-SUCH
vs
CURRENT/RELEVANT-STAGE
```

Central labels are defined from independently attested semantic manipulations.

### F3 — consensus-clear diagnostic inventory

Freeze before GPU:

- adjective/readings with independently attested IL↔SL context shift;
- anti-duration cases;
- depictive-compatible SL controls;
- depictive-degraded IL controls.

Borderline/coercion-sensitive items may be a later analysis, not central gold.

## G. Frozen S0

Primary models:

- `meta-llama/Llama-3.1-8B-Instruct`
- `Qwen/Qwen3-8B`

### G1 — preserve property comprehension

```text
PropertyTruthLogit
```

must confirm that the base property is understood as true in both matched readings.

### G2 — two diagnostic consequences

```text
SituationBoundLogit
DepictiveCompatibilityLogit
```

The same lexical predicate/context manipulation must shift both in the expected direction on consensus-clear items.

### G3 — anti-duration denominator

A duration-only predictor must fail the permanent-stage / temporary-individual counterexamples.

### G4 — cross-surface capability

A model family contributes to the claim only if the frozen qualitative effect survives at least Spanish morphosyntactic calibration and English context-only realization.

## H. Frozen causal-use contract

### H1 — estimate `PredicationLevel`

Estimate IL↔SL state/subspace while balancing/residualizing:

- adjective identity;
- `ser`/`estar` identity;
- explicit temporal adverbs;
- estimated real-world duration;
- subject identity;
- generic event-vs-state/aspect signals.

Discovery/test lexical and context families are disjoint.

### H2 — first consequence

```text
steer toward STAGE
→ increase SituationBoundLogit

steer toward INDIVIDUAL
→ increase individual-characterizing continuation preference
```

while preserving `PropertyTruthLogit`.

### H3 — fixed second consequence

The **same intervention** must shift `DepictiveCompatibilityLogit` in the corresponding direction on held-out consensus-clear examples.

No new second diagnostic can replace depictives after seeing results.

### H4 — mandatory controls

- adjective lexical direction;
- `ser` vs `estar` token direction;
- explicit temporal-adverb direction;
- estimated duration direction;
- tense/aspect/event-state direction;
- random and shuffled subspaces;
- subject/recency controls.

## I. Story invariance

- **A — shared predication-level state:** one state transfers across context/language and causally controls both diagnostics.
- **B — construction-specific implementation:** robust local behavior but no cross-setting shared causal state.
- **C — duration/aspect collapse:** apparent IL/SL behavior is explained by duration, copula or generic aspect features.
- **D — diagnostic dissociation:** situation-bound and depictive behavior rely on different states; unified IL/SL latent-object claim fails.

All outcomes answer the frozen scientific question.

## J. Hard kills

1. Direct neural/LLM causal IL/SL collision -> `KILL-NOVELTY`.
2. Temporary/permanent explains effect -> `KILL-IDENTIFIABILITY`.
3. `ser/estar` tokens explain effect -> `KILL-LEXICAL-CUE`.
4. No same-adjective English context transfer -> no abstract state claim.
5. Only one of the two frozen diagnostics responds causally -> `KILL-UNIFIED-OBJECT`.
6. Depictive result depends only on lexical adjective classes and fails context-induced reading transfer -> `KILL-IDENTIFIABILITY`.
7. Intervention damages `PropertyTruthLogit` -> `KILL-SPECIFICITY`.
8. Effect collapses into habitual/episodic or generic aspect -> `KILL-N2`.
9. Probe/best-layer only -> `KILL-SCALE`.

## K. Strict verdict

```yaml
base_v2_1: PASS
N0_N1_N2: PASS_AFTER_HARD_AUDIT
Lock_A_same_lexical_anti_duration: PASS
Lock_B_cross_setting: PASS
Lock_C_two_exact_diagnostics:
  - SituationBoundLogit
  - DepictiveCompatibilityLogit
  status: PASS
specificity_denominator: PropertyTruthLogit
central_shortcuts:
  - duration
  - ser_vs_estar
  - generic_aspect
identifiable_with_hard_kills: true
story_invariance: PASS
verdict: STRICT-PASS-REGISTER
GPU_AUTHORIZED: true
```

## One-line freeze

> **044 asks whether a property is represented as characterizing an individual or a particular stage. Same-adjective context shifts, anti-duration counterexamples, cross-surface transfer, and the two frozen consequences `SituationBoundLogit` + `DepictiveCompatibilityLogit` are mandatory; the same causal edit must move both while preserving property truth.**