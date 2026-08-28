# Raw-case audit — D0 v2

The D0 v1 results are invalidated in INVALIDATED_D0_V1.md. D0 v2 correctly
parses the LegalBench test TSV and uses issue-level proposition swaps.

Qwen3-8B: only 9/40 cases passed the full recognition plus admitted-sensitivity
capability gate; only 1/20 matched polarity pairs was gated. Supports-other
recognition/capability was the dominant failure. The paired operator therefore
cannot diagnose undo persistence.

Gemma3-12B: only 8/40 cases passed the full gate; only 1/20 matched pairs was
gated. The paired struck delta was negative on that gated pair, while neutral
struck movement failed the control. This is not evidence for UDH-11.

Provisional verdict for this D0: HOLD-D0-POLARITY-ASYMMETRY. Do not lower
thresholds or select favorable cases. No N1 or panel expansion is justified.
