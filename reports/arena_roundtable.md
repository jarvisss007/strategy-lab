# Arena Roundtable — 2026-10-27

Tape: **calm-down** · session 2026-10-26 · 12 agents · opened 53, closed 89 this session · 169 open · 3677 forward closes all-time

> **This lab is 70% of the desk's scored record (3677 of 5270 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 169 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 89 closed this session, 3677 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+270), BOLL_SNAP (+202), DOUBLE_DIP (+78); cold hands: RSI2_DIP (-11), FRESH_HIGH (-84). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +1 bps over 1800 trades (t=0.11) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +147 (n=411, d=106) · SHORT_EXT +27 (n=175, d=66) · PANIC_LITE -37 (n=2015, d=141) · PANIC_BOUNCE -54 (n=966, d=122) · BOLL_SNAP -85 (n=460, d=119) · DOUBLE_DIP -95 (n=826, d=124) · REVERSAL_3 -122 (n=225, d=38) · RSI2_DIP -136 (n=437, d=42) · PULLBACK_50 -148 (n=191, d=38) · DEEP_DIP -219 (n=123, d=72) · TREND_RIDER -243 (n=96, d=34)
- **calm-down**: DEEP_DIP +270 (n=24, d=15) · BOLL_SNAP +202 (n=101, d=17) · DOUBLE_DIP +78 (n=160, d=19) · PANIC_BOUNCE +48 (n=180, d=17) · REVERSAL_3 +41 (n=40, d=6) · PULLBACK_50 +35 (n=28, d=7) · PANIC_LITE +14 (n=318, d=19) · RSI2_DIP -11 (n=85, d=7) · FRESH_HIGH -84 (n=35, d=13)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +728 (n=29, d=17) · DOUBLE_DIP +386 (n=265, d=30) · BOLL_SNAP +376 (n=257, d=27) · STORM_DIP +341 (n=429, d=31) · PANIC_BOUNCE +189 (n=268, d=29) · PANIC_LITE +134 (n=590, d=34) · FRESH_HIGH -154 (n=36, d=20)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **63** entry days — **test LIVE (>=15)**
- PANIC_LITE: **61** entry days — **test LIVE (>=15)**
- PULLBACK_50: **59** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **55** entry days — **test LIVE (>=15)**
- REVERSAL_3: **55** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **55** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **54** entry days — **test LIVE (>=15)**
- TREND_RIDER: **42** entry days — **test LIVE (>=15)**
- DEEP_DIP: **35** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **32** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -200 bps over 35 entry days (row mean +240, n=67) · win rate per entry day 37% (row hit 54%)
- PANIC_BOUNCE: per-entry-day mean -6 bps over 55 entry days (row mean -35, n=492) · win rate per entry day 49% (row hit 48%)
- PANIC_LITE: per-entry-day mean -54 bps over 61 entry days (row mean -68, n=883) · win rate per entry day 41% (row hit 43%)
- DOUBLE_DIP: per-entry-day mean -92 bps over 54 entry days (row mean -81, n=367) · win rate per entry day 39% (row hit 41%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -222 bps over 32 entry days (row mean -175, n=73) · win rate per entry day 34% (row hit 37%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -146 bps over 42 entry days (row mean -152, n=111) · win rate per entry day 45% (row hit 46%)
- RSI2_DIP: per-entry-day mean -41 bps over 63 entry days (row mean -58, n=661) · win rate per entry day 40% (row hit 43%)
- REVERSAL_3: per-entry-day mean -40 bps over 55 entry days (row mean -51, n=391) · win rate per entry day 38% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -44 bps over 55 entry days (row mean +54, n=291) · win rate per entry day 47% (row hit 48%)
- PULLBACK_50: per-entry-day mean -52 bps over 59 entry days (row mean -39, n=267) · win rate per entry day 51% (row hit 47%)
- Exits on copied/zero-volume bars: **0** of 3504 forward exits tested; 173 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+728 bps, n=29); keep me on a short leash in calm-up (-219). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=268); keep me on a short leash in calm-up (-54). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+162 bps, n=98); keep me on a short leash in calm-up (-37). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+386 bps, n=265); keep me on a short leash in calm-up (-95). Status: WATCH — positive but not significant.
- STORM_DIP to the desk: my weather is storm-down (+341 bps, n=429); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+702 bps, n=11); keep me on a short leash in storm-down (-154). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+352 bps, n=10); keep me on a short leash in calm-down (-323). Status: WATCH — positive but not significant.
- TREND_RIDER to the desk: my weather is calm-down (+275 bps, n=8); keep me on a short leash in calm-up (-243). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (-11 bps, n=85); keep me on a short leash in calm-up (-136). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+41 bps, n=40); keep me on a short leash in calm-up (-122). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+376 bps, n=257); keep me on a short leash in calm-up (-85). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+35 bps, n=28); keep me on a short leash in calm-up (-148). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
