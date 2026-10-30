# Arena Roundtable — 2026-10-29

Tape: **calm-up** · session 2026-10-29 · 12 agents · opened 63, closed 47 this session · 142 open · 3822 forward closes all-time

> **This lab is 70% of the desk's scored record (3776 of 5430 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 142 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 47 closed this session, 3822 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+113), SHORT_EXT (+14), PANIC_LITE (-38); cold hands: TREND_RIDER (-177), DEEP_DIP (-205). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +2 bps over 1794 trades (t=0.19) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +113 (n=406, d=103) · SHORT_EXT +14 (n=174, d=66) · PANIC_LITE -38 (n=1999, d=140) · PANIC_BOUNCE -56 (n=960, d=122) · BOLL_SNAP -84 (n=460, d=118) · DOUBLE_DIP -97 (n=820, d=122) · REVERSAL_3 -101 (n=226, d=38) · PULLBACK_50 -111 (n=173, d=37) · RSI2_DIP -131 (n=419, d=42) · TREND_RIDER -177 (n=93, d=35) · DEEP_DIP -205 (n=120, d=71)
- **calm-down**: DEEP_DIP +474 (n=25, d=16) · BOLL_SNAP +244 (n=104, d=18) · DOUBLE_DIP +171 (n=166, d=20) · PULLBACK_50 +62 (n=31, d=8) · REVERSAL_3 +54 (n=44, d=7) · PANIC_BOUNCE +46 (n=182, d=18) · PANIC_LITE +20 (n=327, d=20) · RSI2_DIP +10 (n=96, d=8) · FRESH_HIGH -96 (n=35, d=13)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +808 (n=35, d=18) · DOUBLE_DIP +386 (n=265, d=30) · BOLL_SNAP +374 (n=253, d=27) · STORM_DIP +341 (n=429, d=31) · PANIC_BOUNCE +189 (n=268, d=29) · PANIC_LITE +134 (n=588, d=34) · FRESH_HIGH -100 (n=35, d=20)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **66** entry days — **test LIVE (>=15)**
- PANIC_LITE: **64** entry days — **test LIVE (>=15)**
- PULLBACK_50: **60** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **58** entry days — **test LIVE (>=15)**
- REVERSAL_3: **58** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **57** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **57** entry days — **test LIVE (>=15)**
- TREND_RIDER: **44** entry days — **test LIVE (>=15)**
- DEEP_DIP: **38** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **35** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -229 bps over 38 entry days (row mean +193, n=72) · win rate per entry day 34% (row hit 51%)
- PANIC_BOUNCE: per-entry-day mean +12 bps over 58 entry days (row mean -29, n=499) · win rate per entry day 52% (row hit 48%)
- PANIC_LITE: per-entry-day mean -43 bps over 64 entry days (row mean -60, n=904) · win rate per entry day 42% (row hit 44%)
- DOUBLE_DIP: per-entry-day mean -68 bps over 57 entry days (row mean -28, n=399) · win rate per entry day 40% (row hit 44%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -197 bps over 35 entry days (row mean -162, n=78) · win rate per entry day 34% (row hit 38%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -144 bps over 44 entry days (row mean -153, n=116) · win rate per entry day 46% (row hit 46%)
- RSI2_DIP: per-entry-day mean -42 bps over 66 entry days (row mean -57, n=693) · win rate per entry day 39% (row hit 43%)
- REVERSAL_3: per-entry-day mean -38 bps over 58 entry days (row mean -46, n=406) · win rate per entry day 40% (row hit 45%)
- BOLL_SNAP: per-entry-day mean -23 bps over 57 entry days (row mean +74, n=311) · win rate per entry day 47% (row hit 50%)
- PULLBACK_50: per-entry-day mean -44 bps over 60 entry days (row mean -34, n=270) · win rate per entry day 52% (row hit 47%)
- Exits on copied/zero-volume bars: **0** of 3504 forward exits tested; 318 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+808 bps, n=35); keep me on a short leash in calm-up (-205). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=268); keep me on a short leash in calm-up (-56). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+162 bps, n=98); keep me on a short leash in calm-up (-38). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+386 bps, n=265); keep me on a short leash in calm-up (-97). Status: WATCH — positive but not significant.
- STORM_DIP to the desk: my weather is storm-down (+341 bps, n=429); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+944 bps, n=14); keep me on a short leash in storm-down (-100). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+689 bps, n=8); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+294 bps, n=11); keep me on a short leash in calm-up (-177). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (+10 bps, n=96); keep me on a short leash in calm-up (-131). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+54 bps, n=44); keep me on a short leash in calm-up (-101). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+374 bps, n=253); keep me on a short leash in calm-up (-84). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+62 bps, n=31); keep me on a short leash in calm-up (-111). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
