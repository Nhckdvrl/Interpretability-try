# 038 — Unresolved Reference Representation Architecture

Status: **PASS-REGISTER / GPU AUTHORIZED**  
Date: 2026-09-01

## A. Natural question

When a referring expression remains genuinely ambiguous because the available language does not determine a unique antecedent, **what representation does an LLM maintain before committing to an answer?**

Does it:

1. keep multiple candidate referents causally active in parallel;
2. maintain a single **underspecified reference state** that leaves identity unresolved without enumerating complete alternatives; or
3. prematurely collapse onto one candidate, with later ambiguity awareness computed by a downstream/separate readout?

This question does not depend on AmbiCoref, Correct-Detect, or It Depends. It is a classic language-processing / formal-semantics question about the representational format of unresolved ambiguity.

## B. Why this is paper-scale

Natural language often leaves reference intentionally or unavoidably unresolved. A competent system must not only select a referent when evidence is sufficient; it must represent **what remains undecided** when evidence is insufficient. That matters for clarification, dialogue, reading comprehension, instruction following, uncertainty-aware agents, and reliable reasoning.

The paper is not `LLMs guess on an ambiguity benchmark -> find the layer causing guessing`. Existing work already establishes the behavioral phenomenon. The paper-level question is:

> **What computational architecture represents unresolved linguistic reference in an autoregressive LLM?**

Parallel alternatives, semantic underspecification, and early commitment are independently motivated architectures with distinct causal predictions.

## C. Scientific lineage

The competing accounts predate modern LMs.

### H-theory lineage 1 — parallel alternatives

Psycholinguistic research on lexical and pronominal ambiguity asks whether multiple interpretations are simultaneously activated and how long competitors survive. Work surveyed in ambiguity-processing / semantic-underspecification research reports cases where multiple pronoun interpretations remain active through a sentence rather than being immediately pruned.

### H-theory lineage 2 — semantic underspecification

Formal semantics developed underspecified representations precisely to avoid enumerating every complete reading. An underspecified representation stores constraints shared across possible resolutions while leaving the distinguishing commitment open. This is conceptually different from maintaining a disjunction/superposition of already-complete readings.

Relevant traditions include Reyle-style underspecified semantics / UDRT, Minimal Recursion Semantics and related constraint-based approaches, Egg (2010) `Semantic Underspecification`, and psycholinguistic work on underspecified interpretation.

### H-theory lineage 3 — early commitment

A third processing family predicts rapid winner-take-all selection of a preferred interpretation, followed by reanalysis or separate uncertainty detection if the commitment later becomes inappropriate.

Thus the architecture question exists independently of current LLM benchmarks.

## D. Strong mothers / established phenotype

### Mother 1 — AmbiCoref + Correct-Detect

AmbiCoref (Findings EACL 2023) releases human-validated **minimal ambiguous/unambiguous sentence pairs**. Example:

```text
ambiguous:   The father called James because he is flying abroad soon.
unambiguous: The father called James because he wanted to ask a question.
```

The participants, pronoun and main-clause skeleton stay fixed while a theory-motivated semantic cue changes whether reference is resolved. The public repository releases sentence files by structural family (`ECO-1/2`, `ECS-1/2`, `IC`, `TOP`), ambiguous/unambiguous versions, verb phrases, noun phrases, code and human judgments.

Correct-Detect (EMNLP 2025 Main) evaluates all 1,930 AmbiCoref sentences with GPT-4o and **Llama-3.1-70B-Instruct** and establishes the CORRECT-DETECT trade-off: ordinary prompting yields strong preferred-reference performance but very weak ambiguity detection; ambiguity-oriented prompting improves detection at a large correctness cost. The mother mainly interprets the behavior in terms of training incentives for confident guessing. It does **not** decide whether unresolved input is internally represented as parallel alternatives, an underspecified state or an early single commitment.

### Mother 2 — It Depends

UncertaiNLP 2025 `It Depends` independently establishes persistent referential ambiguity behavior on modern open families including:

