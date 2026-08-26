# 006 — Bayesian latent inference → downstream use

## Complete mechanistic-interpretability plan

**Plan status:** ready for implementation after the Phase 0 behavioral refreeze
**Primary model:** `Qwen/Qwen2.5-14B-Instruct`
**Comparison models:** `Qwen/Qwen3-8B` and `google/gemma-3-12b-it`
**Last literature and design review:** 2026-08-27

## 1. Research objective

The project asks one narrow question:

> When a language model can elicit a sufficiently accurate posterior over a latent state, why does that quantity sometimes fail to control a minimal downstream policy decision, and why does serializing the posterior restore correct action?

The mechanistic study must not assume in advance that the direct prompt contains a causally used posterior. It must distinguish four stages:

1. posterior formation;
2. routing of posterior and threshold information;
3. comparison and semantic action selection;
4. binding of the semantic action to the requested surface label.

The intended contribution is not another behavioral demonstration of a belief–action gap. BayesBench already reports that gains in latent inference do not reliably transfer to downstream prediction, and recent work studies action–belief inconsistency and cross-axis routing failures. The novel claim must be an experimentally supported causal decomposition of what posterior externalization changes.

Closest overlap:

- [BayesBench: Evaluating LLM Belief Trajectories](https://arxiv.org/abs/2606.30850)
- [Knowing What You Know Is Not Enough](https://arxiv.org/abs/2511.13240)
- [CARD: Diagnosing Belief to Action Routing Failures](https://arxiv.org/abs/2608.20763)
- [Where's the Plan?](https://arxiv.org/abs/2605.07984)

## 2. Current evidence and limits

### 2.1 Frozen corrected G0

For Qwen2.5-14B:

- posterior MAE over 24 unique evidence states: `0.105`;
- inference-good, action-identified, non-boundary cases: `42`;
- direct action error: `14/42 = 33.3%`;
- bridged action error: `0/42`;
- bridge rescue among direct errors: `14/14`;
- mean bridged minus direct probability of the gold action: `+0.327`.

Qwen3-8B is primarily a posterior-estimation/report-poor behavioral comparison; its internal formation stage has not been diagnosed. Gemma3-12B is mostly behaviorally correct and serves as a bridge-sensitive/correct-action comparison.

### 2.2 Exploratory diagnostics completed after G0

These diagnostics guide the mechanism design but are not confirmatory evidence:

- all 14 Qwen2.5 direct errors are `WAIT → ACT` errors;
- 11/42 eligible cases change semantic prediction across the two A/B mappings;
- using the likelihood-distribution argmax rather than its expectation leaves the core result intact: approximately 43 eligible cases, 14 direct errors, and all 14 rescued;
- on the 14 error cases under both mappings, serializing the model's own likelihood-elicited posterior gives `28/28` correct decisions;
- presenting the same number as an irrelevant calibration identifier gives `5/28` correct decisions;
- replacing the serialized posterior with a counterfactual value across the threshold makes `27/28` variants follow the counterfactual action;
- neutral action pseudowords and predicate-clause reversal reveal substantial branch-order and label-mapping effects.

These diagnostics suggest that numerical content and semantic role interact, but the existing irrelevant-number control is not topology matched and cannot by itself exclude a contextual numeric-prime explanation. The current data also do **not** establish that the same posterior is formed and causally routed in the direct prompt.

### 2.3 Terminology discipline

The 101-candidate posterior distribution is fairly diffuse. Until a generated/argmax value and a cross-format representation agree, use:

- `likelihood-elicited posterior` for the normalized candidate expectation;
- `posterior argmax` for the highest-likelihood candidate;
- `generated posterior` for greedy numeric generation.

Do not use `reported posterior` as if all three were identical.

## 3. High-level causal model

Let:

- \(\pi\): prior probability of latent Type A;
- \(E\): observations;
- \(z=\operatorname{logit}P(A\mid E)\): posterior log-odds;
- \(t=\operatorname{logit}(\tau)\): threshold log-odds;
- \(d=z-t\): decision margin;
- \(s=\mathbb 1[d>0]\): semantic ACT/WAIT choice;
- \(m\): ACT/WAIT-to-A/B mapping;
- \(y=\operatorname{bind}(s,m)\): output label.

The proposed causal abstraction is:

```text
prior π ─┐
         ├─> posterior z ─┐
evidence ┘                ├─> margin d ─> semantic action s ─┐
threshold t ──────────────┘                                  ├─> output label y
surface mapping m ───────────────────────────────────────────┘
```

This graph defines the variables to decode, patch, and validate with interchange interventions. The relevant methodological foundation is [Causal Abstraction](https://arxiv.org/abs/2301.04709).

## 4. Competing mechanistic hypotheses

### H1 — Query-gated posterior formation

The posterior-report prompt elicits \(z\), but the direct action prompt never forms a comparable posterior representation. The bridge supplies the missing intermediate value.

Predictions:

- report/bridge contain a cross-example, cross-format decodable \(z\);
- direct contains weak or non-generalizing \(z\);
- posterior-state patching within direct has no clean localization because the state is absent;
- report-to-direct transplantation can supply the missing state and rescue behavior.

### H2 — Represented but causally underused posterior

Direct and bridge both contain \(z\), but only bridge gives it causal gain into the policy computation.

Predictions:

- \(z\) is similarly decodable in direct and bridge under held-out splits;
- natural posterior swaps causally affect report/bridge states or downstream action, but the direct posterior-to-comparator path is weak;
- path-specific gain or a same-example posterior-state transplant selectively rescues direct errors.

### H3 — Comparator/control-flow failure

The model transmits \(z\) and \(t\), but fails to compute the sign of \(d=z-t\) reliably. Clause order or predicate polarity may determine which branch wins.

Predictions:

- \(z\) and \(t\) are available and individually causal;
- \(d\) or its sign fails to appear consistently;
- threshold swaps and predicate-polarity swaps reveal the bottleneck;
- bridge activates or bypasses a comparator/control-flow circuit.

### H4 — Semantic-action/readout overwrite

The comparison is correct, but an ACT/default prior or unstable option mapping overwrites the result near output.

Predictions:

- \(d\) and semantic action \(s\) are decodable and causal before the answer;
- A/B mapping interventions alter the final label without changing \(s\);
- failures localize late, after the comparator state;
- neutral action words reduce lexical bias but do not eliminate mapping/binding errors.

These hypotheses are not mutually exclusive. The final account may be a mixture, but each claimed component must have its own intervention evidence.

## 5. Phase 0 — Behavioral refreeze before white-box runs

### 5.1 Factorial policy language

Create a mechanism dataset that crosses:

- likelihood regimes, for example symmetric emission pairs such as `0.7/0.3`, `0.8/0.2`, and `0.9/0.1`;
- observation order permutations at fixed sufficient statistics;
- mirrored Type A/B and red/blue semantics;
- predicate direction: `p > threshold` and `p <= threshold`;
- clause order: high/true branch first and low/false branch first;
- semantic action vocabulary: `ACT/WAIT` and at least two neutral pairs such as `ZORP/KETA`;
- option mapping: both A/B mappings;
- answer-label order and, where possible, prompt order;
- belief condition: `direct`, `gold_bridge`, `self_mean_bridge`, `self_argmax_bridge`, optional `self_generated_bridge`, `counterfactual_bridge`, and `irrelevant_number`.

Every underlying \((\pi,E,\tau)\) state must appear in all surface variants. This makes semantic action separable from branch order, lexical valence, and A/B binding.

The irrelevant-number prompt must use the identical numeric string, position, and surrounding length as its matched posterior bridge, changing only its semantic role to a calibration identifier. Counterfactual posterior values should be placed symmetrically on either side of the threshold. All rule forms require truth-table unit tests, and neutral action words must be tokenizer-audited for continuation-length asymmetry.

Where possible, use a fixed belief slot in every condition so direct/bridge token topology differs minimally: fill it with a posterior, a semantically neutral placeholder, or an equal-length irrelevant identifier. Also include an instruction such as “compute the posterior internally, but output only the action” as a query-gating diagnostic; do not interpret it as proof that the instruction was followed internally.

### 5.2 Counterfactual families

Generate matched families for three independent interventions:

1. **posterior family:** same threshold and mapping, different evidence/prior, with \(z\) on opposite sides of the threshold;
2. **threshold family:** same evidence/posterior and mapping, different thresholds on opposite sides of \(z\);
3. **mapping family:** same posterior, threshold, and semantic action, different A/B mapping.

Add three identification families:

4. **posterior-equivalence family:** same posterior \(z\), but different prior, likelihood regime, observation count/composition, and/or observation order;
5. **margin-equivalence family:** same log-odds margin \(d=z-t\), but different posterior and threshold values;
6. **action-equivalence family:** same semantic action, but different margin magnitude and different posterior/threshold components.

Where exact equality is required, solve the prior or threshold analytically in log-odds space rather than accepting an arbitrary probability tolerance. These families prevent a probe from being called a posterior or comparator probe when it has merely decoded red-minus-blue count, the threshold token, or action class.

For the current symmetric `0.8/0.2` likelihood, \(\ell_E=(n_{red}-n_{blue})\log 4\). A particularly clean exact construction uses priors `0.2`, `0.5`, and `0.8`: posterior `0.5`, for example, can be produced by `(prior=.2, n_red-n_blue=1)`, `(prior=.5, difference=0)`, or `(prior=.8, difference=-1)`. Adding matched red/blue pairs and permuting observation order changes surface evidence while preserving the posterior. Keep these exact families even if additional likelihood regimes are added for generalization.

Also generate nuisance families that change surface wording or evidence order while holding \(z,t,d,s,m\) fixed.

### 5.3 Token alignment

Primary activation-patching pairs must be token-audited for the anchor tokenizer:

- use fixed-width numeric formatting;
- use fixed-format evidence counts for the token-aligned primary corpus;
- retain natural list-format evidence as a held-out generalization template;
- record semantic spans and token indices in the manifest;
- require equal sequence length for exact position-to-position primary patches, or explicitly align named semantic positions rather than raw indices.

Do not patch direct and bridge prompts at the same raw index merely because both contain the same evidence; their lengths and instruction states differ.

### 5.4 Posterior measures

Record all three posterior measures:

- normalized expectation over candidates `0.00 … 1.00`;
- candidate argmax;
- greedy generated value.

Primary inference-good analyses require the argmax or generated value to imply the correct action. The expectation-based definition remains a secondary continuous analysis. Report agreement among the three.

### 5.5 Phase 0 output and decision

Freeze:

- prompts and tokenizer audit;
- unique evidence/counterfactual family IDs;
- discovery/dev/test splits;
- primary semantic score;
- eligibility definitions and all exploratory labels.

Each mechanism row must explicitly store prior and prior logit, observation counts/order and evidence LLR, likelihood regime, posterior and posterior logit, threshold and threshold logit, both raw-probability and log-odds margins, semantic action, action vocabulary, predicate polarity, clause order, option mapping, gold label, belief condition, template, causal-family/donor-pair IDs, and all semantic token spans.

If all apparent direct errors disappear under neutral, polarity-balanced, mapping-stable prompts, stop the posterior-routing claim. A broader instruction control-flow project is viable only if the same branch mechanism generalizes beyond this Bayesian task.

## 6. Phase 1 — Representation timeline

### 6.1 Activations to cache

For each decoder layer cache residual-stream states at:

- the final evidence token or a registered evidence-summary position;
- the end of the posterior/policy statement;
- the threshold span;
- the ACT/WAIT or pseudoword spans;
- option A and option B spans;
- the final user/query token before assistant generation;
- the first answer-prediction position.

For the current Qwen2.5-14B cache, the anchor has 48 decoder layers, hidden size 5120, 40 attention heads, and 8 KV heads. Re-audit this at runtime against the pinned model revision. Cache embedding output plus `resid_pre`, `attn_out`, `mlp_out`, and `resid_post` where feasible; add per-head outputs only after shortlisting.

Register named anchors such as `PRIOR_NUM_END`, `EVIDENCE_END`, `BELIEF_NUM_END`, `THRESHOLD_NUM_END`, `RULE_END`, both action-word spans, `MAPPING_END`, `QUERY_END`, and the first candidate position. Begin with `resid_post`; only expand streams after a layer range is localized.

### 6.2 Probe targets

Fit regularized probes for:

- continuous posterior log-odds \(z\);
- threshold log-odds \(t\);
- continuous margin \(d\);
- sign of \(d\);
- semantic action \(s\);
- surface mapping \(m\);
- output label \(y\).

The log-odds parameterization defines the clean high-level SCM, but it must not be assumed to be the network's representational geometry. Compare raw posterior \(p\) versus logit \(z\), raw margin \(p-\tau\) versus log-odds margin \(z-t\), and sign-only/action encodings under held-out data.

Use ridge regression for continuous targets and regularized logistic regression for categorical targets. A small nonlinear probe may be reported only as a capacity diagnostic, not as the primary representation claim.

### 6.3 Splits and controls

The independent unit is the **unique evidence state/counterfactual family**, not each threshold-expanded row.

Required evaluation:

- held-out priors;
- held-out red/blue count compositions;
- held-out likelihood regimes and observation orders;
- held-out thresholds;
- held-out prompt templates and action vocabularies;
- train on posterior-report and test on direct/bridge, as well as the reverse;
- shuffled-label probes;
- probes from raw surface features, token position, prior alone, count alone, and threshold alone;
- control for the fact that posterior can be algebraically reconstructed from visible counts.

Posterior identity must additionally be tested on posterior-equivalence families, and margin identity on margin-equivalence families. A representation that separates equal-\(z\) examples by likelihood/count regime but fails to align them is not sufficient evidence for an abstract posterior variable.

The main result is the relative timeline across direct/report/bridge, not the maximum in-domain probe score. Linear decodability alone is not causal evidence; [Where's the Plan?](https://arxiv.org/abs/2605.07984) is a direct warning that strong probe signals may have near-zero causal use.

### 6.4 Phase 1 deliverables

- layer × position heatmaps for \(z,t,d,s,m,y\);
- cross-format generalization matrices;
- confidence intervals clustered by evidence family;
- a frozen shortlist of layer/position regions for causal tests.

## 7. Phase 2 — Natural activation interchange

### 7.1 Primary outcome

For each prompt and mapping compute the mapping-aware semantic logit:

\[
S=\log P(\text{label corresponding to ACT})
 -\log P(\text{label corresponding to WAIT}).
\]

Score the full candidate continuation, even if A/B currently tokenize as one token. Do not average A/B probabilities before converting them to semantic coordinates.

For a receiver \(r\), donor \(d\), and patched run \(p\), report:

\[
\operatorname{recovery}=\frac{S_p-S_r}{S_d-S_r}
\]

only when the donor–receiver denominator is sufficiently separated. Also report raw signed logit change, semantic flip rate, and interchange-intervention accuracy (IIA).

For aggregation, orient the score toward the correct semantic action:

\[
S_{gold}=S\quad\text{if gold is ACT},\qquad S_{gold}=-S\quad\text{if gold is WAIT}.
\]

Retain each mapping variant as a separate paired observation and cluster by causal family. Do not average mappings before scoring.

### 7.2 Whole-residual patching

For every counterfactual family:

- patch donor `resid_post` into receiver at one layer and named position;
- run posterior swaps, threshold swaps, and mapping swaps separately;
- run clean→corrupt and corrupt→clean directions;
- patch nuisance-equivalent donors as a selectivity control;
- include both baseline-correct and baseline-error receivers.

The desired modular effects are:

- posterior donor changes \(S\) according to donor \(z\), with threshold/mapping fixed;
- threshold donor changes \(S\) according to donor \(t\), with posterior/mapping fixed;
- mapping donor changes surface A/B label while preserving semantic action;
- nuisance donor produces near-zero effect.

### 7.3 Direct versus bridge comparison

Do not infer routing merely from different probe accuracy. Compare the causal response curves:

- posterior-swap effect in direct;
- posterior-swap effect in self-bridge;
- posterior-swap effect in gold-bridge;
- threshold-swap effect in all three;
- effect of the same signed posterior perturbation as a function of layer.

The main routing comparison is a difference-in-differences: the posterior-swap causal effect in bridge minus the matched effect in direct, after subtracting the corresponding posterior-equivalent nuisance-swap effect.

A strong routing-gap result requires a posterior representation that generalizes into direct, plus substantially weaker natural posterior→action mediation in direct than bridge.

### 7.4 Validation controls

- random layer and random position patches;
- norm-matched random-vector patches;
- same-action donor with different posterior magnitude;
- different-action donor with the same superficial label;
- activation-norm and Mahalanobis-distance diagnostics;
- clean-output KL and unrelated-task output changes.

Natural, matched donors are preferred over Gaussian corruption. Noising and denoising results must agree qualitatively before localization is treated as robust.

## 8. Phase 3 — Low-dimensional causal variables

Use Distributed Alignment Search/Boundless DAS only in layer/position regions that passed whole-state intervention tests.

Train separate low-dimensional alignments for:

- posterior \(z\);
- threshold \(t\);
- margin \(d\);
- semantic action \(s\);
- mapping \(m\).

Evaluation requirements:

- no evidence family shared across train/test;
- held-out priors, thresholds, templates, action words, and mappings;
- counterfactual IIA, not only output accuracy;
- explicit subspace dimensionality sweep;
- random-subspace and label-shuffle baselines;
- in-manifold natural donor interventions;
- comparison with whole-state patch effects.

A successful DAS intervention is not by itself proof of faithful natural computation. Subspace patches can activate dormant pathways; see [Is This the Subspace You Are Looking For?](https://arxiv.org/abs/2311.17030). The aligned subspace must agree with natural whole-state effects and later path-level results.

## 9. Phase 4 — Component and path localization

### 9.1 Screening

Use AtP*/attribution patching to rank candidate:

- attention outputs;
- MLP outputs;
- individual attention heads where hooks permit;
- sender-token/receiver-token groups.

This is a compute-saving screen only. First-order attribution patching can fail through downstream nonlinearities; exact patches are required for every reported component. See [When Attribution Patching Lies](https://arxiv.org/abs/2606.09899).

### 9.2 Exact component tests

At shortlisted layers, run exact noising and denoising patches for:

- `attn_out`;
- `mlp_out`;
- individual head outputs;
- selected residual subspaces.

Freeze the component shortlist on discovery data, then evaluate it once on held-out test families.

### 9.3 Candidate functional paths

Test the following paths in order:

1. prior/evidence tokens → posterior-bearing state;
2. posterior-bearing state → policy/query position;
3. threshold span → comparator/query position;
4. posterior and threshold senders → margin/action state;
5. action state → option-mapping state;
6. mapping/action states → first answer token.

Use path patching after nodes are localized, not as an all-model blind search. Report a circuit-size–faithfulness curve rather than only the best five heads.

## 10. Phase 5 — Mechanism validation and selective rescue

Three intervention families are required:

### 10.1 Same-example posterior transplant

Take a posterior-bearing state elicited from the report prompt for the same evidence and transplant it into the matched direct computation at the causally validated receiving site. This is a sufficiency test for externalization, not evidence that the original direct model formed that state.

### 10.2 Path-gain rescue

Increase only the identified posterior→comparator path or remove the identified late overwrite path, without inserting the gold action. This is the strongest repair test for a routing/control-flow account.

### 10.3 Dose response

Apply small positive and negative interventions along a validated posterior or margin subspace. The semantic action logit should change monotonically and reverse direction across high/low posterior examples.

All rescues must be evaluated on:

- direct errors and direct correct cases;
- ACT and WAIT gold actions;
- both mappings, predicate polarities, and action vocabularies;
- held-out evidence/template families;
- unrelated numeric comparison and instruction-following tasks.

Report:

- error rescue rate;
- damage to originally correct cases;
- off-target KL/output changes;
- monotonicity and bidirectionality;
- selectivity against random paths/subspaces of equal norm.

No single steering direction is allowed to serve as the sole mechanism proof.

## 11. External validation

After the synthetic mechanism and predictions are frozen, test one official BayesBench environment, preferably the recommender setting in which a latent user type controls a held-out rating/policy prediction.

Before running external validation, preregister predictions such as:

- which stage should contain posterior information;
- whether explicit belief serialization should increase posterior→action mediation;
- whether the same component class/path region should be involved;
- which intervention should rescue action without changing posterior estimation.

Do not add several unrelated Bayesian tasks. One external transfer is enough for an ACL/EMNLP/NAACL-sized paper.

## 12. Statistical plan

- Independent unit: unique evidence/counterfactual family.
- Discovery/dev/test split is frozen before component selection.
- Use paired permutation tests for matched donor/receiver effects.
- Use cluster bootstrap by evidence family for confidence intervals.
- Correct layer/head scans with a max-statistic permutation or FDR.
- Report effects on all cases and error-only subsets; never condition the main mechanism claim only on baseline errors.
- Report raw semantic-logit effects, IIA, normalized recovery, flip rates, and confidence intervals.
- Include seed variation for trained probes/DAS.
- Freeze the final circuit on discovery data and run held-out confirmation once.

## 13. Result-to-narrative decision table

| Confirmatory result | Correct conclusion | Project decision |
|---|---|---|
| Direct lacks cross-format/generalizing posterior state | Externalization causes query-gated posterior formation | Continue under formation narrative |
| Direct contains posterior, but natural causal gain to action is absent/weak and bridge restores it | True posterior-routing failure | Strongest intended result |
| Posterior and threshold arrive, margin/comparison fails | Comparator or instruction-control-flow bottleneck | Continue with comparator narrative |
| Margin/action is correct, label binding fails | Late action/readout overwrite | Continue only if mapping mechanism generalizes |
| Only branch order or label lexicality explains errors | Surface instruction bias, not latent-use gap | Stop original claim; broaden only with new cross-task evidence |
| No stable held-out causal effect despite probe/steering success | Decodable but mechanistically unvalidated | Do not publish a circuit claim |

The validation is designed to identify the true failure stage, not to force the routing hypothesis or kill the mother question when a neighboring stage explains it.

## 14. Compute-efficient execution order

1. **Phase 0:** generate and behaviorally validate the factorial/token-aligned corpus.
2. **Phase 1:** one Qwen2.5-14B forward pass per prompt with all hidden states cached; probe offline.
3. **Phase 2:** layer × named-position whole-residual patches on a small discovery set; exact confirmation on held-out pairs.
4. **Phase 3:** DAS only over the localized layer window.
5. **Phase 4:** AtP* screen, then exact component/path patches.
6. **Phase 5:** selective rescue and one external BayesBench transfer.

Qwen2.5-14B fits on one 98GB GPU in BF16. Prefer one model replica per GPU and counterfactual/layer data parallelism across four GPUs; avoid model parallelism because it complicates hooks and path patching. Qwen3-8B and Gemma3-12B require only coarse replication of the stage-level finding, not a full duplicated circuit search.

## 15. Planned artifacts

```text
mechanism/
├── configs/
│   ├── phase0_behavior.json
│   ├── phase1_probes.json
│   ├── phase2_patching.json
│   └── frozen_confirmatory_split.json
├── data/
│   ├── mechanism_cases.jsonl
│   ├── counterfactual_pairs.jsonl
│   └── token_audit.jsonl
├── src/
│   ├── generate_mechanism_data.py
│   ├── cache_activations.py
│   ├── probes.py
│   ├── patching.py
│   ├── das.py
│   ├── path_patching.py
│   └── statistics.py
├── results/
└── tests/
```

Every result row should record model revision, Transformers/PyTorch version, prompt/template ID, evidence-family ID, mapping, tokenizer indices, intervention site, donor/receiver IDs, seed, and exact metric definition.

Minimum mechanism-test coverage:

- closed-form posterior, log-odds, threshold, and margin calculations;
- exact same-posterior and same-margin decompositions;
- posterior/threshold crossing and non-crossing donor pairs;
- every predicate-polarity, clause-order, action-word, and mapping truth table;
- donor pairs differ only in their declared high-level variable;
- semantic spans are unique and token-aligned where required;
- full candidate prefix-boundary checks;
- direct prompts never leak the posterior literal;
- posterior and irrelevant-number controls contain identical number strings;
- no-op/self patches preserve logits within numerical tolerance;
- grouped splits never leak a causal family across partitions.

## 16. Paper-sized target claim

The strongest defensible target is:

> Language models can externalize a quantitatively adequate latent posterior without giving that variable the same causal role in direct policy computation. Causal interchange identifies whether serialization forms the posterior, activates the comparator route, or bypasses a late action/readout bias, and a path-specific intervention selectively restores policy use.

Suggested title:

> **When Does a Reported Belief Become an Action? Causal Decomposition of Posterior Formation, Comparison, and Policy Readout**
