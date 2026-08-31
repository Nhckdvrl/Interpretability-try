# Explicit vs Implicit Memory Systems — Rejection Record

```yaml
question: Do LLMs' explicit recall and implicit behavioral adaptation depend on causally separable memory systems or a shared trace with different readouts?
mother: ACL 2026 Best Resource Paper ImplicitMemBench
semantic_aliases:
  - declarative vs nondeclarative memory systems in LLMs
  - explicit vs implicit memory circuits
  - shared memory trace vs separate memory systems
  - explicit recall vs automatic behavioral adaptation
  - causal dissociation of explicit and implicit memory
what_was_reviewed: full ImplicitMemBench paper including main text and appendices; released dataset; 2026 procedural/implicit memory neighbors
kill_class: F8
kill_evidence: The mother already goes beyond a benchmark. It explicitly asks whether external explicit memory can improve implicit memory, reports that explicit-memory modules give non-uniform gains, states that implicit memory cannot be reduced to explicit storage/retrieval alone, and interprets cross-paradigm capability dissociations as suggesting distinct mechanisms. A new causal double-dissociation paper would therefore most naturally mechanize an interpretation already owned by the mother rather than introduce a new concept-level question. This is the same failure shape as 032: strong broad mother followed by a mechanistic decomposition of the mother's own conclusion.
nearest_neighbor_warning: Do not revive as declarative-vs-procedural circuits, shared-vs-separate memory traces, explicit/implicit double dissociation, or external-memory-vs-native-memory mechanisms by changing the benchmark or model family.
resurrection_condition: A memory-system question orthogonal to ImplicitMemBench's explicit-vs-implicit reducibility claim, with a scientific distinction not already framed by the mother.
```

Decisive evidence: ImplicitMemBench main text states that representative explicit-memory systems do not consistently improve the implicit benchmark and that implicit memory is not reducible to explicit storage/retrieval; it also interprets capability dissociations as suggesting distinct mechanisms. Paper: https://aclanthology.org/2026.acl-long.1301/