- **Qwen3-32B**;
- **Llama-3.1-8B**;
- **DeepSeek-V3**.

When several discourse entities remain valid referents, models often commit to one interpretation or enumerate candidates rather than appropriately preserving uncertainty / clarifying. The public repo contains questions, contexts, generation/evaluation scripts, raw outputs, judged outputs, **all English entity-order permutations**, and row-level `entry` metadata with exact positive candidate referents and a negative distractor.

The published paper uses LLM-as-Judge for free-form response typing, but **038 does not use an LLM judge as central gold**. Candidate sets are deterministic row metadata, e.g. `positive=[helicopter, mosquito]`, `negative=donut`, so candidate scoring and causal tests require no API judge.

### Behavioral premise

Across the two independent windows, modern open LMs can resolve reference when evidence is sufficient yet exhibit systematic pathological commitment/uncertainty behavior when multiple references remain possible. The paper question therefore does not require GPU discovery.

## E. Exact novelty delta — N0 / N1 / N2

### N0 — object ownership

Prior work owns:

- ambiguity detection;
- the Correct-Detect behavioral trade-off;
- clarification / hedging / enumeration / commitment behavior;
- output-level semantic collapse under underspecified coding prompts;
- internal representations of **already context-disambiguated** lexical senses.

No strongest neighbor found owns:

> **What representational format carries a linguistic reference that remains genuinely unresolved inside a modern open-weight LLM?**

### N1 — causal occupancy

No 2025–2026 work found causally adjudicates **parallel candidate referents vs a compact underspecified reference state vs premature commitment** for unresolved reference.

Important nearby work does not occupy this factorization:

- EACL 2026 idiom MI shows literal/figurative pathway competition for one lexicalized ambiguity subtype, not unresolved discourse reference.
- August 2026 ambiguous-word activation patching compares representations after context selects different senses; it studies two *resolved* meanings, not an unresolved variable.
- July 2026 `semantic collapse` establishes output collapse under underspecified programming prompts, not linguistic-reference representational format.
- prompt-ambiguity attribution localizes ambiguous prompt spans, not the semantic state produced by unresolved reference.

### N2 — delta width

038 is not `Correct-Detect found X -> explain X internally`. The competing representations come from an independent formal/psycholinguistic debate about **how ambiguity itself is represented**. AmbiCoref and It Depends are measurement windows.

Deleting all dataset names leaves a normal scientific question:

> **Does an LLM represent unresolved reference with explicit alternatives, with an underspecified state, or by prematurely committing to one interpretation?**

## F. Venue-scale comparison

- **EMNLP 2025 Outstanding — shared filler-gap structure:** mature external linguistic theory -> causal LM adjudication. 038 has the same theory-first shape.
- **NAACL 2025 — taxonomy vs similarity in property inference:** competing scientific organizations exist before the dataset and all outcomes preserve the headline. Same for parallel/underspecified/commitment.
- **ACL 2026 Main — tool irrelevance:** controlled stimuli separate naturally meaningful variables rather than invent the object. AmbiCoref minimal pairs similarly isolate resolution evidence.
- **NAACL 2025 — Racing Thoughts:** architecture-level causal explanation rather than a best-layer contribution. 038 likewise targets a processing architecture signature.

## G. Data / substrate

```yaml
natural_or_synthetic:
  primary: psycholinguistically motivated controlled minimal sentences
  corroboration: controlled multi-turn reference dialogues
central_gold:
  AmbiCoref:
    - released ambiguous/unambiguous template condition
    - structural family ECO-1/2, ECS-1/2, IC, TOP
    - released human reference-confidence judgments
  ItDepends:
    - explicit positive candidate-referent set in every row
    - explicit negative distractor
    - published entity-order permutations
row_level_artifact:
  - LucyYYW/AmbiCoref
  - lukasellinger/itdepends
open_checkpoint_evidence:
  - Llama-3.1-70B-Instruct on Correct-Detect/AmbiCoref
  - Qwen3-32B on It Depends
  - Llama-3.1-8B on It Depends
  - DeepSeek-V3 on It Depends
why_dataset_is_only_a_measurement_window: ambiguity, parallel interpretation, underspecification and early commitment are pre-existing linguistic/cognitive objects
external_validity_path:
  - human-validated AmbiCoref minimal pairs
  - persistent commonsense referential ambiguity in dialogue
  - later lexical/syntactic ambiguity only as out-of-domain validation
```

