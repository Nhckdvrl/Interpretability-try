# Hamdi-Style Topic Search — Current Handoff

Date: 2026-09-01  
Status: **AUTHORITATIVE CURRENT STATE — FRESH REGISTER 4/5 AFTER 039 DEREGISTRATION**

```yaml
CURRENT_FRESH_PASS_REGISTER: 4
CURRENT_FRESH_ACTIVE_TOPICS: 4
fresh_register_target: 5
fresh_register_status: OPEN_AFTER_039_DEREGISTRATION
fresh_target: LLM mechanistic interpretability only
required_protocol: PAPER-SCALE v2.1
registered_projects:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 036_metaphor_processing_route_selection
  - 038_unresolved_reference_representation_architecture
archived_after_registration:
  - 037_generic_generalization_licensing
  - 039_same_kind_vs_go_together_semantic_relation
current_search_style: simplicity-first / Route C legal / strongest-neighbor-first
current_task: complete hard re-audit of 036 and 038, then search for one genuinely novel replacement without protecting count
```

## Mandatory reads

Read first:

1. root [`README.md`](../README.md)
2. [`FINDING_RULES.md`](FINDING_RULES.md) — **v2.1 authoritative protocol; strict ≠ complicated**
3. this handoff
4. registered project READMEs:
   - [`034`](../active/034_prospective_memory_retrieval_architecture/README.md)
   - [`035`](../active/035_shared_dynamic_context_update/README.md)
   - [`036`](../active/036_metaphor_processing_route_selection/README.md)
   - [`038`](../active/038_unresolved_reference_representation_architecture/README.md)
5. [`NEXT_AGENT_PROMPT_2026-09-01.md`](NEXT_AGENT_PROMPT_2026-09-01.md)

037 and 039 are archived. A stale historical reference is never authorization.

---

## Current register

### 034 — Prospective Memory Retrieval Architecture

**PASS-REGISTER / GPU AUTHORIZED / FROZEN.**

> When an agent must remember a future intention while continuing other work, is retrieval supported by strategic monitoring, cue-triggered spontaneous retrieval, or dynamic switching?

No headline edits unless a new fatal collision appears.

### 035 — Shared Dynamic Context Update Across Discourse Phenomena

**PASS-REGISTER / GPU AUTHORIZED / FROZEN.**

> Do anaphora accessibility and presupposition projection reuse a shared dynamically updated local discourse context, or rely on separate/static computations?

No narrowing back to one discourse phenomenon.

### 036 — Metaphor Processing Route Selection

**PASS-REGISTER / GPU AUTHORIZED — HARD RE-AUDIT ACTIVE.**

> What selects comparison vs categorization in metaphor comprehension: conventionality, aptness, or no discrete route switch?

Prior registration rests on the independent Career-of-Metaphor vs aptness debate and the Jones–Estes human 2×2. It remains active, but the present audit must specifically test whether 2025–2026 LLM metaphor work already owns the `conventionality/aptness -> comparison/categorization route` interpretation rather than merely adjacent metaphor competence/representation.

### 038 — Unresolved Reference Representation Architecture

**PASS-REGISTER / GPU AUTHORIZED — HARD RE-AUDIT ACTIVE.**

> When language does not yet identify one unique referent, does the model keep several possibilities alive, leave the reference unresolved, or prematurely pick one?

Prior registration rests on AmbiCoref + Correct-Detect + It Depends and independent ambiguity-representation theories. The present audit must search specifically for modern open-LM work on simultaneous candidate activation, semantic underspecification, early commitment, coreference uncertainty, or causal reference representations.

---

## Deregistered 037 — do not revive

Former 037 generic generalization licensing is **KILL-NOVELTY / ARCHIVED**.

Fatal collision: Hu, van Paridon & Lupyan (2026), `Failures and Successes to Learn a Core Conceptual Distinction from the Statistics of Language` (`arXiv:2607.04523`) directly tests the principled-vs-statistical generic-property distinction while controlling prevalence/cue validity. Causal MI would be too close to behavior/factorization -> mechanism under N2.

