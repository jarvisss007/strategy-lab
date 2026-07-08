# Strategy Lab — honest survey

**Window:** 2011-07-08 … 2026-07-07  ·  **119 tickers**  ·  cost 5 bps/turnover  ·  built 2026-07-07 23:18 PDT

**Benchmark:** SPY buy-and-hold Sharpe = **0.921** (the number any strategy has to beat to be worth the trouble).

Each family was tested across its full parameter grid. `Deflated Sharpe` discounts the best config for how many were tried (≥0.95 = significant). `PBO` is the probability the in-sample winner underperforms out of sample (>0.5 = overfit). `OOS Sharpe` is the in-sample winner's Sharpe on the untouched last 30% of history. A real edge needs DSR high, PBO low, and OOS Sharpe that survives.

| Family | Configs | Best Sharpe (IS) | Deflated Sharpe | PBO | OOS Sharpe | Retained | Verdict |
|---|--:|--:|--:|--:|--:|--:|---|
| Moving-average trend | 8 | 1.203 | 1.0 | 0.123 | 1.468 | 1.37 | **survives** |
| Turn-of-month seasonality | 3 | 1.09 | 0.998 | 0.081 | 1.214 | 1.17 | **survives** |
| Volatility-managed SPY | 6 | 0.986 | 1.0 | 0.369 | 0.95 | 0.95 | **survives** |
| Donchian breakout | 6 | 1.185 | 1.0 | 0.567 | 1.345 | 1.21 | **suspect** |
| Time-series momentum | 24 | 1.315 | 0.941 | 0.073 | 1.1 | 0.88 | **suspect** |
| Cross-sectional momentum | 36 | 0.501 | 0.748 | 0.205 | 0.198 | 0.33 | **suspect** |
| Short-term reversal | 18 | 0.049 | 0.002 | 0.468 | -0.736 | -2.27 | **suspect** |
| Day-of-week (control) | 5 | -0.056 | 0.173 | 0.684 | -0.562 | -4.07 | **OVERFIT** |

## What survived

- **Moving-average trend** — best OOS config `MAtrend basket n200`, OOS Sharpe 1.468 (kept 137% of in-sample). Worth paper-trading forward, not betting on.
- **Turn-of-month seasonality** — best OOS config `TurnOfMonth t5`, OOS Sharpe 1.214 (kept 117% of in-sample). Worth paper-trading forward, not betting on.
- **Volatility-managed SPY** — best OOS config `VolMgd SPY tgt20 lb21`, OOS Sharpe 0.95 (kept 95% of in-sample). Worth paper-trading forward, not betting on.

## Read this before believing any survivor

The gate is working — it correctly rejected the **day-of-week** noise control (OVERFIT) and both genuinely market-neutral alpha attempts (**cross-sectional momentum** and **short-term reversal** failed out of sample). That is the signal that the machinery is honest. But the survivors carry heavy caveats:

- **They are not alpha — they are risk-managed long equity beta.** Every survivor (MA-trend, vol-managed SPY, turn-of-month) is *long-only*. They beat SPY by sidestepping drawdowns or sitting out risky stretches, not by predicting anything. The strategies that would be true market-neutral edge are the ones that **failed**.
- **Survivorship bias.** The universe is *today's* watchlist — names that already won their way onto it. Backtesting them 15 years inflates every long-equity result.
- **The out-of-sample window (≈2022–2026) contains one big bear market.** Trend and vol filters mechanically look great in any sample that holds a drawdown they dodge; that is regime luck, not a stable edge.
- **Costs are modeled simply** (5 bps/turnover, no slippage, borrow, or impact). The market-neutral strategies that need shorting are understated — they look *worse* in reality, not better.
- **Cross-family selection.** Picking the best of 8 families adds a layer of multiple testing the per-family Deflated Sharpe does not capture.

**Bottom line:** consistent with spy-trading and zero-dte-lab — no tradeable market-neutral edge here. The one durable, well-documented *lesson* (not a money machine) is that trend/vol filters improve the risk-adjusted return of long equity exposure. That is beta-timing, worth understanding, not an edge to bet on.

## What may be worth watching

Ranked by out-of-sample Sharpe (survivors + suspects). 'May work' means 'survived the holdout here' — it is a forward-test candidate, never a prediction:
- Moving-average trend (`MAtrend basket n200`): OOS 1.468 vs SPY 0.921 — survives
- Turn-of-month seasonality (`TurnOfMonth t5`): OOS 1.214 vs SPY 0.921 — survives
- Volatility-managed SPY (`VolMgd SPY tgt20 lb21`): OOS 0.95 vs SPY 0.921 — survives
- Donchian breakout (`Donchian hi200 lo50`): OOS 1.345 vs SPY 0.921 — suspect
- Time-series momentum (`TSMOM L21 H63 long`): OOS 1.1 vs SPY 0.921 — suspect

---
*A research survey, not investment advice. Survivors are candidates for forward paper-trading and deeper validation, nothing more.*
