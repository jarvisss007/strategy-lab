# Strategy Lab

A systematic, **honesty-first** research engine. It tests a battery of classic
trading-strategy families across their full parameter grids on 15 years of daily
data, then judges each one through the deflation + overfitting gate from
[backtest-overfitting](../backtest-overfitting) — so the output is a *map of what
has and hasn't been ruled out*, not a pile of curve-fit "edges."

This is the same standard that convicted the r17 sweep and returned "no edge"
verdicts for spy-trading and zero-dte-lab. A strategy is only called a survivor
if it clears **both** gates: significant after Deflated Sharpe *and* keeps its
Sharpe on an out-of-sample holdout it was never fit on.

## Pipeline

1. **`fetch_data.py`** — pulls 15y adjusted daily closes for the Stock Radar
   universe + SPY from Yahoo (free, no key) → `data/prices.csv`.
2. **`strategies.py`** — the battery. Each family (time-series momentum,
   cross-sectional momentum, short-term reversal, MA trend, Donchian breakout,
   vol-managed SPY, turn-of-month, a day-of-week noise control) expands to many
   parameter configs. Positions traded with a 1-day lag, **net of 5 bps/turnover**.
3. **`lab.py`** — for each family builds the (T×N) net-return matrix, runs
   `overfit.analyze()` (Deflated Sharpe + PBO/CSCV + MinBTL), and a 70/30
   out-of-sample holdout. Appends to `knowledge_base.csv` (the lab's memory) and
   renders `reports/report.md` + `reports/data.json`.
4. **`index.html`** — dashboard: the survey table, verdicts, and survivors.

## Run

```bash
/opt/anaconda3/bin/python fetch_data.py   # refresh prices (slow, ~120 tickers)
/opt/anaconda3/bin/python lab.py          # run the survey → report + dashboard
```

## The knowledge base is the point

`knowledge_base.csv` accumulates every family's verdict every run. Over time it
becomes the institutional memory: what's been tested, what the honest verdict
was, so no idea gets re-litigated by vibe. New strategy ideas get added to
`strategies.py` as new families and are held to the same bar.

**Not investment advice.** Survivors are candidates for forward paper-trading and
deeper validation — never signals to trade. The default, expected result on
daily large-cap data is that almost nothing survives.
