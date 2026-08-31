question: Does the entity-binding mechanism used for static relational retrieval support causal rebinding when an entity's state changes over time?
mother: ICLR 2026 Mixing Mechanisms: How Language Models Retrieve Bound Entities
semantic_aliases:
  - static entity binding vs dynamic rebinding
  - entity state update circuit
  - binding update after PUT REMOVE MOVE
  - dynamic entity tracking mechanism
what_was_reviewed: strongest-neighbor / mechanistic ownership
kill_class: F2
kill_evidence: 2026 work already directly studies dynamic entity tracking and rebinding under state changes with causal interventions. 'A retrieval conditioned rebinding circuit for dynamic entity tracking in LLMs' identifies a compact attention-head circuit for updating bindings across state changes in Gemma/Llama, and 'Do Language Models Track Entities Across State Changes?' mechanistically analyzes PUT/REMOVE-style state updates and derives intervention predictions. The proposed static-to-dynamic extension is therefore direct scientific-object ownership, not an omitted axis.
nearest_neighbor_warning: Do not revive by swapping state-change operators, domains, datasets, or model families, or by renaming rebinding as memory update/state tracking. These works own the causal update object.
resurrection_condition: Only reopen for a genuinely different binding property not reducible to static retrieval or dynamic state-update/rebinding, with an independently meaningful axis and no direct causal predecessor.
