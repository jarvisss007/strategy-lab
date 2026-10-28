# Arena Roundtable — 2026-10-28

Tape: **calm-up** · session 2026-10-27 · 12 agents · opened 31, closed 39 this session · 160 open · 3718 forward closes all-time

> **This lab is 70% of the desk's scored record (3718 of 5337 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 57 of 160 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 39 closed this session, 3718 all-time. Oldest due row: TREND_RIDER AMZN, entered 2026-10-07, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+139), SHORT_EXT (+23), PANIC_LITE (-38); cold hands: TREND_RIDER (-176), DEEP_DIP (-181). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +2 bps over 1804 trades (t=0.12) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +139 (n=412, d=106) · SHORT_EXT +23 (n=175, d=66) · PANIC_LITE -38 (n=2014, d=141) · PANIC_BOUNCE -55 (n=968, d=123) · BOLL_SNAP -85 (n=463, d=119) · DOUBLE_DIP -96 (n=825, d=124) · REVERSAL_3 -116 (n=233, d=38) · RSI2_DIP -134 (n=440, d=42) · PULLBACK_50 -146 (n=189, d=38) · TREND_RIDER -176 (n=92, d=35) · DEEP_DIP -181 (n=123, d=73)
- **calm-down**: DEEP_DIP +406 (n=25, d=16) · BOLL_SNAP +238 (n=104, d=18) · DOUBLE_DIP +152 (n=166, d=20) · PANIC_BOUNCE +47 (n=182, d=18) · REVERSAL_3 +42 (n=44, d=7) · PULLBACK_50 +34 (n=31, d=8) · PANIC_LITE +15 (n=327, d=20) · RSI2_DIP -6 (n=96, d=8) · FRESH_HIGH -86 (n=35, d=13)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +633 (n=30, d=17) · DOUBLE_DIP +386 (n=265, d=30) · BOLL_SNAP +376 (n=257, d=27) · STORM_DIP +341 (n=429, d=31) · PANIC_BOUNCE +189 (n=268, d=29) · PANIC_LITE +134 (n=590, d=34) · FRESH_HIGH -151 (n=33, d=20)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **65** entry days — **test LIVE (>=15)**
- PANIC_LITE: **62** entry days — **test LIVE (>=15)**
- PULLBACK_50: **59** entry days — **test LIVE (>=15)**
- REVERSAL_3: **57** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **56** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **55** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **55** entry days — **test LIVE (>=15)**
- TREND_RIDER: **43** entry days — **test LIVE (>=15)**
- DEEP_DIP: **36** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **33** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -229 bps over 36 entry days (row mean +218, n=68) · win rate per entry day 36% (row hit 53%)
- PANIC_BOUNCE: per-entry-day mean -1 bps over 56 entry days (row mean -34, n=494) · win rate per entry day 50% (row hit 48%)
- PANIC_LITE: per-entry-day mean -56 bps over 62 entry days (row mean -69, n=890) · win rate per entry day 40% (row hit 43%)
- DOUBLE_DIP: per-entry-day mean -84 bps over 55 entry days (row mean -75, n=372) · win rate per entry day 40% (row hit 41%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -217 bps over 33 entry days (row mean -171, n=75) · win rate per entry day 33% (row hit 37%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -155 bps over 43 entry days (row mean -162, n=114) · win rate per entry day 44% (row hit 46%)
- RSI2_DIP: per-entry-day mean -42 bps over 65 entry days (row mean -60, n=670) · win rate per entry day 40% (row hit 43%)
- REVERSAL_3: per-entry-day mean -39 bps over 57 entry days (row mean -51, n=394) · win rate per entry day 39% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -36 bps over 55 entry days (row mean +69, n=300) · win rate per entry day 47% (row hit 49%)
- PULLBACK_50: per-entry-day mean -52 bps over 59 entry days (row mean -39, n=267) · win rate per entry day 51% (row hit 47%)
- Exits on copied/zero-volume bars: **0** of 3504 forward exits tested; 214 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+633 bps, n=30); keep me on a short leash in calm-up (-181). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=268); keep me on a short leash in calm-up (-55). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+162 bps, n=98); keep me on a short leash in calm-up (-38). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+386 bps, n=265); keep me on a short leash in calm-up (-96). Status: WATCH — positive but not significant.
- STORM_DIP to the desk: my weather is storm-down (+341 bps, n=429); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+696 bps, n=12); keep me on a short leash in storm-down (-151). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+463 bps, n=9); keep me on a short leash in calm-down (-233). Status: WATCH — positive but not significant.
- TREND_RIDER to the desk: my weather is calm-down (+248 bps, n=12); keep me on a short leash in calm-up (-176). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (-6 bps, n=96); keep me on a short leash in calm-up (-134). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+42 bps, n=44); keep me on a short leash in calm-up (-116). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+376 bps, n=257); keep me on a short leash in calm-up (-85). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+34 bps, n=31); keep me on a short leash in calm-up (-146). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
