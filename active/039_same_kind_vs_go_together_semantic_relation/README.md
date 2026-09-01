# 039 — Same Kind or Go Together? Taxonomic vs Thematic Semantic Relations

Status: **PASS-REGISTER / GPU AUTHORIZED**  
Date: 2026-09-01  
Route: **C — simple phenomenon / simple latent object first**

## A. Natural question

When an LLM says two things are “related,” does it internally distinguish **why** they are related?

- `dog — wolf`: they are related because they are the **same kind / same category** (**taxonomic** relation);
- `dog — leash`: they are related because they **go together in the same event or situation** (**thematic** relation).

The one-line paper question is:

> **Does an LLM represent “same kind” and “go together” as different, causally usable semantic relations, rather than one generic notion of relatedness?**

No benchmark name is needed to explain the object.

## B. Why this is paper-scale

Taxonomic and thematic relations are two major ways humans organize semantic knowledge. They support different downstream behavior: taxonomic relations support category/property generalization, while thematic relations support event/scenario expectations and contextual integration.

The distinction is simple but not trivial. Two pairs can be equally “related” overall while differing in relation type. A model may therefore:

1. encode a reusable **relation-type** variable;
2. encode only generic relatedness and reconstruct relation type task-by-task; or
3. mostly inherit surface similarity/co-occurrence statistics that correlate with the human distinction.

The contribution is not “we found a neuron for taxonomy.” It is a new model fact about whether a basic semantic relation type exists as a separable internal object and whether the model actually uses it.

## C. Independent scientific object

This object predates LLMs by decades.

Human semantic-memory research distinguishes:

- **taxonomic relations**: concepts share category membership/features, e.g. `dog—wolf`;
- **thematic relations**: concepts play complementary roles in a shared event/scenario, e.g. `dog—leash` or `helmet—motorcycle`.

The distinction has behavioral, neuropsychological, EEG/MEG/fMRI and intracranial evidence. Current cognitive work still studies whether the two rely on partly distinct semantic organization/processes.

Useful lineage:

- Estes, Golonka & Jones (2011), *Thematic Thinking: The Apprehension and Consequences of Thematic Relations*;
- Landrigan & Mirman (2016), *Taxonomic and Thematic Relatedness Ratings for 659 Word Pairs*;
- Zhang, Mirman & Hoffman (2023), taxonomic/thematic relations and feature types;
- Adezati et al. (2024), intracranial phase synchronization during taxonomic/thematic processing;
- 2026 Cortex work showing different timing/strength for the two relations in object naming.

The paper does **not** need to claim that LLMs implement the human dual-hub architecture. Human neuroscience establishes that the semantic distinction is scientifically real; our claim is about the model.

## D. Strong measurement windows

### D1 — primary gold: Landrigan & Mirman 659-pair norms

Public CC-BY human norms contain **659 word pairs / 300 target words**. Crucially, every pair has both:

- `Mean_Rating_Tx` — taxonomic similarity;
- `Mean_Rating_Thm` — thematic relatedness;
- `Difference_Score = taxonomic - thematic`;
- rating SDs and counts.

This is unusually clean Route-C substrate because the two axes were independently human-rated on the **same lexical pairs**. We do not have to splice together two benchmarks or ask an LLM judge what relation a pair has.

Repository DOI: `10.7910/DVN/FKTQ4C`  
Data paper: https://doi.org/10.5334/jopd.24

Primary analyses use the **continuous ratings**, not a post-hoc hand-picked binary subset.

### D2 — independent behavioral window: taxonomic–thematic triads

The classic similarity-choice paradigm presents one cue and two natural alternatives: one taxonomic and one thematic. A 2026 LLM cross-cultural-surrogate study runs this exact paradigm with eight model ecosystems including **LLaMA** and **Qwen**, showing that current LLMs can produce systematic taxonomic/thematic choices and explanations.

That paper’s scientific question is cultural-simulation fidelity, not LLM semantic representation. Here the triads are only an independent causal readout window.

Representative source: Zhang et al. (2026), *A Multi-Factor Evaluation of Fidelity in LLM-Based Cross-Cultural Surrogates*, DOI `10.21203/rs.3.rs-8799167/v1`.

