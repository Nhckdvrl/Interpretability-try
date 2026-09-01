# 044 — A Property of the Person, or Only of This Stage? Stage-Level vs Individual-Level Predication in LLMs

Status: **STRICT-PASS-REGISTER / GPU AUTHORIZED**  
Date: 2026-09-01  
Route: **B/C — mature semantic distinction + simple context-conditioned latent object**  
Protocol: `FINDING_RULES.md` v2.1 + `STRICT_EXTENSION_GATE_2026-09-01.md`

## A. Frozen natural question

> **When a property is true of someone, does an LLM know whether it characterizes the individual as such, or only a particular temporal/situational stage of that individual?**

Classic semantic distinction:

- **individual-level (IL) predication** — characterizes an individual without anchoring the property to one particular spatiotemporal stage;
- **stage-level (SL) predication** — applies to a particular stage/situation of the individual and carries a spatiotemporal/event-like dependence.

Examples often used for intuition:

```text
John is intelligent.  # individual-level
John is drunk.        # stage-level
```

But 044 is explicitly **not** a `permanent vs temporary adjective` classifier.

---

## B. Why “temporary vs permanent” is an invalid shortcut

The stage/individual distinction is semantically and grammatically richer than duration.

Reference literature already notes that the distinction is not hard-and-fast in duration: a person can be sober for life while `sober` remains stage-like; a property normally associated with an individual may be contextually coerced into a stage reading.

More decisive counterexamples exist in Spanish/copular systems:

- permanent-looking `dead` can occur with the stage-associated copula `estar`;
- temporary nominal properties such as `queen for a day` can occur with `ser`;
- the same adjective can change interpretation according to copula/context.

Recent theoretical work in *Language* explicitly argues that the prevailing characterization in terms of transitory versus inherent/unchangeable properties must be reconsidered.

Thus a direction that merely predicts real-world duration is not the 044 object.

---

## C. Same-lexical context shift

Spanish supplies an important independent calibration:

```text
Julia es feliz.       # roughly: Julia is a happy person / characterizing reading
Julia está feliz.     # roughly: Julia is happy in the relevant current situation
```

Modern ser/estar semantics describes `estar` predication as depending on a topical situation, while `ser` need not be linked to one. The same adjective can therefore receive IL-like versus SL-like construals.

English can provide a **context-only held-out transfer** where the critical sentence is identical:

```text
Trait context: across years and many settings Maya is consistently cheerful...
Critical: Maya is happy.

Stage context: Maya has just received unexpected good news...
Critical: Maya is happy.
```

The critical lexical predicate is fixed; context changes whether the property is construed as characterizing Maya or her current stage.

This same-lexical shift is mandatory. Pure adjective-list classification is insufficient.

---

## D. Strongest computational-neural audit — N0 / N1 / N2

### D1 — formal and corpus computational work exists

Older corpus-based aspect work, including Xiao & McEnery, explicitly distinguishes individual-level states from stage-level states as lexical/sentential situation-aspect classes.

Therefore 044 may not claim novelty as:

> `computational linguistics has never represented stage-level vs individual-level states`.

The distinction is old and has been operationalized in corpus semantics.

### D2 — no direct neural/LLM object ownership found in the hard search

Targeted searches across BERT, Transformer, neural language model, ser/estar probing and stage/individual predicate terminology did not uncover work that causally studies an abstract context-conditioned IL/SL predication state in pretrained neural LMs.

This is an **absence after targeted search, not proof of global nonexistence**; discovery of a direct collision remains a fatal novelty condition.

### D3 — related neural work is not enough

Neural work on tense/aspect, event/state semantics, habituality and genericity is nearby. Earlier failure memory also kills generic habitual-vs-episodic as a fresh object.

044 survives only because it asks a different semantic level:

> **does a true property predicate attach to the individual-as-such or to a spatiotemporally anchored stage, including context-induced shifts of the same lexical predicate?**

If the project becomes `temporary vs habitual`, `event vs state`, or adjective duration, kill N2.

### D4 — exact N2 delta

> **A cross-lingual/cross-context predication-level state that transfers across the same adjectives and causally controls independent stage-sensitive consequences while preserving the underlying property judgment.**

---

## E. Strict Extension Gate

### Lock A — same-lexical / anti-duration identifiability: PASS

Mandatory cells include:

1. same adjective with context/copula-induced IL vs SL reading;
2. `permanent-but-stage` counterexamples;
3. `temporary-but-individual/ser` counterexamples;
4. duration-matched predicate pairs.

A duration-only model must fail these cells.

### Lock B — cross-setting abstraction: PASS

Required transfer across at least:

- Spanish ser/estar same-adjective calibration;
- English context-induced same-critical-sentence shift;
- held-out adjective/predicate families;
- optional nominal predicates / another language if theory-valid materials are available.

Discovery in Spanish may not be called abstract unless it transfers beyond the copula tokens.

### Lock C — two independent theory-diagnostic consequences: PASS

At least two diagnostics are frozen:

1. **TopicalSituationDependence** — whether the predication is tied to a particular time/situation and supports a situation-specific continuation;
2. **StageDiagnosticCompatibility** — compatibility with a second established stage-sensitive construction, selected before MI from formal literature (e.g. a temporal/depictive/existential/perception diagnostic with clean materials).

Temporal persistence can be reported as a behavioral consequence but cannot alone define the distinction.

The same causal state must affect two independently grounded diagnostics.

---

## F. Substrate

### F1 — external theory and natural-language materials

Use established ser/estar and IL/SL examples from formal/experimental literature, prioritizing same-adjective alternations and counterexamples to duration.

