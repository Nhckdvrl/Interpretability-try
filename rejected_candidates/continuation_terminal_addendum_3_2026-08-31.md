# Continuation Search — Terminal Addendum III (2026-08-31)

This file freezes scientific objects seriously audited after the authoritative `HANDOFF_HAMDI_SEARCH_2026-08-31.md` and the previous continuation addenda. It exists to prevent attractive dead objects from being rediscovered after changing dataset, model, modality, prompt, or MI tool.

**Authority rule:** for the objects below, this file supersedes older `PRE-CANDIDATE`, `SURVIVOR`, `HOLD`, or `under audit` wording unless an explicit resurrection condition is later satisfied.

---

## 1. Conservation under Physical Transformation — KILL-N0

**Natural question:** When appearance changes but quantity should remain invariant, why can a model confuse transformation with change in amount?

**Why it looked good:**

- classical Piagetian conservation is a natural cognitive object independent of VLMs;
- ConservationBench uses real transformation videos rather than a synthetic-only existence substrate;
- the reported behavioral failure is enormous across many VLMs, with human performance near ceiling and most models failing the strict conservation/non-conservation paired criterion;
- plausible mechanisms include endpoint-state encoding failure, invariant-tracking failure, and late appearance-prior override.

**Kill evidence:**

The 2026 mother paper itself is titled around the inability of VLMs to reason about physical transformation and explicitly makes conservation versus matched non-conservation, the appearance-change/invariance conflict, and the finding that visual evidence can hurt judgment central to its scientific narrative. Under the current N0 rule, asking which internal stage causes that same failure is exactly `mother behavior -> mechanism`, even if activation patching has not yet been performed. The old `rejected_candidates/physical_cognition.md` wording `PRE-CANDIDATE / SURVIVOR` is therefore stale and is superseded by this terminal decision.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as invariant state vs appearance state, endpoint perception vs transformation tracking, quantity conservation circuit, or visual-prior override by changing conservation domain/model/MI technique.

**Resurrection condition:** a different physical invariant with a title-level behavioral dissociation not already owned by a transformation/conservation mother, and whose mechanism predicts a qualitatively different intervention.

---

## 2. Recognition != Recall / Entity Known != Name Retrievable — KILL-N0/N1

**Natural question:** A person can recognize someone and know many facts about them yet fail to retrieve the name. Do LLMs likewise separate stored entity knowledge from lexical recall?

**Why it looked good:**

- recognition versus recall is a classic memory distinction, not an LLM-native benchmark label;
- entity facts and entity names give a clean forward/inverse mapping;
- a mechanistic fork between absent knowledge and failed name binding/readout would be easy to explain.

**Kill evidence:**

Google Research 2026 `Empty Shelves or Lost Keys? Recall Is the Bottleneck for Parametric Factuality` already makes encoding, recall, and recognition the central scientific decomposition at very large scale, showing that models can encode facts that they cannot directly recall and that reverse retrieval is especially difficult. Earlier work also directly compares recognition and recall in LMs. A new project locating an entity representation and a failed lexical-name binding/readout would therefore be a mechanistic successor to an already explicit `knowledge present but recall inaccessible` object rather than a new title-level question.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as tip-of-the-tongue in LLMs, inverse factual recall, entity-to-name binding, recognition-without-generation, lost-key circuit, or by replacing entities with books/places/people.

**Resurrection condition:** a memory distinction not reducible to encoding/recognition/recall or inverse retrieval, with a separate natural behavior and competing causal mechanisms.

---

## 3. Content Memory != Source / Speaker Memory — KILL-N0

**Natural question:** Remembering what was said is not the same as remembering who said it or where it came from. Does a model preserve content while losing source binding?

**Why it looked good:**

- item memory versus source memory is a classical cognitive distinction;
- multi-speaker natural discourse permits objective content and speaker identity without an LLM judge;
- the obvious mechanism fork is content state versus source/index binding.

**Kill evidence:**

2026 multi-speaker understanding work already makes the `what` versus `who` dissociation a headline object: models can capture content substantially better than speaker identity/binding, and dedicated benchmarks are built around speaker-content association. Reframing that result as a hidden content state plus source-binding circuit and adding causal MI is therefore mother-behavior-to-mechanism, not a new object.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as quote-to-speaker binding, provenance memory, who-said-what memory, source tag loss, or by changing dialogue corpus.

