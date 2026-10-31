# Strategy Lab

A systematic, **honesty-first** research engine. It tests a battery of classic
trading-strategy families across their full parameter grids on 15 years of daily
data, then judges each one through the deflation + overfitting gate from
[backtest-overfitting](https://github.com/jarvisss007/backtest-overfitting) — so the output is a *map of what
has and hasn't been ruled out*, not a pile of curve-fit "edges."

This is the same standard that convicted the r17 sweep and returned "no edge"
verdicts for spy-trading and zero-dte-lab. A strategy is only called a survivor
if it clears **both** gates: significant after Deflated Sharpe *and* keeps its
Sharpe on an out-of-sample holdout it was never fit on.

**Correction (2026-10-31): the sentence above states the intended gate, not the one
the code runs.** In `lab.py` today, *survives* means exactly: Deflated Sharpe ≥ 0.95
**and** PBO < 0.5 (`overfit.py` `_verdict`). The 70/30 out-of-sample holdout is
computed and shown (OOS Sharpe, retention) but decides no label, and the report's
benchmark "SPY buy-and-hold Sharpe 0.921" is SPY over the full window, not over the
holdout slice the OOS Sharpes are measured on; on that slice (2022-04-20 → 2026-07-07)
SPY's Sharpe is 0.879. So the three 2026-07-07 survivors — Moving-average trend (OOS
1.468), Turn-of-month seasonality (1.214) and Volatility-managed SPY (0.950) — passed
DSR and PBO only. Each is above SPY's 0.879 on that slice, but the holdout has never
been applied as a gate, and SPY is the matching benchmark only for the SPY-only
configs (the first two hold the equal-weight basket). Which benchmark, which measure
and what margin the holdout gate should use is an open rule choice, not yet made; no
verdict has been changed. Until it is, read *survives* as "survives deflation and PBO",
nothing more.

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
python fetch_data.py   # refresh prices (slow, ~120 tickers)
python lab.py          # run the survey → report + dashboard
```

## The knowledge base is the point

`knowledge_base.csv` accumulates every family's verdict every run. Over time it
becomes the institutional memory: what's been tested, what the honest verdict
was, so no idea gets re-litigated by vibe. New strategy ideas get added to
`strategies.py` as new families and are held to the same bar.

**Not investment advice.** Survivors are candidates for forward paper-trading and
deeper validation — never signals to trade. The default, expected result on
daily large-cap data is that almost nothing survives.

## Trading Terminal — everything in one place

`terminal.html` is the unified console: one page, four tabs (Monitor · Returns ·
Day-Type · Strategies) over all datasets. It loads `hub_data.js` via `<script src>`
so it works from a plain file:// double-click — no server needed.

Refresh the whole thing:
```bash
python fetch_data.py        # 15y prices (slow, occasional)
python ~/stock-radar/collector.py   # daily monitor snapshot
python returns_matrix.py            # multi-horizon returns
python universe_daytype.py          # intraday day-type
python lab.py                       # strategy survey
python build_hub.py                 # assemble hub_data.js
```
Open `terminal.html` (or Command Center → Trading Terminal).
