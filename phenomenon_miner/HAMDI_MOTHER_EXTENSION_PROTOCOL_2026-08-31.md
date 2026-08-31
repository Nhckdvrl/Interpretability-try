# Hamdi Mother-Extension Protocol — 2026-08-31

Status: **AUTHORITATIVE IDEA-GENERATION PROTOCOL**

This file corrects a repeated failure in the continuation search: we kept saying “Hamdi-style” while still generating candidate phenomena from scratch and then gambling on whether a costly G0 would reveal the behavior. That is not the successful pattern visible in Hamdi's `#r_hamdi` work.

The governing idea-generation rule is now:

> **Do not invent a phenomenon and then look for a mother. Start from one concrete strong mother scientific object whose behavior/representation is already established, identify one adjacent real-world axis that the mother did not ask about, and inherit the mother's measurement recipe as far as possible.**

The target is not “a nearby topic.” It is an **omitted axis of an established object**.

---

## 1. What the two successful Hamdi examples actually did

### A. Entity knowledge → ontological status

Mother object: `Do I Know This Entity?` studies epistemic access / familiarity — whether the model knows an entity and has facts about it.

Omitted adjacent axis: **whether that entity is real or fictional**.

Why this is not a behavior lottery:

- `known/unknown` and `real/fictional` are different properties in the world;
- famous fictional entities and famous real entities provide natural cross-cells;
- the fictional class can be familiarity-matched, so the new axis is not rarity/unknownness;
- the mother already supplies a concrete representation-analysis recipe at the entity token.

The new paper therefore does not ask “maybe models confuse reality somehow?” It asks whether an already measured **entity representation** contains an additional ontological variable that the mother never tested.

### B. Biased arbitrary choice → random-choice state and distribution writer

Mother behavior: ordinary arbitrary-choice prompts (`pick a random digit`, `choose any color`, `flip a coin`) are already visibly and previously documented as non-uniform; prior work also already shows that behavioral calibration/fine-tuning can make the distribution more diffuse.

Omitted question: **does the model internally represent that the current task is an arbitrary/random choice, and is that state itself the thing that shapes output entropy?**

Why this is not a behavior lottery:

- the biased-choice behavior exists before the mechanism study;
- prior work already supplies a behavioral ceiling;
- the new question is about an internal state not previously asked by the behavioral correction papers;
- the intuitive single-variable story is then causally falsified: the readable choice-state is a switch, while a distinct downstream direction shapes entropy;
- that decomposition predicts a simple gated intervention.

The sequence is therefore:

```text
established behavior
→ unasked internal scientific question
→ causal analysis
→ intuitive story breaks
→ intervention falls out
```

not:

```text
plausible mechanism story
→ invent a benchmark
→ hope a behavior appears
```

---

## 2. Mandatory mother-extension card

No new idea is allowed into P0/S0 until this card is complete.

```yaml
mother_extension:
  mother_paper:
  mother_scientific_object:
  mother_established_result:
  mother_target_models_or_population:
  mother_measurement_recipe:

  omitted_axis_or_question:
  why_the_mother_did_not_already_answer_it:
  why_axis_exists_outside_the_model:
  one_natural_cross_cell_or_counterexample:

  inheritance:
    data_or_units_reused:
    scorer_or_readout_reused:
    intervention_or_control_recipe_reused:

  behavior_lottery:
    requires_guessing_a_new_failure_exists: true|false
    requires_expensive_multifamily_g0_before_we_even_know_there_is_a_question: true|false
    evidence_that_the_base_object_already_exists:

  title_test:
    new_question_in_one_sentence:
    mother_title_cannot_already_answer_it: true|false

verdict: PASS-TO-NEGATIVE-MEMORY | REJECT
```

Immediate REJECT if either behavior-lottery field is `true`, unless the topic is a pure factorization/object extension whose two axes already exist independently with natural cross-cells and the mother recipe directly measures the same object.

---

## 3. The extension must be lateral, not a mechanism follow-up

Bad:

```text
mother shows failure X
→ where is X represented?
→ which head causes X?
→ can steering fix X?
```

This is mother-behavior → mechanism and is not a new scientific object.

Good:

```text
mother measures property A of object O
→ property B of the SAME object O is naturally distinct and omitted
→ A/B have natural cross-cells independent of the model
→ use mother's recipe to ask whether O carries B as well
```

or:

```text
mother establishes behavior X robustly
→ prior work fixes X behaviorally
→ ask an unasked internal state/computation question whose answer is not implied by X
→ causal result must distinguish competing mechanisms and ideally predict a new intervention
```

