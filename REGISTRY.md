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
| RSI2_DIP (RSI(2) < 10, close > 200MA → long 3d) | 2026-07-25 | Connors-style: extreme short-term oversold inside a long-term uptrend mean-reverts; fires often by construction | backtest DEAD (−38 bps, t −1.17) |
| REVERSAL_3 (3 consecutive down closes, close > 200MA → long 2d) | 2026-07-25 | short losing streaks in uptrends are noise, not information; the simplest possible reversal claim | backtest WATCH (positive, not significant) |
| BOLL_SNAP (close < 20d MA − 2×20d σ → long 3d) | 2026-07-25 | 2-sigma stretches below the 20d band snap back (rubber-band); vol-scaled cousin of the fixed-% dip rules | backtest CANDIDATE — forward decides |
| PULLBACK_50 (close > 200MA and crosses below 20d MA → long 5d) | 2026-07-25 | the first dip through the 20d in an uptrend gets bought; trend-plus-pullback, the long-side mirror of what TREND_RIDER tests | backtest WATCH (positive, not significant) |

Implementation notes: RSI(2) uses the simple 2-period average-gain/loss form
(not Wilder smoothing) — fixed at registration.

Fill-integrity fix (2026-07-25 audit): the morning refresh runs during RTH, so
forward fills were booking at partial-bar intraday prices — e.g. BE filled at
184.89 during a −15% flush that closed at 217.30, gifting four dip agents a
fictitious +17% MTM no close ever printed. This violated the registered
"entry/exit at signal close" convention. arena.py now gates fills: intraday
runs (weekdays 6:30–13:05 PT) mark to market only; opens/closes happen on
post-close data. The 2026-07-25 morning intraday fills remain in the book
as-is (recorded is recorded); their flattering fills are documented here.

Roundtable note (same sign-off): every refresh now writes reports/roundtable.md
— one shared report with each agent's journal, per-regime rhythm, and crowding.
Agents READ the prior roundtable and cite peers in their journals. Reading is
awareness only: no rule's entry/exit logic changes based on it — adaptive
variants would be new registered rules, not silent edits.

