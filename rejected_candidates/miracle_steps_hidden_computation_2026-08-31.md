# Rejection — Miracle Steps → Hidden Computation

```yaml
question: When a correct CoT omits a crucial reasoning step, was that step computed internally but not verbalized, or was the answer reached through a shortcut?
mother: Curing "Miracle Steps" in LLM Mathematical Reasoning with Rubric Rewards (ACL 2026)
semantic_aliases:
  - skipped reasoning vs hidden reasoning
  - implicit computation behind omitted CoT steps
  - silent reasoning behind miracle steps
  - shortcut vs latent reasoning in CoT
  - unfaithful omitted intermediate computation
what_was_reviewed: strongest-neighbor/title and mechanism occupancy
kill_class: F2
kill_evidence: The proposed headline is already occupied by step-level CoT faithfulness and hidden-computation work. Bridging Reasoners studies information present for answering but absent from stated CoT; Faithfulness as Information Flow explicitly separates direct prompt-to-answer shortcut flow from CoT-mediated flow; unlearning-reasoning-steps and filler-token/hidden-computation work attack the same causal distinction. Miracle Steps supplies a new behavioral subtype but not a new scientific object.
nearest_neighbor_warning: Do not revive by renaming miracle steps as omitted steps, latent steps, silent reasoning, compressed reasoning, implicit reasoning, shortcut reasoning, or by swapping math datasets/models/faithfulness tools.
resurrection_condition: A genuinely new internal computation must be identified that is not reducible to hidden computation vs direct shortcut / CoT faithfulness, with a distinct causal prediction not already tested by information-flow or step-removal interventions.
```
