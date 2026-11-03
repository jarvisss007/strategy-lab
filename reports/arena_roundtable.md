# Arena Roundtable — 2026-11-03

Tape: **storm-down** · session 2026-11-02 · 12 agents · opened 63, closed 45 this session · 304 open · 3896 forward closes all-time

> **This lab is 70% of the desk's scored record (3896 of 5588 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 79 of 304 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 45 closed this session, 3896 all-time. Oldest due row: DEEP_DIP TSEM, entered 2026-10-20, hold 10, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+808), DOUBLE_DIP (+377), BOLL_SNAP (+363); cold hands: PANIC_LITE (+135), FRESH_HIGH (-132). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -5 bps over 1820 trades (t=-0.39) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +93 (n=392, d=105) · SHORT_EXT +27 (n=173, d=64) · PANIC_LITE -53 (n=1995, d=139) · PANIC_BOUNCE -66 (n=960, d=121) · BOLL_SNAP -88 (n=450, d=117) · DOUBLE_DIP -92 (n=811, d=122) · RSI2_DIP -116 (n=396, d=40) · REVERSAL_3 -120 (n=199, d=35) · PULLBACK_50 -154 (n=154, d=36) · DEEP_DIP -190 (n=127, d=79) · TREND_RIDER -236 (n=98, d=35)
- **calm-down**: DEEP_DIP +283 (n=28, d=16) · BOLL_SNAP +212 (n=114, d=19) · DOUBLE_DIP +100 (n=208, d=21) · PULLBACK_50 +23 (n=35, d=9) · PANIC_LITE +18 (n=384, d=21) · PANIC_BOUNCE +11 (n=226, d=19) · REVERSAL_3 +9 (n=53, d=8) · RSI2_DIP -22 (n=104, d=9) · FRESH_HIGH -203 (n=39, d=14)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +808 (n=37, d=17) · DOUBLE_DIP +377 (n=287, d=31) · BOLL_SNAP +363 (n=264, d=28) · STORM_DIP +339 (n=464, d=32) · PANIC_BOUNCE +190 (n=273, d=30) · PANIC_LITE +135 (n=602, d=35) · FRESH_HIGH -132 (n=49, d=22)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **68** entry days — **test LIVE (>=15)**
- PANIC_LITE: **66** entry days — **test LIVE (>=15)**
- PULLBACK_50: **61** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **60** entry days — **test LIVE (>=15)**
- REVERSAL_3: **60** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **58** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **58** entry days — **test LIVE (>=15)**
- TREND_RIDER: **46** entry days — **test LIVE (>=15)**
- DEEP_DIP: **39** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **36** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -232 bps over 39 entry days (row mean +171, n=75) · win rate per entry day 33% (row hit 49%)
- PANIC_BOUNCE: per-entry-day mean -21 bps over 60 entry days (row mean -51, n=508) · win rate per entry day 50% (row hit 47%)
- PANIC_LITE: per-entry-day mean -71 bps over 66 entry days (row mean -91, n=931) · win rate per entry day 41% (row hit 43%)
- DOUBLE_DIP: per-entry-day mean -71 bps over 58 entry days (row mean -29, n=401) · win rate per entry day 40% (row hit 44%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -184 bps over 36 entry days (row mean -151, n=80) · win rate per entry day 36% (row hit 40%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -148 bps over 46 entry days (row mean -162, n=120) · win rate per entry day 46% (row hit 46%)
- RSI2_DIP: per-entry-day mean -46 bps over 68 entry days (row mean -59, n=707) · win rate per entry day 38% (row hit 43%)
- REVERSAL_3: per-entry-day mean -50 bps over 60 entry days (row mean -51, n=412) · win rate per entry day 38% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -26 bps over 58 entry days (row mean +70, n=315) · win rate per entry day 47% (row hit 49%)
- PULLBACK_50: per-entry-day mean -35 bps over 61 entry days (row mean -28, n=273) · win rate per entry day 52% (row hit 48%)
- Exits on copied/zero-volume bars: **0** of 3759 forward exits tested; 137 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+808 bps, n=37); keep me on a short leash in calm-up (-190). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+190 bps, n=273); keep me on a short leash in calm-up (-66). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+162 bps, n=98); keep me on a short leash in calm-up (-53). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+377 bps, n=287); keep me on a short leash in calm-up (-92). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+339 bps, n=464); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+815 bps, n=17); keep me on a short leash in calm-down (-203). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+511 bps, n=8); keep me on a short leash in calm-down (-323). Status: WATCH — positive but not significant.
- TREND_RIDER to the desk: my weather is calm-down (+46 bps, n=10); keep me on a short leash in calm-up (-236). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+78 bps, n=10); keep me on a short leash in calm-up (-116). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+9 bps, n=53); keep me on a short leash in calm-up (-120). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+363 bps, n=264); keep me on a short leash in calm-up (-88). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+23 bps, n=35); keep me on a short leash in calm-up (-154). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
