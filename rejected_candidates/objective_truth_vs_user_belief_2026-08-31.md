question: Does an LLM represent objective world truth separately from an attributed user's belief about the same proposition?
mother: ACL 2026 How Context Shapes Truth + belief-tracking mechanistic literature
semantic_aliases:
  - world truth vs user belief
  - objective state vs attributed belief
  - p(world) vs p(user)
  - factual truth code vs belief-state code
what_was_reviewed: strongest-neighbor / mechanism ownership
kill_class: F2
kill_evidence: A 2025 open Qwen3-8B study, '(How) do LLMs track user beliefs?', already trains separate p(user) and p(world) probes on the same facts and causally masks attention to belief-bearing context. Under masking, user-belief decoding collapses to ~38-40% while world-state decoding remains >80%, directly supporting separable world-vs-user state signals and a retrieval-based belief mechanism. Existing false-belief mechanistic work likewise explicitly dissociates reality from another agent's belief. The proposed headline is therefore already substantially answered outside formal conference publication.
nearest_neighbor_warning: Do not revive by swapping user for character/agent, changing ToM benchmark, adding a truth-vector method, or restricting to a new model family. The scientific meaning is the same unless the new question concerns a genuinely different social-state object.
resurrection_condition: Only reopen if the question moves beyond world-vs-belief separability to a distinct unoccupied causal computation with different intervention predictions that is not already tested by world/user probes, lookback masking, perspective projection, or false-belief representation work.
