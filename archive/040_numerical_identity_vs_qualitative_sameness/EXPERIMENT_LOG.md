# Experiment Log

## S0 — behavioral identity double dissociation

Question:
Can the primary AR models transfer token-specific event history according to numerical
identity while preserving knowledge that two numerically distinct objects have the same type?

Experiment:
Use all 31 released Davis–Altmann event frames. Cross identity (`same token` vs `different
token, same type`), state-change magnitude (`minimal` vs `substantial`), and two surface cue
families (released determiner cues vs an explicit continuity paraphrase). Score two
label-counterbalanced semantic alternatives (`A`/`B`) for an identity/history question and a
same-type control without an LLM judge. Counterbalancing was added after a discarded pilot
showed a strong `Yes` response bias; no pilot result is used as evidence.

Prediction:
An identity-sensitive model gives positive history margins for SAME_TOKEN and negative
margins for DIFFERENT_TOKEN_SAME_TYPE in both cue families, while answering the type
question `Yes` in both identity conditions. A determiner shortcut fails on the held-out
continuity paraphrase. A generic semantic/coreference disruption changes history and type
readouts together.

Result:
The first counterbalanced implementation (`s0_v2`) passed the released determiner identity
cells but failed the held-out continuity cells in both model families. Qwen3-8B obtained
97.6%/64.5% SAME/DIFFERENT accuracy on the released family, versus 100%/16.9% on the
continuity family. Llama-3.1-8B obtained 91.9%/62.1%, versus 100%/18.5%. Frame-bootstrap
identity-effect intervals excluded zero in every family, but that contrast was driven by
graded margins and did not establish the required bidirectional decisions. Qwen preserved
same-type knowledge (99.4%); Llama's type readout was strongly cue-family dependent.

Audit of `s0_v2` found a deterministic measurement defect: the DIFFERENT continuity bridge
introduced a distinct but otherwise unnamed item and then the next event used `the <noun>`,
which naturally reselected the original named referent. This makes the bridge and final noun
phrase compete. Because the defect was semantic rather than an unfavorable effect, one
frozen repair (`s0_v3`) replaces the final noun phrase with `that item` after the bridge in
both identity conditions. The released family, all frames, questions, models, and gates stay
fixed. No further prompt repair is allowed based on outcome.

Interpretation:
The released-family result establishes local sensitivity to the original determiner contrast,
but `s0_v2` cannot establish cross-surface numerical identity and therefore does not license
representation or causal experiments. The graded positive identity contrast alone is not
enough: the models must correctly reject history transfer for distinct same-type objects.

The once-repaired `s0_v3` removed the semantic conflict without changing the released
family. Qwen3-8B passed: released SAME/DIFFERENT accuracy was 97.6%/64.5%, clean-continuity
accuracy was 100%/100%, type-control accuracy was 99.4%, and the type identity-effect was
only 6.7% of the mean history identity-effect. Llama-3.1-8B passed both history families
(released 91.9%/62.1%; continuity 100%/100%) but failed the type-control denominator at
50.8%, so it is not licensed for the identity-specific causal claim.

Next:
Proceed only with Qwen3-8B to a controlled arbitrary-history microscope and cue-family-
disjoint identity readout. Llama is stopped at a mixed behavioral result. The next experiment
must manipulate token-specific history while preserving type knowledge; a direct identity
classifier or a replication of `the` versus `another` is insufficient.

## S1 — arbitrary history, binding order, and competitor type

Question:
Does the Qwen checkpoint that passed direct identity judgments actually use numerical
identity to inherit an arbitrary episode-specific property, or can a binding-recency
shortcut override identity while shared type knowledge remains intact?

Experiment:
For all 62 released event rows, introduce Object Alpha and Object Beta with arbitrary codes
DAX/VEK, make the first event involve Alpha, and make the second event involve either the
same Alpha or a distinct Beta. Cross explicit labels vs continuity-description cues,
minimal vs substantial state change, and both orders of the two initial entity→code binding
sentences. A further frozen control changes Beta from the same released object type to the
next frame's different object type. A/B answer labels are counterbalanced. The history
readout asks for the later referent's code; the specificity control asks its object type.

Prediction:
Numerical-identity use predicts stable code inheritance across binding order. A last-binding
heuristic predicts a crossover: SAME succeeds when Alpha→DAX is introduced last, DIFFERENT
succeeds when Beta→VEK is introduced last. If same-type similarity causes the collapse,
the crossover should substantially weaken with a different-type competitor; a generic
binding-recency account predicts persistence.

Result:
The first Alpha-first panel revealed the predicted asymmetry and motivated the mandatory
order control: history accuracy was 62.1% for explicit labels and 84.7% for continuity,
while type accuracy was 100%.

With both binding orders, the crossover was decisive. For same-type competitors, target-code
accuracy was 97.8% when its entity→code binding appeared last and 34.3% otherwise. Explicit
SAME rose from 24.2% (Alpha bound first) to 100% (Alpha bound last), while explicit
DIFFERENT fell from 100% (Beta bound last) to 38.7%. Continuity DIFFERENT fell from 100% to
3.2%. State-change magnitude did not remove the pattern.

