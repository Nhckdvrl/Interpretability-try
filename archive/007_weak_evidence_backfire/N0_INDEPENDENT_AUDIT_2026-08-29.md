# Independent N0 audit — Weak-Evidence Backfire

Date: 2026-08-29  
Role: independent collision audit, separate from the proposer-side shortlist record  
Lane: discovery

## Frozen claim

The proposed claim is that a model can correctly recognize a cue as positive evidence for `H`, while adding that cue lowers preference for `H` relative to a matched no-evidence baseline, with the same sign reversal surviving completeness, bidirectional, belief, and consequential-action controls.

## Search and full-text checks

The following exact and near-exact queries were checked on 2026-08-29: `weak evidence effect`, `when good evidence goes bad`, `positive evidence decreases belief no evidence`, `pragmatic weak evidence`, `weak evidence backfire Bayesian`, `absence of stronger evidence implicature`, and `evidence integration sign reversal`. The central papers and their available full text/abstract and citation context were checked:

1. McKenzie, Lee, and Chen, *When good evidence goes bad: The weak evidence effect in judgment and decision-making* (2011), [ScienceDirect record](https://www.sciencedirect.com/science/article/abs/pii/S0010027711000394). The abstract reports the decisive contrast: weak positive evidence produced lower judgments than no evidence, although the evidence was separately judged supportive.
2. Hahn and Oaksford, *A Pragmatic Account of the Weak Evidence Effect* (2022), [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC9692057/) and [arXiv version](https://arxiv.org/abs/2112.03799). This formalizes the weak-evidence backfire as pragmatic reasoning about persuasive speakers and explicitly treats the decrease after weak favorable evidence as the target effect.
3. Pratkanis, Greenwald, Leippe, and Baumgardner, *In Search of Reliable Persuasion Effects: III. The Sleeper Effect Is Dead: Long Live the Sleeper Effect* (1988), [OpenAlex record](https://openalex.org/W2061544316), checked as a citation-chain neighbor because the weak-evidence literature distinguishes pragmatic backfire from source/argument discounting.

## Mother inclusion test

Removing the proposed diagnostics, domain, model family, and downstream action leaves the already reported weak-evidence effect: supportive weak evidence can lower belief relative to no evidence. The project’s completeness and bidirectional controls are useful for a cleaner replication or mechanism follow-up, but they do not make the discovery behavior new. The 2022 pragmatic account also supplies a direct alternative explanation for the exact sign reversal: the listener infers that a persuasive speaker would have presented stronger evidence if it were available.

## Decision

`KILLED-COLLISION` for the discovery lane. This is not a claim that the frozen harness is invalid, nor a claim that the proposed controls are useless. It is a collision kill because the mother behavior that the harness is designed to discover is already an established named phenomenon and has an explicit pragmatic account.

The additional consequential-action and completeness factors would require an explicitly authorized mechanism-followup study; they cannot be used to relabel the same behavior as a new natural phenomenon under the repository’s discovery rules.

## Why not a rename

“Weak-evidence backfire”, “weak evidence effect”, and “when good evidence goes bad” describe the same sign reversal. Changing the readout from belief to action, adding a second evidence direction, or adding a completeness control changes the measurement package, not the mother phenomenon.

## D0 disposition

No natural D0 was constructed or model-run. The project is stopped at N0 collision; `validation_authorized` remains `false`.

