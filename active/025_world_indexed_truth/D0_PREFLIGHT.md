# 025 D0 frozen preflight

Contract: `025-d0-v1-world-indexed-capability`.

## Legal object

The scored contrast holds the proposition and local-world context fixed. Only
the requested evaluation index changes: actual reality versus the explicitly
stipulated local world. Each context produces a joint pair, and the pair—not an
isolated question—is the primary unit.

## Data and provenance

- NASA Science supplies the eight planet ordinals.
- IUPAC supplies the selected element atomic numbers.
- Integer expressions are recomputed independently in the builder.
- Each of 32 source relations yields one true proposition and one deliberately
  mismatched false proposition. Every proposition is placed once in an aligned
  and once in a conflicting local world.
- Three local-world frames and three query-paraphrase families are assigned by
  a deterministic balanced rotation. No character beliefs are used.

This produces 64 propositions, 128 fixed contexts, and 256 queries. Actual
truth, local truth, alignment, domain, world frame, query world, and paraphrase
are all explicit fields in the saved bank.

## Models and scoring

Four already-audited open instruct checkpoints—Qwen, Gemma, Llama, and
SmolLM—are pinned by immutable Hugging Face revision. Candidate labels `TRUE`
and `FALSE` are scored by conditional sequence log likelihood; no generated
text parser or post-hoc prompt selection is used.

## Frozen adjudication

A family must pass overall, conflict, aligned, both conflict-polarity, every
domain, every world-frame, and every paraphrase floor in the JSON contract.
`PROMOTE_BEHAVIOR` requires at least three of four family passes and median
conflict joint accuracy at least 0.75. Only that verdict authorizes mechanism
work. One or two passes are reported as limited evidence, never silently
promoted.

Any change after the first model forward pass requires a new contract version.

## Frozen strong-model replication (v2)

V1 returned `HOLD_PREREQUISITE_CAPABILITY`: all four sub-2B checkpoints failed
the joint gate, despite Qwen and Gemma answering the local index reliably. To
avoid mistaking a scale prerequisite for a dead scientific object, v2 changes
only the four checkpoints to Qwen3-8B, Gemma3-12B, Llama3.1-8B, and
Mistral-Small-24B. The bank, prompts, sequence scoring, thresholds, and aggregate
rule are inherited byte-for-byte from v1. V2 is an independent replication and
cannot overwrite v1.
