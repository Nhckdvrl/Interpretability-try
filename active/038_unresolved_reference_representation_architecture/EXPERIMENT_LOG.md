# Experiment Log

## S0 — deterministic candidate scoring and permutation sensitivity

Question:
Do the primary models have the basic entity/reference denominator required before asking
whether unresolved reference carries parallel candidates, underspecification, or an early
winner?

Experiment:
Use the released English normal ItDepends items. Score every deterministic candidate entity
under all two ClearRef and six SharedRef entity-order permutations. Measure ClearRef accuracy,
whether both licensed SharedRef candidates outrank the negative distractor, candidate-score
asymmetry, and whether preference follows entity order.

Prediction:
ClearRef must strongly separate the licensed candidate from the distractor. SharedRef must
retain information about both licensed candidates relative to the distractor. Large stable
candidate asymmetry or systematic order-following motivates the early-commitment test, but
behavior alone cannot distinguish H1 from H2 and will not be reported as representational
format evidence.

Result:
Llama-3.1-8B-Instruct scored 1,466 released rows (104 ClearRef and 1,362
SharedRef permutations). ClearRef accuracy was 96.15%. On SharedRef, both licensed
candidates outranked the released distractor in 86.64% of rows. The mean absolute log-score
margin between licensed candidates was 2.58. The preferred licensed candidate was the first
mention in 584/1,362 rows and the second mention in 778/1,362 rows. Across the six released
permutations, 45.81% of semantic items changed which licensed candidate was preferred.
Qwen3-32B replication is pending; its exact cached revision is being localized to the compute
node rather than downloaded.

The frozen Qwen3-32B replication is now complete on all 1,466 rows. ClearRef accuracy was
98.08%, and both licensed SharedRef candidates outranked the distractor in 95.96% of rows.
Its mean absolute licensed-candidate margin was 5.88, larger than Llama's 2.58. The preferred
candidate was the first mention in 580/1,362 rows and the second mention in 782/1,362 rows;
41.85% of semantic items flipped their preferred candidate across released permutations.
Both model families pass the behavioral panel gate.

Interpretation:
The Llama checkpoint passes the comprehension and both-candidate coverage denominator, so a
candidate-structure experiment is licensed. The sizeable candidate asymmetry and frequent
permutation-dependent preference reversals make premature commitment a live hypothesis.
The near-identical mention-position counts and frequent order-dependent reversals replicate
the asymmetric behavioral signature in a much larger second family. They are still not
evidence for H3 by themselves: output logits could be a downstream decision
readout over either parallel alternatives or an underspecified state. Likewise, both licensed
candidates beating a distractor does not establish simultaneous internal alternatives.

Next:
Use the completed cross-family behavior only as a denominator. A candidate basis must
transfer to a held-out family and causally change resolved-reference scores before it is
applied to unresolved examples; the Llama causal calibration below is the current test.

## R1/J1–J3 — candidate structure and shared unresolved state

Question:
Does Llama's unresolved-reference state contain balanced, independently causal candidate
components (H1), a cross-template shared unresolved component (H2), or an asymmetric
decision/commitment axis (H3)?

Experiment:
Two preregistered calibration routes were audited. First, 617 human-judged AmbiCoref items
were exactly aligned to released sentence files (303 complete ambiguous/unambiguous pairs).
ECO/ECS were discovery families, IC validation, and TOP held out. Second, ItDepends ClearRef
order pairs were split by semantic-item hash (60/20/20) and used to learn a position-balanced
referent direction. All-layer trajectories were summarized over layers 13–26; the causal
test used the fixed center hidden-state layer 19 (block 18), one discovery projection SD,
and random plus shuffled-label controls.

Prediction:
H1 requires high CCS and balanced Coverage for both licensed candidates. H2 requires a
shared ambiguous-vs-resolved component that transfers across held-out structural families,
then jointly couples both candidates. H3 predicts a strong but asymmetric candidate axis
whose preference is sensitive to published order permutations.

Result:
The AmbiCoref candidate-A/B calibration was invalid before fitting: all 74 eligible ECO/ECS
discovery controls preferred candidate 0, all 26 IC controls preferred candidate 0, whereas
20/22 TOP controls preferred candidate 1. Candidate direction was therefore confounded with
structural family and no probe was fit.

The alternative ItDepends ClearRef calibration was exactly position-balanced (27/27
discovery rows). Across the prespecified middle-layer family, held-out ClearRef test AUC had
median 1.00 and confidence 0.85. On SharedRef, the readout agreed with the ultimate licensed
candidate preference at median 0.662 and had lower confidence, 0.519.

At fixed layer 19, a one-SD intervention passed J1 on 22 held-out ClearRef permutations:
aligned bidirectional effect 0.296, 95% bootstrap CI [0.115, 0.479]. Random was 0.004
[-0.024, 0.033], and shuffled-label was 0.053 [-0.025, 0.131]. On 454 SharedRef
permutations, however, candidate causal separability was 0.000 [-0.026, 0.027] and Coverage
was 0.455 [0.423, 0.487]. Position-0 self/cross effects were 0.249/0.101; position-1
self/cross effects were -0.095/-0.239, an asymmetric opponent-axis pattern rather than two
selective candidate edits.

The paired AmbiCoref ambiguity readout did not supply the missing H2 evidence. Pronoun-state
middle-layer AUC was chance on IC/TOP (0.500/0.516). Final-decision AUC transferred to IC
(0.923) but failed on held-out TOP (0.566; balanced accuracy 0.516). Therefore a general
shared unresolved-state intervention was not licensed.

