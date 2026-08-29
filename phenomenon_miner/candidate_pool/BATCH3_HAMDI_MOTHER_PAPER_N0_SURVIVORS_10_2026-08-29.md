# Batch 3：Hamdi-style Mother-Paper Extensions — 10 个 reviewer-mode N0 survivors

日期：2026-08-29
状态：`MOTHER-PAPER-GROUNDED / REVIEWER-MODE-N0-SURVIVOR / NOT DISPATCHABLE`

```yaml
batch: 3
method: mother-paper-extension
survivor_count: 10
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
validation_authorized: false
```

> 这一批改变找题方式：不从“再找一个没人写过的现象名”开始，而从已经被强论文证明值得研究的 scientific object 开始，问其未解决的 scope boundary、missing axis、causal role、mechanism boundary 或 implementation switch。每题必须回答：**母论文已经解决什么？我们的下一问为什么改变 scientific question，而不是换模型/数据/领域？**

本文件中的 `SURVIVE` 表示经过本轮 proposer→reviewer-mode 对抗式 N0 后，尚未发现 exact collision 或可完整吸收它的母命题；**不等于正式 external independent N0-PASS，更不授权 smoke**。

---

## 最终十题

| # | 新问题 | Mother paper | extension 类型 | 本轮裁决 |
|---:|---|---|---|---|
| 1 | **Alias Entrainment Transfer** | ACL 2025 *Llama See, Llama Do* | token circuit → concept boundary | `SURVIVE-A` |
| 2 | **Task-Switch TR/TL Desynchronization** | EMNLP 2024 Task Interference + ICLR 2026 TR/TL | known behavior × known decomposition → failure mechanism | `SURVIVE-A+` |
| 3 | **Dead-Branch Residue after Invalidation** | ICLR 2026 *Internal Planning* | valid branch awareness → branch lifecycle | `SURVIVE-A-` |
| 4 | **Training-Recency Conflict Arbitration** | ICLR 2026 *Fresh in memory* | readable metadata → causal use | `SURVIVE-A+` |
| 5 | **Predicate-Revision Eager-Flag Staleness** | ICLR 2026 *Filter Heads* | dual implementation → mid-instance implementation switch | `SURVIVE-A+` |
| 6 | **GeoTemporal Binding Bottleneck** | ACL 2025 *Around the World in 24 Hours* | behavioral composition gap → mechanism | `SURVIVE-A+` |
| 7 | **Action-Boundary State Routing** | ACL 2026 *Action Boundary Blindness* | behavioral elicitation gap → causal latent state | `SURVIVE-A-` |
| 8 | **Resolved-Ambiguity Neuron Persistence** | EMNLP 2025 *Sparse Neurons Carry Strong Signals of Question Ambiguity* | feature discovery → semantic identity of feature | `SURVIVE-A` |
| 9 | **Synonym-Saturation Escape in Semantic BM25** | EMNLP 2025 *Pathway to Relevance* | discovered circuit → granularity of saturation unit | `SURVIVE-A-` |
| 10 | **Causal Retrieval Schedule** | ACL 2026 *Retrieval Heads are Dynamic* | predictive correlation → causal plan | `SURVIVE-A+` |

---

# 1. Alias Entrainment Transfer

