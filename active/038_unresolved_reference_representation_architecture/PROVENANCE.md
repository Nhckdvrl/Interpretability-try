# Provenance

Behavioral S0 stimuli are derived from `lukasellinger/itdepends` commit
`e9985ebc3c97d37e6c902d5cb8700c215ca8ad75`.

The build uses English `normal` ClearRef (`01`, `10`) and SharedRef (all six
permutations) entries from the released judged-output files. Only `conversation` and the
deterministic `entry.positive` / `entry.negative` metadata are used; released model answers
and LLM-judge labels are not used as experimental gold.

AmbiCoref commit `69a6639cdaaa2b7bcaadd173da960b20c0335742` is reserved for the
resolved A/B causal calibration stage after S0. Its large generated corpus is not subset by
the present model effects.

Behavioral S0 was run without sampling on cached revisions
`d10aef7999a2b5ba950ab3974312feeedbfe0b77` (Llama-3.1-8B mirror) and
`9216db5781bf21249d130ec9da846c4624c16137` (Qwen3-32B). The Qwen run used a
node-local dereferenced copy verified byte-size-identical by `rsync -aniL`; no
weights were downloaded.

The Llama candidate calibration uses every eligible released item under the
prespecified structural-family or semantic-hash splits. The invalid AmbiCoref
candidate direction is retained as an audit result but was never fit. The
ItDepends causal test records its fixed layer, fitted direction, strength,
random control, and shuffled-label control in raw results.
