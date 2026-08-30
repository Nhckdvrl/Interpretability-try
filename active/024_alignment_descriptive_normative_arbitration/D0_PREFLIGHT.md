# 024 D0 v1 Preflight

**Contract:** `configs/d0_contract.json`

**Stage:** behavioral mother reproduction only

**Mechanism calls:** forbidden until D0 is adjudicated

## Frozen comparison

Four same-provider, architecture- and size-matched base/aligned pairs are used:
Qwen3 1.7B, Gemma 3 1B, Llama 3.2 1B, and SmolLM2 360M. Checkpoint revisions
are written to runtime metadata. A family is the statistical replication unit;
the 3,483 primary human decisions are not treated as independent model
replications.

The official Meta Llama base repository returned HTTP 403 during the access
check, before any Llama forward pass. The Llama entry was therefore amended to
the public Unsloth mirrors of Llama 3.2 1B base and instruct releases, a pair
explicitly included in the mother study.
Both sides use the same mirror provider; no model output informed this access
amendment.

The initially listed Mistral 7B pair required a large uncached transfer. Before
any fourth-family forward pass it was replaced by the mother study's SmolLM2
family; when the 1.7B transfer stalled, the final executable pair was frozen as
the mother-listed SmolLM2 360M base/instruct pair. This preserves the frozen
four-family design and strict pairing; no fourth-family output informed the
substitution. A low-capability result cannot be rescued: the original mass and
informativeness gates still apply.

The mother inventory includes both Gemma 2 2B and Gemma 3 1B pairs. The former
was found during pre-call access audit to serialize its base checkpoint at
10.46 GB. Before any Gemma forward pass, the entry was changed to the mother's
Gemma 3 1B pt/it pair (2.00 GB per checkpoint). No Gemma output informed this
substitution.

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
