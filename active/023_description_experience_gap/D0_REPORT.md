# 023 D0 report — inferring risk vs valuing risk

## Verdict

```yaml
frozen_verdict: HOLD_CAPABILITY_FAILURE
mechanism_authorized: false
additional_d0_authorized: false
topic_killed: false
```

The exact-frequency behavioral prerequisite did not pass. No hidden-state,
probe, patching, attribution, or intervention work is authorized.

## Frozen design

D0 used 12 predeclared gambles from six families, two amount scales, both option
orders, three exact-frequency shuffles, and three presentation modes:
probabilities, summarized counts, and a raw 20-outcome sequence. Each of 432
scenarios had a choice query, an EV comparison, and two frequency queries. Four
pinned open families produced 1,728 records each.

## Family results

| Family | Frequency acc. | EV acc. | Dominance p(target) | Order difference | Gap vs probability | Gap vs counts | Pass |
|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen3-8B | 0.971 | 0.377 | 0.801 | 0.403 | 0.134 | 0.032 | no |
| Gemma3-12B | 0.914 | 0.363 | 0.757 | 0.411 | 0.472 | 0.015 | no |
| Llama3.1-8B | 0.770 | 0.252 | 0.579 | 0.151 | 0.202 | 0.153 | no |
| Mistral-Small-24B | 0.936 | 0.294 | 0.575 | 0.244 | 0.132 | 0.006 | no |

All four models had a positive human-direction normalized gap between explicit
probabilities and exact histories. That comparison alone would misleadingly
look like a successful replication.

The count-description control changes the conclusion. Qwen, Gemma, and Mistral
had residual history-versus-count gaps of only 0.032, 0.015, and 0.006; all
three bootstrap intervals crossed zero. The only clear residual was Llama's
0.153, but Llama failed frequency, EV, stochastic-dominance, and option-order
gates. Selecting it would be an outcome-conditioned rescue.

## Measurement and capability failures

The EV `A/B/TIE` readout showed severe candidate/position bias. Qwen predicted
`A` on 75.5% of EV trials, Gemma on 71.1%, and Mistral on 86.6%, despite gold
labels being exactly balanced. All families consequently failed the frozen EV
gate. Direct choices were also highly option-order sensitive: the mean paired
semantic-option difference ranged from 0.151 to 0.411, above the 0.10 ceiling.

Mistral's current tokenizer backend additionally warned that applying its chat
template with `tokenize=False` and then encoding can be unsafe. Its raw result
is preserved but cannot be used as sole promotion evidence. The aggregate
verdict would remain unchanged without Mistral.

## Scientific judgment

The ACL 2026 mother already owns the broad LLM description-history gap and
reasoning-versus-conversational taxonomy. D0 does not establish the stronger
object needed here: a sequence-specific divergence after exact empirical counts
and basic decision capability are controlled. Three relatively capable
families make histories and count summaries behaviorally similar; the sole
residual occurs in the family that cannot pass the prerequisite.

The topic is held rather than formally killed because the EV instrument itself
has a positional defect. Nevertheless, no bounded measurement repair is
authorized now: option-order sensitivity remains fatal, the count control
removes the effect in three families, and continuing would pressure the title
toward a Llama-only or output-format-specific result. That narrowing is
explicitly forbidden.
