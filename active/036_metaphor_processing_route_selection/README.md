# 036 — What Selects a Metaphor's Processing Route? Conventionality vs Aptness

Status: **PASS-REGISTER / GPU AUTHORIZED**  
Date: 2026-09-01

## A. Natural question

When a language model understands a metaphor, what determines whether it treats the expression as a **comparison between two concepts** or as **categorization under an abstract metaphorical category**: the vehicle's conventionality, the topic–vehicle pair's aptness, or neither in a discrete route-switching sense?

No benchmark name is needed to state the question. This is a long-standing psycholinguistic debate about metaphor comprehension.

## B. Why this is paper-scale

Metaphor comprehension has two major process accounts. On a comparison/structure-mapping account, the topic and vehicle are aligned and relational/common structure is projected. On a categorization account, the vehicle names or evokes an abstract category and the topic is treated as a member of that category.

The central unresolved question is not merely whether both processes are possible, but **what selects between them for a particular metaphor**.

The `Career of Metaphor` predicts that conventionalization changes the mode of processing: novel metaphors favor comparison, while conventional metaphors can be understood by categorization. Competing work argues that **aptness**, rather than conventionality, determines whether categorization is available; other accounts have proposed interpretive diversity or graded/single-process alternatives.

The contribution is therefore not `a metaphor benchmark works/fails -> find metaphor heads`. It is:

> **What property selects the computation used for metaphor comprehension in LLMs?**

A conventionality-driven answer, an aptness-driven answer, or a failure of discrete route switching would each change how we understand figurative composition in LLMs.

## C. Scientific lineage

The question predates neural language models.

### Conventionality / Career-of-Metaphor account

Bowdle & Gentner (2005), *The Career of Metaphor*, proposes that metaphor processing shifts from comparison to categorization as a metaphorical vehicle becomes conventionalized.

- novel metaphor: online comparison / structure mapping;
- conventional metaphor: an established metaphorical category can be accessed and used for categorization;
- grammatical concordance predicts that comparison is naturally expressed by a simile (`X is like Y`) while categorization is naturally expressed by a metaphor (`X is Y`).

### Aptness account

Jones & Estes (2006), *Roosters, robins, and alarm clocks*, orthogonalized conventionality and aptness. Across form preference, comprehension speed/ease, and category-membership judgments, aptness predicted processing while conventionality did not reliably do so.

Glucksberg/Haught and related categorization accounts likewise argue that highly apt topic–vehicle pairings can support categorization even when novel.

### Broader selector debate

Utsumi (2011), *Computational Exploration of Metaphor Comprehension Processes Using a Semantic Space Model*, explicitly formulates the scientific question as which metaphor property selects comparison vs categorization and contrasts conventionality, aptness, and interpretive-diversity accounts. The paper notes that the debate is unresolved and uses human interpretation plus computational models rather than neural-LM causal evidence.

This mature external debate is the source of 036's hypotheses.

## D. Strong mothers / established LLM object

### Mother 1 — 2026 modern-open-family metaphor norms

`LLMs replicate metaphor norms based on word co-occurrence but struggle with topic-vehicle mappings` (Frontiers in Language Sciences, 2026) evaluates eight current open-weight models on human metaphor norms.

Relevant open families include:

- `Mistral-Small-3.2-24B-Instruct-2506`;
- `Qwen3-32B`;
- `Llama-3.3-70B-Instruct`;
- additional Apertus / Qwen3-Next / gpt-oss models.

The study uses a 300-item human-normed metaphor set and reports stable nontrivial aptness judgments on the full set. For example, aptness-in-context reliability (ICC) is 0.91 for Mistral-Small-3.2-24B, 0.78 for Qwen3-32B, and 0.96 for Llama-3.3-70B. Human-model aptness correlations are significant but imperfect (roughly 0.24, 0.41, and 0.36 respectively in context), leaving substantial non-ceiling variation rather than a trivial copied scale.

The paper explicitly states that prompts, datasets and analysis scripts are publicly available at OSF (`https://osf.io/bmnyw`).

Crucially, this mother asks whether LLM-generated norms are reliable/valid substitutes for human psycholinguistic norms. It does **not** test comparison vs categorization, does not contrast conventionality against aptness as a route selector, and contains no mechanistic factorization of that debate.

### Mother 2 — Findings ACL 2025 broad metaphor interpretation

`Metaphor and Large Language Models: When Surface Features Matter More than Deep Understanding` evaluates metaphor interpretation over multiple public datasets/tasks and releases code/data at `elisanchez-beep/metaphorLLM`.

