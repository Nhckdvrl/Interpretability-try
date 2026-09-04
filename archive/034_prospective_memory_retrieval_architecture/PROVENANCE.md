# Provenance

The released-behavior audit uses `genglinliu/PMBench` commit
`e1093c470c8981daf522d4ef047a7c3a71e077d7`: the deterministic
`data/synthetic_week_v9.json` scenario and the generated report over 64 released
trajectories. No API inference or LLM judge is used.

The S0-2 controlled extension is generated deterministically by
`scripts/build_focality_expectancy.py` (version `s0_2_v1`, seed 20260904). It
contains 16 hand-audited semantic items. For each item the critical cue/no-cue
sentence is identical across focality and expectancy conditions; all six
semantic-to-A/B/C mappings are included. It uses no external judge or generated
text and does not select items based on model outcomes.
