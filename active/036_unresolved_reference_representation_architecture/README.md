# 036 — Unresolved Reference Representation Architecture

Status: **PASS-REGISTER / GPU AUTHORIZED**  
Date: 2026-09-01

## A. Natural question

When a referring expression remains genuinely ambiguous because the available language does not determine a unique antecedent, **what representation does an LLM maintain before committing to an answer?**

Does it:

1. keep multiple candidate referents active in parallel;
2. maintain a single **underspecified reference state** that leaves the identity unresolved without explicitly representing each complete alternative; or
3. prematurely collapse onto one candidate, with any later `this is ambiguous` judgment computed downstream from a different uncertainty/readout process?

This question does not require the names AmbiCoref, Correct-Detect, or It Depends. It is an old language-processing / formal-semantics question about the representational format of unresolved ambiguity.

## B. Why this is paper-scale

Natural language is often intentionally or unavoidably ambiguous. A competent system should not merely know how to choose a referent when enough evidence exists; it must also represent **what remains unresolved** when evidence is insufficient. That distinction matters for dialogue clarification, reading comprehension, agent interaction, safety-critical instruction following, and calibrated reasoning.

The contribution is not `LLMs guess on an ambiguity benchmark -> which layer causes guessing?`. Existing work already shows the behavioral failure. The paper-level question is:

> **What computational architecture represents unresolved linguistic reference in an autoregressive language model?**

Parallel alternatives, semantic underspecification, and early commitment are genuinely different architectures with different causal predictions. All three are independently motivated by older theories of language processing rather than invented from an LLM error taxonomy.

## C. Scientific lineage

### Parallel alternatives / multiple interpretations

Psycholinguistic work on lexical and pronominal ambiguity has long asked whether multiple interpretations are simultaneously activated and how long alternatives survive. Work surveyed in semantic-underspecification / utterance-processing research reports cases in which competing pronoun interpretations remain active through the sentence rather than being immediately pruned.

### Underspecified semantic representations

Formal semantics developed underspecification precisely to avoid enumerating every complete reading of an ambiguous expression. An underspecified representation captures constraints shared by several readings while deliberately leaving their distinguishing commitments unresolved. This is conceptually different from storing a disjunction or superposition of already-complete readings.

Relevant theory lineage includes:

- Reyle-style underspecified semantics / UDRT;
- Minimal Recursion Semantics and related constraint-based underspecification traditions;
- Egg (2010), *Semantic Underspecification*;
- psycholinguistic work on semantic underspecification and ambiguity processing;
- ambiguity-resolution work testing parallel activation, delayed commitment, and context-driven pruning.

### Early commitment / winner-take-all

A third class of processing accounts predicts rapid selection of a preferred interpretation, with later reanalysis or uncertainty detection required if that commitment becomes inappropriate. The scientific contrast therefore predates current LLM benchmarks.

## D. Strong mothers / established phenotype

### Mother 1 — AmbiCoref / Correct-Detect

**AmbiCoref** (Findings EACL 2023) constructs human-validated minimal sentence pairs that differ in whether a pronoun has a strongly preferred referent or remains ambiguous. Example shape:

```text
ambiguous:   The father called James because he is flying abroad soon.
unambiguous: The father called James because he wanted to ask a question.
```

The lexical skeleton, discourse participants, and pronoun are held fixed while the semantic cue that resolves the reference changes. The public repository releases generated sentence files by structural category (ECO-1/2, ECS-1/2, IC, TOP), ambiguous/unambiguous variants, verb phrases, noun phrases, code, and human judgments.

**Correct-Detect** (EMNLP 2025 Main) re-evaluates all 1,930 AmbiCoref sentences with GPT-4o and **Llama-3.1-70B-Instruct** and establishes the CORRECT-DETECT trade-off: models can resolve preferred reference under ordinary prompting and can detect ambiguity under ambiguity-oriented prompting, but no tested prompt allows them to reliably do both at once. Llama-3.1-70B changes from high ordinary coreference accuracy / extremely low ambiguity detection to substantially higher ambiguity detection with a large correctness cost.

