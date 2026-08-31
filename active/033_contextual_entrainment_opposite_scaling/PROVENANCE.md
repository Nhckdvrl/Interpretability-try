# V0 provenance audit

- Paper: arXiv `2604.13275v1` / Findings of ACL 2026.
- The arXiv source publishes aggregate raw-logit tables for all six Pythia sizes and describes a 4,265,204-sample LRE-derived corpus.
- The paper and arXiv metadata do not provide a code repository or the item-level generated corpus.
- Consequently, `scripts/replay_paper_scaling.py` is an aggregate-table integrity replay only. It verifies the reported opposite signs and establishes the exact metric contract; it is not an item-level mother reproduction.
- Local cache currently contains Pythia-410M and Pythia-1B. These are sufficient for a two-endpoint pipeline smoke test after item generation is reconstructed, but insufficient to estimate the six-point scaling law.

The next V0 step is to pin the upstream LRE dataset and the ACL 2025 predecessor's context-generation recipe, then create a transparent reconstruction manifest. It must be labeled reconstructed rather than exact unless the mother authors release their generated item table.
