# Final Convergence Rejections — Hamdi-Style Search (2026-08-31)

**Status:** authoritative late-session negative memory.  
**Purpose:** supersede stale `survivor` / `under audit` language left in older domain logs after the repository adopted the strict S0-first gate.

---

# 1. Fallacy Blocking by Premise Reversal — KILL-S0

**Natural question:** Why can reversing the order of logically equivalent premises make an LLM stop committing a structured logical fallacy?

**Why it looked good:**

- ICLR 2026 reports a striking intervention: reversing premise order blocks many ETR-predicted fallacies across a large panel of models;
- the manipulation is logically irrelevant, so the behavioral change looks mechanistically rich;
- the old `cognitive_logical_reasoning.md` therefore left this narrower version as `under audit` even after generic order bias was rejected.

**Kill evidence:**

Under the current S0 contract this is not registrable as a failure-mechanism topic. The ICLR 2026 mother uses PyETR to **programmatically generate 383 formally specified reasoning problems**. The fallacy-blocking phenotype is therefore established in a synthetic formal-reasoning protocol, not in a broad natural row-level population or ordinary everyday behavior. Current S0 explicitly forbids using a synthetic-only contrast as the existence substrate for a new failure mechanism.

This is a stricter adjudication than the older domain log, not a claim that the mother result is invalid. The result is interesting, but it does not satisfy this repository's current registration contract.

**Death code:** `NO_NATURAL_BEHAVIOR`

**Nearest-neighbor warning:** do not revive as `premise reversal repairs reasoning`, `order reversal blocks fallacies`, `non-commutative reasoning`, or by switching to another automatically generated logic grammar. Generic premise-order sensitivity is already crowded separately.

**Resurrection condition:** a large, ordinary, naturally sourced reasoning population with objective gold in which semantically equivalent premise-order reversals show a strong fallacy-blocking effect on at least two current analyzable open families, without selecting items after observing model errors.

**Reference:** ICLR 2026, *Theory-Grounded Evaluation of Human-Like Fallacy Patterns in LLM Reasoning*.

---

# 2. Stronger Reasoners Are More Fragile Off-Trajectory — KILL-N0

**Natural question:** Why can a model that reasons better on its own be more easily derailed by another reasoner's misleading partial trace?

**Why it looked good:**

- ICLR 2026 `Off-Trajectory Reasoning` evaluates 15 open-weight LLMs and reports the counterintuitive pattern that stronger benchmark reasoners are often more fragile under distraction;
- the same paper contrasts recoverability from bad traces with guidability by good traces;
- the phenomenon seems to invite a natural internal fork between trajectory commitment, error detection and collaborative update.

**Kill evidence:**

The mother already owns the scientific object. It introduces **off-trajectory reasoning**, explicitly defines Recoverability and Guidability as the key dimensions, documents stronger-model fragility, and studies post-training contributors including distillation teacher, RL and data selection. A new project whose headline is `why are stronger models more distractible?` followed by probing/patching would be a direct mother-behavior → mechanism follow-up, not a new title-level object under N0.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as reasoning competence vs distraction robustness, recoverability vs guidability, collaborator-trace susceptibility, or stronger-model trajectory lock-in merely by adding MI.

**Resurrection condition:** a different natural collaborative-reasoning phenomenon with a behavior not already defined by recoverability/guidability/off-trajectory reasoning and with an independent title-level scientific question.

**Reference:** ICLR 2026, *Off-Trajectory Reasoning: Can LLMs Collaborate on Reasoning Trajectories?*

---

# 3. Multi-Agent Interaction Expands Quality but Collapses Diversity — KILL-N0

**Natural question:** Why can adding more agents and communication make a group converge prematurely instead of exploring more ideas?

**Why it looked good:**

- Findings ACL 2026 reports a natural-looking collective paradox: stronger models, authority-driven groups, larger groups and denser communication can yield diminishing or reduced semantic diversity;
- the phenomenon invites possible internal questions about copying, shared search direction, conformity gates and loss of independent latent trajectories.

**Kill evidence:**

The mother paper already makes **diversity collapse through structural coupling** its central scientific object. It analyzes model-level, cognition-level and system-level causes, including authority structure, group size and communication topology, and concludes that collapse arises primarily from interaction structure rather than inherent model insufficiency. `Which internal state causes the convergence?` would therefore be mechanism localization for the mother's established object rather than a new scientific question.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as latent conformity, premature consensus, collaboration shrinks search space, communication-induced mode collapse, or authority suppresses diversity by changing the MI method.

**Resurrection condition:** a distinct collective behavior whose headline cannot be reduced to diversity collapse / structural coupling and whose causal predictions require a new internal object.

**Reference:** Findings ACL 2026, *Diversity Collapse in Multi-Agent LLM Systems: Structural Coupling and Collective Failure in Open-Ended Idea Generation*.

---

# 4. Can Generate a Linguistic Feature ≠ Robustly Understand It — DO NOT REGISTER

**Natural question:** Why can a model produce a linguistic construction correctly yet remain brittle when that same construction is used in an input it must understand?

**Why it looked good:**

- 2026 FLUKE reports that a model's ability to use a linguistic feature in generation does not correlate with robustness to that feature on downstream tasks;
- production and comprehension are conceptually distinct and could superficially suggest separate writer/reader mechanisms.

**Kill evidence:**

This proposal has two fatal problems under the current rules. First, the mother already reports the production–robustness dissociation as a headline behavioral result, so generic causal localization would be N0 mechanism follow-up. Second, the proposed narrative is a direct instance of the repository's explicitly forbidden `can/knows X but does not robustly use X` shape unless a genuinely new behavior is identified independently.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as production-vs-comprehension, can-generate-vs-can-handle, linguistic competence-vs-robustness, or reader-vs-writer merely because those words resemble the successful arbitrary-choice reader/writer decomposition. The scientific object must precede the mechanism analogy.

**Resurrection condition:** a new natural production/comprehension phenomenon with independent external gold and a title-level behavior not equivalent to FLUKE robustness or generic knowledge/use dissociation.

**Reference:** Findings EACL 2026, FLUKE robustness study.

---

## Final convergence lesson

Two attractive routes are now explicitly closed:

```text
counterintuitive mother result
→ immediately rename an internal component
→ call causal tracing a new topic
```

and

```text
Hamdi had a reader/writer decomposition
→ look for any task with an input/output distinction
→ force a reader/writer story
```

The correct use of Hamdi's example is stricter: a stable natural behavior or genuinely new external scientific axis must come first; the internal decomposition should be something the causal experiment discovers or adjudicates, not the reason the topic was invented.
