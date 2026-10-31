# Strategy Lab

A systematic, **honesty-first** research engine. It tests a battery of classic
trading-strategy families across their full parameter grids on 15 years of daily
data, then judges each one through the deflation + overfitting gate from
[backtest-overfitting](https://github.com/jarvisss007/backtest-overfitting) — so the output is a *map of what
has and hasn't been ruled out*, not a pile of curve-fit "edges."

This is the same standard that convicted the r17 sweep and returned "no edge"
verdicts for spy-trading and zero-dte-lab. A family is only called a survivor if
it clears **three** bars: Deflated Sharpe ≥ 0.95 and a probability of backtest
overfitting (PBO) below 0.5 over its whole grid, and the **out-of-sample holdout**.
For the holdout, the config picked on the first 70% of history is run on the last
30%, and its mean daily return over its **own universe's** buy-and-hold (SPY for
SPY-only configs, the equal-weight basket for basket configs, cash for long-short
configs), net of costs, must be more than **2 × its standard error**. There is no
retention bar. Missing or broken holdout data, or fewer than 60 holdout days, fails
the gate.

Where that bar comes from: the "> 2 × standard error" test is the first bullet of
[PRE_REGISTRATION §2](PRE_REGISTRATION.md). Section 2 was written for the forward
book, the file is an unratified DRAFT, and its benchmark is SPY / NIFTY; the
own-universe benchmark comes from Anupam's 2026-10-31 ruling. Its second bullet, the
carried ~35-trial deflation budget, is **not** applied: the survey keeps its own
per-family Deflated Sharpe, deflated over each family's 3–36 configs, and whether to
carry the budget is open for Anupam. Its third bullet, "positive after 2×COST per
round trip", is met whenever the first is, because the returns are already net of
5 bps per unit of turnover, which is 2×COST per round trip.

**Correction (2026-10-31, SLAB-001): under that holdout gate, none of the three
2026-07-07 survivors survives.** Before 2026-10-31 the code called a family
*survives* on Deflated Sharpe ≥ 0.95 and PBO < 0.5 alone; the holdout was computed
and shown but decided nothing, although this README promised it. Anupam ruled the
gate on 2026-10-31 and `lab.py` now applies it. Replayed on the July universe and the
July holdout slice (2022-04-20 → 2026-07-07) from the cached prices:

| Family (config the in-sample data picked) | Benchmark | Mean excess | SE | Excess − 2 SE | Holdout |
|---|---|--:|--:|--:|---|
| Moving-average trend (`MAtrend basket n200`) | equal-weight basket | −2.0%/yr | 5.5% | −12.9% | fail |
| Turn-of-month seasonality (`TurnOfMonth t5`) | equal-weight basket | −17.8%/yr | 10.4% | −38.5% | fail |
| Volatility-managed SPY (`VolMgd SPY tgt20 lb21`) | SPY | +4.7%/yr | 4.1% | −3.5% | fail |

All three move from *survives* to *suspect*. The other six families were not
survivors and fail the holdout too. Read this as "not proven on a four-year slice",
not as "proven worthless": each of the three had a higher Sharpe than SPY on that
slice (1.468, 1.214 and 0.950 against 0.879), but none returned more than its own
universe by a margin the slice can tell from noise. The measure is raw excess
return, not risk-adjusted: configs that sit out part of the time are judged against
a benchmark that is always invested, and leverage is rewarded — volatility-managed
SPY can hold up to 2× SPY, which is part of its +4.7%/yr.

What did not change: every published 2026-07-07 value in `knowledge_base.csv`, and
the meaning of its `verdict` column, which is still the Deflated Sharpe + PBO
verdict. New columns record the rest: `gate` says which gate judged a row
(`dsr_pbo` for the July rows, `dsr_pbo_holdout` from now on), `survey_verdict` is the
label after that gate, and `holdout*` hold the holdout's benchmark, numbers and
result. The replay reproduces the July out-of-sample Sharpes of the three configs
above exactly, but it is not a full reproduction of the July run. The price cache
now starts 2011-10-31, not 2011-07-08, so DSR and PBO differ a little (all nine
DSR + PBO verdicts come out the same). Time-series momentum's in-sample data picks a
different config than July's (`TSMOM L126 H21 long`, OOS Sharpe 1.42, against July's
`TSMOM L21 H63 long` at 1.10). Cross-sectional momentum's OOS Sharpe also differs
(0.34 against 0.20), because its rebalance dates shift with the start date. To rerun
it (it prints and writes nothing):
`python lab.py --universe-from <(git show 3aceed3:data/meta.json) --end 2026-07-07 --oos-start 2022-04-20`.
`data/prices.csv` is gitignored, so this needs the lab's local price cache; it cannot
be run from the repo alone. On the current price panel every family fails the
holdout closed, because the panel has three futures-only dates (ES=F/NQ=F rows on
NYSE holidays) inside the slice.

Written before this gate and not updated: `paper/honest_evaluation_survey.*` (its
Study 1 table marks the three as "survives*", and its gate item 5 describes the
holdout with no bar) and `RESEARCH_WRITEUP.md`.

## Pipeline

1. **`fetch_data.py`** — pulls 15y adjusted daily closes for the Stock Radar
   universe + SPY from Yahoo (free, no key) → `data/prices.csv`.
2. **`strategies.py`** — the battery. Each family (time-series momentum,
   cross-sectional momentum, short-term reversal, MA trend, Donchian breakout,
   vol-managed SPY, turn-of-month, a day-of-week noise control) expands to many
   parameter configs. Positions traded with a 1-day lag, **net of 5 bps/turnover**.
3. **`lab.py`** — for each family builds the (T×N) net-return matrix, runs
   `overfit.analyze()` (Deflated Sharpe + PBO/CSCV + MinBTL), and the 70/30
   out-of-sample holdout gate above. Appends to `knowledge_base.csv` (the lab's memory) and
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
