# Next Agent Prompt — 2026-09-01

继续 GitHub 仓库 `Nhckdvrl/Interpretability-try` 的 ACL / EMNLP / NAACL 风格 **LLM mechanistic interpretability 找题工作**。

这是 direct continuation。**当前 authoritative PASS register 是 4/5。不要从旧的 2/5、3/5、短暂 5/5 状态继续。**

## 一、第一步必须完整读取最新 authority

按顺序读：

1. `README.md`
2. `phenomenon_miner/FINDING_RULES.md` — v2.1 唯一选题协议
3. `phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`
4. `phenomenon_miner/CURRENT_SEARCH_FLOW_2026-09-01.md`
5. `rejected_candidates/CANONICAL_FAILURE_INDEX_2026-09-01.md`
6. `phenomenon_miner/HARD_REAUDIT_REGISTER_2026-09-01.md`
7. `active/034_prospective_memory_retrieval_architecture/README.md`
8. `active/035_shared_dynamic_context_update/README.md`
9. `active/036_metaphor_processing_route_selection/README.md`
10. `active/038_unresolved_reference_representation_architecture/README.md`
11. `active/038_unresolved_reference_representation_architecture/HARD_REAUDIT_2026-09-01.md`
12. `active/040_numerical_identity_vs_qualitative_sameness/README.md`
13. `phenomenon_miner/PAPER_EXPANSION_REFERENCE_2026-09-01.md`
14. 本文件

## 二、当前 authoritative state

```yaml
CURRENT_FRESH_PASS_REGISTER: 4
CURRENT_FRESH_ACTIVE_TOPICS: 4
CURRENT_HARD_AUDIT_TOPICS: 1
target: 5
remaining_needed: 1
registered:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 038_unresolved_reference_representation_architecture
  - 040_numerical_identity_vs_qualitative_sameness
hard_audit_not_registered:
  - 036_metaphor_processing_route_selection
archived_after_registration:
  - 037_generic_generalization_licensing
  - 039_same_kind_vs_go_together_semantic_relation
```

## 三、034 / 035 / 038

Keep frozen unless a genuinely new fatal collision is found.

- 034: future intention retrieval — strategic monitoring vs cue-triggered spontaneous retrieval vs dynamic switching.
- 035: shared dynamic local discourse context across anaphora and presupposition.
- 038: still-unresolved reference — multiple candidate referents vs underspecified state vs premature commitment.

Do not rewrite headlines or perform routine re-audits.

## 四、040 — NEW PASS, do not collapse it into generic entity tracking

Status: **PASS-REGISTER / GPU AUTHORIZED**.

Frozen question:

> **If two things are exactly alike, does an LLM still know whether they are literally the same individual object or merely two different objects of the same kind?**

Scientific distinction:

```text
numerical identity
!=
qualitative/type sameness
```

Critical natural cross-cases:

```text
same individual despite substantial state/property change
vs
different individuals despite same type / near-identical qualities
```

### Important strongest neighbors

1. Solomon et al. human event-comprehension work: natural token × state-change substrate.
2. Dranseika et al. Cognition 2023: explicit numerical-vs-qualitative sameness distinction, including lexical separation.
3. Davis & Altmann Cognition 2021: LSTM/RNN hidden representations already distinguish same token vs different token of same type in event contexts.
4. ICLR 2024 / EMNLP 2024 / ACL 2026 binding work: mechanisms for already individuated entities.
5. ICML 2026 entity tracking: PUT/MOVE/REMOVE mechanism; same-label duplicate stress test exposes fragile global removal behavior.

### Why RNN does NOT automatically kill 040

Do not claim novelty merely from moving RNN -> Transformer. That would be insufficient.

040 survives because its required object-level delta is broader:

> **an abstract, reusable numerical-identity state in modern LLMs, separable from qualitative/type similarity and causally controlling token-specific history inheritance.**

Davis–Altmann is a strong precursor and hard baseline. If 040 only reproduces `the onion` vs `another onion` event sensitivity, kill it.

### Frozen first causal contract

Identity intervention must:

```text
change token-specific HistoryTransferLogit
while preserving shared TypeKnowledgeLogit
```

Required controls include:

- `the` vs `another` lexical cue;
- noun repetition;
- recency;
- semantic/type similarity;
- generic coreference/binding;
- random/shuffled directions;
- held-out surface cue family.

### Architecture generalization

After primary Llama/Qwen AR-Transformer evidence is secure, optional secondary generalization can test:

- diffusion LM: LLaDA / Dream-family;
- linear/recurrent-like LM: Mamba / RWKV-family.

