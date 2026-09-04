# Final experimental verdict — 040 Numerical Identity vs Qualitative Sameness

Date: 2026-09-04  
Disposition: **ARCHIVE — abstract identity representation and causal-use contract failed**

Qwen3-8B showed strong direct identity judgments across natural and continuity surfaces while
preserving type knowledge, so the project cleared a stronger bar than merely reproducing the
known `the`/`another` hidden-state contrast. The decisive arbitrary-history tests nevertheless
failed:

- history selection followed whichever entity-to-code binding was introduced last (97.8% vs
  34.3% target accuracy for same-type competitors; 98.4% vs 47.6% for different-type);
- an exact opposite-order residual transplant at the frozen binding boundary moved away from,
  not toward, the donor decision (-0.206 logits), while type knowledge stayed intact;
- a frozen identity direction trained on the natural determiner surface did not transfer to
  held-out continuity paraphrases (AUC 0.474) and had no aligned causal effect on code history
  (-0.0045 logits).

Thus numerical identity is behaviorally answerable but is neither a demonstrated abstract
cross-surface state nor a causally specific controller of token-history inheritance in this
checkpoint. The unexpected order crossover is reproducible, but converting 040 into generic
binding recency would narrow the object and collide with established in-context order/binding
work. All code, controls, outputs and nulls are retained for reproducibility.
