# An Honest Strategy-Discovery Pipeline
### Finding real market patterns — and rejecting them as false edges under rigorous validation

**Anupam Patil** · [github.com/jarvisss007](https://github.com/jarvisss007)

---

## Summary

I built an end-to-end quantitative research pipeline that generates trading
hypotheses, tests each through a multiple-testing-corrected validation gate, and
reports an honest verdict. Applied to 15 years of daily data on a 119-name equity
universe — across momentum, mean-reversion, calendar, structural-friction, and
intraday hypotheses — the pipeline found **no strategy that beats a buy-and-hold
benchmark after transaction costs and survivorship adjustment.** The contribution
is not an edge; it is a disciplined apparatus that repeatedly *discovers real
statistical patterns and then correctly rejects them* as untradeable or
overfit — the failure mode that sinks most retail and even professional backtests.

## Motivation

The dominant risk in quantitative strategy research is **backtest overfitting**:
testing many configurations and reporting the best one as an "edge," when its
performance is a selection artifact that vanishes out of sample. I treated this as
the central design constraint rather than an afterthought.

## Methodology — the validation gate

Every candidate strategy is judged by a battery designed to defeat self-deception:

- **Deflated Sharpe Ratio (Bailey & López de Prado, 2014)** — discounts the best
  configuration's Sharpe for the number of trials it took to find it.
- **Probability of Backtest Overfitting via CSCV (Bailey et al., 2015)** — the
  probability the in-sample winner underperforms out of sample.
- **Minimum Backtest Length** — flags when the data is too short to trust a Sharpe.
- **Out-of-sample holdout + walk-forward folds** — the in-sample winner must retain
  performance on untouched data and stay positive across independent time slices.
- **Transaction costs** — every return series is netted of realistic per-trade cost,
  charged on actual turnover.
- **An honest benchmark** — a strategy must beat *buy-and-hold the basket*, not
  merely beat zero. (This single correction reclassified my one apparent "survivor.")
- **Survivorship awareness** — the universe is today's constituents; long-equity and
  dip-buying results are explicitly flagged as inflated by this.

The gate is implemented as a standalone, unit-tested library
([`backtest-overfitting`](https://github.com/jarvisss007/backtest-overfitting), CI green).

## What was tested

- **Daily strategy families** (full parameter grids): time-series & cross-sectional
  momentum, short-term reversal, moving-average trend, Donchian breakout,
  volatility-managed exposure, turn-of-month and 52-week-high effects, plus a
  **day-of-week noise control** planted to confirm the gate rejects known noise.
- **Structural frictions** (an autonomous discovery engine): overnight-vs-intraday
  return decomposition, options-expiry drift, month-end flows, volume/liquidity premia.
- **Intraday microstructure**: automated day-type classification (efficiency ratio,
  regime), time-of-day return profile, opening-range and first-hour predictability.

## Key results

| Claim tested | Statistical pattern? | Tradeable after costs? |
|---|---|---|
| Day-of-week effect (control) | No (correctly rejected as OVERFIT) | — |
| Cross-sectional momentum / reversal | Fails deflation / out-of-sample | No |
| "% off high" dip-buying | **Yes** — but survivorship-inflated | No |
| Turn-of-month / options-expiry drift | **Yes**, robust across folds | Loses to buy-and-hold |
| **Overnight drift** | **Yes** — gross Sharpe 1.50, *beats* buy-and-hold | **No** — net −0.24 |
| Opening-range breakout ("90% win rate") | Illusion (conditioning bias) | No |

**The overnight-drift result is the thesis in one line.** US equities historically
accrue their return overnight; a strategy capturing it has a gross Sharpe of 1.50 —
higher than buy-and-hold. But capturing overnight-only return requires a round-trip
every session, and those transaction costs turn +1.50 into −0.24. *The friction that
creates the pattern is precisely what makes it untradeable.* A validation pipeline
that reports gross-only would have flagged a spectacular false edge.

Similarly, the "opening-range breakout closes in the breakout direction ~90% of the
time" collapses once entry is modeled at the actual breakout price rather than the
open: you only capture break-to-close, and net of costs the edge is gone. This is a
textbook conditioning-on-the-outcome bias, caught by honest trade simulation.

## What this demonstrates

- Rigorous out-of-sample and multiple-testing-corrected evaluation (DSR, PBO/CSCV).
- Correct handling of transaction costs, survivorship bias, and benchmark selection.
- The scientific discipline to **publish a null result** and to reject one's own
  promising findings — the trait that separates real quant research from marketing.
- Full-stack execution: data engineering, vectorized backtesting, an autonomous
  hypothesis-search loop, and reproducible reporting.

## Reproducibility

Free data (no proprietary feeds); Python/pandas; the validation library and case
studies are public. Every verdict is logged to a growing knowledge base so no
hypothesis is re-litigated by intuition.

## Honest limitations

The null result is conditional on **free daily data and retail transaction costs**.
The one identified real pattern (overnight drift) would be marginally harvestable at
institutional costs and execution access — a structural advantage, not an analytical
one. The remaining honest lever is *differentiated data* (e.g., options
positioning/flow), which the discovery engine is already architected to test. Absent
that, the disciplined conclusion is that liquid daily equity data is efficient enough
that the honest expected edge, net of costs, is zero — and demonstrating *that*
rigorously is the result.

---

*Companion repositories:* `strategy-lab` (this pipeline), `backtest-overfitting`
(the validation library), and a related null-result working paper on ML trading
signals. All emphasize honest evaluation over performance claims.
