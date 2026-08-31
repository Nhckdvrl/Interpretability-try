# Continuation Mother Search — Negative Results (2026-08-31)

This file records scientific objects seriously audited after `HANDOFF_HAMDI_SEARCH_2026-08-31.md`. It is negative memory, not a candidate list. The authority rule remains: newer terminal addenda and the handoff override stale older `lead`, `HOLD`, or `under audit` prose.

---

## 1. Geographic Direction ≠ Distance — KILL-N1

**Natural question:** A place can be north/south/east/west of another place independently of how far away it is. Does an LLM compute relative direction and metric distance from one common spatial representation, or through separable mechanisms?

**Why it looked good:**

- both variables are objectively grounded by real coordinates;
- the same place-pairs supply deterministic gold for bearing and distance;
- the mechanism fork is clean: shared metric map vs qualitative relation state plus quantitative distance state;
- no LLM judge or researcher-created central labels are needed.

**Kill evidence:**

A 2026 mechanistic study already directly probes **relative geographic space** with activation patching in Gemma 2 2B. It contrasts qualitative proximity prompts with quantitative distance prompts over hundreds of real UK places and causally studies where relative spatial information is computed. This is not merely a geolocation benchmark: it occupies the internal scientific object of relative geographic representation and quantitative spatial relations. Renaming one projection of that object as `bearing vs distance` would be a narrower statistic inside an already mechanistically studied spatial substrate.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** do not revive as bearing-vs-distance, direction-vs-proximity, qualitative-vs-metric geography, relative-position-vs-distance, or by switching countries / coordinate sources / model families.

**Resurrection condition:** a different natural spatial variable that is not simply another deterministic readout of the same relative geographic coordinate object, with independent external gold and a distinct causal computation not covered by existing relative-space patching work.

**Reference:** https://arxiv.org/abs/2605.14535

---

## 2. Indifference / Underdetermination ≠ Forced Choice — KILL-N1

**Natural question:** When two options are genuinely tied or the available information does not justify preferring either one, does the model represent that indeterminacy but then force a choice anyway, or does it fail to represent the tie in the first place?

**Why it looked good:**

- the behavioral distinction is natural: humans can be indifferent or indecisive rather than pretending to have a strict preference;
- FAccT 2026 organ-allocation experiments report that humans retain indecision/randomization in difficult cases whereas LLMs overwhelmingly make deterministic choices even when a coin-flip option is available;
- the mechanism fork looked Hamdi-like: `tie/underdetermination reader` vs downstream `forced-choice writer`.

**Kill evidence:**

The title-level object is already crowded from both sides. Large 2026 arbitrary-choice audits establish systematic forced-choice biases under supposedly arbitrary prompts. NeurIPS 2025 explicitly treats **rating indeterminacy resolved by forced choice** as a core evaluation object. Separate 2026 decision-theory work develops experimental procedures specifically to distinguish **indifference** from **indecisiveness/incompleteness**. Therefore a new paper whose novelty is to locate a hidden `tie state` and patch the chooser would be a mechanistic follow-up to an already explicit indeterminacy/forced-choice scientific object, not a new one.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as tie-state-vs-choice, abstention-vs-preference, randomization-vs-decision, weak-vs-strict preference, or `reader/writer` terminology. The vocabulary does not create novelty.

**Resurrection condition:** a qualitatively different natural behavior in which external ground truth establishes underdetermination independently of preference elicitation, and whose failure cannot be reduced to arbitrary-choice bias, abstention, or forced-choice handling.

**References:**

- https://doi.org/10.1145/3805689.3806437
- https://www.microsoft.com/en-us/research/publication/validating-llm-as-a-judge-systems-under-rating-indeterminacy/
- https://doi.org/10.1016/j.geb.2026.05.011

---

## 3. Ordinal Comparison ≠ Cardinal Magnitude — KILL-N0/N1