### D3 — optional external validation

Use independent human semantic-relation materials only after the primary result is frozen, e.g. thematic production norms or matched taxonomic/thematic semantic-decision stimuli from the cognitive literature.

## E. Strongest-neighbor novelty attack — N0 / N1 / N2

### N0 — object ownership

Strong LLM neighbors own adjacent but different objects:

1. **NAACL 2025 — Characterizing the Role of Similarity in the Property Inferences of Language Models.**  
   Causal representational analysis of **taxonomy vs categorical similarity** in property inheritance.

2. **NeurIPS 2025 — Vision-and-Language Training Helps Deploy Taxonomic Knowledge but Does Not Fundamentally Alter It.**  
   Behavioral/representational analysis of **taxonomic vs non-taxonomic** questions while comparing LM/VLM pairs.

3. Older static-embedding work probes taxonomic information in taxonomic/thematic SGNS/GloVe spaces.

4. 2026 cultural-surrogate work uses a taxonomic/thematic triad task to evaluate **cultural fidelity**.

None of these owns the simple model question:

> **Does a modern autoregressive LLM maintain a reusable taxonomic-vs-thematic relation-type representation, separate from generic relatedness, and causally use it across tasks?**

A critical detail for the NeurIPS 2025 neighbor: its “non-taxonomic” negatives are sampled as concepts **outside the target’s WordNet hypernym chain**. They are not controlled thematic matches. Therefore that paper does not factorize `same kind` from `go together`.

### N1 — causal occupancy

The strongest causal neighbor (NAACL 2025 property inference) manipulates taxonomy/similarity in **property inheritance**. It does not test thematic relations or a relation-type state that transfers between neutral pair judgments and taxonomic-vs-thematic choice.

No 2025–2026 work found in the hard search causally patches/steers a **taxonomic-vs-thematic** semantic-relation state in modern open-weight LLMs.

### N2 — delta width

039 is not:

> “A cultural-simulation paper found a taxonomic/thematic choice effect; explain it internally.”

The core object comes from independent cognitive semantics, and the primary gold is the 2016 dual-rated pair norms. The 2026 triad paper is only evidence that modern LLMs can engage the distinction and an external readout window.

Likewise, 039 is not “do taxonomy MI again”: **thematic relatedness is the omitted natural axis** that taxonomy-only work does not isolate.

## F. Exact confounds that must be separated

A relation-type claim is invalid unless it survives the obvious alternatives:

1. **overall relatedness** — use both human ratings jointly; do not compare highly-related taxonomic pairs to weakly-related thematic pairs;
2. **lexical identity** — target/pair words must be disjoint across train/test splits where feasible;
3. **word frequency / length / tokenization / concreteness**;
4. **surface distributional co-occurrence / association strength** — thematic is not defined as mere PMI;
5. **generic embedding similarity** — taxonomic relation cannot silently reduce to cosine similarity;
6. **WordNet hierarchy distance** for the taxonomic side;
7. **explicit label leakage** — representation discovery uses neutral pair carriers, not prompts containing `taxonomic`, `thematic`, `same category`, or `same event`;
8. **prompt choice bias / option order** in triads — counterbalance A/B order and surface phrasing.

If the apparent relation axis disappears after matched overall-relatedness and distributional controls, the reusable semantic-relation claim is killed.

## G. Prespecified open models

First execution targets two MI-friendly open families:

- `meta-llama/Llama-3.1-8B-Instruct`;
- `Qwen/Qwen2.5-7B-Instruct` (14B may replicate if budget allows).

The paper question does not require a two-family effect to exist by assumption. The semantic axis is externally established and deterministic. However, a family contributes to the mechanistic claim only if it passes the frozen capability/causal gates below.

## H. Frozen S0 — obvious experiments first

### S0-1 — relation sensitivity

On the 659 human-normed pairs, before any circuit search, test whether a neutral pair representation/readout tracks the continuous human contrast:

```text
RelationType = z(Mean_Rating_Tx) - z(Mean_Rating_Thm)
OverallRelatedness = z(Mean_Rating_Tx) + z(Mean_Rating_Thm)
```

Use lexical-disjoint held-out evaluation and report continuous prediction, not a hand-selected best subset.

