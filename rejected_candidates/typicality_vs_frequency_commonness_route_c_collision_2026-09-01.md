# Rejection — Typicality vs Frequency / Commonness

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Natural question

Does a model know that an item can be **typical of a category** without simply being the most frequent/common item it has seen?

## Semantic aliases

- typicality vs frequency
- prototype centrality vs lexical frequency
- representative vs common
- category typicality vs exposure

## Why it looked promising

This has the desired Hamdi-style shape: two everyday properties that correlate but are conceptually distinct, with natural cross-cells and extensive human norms.

## Decisive kill evidence

The object is already too crowded in LM research. Typicality in language models has been directly studied for years, including category/property generalization and comparisons with human typicality. More importantly, 2026 work on **LLM word associations** explicitly analyzes lexical factors including frequency alongside response variability and typicality on modern open models (Mistral-7B, Llama-3.1-8B, Qwen-2.5-32B).

Recent source: Rodriguez, Candito & Huyghe, **“Modeling the human lexicon under temperature variations: linguistic factors, diversity and typicality in LLM word associations”** (LREC 2026 / arXiv:2603.18171).

Source: https://arxiv.org/abs/2603.18171

Even if a new project orthogonalized frequency and typicality more cleanly and added causal patching, the scientific delta would mostly be a stronger factorization/method on an already-owned LM conceptual object.

## Strongest-neighbor warning

Do not revive as prototype-vs-frequency, common-vs-representative, typicality direction, or temperature-controlled typicality mechanism without a genuinely new orthogonal object.

## Death code

`F2 / N0-N2 — typicality is already an explicit LM object and recent open-model work jointly analyzes frequency-related lexical factors.`

## Resurrection condition

Only reconsider if a different natural semantic property B can be separated from typicality and is not already covered by prototype/category-representation literature.