The mother interprets this behavior mainly through training incentives that reward confident guessing. It does **not** determine whether the unresolved input is internally represented as parallel alternatives, an underspecified state, or an early single commitment.

### Mother 2 — It Depends

UncertaiNLP 2025 `It Depends: Resolving Referential Ambiguity in Minimal Contexts with Commonsense Knowledge` independently tests persistent reference ambiguity on modern open families including:

- **Qwen3-32B**;
- **Llama-3.1-8B**;
- **DeepSeek-V3**.

When several discourse entities remain valid referents, models commonly commit to one interpretation or enumerate candidates rather than appropriately preserve uncertainty / seek clarification. Crucially, the repository is public and unusually complete:

- questions and generated contexts;
- structured `entry` metadata containing the exact positive candidate referent set and negative distractor;
- all English entity-order permutations;
- raw outputs for Qwen3, Llama and DeepSeek;
- judged and raw-judge outputs;
- generation/evaluation scripts.

The published evaluation uses LLM-as-Judge for free-form response typing, but **036 does not use that judge as central gold**. The candidate set is explicit deterministic metadata in each row, e.g. `positive=[helicopter, mosquito]`, `negative=donut`. That structure is sufficient for candidate-scoring and causal analyses without API judging.

### Established premise

Across the two independent windows, modern open-weight LLMs clearly possess the base ability to resolve references when evidence is sufficient but behave pathologically when several interpretations remain permissible. The behavioral premise therefore exists before 036 and does not need to be discovered with GPU experiments.

## E. Exact novelty delta / N0-N1-N2

### N0 — object ownership

Existing work owns:

- whether models detect referential ambiguity;
- the Correct-Detect behavioral trade-off;
- whether models clarify, hedge, enumerate, or commit under persistent ambiguity;
- output-level semantic collapse under underspecified coding prompts;
- representation of already-disambiguated lexical senses.

No strongest neighbor found asks the headline 036 question:

> **What representational format carries a reference that remains unresolved inside a native modern open-weight LLM?**

### N1 — causal occupancy

No 2025–2026 work found causally adjudicates **parallel candidate referents vs an underspecified reference state vs early commitment** on unresolved reference.

Important neighboring work does not occupy this factorization:

- EACL 2026 idiom MI shows competition between literal and figurative pathways for idioms, a particular lexicalized ambiguity and not unresolved discourse reference.
- August 2026 work on ambiguous word pairs uses activation patching after contextual information selects different word senses; it studies how two *resolved* senses diverge/converge across layers, not how the model stores a still-unresolved variable.
- July 2026 `semantic collapse` work establishes output-level collapse under underspecified programming tasks but does not test linguistic reference representations or the parallel-vs-underspecified distinction.
- prompt-ambiguity attribution work localizes which input spans produce ambiguous instructions, not the format of the resulting unresolved semantic state.

### N2 — delta width

036 is not `Correct-Detect behavior -> mechanism`. The competing computations are an independent formal/psycholinguistic debate about **how ambiguity itself is represented**. AmbiCoref and It Depends are measurement windows that happen to expose this old question in modern LLMs.

Deleting all benchmark/mother names leaves a normal scientific question:

> **Does an LLM represent unresolved reference by maintaining explicit alternatives, by a compact underspecified state, or by prematurely committing to one interpretation?**

That question would remain meaningful if all current benchmark names disappeared.

## F. Venue-scale comparison

