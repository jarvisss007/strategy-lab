# Pre-registration: "buy puts before every earnings report" (2026-10-17)

Written and committed BEFORE any number below was computed. Internal record; his deliverable is the live page.

## His claim (voice, 2026-10-17)
TSMC reported a robust quarter on Thu 2026-10-15 and still fell ("~439 on the 14th, down ~7.2%").
So even after a good quarter the stock falls; no stocks are going to rise. Plan: buy put options on
every earnings report, 1, 2 or 3 days before, on all US stocks.

## Facts checked before registering (prices.csv, Yahoo cross-check)
TSM closes: 10-13 445.12, 10-14 430.00, 10-15 422.25 (report day, pre-open print), 10-16 412.61.
Report-day move -1.8% (SPY +0.3%). The ~7.3% is 10-13 close -> 10-16 close, three sessions, during a
semis-wide drop (AMD -12.7%, NVDA -6.3%, ASML -4.4% over the same dates). Yahoo EPS surprise +1.67%
(smallest beat in five quarters).

## Events
EDGAR 8-K Item 2.02 prints (data/edgar/earnings_8k.json), session by the EARN-006 rule (UTC stamp -> NY;
before 16:00 that session, else next). Panel data/prices.csv, 2011-10 -> 2026-10-16. T = first tradeable
session; reaction = close[T-1] -> close[T].

## Questions and bars (fixed now)
**H1 - "even after a good quarter it falls".** Beat = Yahoo surprise > 0, matched to the EDGAR print
within +-3 calendar days. Supported only if, after beats, the reaction is negative more often than not
(> 50% down) AND the mean reaction excess vs SPY is negative with week-clustered CR1 t <= -2.

**H2 - blanket ATM puts make money.** Buy an ATM put at close[T-h], sell at close[T].
Primary h = 2 ("a day or two before"); secondary h = 1 and h = 3.
Price model (fair to the stock's own history): total sd s = sqrt(J^2 + (h-1)*sigma^2), J = sqrt(pi/2) *
mean |reaction| over that ticker's previous 8 prints (>= 4 required), sigma = sd of daily returns over
the 60 sessions before T-h; ATM put = 0.3989 * s * spot. Payoff max(0, -r). Score = payoff/price - 1.
Supported only if the primary mean > 0 with CR1 t >= 2, positive in each era (2011-15, 2016-20, 2021-26),
and still > 0 after the real-market surcharge k measured on this October's chains (below). A pass goes to
edge-refute before it is called anything.

**H3 - "TSMC fell, so the others will fall".** For each TSM print, the season = every EDGAR print in the
45 calendar days after TSM's reaction day. Supported only if the mean season reaction excess vs SPY after a
TSM down-day (excess < 0) is below the mean after a TSM up-day, difference t <= -2 (one value per season).

**Also reported, no bar:** shorting the stock instead (close[T-2] -> close[T]); 2025-26 only; real-chain
put results for every print 2026-09-24 .. 2026-10-16 with snapshots in stock-radar/data/chains_equity
(ask in at T-2, bid out at T, nearest expiry on or after T); k = real ATM put mid / model price.

## Luck count
Cells: H1 (2), H2 (3 entries x {all, beats, misses} = 9), H3 (1), short (1) = 13 looks. About 1 in 20
cells clears |t| 2 by luck; with 13 looks expect ~0.65 false passes.

## Prior (written before the run)
Earlier work on this universe: the announcement window T-1 -> T+1 carries a POSITIVE premium (+0.60, t 3.6,
earnings-runup-study) and implied > realized in every 0DTE bucket (zero-dte-lab). So I expect H2 to lose
roughly 10-25% of premium per trade at fair price and more at real prices, H1 to fail (beats rise more often
than they fall), and H3 to be flat.
