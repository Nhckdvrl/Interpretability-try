# 006 Interpretability Plan V2

## From serialized belief to role-gated policy use

**Plan status:** methodologically reviewed and frozen for the next execution round; no new model experiment is authorized by this document itself
**Written after:** exploratory Qwen2.5-14B Phase 0–2 runs on 2026-08-27
**Relationship to V1:** `INTERPRETABILITY_PLAN.md` preserves the original hypothesis space; V2 governs the next execution round
**Current evidence class:** all existing white-box results are discovery/exploratory, not confirmatory

---

## 0. Executive decision

006 remains active. The topic is not yet “a circuit for Bayesian arithmetic,” and it is not yet proven to be a posterior-routing failure. The paper-sized question is:

> **When a language model can estimate a latent belief, what makes that belief become a causally used control variable for a downstream policy—and can the discovered use mechanism selectively repair belief–action gaps without changing the belief itself?**

The current anomaly is unusually useful:

1. direct policy use is much worse than posterior reporting plus policy execution;
2. replacing the complete externalized eight-token number is sufficient to control bridge action, while its final token alone is not;
3. replacing that source span controls action almost perfectly through layer 15;
4. the source-span causal effect collapses over layers 16–25;
5. literal serialized-value decodability at the same source span continues to rise and remains high after local causal control disappears.

This motivates a falsifiable **role-gated transport** hypothesis:

> Externalization does not merely add a number. It supplies posterior content in a role that a middle-layer transport mechanism recognizes and routes into a comparator/writer. Direct prompts may form related content without placing it in the causal role consumed by that pathway.

“Reader,” “transport,” and “writer” are roles to be demonstrated, not labels to attach after a probe succeeds.

The intended conference-width package is one mother question, three mechanistic stages, one decisive direct-versus-externalized contrast, one selective repair predicted by the mechanism, and one chosen generality validation. Full circuit recovery is required only for the Qwen2.5-14B anchor; a contrast model or an external task receives stage-level replication before the claim is widened beyond that anchor.

---

## 1. Frozen snapshot of what is known

### 1.1 Behavioral discovery

The mechanism corpus contains 42 non-boundary policy cases, balanced ACT/WAIT, generated from an exact `0.8/0.2` likelihood family with three priors and three thresholds. Across the full surface factorial on Qwen2.5-14B:

- posterior mean MAE is `0.1306`;
- direct semantic action accuracy is `0.570`;
- gold-posterior bridge accuracy is `0.932`;
- self-mean bridge condition-implied accuracy is `0.896`;
- self-argmax bridge condition-implied accuracy is `0.933`;
- counterfactual-posterior follow rate is `0.897`;
- irrelevant-number original-task accuracy is `0.597`.

The selected ACT/WAIT anchor surface has a `36.7%` direct error rate and stronger mapping stability than the aggregate factorial. Current broad-surface mapping consistency is only `55.1%`; therefore all paper-level mechanism claims must be rechecked under a cleaner confirmatory surface set.

### 1.2 Exploratory representation findings

- At the final query position, direct posterior and decision-margin probes peak late (`r=.943/.950`, `R²=.837/.865`).
- Bridge→direct posterior probes on the same matched cases preserve rank ordering but not calibration (`r≈.88–.91`, `R²≈.07`); without held-out evidence families this is descriptive, not cross-example geometry evidence.
- The serialized posterior is exactly eight Qwen tokens under fixed-width formatting.
- An eight-token mean-pooled probe predicts the literal serialized self-mean value at `r=.975`, `R²=.847` around layer 28.
- Last-token-only probes fail for arbitrary self-estimated six-digit values, showing that a final-token-only account is inadequate; the other numeric positions have not yet been tested individually.

The gold span cache contains only 15 unique evidence states and approximately seven unique gold posterior values; threshold and mapping occur later in the sequence and therefore duplicate the source activations. Visible counts algebraically determine the posterior, and token identity directly reveals serialized values. Decodability is not evidence of an abstract posterior variable. Effective sample size, held-out values/formats, raw-token baselines, held-out likelihood regimes, and posterior-equivalent decompositions remain mandatory.

### 1.3 Exploratory causal findings

At layer 0, a natural crossing swap of the full serialized posterior number produces:

- gold bridge: mean recovery `.981 [.944, 1.014]`, `12/12` donor-action IIA;
- self-mean bridge: mean recovery `.981 [.947, 1.015]`, `12/12` donor-action IIA;
- same-posterior gold control: mean absolute effect `0.29` versus crossing effect `49.64` semantic-logit units, in the current deterministic discovery subset;
- full belief-statement swaps are nearly identical to number-only swaps.

The source-span swap trajectory is near-complete through layer 15, decays over layers 16–24, and is approximately zero from layer 25 onward. Single-position swaps at the posterior end token and final query token are null. This identifies a source-site decay window, not a receiver or handoff.