### F2 — controlled context-shift microscope

Construct matched discourse pairs where the final predication is identical and only preceding context establishes:

```text
INDIVIDUAL-AS-SUCH interpretation
vs
CURRENT-STAGE interpretation
```

Example classes include happiness, bravery, generosity, quietness and other adjectives that have independently attested context-sensitive readings.

Central labels come from pre-established semantic manipulations, not an LLM judge.

### F3 — anti-duration test set

Freeze a separate set where real-world expected duration and predication level point in opposite directions. This set is never used to choose a representation layer/direction.

---

## G. Frozen S0

Primary models:

- `meta-llama/Llama-3.1-8B-Instruct`
- `Qwen/Qwen3-8B`

### S0-1 — property comprehension

Verify `PropertyTruthLogit`: the model understands that the relevant property is asserted true of the subject in both matched readings.

### S0-2 — two diagnostic consequences

Define deterministic forced-choice/logit readouts from theory-grounded continuations:

```text
SituationBoundLogit
StageDiagnosticLogit
```

The same lexical predicate should shift both when context changes its predication level.

### S0-3 — anti-duration control

A simple duration predictor must not explain the full pattern. In particular, permanent-stage and temporary-individual counterexamples must retain the theory-predicted signature.

### S0-4 — cross-language/surface generalization

A model family counts only if the qualitative predication-level effect is recoverable across at least two prespecified realization families rather than only `ser` vs `estar` tokens.

---

## H. Frozen causal-use contract

### H1 — estimate `PredicationLevel`

Estimate an IL↔SL state/subspace from balanced training materials with:

- adjective identity crossed with role where possible;
- duration expectations balanced/residualized;
- copula identity not sufficient to solve held-out English transfer;
- noun/person identity balanced;
- train/test lexical families disjoint.

### H2 — first causal consequence

On held-out same-sentence context pairs:

```text
steer toward STAGE
→ increase situation-bound/current-stage continuation preference

steer toward INDIVIDUAL
→ increase individual-characterizing continuation preference
```

while preserving:

```text
PropertyTruthLogit
```

### H3 — independent second consequence

The same intervention must shift a second theory-grounded stage diagnostic in the expected direction. A result on only one readout does not identify `PredicationLevel` under the stricter gate.

### H4 — mandatory controls

- lexical adjective identity;
- `ser` vs `estar` token direction;
- explicit temporal adverb direction;
- estimated real-world duration;
- event-vs-state/aspect direction;
- random/shuffled subspaces;
- subject identity/recency.

The abstract claim requires held-out English/context transfer from any Spanish/cross-lingual calibration.

---

## I. Story invariance

### Result A — abstract stage/individual state

The model represents predication level separately from property truth/duration and causally reuses it across language/context to control multiple stage-sensitive consequences.

### Result B — language-specific implementation

Spanish ser/estar behavior is robust but fails context-only transfer; the model relies mainly on morphosyntactic lexicalization rather than a reusable predication-level state.

### Result C — duration/aspect heuristic

Apparent IL/SL competence collapses under anti-duration controls or is explained by generic tense/aspect states; no distinct predication-level state survives.

All results answer the same question.

---

## J. Hard kills

1. New neural/LLM direct collision on context-conditioned IL/SL causal representation -> `KILL-NOVELTY`.
2. Result is just temporary vs permanent -> `KILL-IDENTIFIABILITY`.
3. Result is just `ser` vs `estar` token/syntax -> `KILL-LEXICAL-CUE`.
4. No same-adjective/context-induced transfer -> no abstract state claim.
5. Only one theory diagnostic can be causally affected -> `KILL-IDENTIFIABILITY` under strict Lock C.
6. Intervention destroys `PropertyTruthLogit` -> no predication-specific causal claim.
7. Effect collapses into already-occupied generic habitual/episodic or generic aspect classification -> `KILL-N2`.
8. Probe/best-layer only -> `KILL-SCALE`.

---

## K. Venue-scale comparison

- **EMNLP 2025 Outstanding filler-gap:** causal transfer across constructions is the standard for an abstract linguistic state.
- **ACL 2026 Tool Irrelevance:** two nearby factors are separated with causal specificity and preservation controls.
- **NAACL 2025 theory-driven property inference:** external cognitive/semantic distinctions remain headline objects under multiple possible model outcomes.
- **2026 Language stage/individual theory:** the object remains scientifically active and explicitly resists a simplistic transitory/inherent definition, motivating the anti-duration controls.

---

## L. Strict registration verdict

```yaml
base_FINDING_RULES_v2_1: PASS
new_orthogonal_object_or_axis: PASS
old_corpus_semantic_ownership: ACKNOWLEDGED
old_neural_exact_object_ownership: CLEAR_IN_TARGETED_SEARCH
recent_LLM_exact_object_ownership: CLEAR_IN_TARGETED_SEARCH
external_semantic_substrate: PASS
Lock_A_same_lexical_anti_duration: PASS
Lock_B_cross_setting_abstraction: PASS
Lock_C_two_diagnostics: PASS
specificity_denominator: PropertyTruthLogit
central_confound: temporary_vs_permanent_or_ser_vs_estar
central_confound_identifiable: PASS_WITH_HARD_KILLS
behavior_lottery: false
verdict: STRICT-PASS-REGISTER
GPU_AUTHORIZED: true
```

## One-line freeze

> **044 asks whether an LLM represents a property as characterizing the individual or only a particular spatiotemporal stage. It is not a temporary/permanent classifier: same-adjective context shifts, anti-duration counterexamples, cross-surface transfer, two independent stage diagnostics and preservation of property truth are mandatory.**