**Mother paper.** Niu et al., ACL 2025 Main, [*Llama See, Llama Do: A Mechanistic Perspective on Contextual Entrainment and Distraction in LLMs*](https://aclanthology.org/2025.acl-long.791/). Mother result: tokens that appeared in context receive elevated later logits, even when random; a sparse set of attention heads causally mediates much of the effect. A 2026 follow-up extends reappearance effects to whole sentences: [*Sentence-Level Contextual Entrainment in Large Language Models*](https://arxiv.org/abs/2606.24077).

**Mother solved.** `same surface token/sentence appeared → same surface continuation becomes more likely` and its attention-head mechanism.

**New question.** If context mentions an entity/concept **only through alias A**, while target alias B never appears anywhere in the prompt, is B also entrained?

Examples: `International Business Machines` → target `IBM`; `New York City` → target `NYC`; a person’s full name → unmentioned canonical short name. Use aliases with stable Wikidata/entity IDs and tokenization controls.

**Decisive contrast.** `exact-target mention` vs `alias-only mention (target string absent)` vs `semantic-related non-alias` vs unrelated matched context. Measure target-logit shift and entrainment-head mediation.

**Scientific fork.** No alias transfer supports a lexical/token-copy circuit whose semantic factors only modulate gain. Selective alias transfer implies entrainment can propagate through a concept/entity representation before affecting the unseen lexical realization.

**why_not_a_rename.** Sentence-level entrainment still requires the candidate sentence itself to have appeared. Here the **scored target string never appeared**; the paper asks whether the causal unit is surface occurrence or semantic identity.

**Strongest neighbor / collision boundary.** Original and sentence-level entrainment; generic semantic priming. This topic dies if alias-only effects are indistinguishable from ordinary semantic priming or a prior paper already shows unseen-alias transfer through the entrainment circuit.

**D0.** Wikidata aliases + high-frequency entity aliases; freeze pairs where both forms are independently familiar and neither form contains the other after tokenizer normalization.

**Mechanisms.** (A) entrainment heads copy lexical identities only; (B) earlier entity canonicalization causes alias B representation to inherit A’s salience; (C) generic semantic priming, with entrainment heads irrelevant.

**Hard kill.** Alias-only target shift disappears after matching semantic relatedness, or entrainment-head ablation does not preferentially affect the alias-transfer component.

---

# 2. Task-Switch TR/TL Desynchronization

**Behavioral mother.** Gupta et al., EMNLP 2024 Main, [*LLM Task Interference: An Initial Study on the Impact of Task-Switch in Conversational History*](https://aclanthology.org/2024.emnlp-main.811/): prior conversational tasks can hurt performance after a task switch.

**Mechanism mother.** Yang et al., ICLR 2026, [*Localizing Task Recognition and Task Learning in In-Context Learning via Attention Head Analysis*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/974726d56a6ddfac48486e57d5e798e4-Abstract-Conference.html): distinct Task Recognition (TR) heads align states to a task subspace, while Task Learning (TL) heads rotate within it toward the correct label mapping.

**New question.** Is conversational task interference a **desynchronization between TR and TL**? After a switch, does TR already identify the new task while TL still applies the old mapping, or can the opposite occur?

**Decisive design.** Construct switch pairs where task identity and label mapping can be independently diagnosed. Compare clean target-task ICL, old-task→target-task switch, and label-remapped controls. Measure TSLA/TR/TL signatures before final prediction; patch only TR or only TL components from the clean target run.

**Prediction.** If interference is TR-stale, TR patch rescues task-subspace alignment; if TL-stale, TL patch rescues within-subspace rotation while TR is already correct. Different task pairs should produce different error signatures rather than one generic history penalty.

**why_not_a_rename.** EMNLP 2024 establishes a behavioral task-switch vulnerability but not its internal computation. ICLR 2026 decomposes ordinary ICL but does not study conversational task-switch history. The new scientific object is **asynchronous switching of two identified mechanisms**.

**Collision boundary.** KILL if TR/TL work or later work already applies the decomposition to task-switch interference, or if switched errors show no dissociation and are fully explained by generic context length/recency.

**D0.** Reuse task-switch mother’s public tasks plus a locked subset expressible as ICL classification with controlled label mappings.

**Mechanisms.** stale TR; stale TL; both switch correctly and interference originates downstream.

---

# 3. Dead-Branch Residue after Invalidation

**Mother paper.** Ustaomeroglu et al., ICLR 2026, [*Internal Planning in Language Models: Characterizing Horizon and Branch Awareness*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/da004051ce3fb70898f12395fc0c1fc3-Abstract-Conference.html). Mother finding: hidden states preserve information about unused **valid** continuations and exhibit task-dependent planning horizons.

**Mother solved.** Whether alternative valid branches are represented before output.

**New question.** What happens to a represented branch after a later observation/irreversible action makes it impossible? Does the representation retire, become actively suppressed, or persist and contaminate downstream planning?

**Decisive design.** Start from matched states with two valid continuations; then introduce a minimal branch-closing fact/action. Verify behaviorally that the model recognizes which branch is now invalid. Probe/compress branch information before and after closure and causally patch the pre-closure branch state into the post-closure run.

**why_not_a_rename.** “Awareness of unused valid branches” and “lifecycle of an invalidated branch” have opposite normative roles. Preserving the first is evidence of planning; preserving the second as action-driving state is a reliability failure. The extension asks for a **retirement operator**, not more branch awareness.

**Mother-inclusion risk.** This is close to the repo’s history/current-state family. It survives only if the effect is specifically tied to the mother paper’s branch representation and can be causally localized, rather than a generic stale-text preference.

**D0.** Pathfinding/game states with programmatically verified reachability plus natural-language route-planning variants; branch closure must change reachability without changing goal wording.

**Mechanisms.** branch erased; branch retained but inhibitory gate added; branch retained without lifecycle metadata.

**Hard kill.** Once invalidity recognition is gated, no branch-specific internal residue predicts behavior, or the phenomenon reduces to generic recent-context/history persistence.

---

# 4. Training-Recency Conflict Arbitration

**Mother paper.** Krasheninnikov et al., ICLR 2026, [*Fresh in memory: Training-order recency is linearly encoded in language model activations*](https://arxiv.org/abs/2509.14223). Mother finding: sequentially trained information carries a persistent, linearly decodable acquisition-recency signal not explained by simple loss/confidence statistics; the paper explicitly notes implications for conflicting data and knowledge modification.

**Mother solved.** Models can encode **when** information was learned.

**New question.** Is this acquisition-time axis merely readable metadata, or does it causally arbitrate which retained fact wins when two incompatible facts are both available?

**Decisive design.** Sequentially teach two mutually exclusive mappings/facts at known stages while balancing exposure and verifying each fact can still be elicited in isolation. In a neutral conflict query, measure preference. Then steer/patch only the recency direction while holding fact-content representations fixed.

**why_not_a_rename.** The mother establishes representation of training order, not functional use. The extension tests the causal semantics of that representation: **metadata vs priority signal**.

**Strongest neighbor.** Knowledge conflict, continual learning and recency-bias literatures. These are not enough to kill the topic unless they manipulate the *identified training-order direction* and show it controls arbitration.

**D0.** Reuse the mother paper’s sequential entity-fact training construction first, then replicate on natural relation triples with balanced templates.

**Mechanisms.** recency direction feeds conflict selector; recency is epiphenomenal while weight strength wins; recency only controls retrieval latency/confidence.

**Hard kill.** Steering the recency axis changes its probe score but not conflict choice under content-preserving controls.

---

# 5. Predicate-Revision Eager-Flag Staleness

**Mother paper.** Sharma et al., ICLR 2026, [*LLMs Process Lists With General Filter Heads*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/6732332e3c4155da82cb9d4970e88133-Abstract-Conference.html). Mother finding: LLMs use a reusable late “filter-head” predicate representation, but can instead use an eager strategy that evaluates each item early and stores an `is_match` flag when the predicate is known before the list.

**Mother solved.** Two distinct implementations of filtering and the information-timing conditions under which they are used.

**New question.** If predicate P is given before the list (encouraging eager flags) and is corrected to predicate Q **after** the list, can the model invalidate P-flags and switch to the late filter-head implementation, or do stale item flags leak into the final selection?

**Decisive factorial.** `Q-before`, `Q-after`, `P→P`, `P→Q`; choose P/Q so membership crosses in all four item categories `(P,Q)∈{00,01,10,11}`. Verify the model explicitly reports the correction and current criterion.

**why_not_a_rename.** Mother asks how information timing selects one implementation. New paper asks whether the model can **migrate state between implementations mid-instance** after a correction. This is an implementation-switch/invalidation question, not another filtering benchmark.

**D0.** Mother’s released list-filtering tasks, with minimal predicate corrections; oracle is programmatic.

**Mechanisms.** old eager flags persist; Q recomputes fresh flags; lazy Q predicate overrides but stale flags remain as competing pathway.

**Hard kill.** Corrected condition behaves exactly like Q-only and no P-specific residual can be found once explicit correction recognition is gated.

---

# 6. GeoTemporal Binding Bottleneck

**Mother paper.** Holtermann et al., ACL 2025 Main, [*Around the World in 24 Hours: Probing LLM Knowledge of Time and Place*](https://aclanthology.org/2025.acl-long.1115/). GeoTemp contains 320k prompts across 289 cities, 217 countries and 37 time zones. Models do relatively well on temporal knowledge alone, while tasks requiring temporal-geographical connection remain constrained.

**Mother solved.** Behavioral localization of a composition gap: temporal capability and geographic knowledge can be individually stronger than their joint use.

**New question.** Where is the failed join? Does the model fail city→timezone retrieval, fail offset arithmetic, or represent both correctly but fail to bind the retrieved offset into the temporal-computation pathway?

**Decisive decomposition.** For each failed joint item, capability-gate geography-only and arithmetic-only variants. Causally patch city/timezone representations from a correct geography run or arithmetic/offset states from a correct temporal run into the joint run. Compare which intervention restores the answer.

**why_not_a_rename.** The mother is a behavioral benchmark paper and leaves the central computational reason unresolved. The extension asks whether the error is **retrieval, arithmetic, or cross-domain binding**, producing different causal predictions.

**D0.** GeoTemp itself supplies natural, programmatically verifiable cases and exact counterfactual controls.

**Mechanisms.** geography retrieval failure; arithmetic failure; correct local states with failed binding/routing.

**Hard kill.** Joint errors disappear after capability gating or no stable cross-model residual remains beyond whichever component is individually wrong.

---

# 7. Action-Boundary State Routing

**Mother paper.** Wang et al., ACL 2026 Main, [*Action Boundary Blindness: When LLM Agents Cannot Tell Where One Action Ends and Another Begins*](https://aclanthology.org/2026.acl-long.1711/). Across 1,655 tasks from six agent benchmarks, the paper identifies granularity confusion, scope creep and boundary ambiguity. Explicit Boundary Prompting improves boundary scores, motivating the claim that failures may be an elicitation gap and that models have latent boundary perception.

**Mother solved.** A broad, natural behavioral phenotype and an elicitation intervention.

**New question.** What exactly is the claimed “latent boundary perception”? Does vanilla inference already contain a boundary-state representation that fails to route into action construction, or does EBP *create* a new representation that vanilla inference lacks?

**Decisive design.** Use matched vanilla/EBP pairs where EBP fixes the action but preserves task state. Train boundary-structure probes only on held-out tasks, then patch EBP boundary state into vanilla at candidate layers without copying action tokens. Test separate granularity/scope/completeness dimensions.

**why_not_a_rename.** A behavioral elicitation gap does not establish a latent internal state. The extension decides between two scientifically different explanations of the mother result: **representation exists but is unread vs representation is created by elicitation**.

**Risk.** Generic “knows but does not use” is occupied. This survives only if a boundary-specific structural representation, causal layer/path and subtype geometry are demonstrated.

**D0.** Mother’s six agent benchmarks and EBP correction pairs.

**Hard kill.** Probe signal tracks generic success/task difficulty, or EBP→vanilla patch cannot rescue boundary errors without transferring answer content.

---

# 8. Resolved-Ambiguity Neuron Persistence

**Mother paper.** Zhang et al., EMNLP 2025 Main, [*Sparse Neurons Carry Strong Signals of Question Ambiguity in LLMs*](https://aclanthology.org/2025.emnlp-main.813/). A small number of Ambiguity-Encoding Neurons (AENs), sometimes one neuron, detect ambiguous questions and can causally shift answer/abstain behavior.

**Strong neighbor.** Su & Cardie 2026, [*Knowing but Not Showing: LLMs Recognize Ambiguity but Rarely Ask Clarifying Questions*](https://arxiv.org/abs/2605.25284), already studies ambiguous/unambiguous/disambiguated questions behaviorally and finds a recognition–behavior gap.

**New question.** Do AENs encode **surface-form ambiguity** or the model’s **current unresolved posterior ambiguity**? Keep the exact same ambiguous question string, but prepend context that uniquely resolves the intended interpretation. Does the AEN state collapse?

**Decisive conditions.** Same exact question under: no context; resolving context; irrelevant matched context; misleading context. Separately check answerability/interpretation recognition and AEN activation.

**Scientific fork.** If AEN remains high after successful contextual resolution, the “ambiguity neuron” is better interpreted as a lexical/surface ambiguity detector. If it dynamically disappears and steering restores uncertainty, it behaves like a context-sensitive unresolved-ambiguity state.

**why_not_a_rename.** The mother discovers a neuron and labels its function using question classes. The extension tests the **semantic identity of that discovered feature** under a state-changing intervention while holding the question string fixed.

**Hard kill.** Mother/follow-up already performs same-surface contextual disambiguation at the AEN level, or AEN differences are fully explained by extra-context length/attention dilution.

---

# 9. Synonym-Saturation Escape in Semantic BM25

**Mother paper.** Lu et al., EMNLP 2025 Main, [*Pathway to Relevance: How Cross-Encoders Implement a Semantic Variant of BM25*](https://aclanthology.org/2025.emnlp-main.1297/). The cross-encoder implements soft semantic term frequency, term saturation, document-length effects and an IDF-like component through localized mechanisms.

**Mother solved.** A semantic BM25-like relevance circuit exists and includes saturation.

**New question.** What is the **counting unit of saturation**? If the same evidence/concept is repeated using different lexical synonyms or aliases, does the semantic matcher recognize every variant as a match while the saturation mechanism mistakenly treats them as independent term-frequency mass?

**Decisive design.** Compare equal-length documents containing: repeated exact query term; several true synonyms/aliases of one query concept; several genuinely distinct relevant concepts; semantic-related non-synonyms. Hold document length and base relevance fixed.

**Key signature.** Exact repetition saturates, but lexical-diverse synonyms of the *same concept* continue raising relevance. Mother matching heads classify them as semantic matches, while saturation fails to pool them into one concept-level count.

**why_not_a_rename.** Generic keyword stuffing/adversarial ranking is known. The scientific question is narrower: the mother paper claims a **semantic** BM25 circuit; does its semantic abstraction extend to the saturation operator, or only to matching?

**D0.** MS MARCO/TREC passages plus WordNet/Wikidata/manual synonym sets; first establish synonym equivalence and equal relevance by human-readable cases.

**Mechanisms.** semantic matching + lexical-type-specific saturation; concept-normalized saturation; generic length/repetition artifact.

**Hard kill.** Synonym accumulation matches exact repetition after length/semantic controls, or existing neural-ranking work already localizes concept-level vs lexical-level saturation in this circuit.

---

# 10. Causal Retrieval Schedule

**Mother paper.** Lin et al., ACL 2026 Main, [*Retrieval Heads are Dynamic*](https://aclanthology.org/2026.acl-long.715/). It establishes that retrieval heads vary by generation timestep, active heads are not replaceable by static sets, and current hidden states can predict **future** retrieval-head patterns. The last result is presented as evidence suggestive of internal planning.

**Mother solved.** Future retrieval schedules are predictable from present hidden state; active retrieval heads are causally important at their timestep.

**New question.** Is the predictive hidden-state signal itself a **causal retrieval plan**, or merely a correlate of a future computation already determined elsewhere?

**Decisive design.** Use multi-hop QA with matched items where the same first hop admits two controlled second-hop destinations. At a pre-retrieval timestep, patch/steer the plan-predictive subspace from a donor requiring the alternative second hop while preserving current-token semantics. Measure both the future dynamic-head pattern and which supporting span is retrieved.

**Prediction.** If causal plan, intervention should retarget the later retrieval-head schedule and evidence destination coherently. If mere correlate, probe prediction changes but actual future heads/evidence do not.

**why_not_a_rename.** Mother Claim 3 is explicitly **Correlation**; Claim 2 ablates heads only when they are already active. The extension upgrades the strongest planning interpretation from prediction to **pre-activation causal control**.

**D0.** Mother’s Needle/multi-hop setup plus HotpotQA-style support pairs with controlled alternative second hops.

**Mechanisms.** causal schedule state; epiphenomenal forecast signal; shared upstream cause drives both hidden-state probe and later retrieval heads.

**Hard kill.** Any content-preserving edit of the predictive subspace fails to retarget future retrieval, or the mother/successor literature already performs pre-activation causal schedule manipulation.

---

## Reviewer-mode N0 summary

All 10 survive the following proposer-side adversarial requirements:

1. **Mother paper is real and scientifically central** to the extension; no “random paper as citation decoration.”
2. **Question changes the scientific object**: causal role, representational semantics, lifecycle, composition locus, implementation switching, or mechanism granularity.
3. **No extension is justified only by a new model, language, benchmark, or domain.**
4. Targeted searches through 2026-08-29 did not reveal an exact paper already answering the decisive contrast.
5. Existing repo F1–F9 families were treated as mother-inclusion attacks; #3/#5/#7 are explicitly high-risk and survive only under the narrow mechanism contracts above.
6. Every topic has a result that can kill it before a full mechanistic paper is built.

These are **not** formal independent sign-offs. Before smoke, another audit must verify primary-paper appendices/code where relevant and freeze D0.