Layer-0 span replacement is close to a controlled textual counterfactual and is not, by itself, a deep mechanism claim. Full-span sufficiency plus final-token insufficiency does not show that information is distributed across all digits. Its value is to motivate subspan necessity tests and a search for a downstream receiver.

### 1.4 Claims not yet established

The existing experiments do **not** establish that:

- direct prompts form the same posterior representation as report/bridge prompts;
- a bridge/direct “reader” is causal rather than merely decodable;
- information leaving the numeric source is carried by specific attention heads or MLPs;
- the comparator, semantic action, and A/B binding stages have been separated;
- a mechanism-derived edit can rescue direct errors without gold-posterior leakage;
- the phenomenon transfers beyond this synthetic closed-form family.

These are the actual V2 targets.

---

## 2. What is borrowed from Hamdi’s research method

### 2.1 The useful pattern

The transferable method is not a particular SAE, steering coefficient, or model. It is the following chain:

1. start from a simple behavioral contradiction;
2. compress it into a falsifiable internal distinction;
3. prove readout before claiming representation, then require causal intervention;
4. turn a failed or saturated intervention into a new structural hypothesis;
5. require that hypothesis to predict the next successful experiment;
6. use the resulting mechanism to predict a more selective method;
7. validate the method as evidence for the mechanism, not as an appended contribution;
8. attack each plausible confound with a dedicated factorial control.

For 006, the failed named-position/final-digit patches and the layer-16–25 source-effect collapse are not nuisances. They generate the transport hypothesis and a concrete prediction: intervening on a validated carrier path should change action while leaving source-span literal-value decodability largely intact.

### 2.2 Ontology/compliance becomes content/role

The “real versus imagined” work separates an entity’s ontology representation from instruction compliance. The analogous axes here are:

- **belief content:** the posterior value represented by the model;
- **causal role/use mode:** whether that value is treated as authoritative input to the policy.

These axes must be crossed, not conflated. The same number must appear in “use,” “report,” and “irrelevant/ignore” roles; different posterior values must appear under the same role. A valid role reader changes sensitivity to posterior content, not merely the ACT/WAIT logit.

### 2.3 Three-stage mechanism

The useful three-stage template is:

1. **formation:** construct or encode posterior content;
2. **transport/use:** move role-licensed content toward the threshold comparator;
3. **commit:** convert the comparison into semantic action and then A/B output.

Current timing evidence only localizes decay in intervention efficacy at the externalized source. It does not establish transport, identify a receiver, or assign components to these stages.

### 2.4 Reader–writer as a hypothesis, not a naming convention

The random-choice work suggests a powerful test:

- a **reader/gate** identifies when a latent quantity should control behavior;
- a **writer/comparator path** converts that quantity into the appropriate output change;
- a gated edit should outperform an unconditional edit on selectivity.

For 006, this predicts a low-rank intervention only if the natural transport path is first validated. We will not begin by training a reader, find any separable direction, and call it the mechanism.

### 2.5 LoRA geometry as an upper-bound diagnostic

If a rescue LoRA is later trained, it serves as a performance ceiling and a source of geometric predictions:

- train multiple seeds;
- decompose deltas by layer/module and singular spectrum;
- test whether successful changes concentrate in the D0 source-decay window and any later causally validated transport path;
- use the observed effective rank to preselect rank-`1/2/4/8` representation interventions.

LoRA or LoReFT is not itself the novelty. A low-rank method is included only if the mechanism predicts that low rank should suffice.

### 2.6 What must not be copied

The following risks are explicitly corrected in V2:

- no final claim may be selected and evaluated on the same examples;
- no layer, latent, rank, strength, or path may be chosen on the test split;
- current layer windows are discovery findings and require held-out confirmation;
- all reported numbers must be generated from raw outputs, never copied manually between versions;
- exploratory, dev-selected, and confirmatory outputs must live in separate directories;
- every headline claim must map to a script, config, result artifact, and Git commit;
- incompatible result versions must be marked superseded rather than silently overwritten.

---

## 3. V2 causal abstraction

Let:

- `x`: prior and evidence;
- `z_dir`: posterior content, if formed in the direct computation;
- `z_ser`: serialized posterior content in report/bridge prompts;
- `r_slot`: role state indicating whether an external number is authorized as a posterior;
- `r_need`: task state indicating that a belief–threshold policy computation is required;
- `g_path`: measured causal gain of an as-yet-unidentified natural transport path;
- `t`: threshold representation;
- `d = z - t`: comparison margin in an unknown internal geometry;
- `s`: semantic action ACT/WAIT;
- `m`: option mapping;
- `y`: surface label A/B.

The target high-level model is:

```text
x ───────────────> z_dir ─┐
text number ─────> z_ser ─┼─> [candidate path gain g_path] ─> comparator d ─> s ─[m]─> y
role/instruction ─> r_slot ┤                                  ↑
task requirement ─> r_need ┘                                  │
threshold ───────────> t ──────────────────────────────────────┘
```

The diagram is schematic rather than a proven architecture. `g_path` is an estimand, not an assumed latent, and the graph is deliberately noncommittal about whether `z_dir` exists. V2 must distinguish six competing accounts.

