# 候选审计与调度注册表

版本：2026-08-28
状态：`AUTHORITATIVE`，覆盖 `00_MASTER_INDEX.md` 的历史 Tier。

## 调度结论

**当前 `READY-TO-SMOKE`：1。**

唯一授权项：

- `active/006_existential_witness_collapse` — independent N0 `PASS`，natural D0 `PASS`，40 items，20/20 manual audit，`validation_authorized: true`。

其余未同时具备独立 N0、D0 和 `validation_authorized: true` 的候选一律不运行。

## 保留的审计

- [OIR/BWA/AIC](audits/ROOT_AUDIT_OIR_BWA_AIC.md)
- [RVC](audits/ROOT_AUDIT_RVC.md)
- [ATW/CSS](audits/ROOT_AUDIT_ATW_CSS.md)
- [六领域汇总](audits/AUDIT_OIR_BWA_AIC_RVC_ATW_CSS.md)
- [MTR/DPC 首轮](audits/AUDIT_MTR_DPC.md)与[二轮](audits/SECOND_PASS_MTR_DPC.md)
- [SEC/KRE](audits/AUDIT_SEC_KRE.md)
- [UDH/MCC](audits/AUDIT_UDH_MCC.md)
- [十题第二轮对抗式 N0](audits/ADVERSARIAL_N0_TEN_2026-08-28.md)
- [006 fresh independent N0](../../active/006_existential_witness_collapse/N0_INDEPENDENT_AUDIT_2026-08-28.md)
- [006 natural D0 audit](../../active/006_existential_witness_collapse/D0_AUDIT.md)

`AUDIT_ROOT_SIX_DOMAINS.md` 是未完成占位，不作证据。

## 已杀掉 / 路由

| 范围 | 状态 | 原因 |
|---|---|---|
| OIR-01–12 | `KILLED/ROUTED` | 独立候选 0 |
| AIC-01–12 | `KILLED/OCCUPIED` | 独立候选 0 |
| ATW-01–15 | `KILLED/OCCUPIED` | 独立候选 0 |
| CSS-01–15 | `KILLED/OCCUPIED` | 独立候选 0 |
| MTR-13 | `KILLED-COLLISION` | ContractBench/TicToc exact 覆盖 |
| MTR-14 | `KILLED` | DCT/event-time 拥挤且 gold 不稳 |
| MTR-07 | `HOLD-NOT-DISPATCHABLE` | identity gold 模糊，counting 邻近过强 |
| **SEC-06** | **`KILLED-COLLISION/ROUTE`** | 2026 *Grounded Continuation* 已把 dependency-graph retraction propagation / stale-premise verification 作为核心 operator；转载链只剩外部 setting |
| **UDH-03** | **`KILLED-MOTHER-OCCUPIED`** | ACL 2026 *Mitigating Lost in Multi-turn Conversation...* 已直接研究 instruction shards 下的 solvability / abstention / multi-turn degradation；partial→full abstention 只剩 error slice |
| Sure-Thing / disjunction violation | `NOT-ADDED / DISCOVERY-OCCUPIED` | 已有工作直接用 Savage sure-thing principle 评价 ChatGPT |
| Equivalent-Quantity Decision Split | `KILLED-COLLISION` | quantity comparison / numeral-unit heuristic 机制近 exact |
| Generation–Reception Trace Asymmetry | `KILLED-MOTHER-OCCUPIED` | self-conditioning / source-monitoring 母区过密 |
| Part–Whole Double Counting | `ROUTED-F6` | local→global reducer 的标准实例，无独立 operator |
| Confidence-Conditioned Correction Relapse | `KILLED-MOTHER-OCCUPIED` | confidence-conditioned persistence/self-correction 已高度占位 |
| 审计中的其他 KILL/OCCUPIED/REJECT/MERGE/ROUTE | `KILLED/ROUTED` | 逐项理由见原审计 |

失败项保留原 ID、审计链接与致死原因，永久去重。路由项只能当 control/外部 setting。

## 当前十题

原第二轮 adversarial shortlist 详见 [`DEEP_N0_SURVIVORS_10_2026-08-28.md`](DEEP_N0_SURVIVORS_10_2026-08-28.md) 与 [`audits/ADVERSARIAL_N0_TEN_2026-08-28.md`](audits/ADVERSARIAL_N0_TEN_2026-08-28.md)。

除 006 外，表中的 survivor 仍只通过 proposer-side adversarial search，不是 formal `N0-PASS`。006 已完成 fresh independent N0、natural D0 和授权。