This asks whether numerical identity is architecture-general or differently implemented. **Architecture comparison is not the novelty claim and cannot rescue a failed primary result.**

## 五、完整 ACL/EMNLP paper 不能停在“现象 + latent direction”

必须读：`phenomenon_miner/PAPER_EXPANSION_REFERENCE_2026-09-01.md`。

从强论文中学到的真实扩展模式：

### ACL 2025 Outstanding — Llama See, Llama Do

```text
broad phenomenon
→ semantic modulation
→ head discovery
→ causal ablation
→ mitigation
```

### NAACL 2025 — Racing Thoughts

```text
recurring failure
→ one algorithmic hypothesis
→ correlational + causal evidence
→ inference-time intervention
```

### ACL 2026 — Do LLMs Know Tool Irrelevance?

```text
natural factor dissociation
→ competing pathways
→ relative pathway strength explains behavior
→ rebalancing intervention
→ verify generic capability is preserved
```

### EMNLP 2025 Outstanding — filler-gap shared structure

```text
external theory
→ causal shared representation
→ cross-construction transfer
→ discover previously overlooked moderators
→ feed mechanism evidence back into linguistic theory
```

### ICML 2026 — entity tracking

```text
behavior
→ mechanism
→ mechanism predicts a new failure missing from original evaluation
→ targeted behavior confirms prediction
→ mechanistic partial fix
```

### Therefore 040's evidence ladder

Do not guess the circuit in advance. Conditional on success:

```text
1. identity double dissociation
2. cross-surface / cross-domain abstraction
3. causal history-transfer specificity while preserving type knowledge
4. mechanism-derived NEW falsifiable failure prediction
5. targeted behavioral verification
6. optional mitigation
7. optional dLLM / linear-LM architecture generalization
```

Only do stages 4–7 if earlier evidence earns them. Do not invent downstream experiments just to make the paper long.

## 六、036

Status: **HARD AUDIT / GPU PAUSED / NOT REGISTERED**.

Question survives:

> conventionality vs aptness — which selects comparison vs categorization in metaphor comprehension?

But former metaphor↔simile causal statistic is underidentified. Re-enter only if a clean two-signature route-identification contract is frozen, with at least one diagnostic not defined by grammatical form.

Do not force-repair 036 merely because one slot remains.

## 七、failure-library discipline — mandatory before new search

Every new serious candidate:

```text
one-sentence scientific object
→ generate 5–10 semantic aliases
→ search CANONICAL_FAILURE_INDEX
→ search rejected_candidates + archive
→ strongest-neighbor BODY/appendix search
→ only then HARD AUDIT
```

Do not recreate killed topics under new names.

Important recent dead clusters include:

- taxonomic vs thematic relation (former 039);
- ownership vs possession;
- authority vs expertise;
- role vs current occupant;
- canonical function vs ad-hoc affordance;
- habitual vs episodic;
- cardinal vs ordinal;
- use vs mention;
- evidential source types;
- Gettier knowledge vs JTB;
- de re vs de dicto;
- desire vs intention;
- relative vs absolute adjectives;
- tool relevance vs availability;
- tool necessity vs usefulness;
- self-authorship vs user source;
- self-consistency/high agreement vs real confidence / false consensus;
- metonymy;
- whole-part vs taxonomy;
- generic same-label entity tracking.

The canonical index contains aliases and warnings. Every serious death must still get an individual rejection record.

## 八、next search task

We need **one** more genuine PASS, but do not search only one candidate.

Continue high-mortality Hamdi-style / Route-C / strong-mother search:

```text
simple natural question
→ semantic dedupe
→ deepest N0/N1/N2 object-ownership attack
→ real deterministic substrate
→ confound identifiability
→ one clear causal-use question
→ PASS only if all survive
```

Do not reinstate the obsolete over-strict rule that a Route-C candidate must already have an exact modern-open published phenotype. A real deterministic human/scientific axis can be enough to justify a frozen cheap S0, as 040 demonstrates.

But also do not confuse `no paper found` with PASS: older RNN/BERT/ELMo work and hidden experiment-level object ownership still count.

Candidate families currently only HARD LEADS, not registered:

- focus vs background / information structure;
- collective vs distributive plurality (currently unattractive due to existing plural-bias work and overlap with 038-style unresolved architecture).

Broad-search beyond them. Do not anchor.

## 九、final discipline

> **Current honest register is 4/5: 034, 035, 038, 040. 040 is a simple natural identity question with a serious RNN precursor and strong modern entity-tracking neighbors, but its novelty is the abstract causal numerical-identity object, not the backbone change. One slot remains. Search broadly, dedupe aggressively, and only register a fifth topic that survives the same depth of audit.**
