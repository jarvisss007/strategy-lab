# Hypothesis Registry — FROZEN as of 2026-07-11

This file is the pre-commitment device (*Behavioral Investing*, Book 3: plan in the
sunshine, execute in the storm). Every hypothesis family in `discover.py`, its full
config grid, and its verdict is recorded here. From this date forward:

**The rules of the registry**
1. **No new family or config gets added to `discover.py` without being written here
   FIRST, with its thesis, before any backtest run sees it.** Adding a config after
   peeking at results is the exact multiple-testing sin `overfit.py` exists to catch.
2. The weekly research sentinel diffs `discover.py`'s `FAMILIES` against this file —
   an unregistered family is flagged as a **mining violation**, not a discovery.
3. Verdicts below may CHANGE as new data accrues (that's the point of re-validation);
   the family list itself only grows by explicit human sign-off (Anupam's, in writing).
4. The trials budget is cumulative and never resets. Every config ever tried counts
   against `min_backtest_length` / DSR deflation forever.

## The trials budget

~35 configs across 6 families (plus the r17 sweep's 6 configs and the mean-rev 18
convicted in [backtest-overfitting case studies](https://github.com/jarvisss007/backtest-overfitting/tree/main/case_studies)).
At this trial count, `min_backtest_length(35, 1.0)` ≈ several years of data are
already required for a Sharpe-1 claim to mean anything — one more reason additions
need sign-off, not enthusiasm.

## The frozen families (verdicts as of 2026-07-11, 15y daily data)

| Family | Configs | Thesis (pre-stated in code) | Verdict |
|---|---|---|---|
| Overnight vs intraday | 3 | Returns accrue overnight; intraday is noise | structural-but-uncostable (gross 1.5, net −0.24 — 2 trades/day eats it) |
| Options-expiry flow | 4 | Hedging flow distorts pre/post-opex weeks | real-but-loses-to-buy&hold (DSR 0.89, PBO 0.54) |
| Turn-of-month flow | 3 | Pension/index flows lift month boundaries | real-but-loses-to-buy&hold (DSR 1.0, PBO 0.01) — **cleanest stats in the KB**, but MC drawdown range 19–38% (case study #4) |
| Volume/liquidity microstructure | 10 | Documented premia; expected weak in liquid large-caps | real-but-loses-to-buy&hold (best: illiquidity q0.2, DSR 0.1) |
| Price-action value-area fade | 6 | Books 7+8: price reverts toward fair value | real-but-loses (DSR 0.16, OOS net negative — weak) |
| Price-action confluence | 6 | Books 7+8: fade + trend agreement beats fade alone | **dead — refuted**: worse than the plain fade everywhere (wf 0–1/5) |

## What re-validation means (the sentinel's job, not mining)

`fetch_data.py` extends the dataset every Monday. Re-running `discover.py` on the
grown dataset and comparing each family's verdict to the row above is **true
out-of-sample validation** — the hypotheses were fixed before the new data existed.
Verdict drift in either direction is a real finding. New configs are not.

## Standing candidates awaiting DATA, not analysis

- **zero-dte-lab**: underpricing verdict needs 60+ recorded sessions (have 1;
  recorder awaiting activation).
- **crypto-microstructure**: LR=0.002 finding re-validates continuously via the
  daily cumulative backtest; watch `edge_found` and skill trajectory, expect ≈0.
- **insider-radar**: deep-sample verdict OVERFIT (PBO 0.914) — frozen; feed keeps
  accruing events for a future, larger re-test.
