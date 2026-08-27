# 候选卡统一格式

## 状态字段

```yaml
id: DOMAIN-XX
working_title: 暂时使用描述性标题，不提前给现象造名
stage: IDEA | N0-AUDITING | N0-PASS | D0-AUDITING | READY-TO-SMOKE | PILOT | N1-AUDITING | HOLD | KILLED
validation_authorized: false
priority: A | B | C
naturalness: N3 | N2 | N1
source_status: LOCAL | HUB | REMOTE | UNKNOWN
collision_risk: LOW | MEDIUM | HIGH | OCCUPIED
proposer:
independent_auditor:
n0_verdict: PASS | HOLD | KILLED-COLLISION
d0_verdict: PASS | HOLD | KILLED-DATA
why_not_a_rename:
```

`READY-TO-SMOKE` 不是作者自评：只有独立 N0、D0 均 PASS，且审计注册表设置 `validation_authorized: true` 才能使用。

`priority=A` 不表示现象成立，只表示在未测试候选中信息价值最高。

## 正文模板

```markdown
### DOMAIN-XX — 描述性标题

**一句话矛盾。** 模型明明 ______，却 ______。

**日常例子。** ______。

**为什么可能是论文题，而非普通错误。** ______。

**自然数据锚点。**
- 主数据：dataset / split / 原始任务 / gold；
- 外部确认：dataset；
- 可得性与 license：______。

**发现轴。**
- 原生进程或规范 relation：______；
- control → target：______；
- nuisance controls：______。

**只有出现以下 signature 才晋级。**
- ______；
- ______；
- 若只是平均 accuracy 小跌，则 KILL。

**规模生存理由。** ______。

**竞争机制。**
1. A：______；预测 ______；
2. B：______；预测 ______；
3. 可选 C：______。

**最近工作与可辩护空位。**
- 母现象：______；
- 最近工作：______；
- 已覆盖：______；
- 只有观察到 ______，本卡才不被其完整包含。

**最便宜的证伪。** 先 ______。若 ______，立即 KILL。
```

## 禁止写法

- “测试模型是否存在 X bias”；
- “换 12 种 prompt 看 robustness”；
- “如果掉点就是现象”；
- “可以 probe attention 看机制”；
- “似乎没人做过”；
- 没有公共数据、没有自然例子、没有强模型生存理由；
- 用一个综合分掩盖 `OCCUPIED`、关系无效或能力地板。

## 文献措辞

文献检索只能写：

```text
截至 YYYY-MM-DD，以检索式 […] 未找到完整覆盖该 signature 的工作。
```

不能写“这是全新现象”，除非行为、一般性和新颖性均完成正式审计；即使如此，也应避免绝对优先权措辞。
