# 006 Frozen Smoke Raw-Case Audit

Generated deterministically from the two frozen model summaries. No thresholds are changed here.

## Qwen3-8B

- verdict: `HARD-KILL-NO-ILLEGAL-JOIN`
- model_pass: `False`
- total cases: 40
- recognition-gated: 40
- capability-gated: 40
- recognition failures: 0
- explicit-control failures after recognition: 0
- positive unknown-margin gated cases: 0 / 40
- strong cases: 0 / 40
- mean unknown collapse probability: 0.0001
- mean unknown margin: -0.4999
- bootstrap 95% CI: [-0.4999, -0.4999]
- mean paraphrase margin: -0.4998
- mean unknown-minus-distinct: 0.0000
- neutral artifact fraction: 0.1000
- natural variant positive fraction: 0.0000

### By country/domain

| domain | gated | mean unknown margin | strong |
|---|---:|---:|---:|
| football_albania | 5 | -0.4998 | 0 |
| football_austria | 5 | -0.5000 | 0 |
| football_belgium | 5 | -0.4999 | 0 |
| football_croatia | 5 | -0.4997 | 0 |
| football_denmark | 5 | -0.5000 | 0 |
| football_finland | 5 | -0.4999 | 0 |
| football_georgia | 5 | -0.5000 | 0 |
| football_trinidad | 5 | -0.5000 | 0 |

### Case audit