The different-type control did not eliminate it: target-last accuracy was 98.4% and
target-not-last accuracy 47.6%. Some cells improved (e.g. explicit DIFFERENT with Beta bound
first, 38.7% -> 68.5%), but continuity DIFFERENT with Beta bound first remained 4.8%.
Type-control accuracy over the expanded panel was 96.1%. The frozen S1 gate failed.

Interpretation:
Qwen can explicitly classify SAME versus DIFFERENT in the natural S0 window, but that
knowledge does not robustly govern arbitrary token-specific history. The code associated in
the last initial binding sentence dominates later retrieval even though Alpha is mentioned
again in the first event, and even when the competitor has a different type. This is closer
to generic property-binding recency than to qualitative-similarity interference. It is a
specific dissociation—identity judgment and type knowledge survive, numerical-identity-based
history inheritance does not—rather than generic task failure.

Next:
Stop identity-direction steering because its behavioral recipient fails the frozen causal
denominator. The strongest 040 result is currently local identity sensitivity without robust
causal history use, plus a mechanism-derived binding-order crossover. A future continuation
should test whether an independently established binding mechanism overwrites identity; it
must not narrow the headline to a recency or Object-Alpha benchmark paper.

## S2 — content-preserving binding-order causal transplant

Question:
Is the behavioral last-binding crossover controlled by a causally active binding-order state,
or is order only correlated with the eventual history decision?

Experiment:
On six frame-held-out Qwen3-8B templates, replace the layer-18 residual at the end of the
second entity-to-code introduction with the exact state from the opposite introduction order.
The donor has identical entities, codes, events, questions, and answer mapping; only the two
binding sentences are swapped. Compare against an equal transition from another frame and a
matched-norm random vector. Aggregate both A/B label orders and retain the type readout.

Prediction:
If this boundary state carries the order trace that later overrides identity, the same-item
transplant should move HistoryTransferLogit toward the clean opposite-order decision more
than shuffled and random controls, while TypeKnowledge accuracy remains intact.

Result:
The prespecified causal gate failed. Across 192 label-aggregated history contrasts, the real
transplant moved *away* from the clean opposite-order decision by -0.206 logits (frame-
bootstrap 95% CI [-0.292, -0.135]). Shuffled order deltas were -0.155 and random vectors
-0.051; real-minus-shuffled was -0.051 [-0.078, -0.025]. Clean type accuracy was 0.974 and
remained 0.969 under the real transplant.

Interpretation:
Binding order robustly predicts behavior, but its causal carrier is not the single
prespecified middle-layer state at the end of the second binding sentence. The preserved type
control makes this an intervention-specific null rather than generic damage. Searching nearby
layers or coefficients would be post-hoc rescue. The broader identity question still has one
orthogonal, higher-information test: whether the cross-surface numerical-identity state from
S0 transfers causally into the S1 history decision. This directly tests the original causal
contract rather than continuing to localize generic recency.

Next:
Run S3 once at the same fixed layer: train identity on released-determiner discovery frames,
require transfer to held-out continuity-description frames, then intervene on held-out S1
history and type readouts. KEEP only if the identity direction is abstract and causally
specific; otherwise archive 040 rather than pivoting to a binding-recency paper.

## S3 — cross-surface identity state and cross-task causal use

Question:
Does the Qwen checkpoint contain an abstract numerical-identity state that transfers across
surface formulations and controls arbitrary history inheritance?

Experiment:
At the same fixed layer 18, fit a balanced linear identity direction on the natural released-
determiner family using 25 discovery frames. Test it without refitting on six held-out frames
expressed only through continuity descriptions. Then add or subtract one discovery projection
SD at the final decision state of the independently constructed S1 code-history task. Compare
with shuffled-label and random directions, aggregate A/B orders, and retain TypeKnowledge.

Prediction:
The frozen causal contract requires above-0.75 held-out cross-surface AUC and a bidirectional
effect: moving toward SAME should improve SAME history inheritance and impair DIFFERENT
history separation, with the reverse for moving toward DIFFERENT. The effect must exceed the
shuffled direction and preserve type accuracy.

Result:
The identity direction did not transfer across surface families: held-out AUC was 0.474 and
balanced accuracy 0.521 (48 balanced examples). On 192 label-aggregated history items, the
aligned bidirectional effect was -0.0045 logits, 95% CI [-0.0092, -0.0015], versus -0.0015
for shuffled and -0.0008 for random. Identity-minus-shuffled included zero. The result was
null both when the target binding was last and when it was not. Clean type accuracy was
0.969 and no identity intervention reduced it.

Interpretation:
Qwen's direct cross-surface identity judgments do not correspond to a shared linear identity
state at the fixed middle-layer decision readout, and that direction has no specific causal
effect on token-specific history. Together with S1 and S2, the evidence supports a behavioral
dissociation—identity answers and type knowledge coexist with order-dominated arbitrary
binding—but not the abstract identity mechanism required by 040. The remaining binding-order
effect is close to generic in-context recency/key-value interference and is too narrow and
crowded to replace the registered object.

Next:
Archive 040. Do not search layers, coefficients, or selected cue families. Reopening would
require an independently motivated representational format or model family that satisfies
the same cross-surface and history-specific causal contract.
