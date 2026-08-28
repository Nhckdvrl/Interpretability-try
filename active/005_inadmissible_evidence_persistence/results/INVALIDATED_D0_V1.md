# Invalidated D0 v1 results

All 005 result files produced before the D0 v2 rebuild on 2026-08-28 are invalid.

The v1 builder parsed the first TSV column (index) as case text, so prompts
contained record numbers rather than LegalBench facts. It also used abstract
TARGET/OTHER meta-statements and a verdict-oriented neutral control. Those runs
cannot support a behavioral verdict and must not be pooled with D0 v2.

Invalidated filename patterns:

- qwen3_8b.exploratory*
- qwen3_8b.exact*
- gemma3_12b.exploratory*

They are retained only as a reproducibility/postmortem record.
