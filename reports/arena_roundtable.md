# Arena Roundtable — 2026-11-18

Tape: **storm-down** · session 2026-11-18 · 12 agents · opened 84, closed 128 this session · 251 open · 4744 forward closes all-time

> **This lab is 71% of the desk's scored record (4616 of 6459 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 251 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 128 closed this session, 4744 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+753), BOLL_SNAP (+412), DOUBLE_DIP (+297); cold hands: RSI2_DIP (-2), FRESH_HIGH (-139). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 44% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -19 bps over 1858 trades (t=-1.42) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +92 (n=339, d=95) · SHORT_EXT +2 (n=167, d=59) · BOLL_SNAP -15 (n=400, d=106) · PANIC_LITE -45 (n=1844, d=128) · DOUBLE_DIP -53 (n=733, d=112) · PANIC_BOUNCE -58 (n=872, d=110) · DEEP_DIP -178 (n=118, d=63) · RSI2_DIP -183 (n=257, d=29) · REVERSAL_3 -225 (n=125, d=24) · PULLBACK_50 -246 (n=109, d=26) · TREND_RIDER -391 (n=71, d=25)
- **calm-down**: BOLL_SNAP +224 (n=125, d=23) · REVERSAL_3 -7 (n=62, d=12) · TREND_RIDER -22 (n=29, d=12) · RSI2_DIP -82 (n=139, d=15) · DOUBLE_DIP -111 (n=246, d=26) · PANIC_LITE -124 (n=512, d=27) · PULLBACK_50 -141 (n=46, d=13) · PANIC_BOUNCE -160 (n=290, d=24) · FRESH_HIGH -234 (n=53, d=17) · DEEP_DIP -282 (n=33, d=20)
- **storm-up**: FRESH_HIGH +782 (n=21, d=3) · PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +114 (n=53, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +753 (n=46, d=20) · BOLL_SNAP +412 (n=313, d=32) · DOUBLE_DIP +297 (n=373, d=35) · PANIC_BOUNCE +265 (n=343, d=33) · STORM_DIP +217 (n=562, d=36) · PANIC_LITE +144 (n=689, d=39) · PULLBACK_50 +82 (n=25, d=6) · REVERSAL_3 +12 (n=25, d=6) · RSI2_DIP -2 (n=65, d=6) · FRESH_HIGH -139 (n=43, d=23)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **80** entry days — **test LIVE (>=15)**
- PANIC_LITE: **78** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **72** entry days — **test LIVE (>=15)**
- REVERSAL_3: **70** entry days — **test LIVE (>=15)**
- PULLBACK_50: **70** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **69** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **69** entry days — **test LIVE (>=15)**
- TREND_RIDER: **55** entry days — **test LIVE (>=15)**
- DEEP_DIP: **48** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **41** entry days — **test LIVE (>=15)**
- SHORT_EXT: **20** entry days — **test LIVE (>=15)**
- STORM_DIP: **3** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -345 bps over 48 entry days (row mean -56, n=92) · win rate per entry day 31% (row hit 42%)
- PANIC_BOUNCE: per-entry-day mean -53 bps over 72 entry days (row mean -132, n=664) · win rate per entry day 46% (row hit 42%)
- PANIC_LITE: per-entry-day mean -108 bps over 78 entry days (row mean -138, n=1135) · win rate per entry day 38% (row hit 40%)
- DOUBLE_DIP: per-entry-day mean -142 bps over 69 entry days (row mean -66, n=522) · win rate per entry day 38% (row hit 42%)
- STORM_DIP: per-entry-day mean +525 bps over 3 entry days (row mean +525, n=120) · win rate per entry day 67% (row hit 65%)
- FRESH_HIGH: per-entry-day mean -180 bps over 41 entry days (row mean -156, n=93) · win rate per entry day 39% (row hit 43%)
- SHORT_EXT: per-entry-day mean +161 bps over 20 entry days (row mean +169, n=36) · win rate per entry day 55% (row hit 53%)
- TREND_RIDER: per-entry-day mean -269 bps over 55 entry days (row mean -267, n=141) · win rate per entry day 42% (row hit 43%)
- RSI2_DIP: per-entry-day mean -62 bps over 80 entry days (row mean -73, n=804) · win rate per entry day 38% (row hit 43%)
- REVERSAL_3: per-entry-day mean -37 bps over 70 entry days (row mean -52, n=449) · win rate per entry day 39% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -54 bps over 69 entry days (row mean +112, n=385) · win rate per entry day 45% (row hit 52%)
- PULLBACK_50: per-entry-day mean -56 bps over 70 entry days (row mean -52, n=303) · win rate per entry day 53% (row hit 48%)
- Exits on copied/zero-volume bars: **0** of 4492 forward exits tested; 252 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+753 bps, n=46); keep me on a short leash in calm-down (-282). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+265 bps, n=343); keep me on a short leash in calm-down (-160). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+162 bps, n=98); keep me on a short leash in calm-down (-124). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+297 bps, n=373); keep me on a short leash in calm-down (-111). Status: WATCH — positive but not significant.
- STORM_DIP to the desk: my weather is storm-down (+217 bps, n=562); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+782 bps, n=21); keep me on a short leash in calm-down (-234). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+369 bps, n=10); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (-22 bps, n=29); keep me on a short leash in calm-up (-391). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (-2 bps, n=65); keep me on a short leash in calm-up (-183). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is storm-down (+12 bps, n=25); keep me on a short leash in calm-up (-225). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+412 bps, n=313); keep me on a short leash in storm-up (-72). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (+82 bps, n=25); keep me on a short leash in calm-up (-246). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