Archive: [`archive/037_generic_generalization_licensing/`](../archive/037_generic_generalization_licensing/)

---

## Deregistered 039 — canonical new N2 lesson

Former 039 asked:

> Does an LLM distinguish **same kind / taxonomic similarity** from **go together / thematic relatedness** as a reusable, causally used relation type?

The naturalness and data were real, but a deeper strongest-neighbor search found the object was already occupied:

1. 2026 `Disentangling Similarity and Relatedness in Topic Models` explicitly factorizes taxonomic similarity vs thematic relatedness, uses the same Landrigan–Mirman TxThmNorms 659-pair human data, evaluates language-model embedding representations on both axes, and obtains both-axis ratings from modern LLMs including Qwen.
2. CoNLL 2025 `Human-likeness of LLMs in the Mental Lexicon` studies Llama-3.1 semantic-relatedness representations and explicitly includes taxonomic/thematic relations.
3. 2026 cross-cultural-surrogate work directly runs LLaMA/Qwen on taxonomic–thematic forced choice and explicitly analyzes taxonomic versus thematic reasoning in LLM explanations.

Therefore the proposed `hidden relation direction -> steering / cross-task causal transfer` was primarily **stronger MI on an already-owned scientific object**, which fails v2.1 N2.

Detailed record: [`rejected_candidates/taxonomic_vs_thematic_relation_type_n2_collision_2026-09-01.md`](../rejected_candidates/taxonomic_vs_thematic_relation_type_n2_collision_2026-09-01.md)

Archive: [`archive/039_same_kind_vs_go_together_semantic_relation/`](../archive/039_same_kind_vs_go_together_semantic_relation/)

### New canonical lesson from 039

Do not infer novelty from a neighbor's headline. A paper whose headline is cultural fidelity, topic modeling, or mental lexicon can still **own the scientific object inside its experiments and interpretation**.

Hard N2 question must be:

> If we remove the words `activation`, `steering`, `patching`, `SAE`, and `causal`, what scientific object remains that the strongest prior did not already study?

If the answer is “none,” KILL.

---

## v2.1 simplicity rule

Legal Route C:

```text
simple natural object / robust ordinary phenomenon
→ benchmark-removal + normal-scope
→ strongest-neighbor N0/N1/N2
→ auditable existing axis / substrate
→ obvious confounds
→ one minimal causal-use question
→ richer mechanism only if the data earn it
```

Still forbidden:

- behavior lottery on GPU;
- benchmark construct becoming the headline;
- `prior behavior/representation paper -> our activation patching` as the entire N2 delta;
- probe-only paper whose final claim is “feature decodable”;
- changing the scientific object after null results;
- protecting a 5/5 count from fatal evidence.

---

## Serious deaths from the latest simplicity-first search

Written to `rejected_candidates/`:

- use vs mention / asserted vs quoted;
- speaker commitment / factivity;
- typicality vs frequency/commonness;
- action precondition vs effect;
- hard constraint vs soft preference;
- cause vs enabling condition;
- epistemic vs deontic modality;
- final goal vs subgoal status;
- concrete vs abstract representation;
- causal vs correlational relation;
- intentional lie vs honest error;
- **taxonomic vs thematic relation type (former 039)**.

Do not revive by changing model, benchmark, language, or MI method.

---

## Current task

The honest state is **4/5**, not 5/5.

1. Finish a fresh direct-collision audit of 036 and 038.
2. Do a lightweight fatal-collision scan of frozen 034/035 only; do not rewrite their headlines absent new evidence.
3. Only after the surviving register is clean, resume broad Hamdi-style search for **one** replacement.
4. A replacement must survive the exact 039 lesson: strongest neighbors are read for internal object ownership, not merely titles/abstract headlines.
5. Do not register a new number merely because the count is 4.

## One-line instruction

> **Current register is 4/5. 039 was correctly killed after deeper N2 audit. Audit first, replacement second; simple is good, method-only novelty is not.**
