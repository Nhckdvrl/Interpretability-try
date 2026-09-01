# Rejection — Taxonomic vs Thematic Relation Type in LLMs

Date: 2026-09-01  
Former project: `039_same_kind_vs_go_together_semantic_relation`  
Verdict: **KILL-NOVELTY / DEREGISTER**

## Natural question

When two concepts are related, does an LLM distinguish **same kind / taxonomic similarity** from **go together in an event or scenario / thematic relatedness** as a reusable semantic relation?

## Semantic aliases

- taxonomic vs thematic semantic relation
- similarity vs relatedness
- same kind vs go together
- categorical similarity vs event association
- taxonomic/thematic mental lexicon organization
- taxonomic–thematic triad reasoning
- relation-type direction / relation-type steering

## Why it looked promising

The distinction is exceptionally natural and scientifically legitimate. Landrigan & Mirman (2016) release 659 word pairs with independent human taxonomic-similarity and thematic-relatedness ratings on the same pairs, so the object does not depend on an invented benchmark label or an LLM judge. The design also admits obvious controls for generic relatedness, lexical identity, frequency, similarity, and co-occurrence.

That made the candidate look like a good Route-C analogue of a Hamdi-style simple semantic axis.

## Decisive hard-audit evidence

The fatal problem is **not substrate**. It is N2: after a deeper strongest-neighbor search, the remaining contribution is too close to `existing taxonomic/thematic LLM behavior/representation -> causal MI`.

### 1. 2026: the exact two-dimensional object is already operationalized with modern language-model representations

Xiao, Wang, Álvarez & Breitling (2026), **`Disentangling Similarity and Relatedness in Topic Models`** (`arXiv:2603.10619`, v3 July 2026), explicitly formalizes the two axes as:

- thematic relatedness: `dog–bone`;
- taxonomic similarity: `dog–wolf`.

It uses the same Landrigan–Mirman `TxThmNorms` 659-pair human dataset for external validation. More importantly for object ownership, it evaluates representations from BERT and OpenAI embeddings on the two dimensions and shows that they separately predict the human axes. It also has DeepSeek-V4, GPT-4.1-mini and **Qwen-Turbo** independently score both dimensions; the paper reports high correlations with human TxThmNorms ratings.

Relevant evidence:

- arXiv: https://arxiv.org/abs/2603.10619
- the paper states that the distinction is taxonomic similarity vs thematic relatedness and evaluates both on TxThmNorms;
- Table 1 evaluates BERT/OpenAI embedding representations on both axes;
- Table 14 evaluates LLM annotators, including Qwen-Turbo, against human ratings on both axes.

This is not a mechanistic causal paper, but it removes the claim that `taxonomic vs thematic is a previously unseparated model-semantic object`.

### 2. CoNLL 2025: Llama mental-lexicon semantic relatedness representation already includes both relation families

Xiao, Duan, Haslett & Cai (2025), **`Human-likeness of LLMs in the Mental Lexicon`**, evaluates GPT-4 and **Llama-3.1** lexical organization. Its semantic-relatedness measure explicitly encompasses taxonomic similarity and thematic/functional/associative relationships, and the paper concludes that LLMs—especially GPT, but also Llama—produce human-like semantic-relatedness representations.

Source: https://aclanthology.org/2025.conll-1.38/

This is broader than the exact two-axis factorization, but it occupies the surrounding LLM mental-lexicon representation story.

### 3. 2026: LLMs are already directly tested on taxonomic–thematic forced choice and explanation

Zhang et al. (2026), **`A Multi-Factor Evaluation of Fidelity in LLM-Based Cross-Cultural Surrogates`**, uses the classic taxonomic–thematic similarity task with eight LLM ecosystems. The model set explicitly includes **LLaMA** and **Qwen**. The paper does not merely use the triads as a hidden benchmark: Section 3.3.1 is titled **`Taxonomic versus Thematic Reasoning in LLM Explanations`** and analyzes whether generated explanations are taxonomic or thematic.

Source / DOI: https://doi.org/10.21203/rs.3.rs-8799167/v1

Its headline is cross-cultural simulation fidelity, but our discovery rules explicitly forbid judging object ownership only from the title. The paper already interprets model behavior through the taxonomic-vs-thematic reasoning distinction.

## Why this fails N2 despite a possible causal-steering experiment

After these neighbors, the proposed 039 contribution becomes approximately:

```text
existing work:
  LLM/PLM representations and outputs discriminate taxonomic similarity vs thematic relatedness
  + Llama/Qwen can make taxonomic–thematic choices / explanations

proposed 039:
  learn the distinction from hidden activations
  + residualize confounds
  + steer/patch it causally across a second task
```

That is a stronger **methodological treatment of an already-owned scientific object**, not a new scientific/model object. Under `FINDING_RULES.md` v2.1, `behavior/representation -> mechanism`, `probe -> patching/steering`, or `same object with stronger MI` does not by itself clear N2.

This is exactly the mistake the Route-C correction was meant to avoid: **simple is good, but simplicity does not excuse object reuse.**

## Secondary design risk: causal identifiability

Even without the novelty collision, the frozen steering design was less decisive than initially claimed. A relation direction learned from neutral two-word carriers and injected into a triad prompt could change generic semantic compatibility, lexical similarity, or association geometry rather than instantiate a task-independent `relation-type variable`. Residualizing observable nuisance covariates helps but does not make the edit uniquely interpretable as taxonomic-vs-thematic computation.

This is secondary; novelty already kills the project.

## Strongest-neighbor warning

Do not revive by changing:

- Llama -> Qwen / Gemma / Mistral;
- probe -> SAE / steering / activation patching / conceptors;
- 659-pair norms -> SimLex / WordSim / custom pairs;
- word pairs -> triads;
- `taxonomic vs thematic` -> `similarity vs relatedness`;
- `representation` -> `reusable causal relation state`.

Those variants preserve the same occupied scientific axis.

## Death code

`F2 / N0-N2 — exact semantic axis already studied in language-model representations and LLM behavior; remaining delta is primarily stronger causal MI.`

## Resurrection condition

Only reconsider if there is a **genuinely new independent semantic object beyond the taxonomic/thematic distinction**—for example a natural third axis that is not already subsumed by similarity/association/lexical-relation work, has clean natural cross-cells, and remains paper-scale after deleting the old taxonomic/thematic framing.

Do **not** resurrect merely because no prior paper has applied the exact planned steering statistic.
