# 找题流程复盘：为什么验证后才发现撞车

日期：2026-08-28

## 症状

候选池增长快于审计；历史 Tier 被当验证优先级；首轮 `PROMOTE/ADVANCE` 被误读成“题已新”；exact 审计太晚；生成者自审偏松；行为发现与机制续作混线。MTR-13 首轮晋级、二轮被 ContractBench/TicToc exact collision 推翻，是标准案例。

## 修正

1. N0 前置到任何模型调用前；
2. 必查错误目的地、解离、scale law、机制接口和 appendix；
3. raw pool 不再有调度权，注册表是唯一入口；
4. 生成者与 novelty 签署者分离；
5. discovery 与 mechanism-followup 分线；
6. smoke 后立即 N1，再扩模型；
7. `KILLED/HOLD` 移出队列但永久保留证据。

## 运行验收

全文级 N0、独立复核、`why_not_a_rename`、公开数据和独立 gold、20例人工审计、注册表 `validation_authorized: true` 缺一不可。
