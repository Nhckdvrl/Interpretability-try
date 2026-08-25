# 001 — Role-Value Binding in Structured Generation

**Status:** `KILLED / ARCHIVED`  
**Archived:** 2026-08-26  
**Final verdict:** `STOP_NO_NATURAL_BINDING_FAILURE`

---

## 1. Mother question

本项目原本研究：

> 当结构化生成所需的正确值已经存在时，模型是否会把这些值绑定到错误的语义槽位；如果会，错误究竟发生在值提取、角色理解、角色—值绑定，还是最终序列化阶段？

典型例子：

```text
Tokyo -> origin
Osaka -> destination
```

却生成：

```json
{"origin": "Osaka", "destination": "Tokyo"}
```

题目原本的优势是：BFCL 有公开数据、字段级 ground truth 和公开模型输出，因此可以在投入 hidden-state / causal analysis 前先做几乎零成本的自然行为 G0。

---

## 2. Frozen public G0

使用 BFCL V4 `simple_python`：

- 只考虑单工具样本，排除 tool-selection 混淆；
- 只保留至少两个可形成 role pair 的 eligible 样本；
- 严格 binding failure 必须满足：
  - 所需值本身已经存在/可得；
  - 不是漏参数；
  - 不是 hallucinated value；
  - 不是 unknown field；
  - 不是 tool mismatch；
  - 而是值集合基本正确、slot assignment 错误。

公开轨迹预检模型：

- Qwen3-4B
- Gemma3-4B

---

## 3. Actual result

执行环境：已有 Conda 环境 `dlm_clean`。

代码验证：

```text
unit tests: 9 passed
```

公共 BFCL V4 `simple_python` 预检：

```text
eligible samples:    174
eligible role pairs: 247

Qwen3-4B strict natural binding failures: 0 / 174
Gemma3-4B strict natural binding failures: 0 / 174
```

因此目标 mother phenomenon 在冻结的最低成本自然数据检验中没有证据。

---

## 4. STOP decision

按项目预注册的 STOP gate：

> 如果自然 role-value binding failure 太少或为零，则停止；不允许为了进入可解释性阶段主动制造 failure。

最终 verdict：

```text
STOP_NO_NATURAL_BINDING_FAILURE
```

后续以下工作全部取消：

- 本地模型重跑；
- hidden-state probing；
- SAE；
- attention-head sweep；
- activation patching / causal tracing；
- role-binding intervention；
- method development。

---

## 5. Why we do NOT continue

不能通过以下方式续命：

1. 自己合成大量 `origin/destination` swap 样本；
2. 故意诱导模型产生 binding error；
3. 换更弱模型直到出现错误；
4. 去更复杂 benchmark 中捞少数案例；
5. 把普通 parameter extraction / omission error 重新命名成 binding failure；
6. 行为现象为零后继续做 probe / SAE，希望“内部也许有东西”。

这些操作会把原问题从：

> 解释一个自然存在的结构化生成 failure

变成：

> 为了做可解释性而制造一个可解释 failure。

这不符合本仓库的选题原则。

---

## 6. What this failure taught us

这次失败信息量很高，因为几乎没有使用 GPU 就杀掉了一个原本可能需要数周机制实验的方向。

之后所有可解释性候选新增一条强约束：

> **不能只看到 benchmark 总分差或某大类错误存在，就推测目标子现象应该存在；尽可能先利用公开原始输出确认目标 failure 本身的真实样本和规模。**

同时确认以下 workflow 是有效的：

```text
paper idea
-> mother-question collision audit
-> public-data / public-output behavioral preflight
-> hard STOP gate
-> only then mechanistic analysis
```

这份项目代码保留作为以后设计 G0、错误分类和 STOP gate 的模板。

---

## 7. Archived contents

- `ORIGINAL_README.md`：项目时期原 README；
- `docs/`：详细研究方案；
- `src/`：BFCL 下载、输出解析、严格错误分类、G0 等代码；
- `scripts/`：执行入口；
- `tests/`：测试；
- `pyproject.toml`：原项目依赖与包配置。