Interpretation:
The results argue against the clean H1 signature: both candidates are behaviorally licensed,
but the causally qualified direction does not independently manipulate them. A reusable H2
state also fails its required structural-family transfer. The combined behavioral order
flips, moderate internal/output agreement, and causal asymmetry are most compatible with an
H3-like downstream single competition/commitment axis, but this is not yet a unique causal
identification of premature commitment. In particular, the qualified direction tracks
mention position rather than candidate identity, and the AmbiCoref family confound prevents
using that artifact as a rescue.

Next:
For Llama, do not search layers for H1 or H2. The replicated Qwen behavioral asymmetry makes
cross-family candidate competition credible, but does not justify duplicating an
underidentified position-direction intervention at 32B scale. The next defensible experiment
is an independently balanced resolved-A/resolved-B stimulus
construction that permits entity-specific (not position-only) removal; otherwise stop the
architecture claim as not fully identifiable and report the asymmetric decision-axis result.

## R2 — same-content permutation transplant at the unresolved pronoun

Question:
Is the order-dependent winner an entity-specific commitment already active when the ambiguous
pronoun is processed, or only a later response-comparison state?

Experiment:
Use the 36 held-out ItDepends semantic items and all six discourse permutations. Pair
permutations that swap the two licensed candidates while leaving the distractor position
fixed. At the exact `it` token, replace the frozen layer-19 state with its same-item,
opposite-order counterpart. Compare with the same permutation delta from another semantic
item and matched-norm random vectors. Candidate names and the later response list retain a
fixed semantic order, so the primary margin is candidate-specific rather than position-only.

Prediction:
Premature commitment at the pronoun predicts movement toward the same-item donor's semantic
candidate preference beyond the transferable generic order delta. A null despite strong
clean order flips predicts that the preference is constructed after pronoun interpretation.

Result:
Both licensed candidates beat the distractor in 0.769 of the held-out rows, and paired clean
permutations flipped the preferred licensed candidate in 0.269. Nevertheless, across 210
nonzero donor contrasts the exact same-item transplant changed the donor-aligned margin by
-0.003 logits, 95% CI [-0.018, 0.012]. Shuffled-item order deltas changed it by +0.002 and
random vectors by -0.006; real-minus-shuffled also included zero. No permutation pair showed
a stable positive real effect.

Interpretation:
The earlier causal final-decision axis and the current pronoun-state null form a temporal
dissociation: the model has an order-sensitive response competition state, but the tested
semantic winner is not causally present at the unresolved pronoun. This directly weakens H3
as *premature* commitment. It does not establish H1 or H2, whose required balanced candidate
and cross-family shared-state signatures already failed. The best surviving account is late
construction of a choice from an unresolved or distributed state.

Next:
Test the mechanism-derived behavioral prediction once: counterbalance the response candidate
list after fixed ambiguous discourses, while using ClearRef as the specificity control. Late
decision construction predicts ambiguity-specific semantic preference flips from response
order while resolved references remain stable. If this fails, archive 038 as
non-identifiable; if it passes across families, KEEP the original question with a late-
selection answer and pursue the locus of response-time construction.

## R3 — response-list order as a mechanism-derived behavioral test

Question:
If the model has not committed to one semantic referent at the pronoun and constructs a winner
during response comparison, should the answer interface influence unresolved references much
more than resolved references?

Experiment:
On the held-out semantic split, keep each discourse and question fixed while evaluating every
permutation of the displayed candidate list. ClearRef rows receive both list orders and
SharedRef rows all six orders. Score the same candidate strings regardless of their displayed
position. Run Llama-3.1-8B-Instruct and Qwen3-8B. ClearRef is the hard specificity control:
generic list bias may change margins, but should not change an already resolved referent.

Prediction:
Late response-time selection predicts frequent licensed-candidate preference flips for
SharedRef, a significant list-order margin effect, and a much smaller flip rate for ClearRef.
An already committed semantic winner predicts stability in both conditions.

Result:
The panel gate passed in both families. Llama ClearRef accuracy was 0.955 and only 0.045 of
resolved discourse rows flipped across candidate-list orders; SharedRef both-candidate
coverage was 0.787 and 0.310 flipped their licensed-candidate preference, an ambiguity-
specific gap of 0.265. Qwen ClearRef accuracy was 1.000 with zero flips; SharedRef coverage
was 0.813 and preference flips were 0.324. The list-order margin effect excluded zero in both
models, although its direction differed: -0.395 logits for Llama and +5.679 for Qwen.

Interpretation:
Unresolved-reference behavior is not a stable hidden winner merely revealed by forced choice.
The semantic winner is unusually susceptible to the later response interface, whereas the
same manipulation leaves resolved referents behaviorally stable even when it shifts their
confidence. Together with the same-layer causal dissociation—null at the pronoun, positive at
the final decision—this supports a late-selection architecture. It rejects the clean H1
parallel-alternatives signature and weakens premature H3 commitment; H2 versus another
distributed unresolved format remains open and is not collapsed into a generic ambiguity
claim.

Next:
KEEP 038. Develop the late-selection account by localizing the transition between the pronoun
and candidate comparison with token-trajectory causal mediation, using response-order as a
causal handle and ClearRef as the preserved-capability control. A new behavioral prediction is
that removing explicit candidate comparison should sharply reduce order-dependent winner
commitment for ambiguous references while leaving clarification-seeking behavior intact.