**Resurrection condition:** a source-memory phenomenon not already reducible to speaker/content association or ordinary provenance attribution, with a distinct behavioral anomaly and method consequence.

---

## 4. Object Identity != Current Functionality / Broken-State Affordance — KILL-N0

**Natural question:** A broken chair is still a chair even if it is no longer safe to sit on. Does a model separate what an object is from what its current state allows it to do?

**Why it looked good:**

- identity and current affordance/function are naturally different properties;
- broken/intact instances offer intuitive natural cross-cells;
- possible mechanisms include persistent category identity versus state-conditioned affordance binding.

**Kill evidence:**

2026 object-state/affordance work already treats `object + current state + affordance` as the core scientific object, and broader physical-perception taxonomies explicitly model object, material, physical property, affordance, and function together. Restricting that occupied object to broken/intact cases would be subtype narrowing, not a new title-level scientific object.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** broken-vs-intact affordance, damaged-tool usability, state-dependent function, identity-vs-function, or another embodied dataset are the same occupied neighborhood.

**Resurrection condition:** an independently established state-dependent behavior whose title cannot be restated as generic state-conditioned affordance/function reasoning.

---

## 5. Semantic Fluency: Cluster Generator vs Switch Controller — KILL-N1

**Natural question:** When listing examples from a category, does a model use one semantic-search process or separate mechanisms for exploiting a local cluster and switching to a new cluster?

**Why it looked good:**

- semantic fluency is a mature human cognitive phenomenon;
- cluster exploitation versus switching naturally suggests competing internal control mechanisms;
- ordinary prompts can expose the behavior without a benchmark.

**Kill evidence:**

2026 work explicitly studies mechanistic interpretability of semantic-memory foraging in LLMs and analyzes convergent versus divergent search signatures across model layers. Therefore the attractive `generator vs switch controller` mechanism is not an open scientific object; it is already part of an active mechanistic program.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** do not revive as category-list switching, local semantic cluster vs global jump, exploit/explore in word generation, or by using another category list.

**Resurrection condition:** an everyday retrieval phenomenon with a different cognitive object and a causal computation not reducible to semantic-search exploit/switch dynamics.

---

## 6. What != Where / Object Recognition != Localization — KILL-N1

**Natural question:** Knowing what object is present and knowing where it is are distinct. Are object-content and spatial-location representations causally separable in VLMs?

**Why it looked good:**

- category and location have independent objective gold in natural images;
- object identity can be correct while spatial binding/localization fails;
- the mechanism naturally suggests content versus binding/index states.

**Kill evidence:**

By 2025-2026 this exact internal object is already occupied. Mechanistic VLM work directly compares classification and localization, and 2026 `Grounding Isn't Knowing` uses token ablation, layer probes, attention knockout, and causal mediation in modern open VLMs to study how object grounding and spatial reasoning share early computation and later diverge. ACL 2026 work also explicitly frames segmentation as disentangling `what` from `where`. A new causal patching paper on object-content versus location binding would therefore collide directly.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** do not revive as object token vs box token, recognition vs grounding, content vs coordinate binding, classification vs localization, or by switching image datasets.

**Resurrection condition:** a different binding variable not reducible to spatial localization/grounding and not already mechanistically studied.

---

## 7. Stock != Flow — KILL-N0

**Natural question:** A stock is an accumulated state while a flow is a rate of change. Why can a reasoner confuse the two even when both quantities are available?

**Why it looked good:**

- stock-flow failure is a classic systems-thinking/cognitive phenomenon;
- the distinction is mathematically and scientifically natural;
- potential mechanisms include rate/state encoding and accumulation.

**Kill evidence:**

2026 financial-reasoning work already explicitly diagnoses stock-flow caliber mismatch and related de-cumulation/period-conversion errors as central failure types, and shows large dependence on formula/structural hints. Its benchmark construction also contains automatically generated/adversarial trap structure. A new `stock accumulator vs flow reader` MI project would both follow the mother's named failure and inherit a less-than-ideal existence substrate.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as balance-vs-income, level-vs-rate, stock-vs-change, cumulative-vs-period quantity, or by changing finance to population/climate.

**Resurrection condition:** a large natural non-benchmark population showing a stable current-open-family stock-flow anomaly not already defined by the mother task.

---

## 8. Thematic Content != Agent/Patient Role — KILL-N1

**Natural question:** Representing the words/events in a sentence is not enough; `dog bites man` and `man bites dog` contain the same entities and predicate but reverse who did what to whom. Does the model bind content to semantic roles separately?