- **EMNLP 2025 Outstanding — shared filler-gap structure.** A mature external linguistic theory asks what abstract computation several constructions share; causal LM intervention adjudicates the alternatives. 036 likewise imports a mature ambiguity-representation debate and uses LMs as a causal test bed.
- **NAACL 2025 — taxonomy vs similarity in property inference.** The competing organizations exist before the dataset, and either answer preserves the paper question. 036 has the same result-invariant shape for parallel alternatives vs underspecification vs early commitment.
- **ACL 2026 Main — tool irrelevance.** Controlled stimuli separate natural variables rather than inventing the scientific object. AmbiCoref's ambiguous/resolved minimal pairs isolate naturally meaningful reference evidence; the dataset is a microscope.
- **NAACL 2025 — Racing Thoughts.** A broad processing architecture is tested with causal tools rather than reducing the contribution to best-layer localization. 036 similarly targets an architecture-level representation signature.

## G. Data / substrate

```yaml
natural_or_synthetic: psycholinguistically motivated controlled language + controlled dialogue; scientific object is external
central_gold:
  AmbiCoref:
    - template-defined ambiguous vs unambiguous condition
    - structural family ECO-1/2, ECS-1/2, IC, TOP
    - human reference-confidence judgments on released subset
  ItDepends:
    - row-level explicit positive candidate referent set
    - explicit negative distractor
    - all entity-order permutations
row_level_artifact:
  - LucyYYW/AmbiCoref (public)
  - lukasellinger/itdepends (public)
open_checkpoint_evidence:
  - Llama-3.1-70B-Instruct on Correct-Detect/AmbiCoref
  - Qwen3-32B on It Depends
  - Llama-3.1-8B on It Depends
  - DeepSeek-V3 on It Depends
why_dataset_is_only_a_measurement_window: ambiguity, referential uncertainty, parallel interpretation, semantic underspecification, and early commitment all predate both datasets
external_validity_path:
  - human-authored AmbiCoref minimal pairs
  - persistent commonsense reference ambiguity in dialogue
  - later lexical/syntactic ambiguity as out-of-domain validation, not primary registration evidence
```

The central experiments **do not require an LLM judge**. Free-form response categories from the mother are prior behavioral evidence only. 036's central outputs are candidate-token / candidate-string scores and causal changes relative to deterministic candidate labels.

## H. Competing mechanisms and frozen predictions

### H1 — Explicit parallel alternatives

The unresolved pronoun maintains causally usable representations of multiple candidate referents simultaneously.

Predictions:

- both candidate identities remain causally available at the unresolved decision state;
- candidate-specific causal edits derived from resolved-A and resolved-B controls can independently suppress/restore their corresponding candidate score;
- removing candidate A's component leaves B substantially intact and vice versa;
- disambiguating evidence prunes one branch rather than constructing a previously absent candidate representation;
- order permutations change surface location but not the existence of two independently causal candidate components.

### H2 — Underspecified reference state

The model represents a single unresolved reference variable / constraint state rather than two complete candidate-specific readings.

Predictions:

- unresolved examples have weak candidate-specific causal components despite intact lexical representations of A and B;
- a causal ambiguity/underspecification component is shared across different candidate identities and structural templates;
- manipulating this shared component changes candidate competition jointly rather than selectively deleting one fully represented branch;
- disambiguating evidence resolves/fills the state, producing a candidate-specific representation that was not independently causally available beforehand.

### H3 — Premature commitment

The model resolves the pronoun internally to one preferred candidate before sufficient evidence exists; ambiguity detection is a downstream readout or separate metalinguistic process.

Predictions:

- unresolved examples contain one dominant candidate-specific causal component and little causal availability for the competitor;
- the dominant internal candidate tracks known order/semantic biases and can flip under prespecified position permutations;
- ablating the committed candidate destabilizes the output rather than revealing a symmetric latent competitor;
- ambiguity prompting can alter downstream reporting while leaving the earlier committed reference state comparatively intact.

These are computation/representation alternatives, not early/middle/late layer labels.

## I. Frozen S0 / causal microscope

### S0-0 — behavioral existence

Already satisfied by prior public work:

- Llama-3.1-70B on AmbiCoref/Correct-Detect shows strong coreference ability plus the ambiguity-detection trade-off;
- Qwen3-32B, Llama-3.1-8B and DeepSeek-V3 on It Depends show high ClearRef capability but systematic abnormal behavior when multiple referents remain valid.

