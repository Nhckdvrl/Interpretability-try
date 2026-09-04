# 045 — Final Verdict

Decision: **ARCHIVE**
Date: 2026-09-04

## Registered object

Donnellan's referential/attributive distinction: whether a definite description follows the
speaker's independently selected target or the object satisfying its descriptive content, and
whether LLMs represent and causally use a context-conditioned `DescriptionUseMode` that decides
between them.

## Why it does not survive

**1. The referential effect is carried by frame wording, not by the use mode.** Within a single
condition, swapping one paraphrase moves accuracy across most of the range — Qwen 0.46 to 0.96
across three referential wordings, Phi 0.15 to 0.92 across three inferred wordings — while the
condition effect it is meant to support is smaller than that swing. A factor whose within-condition
variance exceeds its between-condition variance is not the factor doing the work.

**2. Only the default side is stable.** Attributive use is at 1.000 in every family, every frame
and every readout. Stable attributive behaviour is descriptions denoting, which nothing in the
literature disputes.

**3. Speaker reference is largely not inferred.** Removing only the clause that states whom the
speaker is talking about, while keeping the attention sentence and the false belief, drops Phi from
0.931 to 0.519 and Qwen from 0.701 to 0.609. What the explicit frames measure is following a stated
referent.

**4. The panel does not hold.** Llama fails its raw-fact denominators in every version
(speaker-target 0.506 / 0.574, entity 0.70), answers by A/B position when it does not know
(0.16 versus 0.86 by mapping), and in v6 moves in the wrong direction. Three families survive at
best, and one of those (Phi) collapses under the inference test.

**5. There is no mechanistic foothold.** The use-mode state at the description token is at layer-0
chance and at AUC 1.000 by 37.5% depth in all four families, i.e. it is fully determined by the
frame text. Nothing discriminating is left for the registered causal contract, and the attributive
side has no behavioural variance to intervene on.

## What was genuinely learned, and is recorded rather than pursued

Six rounds of stimulus repair were needed before the phenomenon appeared at all, and each round
fixed a real construction defect rather than an unfavourable result: the referential use was not
instantiated at all until the speaker's belief that the description fits their target was stated;
a disjunctive denominator question scored below chance; establishing the target descriptively
rather than by name cost two families their denominators; a bare belief assertion was absorbed as a
world fact and cost the referential condition its raw-entity accuracy until the belief was marked
false; and the apparent representation-action gap in v4 was an artifact of asking about an actor
who did not share the speaker's information state.

That last correction produced the one durable observation here, recorded for reuse rather than
developed: with the actor's information state manipulated explicitly, Qwen/Phi/Gemma give
0.803/0.743/0.812 for the speaker's own action, 0.653/0.479/0.706 for a stipulated fully-informed
assistant, and 0.463/0.206/0.481 for an uninformed third party. The models are graded by whose
information state fixes the referent, and they under-transfer the speaker's referential intention
to a third agent even when that agent is stipulated to know everything the speaker knows. If that
is ever worth a topic, it is an information-state-transfer object and must be registered on its own
terms, not as a continuation of Donnellan.

## Not done, deliberately

No further frame engineering. Six versions is already past the point where additional wording work
would be selecting for a result rather than repairing a defect.

## Correction recorded after archiving

The captured residual states were stored in float16, which overflowed to inf on Gemma-3-12B
(509 values; that model's residual stream exceeds 65504 in the middle of the stack). The probe
figure reported for Gemma in the log above is therefore unreliable. It changes nothing here: the
archive decision rests on the behavioural paraphrase variance (Qwen 0.46-0.96, Phi 0.15-0.92
within a single condition) and on the raw-fact denominators, neither of which uses those states.
The state-capture scripts now store float32; `041` re-ran its Gemma probe and causal test under the
fix.
