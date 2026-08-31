# Analogical transfer: relational abstraction vs familiarity-bound transformation

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Semantic aliases

- relational structure mapping vs symbol-specific transformation
- abstract analogy transfer vs familiarity-bound completion
- far analogical transfer mechanism
- conceptual abstraction vs alphabet-specific rule execution

## Natural question considered

When LLMs solve analogies, do they construct a domain-general relational transformation that can transfer to unfamiliar symbol systems, or do they rely on representations tied to familiar alphabets/tokens?

## Why it looked strong

The question is rooted in structure-mapping theory and developmental analogy research. TACL 2026 `Can Large Language Models Generalize Analogy Solving Like Children Can?` provides a strong behavioral window: adults and children transfer letter-string analogy rules across Latin, Greek, and novel-symbol alphabets, whereas tested LLMs degrade sharply with domain unfamiliarity. The study includes open families such as Gemma-2 and Llama-3.1, additional Mixtral/Qwen variants, and public preregistration/materials/data/code.

## Decisive N2 kill

The mother does not stop at behavior. Its RQ3 and Discussion explicitly ask why LLMs fail to generalize and argue that the core problem is that the conceptual abstraction of an alphabet as an ordered relational system does not flexibly map to less familiar domains. Rule-check experiments are used to support this explanation: repetition transfers relatively well, while predecessor/successor operations that require an abstract ordered-sequence representation degrade.

Therefore a mechanistic project contrasting `relational abstraction / structure mapping` with `familiarity-bound symbol transformation` would most naturally be described as causal validation/localization of the mother paper's own headline interpretation.

This fails the current N2 delta-width rule even though the dataset and phenotype are unusually attractive.

## Nearest-neighbor warning

Do not resurrect by changing the analogy format, replacing `relational abstraction` with `structure mapping`, or moving from behavior to activation patching. The scientific interpretation itself is already occupied.

## Resurrection condition

Only reopen if a distinct external analogical-reasoning debate can be instantiated on the same artifact without being equivalent to `abstract relational transfer vs familiarity-bound execution`, or if a separate cross-phenomenon shared computation question emerges for which this dataset is only one measurement window.
