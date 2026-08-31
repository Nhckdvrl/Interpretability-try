# Continuation Terminal Addendum 4 — 2026-08-31

This file records serious candidates audited after `continuation_terminal_addendum_3_2026-08-31.md`. Latest handoff/gates remain authoritative. None of the topics below is a `PASS-REGISTER`; changing model, dataset, language, prompt, or interpretability tool does not by itself reopen them.

---

## 1. Surface color ≠ illumination-caused appearance / color constancy

**Natural question.** When lighting changes the pixels reflected by an object, does a model preserve the object's surface color rather than confusing current appearance with intrinsic color?

**Why it looked good.** Color constancy is a classical perceptual object, not a VLM-native benchmark concept. It naturally separates an object property from a context-dependent appearance and would support a real mechanism fork: stable surface-color state vs direct readout of local chromatic evidence.

**Kill evidence.** Current evidence did not establish the required behavior-first phenotype on modern interpretable open VLMs. 2026 work demonstrates that dedicated color-constancy correction can be engineered/fine-tuned, while contemporary VLM benchmarks also show that fine-grained color recognition itself remains imperfect. That is insufficient to establish the sharper dissociation required here: object/content recognition remains intact, but illumination alone systematically rewrites the model's judgment of surface color across modern open families. Building paired color-chart or relighting stimuli ourselves before demonstrating that naturally occurring phenotype would reverse the repository's S0 order.

**Death code.** `KILL-S0 / NO-ESTABLISHED-OPEN-MODEL-PHENOTYPE`

**Nearest-neighbor warning.** Do not resurrect this by switching to another color chart, synthetic relighting engine, language, weaker checkpoint, or probe. A color-recognition deficit is not color-constancy failure.

**Resurrection condition.** A broad natural/externally grounded relighting substrate must show a large paired illumination-induced surface-color failure on at least 2/3 modern interpretable open families under ordinary prompts, with object recognition/capability controls already passing.

---

## 2. Physical ordering ≠ physical magnitude / unified visual magnitude compression

**Natural question.** Do VLMs preserve which physical quantity is larger while systematically compressing how much larger it is?

**Why it looked good.** Several physical-estimation tasks show regression-to-the-middle or large-magnitude underestimation, suggesting an appealing psychophysical story: an ordinal quantity code might survive while a cardinal magnitude readout is compressed. If shared across count, length, mass, portion size, etc., this would be much wider than one benchmark.

**Kill evidence.** The strongest neighboring work already occupies the key internal object. 2026 visual-counting work reports that visual representations can linearly encode quantity and support relative comparison while exact enumeration fails at the mapping from visual magnitude to discrete symbolic output, explicitly advancing a fragmented-magnitude/symbolic-mapping account. Contemporary causal work additionally uses mediation/activation intervention to localize counting mechanisms. Recasting mass/portion underestimation as `ordinal state -> cardinal writer` would therefore collapse into an existing visual-magnitude-to-symbolic-mapping family unless a genuinely different cross-quantity mechanism were first established. No such independent cross-quantity phenotype was found.

**Death code.** `KILL-N1 / VISUAL-MAGNITUDE→SYMBOLIC-MAPPING-ALREADY-MECHANISTIC`

**Nearest-neighbor warning.** Do not resurrect with distance, count, area, portion, weight, another output unit, or a different visual model if the novelty remains `relative quantity survives but exact number fails`.

**Resurrection condition.** Only a new cross-quantity behavioral law with a mechanism that cannot be reduced to the already studied visual-magnitude/symbol mapping (for example, a causal interference between two distinct physical attributes) would justify reopening.

---

## 3. Visual evidence ≠ canonical parametric prior under counterfactual images

**Natural question.** Why can a VLM recognize an object in an edited image yet answer with the object's memorized canonical attribute instead of the visible counterfactual attribute?

**Why it looked good.** The behavior is large and counterintuitive: recent VLM evaluations report near-perfect performance on ordinary canonical images but severe collapse after small counterfactual edits. It superficially offers a strong mechanism fork between failed visual encoding, parametric-prior overwrite, and late conflict resolution.

**Kill evidence.** This fork has already been causally resolved by direct 2026 mechanistic neighbors. `Vision-Default, Prior-Override` analyzes perception–knowledge conflict across multiple VLM families with residual/head/MLP activation patching and identifies a sparse set of late attention heads through which the parametric prior overrides visual evidence, further decomposing the mechanism into routing and writing roles. ACL 2026 work likewise identifies heads that can steer models between visual evidence and internal knowledge. This is an exact `behavior -> routing/writing causal mechanism` collision, not merely related work.

**Death code.** `KILL-N1 / EXACT-CAUSAL-MI-COLLISION`

**Nearest-neighbor warning.** Do not resurrect by changing the edited attribute, object category, VLM family, benchmark, or by renaming routing/writing as reader/writer.

**Resurrection condition.** A distinct natural conflict whose scientific object is not perception-vs-parametric-knowledge arbitration and whose causal mechanism is demonstrably not the already identified conflict-routing/writing pathway.

---

## 4. Likelihood ≠ severity / risk factorization

**Natural question.** Does a model represent `how likely a harmful event is` separately from `how bad it would be if it happened`, or collapse both into a single dangerousness signal?

**Why it looked good.** Likelihood and severity are constitutive components of risk rather than arbitrary labels. Natural cross-cells (likely/mild, unlikely/severe, etc.) are ubiquitous, and the scientific question remains meaningful even if the model separates the axes perfectly.

**Kill evidence.** A 2026 direct neighbor, `Expected Harm: Rethinking Safety Evaluation of (Mis)Aligned LLMs`, already makes this exact factorization central: severity alone is insufficient and execution likelihood/cost must be modeled separately. More importantly for this repository, the work performs latent probing and reports that model representations encode severity while lacking an equally distinguishable execution-cost/likelihood representation. Thus `one risk scalar vs separate severity/likelihood axes` is already an internal-representation scientific object; moving to medicine, disasters, finance, or another risk dataset would be a domain swap rather than a new title-level question.

**Death code.** `KILL-N1 / EXACT-FACTORIZATION-COLLISION`

**Nearest-neighbor warning.** Do not resurrect as probability vs impact, frequency vs harm, chance vs consequence, expected harm components, or another domain's risk matrix.

**Resurrection condition.** A genuinely different risk component whose theoretical distinction and internal mechanism are not subsumed by severity × execution-likelihood/expected-harm factorization.

---

## Non-terminal notes (not survivors)

Two leads remain below registration and are intentionally **not** counted as survivors:

- `Visual size -> mass prior / size–weight-style illusion`: `PRE-S0 LEAD`. Real mass gold and deterministic metric-size recovery are available in candidate substrates, but no item-level modern-open-family evidence yet shows that mass residuals are systematically driven by visible size. Ordinary mass estimation error is insufficient.
- `Relational essentialization (species invasive status × region)`: `PRE-G0 / NOT REGISTERED`. Country-level expert status data are promising, but row-level natural flip counts and open-family essentialization behavior have not yet been parsed/established. Generic relation binding is already occupied by 2026 causal representation work.

No candidate in this addendum passes the current bar.
