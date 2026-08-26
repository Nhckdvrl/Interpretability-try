# Rejected Candidates — Cognitive / Logical Reasoning Phenomena

**Domain:** natural reasoning phenomena from cognitive science and formal reasoning where surface content, order, framing, or background belief changes judgments despite invariant logical structure.  
**Search status:** active scan, 2026-08-26.

## Domain goal

The attractive shape in this domain is:

```text
same underlying logical problem
+ one psychologically meaningful manipulation
→ large, stable behavioral change
→ competing internal explanations
→ selective causal intervention
→ mechanism-specific repair
```

The main danger is that many classic reasoning biases have already received direct mechanistic follow-up, or no longer survive in modern models.

---

# 1. Generic belief bias in syllogistic reasoning

**Natural question:** Why does a model reject a logically valid argument when its conclusion conflicts with commonsense belief, or accept an invalid argument because its conclusion sounds believable?

**Why it initially looked good:**

- classic, immediately understandable human reasoning phenomenon;
- public syllogism datasets exist;
- very clean `logical validity × believability` factorial design;
- natural competing explanations: logic computation failure vs world-knowledge contamination vs late arbitration.

**Kill evidence:**

This is already a direct mechanistic result. `Reasoning Circuits in Language Models: A Mechanistic Interpretation of Syllogistic Inference` (Findings ACL 2025) discovers a sufficient and necessary content-independent syllogistic circuit based on middle-term suppression, then explicitly studies belief bias and finds contamination from additional attention heads encoding commonsense/contextual knowledge. The paper also tests transfer across syllogistic schemes and model families.  
https://aclanthology.org/2025.findings-acl.525/

This covers essentially the same decisive contrast we would want: content-independent logical computation vs world-knowledge interference.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** Do not revive as “logic vs common sense”, “believable vs unbelievable conclusion”, or “world knowledge contaminates deduction” by swapping datasets/languages/models.

**Resurrection condition:** A different reasoning paradigm must exhibit a qualitatively different behavioral dissociation not explainable as another instantiation of the already-localized syllogistic content-effect circuit.

---

# 2. Generic content effects / representativeness / conjunction fallacy

**Natural question:** Why can a vivid, representative description make a model prefer an intuitively plausible but probabilistically impossible answer?

**Why it initially looked good:**

- classic Linda-style conjunction fallacy is easy to explain;
- ReHeAT reports representativeness-heuristic behavior and cases where models possess relevant knowledge but still reason incorrectly;
- a clean heuristic-vs-probability mechanism story appears possible.

**Kill evidence:**

The natural behavior is not stable enough across modern model generations to support a strong G0 without carefully selecting models/settings.

- Earlier work reports representativeness effects across several LLMs: `Will the Real Linda Please Stand up...to Large Language Models?`  
  https://arxiv.org/abs/2404.01461
- However, later evaluations find GPT-4 already near-perfect on classic Linda problems, and 2026 work reports GPT-5 far fewer conjunction fallacies than humans.  
  https://www.nature.com/articles/s44271-024-00091-8  
  https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2026.1782184/full
- A 2026 Scientific Reports paper also goes beyond behavior to analyze internal representation geometry of conjunction-fallacy and order effects across open-weight models.  
  https://www.nature.com/articles/s41598-026-65824-7

Thus the generic “why do LLMs commit the conjunction fallacy / representativeness heuristic?” narrative is both behaviorally model-dependent and increasingly mechanistically occupied.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Linda variants, stereotype-vs-base-rate variants, and synthetic conjunction problems are not separate topics unless a stable modern-model phenomenon with a new decisive contrast is established first.

**Resurrection condition:** A modern open-model family shows a large, reproducible failure under a controlled setting where the model demonstrably computes the relevant probabilities correctly elsewhere but selectively ignores them under one natural manipulation.

---

# 3. Moses / semantic illusion as a modern-LLM mechanism topic

**Natural question:** Why does a system answer the intended question while failing to notice that a semantically related entity in the question is wrong? Example: “How many animals did Moses take on the Ark?”

**Why it initially looked good:**

- one of the cleanest classic semantic illusions in cognitive psychology;
- human literature already offers competing explanations such as incomplete encoding, impoverished retrieval, and partial matching;
- these explanations map naturally onto representation / retrieval / matching interventions in LMs.

**Kill evidence:**

The phenomenon does not remain a robust modern-model failure. Earlier GPT models increasingly displayed human-like semantic illusions as scale increased, but the same study reports that the effect **disappeared in ChatGPT**, with ChatGPT-3.5/4 reliably avoiding the traps.  
https://www.nature.com/articles/s43588-023-00527-x

