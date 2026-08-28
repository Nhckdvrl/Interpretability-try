# Independent N0 audit — Source-Discount Recovery

Date: 2026-08-29  
Role: independent collision audit, separate from the proposer-side shortlist record  
Lane: discovery

## Frozen claim

The proposed claim is that a model retains source identity, source credibility, and message direction after delay, yet stops applying the credibility discount to the message; low-source influence rebounds, the high/low gap shrinks, and source metadata reinstatement restores the gap.

## Search and full-text checks

The following exact and near-exact queries were checked on 2026-08-29: `sleeper effect source credibility delay`, `source-message dissociation`, `source credibility decay persuasion`, `source memory message influence delay`, `delayed persuasion low credibility source`, `source cue reinstatement`, and `LLM source credibility memory`. The central papers and citation-chain neighbors were checked:

1. Hovland, Janis, and Kelley’s sleeper-effect line is summarized and citation-linked in Pratkanis et al., *The Sleeper Effect in Persuasion: A Meta-Analytic Review* (2001), [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC3100161/). The review describes delayed increases for messages from noncredible sources, the dissociation hypothesis, retained source recall, and weakening of the source/message association.
2. Pratkanis et al. (1988), *In Search of Reliable Persuasion Effects: III. The Sleeper Effect Is Dead: Long Live the Sleeper Effect*, [OpenAlex record](https://openalex.org/W2061544316), was checked as the foundational source/dissociation citation.
3. Kumkale and Albarracín, *How people can become persuaded by weak messages presented by credible communicators: Not all sleeper effects are created equal* (2017), [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC8157953/) and [ScienceDirect record](https://www.sciencedirect.com/science/article/pii/S0022103116303936). This work explicitly studies delayed changes in persuasion as a function of source/message accessibility and reports source- and argument-based sleeper effects.
4. Albarracín et al., *The Effects of Source Credibility in the Presence or Absence of Prior Attitudes* (2010), [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC3101500/), was checked for the high/low credibility-by-delay contrast and its distinction from ordinary source effects.

## Mother inclusion test

The proposed source state is the classic sleeper-effect dissociation in more explicit computational language. The literature already contains the decisive ingredients: low-credibility messages are initially discounted; later influence can increase; source recall can remain intact; and the proposed explanation is weakened source–message association rather than complete source forgetting. Source re-presentation at delayed testing is also part of the historical literature, so “reinstatement restores discount” is not sufficient to establish a new mother phenomenon.

The project’s directional likelihood-ratio calibration, matched same-delay no-message baselines, and selective reinstatement are valuable safeguards for an LLM replication or mechanism study. They do not remove the exact collision under the discovery-lane rules.

## Decision

`KILLED-COLLISION` for the discovery lane. The claim is a modern LLM operationalization of the established sleeper-effect/source–message dissociation family, not an unreported natural phenomenon.

## Why not a rename

“Source-discount recovery”, “sleeper effect”, “delayed persuasion from low-credibility sources”, and “source/message dissociation” differ in vocabulary and implementation, but share the same central trajectory: the source discount loses influence relative to remembered message content while source/message accessibility is dissociated over time.

## D0 disposition

No natural D0 was constructed or model-run. The project is stopped at N0 collision; `validation_authorized` remains `false`.

