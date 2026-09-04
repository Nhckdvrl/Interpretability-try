# Final experimental verdict — 035 Shared Dynamic Context Update

Date: 2026-09-04  
Disposition: **ARCHIVE — behavioral recipient absent; venue-scale claim not testable here**

The question remains scientifically broad, but this concrete project cannot currently test it.
Released Llama ratings were only weakly separated and nonmonotone. After correcting an
implementation bug in the first forced-choice runner, the full 90-item, six-label-order panel
still failed in both frozen model families:

- Llama-3.1-8B-Instruct: three-class balanced accuracy 0.333; forced high/low accuracy 0.500;
  all 90 aggregated predictions were `high`.
- Qwen3-8B: three-class balanced accuracy 0.367; forced high/low accuracy 0.550; 68/90
  aggregated predictions were `low`.

Thus the presupposition side is governed by opposite model-specific class priors rather than a
stable recipient behavior. Without that recipient, a null cross-task intervention cannot
distinguish separate mechanisms from an inactive measurement. The failure does not license an
anaphora-only story, an ambiguity about shared computation, or a narrower prompt-bias paper.

All frozen items, corrected scripts, raw outputs, deterministic analysis and provenance are
retained so the decision is reproducible. Reopening requires an independently established
presupposition support measure on a new external behavior window.