The public configuration includes open checkpoints from multiple genuinely different families:

- Meta-Llama-3-8B / 70B;
- Mistral-7B;
- Qwen2.5-7B / 72B;
- Gemma-3-4B / 27B.

This establishes that metaphor interpretation itself is a broad modern-LLM object, while its headline concerns surface-feature dependence rather than the conventionality-vs-aptness process-selection debate.

### Mother 3 / nearest LLM analysis — ACL 2026 Main

`Probing Semantic Alignment, Lexical Invariance, and Syntactic Influence in LLM Metaphor Processing` studies semantic alignment, stable lexical anchors and syntactic sensitivity, including novelty-related analyses. It suggests that lexical anchors may help familiar/conventional metaphors while biasing novel cases requiring contextual integration.

This is an important N2 warning, but it still does not manipulate aptness independently of conventionality, does not contrast comparison with categorization, and does not ask what selects between those computations.

## E. Exact novelty delta — N0 / N1 / N2

### N0 — object ownership

No 2025–2026 LLM paper found owns the headline question:

> `Does conventionality or aptness select comparison vs categorization in LLM metaphor comprehension?`

Recent LLM work owns metaphor task performance, human-norm replication, lexical anchoring, semantic alignment, novelty effects, and syntactic sensitivity.

### N1 — causal occupancy

No strongest neighbor found performs a theory-diagnostic causal intervention that distinguishes comparison from categorization as a function of conventionality vs aptness on modern open-weight LLMs.

### N2 — delta width

The project is not:

> `ACL'26 found lexical anchors; we locate their heads.`

The concept-level delta is:

> `LLMs can process/rate metaphors, and may show lexical/contextual effects`
> **→ `Which externally theorized property selects the kind of computation used for metaphor comprehension?`**

Conventionality and aptness were explicitly designed to be separable in the human theory literature and make opposing predictions when orthogonalized. The new scientific object therefore exists independently of the recent LLM mothers.

## F. Venue-scale comparison

- **NAACL 2025 — taxonomy vs similarity in property inference:** an established cognitive-science competition is brought to LMs and causal evidence adjudicates it. 036 has the same shape: conventionality vs aptness as competing selectors of comparison/categorization.
- **EMNLP 2025 Outstanding — shared filler-gap structure:** a mature external theory question exists before the LM experiment; causal intervention tests abstract computation. 036 likewise imports a mature metaphor-processing debate rather than inventing a layer taxonomy.
- **ACL 2026 Main — tool irrelevance:** a controlled design orthogonalizes natural factors that otherwise correlate. Jones–Estes' conventionality × aptness design plays the same role: the 2×2 does not create the scientific variables; it separates two real psycholinguistic factors.
- **ACL 2025 Outstanding — contextual entrainment:** broad behavior precedes causal explanation. Here broad modern-open metaphor competence/norm sensitivity is already established before mechanism work begins.

The question remains intelligible and paper-scale after every dataset name is removed.

## G. Data / substrate

### Primary theory-diagnostic substrate — Jones & Estes 2006

The paper publishes its exact experimental stimuli in the Appendix.

It contains **64 high/low-aptness pairs = 128 metaphor sentences**, with:

- 32 sentences in each cell of a natural 2 × 2 design:
  - high conventionality / high aptness;
  - high conventionality / low aptness;
  - low conventionality / high aptness;
  - low conventionality / low aptness;
- per-item vehicle-conventionality ratings;
- per-item aptness ratings for the high- and low-apt topic variants;
- identical vehicle within each high/low-aptness pair, so aptness changes while vehicle conventionality is held fixed;
- both **metaphor** and matched **simile** grammatical forms in the original human experiments;
- human validation through form preference, comprehension latency/ease, and category-membership experiments.

Example natural cross-cells from the released Appendix include conventional/high-apt `Some runners are cheetahs`, conventional/low-apt `Some skaters are cheetahs`, novel/high-apt `That fashion model is a rail`, and novel/low-apt `That football player is a rail`.

The 2×2 is not synthetic manufacturing for this project: it is a published human psycholinguistic design created specifically to orthogonalize the competing scientific variables.

### External/naturalistic validation

- Roncero & de Almeida (2015): 84 topic–vehicle pairs with human aptness, familiarity, conventionality, interpretive-diversity and semantic-property norms, with supplementary materials.
- `Figurative Archive` (Scientific Data 2025): 996 metaphor items, harmonized psycholinguistic ratings, original study spreadsheets, CSVs and code released through Zenodo (`10.5281/zenodo.14924803`), providing a broader external-validity route.
- 2026 300-item metaphor norming dataset + open-model outputs/scripts at OSF.

