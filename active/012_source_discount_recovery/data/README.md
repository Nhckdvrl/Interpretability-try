# D0 materialization — Source-Discount Recovery

No `frozen_d0.jsonl` is signed yet. The primary source is NetEaseCrowd (CC BY-SA 4.0); the builder expects the released CSV schema and performs task-ID-disjoint calibration/validation before selecting any worker pair.

For NetEaseCrowd, concatenate the released partitions and run:

```bash
python data/build_natural_d0.py \
  --csv /path/to/NetEaseCrowd.csv \
  --dataset-name NetEaseCrowd \
  --license 'CC BY-SA 4.0' \
  --source-url 'https://github.com/fuxiAIlab/NetEaseCrowd-Dataset' \
  --domain-col capability \
  --task-col taskId \
  --taskset-col tasksetId \
  --worker-col workerId \
  --truth-col truth \
  --answer-col answer \
  --time-col completeTime \
  --min-per-class 20 \
  --pairs-per-domain 4 \
  --out data/candidate_netease_d0.jsonl
```

This output is only a **candidate D0**. Do not rename it `frozen_d0.jsonl` and do not authorize model calls until it contains at least 20 globally source-disjoint scenarios across at least two capabilities and the fixed 20-row manual audit passes.