No GPU is required to decide whether unresolved-reference behavior exists.

### S0-1 — AmbiCoref minimal-pair set

Use **all programmatically alignable ambiguous/unambiguous pairs** within the released structural files, defined before model execution:

- ECO-1 / ECO-2;
- ECS-1 / ECS-2;
- IC;
- TOP.

A pair is valid only if noun phrases, pronoun morphology, main-clause skeleton, and template identity align, with the released ambiguity-manipulating verb/phrase difference being the intended change. Do not select pairs based on model effect size.

Primary human-valid subset: released human-judgment items. Full generated pairs are replication/scale-up.

### S0-2 — resolved-A / resolved-B reference components

Candidate-specific causal components are defined only from **resolved controls with known antecedent direction**, balanced across:

- candidate position A/B;
- structural family;
- names vs noun phrases where available;
- lexical verbs/phrases.

Do not define `A component` by selecting a layer that happens to decode A best on ambiguous items.

### S0-3 — It Depends persistent-ambiguity replication

Use the frozen English `normal` SharedRef/ClearRef rows for Qwen3-32B and Llama-3.1-8B first, with published entity-order permutations as mandatory controls.

For SharedRef, the positive candidate set is taken directly from row metadata; the negative item is a comprehension/distractor control. No free-form judge is used.

### Behavioral reproduction gate before broad MI

On the frozen checkpoints/items, verify only the already-established premise:

1. ClearRef candidate discrimination is strong enough to establish basic reference/comprehension capability.
2. Ambiguous/SharedRef items do not collapse to pure random behavior.
3. Candidate-score/order patterns reproduce the published qualitative ambiguity sensitivity/commitment behavior.

Failure on a prespecified checkpoint terminates that replication; it does not authorize subset/prompt hunting or a new paper story.

## J. First causal experiment contract

### J1 — resolved-reference causal basis

Using resolved A- and B-biased AmbiCoref controls, identify a **candidate-reference causal subspace/basis** with cross-validated training families and held-out lexical templates. Candidate directions must causally change forced candidate-reference score on held-out resolved items before they can be used on ambiguous items.

This is a measurement calibration, not the headline result.

### J2 — unresolved-state intervention

At prespecified reference-decision positions (pronoun representation and final query/reference decision; exact token mapping fixed before sweeps), apply candidate-specific removal/restoration edits to unresolved items.

For candidate `i`, define:

```text
self_effect_i = change in score(candidate_i) under intervention targeting i
cross_effect_i = change in score(other candidate) under the same intervention
```

### Primary preregistered causal signature — Candidate Causal Separability (CCS)

For each item with candidates A/B:

```text
CCS = 0.5 * [
  (|self_effect_A| - |cross_effect_A|) / (|self_effect_A| + |cross_effect_A| + eps)
+ (|self_effect_B| - |cross_effect_B|) / (|self_effect_B| + |cross_effect_B| + eps)
]

Coverage = min(|self_effect_A|, |self_effect_B|)
            / (max(|self_effect_A|, |self_effect_B|) + eps)
```

Interpret **CCS jointly with Coverage and the shared unresolved-state control below**, with signs/direction fixed from resolved calibration. Do not threshold post hoc to manufacture categories.

Frozen theory signatures:

- **H1 parallel alternatives:** high candidate selectivity **and** substantial balanced Coverage for both candidates.
- **H3 early commitment:** high selectivity for one candidate but strongly asymmetric/low Coverage for the competitor; asymmetry tracks prespecified order/bias manipulations.
- **H2 underspecified state:** weak candidate-specific Coverage for both before disambiguation, despite intact entity comprehension, plus a causal shared unresolved-state effect that changes both candidate scores jointly.

### J3 — shared unresolved-state control for H2