The same object/unit matters. Swapping to a different dataset/domain merely because it exposes another axis is a warning sign.

---

## 4. Mother inheritance is a feature, not a novelty problem

A strong Hamdi-style extension should inherit as much as possible:

- same statistical unit;
- same prompt/readout location;
- same general analysis recipe;
- same validated model family when useful;
- same behavioral object;
- one new external axis or scientific question.

Novelty should come from **what is being asked**, not from inventing a new experimental stack.

This sharply reduces artifact risk: the mother has already established that the measurement setup can see the relevant object.

---

## 5. No-behavior-lottery rule

The following old search pattern is now forbidden as a default source of candidates:

```text
natural sounding distinction
→ find a dataset with fields that approximate it
→ design an expensive 3–4 family G0
→ discover the phenomenon is absent / scorer-driven / capability-floor / metadata-driven
```

Examples from the current continuation include the NTSB relevance→role frontier and multiple synthetic/open-model existence bets.

For a **failure-mechanism** idea, candidate generation now requires one of:

1. the exact behavior is already directly reported on relevant open families;
2. raw/public outputs already expose the anomaly and we can re-score them cheaply;
3. the behavior is trivially visible under ordinary prompts and has prior-work support.

For a **factorization/object** idea, candidate generation requires:

1. mother already measures the same object/unit;
2. the omitted axis is independently defined outside the model;
3. natural cross-cells exist without synthetic construction;
4. the mother's recipe can be extended without first inventing a new central gold.

If neither contract is satisfied, do not dispatch costly G0 merely because the mechanism would be interesting.

---

## 6. Search procedure from now on

The idea pool is generated **mother by mother**, not domain by domain and not by free association.

For each strong 2025–2026 mother:

1. Write its scientific object in one sentence.
2. List exactly what variables/axes the paper measures.
3. List what properties of the **same object** are explicitly held fixed, ignored, collapsed, or left to future work.
4. Generate at most 1–3 omitted axes that exist independently in the real world.
5. Run the mandatory mother-extension card.
6. Run semantic negative-memory audit immediately.
7. Run strongest-neighbor/title collision immediately.
8. Only then inspect artifact/cross-cells or existing raw outputs.
9. Only after the extension itself survives do S0/N0/N1/anti-narrowing/MI-fit proceed.

The most valuable source sentence in a mother paper is often not the headline result but something like:

- “we control for X”;
- “we do not distinguish Y and Z”;
- “future work should determine whether…”;
- “performance is similar overall, but…”;
- a residual table/ablation where one dimension remains unexplained.

But a future-work sentence is not sufficient by itself: the omitted axis must still pass title-level novelty and negative memory.

---

## 7. Cheap falsifier before any expensive model run

Even after a mother-extension card passes, use the cheapest fatal test first:

- existing raw model outputs;
- public prediction files;
- row-level cross-cell count;
- deterministic metadata/leak audit;
- obvious majority/length/position baseline;
- 5–20 faithful examples only when the behavior is already high-prior;
- mother-reported per-model table or appendix.

A 3–4-family fresh G0 is a **late S0 tool**, not the way we discover whether the candidate has a scientific object.

---

## 8. Success criterion

A candidate is promising when it can be summarized in the following form:

> **Paper M established A about object O. But A does not answer B, because B is an independently meaningful property of the same O. Natural A/B counterexamples already exist. We can reuse M's validated measurement recipe to ask B. Prior work has not asked B at title level. If B is internally represented, competing causal mechanisms make different intervention predictions.**

If that paragraph cannot be written cleanly, the idea is not Hamdi-style enough for the current search.

---

## 9. Relation to existing gates

This protocol sits **before** the existing funnel:

```text
strong concrete mother
→ HAMDI MOTHER-EXTENSION CARD
→ semantic negative-memory audit
→ strongest-neighbor/title collision
→ P0
→ S0
→ current-open-model existence/capability when required
→ N0
→ N1
→ anti-narrowing
→ MI-fit / surprise
→ PASS-REGISTER
```

It does not weaken `NATURAL_QUESTION_GATE.md` or `SCIENTIFIC_SUBSTRATE_GATE.md`; it changes how ideas are generated so fewer candidates arrive at S0 as expensive existence bets.

---

## One-line discipline

> **Do not ask “what new phenomenon might models have?” Ask “what important property of this already-established object did the mother paper not ask?”**
