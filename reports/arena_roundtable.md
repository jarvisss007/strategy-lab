# Arena Roundtable — 2026-10-30

Tape: **storm-down** · session 2026-10-30 · 12 agents · opened 171, closed 29 this session · 284 open · 3851 forward closes all-time

> **This lab is 70% of the desk's scored record (3822 of 5492 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 284 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 29 closed this session, 3851 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+823), DOUBLE_DIP (+382), BOLL_SNAP (+369); cold hands: PANIC_LITE (+134), FRESH_HIGH (-142). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -7 bps over 1801 trades (t=-0.52) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +89 (n=405, d=105) · SHORT_EXT +26 (n=173, d=65) · PANIC_LITE -49 (n=2010, d=140) · PANIC_BOUNCE -62 (n=965, d=122) · BOLL_SNAP -90 (n=456, d=118) · DOUBLE_DIP -96 (n=812, d=122) · REVERSAL_3 -114 (n=218, d=37) · RSI2_DIP -115 (n=416, d=42) · PULLBACK_50 -130 (n=163, d=37) · DEEP_DIP -179 (n=123, d=73) · TREND_RIDER -256 (n=98, d=35)
- **calm-down**: DEEP_DIP +312 (n=24, d=15) · BOLL_SNAP +243 (n=104, d=18) · DOUBLE_DIP +170 (n=166, d=20) · PULLBACK_50 +68 (n=31, d=8) · REVERSAL_3 +54 (n=44, d=7) · PANIC_BOUNCE +46 (n=182, d=18) · PANIC_LITE +20 (n=327, d=20) · RSI2_DIP +10 (n=96, d=8) · FRESH_HIGH -112 (n=36, d=13)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +823 (n=35, d=19) · DOUBLE_DIP +382 (n=266, d=30) · BOLL_SNAP +369 (n=255, d=27) · STORM_DIP +341 (n=429, d=31) · PANIC_BOUNCE +189 (n=268, d=29) · PANIC_LITE +134 (n=588, d=34) · FRESH_HIGH -142 (n=38, d=21)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **67** entry days — **test LIVE (>=15)**
- PANIC_LITE: **65** entry days — **test LIVE (>=15)**
- PULLBACK_50: **60** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **59** entry days — **test LIVE (>=15)**
- REVERSAL_3: **59** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **58** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **58** entry days — **test LIVE (>=15)**
- TREND_RIDER: **45** entry days — **test LIVE (>=15)**
- DEEP_DIP: **39** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **36** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -232 bps over 39 entry days (row mean +171, n=75) · win rate per entry day 33% (row hit 49%)
- PANIC_BOUNCE: per-entry-day mean +1 bps over 59 entry days (row mean -30, n=500) · win rate per entry day 51% (row hit 48%)
- PANIC_LITE: per-entry-day mean -53 bps over 65 entry days (row mean -64, n=909) · win rate per entry day 42% (row hit 43%)
- DOUBLE_DIP: per-entry-day mean -71 bps over 58 entry days (row mean -29, n=401) · win rate per entry day 40% (row hit 44%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -184 bps over 36 entry days (row mean -151, n=80) · win rate per entry day 36% (row hit 40%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -155 bps over 45 entry days (row mean -166, n=119) · win rate per entry day 44% (row hit 45%)
- RSI2_DIP: per-entry-day mean -42 bps over 67 entry days (row mean -57, n=699) · win rate per entry day 39% (row hit 43%)
- REVERSAL_3: per-entry-day mean -42 bps over 59 entry days (row mean -48, n=409) · win rate per entry day 39% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -26 bps over 58 entry days (row mean +70, n=315) · win rate per entry day 47% (row hit 49%)
- PULLBACK_50: per-entry-day mean -44 bps over 60 entry days (row mean -34, n=270) · win rate per entry day 52% (row hit 47%)
- Exits on copied/zero-volume bars: **0** of 3504 forward exits tested; 347 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+823 bps, n=35); keep me on a short leash in calm-up (-179). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=268); keep me on a short leash in calm-up (-62). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+162 bps, n=98); keep me on a short leash in calm-up (-49). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+382 bps, n=266); keep me on a short leash in calm-up (-96). Status: WATCH — positive but not significant.
- STORM_DIP to the desk: my weather is storm-down (+341 bps, n=429); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+842 bps, n=16); keep me on a short leash in storm-down (-142). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+511 bps, n=8); keep me on a short leash in calm-down (-323). Status: WATCH — positive but not significant.
- TREND_RIDER to the desk: my weather is calm-down (+158 bps, n=11); keep me on a short leash in calm-up (-256). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (+10 bps, n=96); keep me on a short leash in calm-up (-115). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+54 bps, n=44); keep me on a short leash in calm-up (-114). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+369 bps, n=255); keep me on a short leash in calm-up (-90). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+68 bps, n=31); keep me on a short leash in calm-up (-130). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