**Why it looked good:**

- thematic role binding is a natural linguistic-cognitive object;
- role reversal gives clean matched structure;
- a content-vs-role/index mechanism would be highly interpretable.

**Kill evidence:**

2026 internal-representation work directly asks whether language models know who did what to whom, studies hidden sensitivity to thematic-role reversals, and identifies attention heads that robustly encode agent/patient roles even when broader sentence representations are relatively insensitive. That directly occupies the internal role-binding object.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** do not revive as agent-vs-patient binding, semantic-role swap, subject/object reversal, who-did-what-to-whom circuit, or by changing language/corpus.

**Resurrection condition:** a non-thematic binding relation with independent natural gold and a distinct causal computation.

---

## 9. Descriptive Norm != Injunctive Norm (`Common != Right`) — resurrection check failed; prior KILL-DATA unchanged

**Natural question:** What people commonly do and what people think one ought to do are distinct social facts.

**Why it was rechecked:** the older repository decision allowed resurrection if a broad row-level natural corpus appeared with human commonness/prevalence and ought/approval judgments for the same behaviors.

**Result:** 2025-2026 work and meta-analyses continue to treat descriptive and injunctive norms as distinct, but the artifacts found in this continuation remain small behavior sets, experimental manipulations, or cross-study aggregates rather than a broad same-behavior double-gold population. The explicit resurrection condition is therefore not met.

**Death code:** `ARTIFACT_FAILURE` (unchanged)

**Nearest-neighbor warning:** experimental messages saying `most people do X`, small vignette sets, or combining separate studies do not satisfy the natural row-level substrate requirement.

**Resurrection condition:** unchanged: a large released same-behavior corpus with independently elicited descriptive-prevalence and injunctive/approval gold and useful natural cross-cells.

---

## Active leads explicitly NOT promoted by this addendum

### Size / Volume != Mass / Density (`size -> mass shortcut`)

Current status: `PRE-S0 LEAD / NOT REGISTERED / NO MI AUTHORIZED`.

- VisPhysQuant provides real multi-view RGB-D objects and measured mass; its public code can derive metric x/y extents from depth and camera intrinsics, but the released lightweight metadata itself contains only object ID, mass, and image paths, so full metric-size extraction still requires processing the raw RGB-D artifact.
- Amazon Berkeley Objects provides a much larger natural alternative with product dimensions, weight, material, and images on the same real product listings.
- No evidence has yet established the necessary phenotype: mass-estimation residuals must systematically track visual size/volume on current analyzable open VLM families, especially in natural small-heavy and large-light cross-cells. Improvement from explicit scale cues is not sufficient evidence of a size-to-mass shortcut.
- If the phenotype does not exist broadly, kill rather than manufacture a subset.

### Causal Relevance != Causal Selection (`cause` vs `contributing/background factor`)

Current status: `PRE-G0 / UNDER S0-N1 AUDIT / NOT REGISTERED`.

- NTSB aviation findings provide an unusually promising real-world expert substrate. Historical `cause_factor` explicitly codes `C` (cause), `F` (factor), or blank finding; 2024 NTSB releases preserve legacy C/F and add `cm_inPC`, indicating whether a finding appears in the probable-cause statement as a cause or contributing factor.
- The distinction is independently natural in causal philosophy/cognition: many causally relevant conditions are not selected as the explanatory cause.
- However, using the NTSB taxonomy merely to train a `C` vs `F` probe would violate the repository's `existing labels -> disentangle with MI` prohibition. A viable project requires an independently established open-model behavioral dissociation: e.g. models correctly recognize causal relevance yet systematically fail expert-like causal selection.
- 2025 `AC-Reason` already occupies formal actual-causality reasoning using sufficiency, necessity, and normality, so exact N1 must show that real-world causal selection is not merely another actual-causality benchmark/mechanism follow-up.
- Bulk C/F counts and current-open-family G0 have not yet been completed. Do not promote before both are resolved.

---

## Search lesson

This continuation again confirms that a classic cognitive distinction is not automatically a new MI topic. Several exceptionally natural pairs (`recognition/recall`, `what/where`, `content/source`, `content/semantic role`) fail because recent work already uses that distinction as the scientific object itself. The remaining promising shape is narrower: **a real-world distinction with expert/objective gold plus a large current-open-model behavioral dissociation that prior work has not already named, where causal MI can adjudicate genuinely different computations rather than merely localize a known benchmark error.**
