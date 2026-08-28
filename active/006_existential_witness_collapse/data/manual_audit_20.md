# 006 D0 Manual Audit — 20 Random Items

Seed: `20260828`
Result: `20 / 20 PASS`

Each sampled item was checked against the source-table entry and the frozen logical/action invariants.

| scenario_id | source record | P exists | Q exists | same possible | distinct possible | identity unresolved | same ctrl | distinct ctrl | paraphrase | neutral | verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `football:denmark:2016-17` | Copenhagen — 2016–17 (denmark) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:denmark:2008-09` | Copenhagen — 2008–09 (denmark) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:belgium:1976-77` | Club Brugge — 1976–77 (belgium) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:croatia:1997-98` | Dinamo Zagreb — 1997–98 (croatia) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:finland:2017` | HJK — 2017 (finland) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:belgium:1995-96` | Club Brugge — 1995–96 (belgium) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:albania:1949` | Partizani — 1949 (albania) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:georgia:1992-93` | Dinamo Tbilisi — 1992–93 (georgia) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:trinidad:1981` | Defence Force Chaguaramas — 1981 (trinidad) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:belgium:1993-94` | Anderlecht — 1993–94 (belgium) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:belgium:1971-72` | Anderlecht — 1971–72 (belgium) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:croatia:2006-07` | Dinamo Zagreb — 2006–07 (croatia) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:albania:1958` | Partizani — 1958 (albania) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:finland:2014` | HJK — 2014 (finland) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:georgia:1993-94` | Dinamo Tbilisi — 1993–94 (georgia) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:albania:1957` | Partizani — 1957 (albania) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:finland:2003` | HJK — 2003 (finland) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:austria:1925-26` | Austria Wien — 1925–26 (austria) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:trinidad:1996` | Defence Force Chaguaramas — 1996 (trinidad) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| `football:finland:2011` | HJK — 2011 (finland) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |

## Audit notes

- The source-table entry is a real historical same-club Double, but that identity fact is not present in the model-visible unknown/paraphrase conditions.
- `same possible` and `distinct possible` are claims about the identity-redacted excerpt, not the hidden historical world.
- No sampled premise linguistically forces co-reference or distinctness.
- The archive action has a unique rule-governed answer: without same-club identity evidence, the Double entry cannot be certified from the excerpt.
- Neutral addenda state only same-season context and do not bear on champion identity.
