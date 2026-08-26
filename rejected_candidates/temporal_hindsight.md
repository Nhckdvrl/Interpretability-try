# Rejected Candidates — Temporal Reasoning / Hindsight Leakage

**Domain:** reasoning and decision-making under historical time constraints, including outcome bias, temporal knowledge, and future-information leakage.  
**Search date:** 2026-08-26.

## Domain goal

The scientifically attractive failure is not merely “models know outdated facts.” It is a temporal-causality constraint:

```text
make a judgment using only information available at time t
future outcome information is not legally available to that judgment
yet later-acquired knowledge may leak backward into the answer
```

This permits a clean distinction between temporal-scope representation, historical knowledge retrieval, future-outcome memory, and late decision arbitration.

---

# 1. Generic temporal knowledge / outdated facts

**Natural question:** Why do LLMs confuse which fact was true at which time?

**Why it initially looked good:**

- temporal validity is a real property of world knowledge;
- presidents, teams, jobs, prices, policies, etc. change over time;
- temporal scopes provide structured gold labels.

**Kill evidence:**

This broad problem is mature and heavily method-driven:

- `Time-Aware Language Models as Temporal Knowledge Bases` already studies temporally scoped facts and timestamp-conditioned training.  
  https://arxiv.org/abs/2106.15110
- AAAI 2024 `History Matters: Temporal Knowledge Editing in Large Language Model` explicitly argues that updated models should retain historical knowledge and introduces temporal knowledge editing benchmarks/methods.  
  https://arxiv.org/abs/2312.05497
- Findings ACL 2025 and subsequent temporal-KG work provide dedicated temporal reasoning benchmarks and structured temporal encoders/reasoning frameworks.  
  https://aclanthology.org/2025.findings-acl.378/

“Where is temporal knowledge stored?” or “why does the model answer an old fact incorrectly?” is much too broad.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** outdated knowledge, temporal QA, old-vs-new fact representation, president-at-year-X, temporal editing, and chronology confusion are one crowded family.

**Resurrection condition:** a specific behavioral violation where the relevant historical fact is demonstrably available but a different temporally scoped computation overrides it.

---

# 2. Generic human-style outcome bias

**Natural question:** Why does knowing how a risky decision turned out change how an LLM judges the quality of the original decision, even though the outcome was unavailable when the decision was made?

**Why it initially looked good:**

- classic real-world judgment bias;
- easy matched design: identical decision process, random good/bad outcome appended afterward;
- current open-source LLM work reports outcome effects in legal judgment.

**Why it is rejected as the generic topic:**

Outcome bias is already a famous, expected cognitive-bias replication target, and broad cognitive-bias suites now evaluate dozens of such biases across many LLMs. Without a sharper model-specific dissociation, “LLMs also judge lucky outcomes more favorably” has low surprise and weak mechanistic specificity.  
https://aclanthology.org/2025.nlp4dh-1.50/

A 2026 open-model legal replication further establishes the behavior across current model families, making another broad behavior+mechanism paper vulnerable to the critique that it merely mechanizes an expected salience effect.  
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6227899

**Death code:** `LOW_SURPRISE`

**Nearest-neighbor warning:** good-outcome vs bad-outcome blame, legal culpability after harm, lucky-vs-unlucky decision evaluation, and ex-post performance judgment are one family.

**Resurrection condition:** a temporal information-control manipulation showing the model explicitly represents what was knowable ex ante yet later outcome knowledge causally rewrites that historical state.

---

# Survivor under audit: Parametric hindsight / future-information leakage into historical decisions

**Natural question:** When asked to make a decision *as of a historical date*, why does a modern LLM leak knowledge of what happened afterward into the decision—even though that future information should be unavailable at the requested time?

**Behavior foundation:** `HindsightBench` (2026-07, revised 2026-08) provides a preregistered black-box audit with a 258-node vintage-correct macroeconomic panel, four date-manipulation arms (revealed / date-only / masked / historically transplanted), outcome/date memory probes, frozen transcripts, audit rows, and one-command regeneration.  
https://arxiv.org/abs/2607.18867  
https://github.com/Khaozhe/hindsightbench

The behavioral findings are unusually strong and surprising:

- the date-trigger reflex tracks **model generation, not scale**;
- it is absent across tested 2024 open-weight models from 1B through 70B but present in every tested 2026-generation model where identifiable;
- within one vendor lineage it switches on from Qwen3 to Qwen3.6 at roughly fixed active parameter scale;
- effective knowledge cutoffs vary substantially across vendors and can precede vendor-reported cutoff dates.

The paper explicitly states that the behavioral audit does **not identify what installs the reflex**.

**Competing mechanisms:**

```text
A. no historical-scope state:
   the model retrieves facts globally and never constructs a causal “available by time t” gate;

B. historical state exists but future memory wins arbitration:
   time scope is represented correctly, yet later parametric knowledge dominates the decision pathway;

C. future knowledge contaminates the historical representation itself:
   once the date/entity is recognized, future outcomes rewrite the latent state used to represent the past;

D. computation is historically correct but late readout leaks future outcome tokens/associations.
```

These make different causal predictions under activation interchange between revealed/masked/transplanted arms.

**Method closure:**

- A → learn/insert an explicit temporal availability gate or time-scoped retrieval objective;
- B → temporal arbitration/routing intervention suppressing post-t evidence only when an as-of constraint is active;
- C → representation-preserving temporal editing / orthogonalization between historical state and future update;
- D → targeted late readout suppression rather than retraining knowledge storage.

**Surprise potential:** very high. A particularly strong result would be that the model *correctly encodes the historical cutoff and the period’s available evidence, but a later learned future-outcome pathway causally overwrites the answer only after the historical state has been constructed*. That would turn “training data contamination” into a specific computational hindsight mechanism.

**Main risks:**

- behavior is currently demonstrated on a macro/financial carrier task; need generalization to at least one second natural historical-decision domain without inventing a synthetic benchmark;
- current 2026 open models that exhibit the reflex and are locally tractable must be identified;
- must distinguish this from generic context-vs-parametric-memory conflict: the key novelty is *time-legality of information*, not contradiction between two simultaneous sources.

**Status:** `PRE-CANDIDATE / HIGH-PRIORITY SURVIVOR`.