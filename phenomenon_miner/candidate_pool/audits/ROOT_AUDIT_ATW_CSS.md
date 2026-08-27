# ATW / CSS novelty-first 淘汰审计

日期：2026-08-28。范围 30 张卡。结论：**0 个进入优先行为队列**。

## ATW（15 → 0）

| 卡 | 裁决 | 决定性理由 |
|---|---|---|
| ATW-01 | OCCUPIED | runtime tool failure recovery 已有 Failing Tools、FailureAtlas 等大量工作 |
| ATW-02 | KILL | stale success substitution 是一般 state tracking，缺少独特 signature |
| ATW-03 | KILL | omitted parameter 被旧值补回接近 slot carryover/API argument tracking |
| ATW-04 | KILL | 同名对象读写错位是 entity resolution |
| ATW-05 | OCCUPIED | Memory Provenance Laundering 已研究记忆重写后的 authority amplification |
| ATW-06 | OCCUPIED | Guardrails as Scapegoats 直接包含 HTTP 200 + empty/null/malformed semantic failure |
| ATW-07 | OCCUPIED | partial success/completion 已是 agent task-success evaluation 核心类别 |
| ATW-08 | OCCUPIED | retry、idempotency、duplicate side effects 是 recovery/transaction benchmark 中心问题 |
| ATW-09 | OCCUPIED | semantic rollback、memory rollback、KV-cache rollback 已正面命中 |
| ATW-10 | KILL | preview/dry-run→actuality 是 event actuality 的应用 |
| ATW-11 | KILL | canceled pending result 更像 framework race/协议缺陷，难证明是 LM 内部普遍现象 |
| ATW-12 | OCCUPIED | empty result→false 是 open/closed-world 与 agentic abstention |
| ATW-13 | KILL | read-only→world change 是 event actuality/tool semantics |
| ATW-14 | OCCUPIED | compensation/rollback 后 stale failure 已被 rollback repair 覆盖 |
| ATW-15 | KILL | path-dependent trust 规范不清，prompt 容易定义现象 |

关键正面碰撞：

- [Memory Provenance Laundering](https://arxiv.org/abs/2607.29167)；
- [Guardrails as Scapegoats](https://arxiv.org/abs/2607.19449)；
- [ChronoMem](https://arxiv.org/abs/2607.27773)；
- [Aborted but Not Forgotten](https://arxiv.org/abs/2608.15939)；
- [ACRFence](https://arxiv.org/abs/2603.20625)。

这些卡在 2025 年可能有空间，到 2026-08 已不该优先投入。

## CSS（15 → 0）

| 卡 | 裁决 | 决定性理由 |
|---|---|---|
| CSS-01 | OCCUPIED | Semantic Conflicts 已做 misleading comments vs executable code 的多模型机制 |
| CSS-02 | OCCUPIED | Validation Evidence 已量化 passing tests 缺乏 bug-discriminating evidence 仍触发 closure |
| CSS-03 | OCCUPIED | no-op/incorrect patch 被视为修复属于 repair validation 主问题 |
| CSS-04 | KILL | exception path 是一般 code reasoning |
| CSS-05 | KILL | scope shadowing 是基础程序语义测试 |
| CSS-06 | KILL | value equality/object identity 是基础 alias 语义 |
| CSS-07 | KILL | alias propagation 同上 |
| CSS-08 | OCCUPIED | deleted/stale API 是 repository evolution 与 code maintenance 常见问题 |
| CSS-09 | OCCUPIED | rollback state 已被 Agent/系统工作正面占位 |
| CSS-10 | KILL | unreachable code 是基本 execution reasoning benchmark |
| CSS-11 | OCCUPIED | CodeJudgeBench 与 Semantic Conflicts 已覆盖名称/注释和执行证据冲突 |
| CSS-12 | KILL | later-definition resolution 是基础语言语义 |
| CSS-13 | KILL | shallow-copy alias 是基础程序状态题 |
| CSS-14 | OCCUPIED | patch completeness 已被 SWE-bench+、ContractEval 与 repair validation 包含 |
| CSS-15 | OCCUPIED | old/new API schema use 是 codebase evolution 与 stale-context 子类 |

最接近工作：[A Mechanistic Lens on Semantic Conflicts](https://arxiv.org/abs/2607.05587)、[CodeJudgeBench](https://aclanthology.org/2026.acl-long.888.pdf)、[ContractEval](https://aclanthology.org/2026.findings-acl.2112/)、[Validation Evidence in LLM Repair Agents](https://arxiv.org/abs/2607.28871)、[TestCase-Eval](https://aclanthology.org/2025.acl-short.82/)、[SWE-Bench+](https://openreview.net/pdf?id=DmUaCItx3J)。

## 流程教训

旧索引让“自然、可测、能写两个机制”先于 exact collision，导致 ATW-05、CSS-02、ATW-09 排得过高。以后固定为：

```text
先写最近工作和 decisive contrast
→ 不能用一句非领域差异说清空位，直接淘汰
→ 只有 surviving candidate 才审数据
→ 数据与 gold 冻结后才调用模型
```
