# Interpretability Try — Role–Value Binding in Structured Generation

这个仓库用于验证一个**候选研究问题**，目前还不是已经成立的课题：

> **当大模型在结构化生成中拿到了正确的值，却把值填进了错误的语义槽位时，错误究竟发生在值提取、角色理解、角色—值绑定，还是最终序列化阶段？**

第一阶段只做一个非常便宜、可以直接杀题的预检：在公开 BFCL V4 数据和官方公开模型输出中，寻找严格定义的**自然角色—值绑定错误**。如果这类错误太少或集中在个别 API，本题停止，不造新 benchmark 续命。

详细方案见 [`docs/RESEARCH_PLAN.md`](docs/RESEARCH_PLAN.md)。

## 当前状态

`PRE-CANDIDATE / PUBLIC-DATA PREFLIGHT`

- 不把“工具参数会出错”当 novelty；这已经有大量行为研究。
- 不把“role-filler binding 存在”当 novelty；这是经典问题，2026 年也已有 LLM 内部绑定工作。
- 真正待验证的叙事是：**自然结构化生成错误发生在哪一个计算阶段，以及这种诊断能否导出针对性的修复方法。**
- 在自然错误数量过门槛之前，不做 SAE、不扫 attention head、不做大规模自造数据。

## 冻结数据版本

BFCL 官方当前榜单声明使用提交：

```text
ShishirPatil/gorilla
f7cf7359b7ac615a0b294831c5ba2bc95ee4a000
```

BFCL 官方结果归档冻结为：

```text
HuanzhiMao/BFCL-Result
6830ed13035c0cfee9aa7a9a0ffed70f10b3dd50
snapshot: 2025-12-16
```

这样不会因为 BFCL 后续修改数据或结果文件导致 G0 漂移。

## 零 GPU 第一枪

### 1. 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. 一键跑公开结果预检

```bash
bash scripts/run_public_g0.sh
```

脚本会：

1. 下载 pinned BFCL `simple_python` 测试集和答案；
2. 在看模型输出之前筛出严格的 binding-eligible 样本；
3. 下载 BFCL 官方归档中的 Qwen3-4B 与 Gemma-3-4B 输出；
4. 自动诊断错误类型；
5. 只把“正确工具 + 正确 schema keys + 所有值来自正确值集合 + 值只是绑定到错误角色”计为 `strict_natural_binding`。

### 3. 如果需要本地复现 Qwen

只有公开轨迹证明现象值得继续时才跑：

```bash
bash scripts/run_local_qwen.sh
```

默认模型：

```text
Qwen/Qwen3-4B-Instruct-2507
```

只跑预先筛出的 eligible IDs，greedy decoding，不浪费 GPU 在与绑定问题无关的样本上。

## 主要命令

```bash
binding-fetch
binding-scan
binding-official
binding-infer
binding-classify
```

示例：

```bash
binding-fetch --category simple_python --out-dir data/bfcl

binding-scan \
  --data data/bfcl/BFCL_v4_simple_python.json \
  --answers data/bfcl/BFCL_v4_simple_python_answers.json \
  --out artifacts/eligible_simple_python.jsonl

binding-official \
  --model-dir Qwen_Qwen3-4B-Instruct-2507-FC \
  --out artifacts/qwen3_4b_official.jsonl

binding-classify \
  --data data/bfcl/BFCL_v4_simple_python.json \
  --answers data/bfcl/BFCL_v4_simple_python_answers.json \
  --outputs artifacts/qwen3_4b_official.jsonl \
  --out artifacts/qwen3_4b_diagnosis.jsonl
```

## 严格自然绑定错误定义

一个样本只有满足以下条件，才允许进入当前 G0：

- BFCL `simple_python`：输入只提供一个工具，先去掉 tool selection 混淆；
- 至少两个**必填**参数；
- 两个参数 schema type 相同；
- 两个正确值不同；
- 每个正确值都有一个 BFCL 接受值以独立 literal 明确出现在用户问题中；
- 模型调用正确工具；
- required keys 全部存在，没有未知 key；
- optional field 若输出，也必须正确；
- required values 必须是 ground-truth values 的一一置换；
- 错误置换发生在预先定义的 eligible role pair 内。

因此以下错误**不算** binding：

- 工具选错；
- 漏参数；
- 参数名 hallucination；
- 值本身算错/抽错；
- 默认参数不一致；
- 单位转换；
- 推导型参数；
- 不同类型参数之间的偶然数值混淆。

## 测试

```bash
pytest -q
```

当前单元测试覆盖：Qwen `<tool_call>`、BFCL prompt-mode Python-like call、literal 边界、strict eligibility、纯 swap、非 binding value error、跨类型反例和 eligible-ID 读取。

## 原则

如果公开现有数据上没有足够的自然 binding failure：**STOP**。

不做：

- 先生成几千条 origin/destination 合成数据把现象造出来；
- 为了得到结果不断换错误定义；
- 看到某层 probe 很高就反过来定义 construct；
- 自然 failure 不成立后改做“某个 API 的 binding circuit”。

如果现象通过预检，再进入 [`docs/RESEARCH_PLAN.md`](docs/RESEARCH_PLAN.md) 中的表示与因果阶段。