```yaml
natural_or_synthetic: human-designed psycholinguistic stimuli with human ratings; natural scientific variables
central_gold: Jones–Estes item-level conventionality/aptness ratings and validated 2x2 cells
row_level_artifact: exact 128 stimuli printed in publication Appendix; additional public OSF/Zenodo datasets
open_checkpoint:
  - Mistral-Small-3.2-24B-Instruct-2506
  - Qwen3-32B
  - Llama-3.3-70B-Instruct
modern_open_family_evidence: published 2026 stable aptness judgments on all three families; broad metaphor interpretation also established on Llama/Mistral/Qwen/Gemma in ACL 2025
why_dataset_is_only_a_measurement_window: comparison, categorization, conventionality and aptness are pre-existing psycholinguistic objects
external_validity_path:
  - 84-item Roncero/de Almeida semantic-property norms
  - 300-item modern norm set
  - Figurative Archive
  - additional nominal/predicate metaphor datasets
```

## H. Competing mechanisms and frozen predictions

### H1 — Conventionality-selected Career-of-Metaphor route

Vehicle conventionality determines whether an accessible metaphorical category exists.

Predictions:

- low-conventionality / novel metaphors rely more strongly on a comparison-like computation shared with their simile counterparts;
- high-conventionality metaphors show a more distinct categorization computation relative to matched similes;
- causal cross-form non-interchangeability therefore increases with conventionality after controlling aptness;
- changing aptness while holding vehicle conventionality fixed can affect success/difficulty but should not be the principal selector of the route.

### H2 — Aptness-selected categorization route

Apt topic–vehicle relationships enable a useful ad-hoc/metaphorical category regardless of conventionality; low-aptness expressions require comparison or fail to support categorization.

Predictions:

- high-aptness metaphors show stronger metaphor-vs-simile causal route differentiation;
- low-aptness metaphors are more causally interchangeable with their matched simile/comparison form;
- this pattern follows aptness even within the same vehicle, including novel but highly apt metaphors;
- conventionality contributes little once aptness is controlled.

### H3 — No discrete selector / graded single-process contextual integration

The model does not implement a clean comparison-vs-categorization route switch indexed by either factor. Lexical salience, contextual integration, or a graded mixture supports all cases.

Predictions:

- cross-form causal signatures change smoothly or idiosyncratically rather than according to the 2×2 selector factors;
- both conventionality and aptness may affect output difficulty without producing the predicted route-specific causal interaction;
- lexical/contextual controls explain more variance than either route-selector account.

These are computation-level alternatives, not early/middle/late localization labels.

## I. Frozen S0 / causal microscope

### S0-0 — broad capability / premise (already satisfied)

No experiment is needed to discover whether modern open LLMs can engage with metaphor or human aptness structure.

Published evidence already shows:

- broad metaphor interpretation across Llama/Mistral/Qwen/Gemma families (ACL 2025);
- reliable nontrivial aptness judgments on Mistral-Small-3.2-24B, Qwen3-32B and Llama-3.3-70B (2026 norming study), with significant but non-ceiling human alignment.

### S0-1 — frozen primary cells

Use **all valid Jones–Estes Appendix items** in the four preregistered cells. Do not select items by model effect.

Factor definitions are the human norms, not model ratings:

1. conventional / high apt;
2. conventional / low apt;
3. novel / high apt;
4. novel / low apt.

Keep each high/low-aptness pair linked by its shared vehicle.

### S0-2 — frozen grammatical-form microscope

For each item use the two forms already used in the human theory literature:

- metaphor: `X is Y`;
- simile: `X is like Y`.

The topic and vehicle are identical across forms. The simile is the theory-defined comparison-concordant form; the metaphor is the categorization-concordant form.

Primary behavioral readout is frozen to a forced-choice / logit-based version of the original **category-membership** diagnostic, with the exact same response format across conditions. A secondary behavioral diagnostic may reproduce metaphor-vs-simile form preference. Neither is used to redefine cells.

### S0-3 — hard measurement gate

Before expensive causal sweeps, on at least two of the published modern families (primary: Qwen3-32B and Mistral-Small-3.2-24B; Llama-3.3-70B as replication if feasible):

- basic comprehension/category judgments must show non-degenerate variance;
- low-aptness items must not reduce to unparseable/nonsensical floor performance;
- metaphor/simile response format must be understood;
- the model must retain the already-established ability to make stable metaphor-related judgments.

If these fail, terminate the checkpoint/project rather than search prompts/subsets to manufacture the theory effect.