### H1 — Query/role-gated belief formation

The direct prompt never forms a sufficiently abstract posterior; report and bridge contexts cause formation. Prediction: strong cross-family posterior identity appears only in report/bridge, and transplanting a direct state cannot drive a validated comparator even when the route is opened.

### H2 — Role-gated transport failure

Direct and bridge both form related posterior content, but only bridge assigns it the causal role consumed by the policy. Prediction: a causal role state modulates posterior sensitivity; opening the route selectively rescues inference-good direct errors without supplying the gold posterior.

### H3 — Coordinate/alignment mismatch

Direct contains posterior information in a context-specific code that is not readable by the bridge comparator. Prediction: a low-dimensional alignment learned on dev maps direct content into the natural bridge receiving geometry; raw state transplants fail while aligned transplants succeed.

### H4 — Comparator failure

Posterior and threshold arrive, but their comparison is unreliable. Prediction: `z` and `t` are individually causal at a common site while `d` or `sign(d)` is missing; a comparator-specific intervention repairs action without changing posterior reports.

### H5 — Late semantic/label binding failure

The correct comparison and semantic action are present, but ACT/WAIT is mapped incorrectly to A/B. Prediction: semantic-action probes/patches succeed before the output, while mapping swaps or late binding components determine the error.

### H6 — Generic numeric authority/compliance gate

The apparent role reader is not posterior-specific: it merely detects whether any external numerical score is authorized. Prediction: the topology-matched generic authority control produces the same content-sensitivity interaction as the posterior condition, so nuisance subtraction removes the headline effect even though both raw interactions are positive.

No experiment is useful unless its possible outcomes discriminate at least two of these accounts.

---

## 4. Data and split freeze

### 4.1 Discovery split D0

All data and white-box outputs generated before V2 are permanently labeled `D0-exploratory`. They may define hypotheses and the provisional layer window `14–25`; they may not provide final confirmatory effect sizes. The existing config's `case_id + surface_id` independent unit is superseded: all future split and inference units are complete evidence/counterfactual causal families.

### 4.2 Development split D1

D1 is used for:

- choosing named positions and components inside layers 14–25;
- selecting probe regularization, subspace rank, intervention strength, and circuit size;
- debugging token alignment and numerical controls;
- selecting at most one external BayesBench environment.

D1 must add programmatically generated variation beyond D0:

- multiple likelihood regimes, including held-out evidence LLR scales;
- posterior-equivalent decompositions across priors and count compositions;
- posterior-distance-matched crossing and non-crossing pairs;
- observation-order permutations;
- neutral and pseudoword action vocabularies;
- rule polarity and clause-order counterbalancing;
- both A/B mappings;
- round and non-round fixed-width posteriors with matched token fertility.

### 4.3 Confirmatory split D2-ID

D2-ID is the primary confirmatory test. It is generated once, checksummed, and left untouched until all choices are frozen. It contains new causal families and new posterior numeric values within the same supported task factors and fixed-decimal format used in D1, so failure is interpretable rather than a bundle of OOD shifts.

Causal families—not threshold-expanded rows or mapping duplicates—are the independent split unit. No evidence family, posterior-equivalence family, value quadruple, or donor pair may cross D1/D2-ID.

### 4.4 Factorial generalization D2-OOD

D2-OOD changes one factor at a time:

- held-out likelihood regime;
- held-out prior/count composition;
- held-out numeric value range;
- held-out numeral format such as percent, fraction, words, or log-odds;
- held-out prompt template or action vocabulary;
- held-out observation-order family.

Each one-factor OOD result is reported separately. A fully compositional OOD set is a stress test, not the primary confirmatory gate. This prevents an unnecessarily hard combined distribution shift from being mistaken for evidence against the mother question.

### 4.5 External transfer T1

One official BayesBench recommender or triage setting is selected on D1 and frozen. It must expose:

- a separately scoreable latent belief or probability estimate;
- a downstream decision with a known relation to that belief;
- a direct versus belief-externalized contrast;
- enough open-weight examples for activation interventions.

T1 tests the stage-level claim and selective repair, not a complete duplicated circuit.

### 4.6 Model roles

- **Qwen2.5-14B-Instruct:** anchor model; full localization.
- **Qwen3-8B:** posterior-estimation/report-poor behavioral contrast; coarse formation/use diagnosis only, with internal formation failure left to be tested.
- **Gemma3-12B-IT:** behaviorally different contrast; stage-level replication and optional Gemma-Scope analysis only after causal sites are stable.

Base-versus-instruct comparisons are desirable controls but not required for the main circuit unless local checkpoints and compute make them cheap.

---

## 5. Metrics and statistical unit

### 5.1 Behavioral quantities

- posterior mean/argmax/generated-value error;
- inference-good eligibility, frozen before action analysis;
- direct semantic action accuracy and mapping consistency;
- gold/self bridge condition-implied accuracy;
- bridge rescue and counterfactual follow rate;
- accuracy under irrelevant-number and explicit-ignore controls.