| # | 题目 | 注册状态 | Active 实现 | 授权 |
|---:|---|---|---|---|
| 1 | First-Negative-Evidence Harm | `ADVERSARIAL-N0-SURVIVOR` | — | false |
| 2 | Packed–Unpacked Event Splitting | `ARCHIVED / HOLD-OPERATIONALIZATION-ARTIFACT` | [`archive/009_packed_unpacked_event_splitting`](../../archive/009_packed_unpacked_event_splitting/) | false |
| 3 | Publicness–Coordination Dissociation (SEC-01 narrow contract) | `ADVERSARIAL-N0-SURVIVOR` | — | false |
| 4 | Existential Witness Collapse (RVC-04 narrow contract) | `N0-PASS / D0-PASS / READY-TO-SMOKE` | [`active/006_existential_witness_collapse`](../../active/006_existential_witness_collapse/) | **true** |
| 5 | Inadmissible-Evidence Persistence (UDH-11 narrow contract) | `ARCHIVED / TERMINAL-HOLD-D0V3-CONTRACT` | [`archive/010_inadmissible_evidence_persistence`](../../archive/010_inadmissible_evidence_persistence/) | false |
| 6 | Habitual → Episode Actualization (NG-01 narrow contract) | `ADVERSARIAL-N0-SURVIVOR` | — | false |
| 7 | Mixed-Status Event Attraction (NG-02 narrow contract) | `ADVERSARIAL-N0-SURVIVOR` | — | false |
| 8 | Dissent → Holding Role Swap (UDH-09 narrow contract) | `ADVERSARIAL-N0-SURVIVOR` | — | false |
| 9 | Source-Discount Recovery | `ADVERSARIAL-N0-SURVIVOR` | — | false |
| 10 | Weak-Evidence Backfire | `ADVERSARIAL-N0-SURVIVOR / ACTIVE-PREFLIGHT / HARNESS-READY` | [`active/007_weak_evidence_backfire`](../../active/007_weak_evidence_backfire/) | false |

### Implementation registration and archived dispositions

`active/` 编号按项目进入 active 的先后顺序继续递增，不复用上表 shortlist 编号：

```yaml
archive/009_packed_unpacked_event_splitting:
  canonical_shortlist_number: 2
  status: ARCHIVED
  harness: HOLD-OPERATIONALIZATION-ARTIFACT
  formal_n0_verdict: null
  independent_auditor: null
  d0_verdict: HOLD
  behavioral_verdict: HOLD-OPERATIONALIZATION-ARTIFACT
  validation_authorized: false

archive/010_inadmissible_evidence_persistence:
  canonical_shortlist_number: 5
  status: ARCHIVED
  harness: TERMINAL-HOLD-D0V3-CONTRACT
  formal_n0_verdict: null
  independent_auditor: null
  d0_verdict: HOLD
  behavioral_verdict: TERMINAL-HOLD-D0V3-CONTRACT
  validation_authorized: false

active/006_existential_witness_collapse:
  canonical_shortlist_number: 4
  status: READY-TO-SMOKE
  harness: READY-r4-natural-d0
  formal_n0_verdict: PASS
  independent_auditor: GPT-5.6 Sol (fresh adversarial audit role)
  d0_verdict: PASS
  d0_items: 40
  manual_audit: 20/20 PASS
  validation_authorized: true

active/007_weak_evidence_backfire:
  canonical_shortlist_number: 10
  status: ACTIVE-PREFLIGHT
  harness: READY
  formal_n0_verdict: null
  independent_auditor: null
  d0_verdict: null
  validation_authorized: false
```

006 的授权仅覆盖冻结的 first-shot two-family smoke。跑完 Qwen3-8B + Gemma3-12B 后必须做 raw-case / capability / artifact audit 和 N1；在此之前不得扩 panel、跑 scaling 或进入 mechanism。

## 其他未死但不准运行

历史 `SURVIVOR-UNAUDITED / FINALIST-CONDITIONAL` 中，除上表已窄化进入十强者外，仍包括 BWA-01、RVC-01、SEC-04/10、MCC-01/10/11、DPC-11、NG-03 等。它们不因旧 `PROMOTE/ADVANCE` 自动获得优先级或验证授权。

正式进入 smoke 必须补齐：

```yaml
n0_verdict: PASS
independent_auditor: <independent reviewer>
d0_verdict: PASS
validation_authorized: true
```

生成者与 novelty 签署者不得视为同一角色；任何 adversarial survivor 在独立复核中发现 exact collision、mother inclusion、自然 gold 失败或只是 F1–F9 换皮，立即 KILL/ROUTE。
