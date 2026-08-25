# Active Interpretability Projects

这个目录只放**已经过纸面 collision audit，值得实际运行行为 G0 的题目**。

纪律：

1. 先复用公开数据 / 原作者公开实验；
2. 第一枪只验证自然现象是否真实、稳定、规模足够；
3. 行为 G0 未通过，不做 probe / SAE / attention sweep / activation patching；
4. 不通过换弱模型、主动制造 failure、缩窄到少数特例来续命；
5. 通过 G0 后，才把状态从 `PRE-CANDIDATE` 升到 `ACTIVE-MECHANISM`。

当前项目：

- `002_facts_vs_shortcuts_arbitration/` — 实体数值比较中，模型已有可用事实但最终选择违背事实的自然 failure；先验证当前开源模型上的规模与可复现性，再决定是否进入“事实信号 vs 捷径信号仲裁机制”的因果分析。