### 5.2 Causal quantities

For mapping-aware semantic logit `S`:

```text
recovery = (S_patched - S_receiver) / (S_donor - S_receiver)
```

Report raw signed effect, donor-direction fraction, semantic flip rate, IIA, normalized recovery when the denominator is adequate, and a selectivity contrast against matched controls.

First define the posterior-role interaction and one frozen topology-matched generic-authority control. The primary control uses the **same receiver policy task, evidence/counterfactual family, ACT/WAIT semantic-logit coordinate, threshold, option mapping, numeric values, and aggregation rule**. Its external number is described as an independently supplied decision score—not a probability and not evidence-derived—and the matched instructions either authorize comparing that score with the same threshold or explicitly require ignoring it and solving from the evidence. Thus only posterior semantics versus generic numerical authority changes. A separate non-Bayesian numerical task is a secondary negative control and never enters the primary subtraction.

```text
G_posterior = [S(use, z_high) - S(use, z_low)]
            - [S(ignore, z_high) - S(ignore, z_low)]

G_generic_control = the same family-matched interaction for the frozen
                    non-posterior decision-score authority control

G_specific = G_posterior - G_generic_control
```

Compute both interactions within each matched causal family, subtract them within family, and only then aggregate or bootstrap by family. The same frozen control and aggregation rule define `G_specific` and `G_patch_specific` everywhere. `G_specific`, not the raw interaction, is the primary role-gating estimand. A reader intervention is causal only if it changes `G_specific` in the predicted direction while preserving posterior content and unrelated outputs. `G_posterior` and `G_generic_control` are reported as constituent diagnostics so subtraction cannot hide a generic instruction-following effect.

### 5.3 Uncertainty

- cluster bootstrap and paired permutation by causal/evidence family;
- Wilson intervals for small-sample flip/IIA rates;
- paired differences across mappings and prompt variants;
- no treating mappings, thresholds, or repeated surface forms as independent evidence;
- exact per-model estimates plus a hierarchical or mixed-effects aggregate only after model-level results are shown;
- the existing pair bootstrap is reported only as conditional uncertainty over 12 deterministically selected, baseline-correct crossing pairs, some sharing donors; it is not a population-level family interval.

### 5.4 Selectivity and collateral damage

- unrelated-task KL and accuracy;
- direct-correct versus direct-error effects;
- inference-good versus inference-bad effects;
- activation norm and Mahalanobis distance;
- effect per intervention norm;
- monotonicity across positive/negative strengths selected only on D1.

Posterior-content preservation is a formal equivalence test, not a nonsignificant difference. Before D2-ID, use D1 no-op patches and batch-shape reruns to freeze two margins:

```text
epsilon_value  = max(0.01 posterior-probability units,
                     family-level 95th percentile of absolute no-op/batch drift)
epsilon_report = max(0.02 total-variation distance,
                     family-level 95th percentile of no-op/batch report drift)
```

After every claimed role/path intervention, evaluate both (i) a content decoder fixed on held-out families and formats and (ii) a topology-matched posterior-report continuation. The family-clustered 95% confidence intervals for **both** the decoder-implied posterior change and the generated numeric posterior change must lie inside `[-epsilon_value, +epsilon_value]`; the teacher-forced distribution over the preregistered numeric candidate grid must also remain within `epsilon_report`. All three criteria must pass. An intervention exceeding either margin is a joint content-and-use rewrite and cannot support content/use dissociation. Margins are frozen from D1 and never widened after D2-ID is opened.

### 5.5 Family count and precision freeze

Before opening D2-ID, freeze:

- the number of independent content × role quadruple families;
- posterior-, threshold-, and mapping-intervention family counts;
- the minimum scientifically relevant semantic-logit/recovery interaction;
- a power or confidence-interval-width calculation based on D0/D1 family-level variance;
- a prohibition on adding families after inspecting D2-ID.

Mappings, thresholds, and surface duplicates remain repeated measures inside a family. This precision plan is not a new kill gate; it prevents an underpowered null from being misread as absence of a mechanism.

---

## 6. Experiment V2-A — Separate belief content from causal role

Construct four serialized-role conditions with an identical eight-token slot at the same position and matched topology:

1. **authoritative use:** “use posterior `z` for this decision”;
2. **report only:** ask for or state `z`, then pose a separate policy query without granting authority;
3. **irrelevant mention:** explicitly state the same number is unrelated;
4. **explicit ignore:** state `z` but require evidence-based computation;

The **direct** condition contains no serialized posterior and is therefore a separate matched-suffix comparison, not a member of the identical-slot factorial. If a placeholder direct control is used, it must be an equal-length neutral slot whose lack of semantic authority is independently validated.

`authoritative use` is scored against the serialized value; `explicit ignore` is scored against the evidence-derived value. `report only` is diagnostic unless its downstream rule is made unambiguous and therefore does not enter primary accuracy by default.

Cross role with:

- low/high and boundary-near/far posterior values;
- gold, self-estimated, and counterfactual values;
- round versus non-round numerals;
- matched digit multisets where possible;
- both semantic actions and A/B mappings.

The irrelevant/ignore wording must match bridge length, position, surrounding syntax, and answer topology; the current calibration-identifier control does not satisfy this requirement.

Before interpreting the whole-span result, run a frozen position lattice:

- each of the eight token positions alone;
- cumulative prefixes and suffixes;
- leave-one-position-out swaps;
- punctuation-only, leading-zero-only, and significant-digit-only swaps;
- digit-position and numerical-distance matched donors.

This identifies sufficiency and necessity without assuming the effect is distributed. Any claim that the full belief statement and number-only intervention are equivalent requires a predeclared equivalence margin, not merely similar point estimates.

Required behavioral result: output sensitivity to `z` must depend on role, while the number is equally parseable in all serialized conditions.

Required representational result:

- a content probe predicts `z` across roles;
- a role probe predicts use versus ignore while balanced over `z`, threshold, action, and mapping;
- content and role directions are tested for independence and leakage;
- neither direction is called causal until the interventions below succeed.

This is the direct analogue of separating ontology from instruction compliance.

Add the frozen generic-authority difference-in-differences control from Section 5.2. Keep the receiver policy, semantic-logit coordinate, evidence family, threshold, mapping, values, and use/ignore topology fixed; replace only posterior semantics with the independently supplied non-probability decision score. Balance whether serialized content agrees or conflicts with evidence. The non-Bayesian numerical task remains a secondary negative control. Natural whole-state role interchange precedes any learned reader steering.

---

## 7. Experiment V2-B — Determine whether direct posterior content exists

### 7.1 Representation identity

Search only semantically justified sites:

- prior span;
- evidence tokens and evidence-summary positions;
- rule/threshold positions;
- query/answer-prediction positions;
- pooled evidence spans, not only last tokens.

For posterior `z`, compare:

- raw probability versus log-odds geometries;
- numeral formats such as fixed decimal, percent, fraction, words, and log-odds, with semantic equivalence and token fertility controlled;
- held-out numerical values, not only held-out rows using the same small value set;
- linear and small nonlinear capacity diagnostics;
- within-format and cross-format generalization;
- posterior-equivalent families across likelihood/prior/count decompositions;
- held-out likelihood regimes where visible-count shortcuts fail;
- raw-feature baselines using token embeddings/identity, digit histogram, prior, counts, token positions, threshold, and prompt length;
- label-shuffled and nested selection baselines, with layers and regularization chosen on D1 only.

### 7.2 Causal criterion for formation

A direct state counts as a posterior state only if at least one of the following holds on held-out families:

- transplanting it into a validated bridge receiving site changes action according to donor `z` and not surface label;
- in a topology-matched dual-query or branched-continuation auxiliary condition, natural swaps change the later posterior report while holding the pre-branch direct computation fixed.

Suppressing a state in a separate report prompt establishes report-state causality, not direct-state identity. Because the natural direct prompt emits no posterior report, it cannot satisfy the formation criterion merely by changing the query.

High direct probe accuracy alone is insufficient.

### 7.3 Outcome interpretation

- failure across strong cross-family tests supports H1;
- aligned and causal content with weak policy mediation supports H2;
- rank-preserving but miscalibrated content may motivate H3. A learned alignment supports natural coordinate mismatch only if it also aligns posterior-equivalent families, predicts matched natural bridge receiver geometry, stays on the natural norm/Mahalanobis manifold, acts through a validated comparator path, defeats random/inverse/wrong-path maps, and preferably works bidirectionally. Otherwise the conclusion is only that a trained interface can exploit direct information.

---

## 8. Experiment V2-C — Localize the middle-layer transport path

The D0 discovery window is layers `14–25`. Search elsewhere only if D1 shows the transition moved under a new template or model.

### 8.1 Screen

Use AtP*/attribution patching to rank:

- attention heads receiving from the belief-number span;
- attention outputs at threshold, rule, mapping, and query tokens;
- MLP outputs that amplify posterior or margin directions;
- residual paths from the serialized span to later semantic positions.

The screen chooses candidates on D1 only. First-order attribution is not a result.

### 8.2 Exact confirmation

For each shortlisted component run exact:

- clean→counterfactual and counterfactual→clean patches;
- noising and denoising;
- same-posterior/different-decomposition controls;
- same-action controls matched on absolute posterior/log-odds intervention distance, distance to threshold, and baseline semantic logit;
- random-head and random-layer controls;
- norm-matched random vectors/subspaces;
- both A/B mappings.

The transport hypothesis predicts that blocking the path reduces downstream action sensitivity to the serialized posterior while leaving the source-span posterior probe largely intact. Restoring the path should recover the donor effect.

### 8.3 Three-stage evidence

The paper may claim three stages only if the following order is causally supported:

1. posterior content becomes available at the source/evidence representation;
2. a middle-layer component transports role-licensed content to a comparator site;
3. later components convert margin sign into semantic action and bind it to A/B.

Temporal probe peaks without path interventions do not satisfy this requirement.

---

## 9. Experiment V2-D — Test a causal role reader

### 9.1 Reader construction

Train a role reader on D1 to distinguish authoritative-use from irrelevant/ignore conditions while balancing all content and answer variables. Candidate constructions:

- logistic probe direction;
- difference-of-means direction;
- a sparse SAE latent only if an appropriate pretrained SAE exists and outperforms dense controls.

The reader is selected for cross-template generalization, not maximum in-sample accuracy.

### 9.2 Reader interventions

Use activation patching, signed steering, and—only at a validated site—weight orthogonalization. Primary `r_slot` validation is restricted to the topology-matched serialized `{use, ignore}` conditions. A valid reader must:

- increase posterior sensitivity `G_specific` when transplanted `use→ignore`;
- decrease `G_specific` when transplanted `ignore→use`;
- leave the represented posterior value approximately unchanged;
- not directly encode ACT versus WAIT or A versus B;
- preserve arithmetic, factual, attribute, and unrelated policy outputs.

Reader steering that merely biases one answer label is a failure.

Natural direct prompts contain no external posterior slot. Therefore an `r_slot` intervention is not a direct-policy reader or a valid direct rescue by default. Direct rescue becomes eligible only after establishing that `z_dir` exists, locating a homologous receiver, and either independently validating a direct `r_need` state or demonstrating a natural homologous causal path. Any direct reader state must be named and tested separately from the serialized use/ignore reader; the measured path gain `g_path` is an effect estimate, not a per-example activation.

### 9.3 Gate/path interaction

Freeze an exact reader-donor `{use, ignore}` × content-donor `{high, low}` four-cell intervention on the same receiver **example**, evidence, threshold, and mapping. Content is intervened on at the validated numeric source/carrier path, while role is intervened on at an independently validated reader site or component. If both variables can only be manipulated at one position, use separately validated, leakage-controlled, approximately orthogonal subspace interventions. Sequential whole-residual replacements at the same activation vector are forbidden because the second patch would overwrite the first.

Define the posterior and generic-control joint-patch interactions separately:

```text
G_patch_posterior = [S(r_use, z_high) - S(r_use, z_low)]
                  - [S(r_ignore, z_high) - S(r_ignore, z_low)]

G_patch_generic_control = the corresponding four-cell interaction in the
                          matched generic-compliance control

G_patch_specific = G_patch_posterior - G_patch_generic_control
```

`G_patch_specific` is the primary causal joint-intervention estimand; it uses exactly the Section 5.2 primary control and family-first aggregation, and both raw constituent interactions remain visible. High/low values are symmetrically matched around the threshold. Report both slope and intercept in semantic-logit space so a global ACT bias cannot masquerade as gating. A causal reader changes the `z → S` slope while passing the frozen posterior-content equivalence tests in Section 5.4. Reader and content interventions must be separately interpretable, and the joint intervention must open or close policy use in the predicted direction.

Where an attention component is implicated, decompose the hypothesis rather than reading attention maps: patch Q/K or selector states to test the role reader, patch V/OV content to test the writer, and then exactly confirm the full head/path effect. Single-head ablation must be followed by component-set ablation and re-attribution because remaining heads may reroute.

---

## 10. Experiment V2-E — Identify the comparator/writer

The writer is the component or low-dimensional path that converts posterior/threshold information into semantic action. It is not defined as “whatever direction increases accuracy.”

Required tests:

- a full posterior-high/low × threshold-high/low factorial with separate and joint patches;
- posterior swaps move semantic logit monotonically with fixed threshold;
- threshold swaps move action in the opposite direction with fixed posterior;
- equal-margin/different-posterior-and-threshold families align at the comparator and in output effects;
- raw-probability and log-odds margin hypotheses are compared rather than assumed;
- mapping swaps change A/B but preserve ACT/WAIT;
- writer intervention changes decision margin/action but not posterior reports;
- effects generalize across action vocabularies and rule polarity;
- random subspaces and shuffled labels fail.

If a low-dimensional subspace is suggested, sweep rank `1/2/4/8` on D1, then freeze one rank for D2-ID. DAS/LoReFT is permitted only within the naturally validated layer/path window and must be compared with natural whole-state effects.

---

## 11. Experiment V2-F — Mechanism-predicted selective repair

### 11.1 No gold leakage

Distinguish three candidate gates:

- `r_slot`: whether an external numeric slot is authorized as posterior;
- `r_need`: whether the current task requires a belief–threshold policy;
- `g_path`: the measured causal gain of a validated natural path.

Natural direct prompts have no external slot, so an `r_slot` classifier cannot be reused as the direct-repair gate without separate validation. The repair may use only:

- the model’s own direct internal posterior estimate/state;
- a role/policy reader computed from the prompt;
- a writer/transport map learned on D1.

It may not inject the true posterior, gold action, or test label.

