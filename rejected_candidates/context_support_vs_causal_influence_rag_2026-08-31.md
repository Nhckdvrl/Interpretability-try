# Rejection — Context Support vs Causal Influence in RAG

```yaml
question: Can a retrieved context passage semantically support an answer without causally influencing generation, or causally influence generation without actually supporting the answer?
mother: Attributing Response to Context: A Jensen–Shannon Divergence Driven Mechanistic Study of Context Attribution in RAG (ICLR 2026)
semantic_aliases:
  - evidence support vs causal reliance in RAG
  - citation correctness vs faithfulness
  - semantic attribution vs causal attribution
  - supported-by-context vs generated-because-of-context
  - post-rationalized citations
what_was_reviewed: strongest-neighbor/title ownership and source-separation neighbors
kill_class: F2
kill_evidence: Correctness is not Faithfulness in RAG Attributions explicitly defines citation faithfulness using both document support and causal impact and studies cases where citations are correct/supportive but did not cause the answer. This directly owns the proposed distinction. Additional 2026 context-attribution work on what the model already knows further occupies context-vs-parametric source separation.
nearest_neighbor_warning: Do not revive as semantic vs causal attribution, support vs reliance, correct vs faithful citation, post-rationalization, parametric vs contextual knowledge, or by changing RAG corpus/model/attribution method.
resurrection_condition: Reopen only for a different same-object property not reducible to support/correctness, causal reliance/faithfulness, or context-vs-parametric source separation.
```