Date-semantics fix (2026-08-06 council audit): dates are bar dates, not run
dates — corrected 2026-08-06. Forward rows had been stamped with the RUN date
while being priced at the latest completed bar's close, so printed dates ran
one session late vs their prices (e.g. BOLL_SNAP EBAY stamped "2026-08-04"
@107.13, which is EBAY's 08-03 close). entry_date/exit_date now carry the date
of the bar whose close the row is priced at; regime tags and the roundtable's
opened/closed counters key off the same latest completed session. Existing
rows (135 open + 532 closed) were migrated by matching each row's price to
the dated bar series: 110 open and 526 closed entry dates shifted one session
earlier; exit dates were already bar-dated (531/532 confirmed). Seven rows
whose price matches no daily close (partial-bar-era fills: REVERSAL_3
GFS/HUM/MOH 07-29, BOLL_SNAP TSLA 07-29, and three QBTS rows) kept their old
stamp on the unmatched field rather than guessing. Regime tags were verified
already bar-dated (0 changed on recomputation). No trading logic, thresholds,
or rule parameters changed — labeling only.

## ACCRUAL GATE — Anupam ruling, Review #2, 2026-08-09
No Arena rule may be discussed as a promotion candidate until its forward book holds
**≥20 distinct entry days AND ≥3 distinct storm sessions** (storm = VIX≥20 at entry).
Origin: all 136 storm-down trades to date were entered on ONE day (2026-07-29);
STORM_DIP's t=4.82 was that Wednesday wearing a sample size. Fixed before the data
arrives, same shape as the zero-DTE 60-session gate and the n≥15 morning floor.
The deflation gate (arena_gate.py, failed 2026-08-08) remains a separate, additional bar.

## HORIZON HYPOTHESIS — pre-registered 2026-08-12, Anupam

Registered BEFORE the data that will test it exists. Anupam, 2026-08-11: "why does
the agent take the trade until a certain date? Is there any analysis based on that?
Why not one day, two day, five day, ten day?" There was none. Every hold above was
registered with its signal justified and its horizon simply asserted — 10d, 2d, 3d,
15d — and this file is where that gap is now closed.

**H1.** For Arena entries, mean excess vs SPY over the hold's own window is
NON-DECREASING from 1 to 5 trading days and does NOT improve materially beyond 5.
Informally: most of the move lands in the first week.

**Where it came from, stated so it cannot later be dressed up as a prediction.**
`stock-radar/horizon_study.py --arena`, run 2026-08-12 over all 622 closed Arena
rows, gave +0.73 / +1.16 / +2.08 / +3.45 / +3.19 % at 1/2/3/5/10 days. That is a
RETROSPECTIVE SWEEP over the same data that suggested the shape, and its best
column FAILED its own bar: t = +2.18 against the 2.31 required on n = 9 entry days.
It is a hypothesis, not a result. Recording it here is what makes the next test
honest.

**Test.** Entry days from 2026-08-13 onward ONLY — days the sweep never saw. Bar,
fixed now: mean excess at 5d must exceed 1d by a margin significant across ENTRY
DAYS (t computed on day means, not rows) at the Bonferroni-corrected level for the
7 horizons swept. Costs must be modelled: a shorter hold trades more often, and the
sweep above measured everything before the extra round trips.

**Minimum sample.** 30 independent entry days. The Arena currently has 11 across
622 rows, and this file will not be read as settled before then.

**Not to be acted on in the meantime.** No rule's `hold` changes on the basis of the
sweep. Sweeping a parameter and adopting the winner is the exact procedure
~/backtest-overfitting convicted this account's own r17 for, and a horizon is a
parameter like any other. A change requires this hypothesis to clear the bar above
on unseen days AND to pass the deflation/PBO gate.

---

## RE-STATED 2026-08-13 — the `fixed_10d` replay claim, with its provenance

**The claim:** a replay showed `fixed_10d` beating the registered exits by **+4.13pp over
583 closes**.

**Status: REPRODUCED, and it is a retrospective sweep — not a result.** The council
(directive 2026-08-13) asked that it be re-stated with its build date attached or retired.
It re-states. Provenance, in full:

- **Source of truth:** `~/stock-radar/data/exit_study_cache/arena_progress.json`, the
  per-trade cache written by `stock-radar/exit_study.py --arena`. **Build date
  2026-08-09 14:43:50.** The study lives in `stock-radar`, not here — the same place
  `horizon_study.py` does (see H1 above).
- **Why the council saw an empty file:** `~/stock-radar/data/exit_study.json` — the
  *report* — was overwritten on **2026-08-11 21:13:52** by a plain, non-Arena run
  (`arena_included: false`, `n_trades: 10`). The report was clobbered; the cache was not.
  A run without `--arena` silently replaces the Arena report with a ledger-only one.
- **Recomputed today from that cache:** 583 cached Arena rows, of which **503 carry an
  excess-vs-SPY figure** (80 do not). Mean excess: `registered` **+2.076pp**,
  `fixed_10d` **+6.268pp**, `bracket` +0.297pp, `trail_1r` +0.784pp.
  **`fixed_10d` − `registered` = +4.19pp**, against the +4.13pp on record. The small
  difference is not reconciled and is not worth reconciling — the point is the figure
  reproduces to a tenth of a point, not that the tenth matches.

**What the number is NOT.** Those 583 rows span **2026-07-23 to 2026-08-05 across 10
distinct entry days**. Ten days is the honest denominator, not 583. This is the same
retrospective sweep over the same book that produced H1 above, and it is governed by H1's
pre-registered bar: entry days from **2026-08-13 onward only**, t computed on **day means**
at the Bonferroni-corrected level, costs modelled, **minimum 30 independent entry days**.

**Not to be acted on.** No rule's `hold` changes on the basis of this. Sweeping a parameter
and adopting the winner is the exact procedure `~/backtest-overfitting` convicted this
account's own r17 for, and a hold horizon is a parameter like any other. A change requires
H1 to clear its bar on unseen days AND to pass the deflation/PBO gate.

**Housekeeping owed:** re-run `exit_study.py --arena` so the *report* matches the cache
again, and make a no-`--arena` run stop overwriting the Arena report. Filed, not done.
