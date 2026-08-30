# 024 D0 v1 Preflight

**Contract:** `configs/d0_contract.json`

**Stage:** behavioral mother reproduction only

**Mechanism calls:** forbidden until D0 is adjudicated

## Frozen comparison

Four same-provider, architecture- and size-matched base/aligned pairs are used:
Qwen3 1.7B, Gemma 2 2B, Llama 3.2 3B, and Mistral 7B v0.3. Checkpoint revisions
are written to runtime metadata. A family is the statistical replication unit;
the 3,483 primary human decisions are not treated as independent model
replications.

The primary comparison follows the mother paper's native-format design: plain
structured completion for a base checkpoint and the provider chat template for
its aligned counterpart. The shared-plain comparison is frozen as a format
control. Both use identical game content, histories, and the same JSON decision
prefix. No text is generated; the harness extracts deterministic F/J token
probabilities.

## Frozen decision rule

`PROMOTE_BEHAVIOR` requires at least three of four families to show native
base-minus-aligned Pearson r >= .05 with participant-cluster bootstrap lower
bound above zero, median native delta-r >= .05, and a positive shared-plain
delta-r in at least three families. The mass and informativeness gates in the
JSON contract are evaluated before this rule.

This gate is intentionally about reproducing the broad mother object. Passing
does not establish descriptive retention, normative-state strengthening, or
late arbitration. It only authorizes a separately frozen mechanistic stage.
