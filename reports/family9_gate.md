# FAMILY 9 — own-history value + quality floor · 2026-08-24 08:18 PT

124 names · monthly excess vs SPY · IS 2010-02-28→2021-08-31 · OOS 2021-09-30→2026-08-31

**Verdict: FAILS the gate**

| bar | value | pass |
|---|---|---|
| 1 · DSR ≥ 0.95 (best of 8, IS) | 0.7934 | ❌ |
| 2 · PBO < 0.5 | 0.5185 | ❌ |
| 3 · OOS total excess > 0 | 23.1% | ✅ |

Best IS config D=20th pctile, F≥6, hold 6m: IS excess Sharpe 0.514 vs deflated benchmark 0.215. Toolkit: OVERFIT: not significant after deflation AND high overfitting probability.

Caveats: survivorship-tilted, growth-heavy universe (bias against value in-sample, stated at registration) · annual filings only; quarterly TTM would react faster · one 70/30 split; n=1 experiment

| D | Q | H | IS xs Sharpe | OOS xs Sharpe |
|---|---|---|---|---|
| 10 | 6 | 6 | 0.133 | 0.109 |
| 10 | 6 | 12 | 0.123 | 0.196 |
| 10 | 7 | 6 | 0.099 | -0.141 |
| 10 | 7 | 12 | 0.095 | -0.275 |
| 20 | 6 | 6 | 0.363 | 0.353 |
| 20 | 6 | 12 | 0.329 | 0.464 |
| 20 | 7 | 6 | 0.185 | -0.098 |
| 20 | 7 | 12 | 0.222 | -0.259 |
