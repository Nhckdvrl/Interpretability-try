# Continuation Search — Terminal Addendum II (2026-08-31)

This file freezes additional scientific objects seriously audited after `continuation_mother_search_2026-08-31.md`. It is negative memory. Do not revive an object by switching the entity domain, benchmark, rating scale, language, model family, or MI tool unless its explicit resurrection condition is met.

---

## 1. Popularity / Fame ≠ Quality / Acclaim — KILL-N0/N1

**Natural question:** Something can be widely known or frequently consumed without being highly regarded, and a niche item can be highly regarded without being popular. Does a model represent popularity and quality as separate properties rather than collapsing them into one generic item-value/salience axis?

**Why it looked good:**

- the distinction is ordinary and externally meaningful before any dataset exists;
- movies, books, music and products naturally contain all four cells (popular/high-quality, popular/low-quality, niche/high-quality, niche/low-quality);
- large real artifacts can provide popularity and evaluation signals on the same items without LLM judges;
- a shared-scalar vs separate-axes causal question would remain meaningful even if the model separates the axes perfectly.

**Kill evidence:**

The title-level object is already occupied in the recommendation literature. A 2026 paper is explicitly titled **Disentangling popularity and quality: An edge classification approach for fair recommendation**, framing high-quality long-tail items versus genuinely low-quality items as the central distinction. More importantly for internal representation, FAccT 2026 **Aligning Recommendations with User Popularity Preferences** identifies a controllable popularity direction in representation space and performs activation steering with direction and magnitude adjusted per user. LLM/recommender work in 2026 also treats popularity bias, recommendation quality, long-tail behavior and preference intensity as explicit modeling dimensions. A new project asking whether a language model hidden state separates `fame` from `quality` would therefore transplant an already explicit recommendation-system factorization into mechanistic-interpretability vocabulary rather than establish a new title-level scientific object.

**Death code:** `NARRATIVE_COLLISION / DIRECT_REPRESENTATION_NEIGHBOR`

**Nearest-neighbor warning:** do not revive as fame-vs-goodness, popularity-vs-rating, exposure-vs-quality, mainstream-vs-acclaimed, cult-classic-vs-blockbuster, or by switching from movies to books/music/products.

**Resurrection condition:** a different real-world property whose scientific distinction is not already an explicit debiasing/factorization target and whose mechanism is not reducible to an existing popularity direction plus another ordinary item score.

**References:**

- https://doi.org/10.1016/j.asoc.2026.115619
- https://doi.org/10.1145/3805689.3806483
- https://aclanthology.org/2026.acl-long.656/

---

## 2. Strong Memory ≠ Executive Control — KILL-N0

**Natural question:** A system may retain information well while still being poor at inhibiting a dominant response, switching rules, or maintaining goal-directed control. Are memory capacity and executive control distinct bottlenecks in LLM cognition?

**Why it looked good:**

- memory and control are classic cognitive constructs rather than LLM-internal labels;
- the 2026 study evaluates multiple modern open families, including Gemma, Llama and Qwen;
- the headline dissociation is large enough to tempt a mechanistic follow-up.

**Kill evidence:**

The mother paper is literally **Strong Memory, Weak Control: An Empirical Study of Executive Functioning in Large Language Models**. It already owns the title-level scientific object: memory performance can be strong while inhibitory/cognitive-control performance remains weak. Its test battery includes the exact executive-function families that would motivate a control-mechanism analysis. Recasting the result as `memory state exists but control/readout fails` and adding activation patching would be the prohibited `mother behavior → mechanism` shape. In addition, rule-switching/task-switch carryover is explicitly excluded by the repository's current search policy.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as memory-vs-inhibition, storage-vs-control, recall-vs-rule switching, knowledge-retention-vs-executive function, or by selecting only one cognitive test.

**Resurrection condition:** a qualitatively different natural control phenomenon whose headline is not the memory/executive-control dissociation and whose behavior survives outside synthetic cognitive-test protocols.

---

## 3. Rank Fidelity ≠ Absolute Calibration — KILL-N0/N1

**Natural question:** A model can order cases correctly from easier to harder (or weaker to stronger) while assigning systematically wrong absolute scores. Are relative ordering and absolute calibration different computations?

**Why it looked good:**

- ordinal ordering and cardinal calibration are genuinely distinct;
- real exams and human-scored artifacts can provide independent external targets;
- recent educational studies report moderate/high rank fidelity alongside systematic score or difficulty bias.

**Kill evidence:**