### S0-2 — behavioral use

On independent cue + two-option trials, require non-random sensitivity to which option is taxonomic vs thematic, with option order counterbalanced. The model need not prefer one relation globally; it only needs a measurable relation-sensitive decision surface.

### S0-3 — confound denominator

RelationType must add held-out information beyond preregistered nuisance controls for overall relatedness, lexical frequency/length/concreteness, static semantic similarity and corpus association/co-occurrence.

If both open families fail basic relation sensitivity after controls, terminate 039 rather than inventing a new semantic story.

## I. Minimal frozen causal contract

Route C does **not** require three elaborate architectures before registration. It does require a real causal-use question.

### I1 — learn the relation-type state without relation words in the prompt

At every layer, estimate a relation-type direction/subspace from **neutral word-pair carriers** using training pairs and continuous human `RelationType`, while residualizing `OverallRelatedness` and the frozen nuisance variables.

No layer is selected because it looks best on the test set. Held-out lexical targets validate the direction.

### I2 — first causal test: cross-task relation steering

Apply the training-derived relation edit in an **independent unlabeled triad-choice prompt**.

Primary readout:

```text
ChoiceLogit = log P(taxonomic option) - log P(thematic option)
```

Prediction for a reusable relation-type state:

- steering toward the taxonomic end increases `ChoiceLogit`;
- steering toward the thematic end decreases `ChoiceLogit`;
- matched random directions, shuffled labels and generic-relatedness directions do not reproduce the bidirectional effect.

Summarize the prespecified intervention across depth rather than choosing a best layer post hoc.

This is deliberately simple: **a relation axis learned from pair semantics must causally transfer to a different choice task.**

### I3 — representation is not enough

A probe that decodes RelationType but whose intervention does not affect held-out relation-sensitive decisions supports only passive decodability, not the paper’s causal-use claim.

## J. Result-invariant paper stories

- **Result A — reusable relation type:** same-kind vs go-together is represented as a cross-lexical semantic variable and causally transfers across tasks.
- **Result B — task-specific reconstruction:** relation type is decodable in some contexts but does not causally transfer; the model reconstructs the distinction from more local semantic features when a task requires it.
- **Result C — generic relatedness / distributional collapse:** after controls, apparent taxonomic/thematic sensitivity is explained by generic similarity/co-occurrence rather than a separable relation-type state.

All three answer exactly:

> **Does an LLM distinguish “same kind” from “go together” as a causally usable semantic relation?**

No result requires changing the headline to a benchmark, a layer, a cultural-bias story, or an SAE feature.

## K. Hard kill conditions

1. A newly found 2025–2026 work directly factorizes and causally manipulates taxonomic-vs-thematic relation type in modern open LLMs -> **KILL-NOVELTY**.
2. Human pair norms cannot be separated from generic relatedness / co-occurrence under the frozen controls -> **KILL-IDENTIFIABILITY**.
3. Basic held-out relation sensitivity is absent across the prespecified open families -> **KILL-BEHAVIOR for this substrate**.
4. Only explicit prompts containing relation labels reveal the distinction -> **KILL-LEXICAL-CUE**.
5. RelationType is decodable but no causally validated direction transfers to independent relation-sensitive behavior -> do **not** claim a reusable causal semantic state.
6. The only surviving result is a best-layer/neuron localization -> **KILL-SCALE**.

## L. Registration verdict

```yaml
route: C
paper_scale: PASS
benchmark_removal: PASS
natural_object: PASS
normal_scope: PASS
N0_object_ownership: PASS
N1_causal_occupancy: PASS
N2_delta_width: PASS
primary_human_gold: PASS
central_gold_without_llm_judge: PASS
natural_cross_axis: PASS
accessible_open_models: PASS
obvious_confound_controls: PASS
causal_use_question: PASS
story_invariance: PASS
frozen_S0: PASS
minimal_falsifiable_causal_contract: PASS
verdict: PASS-REGISTER
GPU_AUTHORIZED: true
```

Registration freezes the simple headline. Mechanistic detail may grow during execution, but it may not turn 039 into a taxonomy benchmark paper, cultural-simulation mechanization, generic relatedness probe, or best-layer story.