Core repair defaults to acting structurally on the already naturally validated path; `g_path` measures that path's causal gain and is never treated as a prompt-level gate. A decoded task label is not enough to substitute `r_need`. The optional `r_need` route becomes eligible only after an independent, topology-matched `{policy computation needed, policy computation not needed}` × `{z_high, z_low}` factorial. It must generalize across held-out templates, change the causal `z → S` slope rather than an answer intercept, preserve posterior content under the Section 5.4 equivalence tests, and survive task-classifier, answer-label, and generic-compliance controls. Until then, `r_need` is only a task classifier and cannot enter the repair or reader–writer claim.

### 11.2 Gradient-free gated edit

The primary direct-versus-bridge mechanistic statistic is a nuisance-subtracted difference-in-differences: the posterior-swap effect in bridge minus the matched effect in direct, after subtracting the same-posterior/topology control in each condition.

The first repair is a reader-gated margin edit of the schematic form:

```text
belief_state    = model_internal_z(h)
threshold_state = model_internal_t(h)
margin_state    = f(belief_state, threshold_state)

# Core: write structurally on the independently validated natural path.
delta_h_on_validated_path = writer(margin_state) × strength

# Optional only after the independent r_need factorial succeeds.
delta_h_on_validated_path = r_need(h) × writer(margin_state) × strength
```

The exact parameterization follows the validated causal abstraction. The prediction is selective improvement on inference-good/direct-use errors, little change on direct-correct items, and no benefit when either reader or writer is randomized.

### 11.3 Required baselines

- unconditional writer edit;
- reader-only and content-only edits;
- random reader, random writer, wrong layer, wrong sign;
- gold-posterior bridge as a nondeployable ceiling;
- prompt-only self-bridge;
- if and only if the low-rank stretch line is activated: rank-matched LoReFT and rank-8 LoRA as a performance upper bound, not the claimed method.

### 11.4 LoRA-derived prediction, if needed

Train multiple LoRA seeds only after the natural path is confirmed. Use SVD/Gram analysis to determine whether effective changes concentrate in the localized modules and a stable low-rank subspace. A low-rank spectrum predicts that small-rank ReFT should approach LoRA; that prediction is tested once on D2-ID if this stretch line is activated.

If LoRA succeeds through unrelated modules or high-dimensional changes, it does not validate the proposed mechanism.

---

## 12. Confound and negative-control suite

### Numerical/token controls

- fixed-width eight-token numbers;
- matched token fertility and digit positions;
- round/non-round `2×2` with correct/counterfactual content;
- matched numerical distance and threshold side;
- matched baseline semantic logit and action direction;
- digit-multiset or edit-distance controls where feasible;
- full-candidate teacher-forced A/B scoring.

### Semantic controls

- neutral actions and pseudowords;
- rule polarity and clause order;
- both option mappings analyzed separately;
- irrelevant and explicit-ignore numbers;
- topology-matched role paraphrases that do not reduce to detecting the token `posterior`;
- same posterior from different evidence decompositions;
- same action with different posterior magnitude;
- counterfactual posterior with unchanged surface label.

### Intervention controls

- self/no-op patches;
- batch-local identical-shape baselines;
- random layers, positions, heads, latents, and subspaces;
- norm-matched random directions;
- noising/denoising agreement;
- activation norm, Mahalanobis distance, and off-manifold degeneration;
- unrelated arithmetic, factual, attribute, and instruction-following tasks.

### Replication controls

- anchor versus posterior-estimation/report-poor and action-good behavioral contrasts;
- instruct versus base where practical;
- at least one held-out template and likelihood regime;
- an external task only if T1 is selected as the required-generality route;
- no coefficient or layer retuning outside D1.

---

## 13. Decision tree and honest narrative pivots

### Outcome A — Direct posterior absent

If direct content fails cross-family and causal formation tests, the topic becomes **query/serialization-gated belief formation**, not routing failure. The method target is eliciting/forming a usable belief state. Keep the project only if this generalizes beyond one synthetic family.

### Outcome B — Direct posterior present, role gate weak

This is the strongest intended result. Show content/role separation, transport interaction, and selective gated rescue.

### Outcome C — Direct code is misaligned

The story becomes **context-specific belief codes and interface alignment**. A fixed low-dimensional alignment must generalize across held-out likelihoods and tasks; otherwise it is an in-sample decoder trick.

### Outcome D — Comparator or binding failure

Pivot to the localized failing stage only if causal evidence clearly separates comparator from semantic action and option binding.

### Outcome E — Only textual substitution works

If no selective transport component or held-out causal path survives, do not claim a belief-use circuit. The layer trajectory remains a diagnostic observation, but the mechanism paper is not ready.

### Outcome F — Repair needs gold posterior or harms controls

Drop the method claim. A repair that secretly supplies the answer does not validate the mechanism.

### Outcome G — No external transfer

Do not expand claims to general latent-belief use. A successful contrast-model replication may still support model-level generality while keeping the task claim synthetic; otherwise find a second naturally aligned task before submission or present/archive the project as a synthetic mechanistic case study.

