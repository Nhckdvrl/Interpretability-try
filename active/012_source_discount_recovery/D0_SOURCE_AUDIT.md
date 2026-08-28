# D0 source audit — Source-Discount Recovery

Date: 2026-08-29  
Verdict: `D0-AUDITING` — **source pool is valid, frozen scenario set not yet signed**.

The point of this audit is to prevent a common shortcut: assigning a source a verbal “high/low reliability” label without a real history from which the report-specific likelihood ratios can be calculated.

## Primary source candidate: NetEaseCrowd

- real production crowdsourcing platform data
- about 2,413 workers, about 1M tasks, about 6M annotations
- worker ID, task ID, task-set ID, answer, truth, timestamp, capability are released
- all sensitive IDs are anonymized
- license: **CC BY-SA 4.0**
- public GitHub / Hugging Face release

This is a strong natural source because source credibility is an empirical worker property, not a prompt adjective.

### Required derivation

For each capability / task family and each selected pair of truth labels:

1. split by **task ID**, not annotation row, into fixed 60% calibration / 40% held-out tasks;
2. retain all worker responses in denominators, including a third-class response in a 3-way task;
3. compute per-worker report-specific LRs with Jeffreys smoothing:

```text
LR_target(report target) = P(report target | truth target) / P(report target | truth other)
LR_other(report other)   = P(report other  | truth target) / P(report other  | truth other)
```

4. require both source workers to be above chance on calibration and validation;
5. require the same high-vs-low ordering in both directions on both splits:

```text
1 < low_target_lr < high_target_lr
0 < high_other_lr < low_other_lr < 1
```

6. use each worker in at most one frozen scenario to reduce source-level pseudoreplication;
7. never use the target task's gold label in the model prompt.

`data/build_natural_d0.py` implements this extraction contract and was unit-tested on a task-disjoint fixture before commit.

## Second source candidate: CIFAR-10H

- raw annotator-level human labels for the 10,000 CIFAR-10 test images
- each anonymized annotator has about 200 normal trials plus attention checks
- raw release contains annotator ID, true category, chosen category, true/chosen labels, correctness, and image index
- license: **CC BY-NC-SA 4.0**

CIFAR-10H is useful as a genuinely different source domain. Binary class-pair slices can be calibrated exactly as above, using task/image-disjoint splits. It should not be mixed into a formal frozen set until worker histories for the chosen class pairs satisfy both directional LR constraints on the held-out split.

## Rejected / lower-priority sources

### Toloka Relevance-2

Scientifically attractive (hundreds of thousands of real binary relevance votes with worker IDs and partial gold), but a clear redistributable dataset license was not established in this audit. It is therefore not used for the formal D0 despite fitting the statistical design.

### RTE crowd annotations

The public reprocessed files expose worker IDs, responses and gold and are useful for code checks, but the underlying RTE/crowd-annotation redistribution chain is less clean than NetEaseCrowd/CIFAR-10H. It is not the first-choice formal source.

## Delay-material rule

Delay is not allowed to be arbitrary lorem ipsum. The builder must draw source-neutral administrative metadata from unrelated tasks: task IDs/task-set IDs/timestamps from other annotators, with no current message, truth label, high/low source identity, or class-diagnostic content. Short and long blocks differ only in the number of unrelated records.

Source reinstatement may restore source identity and the frozen calibration profile, but may not repeat the source's message. The matched-length control may restore only record/protocol context.

## Why D0 is not signed yet

A dataset card is not enough. Before `validation_authorized` can become true, the actual downloaded source version must be frozen and the builder must produce at least 20 disjoint worker-pair scenarios spanning at least two real task domains, followed by a 20-row manual audit of the resulting LR tables and prompts.

Until that exists, `D0-AUDITING` is the correct state.