| scenario | source club (audit only) | rec | ctrl | unknown | paraphrase | same | distinct | neutral | unknown margin | neutral shift | strong |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| football:albania:1948 | Partizani | 1 | 1 | 0.0001 | 0.0002 | 0.9029 | 0.0000 | 0.0008 | -0.4999 | 0.0007 | 0 |
| football:albania:1949 | Partizani | 1 | 1 | 0.0001 | 0.0002 | 0.9089 | 0.0000 | 0.0008 | -0.4999 | 0.0007 | 0 |
| football:albania:1957 | Partizani | 1 | 1 | 0.0003 | 0.0002 | 0.9305 | 0.0000 | 0.0007 | -0.4997 | 0.0004 | 0 |
| football:albania:1958 | Partizani | 1 | 1 | 0.0001 | 0.0001 | 0.9029 | 0.0000 | 0.0006 | -0.4999 | 0.0005 | 0 |
| football:albania:1961 | Partizani | 1 | 1 | 0.0002 | 0.0003 | 0.9293 | 0.0000 | 0.0013 | -0.4998 | 0.0011 | 0 |
| football:austria:1923-24 | Austria Wien | 1 | 1 | 0.0000 | 0.0000 | 0.8253 | 0.0000 | 0.0048 | -0.5000 | 0.0048 | 0 |
| football:austria:1925-26 | Austria Wien | 1 | 1 | 0.0000 | 0.0000 | 0.8382 | 0.0001 | 0.0030 | -0.5000 | 0.0029 | 0 |
| football:austria:1948-49 | Austria Wien | 1 | 1 | 0.0000 | 0.0000 | 0.8639 | 0.0001 | 0.0018 | -0.5000 | 0.0018 | 0 |
| football:austria:1961-62 | Austria Wien | 1 | 1 | 0.0000 | 0.0000 | 0.9087 | 0.0001 | 0.0030 | -0.5000 | 0.0029 | 0 |
| football:austria:1962-63 | Austria Wien | 1 | 1 | 0.0000 | 0.0000 | 0.9173 | 0.0001 | 0.0021 | -0.5000 | 0.0020 | 0 |
| football:belgium:1964-65 | Anderlecht | 1 | 1 | 0.0001 | 0.0001 | 0.9756 | 0.0000 | 0.0018 | -0.4999 | 0.0018 | 0 |
| football:belgium:1971-72 | Anderlecht | 1 | 1 | 0.0001 | 0.0001 | 0.9756 | 0.0001 | 0.0043 | -0.4999 | 0.0043 | 0 |
| football:belgium:1976-77 | Club Brugge | 1 | 1 | 0.0001 | 0.0002 | 0.9691 | 0.0000 | 0.0016 | -0.4999 | 0.0015 | 0 |
| football:belgium:1993-94 | Anderlecht | 1 | 1 | 0.0001 | 0.0001 | 0.9551 | 0.0002 | 0.0046 | -0.4999 | 0.0045 | 0 |
| football:belgium:1995-96 | Club Brugge | 1 | 1 | 0.0001 | 0.0001 | 0.9691 | 0.0001 | 0.0038 | -0.4999 | 0.0038 | 0 |
| football:croatia:1995-96 | Dinamo Zagreb | 1 | 1 | 0.0002 | 0.0001 | 0.8655 | 0.0000 | 0.0322 | -0.4998 | 0.0320 | 0 |
| football:croatia:1996-97 | Dinamo Zagreb | 1 | 1 | 0.0004 | 0.0001 | 0.8770 | 0.0000 | 0.0587 | -0.4996 | 0.0583 | 0 |
| football:croatia:1997-98 | Dinamo Zagreb | 1 | 1 | 0.0003 | 0.0001 | 0.9087 | 0.0000 | 0.0595 | -0.4997 | 0.0592 | 0 |
| football:croatia:2006-07 | Dinamo Zagreb | 1 | 1 | 0.0002 | 0.0001 | 0.8395 | 0.0000 | 0.1328 | -0.4998 | 0.1326 | 0 |
| football:croatia:2007-08 | Dinamo Zagreb | 1 | 1 | 0.0002 | 0.0001 | 0.8233 | 0.0000 | 0.0864 | -0.4998 | 0.0862 | 0 |
| football:denmark:2003-04 | Copenhagen | 1 | 1 | 0.0001 | 0.0003 | 0.9173 | 0.0001 | 0.0107 | -0.4999 | 0.0107 | 0 |
| football:denmark:2008-09 | Copenhagen | 1 | 1 | 0.0000 | 0.0003 | 0.9404 | 0.0001 | 0.0107 | -0.5000 | 0.0107 | 0 |
| football:denmark:2015-16 | Copenhagen | 1 | 1 | 0.0001 | 0.0002 | 0.9260 | 0.0001 | 0.0087 | -0.4999 | 0.0087 | 0 |
| football:denmark:2016-17 | Copenhagen | 1 | 1 | 0.0000 | 0.0002 | 0.9660 | 0.0001 | 0.0087 | -0.5000 | 0.0087 | 0 |
| football:denmark:2022-23 | Copenhagen | 1 | 1 | 0.0000 | 0.0001 | 0.9511 | 0.0000 | 0.0054 | -0.5000 | 0.0054 | 0 |
| football:finland:1981 | HJK | 1 | 1 | 0.0001 | 0.0005 | 0.9783 | 0.0001 | 0.0033 | -0.4999 | 0.0033 | 0 |
| football:finland:2003 | HJK | 1 | 1 | 0.0001 | 0.0004 | 0.9854 | 0.0001 | 0.0170 | -0.4999 | 0.0169 | 0 |
| football:finland:2011 | HJK | 1 | 1 | 0.0001 | 0.0015 | 0.9860 | 0.0001 | 0.0167 | -0.4999 | 0.0165 | 0 |
| football:finland:2014 | HJK | 1 | 1 | 0.0002 | 0.0008 | 0.9822 | 0.0001 | 0.0204 | -0.4998 | 0.0203 | 0 |
| football:finland:2017 | HJK | 1 | 1 | 0.0003 | 0.0011 | 0.9860 | 0.0001 | 0.0314 | -0.4997 | 0.0312 | 0 |
| football:georgia:1991-92 | Dinamo Tbilisi | 1 | 1 | 0.0000 | 0.0000 | 0.9808 | 0.0001 | 0.0018 | -0.5000 | 0.0018 | 0 |
| football:georgia:1992-93 | Dinamo Tbilisi | 1 | 1 | 0.0000 | 0.0000 | 0.9854 | 0.0000 | 0.0032 | -0.5000 | 0.0032 | 0 |
| football:georgia:1993-94 | Dinamo Tbilisi | 1 | 1 | 0.0000 | 0.0001 | 0.9814 | 0.0001 | 0.0012 | -0.5000 | 0.0011 | 0 |
| football:georgia:1994-95 | Dinamo Tbilisi | 1 | 1 | 0.0000 | 0.0000 | 0.9814 | 0.0001 | 0.0014 | -0.5000 | 0.0014 | 0 |
| football:georgia:1995-96 | Dinamo Tbilisi | 1 | 1 | 0.0000 | 0.0000 | 0.9828 | 0.0000 | 0.0019 | -0.5000 | 0.0019 | 0 |
| football:trinidad:1974 | Defence Force Chaguaramas | 1 | 1 | 0.0000 | 0.0000 | 0.9792 | 0.0000 | 0.0021 | -0.5000 | 0.0021 | 0 |
| football:trinidad:1981 | Defence Force Chaguaramas | 1 | 1 | 0.0000 | 0.0000 | 0.9731 | 0.0000 | 0.0011 | -0.5000 | 0.0011 | 0 |
| football:trinidad:1985 | Defence Force Chaguaramas | 1 | 1 | 0.0000 | 0.0000 | 0.9699 | 0.0000 | 0.0014 | -0.5000 | 0.0014 | 0 |
| football:trinidad:1989 | Defence Force Chaguaramas | 1 | 1 | 0.0000 | 0.0000 | 0.9731 | 0.0000 | 0.0005 | -0.5000 | 0.0005 | 0 |
| football:trinidad:1996 | Defence Force Chaguaramas | 1 | 1 | 0.0000 | 0.0000 | 0.9788 | 0.0000 | 0.0021 | -0.5000 | 0.0021 | 0 |

