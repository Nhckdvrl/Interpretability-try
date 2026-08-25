# Collision Audit — Facts vs Shortcuts Arbitration

Checked: 2026-08-26

## Candidate narrative

不是“LLM 有数值知识却会犯错”，也不是“shortcut 存在”。

目标 narrative：

> 当实体数值事实与 popularity / mention-order / semantic-co-occurrence shortcut 同时可用且发生冲突时，训练完成的 LLM 如何在推理阶段仲裁两类信号？错误发生在 factual activation、comparison computation，还是 late arbitration？规模增长改善的是否是这种基于 evidence reliability 的 arbitration？

## Must-cite / must-not-overclaim papers

1. Lehmann et al. 2026, EACL Main, *Knowing the Facts but Choosing the Shortcut*  
   https://aclanthology.org/2026.eacl-long.222/

2. El-Shangiti et al. 2025, NAACL Short, *The Geometry of Numerical Reasoning: Language Models Compare Numeric Properties in Linear Subspaces*  
   https://aclanthology.org/2025.naacl-short.47/

3. Yuchi et al. 2026, EACL Short, *LLMs Know More About Numbers than They Can Say*  
   https://aclanthology.org/2026.eacl-short.47/

4. *Pretraining Data Statistics Shape the Phases of Learning Entity Comparison in Language Models* (2026, under review)  
   Training-dynamics collision, not yet inference-time arbitration collision.

## Claims currently prohibited

- “首次发现模型有数值知识但输出比较错误” — false.
- “首次发现实体数值属性在内部可读出” — false.
- “首次证明内部数值属性因果影响比较” — false.
- “首次发现 popularity / position shortcuts in entity comparison” — false.
- “首次发现 shortcut -> correct-comparison strategy transition” — too broad / unsafe.

## Claim that remains open enough for G0

- inference-time competition/arbitration between already-available factual numerical evidence and natural shortcut signals;
- failure localization across factual activation -> comparison -> arbitration;
- explaining the EACL 2026 scale effect as a difference in reliability-sensitive arbitration rather than raw factual knowledge.

## Re-audit trigger

Before any mechanism experiments, repeat search for newly released papers using at least:

- `entity comparison mechanistic interpretability shortcut`
- `numerical knowledge popularity bias activation patching`
- `factual shortcut arbitration LLM`
- `entity comparison inference mechanism shortcut factual path`
- citations / follow-ups of Lehmann et al. 2026 and El-Shangiti et al. 2025.

If a paper already performs essentially the same factual-vs-shortcut causal arbitration experiment, archive immediately.
