# 默认模型验证面板

版本：2026-08-27

## 家族门槛

核心现象必须在下列五个独立家族中至少 `3/5` 同方向成立：

| 家族 | 当前标准 checkpoint | 用途 |
|---|---|---|
| Qwen | Qwen3-4B / 8B / 32B | 三尺寸 scaling 主序列 |
| Gemma | Gemma3-4B / 12B | 第二家族与尺寸复现 |
| Phi | Phi-4-mini-instruct | 第三独立家族 |
| Llama | Meta-Llama-3.1-8B-Instruct | 第四独立家族 |
| Mistral | Mistral-Small-24B-Instruct-2501 | 第五独立家族与较强模型边界测试 |

至少一个家族必须有三个尺寸；当前默认由 Qwen3 4B/8B/32B 满足。其他家族用于检验架构与训练谱系的一般性，不要求每个家族都凑齐三尺寸。

## Llama 来源记录

Meta 官方仓库 `meta-llama/Llama-3.1-8B-Instruct` 对当前 Hugging Face 账户返回 license gate 403。因此使用公开的未量化 BF16 权重镜像：

```text
repo: NousResearch/Meta-Llama-3.1-8B-Instruct
revision: d10aef7999a2b5ba950ab3974312feeedbfe0b77
architecture: LlamaForCausalLM
weight shards: 4 × safetensors, approximately 15.8 GB total
```

核验时同时比较了 `unsloth/Meta-Llama-3.1-8B-Instruct`：四个 safetensor 分片字节大小一致，模型配置均为 Llama 3.1 8B 架构。实验必须在结果中明确写出实际 repo 和 revision，不得只写模糊的 “Llama-8B”。

## 使用原则

1. 五家族 `3/5` 是晋级门槛，不是多数投票式掩盖反例；失败家族仍须报告原始结果。
2. 某家族失败时，先区分能力地板、过度保守策略、chat template 和真实边界。
3. 跨尺寸判断看结构和 paired trajectory，不要求效应严格单调。
4. 不用量化模型作为正式基线，除非所有比较均采用同一量化方案并独立验证量化不改变 phenotype。
5. 每轮实验记录精确 revision、dtype、chat template、decoding 和 vLLM 版本。