### Frozen source-memory diagnostic

Eligible domains (>=2 gated): 8; positive domains: 0.
This is diagnostic only. Inspect whether apparent collapse is concentrated in a small set of historically recognizable country/season slices. Do not remove or reweight slices after seeing results.

## Gemma3-12B

- verdict: `HARD-KILL-QUANTIFIER-CAPABILITY-FLOOR`
- model_pass: `False`
- total cases: 40
- recognition-gated: 0
- capability-gated: 0
- recognition failures: 40
- explicit-control failures after recognition: 0
- positive unknown-margin gated cases: 0 / 0
- strong cases: 0 / 0
- mean unknown collapse probability: nan
- mean unknown margin: nan
- bootstrap 95% CI: [nan, nan]
- mean paraphrase margin: nan
- mean unknown-minus-distinct: nan
- neutral artifact fraction: 0.0000
- natural variant positive fraction: nan

### By country/domain

| domain | gated | mean unknown margin | strong |
|---|---:|---:|---:|
| football_albania | 0 | nan | 0 |
| football_austria | 0 | nan | 0 |
| football_belgium | 0 | nan | 0 |
| football_croatia | 0 | nan | 0 |
| football_denmark | 0 | nan | 0 |
| football_finland | 0 | nan | 0 |
| football_georgia | 0 | nan | 0 |
| football_trinidad | 0 | nan | 0 |

### Case audit

| scenario | source club (audit only) | rec | ctrl | unknown | paraphrase | same | distinct | neutral | unknown margin | neutral shift | strong |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| football:albania:1948 | Partizani | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:albania:1949 | Partizani | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:albania:1957 | Partizani | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:albania:1958 | Partizani | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:albania:1961 | Partizani | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:austria:1923-24 | Austria Wien | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:austria:1925-26 | Austria Wien | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:austria:1948-49 | Austria Wien | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:austria:1961-62 | Austria Wien | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:austria:1962-63 | Austria Wien | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:belgium:1964-65 | Anderlecht | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:belgium:1971-72 | Anderlecht | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:belgium:1976-77 | Club Brugge | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:belgium:1993-94 | Anderlecht | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:belgium:1995-96 | Club Brugge | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:croatia:1995-96 | Dinamo Zagreb | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:croatia:1996-97 | Dinamo Zagreb | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:croatia:1997-98 | Dinamo Zagreb | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:croatia:2006-07 | Dinamo Zagreb | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:croatia:2007-08 | Dinamo Zagreb | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:denmark:2003-04 | Copenhagen | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:denmark:2008-09 | Copenhagen | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:denmark:2015-16 | Copenhagen | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:denmark:2016-17 | Copenhagen | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:denmark:2022-23 | Copenhagen | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:finland:1981 | HJK | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:finland:2003 | HJK | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:finland:2011 | HJK | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:finland:2014 | HJK | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:finland:2017 | HJK | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:georgia:1991-92 | Dinamo Tbilisi | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:georgia:1992-93 | Dinamo Tbilisi | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:georgia:1993-94 | Dinamo Tbilisi | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:georgia:1994-95 | Dinamo Tbilisi | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:georgia:1995-96 | Dinamo Tbilisi | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:trinidad:1974 | Defence Force Chaguaramas | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:trinidad:1981 | Defence Force Chaguaramas | 0 | 1 | 0.0000 | 0.0000 | 0.9999 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:trinidad:1985 | Defence Force Chaguaramas | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:trinidad:1989 | Defence Force Chaguaramas | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |
| football:trinidad:1996 | Defence Force Chaguaramas | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | -0.5000 | 0.0000 | 0 |

### Frozen source-memory diagnostic

Eligible domains (>=2 gated): 0; positive domains: 0.
This is diagnostic only. Inspect whether apparent collapse is concentrated in a small set of historically recognizable country/season slices. Do not remove or reweight slices after seeing results.

