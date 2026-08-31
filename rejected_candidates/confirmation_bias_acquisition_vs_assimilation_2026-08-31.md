# Confirmation-bias locus: acquisition vs assimilation — rejection record

```yaml
question: Is LLM confirmation bias primarily a bias in what evidence is actively sought, a bias in how already-observed evidence is assimilated/used, or a shared belief-consistency mechanism spanning both stages?
mother: Failing to Falsify (2026) + independent LLM choice-supportive/confidence-bias work
semantic_aliases:
  - confirmation bias evidence selection vs evidence updating
  - search bias vs assimilation bias in LLMs
  - query selection vs belief update confirmation bias
  - evidence acquisition vs evidence use
what_was_reviewed: PAPER-SCALE, classic confirmation-bias decomposition, active-search LLM behavior, passive/choice-supportive evidence-use behavior, official artifact, N0/N1/N2, substrate gate
kill_class: F3
kill_evidence: The concept-level question is natural, and Failing to Falsify reports a strong active-search confirmation phenotype across eleven LLMs. However its official public GitHub currently contains only the README and explicitly marks the code/data/model-output repository structure as 'Coming Soon'. Independent passive-evidence/choice-supportive studies use different tasks and can show different or even opposing evidence-weighting effects, so merging them cannot legitimately stand in for a matched acquisition-vs-assimilation phenotype. A direct project would first need to build and behaviorally validate a forced-evidence counterpart to the active hidden-rule task, which would make the experiment discover whether the paper premise exists.
nearest_neighbor_warning: Do not revive by merely implementing Wason 2-4-6 yourself, swapping rule families, using a different confidence benchmark, or treating choice-supportive bias as the assimilation half without a matched measurement contract.
resurrection_condition: Release of the original auditable artifact and/or an existing matched active-search vs forced-evidence dataset on modern open models that isolates selection from assimilation with deterministic gold.
```

Verdict: **KILL-DATA / KILL-BEHAVIOR for current authoritative register**.
