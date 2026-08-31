# Rejection — Tool Relevance → Tool Necessity

```yaml
question: Does an LLM distinguish a tool being semantically relevant from the tool being actually necessary or incrementally useful for answering the current query?
mother: Do LLMs Know Tool Irrelevance? Demystifying Structural Alignment Bias in Tool Invocations (ACL 2026)
semantic_aliases:
  - relevant vs necessary tool
  - useful vs unnecessary tool calls
  - when to call tools
  - redundant tool invocation
  - tool need vs semantic match
  - tool abstention when answerable directly
what_was_reviewed: strongest-neighbor/title and mechanistic occupancy
kill_class: F2
kill_evidence: Two 2026 works directly own tool necessity. LLM Agents Already Know When to Call Tools -- Even Without Reasoning introduces When2Tool, explicitly defines tool-necessary vs tool-unnecessary tasks and finds necessity linearly decodable from pre-generation hidden states across six models. Model-Adaptive Tool Necessity Reveals the Knowing-Doing Gap further decomposes tool use into internal necessity cognition and execution, finding both decodable and a late-layer cognition-to-action mismatch. Thus relevance→necessity is not an unasked adjacent property.
nearest_neighbor_warning: Do not revive as tool utility, redundancy, answerability-without-tool, invocation abstention, knowing when to call, cognition-vs-action, or by changing tool domains/models/agent harnesses.
resurrection_condition: Reopen only for a different property of tool-choice computation not reducible to semantic relevance, structural alignment, necessity, abstention, or cognition-to-action translation.
```