Central scoring is deterministic candidate scoring / candidate-string likelihood plus causal effects. No API judge is required.

## H. Competing mechanisms and frozen predictions

### H1 — explicit parallel alternatives

The unresolved expression maintains causally usable representations of multiple candidate referents simultaneously.

Predictions:

- both candidate identities are causally available before output;
- candidate-specific edits calibrated on resolved-A / resolved-B controls can independently suppress or restore the corresponding candidate score;
- removing A leaves B substantially intact and vice versa;
- disambiguating evidence prunes one already-active branch;
- entity-order permutations change surface location but not dual candidate availability.

### H2 — underspecified reference state

The model maintains one unresolved variable/constraint state rather than two complete candidate readings.

Predictions:

- unresolved items show weak candidate-specific causal components despite intact lexical representations of both candidates;
- an ambiguity/underspecification component generalizes across candidate identities and structural templates;
- manipulating it changes candidate competition jointly rather than selectively deleting one complete branch;
- disambiguating evidence fills/refines the state and creates a candidate-specific representation that was not independently causally available beforehand.

### H3 — premature commitment

The model selects one preferred candidate before the linguistic evidence licenses a unique reference; ambiguity detection is later/separate.

Predictions:

- unresolved items contain one dominant candidate-specific causal component and little causal availability for the competitor;
- dominance tracks prespecified semantic/order biases and can flip under published entity permutations;
- ablating the committed candidate destabilizes the answer rather than revealing a symmetric latent competitor;
- ambiguity prompting can change downstream reporting without equivalently changing the earlier committed reference state.

These are representation/computation alternatives, not early/middle/late localization labels.

## I. Frozen S0 / causal microscope

### S0-0 — existence

Already satisfied by prior work: Llama-3.1-70B exhibits the AmbiCoref/Correct-Detect trade-off; Qwen3-32B, Llama-3.1-8B and DeepSeek-V3 show high ClearRef competence and abnormal behavior under persistent SharedRef ambiguity. GPU is not needed to discover the phenomenon.

### S0-1 — AmbiCoref minimal pairs

Use **all programmatically alignable ambiguous/unambiguous pairs** in the released `ECO-1/2`, `ECS-1/2`, `IC`, and `TOP` files. A pair is valid only when noun phrases, pronoun morphology, main-clause skeleton and template identity align, with the released ambiguity-manipulating verb/phrase being the intended difference. Do not select pairs by model effect size.

The human-judgment subset is the primary human-valid analysis; the full generated set is scale-up/replication.

### S0-2 — resolved A/B calibration

Candidate-reference causal components are defined only from resolved controls with known antecedent direction, balanced across candidate position, structural family, names/noun phrases and lexical templates. No layer may be selected because it happens to decode the ambiguous items best.

### S0-3 — persistent-ambiguity replication

Use frozen English `normal` SharedRef/ClearRef rows from It Depends on **Qwen3-32B** and **Llama-3.1-8B** first, with all published candidate-order permutations as mandatory controls. Positive/negative candidate labels come directly from row metadata.

### Cheap reproduction gate

Before broad MI, only reproduce the already-established premise:

1. strong ClearRef candidate discrimination;
2. non-random SharedRef candidate behavior;
3. published qualitative ambiguity/commitment sensitivity.

Failure terminates a prespecified checkpoint; it does not authorize prompt/subset hunting.

## J. Frozen first causal experiment

### J1 — resolved-reference causal calibration

Using resolved A- and B-biased AmbiCoref controls, learn a candidate-reference causal basis with training structural families and held-out lexical/template validation. A candidate direction must **causally change forced candidate-reference score on held-out resolved items** before it can be used on unresolved examples.

