# Rejection — Lexical Identity / Inflection → Derivational Morphology

```yaml
question: Do modern LLMs represent derivational morphology as a factor separable from lexical identity and inflectional features?
mother: Model Internal Sleuthing: Finding Lexical Identity and Inflectional Features in Modern Language Models (ACL 2026)
semantic_aliases:
  - derivation vs inflection representations
  - word formation vs inflection in LLM internals
  - derivational feature vectors
  - lexeme identity vs derivational morphology
  - morphological derivation geometry
what_was_reviewed: mother omitted-axis plausibility and strongest-neighbor ownership
kill_class: F2
kill_evidence: The adjacent axis is natural, but ACL 2026 Findings Vocab Diet explicitly studies transformation vectors for inflection, derivation and capitalization across languages and shows the model can interpret compositional word representations. Earlier linear-representation work also directly includes derivational prefix relations. Thus derivation is not an unasked neighboring property of modern LM word representations.
nearest_neighbor_warning: Do not revive by swapping DeriNet/UniMorph/language, limiting to prefixes or suffixes, or replacing probes with patching/SAE/steering. Those change measurement or subtype, not the scientific question.
resurrection_condition: Only reopen if a different classical word-formation property yields a genuinely unasked scientific object and the nearest modern representation papers do not already measure it.
```