This is reproduction/measurement of a frozen Route-A question, not behavior discovery.

## J. First mechanistic experiment contract

The first causal test is fixed before GPU use.

1. Run each Jones–Estes item in matched metaphor and simile form using the same frozen category-membership readout.
2. Record residual-stream/attention states at matched topic and vehicle positions across all layers; do **not** choose a best layer from behavioral effect.
3. Perform bidirectional matched-form activation patching at the vehicle/integration state:
   - simile donor -> matched metaphor recipient;
   - metaphor donor -> matched simile recipient.
4. Measure the absolute causal change in the category-membership logit and integrate it across model depth (AUC), yielding a preregistered **cross-form causal non-interchangeability** score per item rather than a `best layer` statistic.
5. Fit the frozen 2×2 model to this causal score using the human-defined factors.

Primary discriminating statistic:

```text
route_selector_index =
    beta_conventionality(cross_form_causal_noninterchangeability)
  - beta_aptness(cross_form_causal_noninterchangeability)
```

with the two binary factors coded symmetrically from the published 2×2 design.

Predictions:

- H1 Career / conventionality selector: `beta_conventionality > beta_aptness`, hence positive selector index;
- H2 aptness selector: `beta_aptness > beta_conventionality`, hence negative selector index;
- H3 single/graded computation: both route-selective coefficients small/unstable after controls, or neither yields the predicted cross-form causal structure.

The full coefficient pattern and confidence intervals are reported; no post-hoc threshold converts a weak result into a discrete route claim.

### Secondary causal confirmation

Only after the primary interaction is evaluated:

- test whether a form-derived causal state transfers across different lexical vehicles within the same theory-defined cell;
- test Roncero/de Almeida items as external validation using their semantic-property norms;
- analyze pathway/head localization as explanatory detail, never as the headline result.

## K. Story invariance

- **Result A — conventionality dominates:** LLM metaphor processing supports a Career-of-Metaphor-like route shift: conventionalized vehicles enable categorization, while novel metaphors remain more comparison-like.
- **Result B — aptness dominates:** route selection follows the quality of the topic–vehicle mapping rather than lexical conventionalization; even novel but apt metaphors can be categorization-like.
- **Result C — neither discrete selector dominates / mixed result:** apparent metaphor competence is implemented by a graded or heterogeneous computation not organized by the classic discrete selector accounts.

All three results answer exactly:

> **What selects the computation used to understand metaphors in LLMs?**

No result requires changing the headline to a benchmark failure, lexical-anchor localization, or a particular layer.

## L. Fatal controls / hard kills

1. **`like` lexical-token control.** Cross-form causal effects must not be reducible to the extra token `like`. Include literal comparison/category controls with the same `is` vs `is like` contrast and matched lengths.
2. **Basic comprehensibility control.** Low-aptness items must still permit the task; effects caused solely by nonsense/floor behavior do not support H2.
3. **Shared-vehicle pairing.** Aptness effects must survive within-vehicle comparisons, the key design feature that separates aptness from conventionality.
4. **Lexical frequency/familiarity control.** Conventionality cannot be silently replaced by raw token frequency; include available human familiarity/frequency covariates where possible.
5. **Shuffled-donor control.** Cross-form patch effects must exceed shuffled lexical donors and same-form irrelevant donors.
6. **No best-layer selection.** Primary causal statistic uses the frozen across-depth AUC; layer/head localization is secondary.
7. **No metaphor-benchmark rescue.** If Jones–Estes cells are not measurable on the prespecified modern checkpoints, do not switch to a benchmark subset and rewrite the question.
8. **Novelty kill.** If a newly found 2025–2026 neighbor causally adjudicates conventionality-vs-aptness selection of comparison/categorization in modern open LLMs, terminate for novelty.

## Registration verdict

```yaml
paper_scale: PASS
benchmark_removal: PASS
natural_object: PASS
venue_comparators: PASS
N0_object_ownership: PASS
N1_causal_occupancy: PASS
N2_delta_width: PASS
substrate: PASS
central_human_gold: PASS
natural_cross_cells: PASS
modern_open_model_premise: PASS
open_family_evidence: PASS
route_A_omitted_axis: PASS
story_invariance: PASS
competing_mechanisms: PASS
frozen_S0_contract: PASS
frozen_first_causal_statistic: PASS
fatal_controls: PASS
verdict: PASS-REGISTER
GPU_AUTHORIZED: true
```

Registration freezes the scientific question and first causal test. GPU may now be used only to answer this question; nulls must terminate/answer the same question rather than trigger a new metaphor story.