Independently derive an ambiguity-state direction/subspace from ambiguous-vs-resolved pairs using training templates only, with candidate identities and antecedent direction balanced out. It must generalize to held-out structural families and It Depends candidate identities.

Intervene on this shared state and measure **joint candidate coupling**:

```text
JointCoupling = min(|delta score_A|, |delta score_B|)
                / (max(|delta score_A|, |delta score_B|) + eps)
```

H2 specifically predicts low candidate-specific Coverage but high cross-item/generalized JointCoupling. H1 predicts candidate-specific causal availability dominates; H3 predicts commitment asymmetry dominates.

### J4 — disambiguation transition

For minimal ambiguous/resolved AmbiCoref pairs, measure whether resolution:

- prunes one already-causal branch (H1),
- fills/refines a previously underspecified state (H2), or
- reinforces/reverses an existing winner (H3).

The headline statistic is the **causal representation signature**, not the layer at which the change peaks.

## K. Story invariance

- **Result A — parallel alternatives:** LLMs causally preserve multiple referents during genuine ambiguity and later prune them when evidence arrives.
- **Result B — underspecified state:** LLMs avoid explicit branch enumeration and carry a compact unresolved reference state that becomes candidate-specific only after disambiguation.
- **Result C — early commitment:** LLMs internally commit before evidence licenses commitment; later ambiguity awareness is downstream/separate.

All results answer exactly:

> **How do LLMs represent unresolved linguistic reference?**

None requires retitling the paper as Correct-Detect mechanism, prompt sensitivity, benchmark validity, or best-layer localization.

## L. Fatal controls / hard kills

1. **Order bias:** It Depends publishes all candidate permutations; a claimed architecture must survive or explicitly follow the frozen H3 order prediction. No single ordering is sufficient.
2. **Entity lexical identity:** candidate-specific effects must generalize across held-out names/noun phrases; memorized entity semantics cannot define the reference component.
3. **Verb/phrase semantics:** resolved-vs-ambiguous effects must generalize across AmbiCoref structural/template families rather than being a single implicit-causality verb direction.
4. **Basic entity comprehension:** if the model cannot distinguish the candidate entities or the negative distractor, the item is excluded by prespecified capability criteria, not post-hoc MI effect.
5. **Prompt/readout confound:** forced candidate scoring and free generation are analyzed separately. A change in wording such as `I am unsure` is not evidence for an internal ambiguity state.
6. **Shuffled donor / random subspace:** causal effects must exceed matched shuffled-donor and norm-matched random-subspace controls.
7. **Candidate-direction calibration:** a direction that is merely decodable but fails causal validation on held-out resolved items cannot be used to claim parallel alternatives.
8. **H1 vs H2 identifiability:** if candidate-specific Coverage and shared-state JointCoupling cannot be estimated robustly enough to distinguish explicit alternatives from underspecification, terminate the architectural claim rather than collapse the paper into `ambiguity is represented somewhere`.
9. **Novelty kill:** if new work demonstrates causal parallel-vs-underspecified-vs-commitment factorization for unresolved linguistic reference, KILL-NOVELTY immediately.
10. **No human-mechanism identity claim:** matching a psycholinguistic theory signature supports an analogous computational architecture in LLMs, not biological equivalence.

## M. Registration verdict

```yaml
paper_scale: PASS
benchmark_removal: PASS
natural_object: PASS
venue_comparators: PASS
N0_object_ownership: PASS
N1_causal_occupancy: PASS
N2_delta_width: PASS
substrate: PASS
central_gold_without_llm_judge: PASS
existing_behavior: PASS
modern_open_family_evidence: PASS
story_invariance: PASS
competing_mechanisms: PASS
frozen_S0_contract: PASS
frozen_first_causal_signature: PASS
fatal_controls: PASS
verdict: PASS-REGISTER
GPU_AUTHORIZED: true
```

Registration freezes the headline and the architecture-level alternatives. Negative results may kill measurement/identifiability, but they may not turn 036 into a benchmark-mechanization or layer-localization project.
