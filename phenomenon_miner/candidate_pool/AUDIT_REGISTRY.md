# 候选审计与调度注册表

版本：2026-08-28
状态：`AUTHORITATIVE`，覆盖 `00_MASTER_INDEX.md` 的历史 Tier。

## 调度结论

**当前 `READY-TO-SMOKE`：0。** 未同时具备独立 N0、D0 和 `validation_authorized: true` 的候选一律不运行。

## 保留的审计

- [OIR/BWA/AIC](audits/ROOT_AUDIT_OIR_BWA_AIC.md)
- [RVC](audits/ROOT_AUDIT_RVC.md)
- [ATW/CSS](audits/ROOT_AUDIT_ATW_CSS.md)
- [六领域汇总](audits/AUDIT_OIR_BWA_AIC_RVC_ATW_CSS.md)
- [MTR/DPC 首轮](audits/AUDIT_MTR_DPC.md)与[二轮](audits/SECOND_PASS_MTR_DPC.md)
- [SEC/KRE](audits/AUDIT_SEC_KRE.md)
- [UDH/MCC](audits/AUDIT_UDH_MCC.md)

`AUDIT_ROOT_SIX_DOMAINS.md` 是未完成占位，不作证据。

## 已杀掉

| 范围 | 状态 | 原因 |
|---|---|---|
| OIR-01–12 | `KILLED/ROUTED` | 独立候选 0 |
| AIC-01–12 | `KILLED/OCCUPIED` | 独立候选 0 |
| ATW-01–15 | `KILLED/OCCUPIED` | 独立候选 0 |
| CSS-01–15 | `KILLED/OCCUPIED` | 独立候选 0 |
| MTR-13 | `KILLED-COLLISION` | ContractBench/TicToc exact 覆盖 |
| MTR-14 | `KILLED` | DCT/event-time 拥挤且 gold 不稳 |
| MTR-07 | `HOLD-NOT-DISPATCHABLE` | identity gold 模糊，counting 邻近过强 |
| 审计中的 KILL/OCCUPIED/REJECT/MERGE/ROUTE | `KILLED/ROUTED` | 逐项理由见原审计 |

路由项只能当 control/外部 setting。

## 未死但不准运行

`SURVIVOR-UNAUDITED / FINALIST-CONDITIONAL`：BWA-01、RVC-01；RVC-04 WATCH；SEC-01/04/06/10；UDH-03/09/11；MCC-01/10/11；DPC-11、NG-01/02/03。

它们必须补齐独立 N0、`why_not_a_rename`、D0 和 20例抽样。首轮 `PROMOTE/ADVANCE` 不继承验证授权。所有 `HOLD/WATCH` 默认不分发。

```yaml
n0_verdict: PASS
independent_auditor: <name>
d0_verdict: PASS
validation_authorized: true
```

失败项保留原 ID、审计链接与致死原因，永久去重。
