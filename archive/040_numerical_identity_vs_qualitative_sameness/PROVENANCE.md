# Provenance

Primary event stimuli are derived deterministically from `forrestdavis/ExperimentNorming`
at commit `58957bf124363a7290c4bbebb3947fb41917dc78`, specifically
`stimuli/multi_sent.xlsx` and `stimuli/multi_sent_another.xlsx`.

The build script requires an explicit source checkout and records its commit. It uses all
31 released event frames, both adjacent state-change rows per frame, and both identity
conditions. No item is selected using model behavior.

The cached Llama checkpoint used in the first local run is the
`NousResearch/Meta-Llama-3.1-8B-Instruct` mirror because the official Meta cache contains
only metadata while the compatible full mirror is already local. Results always record the
exact model identifier and local snapshot hash.

S1 deterministically crosses all 62 released rows with cue family, identity,
state-change magnitude, both initial entity-to-code binding orders, and
same-type versus different-type competitors. The different-type competitor is
the next frame's object type under a fixed cyclic rule. All A/B answer mappings
are included; no item or condition was selected from model behavior.
