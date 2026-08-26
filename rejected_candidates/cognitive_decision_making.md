# Rejected Candidates — Cognitive / Decision-Making Phenomena

**Domain:** cognitive effects, judgment, choice, uncertainty, evidence accumulation, social decision-making.  
**Status:** active breadth-first scan.  
**Rule:** classic human effects are not assumed to transfer to modern LLMs. A candidate needs direct, modern open-weight behavioral evidence before mechanism work.

---

## Prior negative knowledge

This file records candidate families that looked natural but failed either because the behavior was weak/nonexistent on modern models, the mother question was already occupied, or the mechanism would not change the practical method.

### Generic authority / source-status bias

**Kill:** broad authority-bias and source-credibility framings are too easy to confound with factual prior, style, and context-memory conflict, and the surrounding literature is already dense. Do not revive by swapping profession/domain/source labels.

### Generic anchoring / certainty / risk / sunk-cost / outcome-bias families

**Kill:** classic-bias-to-LLM transfer is no longer accepted as a premise. Earlier search rounds repeatedly overestimated how strongly modern models inherit textbook cognitive biases. A title saying an LLM shows a bias is insufficient; require model-level effect sizes on current open weights.

---

## 2026-08-27 phenomenon-first round: candidates inspected and killed

### A. Generic false-belief / Theory-of-Mind failure

**Natural phenomenon:** People can represent another agent's belief separately from the actual state of the world.

**Why it looked promising:** Modern behavioral work still shows large failure rates on hard false-belief benchmarks. ACL 2026 PICTURE reports vanilla false-belief accuracy of 58.8/54.7/41.5 on BigToM/ToMi/FANToM for Llama-3.1-8B-Instruct and 61.3/62.3/28.7 for Qwen3-8B, so the phenomenon is certainly real on two open families.

**Kill evidence:** The mother question is already mechanism-dense. Recent work explicitly studies sparse ToM-sensitive parameters, causal belief-tracking mechanisms ('lookbacks'), and a 2026 mechanistic investigation in Qwen2.5-14B that separates mid-layer representation-vs-reality divergence heads from later answer-retrieval heads. A generic 'why do LLMs fail false belief?' project would collide directly with existing behavioral, training, and mechanistic narratives.

**Death code:** `MECHANISM_COLLISION`

**Resurrection condition:** Only with a new natural ToM phenomenon that is behaviorally distinct from classic false belief and not reducible to belief-state tracking / representation-reality divergence.

**References:** https://aclanthology.org/2026.acl-long.1674.pdf ; https://www.nature.com/articles/s44387-025-00031-9 ; https://arxiv.org/abs/2505.14685 ; https://digitalcommons.dartmouth.edu/cognitive-science_senior_theses/11/

### B. Generic working-memory interference / recency

**Natural phenomenon:** Multiple active memories interfere, with retrieval biased by recency and competing items.

**Why it looked promising:** `In-context superposition: human-like working memory interference in large language models` (2026) reports load-dependent working-memory limits and human-like recency/statistical interference in a diverse set of pretrained LLMs.

**Kill evidence:** The same paper already supplies the mechanistic story: recent items occupy overlapping internal representations ('in-context superposition'), separation across layers predicts retrieval success, and selectively suppressing competing information modestly improves performance. This is essentially the phenomenon → mechanism → intervention arc we would otherwise want to discover.

**Death code:** `MECHANISM_COLLISION`

**Resurrection condition:** A different memory phenomenon whose decisive contrast cannot be explained by overlapping-representation interference.

**Reference:** https://arxiv.org/abs/2604.09670

### C. Generic belief-revision inertia after minimal premise edits

**Natural phenomenon:** Rational belief revision should change conclusions when decisive evidence changes while preserving unrelated beliefs.

**Why it looked promising:** DeltaLogic reports Qwen3-1.7B initial accuracy 0.667 but revision accuracy 0.467 with 0.600 inertia, and Qwen3-4B 0.650 initial / 0.450 revision / 0.600 inertia. This is a visible effect, not a 2–5 pp difference.

**Why it is not promoted yet:** Current strong evidence for the exact minimal-edit inertia pattern is concentrated in Qwen3 plus Phi-4-mini; it does not yet satisfy our new 'at least two relevant modern open model families' evidence preference. The broader ICLR 2026 AGM-style belief-revision benchmark does replicate preservation/inclusion failures on Llama-3.3-70B and Qwen2.5-72B, but that is a related rather than identical operationalization. Treating them as the same phenomenon would repeat the broad→strict extrapolation mistake from the decoy project.

**Death code:** `INSUFFICIENT_EXACT_CROSS_FAMILY_EVIDENCE`

**Resurrection condition:** Replicate the minimal-edit inertia contrast on at least one additional modern open family (Gemma/Llama preferred) with deterministic constrained scoring before candidate registration.

**References:** https://arxiv.org/abs/2604.02733 ; https://openreview.net/pdf/0cf99120b6e1d209b18452f9db476edca54678e0.pdf

### D. Causal-ladder degradation (observation → intervention → counterfactual)

**Natural phenomenon:** Pearl's causal hierarchy distinguishes seeing, doing, and imagining a contrary intervention; competence at a lower rung does not logically entail competence at a higher one.

**Why it looked excellent behaviorally:** ACL 2026 Main METER reports a large monotonic drop on modern open models. For example, Qwen3-8B is about 86.3% on causal discovery, 64.5% on intervention, and 51.4% on counterfactual reasoning; Qwen3-14B about 88.0/67.5/52.1; Llama-3.3-70B about 87.2/78.2/62.1. This is exactly the kind of large, cross-family natural phenomenon we now require.

**Kill evidence:** Unfortunately METER itself already goes well beyond benchmarking. It performs internal information-flow tracing and attention masking, identifies context-utilization / evidence-flow failure modes, and demonstrates a lightweight evidence-grounding intervention that improves Counterfactual performance by about 4.8 points. The exact phenomenon → internal flow → intervention narrative therefore has substantial prior occupancy. A new generic mechanistic paper on the same rung gap would be a follow-up, not a fresh mother question.

**Death code:** `MECHANISM_COLLISION`

**Nearest-neighbor warning:** Do not revive by renaming the three rungs, swapping SCM domains, or doing another layer/head localization of evidence use.

**Resurrection condition:** A new causal phenomenon with a decisive behavioral contrast not explained by METER's context-faithfulness/evidence-flow account, ideally with different predictions for multiple mechanisms and a different repair.

**Reference:** https://aclanthology.org/2026.acl-long.1668/

---

# Current lessons

1. Naturalness alone is not enough; classic cognitive phenomena still require modern open-model evidence.
2. Do not merge nearby operationalizations just to manufacture cross-family support.
3. A beautiful behavioral effect is unusable if a recent paper has already completed the same mechanistic arc.
4. The best remaining cognitive candidates are formal/normative phenomena with exact scorers (Bayesian updating, causal intervention/counterfactual structure), not vague named biases.