The study's source data show GPT-3-davinci-003 falling for semantic illusions at high rates, but later ChatGPT systems behave qualitatively differently. Using weak/old checkpoints to recover the illusion would violate the repository’s no-resuscitation rule.

**Death code:** `NO_NATURAL_BEHAVIOR`

**Nearest-neighbor warning:** Armstrong illusion, Mega-Moses, “bury the survivors”, and other semantic-illusion variants are the same family unless a strong failure is first demonstrated on current open models.

**Resurrection condition:** New evidence shows a stable semantic-illusion failure on current capable open models under an ordinary, non-adversarial prompt format.

---

# 4. Generic premise-order sensitivity as “order bias”

**Natural question:** Why can merely reordering logically equivalent premises change an LLM’s reasoning answer?

**Why it initially looked good:**

- very surprising external phenomenon: ICML 2024 reports accuracy drops over 30% although logical content is unchanged;
- ICLR 2026 further reports that reversing premise order can *eliminate* many human-like logical fallacies;
- exact permutations create ideal matched pairs for causal analysis.

**Why the generic version is rejected:**

The broad `order bias` narrative and its obvious repair space are now crowded:

- ICML 2024 established large premise-order effects across deductive and mathematical reasoning.  
  https://proceedings.mlr.press/v235/chen24i.html
- EMNLP 2025 proposed order-centric augmentation specifically to make reasoning invariant to logically equivalent reordering.  
  https://aclanthology.org/2025.emnlp-main.1382/
- ACL 2026 Main proposed DGAO, an RL objective explicitly optimizing both correctness and order stability across RAG, math, and classification.  
  https://aclanthology.org/2026.acl-long.219/

A generic mechanistic paper saying “order changes hidden states, so we find order-sensitive heads and steer them” would not naturally own the method story.

**Death code:** `METHOD_COLLISION`

**Nearest-neighbor warning:** Context order, premise order, option order, retrieval chunk order, and few-shot demonstration order should not be treated as separate novelty claims merely by changing the element being permuted.

**Resurrection condition:** A narrower *counterintuitive order effect* whose mechanism implies a repair qualitatively different from generic permutation augmentation / order-stability RL. The ICLR 2026 observation that **premise reversal specifically blocks structured fallacies** remains worth separate audit and is not declared dead here.

---

# 5. Generic deontic / normative reasoning difficulty

**Natural question:** Why do models struggle to apply obligations, permissions, prohibitions, statutes, and policies consistently?

**Why it initially looked good:**

- highly natural and consequential;
- explicit rules provide deterministic gold;
- errors can be decomposed into rule retrieval, interpretation, chaining, and decision.

**Kill evidence:**

The broad domain has rapidly become benchmark- and method-heavy:

- `Normative Reasoning in Large Language Models` already compares normative and epistemic modals across formal patterns and human-like cognitive factors.  
  https://aclanthology.org/2025.blackboxnlp-1.17/
- `DeonticBench` (2026) provides 6,232 tasks from tax, airline policy, immigration, and housing law, including executable Prolog references.  
  https://arxiv.org/abs/2604.04443
- `DAR: Deontic Reasoning with Agentic Harnesses` (2026) studies tool/harness methods for difficult DeonticBench subsets.  
  https://arxiv.org/abs/2606.05009

“Why deontic reasoning is hard” is therefore much too broad and risks becoming another rule-retrieval / long-context paper.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Legal rules, company policy, tax rules, obligations, permissions, and prohibitions are one broad family unless a precise cognitive contrast is isolated.

**Resurrection condition:** A compact, logically matched behavioral phenomenon where *normative framing itself* changes reasoning despite invariant formal structure. The Wason deontic-vs-descriptive facilitation effect satisfies this condition and remains under audit rather than being rejected.

---

# Domain survivors under audit

Two narrower questions currently survive the paper audit:

1. **Deontic facilitation in the Wason Selection Task:** why does the same conditional logic become easier when framed as a norm/permission/obligation rather than a descriptive rule? EACL 2026 establishes the behavior and releases the dataset, but the current search has not found a causal-mechanistic follow-up.  
   https://aclanthology.org/2026.eacl-short.42/  
   https://github.com/kmineshima/NeuBAROCO

2. **Fallacy blocking by premise reversal:** ICLR 2026 finds that reversing premises can turn many logically wrong outputs into correct ones, including in strong models. The generic order-bias topic is crowded, but this specific “why does reversal repair a structured fallacy?” dissociation may still support a different mechanism question.  
   https://iclr.cc/virtual/2026/poster/10011847

Neither survivor is promoted to a final candidate until its mechanism collision and method closure are audited further.