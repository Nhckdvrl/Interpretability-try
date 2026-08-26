# Rejected Candidates — Psycholinguistic Processing

**Domain:** garden-path parsing, good-enough comprehension, ambiguity/reanalysis, negation, linguistic conflict.  
**Search date:** 2026-08-27.

---

## 1. Garden-path / good-enough reanalysis

**Natural question:** Why can an initially plausible interpretation persist even after later words show that the sentence must be reanalyzed?

**Why it initially looked good:** Garden-path effects are a classic psycholinguistic phenomenon. Recent LLM behavior remains substantial and structured, and the natural competing explanations—single-parse commitment, parallel parses, failed reanalysis, or late answer selection—would normally make an excellent mechanism question.

**Kill evidence:** Hanna & Mueller, `Incremental Sentence Processing Mechanisms in Autoregressive Transformer Language Models` (NAACL 2025), directly asks whether LMs use syntactic vs shallow features, represent one vs multiple interpretations, and reanalyze/repair garden-path representations. It uses sparse autoencoders to identify interpretable features supporting both readings and analyzes reanalysis. That occupies essentially the exact mother mechanism question.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** good-enough parsing, lingering misparse, temporary ambiguity, main-verb/reduced-relative garden paths, or swapping in stronger 2026 models does not restore novelty.

**Resurrection condition:** A distinct natural parsing phenomenon with a different decisive contrast and mechanism not reducible to multiple-parse representation/reanalysis.

**References:** https://aclanthology.org/2025.naacl-long.164/ ; https://aclanthology.org/2025.acl-long.403/

---

## 2. Generic negation blindness

**Natural question:** Why can adding a logically decisive “not” fail to reverse a judgment?

**Why it initially looked good:** Natural linguistic/logical phenomenon, clean affirmative-vs-negated matched pairs, and large errors are easy to score.

**Kill evidence:** `How Language Models Process Negation` (2026) already performs observational and causal interpretability on open Mistral/Llama models. It finds correctly functioning negation components, late shortcut-promoting attention, and two competing mechanisms—suppression of negated concepts and constructive negative representations—then improves behavior by ablating the offending attention modules. A separate 2026 causal GPT-2 study also uses activation patching and head ablation.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** negated QA, negative facts, “not X”, contradiction by negation, or another semantic domain remain the same mother mechanism unless a qualitatively new contrast is isolated.

**Resurrection condition:** A non-generic negation phenomenon whose failure cannot be explained by the already identified suppression/constructive/late-shortcut mechanisms.

**References:** https://arxiv.org/abs/2605.03052 ; https://arxiv.org/abs/2603.12423

---

## 3. Stroop / congruency-style conflict

**Natural question:** Why does an automatic/default association interfere with applying an explicit conflicting rule?

**Why it initially looked good:** Stroop/congruency effects are canonical cognitive-control phenomena and naturally decompose into default pathway vs rule-governed pathway competition.

**Kill evidence:** `Conflict and Congruency Effects in Large Language Models` (August 2026) already does the causal mechanism study: causal attribution, attention analysis/ablation, and manipulations identify short-range default-cue and long-range rule pathways whose competition explains the congruency effect.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** verbal Stroop, flanker-like conflict, default-vs-rule mappings, or changing colors/categories is not enough.

**Resurrection condition:** A different cognitive-control effect whose causal bottleneck is not competition between an in-weight default mapping and an in-context rule.

**Reference:** https://arxiv.org/abs/2608.11510