### Outcome H — Only a generic authority gate survives

If `G_posterior > 0` but `G_generic_control ≈ G_posterior` and `G_specific ≈ 0`, reject the posterior-specific role-reader claim. The supported mechanism is generic external numeric authority/compliance. Keep it only as a renamed topic if it survives the secondary non-Bayesian control, appears across task families, and remains causally distinct from answer-label bias; otherwise treat role gating as a confound rather than a result.

These are narrative pivots, not post-hoc threshold changes. The mother question remains fixed; the answer may differ.

---

## 14. Paper-sized deliverable

### Target story

Provisional title:

> **Knowing Is Not Using: How Serialized Beliefs Become Causal Inputs to Language-Model Decisions**

Desired abstract-level findings, conditional on confirmation:

1. open-weight models dissociate posterior estimation, direct policy use, and explicit-belief execution;
2. identify the minimal serialized causal carrier and test whether a middle-layer path transfers its control;
3. belief content and causal role are separable, with a role-gated transport path linking content to comparison and action;
4. a mechanism-derived path-specific edit selectively repairs inference-good use failures;
5. the stage-level effect passes the chosen generality validation: either a contrast model or an official latent-belief decision benchmark.

“Low-rank” enters finding 4 only if the validated natural path itself exhibits stable low-dimensional geometry on D1 and the frozen low-rank prediction succeeds on D2-ID. It is not part of the default story.

This is appropriately narrower than “how LLMs reason” and broader than “one Qwen layer contains a posterior direction.”

### Minimum figures

1. behavioral formation/use/execution dissociation across models;
2. content × role factorial and causal sensitivity interaction;
3. layer timeline overlaying decodability and natural causal recovery;
4. exact transport/path localization with controls;
5. selective repair versus unconditional edit and, only if enabled by the low-rank analysis, LoRA/LoReFT ceilings;
6. the chosen generality validation: one contrast-model replication **or** one external-transfer figure.

### Core, required generality, and stretch

**Core:** Qwen2.5 D2-ID; content × role causal interaction; exact transport/comparator path; direct diagnosis; natural/path-specific rescue.

**Required generality:** either one contrast model or one external task before the main claim is expanded beyond the anchor setting.

**Stretch:** whichever generality route was not selected, the second contrast model, T1 beyond a selected model replication, LoRA multi-seed SVD, LoReFT, Gemma-Scope, and base/instruct comparisons. These activate only when the natural mechanism predicts them and are not completion gates for the core paper.

There is no requirement to duplicate exact head identities or every path analysis across models.

---

## 15. Reproducibility and result governance

Every run manifest must record:

- claim ID and exploratory/dev/confirmatory status;
- Git commit and dirty-worktree flag;
- exact model repository and revision;
- tokenizer revision and token audit;
- config checksum and dataset checksum;
- seed, dtype, device, batch shape, and scoring convention;
- split and causal-family IDs;
- layer/latent/rank/strength selection source;
- raw output path and generated summary path;
- supersedes/superseded-by relation.

The result index must mark the original FP16/cross-batch direct-query outputs `invalidated`, record that current causal pairs are baseline-correct discovery examples, and report effective unique evidence/value counts rather than duplicated threshold/mapping rows.

Directory policy:

```text
mechanism/
├── configs/
│   ├── discovery/
│   ├── dev/
│   └── confirmatory/
├── manifests/
├── results/
│   ├── discovery/
│   ├── dev/
│   └── confirmatory/
├── src/
├── tests/
├── CLAIM_EVIDENCE_LEDGER.md
└── MECHANISM_LOG.md
```

Final tables and figures must be regenerated from raw outputs by one command. Manual transcription is prohibited. Compact canonical summaries are committed to Git; large activations remain ignored and receive checksums plus external artifact locations if the project reaches submission.

The old FP16/cross-batch direct-query outputs are explicitly superseded and must never enter a final table.

---

## 16. Execution order after approval

No experiment is run as part of writing V2. When execution resumes:

1. freeze D1, D2-ID, and one-factor D2-OOD families, manifests, token audit, and automatic report schema;
2. run the cheap content × role behavioral factorial;
3. test direct posterior identity/formation on Qwen only;
4. screen layers 14–25, then exact-confirm shortlisted transport components;
5. test the role-reader interaction;
6. localize comparator/writer and semantic binding;
7. attempt natural bridge→direct rescue, then the gated edit;
8. freeze all choices and open D2-ID, then run the registered one-factor D2-OOD sets;
9. choose and run exactly one required-generality test: stage-level replication on one contrast model **or** one T1 external transfer;
10. only after the core and chosen generality test, decide whether a second contrast model, the unchosen T1/model route, or other replication adds useful scope;
11. activate LoRA/LoReFT only if the validated natural path first yields a low-rank prediction.

The priority is not to accumulate interpretability tools. It is to make each result eliminate a competing explanation and force the next experiment.