The scientific object is already explicit in current evaluation work. The 2026 ENEM difficulty paper evaluates LLMs on **absolute calibration, rank fidelity, and context sensitivity** against official IRT parameters for 1,031 exam items and reports moderate ranking ability together with systematic difficulty underestimation. 2026 high-stakes grading work similarly reports strong rank-order correlations but poor categorical/absolute agreement. This is also a domain-specific instance of the already-killed `ordinal comparison ≠ cardinal magnitude` family. A mechanistic paper that asks whether the model stores an ordinal score separately from a cardinal score would therefore be adjective/domain narrowing after N0/N1 collision.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as ranking-vs-scoring, difficulty-order-vs-IRT-value, relative-vs-absolute grading, discrimination-vs-calibration, or by moving from education to medicine/hiring/review scoring.

**Resurrection condition:** a non-score/non-magnitude scientific relation where relative structure is not simply a transformation of a cardinal target and where the mother literature does not already define ranking versus calibration as the core evaluation distinction.

**References:**

- https://arxiv.org/abs/2602.06631
- https://doi.org/10.1080/10872981.2026.2684837

---

## 4. Moral Ordering ≠ Moral Intensity / Extremity — KILL-S0/N0

**Natural question:** A model might broadly agree with humans about which scenarios are more moral or immoral while systematically exaggerating how good or bad they are. Does it represent moral direction/order separately from moral intensity?

**Why it looked good:**

- a preregistered 2025 Scientific Reports study with N=940 humans found near-perfect scenario-level correlations but systematic extremization and rating clumping;
- the behavior superficially resembles a useful `qualitative sign/order vs quantitative gain` dissociation;
- the study releases analysis materials.

**Kill evidence:**

The available existence substrate is only 60 scenarios and the reported model evidence is centered on text-davinci-003/GPT-4o rather than the current interpretable open-model families required by S0. More importantly, the mother's headline is already that high correlation hides systematic moral-rating extremity/calibration error. Recent 2026 moral-judgment work expands to 1,618 real-world dilemmas and explicitly models consensus, disagreement and value diversity, while internal moral-representation work is already active. Narrowing the mother to `polarity/order vs intensity` would therefore be both under-supported on current open checkpoints and narratively narrower than the existing human–LLM moral-judgment object.

**Death code:** `INSUFFICIENT_OPEN_MODEL_EXISTENCE / NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as moral polarity-vs-strength, direction-vs-intensity, rank-vs-extremity, moral calibration, or by collecting another small moral rating scale.

**Resurrection condition:** a large natural item-level population on which at least two modern open families independently reproduce a broad monotonic-order / systematic-intensity dissociation, plus a new scientific variable not already equivalent to moral calibration or human-value distribution modeling.

**References:**

- https://www.nature.com/articles/s41598-025-24700-6
- https://aclanthology.org/2026.eacl-long.241/

---

## 5. Explicit Recall ≠ Implicit Behavioral Adaptation — KILL-N0/S0

**Natural question:** Remembering an experience explicitly is not the same as automatically changing behavior because of that experience. Does an LLM have separable explicit and implicit memory systems?

**Why it looked good:**

- declarative versus non-declarative/implicit memory is a classic cognitive distinction;
- ACL 2026 ImplicitMemBench reports large modern-model deficits and a striking preference-versus-inhibition asymmetry across 17 models, including Qwen3 and DeepSeek-R1;
- the natural mechanism fork would appear to be retrievable content versus automatically enacted policy change.

**Kill evidence:**

The mother paper explicitly frames its contribution as moving from `what agents recall` to `what they automatically enact` and defines procedural memory, priming and classical conditioning as the core scientific object. Therefore explicit-versus-implicit memory is already the mother narrative, not a new extension. Its 300-item Learning/Priming–Interfere–Test suite is also a constructed cognitive-test protocol rather than a broad natural population, so a failure-mechanism paper cannot use the benchmark alone as S0 evidence under the repository's current contract.

**Death code:** `NARRATIVE_COLLISION / SYNTHETIC_PROTOCOL`

**Nearest-neighbor warning:** do not revive as recall-vs-habit, declarative-vs-procedural, preference-learning-vs-inhibition-learning, priming-vs-explicit memory, or by selecting one of ImplicitMemBench's subtests.

**Resurrection condition:** a naturally occurring behavioral adaptation phenomenon with external ground truth that is not already reducible to the mother benchmark's explicit/implicit memory framing.

**Reference:** https://aclanthology.org/2026.acl-long.1301/

---

## Search-state consequence

This batch reinforces a stronger negative lesson:

```text
natural orthogonal axes + huge public dataset
is still not enough when the distinction is already an explicit scientific object elsewhere.
```

and

```text
mother reports a large dissociation
is still not enough when our only novelty would be to rename its two sides as hidden-state variables.
```

As of this addendum, no new candidate from these families reaches `PASS-REGISTER`.
