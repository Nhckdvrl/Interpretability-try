# 028 source and matched-population audit

Date: 2026-08-31
Verdict: `PARK-ARTIFACT / NO MODEL CALL`

## Required fields

```yaml
FrECI_paper_schema: pass
human_label_provenance: pass_in_paper
official_row_level_artifact: unavailable
same_cause_effect_pair_across_frames: not_countable
different_frame_matched_clusters: not_countable
language_source_cluster_independence: not_countable
second_source_with_both_axes: absent
behavior_call_authorized: false
```

## 1. What the paper establishes

Zhao et al. define each target-specific framed causal assertion as

```text
(cause event, effect event, source type, epistemic modality,
 responsibility target, framing effect)
```

The framing effects are Credit, Blame, Undermine Credit, Exonerate Blame,
and Neutral. The paper reports 51 politically contentious topics, 661
documents, 5,520 event mentions, 2,203 causal relations, and 4,775
responsibility-target annotations. English contributes 845 relations, Chinese
source articles translated into English contribute 1,244, and Arabic source
articles translated into English contribute 114.

The annotation provenance passes at the paper level. Three computational
linguistics annotators used a two-pass verify-and-refine workflow; 20% of topics
were double annotated and disagreements were adjudicated. Reported agreement is
0.65 pairwise link F1 for causal links, 0.71 span F1 for targets, and Cohen's
kappa of 0.62/0.74/0.88 for framing/source/modality.

Audited paper SHA-256:
`4e7450dd10ba7f94523856a3c032b72771bd6f1b229f9908ebb7250e6f6040ea`.

## 2. The reported alignment is not yet the required match

The paper reports 756 cross-document event-coreference chains, 569 of them
non-singleton. Its quantitative analysis groups relations by a shared **effect**
cluster and measures entropy over competing **cause** clusters. Eligible
outcomes have at least two causal relations and average causal fragmentation is
0.44.

This is valuable evidence of contested causal explanation, but it does not
count the registered 028 money contrast:

```text
same cause cluster -> same effect cluster
causal relation held across documents
responsibility target or framing effect differs
```

The paper's Figure 1 instead illustrates one shared effect (airstrikes) with
different causes (rocket fire, occupation/blockade, and regional
developments). Such units are appropriate `causality + frame both vary`
controls, not `causal core held / frame varies` treatment pairs. Neither the
paper tables nor appendix report the number of repeated cause-effect cluster
pairs, the number with divergent frame labels, or their topic/source/language
distribution.

The 2,203 total relations therefore cannot be used as the D0 sample count.

## 3. Official artifact availability

The ACL paper states that data and code are public at
`https://github.com/jinzhao3611/freci`. On 2026-08-31:

- the repository URL and GitHub repository API both returned 404;
- the author's GitHub account existed and exposed 22 public repositories;
- the complete public-repository listing did not contain `freci` or another
  repository advertising the FrECI artifact.

Without row-level documents, event/coreference IDs, links, targets, and frame
labels, the required matched-cluster audit is not reproducible. A model run
cannot be frozen from aggregate counts or examples in a PDF.

## 4. Breadth / second-source audit

The most plausible public complements split the two targets rather than
joining them:

- Causal News Corpus provides causal sentence/link and cause/effect-span gold,
  but no responsibility target or blame/credit frame.
- Media Frames Corpus provides issue-generic frame spans, document-level
  primary frame, and tone, but no aligned event cause-effect relation or
  responsibility target.
- Gun Violence Frame Corpus provides expert headline focus/theme labels, but no
  event-causal pair and no blame/credit target attached to that pair.

They can later validate one axis or serve as auxiliary controls. None can
replace FrECI for the paired scientific object, and concatenating them would
confound dataset identity with the causal-versus-responsibility axis.

## Stop rationale

Running now would require one of the forbidden substitutions:

1. treat shared-effect/different-cause examples as a stable causal core;
2. infer frame labels from sentiment or explicit blame words;
3. construct one axis from FrECI examples in the PDF and the other from an
   unrelated corpus;
4. shrink the study to a few hand-transcribed examples.

The failure is artifact-level and matched-population-level, not a negative
scientific result.

## Unlock condition

Reopen when the official row-level artifact becomes accessible and a frozen
audit confirms:

- canonical cross-document cause and effect cluster identifiers;
- enough repeated cause-effect cluster pairs across independent documents;
- frame or responsibility divergence within those repeated pairs;
- controls where cause-effect pairs genuinely differ;
- cluster-level support across topics and at least two source-language origins;
- topic/event/actor-disjoint splits and an explicit-blame lexical control;
- a documented confirmation source or an appropriately scoped
  contested-political-narrative claim.

Only after those counts are committed may a four-family capability D0 run.

## Sources

- https://aclanthology.org/2026.acl-long.2173/
- https://github.com/jinzhao3611/freci
- https://github.com/tanfiona/CausalNewsCorpus
- https://github.com/dallascard/media_frames_corpus
- https://derrywijaya.github.io/GVFC.html