### J2 — unresolved-state intervention

At prespecified reference-decision positions (pronoun representation and final reference decision), apply candidate-specific removal/restoration edits to unresolved items.

For candidate `i`:

```text
self_effect_i  = change in score(candidate_i) under intervention targeting i
cross_effect_i = change in score(other candidate) under the same intervention
```

### Primary preregistered causal signature — Candidate Causal Separability

```text
CCS = 0.5 * [
  (|self_A| - |cross_A|) / (|self_A| + |cross_A| + eps)
+ (|self_B| - |cross_B|) / (|self_B| + |cross_B| + eps)
]

Coverage = min(|self_A|, |self_B|)
           / (max(|self_A|, |self_B|) + eps)
```

Interpret the coefficient pattern and confidence intervals, not a post-hoc threshold.

Frozen signatures:

- **H1:** high candidate selectivity + substantial balanced Coverage for both candidates.
- **H3:** one candidate strongly causal but low/asymmetric Coverage for the competitor; asymmetry follows prespecified order/bias manipulation.
- **H2:** candidate-specific Coverage weak for both before resolution, despite intact entity comprehension, plus a shared unresolved-state intervention that moves both candidates jointly.

### J3 — shared unresolved-state test

Independently derive an ambiguity-state subspace from ambiguous-vs-resolved training pairs with candidate identities and antecedent direction balanced out. Require held-out structural-family transfer.

```text
JointCoupling = min(|delta score_A|, |delta score_B|)
                / (max(|delta score_A|, |delta score_B|) + eps)
```

H2 predicts low candidate-specific Coverage but high cross-item/shared JointCoupling. H1 predicts candidate-specific causal availability dominates. H3 predicts commitment asymmetry dominates.

### J4 — resolution transition

On aligned ambiguous/resolved pairs, test whether resolution:

- prunes one already-causal branch (H1),
- fills/refines an underspecified state (H2), or
- reinforces/reverses an existing winner (H3).

The headline result is the **causal representation signature**, never the best layer.

## K. Story invariance

- **Result A — parallel alternatives:** LLMs preserve multiple causally active referents and later prune them when evidence arrives.
- **Result B — underspecified state:** LLMs carry a compact unresolved reference state and instantiate a candidate-specific interpretation only after disambiguation.
- **Result C — early commitment:** LLMs internally commit before evidence licenses commitment; ambiguity awareness is downstream/separate.

All outcomes answer exactly:

> **How do LLMs represent unresolved linguistic reference?**

No outcome requires retitling the project as benchmark validity, prompt sensitivity or layer localization.

## L. Fatal controls / hard kills

1. **Order bias:** use all published It Depends candidate permutations; no single ordering is sufficient.
2. **Entity identity:** candidate effects must generalize over held-out names/noun phrases.
3. **Verb/template semantics:** the signature must generalize across AmbiCoref structural families; a single IC-verb direction is insufficient.
4. **Basic comprehension:** entity/distractor comprehension must pass a frozen capability denominator.
5. **Prompt/readout confound:** forced candidate scoring and free generation are separate; wording such as `I am unsure` is not evidence for an internal ambiguity state.
6. **Shuffled donor/random subspace:** all causal claims require matched controls.
7. **Direction validity:** decodability without held-out causal validation is insufficient.
8. **H1-vs-H2 identifiability:** if candidate Coverage and shared-state JointCoupling cannot robustly distinguish explicit alternatives from underspecification, terminate the architecture claim rather than shrinking to `ambiguity is represented somewhere`.
9. **Novelty kill:** any new work that already causally factorizes parallel-vs-underspecified-vs-commitment for unresolved linguistic reference terminates 038.
10. **No biological identity claim:** theory-signature alignment supports analogous computation, not human-neural equivalence.

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

Registration freezes the headline and architecture-level alternatives. A null may kill measurement/identifiability, but may not turn 038 into a Correct-Detect mechanization or layer-localization paper.
