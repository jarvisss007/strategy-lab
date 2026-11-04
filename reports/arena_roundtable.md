# Arena Roundtable — 2026-11-04

Tape: **storm-down** · session 2026-11-03 · 12 agents · opened 31, closed 79 this session · 250 open · 3981 forward closes all-time

> **This lab is 70% of the desk's scored record (3981 of 5686 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 250 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 79 closed this session, 3981 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+1053), DOUBLE_DIP (+368), BOLL_SNAP (+354); cold hands: PANIC_LITE (+132), FRESH_HIGH (+23). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -8 bps over 1813 trades (t=-0.6) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +53 (n=378, d=105) · SHORT_EXT +20 (n=171, d=64) · PANIC_LITE -54 (n=1984, d=138) · PANIC_BOUNCE -67 (n=956, d=120) · DEEP_DIP -76 (n=128, d=72) · BOLL_SNAP -88 (n=438, d=116) · DOUBLE_DIP -93 (n=809, d=121) · REVERSAL_3 -108 (n=195, d=35) · RSI2_DIP -111 (n=389, d=39) · PULLBACK_50 -154 (n=152, d=35) · TREND_RIDER -242 (n=96, d=34)
- **calm-down**: DEEP_DIP +211 (n=26, d=15) · BOLL_SNAP +208 (n=114, d=19) · DOUBLE_DIP +93 (n=208, d=21) · PULLBACK_50 +24 (n=35, d=9) · PANIC_LITE +5 (n=384, d=21) · PANIC_BOUNCE +2 (n=226, d=19) · REVERSAL_3 -2 (n=53, d=8) · RSI2_DIP -25 (n=104, d=9) · FRESH_HIGH -173 (n=40, d=14)
- **storm-up**: FRESH_HIGH +746 (n=20, d=3) · PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +1053 (n=34, d=15) · DOUBLE_DIP +368 (n=287, d=31) · BOLL_SNAP +354 (n=272, d=28) · STORM_DIP +335 (n=464, d=32) · PANIC_BOUNCE +187 (n=273, d=30) · PANIC_LITE +132 (n=603, d=35) · FRESH_HIGH +23 (n=55, d=21)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **70** entry days — **test LIVE (>=15)**
- PANIC_LITE: **67** entry days — **test LIVE (>=15)**
- REVERSAL_3: **62** entry days — **test LIVE (>=15)**
- PULLBACK_50: **62** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **61** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **60** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **59** entry days — **test LIVE (>=15)**
- TREND_RIDER: **46** entry days — **test LIVE (>=15)**
- DEEP_DIP: **40** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **37** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -255 bps over 40 entry days (row mean +154, n=76) · win rate per entry day 32% (row hit 49%)
- PANIC_BOUNCE: per-entry-day mean -24 bps over 61 entry days (row mean -60, n=540) · win rate per entry day 49% (row hit 46%)
- PANIC_LITE: per-entry-day mean -71 bps over 67 entry days (row mean -91, n=949) · win rate per entry day 40% (row hit 43%)
- DOUBLE_DIP: per-entry-day mean -86 bps over 59 entry days (row mean -31, n=402) · win rate per entry day 39% (row hit 44%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -153 bps over 37 entry days (row mean -137, n=81) · win rate per entry day 38% (row hit 41%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -148 bps over 46 entry days (row mean -162, n=120) · win rate per entry day 46% (row hit 46%)
- RSI2_DIP: per-entry-day mean -55 bps over 70 entry days (row mean -68, n=719) · win rate per entry day 37% (row hit 43%)
- REVERSAL_3: per-entry-day mean -50 bps over 62 entry days (row mean -53, n=424) · win rate per entry day 39% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -42 bps over 60 entry days (row mean +57, n=321) · win rate per entry day 45% (row hit 49%)
- PULLBACK_50: per-entry-day mean -42 bps over 62 entry days (row mean -31, n=275) · win rate per entry day 52% (row hit 48%)
- Exits on copied/zero-volume bars: **0** of 3759 forward exits tested; 222 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+1053 bps, n=34); keep me on a short leash in calm-up (-76). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+187 bps, n=273); keep me on a short leash in calm-up (-67). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+162 bps, n=98); keep me on a short leash in calm-up (-54). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+368 bps, n=287); keep me on a short leash in calm-up (-93). Status: WATCH — positive but not significant.
- STORM_DIP to the desk: my weather is storm-down (+335 bps, n=464); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+746 bps, n=20); keep me on a short leash in calm-down (-173). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+382 bps, n=9); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+5 bps, n=10); keep me on a short leash in calm-up (-242). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+33 bps, n=10); keep me on a short leash in calm-up (-111). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (-2 bps, n=53); keep me on a short leash in calm-up (-108). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+354 bps, n=272); keep me on a short leash in calm-up (-88). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+24 bps, n=35); keep me on a short leash in calm-up (-154). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
