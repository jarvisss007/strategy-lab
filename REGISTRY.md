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

## Paper Arena rules (registered 2026-07-25, sign-off: Anupam in session — "make agents take as many trades as possible and learn accordingly")

Fixed parameters, never tuned after registration. Evaluated in arena.py: 1y
backtest replay + live forward paper book, entry/exit at signal close, 10 bps
per side, benchmarked vs SPY. Every trade is tagged with the regime at entry
(calm/storm = VIX < / ≥ 20 · up/down = SPY above/below its 50d MA) so each
rule's per-condition record accrues honestly.

| Rule | Registered | Thesis (pre-stated) | Status |
|---|---|---|---|
| DEEP_DIP (fresh −40% off 52w hi → long 10d) | 2026-07-25 | user hypothesis: deep discount from year-high mean-reverts | backtest DEAD (−112 bps vs SPY) |
| PANIC_BOUNCE (1d ≤ −5% → long 2d) | 2026-07-25 | violent 1-day flush overshoots | backtest CANDIDATE (t 2.7) |
| DOUBLE_DIP (2d ≤ −6% → long 3d) | 2026-07-25 | two-day washouts overshoot harder | backtest CANDIDATE (t 2.9) |
| FRESH_HIGH (new 52w hi → long 10d) | 2026-07-25 | breakout momentum persists | backtest WATCH (t 1.7) |
| SHORT_EXT (new hi & ≥2× 52w lo → short 5d) | 2026-07-25 | user hypothesis: over-extension snaps back | backtest DEAD (−75 bps vs SPY) |
| TREND_RIDER (cross > 50MA, above 200MA → long 15d) | 2026-07-25 | classic trend-following entry | backtest DEAD (−149 bps vs SPY) |
| PANIC_LITE (1d ≤ −3% → long 2d) | 2026-07-25 | if the −5% flush bounce is real, a −3% version trades 3-4× as often at lower per-trade edge — tests whether the effect scales or only lives in the extreme tail | NEW — no results yet |
| STORM_DIP (1d ≤ −4% AND VIX ≥ 20 → long 3d) | 2026-07-25 | the dip-buy premium should concentrate in high-vol tape where liquidity providers demand more; regime-gated version of the same family | NEW — no results yet |

Trials-budget note: these 8 count against the cumulative budget like everything
else, and the two dip CANDIDATEs are same-family cousins of the mean-reversion
configs already convicted on 15y data — forward record + deflation gate decide,
not the 1y replay.

### Tempo raise (registered 2026-07-25 PM, sign-off: Anupam in session — "raise the trading tempo so the agents gather experience fast")

Four higher-frequency rules added, theses pre-stated below BEFORE any backtest
saw them. Same conventions, parameters frozen at registration. Cap raised
25 → 40 open per rule (capacity, not signal logic). These 4 also count against
the cumulative trials budget forever.

| Rule | Registered | Thesis (pre-stated) | Status |
|---|---|---|---|
| RSI2_DIP (RSI(2) < 10, close > 200MA → long 3d) | 2026-07-25 | Connors-style: extreme short-term oversold inside a long-term uptrend mean-reverts; fires often by construction | NEW — no results yet |
| REVERSAL_3 (3 consecutive down closes, close > 200MA → long 2d) | 2026-07-25 | short losing streaks in uptrends are noise, not information; the simplest possible reversal claim | NEW — no results yet |
| BOLL_SNAP (close < 20d MA − 2×20d σ → long 3d) | 2026-07-25 | 2-sigma stretches below the 20d band snap back (rubber-band); vol-scaled cousin of the fixed-% dip rules | NEW — no results yet |
| PULLBACK_50 (close > 200MA and crosses below 20d MA → long 5d) | 2026-07-25 | the first dip through the 20d in an uptrend gets bought; trend-plus-pullback, the long-side mirror of what TREND_RIDER tests | NEW — no results yet |

Roundtable note (same sign-off): every refresh now writes reports/roundtable.md
— one shared report with each agent's journal, per-regime rhythm, and crowding.
Agents READ the prior roundtable and cite peers in their journals. Reading is
awareness only: no rule's entry/exit logic changes based on it — adaptive
variants would be new registered rules, not silent edits.