**Natural question:** If a model knows the absolute magnitude of two real-world quantities, does it compare them by reading a common magnitude representation, or does it store/use pairwise ordinal relations separately?

**Why it looked good:**

- the distinction is scientifically clean: knowing `A > B` is not identical to knowing the values of A and B;
- real entity attributes such as river length or country population provide objective source-grounded magnitudes;
- pairwise order is deterministically derived from those same external values;
- competing mechanisms include a shared scalar magnitude axis versus shortcut/pairwise comparison states.

**Kill evidence:**

EACL 2026 **Knowing the Facts but Choosing the Shortcut: Understanding How LLMs Compare Entities** already owns almost exactly this object. It studies entity comparisons with numerical ground truth, contrasts model decisions with their own numerical knowledge, and identifies popularity, mention order and semantic co-occurrence as competing shortcut features. It further finds model-size-dependent use of numerical knowledge and shows that chain-of-thought can steer models toward numerical features. In parallel, 2026 work on numerical representations reports that internal states encode scalar magnitude. A project asking whether ordinal judgments use a shared cardinal magnitude representation would therefore be a direct mechanistic successor to an already explicit `numerical fact vs comparison shortcut` story.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as rank-vs-value, greater-than-vs-magnitude, relative-vs-absolute quantity, scalar-vs-pairwise comparison, or by using a different Wikidata property.

**Resurrection condition:** a non-numerical relation where the relational variable is not simply a deterministic function/readout of the same scalar quantity and where the title-level internal object is not already occupied.

**References:**

- https://aclanthology.org/2026.eacl-long.222/
- https://arxiv.org/search/?query=%22LLMs+Know+More+About+Numbers+than+They+Can+Say%22&searchtype=all

---

## 4. Subliminal Trait Transmission / Hidden-Signal Reader–Writer — KILL-N1

**Natural question:** When a student model acquires a teacher's behavioural trait from semantically unrelated outputs, is there a hidden signal decoder separate from the downstream trait writer, or is transfer a single distributed parameter-alignment effect?

**Why it looked good:**

- the Nature 2026 mother phenomenon is large and counterintuitive;
- transfer occurs through number sequences, reasoning traces and code even after semantic references to the trait are removed;
- teacher/student identity constraints create natural competing mechanism hypotheses;
- the effect is already reproducible in open models.

**Kill evidence:**

The mechanistic opening has already been occupied. ICLR 2026 **Towards Understanding Subliminal Learning: When and How Hidden Biases Transfer** studies when hidden transfer occurs, identifies divergence-bearing tokens/data regions, tests masking interventions, and localizes the critical learning dynamics to early layers / parameter changes. Public follow-up code around subliminal learning also includes representation-oriented analyses such as probes/steering/SAE work. Consequently, reframing the phenomenon as a `hidden-signal reader + trait writer` is not a new scientific object; it is a different mechanistic vocabulary for an already active mechanism program.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** do not revive as decoder-vs-writer, covert channel, latent trait code, hidden bias direction, early-layer receiver, or by swapping the transmitted trait.

**Resurrection condition:** a different **naturally occurring** transmission phenomenon, not another distillation/task-generated hidden channel, with a causal mechanism not reducible to the currently studied divergence-token / parameter-alignment / early-layer transfer story.

**References:**

- https://www.nature.com/articles/s41586-026-10319-8
- https://proceedings.iclr.cc/paper_files/paper/2026/hash/b51b50262b492dd89bb9cd3105a46702-Abstract-Conference.html

---

## 5. Abstract Moral Recognition ≠ Concrete Moral Choice — KILL-N0

**Natural question:** Why can a model correctly name or detect a moral principle yet violate or weight it differently when making a concrete choice?

**Why it looked good:**

- Nature Communications 2026 speciesism work reports striking dissociations: models can detect speciesist statements while often judging them acceptable, and abstract attitudes can diverge from concrete rescue choices;
- the same paper finds unusually strong sensitivity to cognitive capacity in concrete dilemmas;
- this could superficially suggest `principle representation` versus `decision policy` mechanisms.

