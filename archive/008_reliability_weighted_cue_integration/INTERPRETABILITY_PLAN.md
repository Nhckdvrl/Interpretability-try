# 008 — Reliability-weighted multimodal cue integration

## Complete mechanistic-interpretability plan

**Plan status:** historical only; project killed and archived before white-box experiments

**Primary models:** `Qwen/Qwen3-VL-2B-Instruct`, `google/gemma-3-4b-it`
**Last literature and design review:** 2026-08-27

## 1. Research objective

The project asks:

> Where in an open vision-language model does reliability information from visual and textual measurements form, and why does it sometimes control cue selection without producing reliability-weighted integration?

The mechanism must be decomposed into four stages:

1. access/extraction of each cue value;
2. representation of each cue's spread or precision;
3. reliability-dependent routing or cue selection;
4. continuous weighted integration and numeric readout.

The study is not intended to make a generic text-dominance claim. Behavioral cue-combination and large-scale text–vision conflict benchmarks already exist, and causal work has begun mapping visual information routes. The intended contribution is a causal, architecture-aware decomposition of **mean**, **precision**, **gate**, and **integration**, followed by a reliability-specific rescue.

Closest overlap:

- [Emergent Bayesian Behaviour and Optimal Cue Combination](https://arxiv.org/abs/2512.02719)
- [SIGNPOST-Bench](https://arxiv.org/abs/2608.04244)
- [Pathways of Visual Information Flow in Vision-Language Models](https://arxiv.org/abs/2607.03358)
- [Who Wins the Conflict? Mechanistic Interpretability of Text Bias in Audio LLMs](https://arxiv.org/abs/2606.18924)
- [Decodable Is Not Grounded](https://arxiv.org/abs/2606.31257)

## 2. Current evidence and why G1 must change

### 2.1 Frozen G0 result

The current G0 reports:

| Model | Image readout MAE | Text readout MAE | Weight MAE | Five-regime correlation |
|---|---:|---:|---:|---:|
| Qwen3-VL-2B | 1.82 | 0.024 | 0.556 | -0.459 |
| Gemma3-4B | 2.52 | 0.56 | 0.400 | +0.802 |

Qwen's combined estimate is almost always equal to its text-only estimate; Gemma adjusts somewhat with reliability but systematically underweights the image.

### 2.2 Access asymmetry in the current prompt

The current text cue includes nine readings **and explicitly states their mean**. The image cue shows nine dots and requires visual localization plus averaging. Therefore combined behavior conflates:

- modality preference;
- explicit scalar copying;
- visual value extraction;
- arithmetic cost;
- reliability use.

In Qwen, 58/60 combined responses are numerically identical to the text-only response. This is primarily evidence for an explicit scalar access/copy shortcut, not yet evidence that a correctly represented image reliability is ignored.

### 2.3 Exploratory matched-access diagnostic

A 12-item exploratory control found:

- removing the explicit text mean removes exact text copying;
- rendering `IMAGE SENSOR MEAN = x.x` inside the image gives 12/12 accurate image-only mean readout;
- when both means are explicit, Qwen copies the image mean on 5 items and the text mean on 7 items;
- it selects the actually more reliable cue on 9/12 items, but rarely returns a genuine intermediate weighted average.

This is too small for a confirmatory result, but motivates a stronger candidate phenotype:

> after scalar access is matched, reliability may drive winner-take-all cue selection rather than continuous inverse-variance integration.

### 2.4 Statistical problems in the current score

The per-item observed weight

\[
\hat w_v=\frac{y-\hat\mu_t}{\hat\mu_v-\hat\mu_t}
\]

is unstable when the two unimodal estimates are close. In the current Gemma run, 14 of 47 analyzable weights are negative. The reported `0.802` correlation uses only five condition-level points. It is an exploratory trend, not strong evidence that Gemma internally estimates reliability.

The current oracle also uses hidden generating sigmas. The model sees only nine realized readings, so the primary mechanism dataset must use exactly controlled **visible sample spread** or explicitly supplied reliability statistics.

The generator also samples, clips, and rejects cases until `|image mean - text mean| >= 4`. This conditions different reliability regimes on different tail events and entangles realized spread, cue conflict, and hidden sigma. G1 must use deterministic affine construction with no clipping and no rejection sampling. Current image MAEs in the summary are computed only after the observed-weight denominator filter (36/60 Qwen and 47/60 Gemma), not over all 60 trials, so they must not be reused as unconditional accessibility estimates.

## 3. High-level causal model

For visual and textual cues let:

- \(\mu_v,\mu_t\): cue means;
- \(s_v,s_t\): visible sample standard deviations;
- \(r_v=1/(s_v^2+\epsilon), r_t=1/(s_t^2+\epsilon)\): operational precisions;
- \(w_v=r_v/(r_v+r_t)\): inverse-variance image weight;
- \(y=w_v\mu_v+(1-w_v)\mu_t\): fused estimate.

The mechanistic graph is:

```text
image samples ─> image value μv ───────────────────────┐
             └─> image precision rv ─┐                │
                                     ├─> gate wv ─────┼─> fused estimate y
text samples  ─> text precision rt ──┘                │
             └─> text value μt ────────────────────────┘
```

This graph separates a failure to perceive a value, a failure to represent precision, a failure to route precision into a gate, and a failure to perform continuous integration.

## 4. Competing mechanistic hypotheses

### H1 — Visual value-access bottleneck

The combined prompt uses the explicit text mean because visual mean extraction is weaker or more costly.

Predictions:

- raw/raw behavior is less text-captured than current G0 but noisier overall;
- summary/summary behavior changes sharply once image mean access is matched;
- image mean is weak or late before the projector/query path in raw images;
- explicit image mean creates a strong value path without necessarily improving reliability use.

### H2 — Precision-formation failure

The model represents cue means but does not form a generalizable representation of one or both spreads/precisions.

Predictions:

- mean probes and mean patches succeed;
- spread probes fail cross-template/layout or are explained by surface features;
- matched spread patches do not alter conflict behavior;
- explicitly supplying both SDs produces a large upper-bound improvement.

### H3 — Decodable but unused precision

Precision is represented, but its natural path to the gate/integration computation is weak.

Predictions:

- precision is cross-template decodable and image-dependent;
- natural precision swap has weak causal effect on the combined answer;
- explicit-stat bridge or path-gain intervention restores reliability-dependent weighting;
- mean paths remain intact.

### H4 — Reliability-controlled hard gating

The model uses reliability to select one accessible cue rather than computing an intermediate weighted estimate.

Predictions:

- outputs cluster at \(\mu_v\) or \(\mu_t\);
- reliability changes cue-selection probability rather than a continuous weight;
- a gate state is causal, but no stable weighted-sum state appears;
- intervention on the gate switches which mean path reaches the answer.

### H5 — Weighted state exists but numeric readout fails

An appropriate intermediate \(w_v\) or \(y\) is present, but late numeric generation/copy circuits overwrite it.

Predictions:

- fused estimate is decodable and naturally patchable before output;
- later text-number/copy paths dominate the generated answer;
- late path ablation or transplant exposes the already-computed fused value.

These alternatives define valid result-dependent narratives. The project should not force H3 if H1, H2, H4, or H5 better explains the evidence.

## 5. Phase 0 — Symmetric G1 mechanism dataset

### 5.1 Exact realized statistics

Construct a library of nine-element residual templates \(u_k\) satisfying:

- exact sample mean `0`;
- exact sample standard deviation `1` under the scorer's convention;
- mirrored and permuted variants;
- no clipping after transformation.

Generate readings as:

\[
x_{m,k}=\mu_m+s_m u_k, \qquad m\in\{v,t\}.
\]

Choose safe means/spreads so all readings remain in `[0,100]`. Store exact realized mean and SD in the manifest and test them numerically.

Suggested frozen factorial:

- center \(c\in\{35,50,65\}\);
- conflict \(\Delta=\mu_v-\mu_t\in\{\pm6,\pm12,\pm24\}\), with `|Δ|=12` designated as the primary mechanism contrast;
- reliability pairs `(2,8), (4,8), (6,6), (8,4), (8,2)`;
- 12 residual-template families, balanced over mirror/permutation;
- image-first and text-first prompt layouts;
- raw/raw and summary/summary access conditions.

Set \(\mu_v=c+\Delta/2\) and \(\mu_t=c-\Delta/2\). Within each contrast this keeps conflict magnitude fixed and prevents “higher number” from being confounded with “more image reliance.” Add congruent \(\mu_v=\mu_t\) controls for every reliability regime.

Conflict magnitude must be modeled rather than treated as a nuisance. Under sufficiently discrepant cues, hard selection can be a rational response to an implicit common-cause versus separate-cause inference problem, not a failure of Gaussian cue fusion. The primary fusion claim therefore uses moderate, in-family conflicts; the small/large contrasts test whether winner-take-all behavior emerges only when a common-source assumption becomes implausible. The prompt must state that both sensors measure the same unknown value, but this statement does not remove the need for the magnitude analysis.

The full behavior grid may be generated once, but mechanism discovery should use a balanced subset of matched families. Hold out entire residual-template families and at least one center for confirmation.

### 5.2 Access conditions

Use three interfaces:

1. **raw/raw:** image shows nine points; text gives nine values; neither mean is stated;
2. **mean/mean:** both raw samples remain visible, text states its mean, and the image renders its mean with matched precision/prominence;
3. **stats/stats bridge:** both modalities explicitly provide mean and sample SD using matched formatting.

The third condition is an upper bound: it tests whether the language decoder can apply the weighting rule when all sufficient statistics are serialized. It must not be mixed with evidence that the raw model inferred the statistics.

Add two diagnostics: a `means-only` condition with no reliability evidence to estimate fixed modality prior, and a taught-rule condition explicitly stating that smaller visible spread means higher reliability. Compare these with natural wording instead of assuming the instruction is already understood.

### 5.3 Representation swap and nuisance controls

For selected families render the identical nine numeric values:

- as image positions;
- as image text/OCR numbers;
- as text tokens;
- with the modality assignments swapped.

Also vary:

- dot vertical order while preserving x-values;
- text reading order;
- ruler style, font, and benign layout;
- prompt wording and modality order;
- mean labels that are equally salient but irrelevant distractor numbers.

These controls separate modality, representation format, explicit scalar access, and surface salience.

Add spread-shape controls to separate true variance/precision from heuristics:

- same sample SD but different range;
- same range but different sample SD;
- same SD with one outlier versus symmetric deviations;
- same mean/SD under different residual kurtosis and ordering.

A state that only tracks range, maximum deviation, or an outlier token should not be named a precision representation.

In a smaller diagnostic block vary sample count while keeping sample variance fixed. If the task explicitly defines independent measurements, effective precision should scale approximately as \(n/s^2\), whereas a pure spread/range heuristic ignores \(n\). This block is diagnostic rather than part of the primary nine-sample claim.

Add same-modality cue-combination controls:

- text-list + text-list;
- visual-plot + visual-plot;
- cross-modal raw/raw;
- cross-modal mean/mean.

These determine whether hard selection or failed integration is a general two-cue computation or specifically a cross-modal routing effect. Use neutral `Sensor X/Sensor Y` names, mirror which modality is introduced first, and balance which cue mean is numerically higher, which side of 50 it lies on, and the sign of conflict. An image containing a written mean is an OCR/access diagnostic and must not, by itself, be treated as evidence for a visual-value route.

### 5.4 Behavioral subprobes

For every stimulus family measure separately:

- image-only mean readout;
- text-only mean readout;
- image-only spread/reliability judgment;
- text-only spread/reliability judgment;
- pairwise “which sensor is more reliable?” judgment with mirrored A/B mappings;
- combined numeric estimate;
- optional “closer to image or text?” diagnostic, never as the sole fusion measure.

Reliability judgment should use full candidate-continuation likelihood with mapping counterbalancing. It establishes explicit behavioral access but is not a substitute for internal causal analysis.

### 5.5 Numeric scoring

For the primary white-box metric, teacher-force all integer candidates `0 … 100` as complete continuations and normalize their sequence log-likelihoods. Record:

- expected estimate;
- candidate argmax;
- entropy;
- probability mass near image mean, text mean, and normative fused mean.

Validate the final conclusions with greedy open generation. The candidate scorer must verify prompt/candidate token-boundary stability and score every candidate's complete token sequence.

### 5.6 Behavior models

Replace unstable per-item ratios with a hierarchical cue-weight model. A primary parameterization is:

\[
\operatorname{logit}(w_v)=a+b\log(r_v/r_t),
\]

\[
y=\alpha+w_v\mu_v+(1-w_v)\mu_t+\varepsilon.
\]

Fit model-specific and access-condition-specific intercepts/slopes with stimulus-family bootstrap. Also fit a mixture model in which output selects \(\mu_v\), \(\mu_t\), or an intermediate integration component. Compare continuous-integration and hard-selection models by held-out likelihood.

Include conflict magnitude and its interaction with reliability in both models. Do not diagnose fusion failure from winner-take-all behavior that appears only at the largest cue discrepancy.

Interpretation:

- `a << 0`, `b ≈ 0`: fixed text prior;
- `a << 0`, `b > 0`: text prior plus reliability correction;
- reliability-dependent mixture probabilities concentrated on cue means: hard gating;
- stable intermediate mass and appropriate `b`: continuous integration.

The old per-item observed weight remains a visualization only.

### 5.7 Phase 0 output and decision

Freeze:

- residual templates and exact-stat tests;
- access conditions and prompts;
- counterfactual family IDs;
- discovery/dev/test splits;
- candidate scoring and hierarchical models;
- the raw behavior taxonomy: fixed prior, reliability correction, hard gating, or continuous integration.

Do not begin large-scale patching until at least one model shows a stable, symmetric-access phenotype that survives representation swaps and prompt mirroring.

## 6. Phase 1 — Representation timeline

### 6.1 Variables to decode

Probe:

- image mean \(\mu_v\);
- text mean \(\mu_t\);
- image log-spread/log-precision;
- text log-spread/log-precision;
- reliability log-ratio \(\log(r_v/r_t)\);
- cue-selection state;
- continuous weight \(w_v\);
- normative and model-predicted fused estimate \(y\).

Use regularized linear probes first. Since spread is a second-order statistic, add a frozen low-capacity quadratic probe as a diagnostic. A high-capacity MLP probe is not acceptable as primary representation evidence.

### 6.2 Required generalization

Train/test splits must hold out:

- target centers;
- residual-template families;
- visual layouts/fonts;
- prompt templates;
- reliability ratios;
- conflict direction;
- access conditions where testing cross-format alignment.

Include shuffled labels, pixel-level/simple summary baselines, token-position baselines, and probes trained on blank/constant images.

The blank-image control is mandatory because a probe or steering direction can encode a modality prior rather than grounded visual information. [Decodable Is Not Grounded](https://arxiv.org/abs/2606.31257) demonstrates exactly this failure mode.

### 6.3 Qwen3-VL-2B sites

Based on the current cached configuration/Transformers implementation, instrument:

- the 24-layer, hidden-size-1024 vision tower from patch embeddings onward;
- ViT blocks `5`, `11`, `17`, and the final vision block;
- the main visual merger producing hidden-size-2048 language inputs;
- the three DeepStack mergers/features;
- the DeepStack injections after language decoder layers `0`, `1`, and `2`;
- decoder image-token residuals across the 28-layer, hidden-size-2048 language model;
- final prompt/query residuals;
- answer-prediction residuals.

Re-audit exact module names and tensor shapes against the pinned Transformers revision before implementing hooks. In the current implementation the DeepStack addition is performed outside the ordinary language-layer module output; a hook on `language_model.layers[i]` alone may miss the post-layer addition. Instrument the DeepStack processing function or an equivalent pre/post injection boundary explicitly. Qwen's official description confirms that DeepStack fuses multi-level ViT features; omitting these streams could falsely imply that visual information is absent. [Qwen3-VL model card](https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct)

### 6.4 Gemma3-4B sites

Based on the current cached model config, instrument:

- all 27 hidden-size-1152 SigLIP vision layers, initially sampled coarsely then narrowed;
- vision output before and after the projector's spatial pooling;
- projector RMSNorm and 1152→2560 linear projection boundaries;
- the 256 image-token states;
- decoder residuals across the 34 text layers;
- image tokens, final query token, and answer-prediction token;
- local versus global-attention layers, including the current full-attention indices `5, 11, 17, 23, 29`.

Confirm the exact layer counts/module paths at runtime. The architecture uses a SigLIP vision encoder and multimodal projector before image tokens enter the decoder. [Gemma3 Transformers documentation](https://huggingface.co/docs/transformers/model_doc/gemma3)

Qwen versus Gemma results are two mechanistic case studies, not sufficient evidence that an architectural difference caused a behavioral difference. Architecture-level claims require within-model interventions on DeepStack/projector/routes or additional same-family models.

### 6.5 Phase 1 deliverables

- architecture-specific layer × site maps for means and precisions;
- cross-format and blank-image control matrices;
- emergence timeline for cue-selection/weight/fused-value states;
- a frozen shortlist of causal test sites.

Probe results answer only where a variable is decodable, not whether the model naturally uses it.

## 7. Phase 2 — Natural counterfactual patching

### 7.1 Matched intervention families

Construct donors that differ in exactly one high-level variable:

1. **image-mean swap:** same image spread, text cue, conflict magnitude class, layout, and access condition; change \(\mu_v\);
2. **image-spread swap:** same image mean and all text statistics; change \(s_v\);
3. **text-mean swap:** same text spread and image cue; change \(\mu_t\);
4. **text-spread swap:** same text mean and all image statistics; change \(s_t\);
5. **modality swap:** exchange matched numeric distributions between image and text;
6. **nuisance swap:** change residual permutation/layout while preserving means and spreads.

Use natural on-manifold donors, with clean→corrupt and corrupt→clean directions.

### 7.2 Primary causal double dissociation

The key confirmatory result is:

- a **mean patch** changes the combined estimate directly while spread is fixed;
- a **spread patch** changes the sensitivity/gain of the corresponding mean path during cue conflict, while producing little or no change on congruent trials.

Define the image-mean causal elasticity under reliability condition \(r\):

\[
G_v(r)=\frac{\Delta\mathbb E[y]}{\Delta\mu_v}
\]

and analogously \(G_t(r)\). The central interaction is whether patching reliability changes \(G_v\) or \(G_t\) in the normatively correct direction.

The preregistered image-path difference-in-differences is:

\[
\Delta_v=
\big[\text{image-mean patch effect}\big]_{\text{image reliable}}
-\big[\text{image-mean patch effect}\big]_{\text{image unreliable}},
\]

with a modality-mirrored \(\Delta_t\). Precision-controlled routing predicts positive, directionally mirrored interactions rather than a global increase in one modality.

This is stronger than asking whether a reliability patch changes the answer: precision should modulate a value path rather than directly encode the numeric answer.

### 7.3 Whole-state localization

Begin with whole-output patches at each architecture stage:

For Qwen:

- individual ViT block outputs;
- main merger output;
- each DeepStack stream separately;
- each early language-layer injection;
- later image-token and query-token residuals.

For Gemma:

- sampled SigLIP blocks;
- projector input/output;
- image-token residuals;
- decoder image/query/answer residuals.

Patch only matched token groups or named architecture tensors. Preserve all other visual streams when testing one Qwen DeepStack channel, and separately test joint patches to detect redundancy.

### 7.4 Outcomes

Report:

- change in expected numeric candidate value;
- full candidate-distribution KL/Jensen–Shannon divergence;
- probability-mass shift toward image, text, and fused means;
- cue-selection mixture probability;
- normalized recovery where donor and receiver are separated;
- reliability × mean-path interaction;
- behavior on congruent and unimodal controls.

### 7.5 Controls

- blank, constant, and naturally corrupted images;
- random image from the same visual-statistics family;
- nuisance-equivalent residual/layout donor;
- random layer/site and norm-matched vector;
- same mean and spread but different sample order;
- same reliability class but different modality;
- patches on both baseline-correct and baseline-incorrect cases;
- activation norm and distance-to-data-manifold diagnostics.

Attention knockout is only a coarse path screen. Visual-routing work shows that ablating one route can recruit a fallback route, revealing what the model could do rather than its normal computation. [Pathways of Visual Information Flow](https://arxiv.org/abs/2607.03358)

## 8. Phase 3 — Causal subspaces and stage tests

After whole-state causal sites are localized, train separate DAS/causal-alignment subspaces for:

- image mean;
- image precision;
- text mean;
- text precision;
- reliability log-ratio;
- cue-selection state or continuous weight.

Required tests:

- held-out target centers, residual templates, layouts, and prompt forms;
- cross-access evaluation where semantically justified;
- natural donor interchange-intervention accuracy;
- dimensionality and random-subspace controls;
- comparison with full-state patch effects;
- blank-image and modality-prior controls;
- separate mean and precision selectivity.

A precision subspace is accepted only if swapping it changes mean-path gain without directly injecting the answer value. Steering success alone does not establish natural use; subspace patches may activate dormant computation. See [Interpretability illusion for subspace patching](https://arxiv.org/abs/2311.17030).

## 9. Phase 4 — Components and information paths

### 9.1 Screening

Use AtP*/gradient-based attribution to rank:

- vision blocks/channels;
- multimodal merger/projector components;
- decoder attention heads and MLPs;
- image→query, text-number→query, and query→answer paths.

Use the expected numeric candidate value or a signed image-versus-text mass contrast as the differentiable metric. Attribution is only a shortlist mechanism; validate every reported component with exact patches.

### 9.2 Candidate routes

Test:

1. image samples → image-mean representation;
2. image spread → image-precision representation;
3. visual mean/precision through merger/projector/DeepStack;
4. text numeric tokens → text mean/precision;
5. image/text precision states → gate/query state;
6. gate → modulation of image/text mean paths;
7. mean paths → fused-value state;
8. fused-value or selected-cue state → numeric answer;
9. explicit text-mean token → copy circuit → answer.

The key path-level test is an interaction, not merely node importance: the causal contribution of an image-mean sender should grow when the image-precision/gate path indicates higher reliability.

### 9.3 Hard-gating diagnosis

If output mass clusters at cue means:

- identify heads/MLPs whose patches switch image-versus-text selection;
- test whether they receive precision information;
- verify that changing the gate leaves both unimodal values intact;
- test whether a latent intermediate weighted estimate exists elsewhere or is truly absent.

### 9.4 Late-copy diagnosis

If a fused estimate is causally present before output but text-copy wins late:

- patch/ablate exact text-number sender heads or MLP outputs;
- confirm that the previously computed fused estimate emerges;
- ensure general numeric generation remains intact;
- require selective improvement only under conflicting cues.

The audio-LLM result that text can actively suppress an intact non-text representation is a useful hypothesis, not something to assume. [Who Wins the Conflict?](https://arxiv.org/abs/2606.18924)

## 10. Phase 5 — Reliability-specific rescue

The final intervention must target the identified mechanism rather than globally increase visual attention.

Candidate rescues:

- amplify the image-precision→gate path only when image spread is smaller;
- restore a weak precision path through a merger/projector/DeepStack channel;
- soften a hard gate so both mean paths contribute continuously;
- weaken a late explicit-number copy path only when it conflicts with a validated fused state;
- transplant a same-example precision state from a reliability-readout prompt into the combined prompt as a sufficiency test.

Success requires:

- increased image weight when image is more reliable;
- no increased image weight when text is more reliable;
- stable equal-reliability and congruent behavior;
- stable image-only and text-only mean readout;
- minimal unrelated-task/output degradation;
- bidirectional effects under modality and reliability reversal;
- generalization to new means, residual templates, layouts, and prompts.

Report necessity, sufficiency, and selectivity. A global “more visual” steering vector that helps one image-reliable condition but harms text-reliable cases is not a successful mechanism repair.

## 11. External and second-task validation

After freezing the mechanism on the ruler/dot task, validate on one second continuous magnitude task, such as line length, spatial location, or an official BayesBench cue-combination subset.

Freeze in advance:

- expected stage of mean and precision formation;
- expected architecture site/path class;
- expected reliability × mean-path interaction;
- rescue direction and off-target controls.

The second task need not reproduce the exact same individual heads. The transferable claim should concern the computation stage and functional path: whether precision is formed, reaches a gate, and modulates cue-value gain.

Do not expand to generic multimodal hallucination, all forms of text dominance, or arbitrary visual reasoning.

## 12. Statistical plan

- Independent unit: matched stimulus/residual-template family.
- Freeze discovery/dev/test families before component selection.
- Use paired permutation tests for matched patches.
- Use cluster bootstrap by stimulus family for confidence intervals.
- Fit the hierarchical weight and cue-selection mixture models on all cases, not only analyzable denominators.
- Report condition-specific intercept/slope uncertainty rather than a correlation over five means.
- Correct architecture/layer/head scans using max-statistic permutation or FDR.
- Report whole-state, top-component, and circuit-size–faithfulness effects.
- Include both baseline-success and baseline-failure examples.
- Run trained probes/DAS with multiple seeds.
- Confirm the frozen circuit once on held-out families.

Primary confirmatory statistics:

1. mean-patch effect at fixed spread;
2. spread-patch × cue-conflict interaction;
3. reliability × mean-path causal elasticity;
4. intervention selectivity on congruent/unimodal controls;
5. held-out behavior-model improvement over fixed-prior and hard-selection baselines.

## 13. Result-to-narrative decision table

| Confirmatory result | Correct conclusion | Project decision |
|---|---|---|
| Image mean absent/late in raw but restored by explicit mean | Visual value-access bottleneck | Continue under access/routing narrative |
| Means present, precision not generalizably represented | Precision-formation failure | Continue if localized to a meaningful architecture bottleneck |
| Precision decodable/grounded but spread swaps do not affect mean-path gain | Decodable but unused reliability | Strong routing-failure result if controls pass |
| Reliability changes selection between intact cue means, with no intermediate weighted state | Reliability-controlled hard gating | Strong revised narrative |
| Weighted/fused state exists and is causal, but late copy path overwrites it | Numeric readout/copy competition | Continue with late-routing narrative |
| Symmetric access removes all reliable modality/reliability effects | Original G0 was an access artifact | Stop mechanism project unless a second task supplies a stable phenotype |
| Only probe/steering succeeds; natural patch and grounding controls fail | No faithful mechanism evidence | Do not claim a precision circuit |

The purpose is to locate where precision disappears, not to force a preselected “text dominance” explanation.

## 14. Compute-efficient execution order

1. **Phase 0a:** implement exact-stat residual templates and symmetric access prompts.
2. **Phase 0b:** run the full behavior grid on Qwen/Gemma and fit continuous-versus-hard-gating models.
3. **Phase 1:** cache all named architecture states once per stimulus; train probes offline.
4. **Phase 2:** whole-state mean/spread patches on a balanced discovery subset.
5. **Phase 3:** DAS only in causally localized sites.
6. **Phase 4:** AtP* shortlist followed by exact component/path patches.
7. **Phase 5:** selective rescue and one second-task validation.

Both models fit comfortably on one 98GB GPU. Use four single-GPU replicas for stimulus/counterfactual data parallelism. Keep Qwen and Gemma hook implementations separate because their visual injection mechanisms differ.

## 15. SAE policy

SAEs are not part of the primary plan.

Gemma Scope 2 provides relevant Gemma3-4B residual/attention/MLP SAEs and transcoders, but these were trained primarily on text/chat activations rather than the current multimodal image-token distribution. If used after the causal route is established, first test:

- reconstruction-induced task-score change;
- full-output KL;
- image/query-token reconstruction error;
- activation sparsity/dead features;
- distribution shift relative to text tokens.

Only feature interventions that preserve task behavior and reproduce the natural causal path may support a feature-level follow-up. Do not train a new Qwen SAE before the stage/path mechanism is established.

## 16. Planned artifacts

```text
mechanism/
├── configs/
│   ├── phase0_symmetric_behavior.json
│   ├── phase1_probes.json
│   ├── phase2_patching.json
│   └── frozen_confirmatory_split.json
├── data/
│   ├── residual_templates.json
│   ├── mechanism_manifest.jsonl
│   ├── counterfactual_pairs.jsonl
│   └── token_and_vision_shape_audit.json
├── stimuli/
│   ├── raw_raw/
│   ├── mean_mean/
│   └── stats_stats/
├── src/
│   ├── generate_mechanism_data.py
│   ├── candidate_scoring.py
│   ├── behavior_models.py
│   ├── cache_qwen.py
│   ├── cache_gemma.py
│   ├── probes.py
│   ├── patching.py
│   ├── path_patching.py
│   └── statistics.py
├── results/
└── tests/
```

Every result must record model revision, Transformers/PyTorch version, image processor settings, exact rendered stimulus, residual-template family, access condition, architecture site, donor/receiver IDs, intervention tensor shape, seed, and metric definition.

Minimum mechanism-test coverage:

- rendered and serialized values reproduce manifest means/SDs exactly;
- no clipping, rejection sampling, or unrecorded processor randomness;
- mean, spread, modality, and nuisance swaps preserve all declared invariants;
- conflict sign, modality order, sensor name, and center are balanced by family;
- raw prompts leak neither mean nor SD, while mean/mean and stats/stats are symmetric;
- paired images have identical processor grid/token topology where patching requires it;
- actual `input_ids`, image placeholders, and content order match the manifest;
- the visible-precision oracle and continuous integrator recover their known synthetic parameters;
- simulated text-copy, fixed-prior, continuous-fusion, and WTA outputs are distinguished by the behavior-model code;
- no trial is deleted because an inferred-weight denominator is small;
- complete multi-token candidate scoring matches a slow reference implementation;
- Qwen uses `enable_thinking=False` where supported;
- Qwen DeepStack and Gemma projector pre/post hooks have asserted shapes and locations;
- identity/no-op patches preserve logits within numerical tolerance;
- batched and single-example patching agree;
- manifests, donor pairs, splits, and results are reproducible from the frozen seed/config.

## 17. Paper-sized target claim

The strongest defensible target is:

> Open VLMs can preserve modality-specific cue values while losing precision at different stages of multimodal computation. Causal mean/spread interchange separates value extraction, precision formation, reliability gating, and weighted integration; architecture-aware path interventions reveal whether a model ignores precision, uses it for hard cue selection, or computes a fused value that is overwritten by a late copy route.

Suggested title:

> **Where Does Precision Disappear? A Causal Dissection of Reliability-Weighted Fusion in Vision-Language Models**
