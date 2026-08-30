# 027 source and target audit

Date: 2026-08-31
Verdict: `PARK-DATA / NO MODEL CALL`

## Required fields

```yaml
natural_force_gold: pass
multi_function_question_support: pass
implied_assertion_gold: fail
source_authored_self_answer_gold: insufficient_and_unreleased
no_llm_judge_as_primary_gold: pass
anti_polarity_narrowing: would_fail_if_forced
behavior_call_authorized: false
```

## 1. SRAQ

Repository: `Abby-OGV/sraq`

Frozen audit commit:
`ee076c2306ee78207a92c0ef118932f38f7891a1`

SRAQ contains 971 Reddit examples: 384 train, 103 development, and 484
test. The audited label counts are 609 rhetorical and 362 informational.
Its eleven fields provide the question, surrounding turns, author, subreddit,
and binary force label. There is no implied answer, asserted proposition,
speaker-commitment target, stance span, or answer-to-assertion alignment.

Frozen file SHA-256 values:

- train: `8b6924cd6b3d77312f101feb22b57720ca3bb469159b57eee5f022e1b05e81ac`
- development: `228300f77b2de9a94dea050fc9cddbc1a899f3e046e1dcbd1f829f554c5942ba`
- test: `e6341cd8d613cdf44ef92228bfb050d396a788a482847a928af815b273d8f092`

SRAQ therefore supplies a legitimate contextual-force prerequisite, but no
gold for the new scientific variable.

## 2. QT30 / question-type artifact

Repositories:

- `arg-tech/aif-arg-datasets`, audited at
  `277e3912ee3d089b6f9df748caa16efa71244727`;
- `ZlataKikteva/sigdial2024-questions`, audited at
  `ae1322c23e009c5eb1488a647ab55d1fbc707556`.

The released question table contains 2,867 natural broadcast-debate
questions and three force classes:

| force | count |
|---|---:|
| Pure Questioning | 2,001 |
| Rhetorical Questioning | 393 |
| Assertive Questioning | 473 |

This passes the natural and multi-function force gates. The CSV schema has 22
columns: question text, force class, one preceding locution, a list of following
response locutions, response/argument-relation aggregate features, speaker
identity/role, and same-speaker indicators. It has no column identifying which
proposition a rhetorical question commits the speaker to.

Frozen CSV SHA-256 values:

- train (2,204 rows):
  `ed4dca43c4be9b3d3cd7cc8e0ba3f8efc0099b2155e0790730944f6d8c7bdf96`
- test (663 rows):
  `95f6e9919d93471079f7fd7e7cd9e634fc3b706861d545d43768c1e6b9a5d5c2`

### Why the AIF proposition node is not the missing gold

In IAT/AIF, the I-node aligned to a question represents the semantic content of
the interrogative. In the public DialAM fixture, for example, the pure question
`What can the panel suggest ...?` maps to the proposition
`xxx is what the panel can suggest ...`. The `Pure Questioning`, `Rhetorical
Questioning`, or `Assertive Questioning` YA-node supplies illocutionary force;
it does not add a second node containing the assertion pragmatically conveyed
by an RQ.

The neighboring response list also cannot be used as automatic implied-content
gold. In the 393 RQ rows, 182 have `same_speaker_rq=0`, 20 have the third/unknown
code, and many response lists are empty. Non-empty lists often contain a
moderator's or opponent's next turn, multiple propositions, follow-up questions,
or topic management. The artifact provides no span or graph edge selecting a
response as the questioner's implied assertion.

## 3. Natural self-answers

Špago's study of 2016/2020 US presidential debates reports 142 RQs, of which 43
(30.2%) receive 52 answers. Its qualitative answer taxonomy is valuable: some
addressor answers explicitly confirm the implied answer, while other answers
treat the RQ literally, reject or acknowledge it, or are sarcastic/ironic.

This evidence shows why “take the next utterance” is not a valid labeling rule.
The row-level annotation is not released as a machine-readable corpus, and the
paper's reported subset is a small, single-genre qualitative sample. Rebuilding
all labels from transcripts would be a new subjective annotation project, not
source-authored gold already supplied by the source.

## Cross-target audit

The audited sources jointly provide strong force labels but zero released rows
with a validated `rhetorical/assertive force + implied assertion` target pair.
Starting D0 now would require one of the forbidden moves:

1. negate polar questions and call the result the universal implied content;
2. treat any following utterance as a self-answer;
3. have an LLM or this project write the stance labels;
4. shrink the claim to an easy polar or explicit-`of course` subtype.

Each move breaks the registered ACL/EMNLP/NAACL-scale scientific object.

## Unlock condition

Reopen model calls only after obtaining or prospectively collecting a corpus
that provides:

- natural question and discourse context;
- human-validated force from at least rhetorical, assertive, and
  information-seeking functions;
- an independently annotated, text-grounded implied proposition or speaker
  commitment, with adjudication and reliability;
- explicit provenance for source-authored self-answers and negative cases where
  the following turn is not the intended answer;
- more than one genre/source and sufficient non-polar, evaluative,
  argumentative, and hybrid cases;
- a frozen train/test split that prevents source, party, and topic leakage.

Until then, the question retains scientific potential, but the public data do
not identify its central dependent variable.

## Sources

- https://aclanthology.org/2025.emnlp-main.1553/
- https://github.com/Abby-OGV/sraq
- https://aclanthology.org/2024.sigdial-1.53/
- https://github.com/ZlataKikteva/sigdial2024-questions
- https://aclanthology.org/2022.lrec-1.352/
- https://github.com/arg-tech/aif-arg-datasets
- https://revista-aef.unex.es/index.php/AEF/article/view/2281