**Kill evidence:**

The mother already defines and measures the abstract/concrete dissociation as part of its headline behavioral object, including explicit detection, moral classification, psychological measures and concrete dilemmas. More broadly, EMNLP 2025 **Mind the Value-Action Gap** explicitly studies the value/action distinction in LLM behavior. Therefore `principle state exists but downstream action ignores it` is exactly the prohibited mother-behavior→mechanism / generic `knows but does not use` shape.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as moral-belief-vs-action, principle-vs-choice, abstract-vs-concrete morality, recognition-vs-application, or by switching to another protected class / moral domain.

**Resurrection condition:** a new natural decision phenomenon with independent external outcomes and a title-level distinction not reducible to the already occupied value–action / recognition–application object.

**References:**

- https://www.nature.com/articles/s41467-026-72297-9
- https://aclanthology.org/2025.emnlp-main.154/

---

## 6. Pattern Detection ≠ Pattern Hallucination on Random Sequences — KILL-S0

**Natural question:** Why can a model identify real numerical regularities yet confidently invent a rule for a sequence generated without one?

**Why it looked good:**

- the behavior resembles apophenia / seeing order in randomness;
- a 2025 EMNLP Findings paper reports that LLMs can solve genuine arithmetic/geometric patterns while constructing elaborate rules for random integer sequences;
- mechanism forks could distinguish a pattern-detector from a compulsory pattern-explainer/readout.

**Kill evidence:**

The existence substrate is synthetic random-number-series generation, and `no pattern` in a finite sequence is not an independently grounded natural-world label: infinitely many rules can interpolate any finite sequence. The scientific object therefore depends on researcher-generated stimuli plus a convention about which patterns count as intended/valid. Under the current S0 contract this cannot support a failure-mechanism registration, regardless of how clean the mechanistic story sounds.

**Death code:** `SYNTHETIC_ONLY_EXISTENCE_SUBSTRATE`

**Nearest-neighbor warning:** do not revive as apophenia, order-in-noise, hallucinated规律, random-sequence explanation, or by generating different random symbols.

**Resurrection condition:** a large natural population with externally established signal-present/signal-absent ground truth and a robust modern-open-family tendency to infer structure in genuine null cases.

---

## 7. Intervention Effect Direction ≠ Magnitude — frontier status unchanged

This search does **not** promote the existing frontier.

Current status remains:

```text
HOLD-FATAL-CONTROL / NOT REGISTERED / NO MI AUTHORIZED
```

Artifact audit in this continuation:

- the Nature 2026 treatment-effect paper's public data/code points to a Code Ocean capsule, but the capsule was not retrievable through the present interface during this audit;
- the 2026 **The Illusion of Intervention** paper and method were obtained/read, confirming treatment-induced user drift and negative-control/confounder adjustment as a genuine fatal alternative explanation;
- no official complete code/raw-output artifact for the user-drift paper was located in the searches performed here;
- therefore the required cross-open-family rerun plus faithful correction has **not** been executed, and no residual magnitude-inflation claim is authorized.

Do not proceed to probe/SAE/patching until the fatal control is actually run.

**References:**

- https://www.nature.com/articles/s41586-026-10742-x
- https://codeocean.com/capsule/9843791/tree/v1
- https://arxiv.org/abs/2605.20767

---

## Search lesson from this continuation

Three shapes repeatedly looked strong and still failed:

```text
beautiful objective two-axis gold
→ but the internal object is already mechanistically occupied
```

```text
large surprising mother anomaly
→ but the most obvious “Hamdi-style” reader/writer reinterpretation is only new vocabulary
```

```text
clean behavioral dissociation
→ but its existence depends on synthetic nulls / researcher-defined central labels
```

The bar therefore remains unchanged: **external cleanliness cannot rescue N0/N1 collision, and mechanistic elegance cannot rescue a missing natural scientific object.**
