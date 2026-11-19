# Arena Roundtable — 2026-11-19

Tape: **storm-down** · session 2026-11-18 · 12 agents · opened 84, closed 130 this session · 248 open · 4746 forward closes all-time

> **This lab is 72% of the desk's scored record (4746 of 6612 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 82 of 248 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 130 closed this session, 4746 all-time. Oldest due row: TREND_RIDER JPM, entered 2026-10-29, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+783), BOLL_SNAP (+391), DOUBLE_DIP (+305); cold hands: PULLBACK_50 (-64), FRESH_HIGH (-98). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 44% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -19 bps over 1853 trades (t=-1.45) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +71 (n=336, d=95) · SHORT_EXT +19 (n=160, d=59) · BOLL_SNAP -17 (n=398, d=106) · PANIC_LITE -47 (n=1819, d=128) · DOUBLE_DIP -53 (n=721, d=112) · PANIC_BOUNCE -61 (n=855, d=109) · RSI2_DIP -175 (n=252, d=28) · DEEP_DIP -190 (n=116, d=62) · REVERSAL_3 -222 (n=121, d=24) · PULLBACK_50 -251 (n=106, d=24) · TREND_RIDER -395 (n=71, d=25)
- **calm-down**: BOLL_SNAP +218 (n=124, d=23) · REVERSAL_3 -7 (n=62, d=12) · TREND_RIDER -46 (n=29, d=12) · RSI2_DIP -86 (n=138, d=15) · DOUBLE_DIP -112 (n=241, d=26) · PANIC_LITE -114 (n=505, d=27) · PULLBACK_50 -132 (n=46, d=13) · PANIC_BOUNCE -149 (n=284, d=24) · DEEP_DIP -248 (n=32, d=19) · FRESH_HIGH -252 (n=53, d=17)
- **storm-up**: FRESH_HIGH +695 (n=20, d=3) · PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +117 (n=68, d=4) · DOUBLE_DIP +106 (n=52, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -305 (n=88, d=4)
- **storm-down**: DEEP_DIP +783 (n=46, d=20) · BOLL_SNAP +391 (n=320, d=33) · DOUBLE_DIP +305 (n=375, d=35) · PANIC_BOUNCE +252 (n=339, d=34) · STORM_DIP +224 (n=558, d=37) · PANIC_LITE +133 (n=691, d=40) · REVERSAL_3 -37 (n=37, d=7) · RSI2_DIP -38 (n=74, d=7) · PULLBACK_50 -64 (n=32, d=7) · FRESH_HIGH -98 (n=42, d=23)

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
- RSI2_DIP: per-entry-day mean -62 bps over 80 entry days (row mean -73, n=805) · win rate per entry day 38% (row hit 43%)
- REVERSAL_3: per-entry-day mean -37 bps over 70 entry days (row mean -52, n=450) · win rate per entry day 39% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -54 bps over 69 entry days (row mean +112, n=385) · win rate per entry day 45% (row hit 52%)
- PULLBACK_50: per-entry-day mean -56 bps over 70 entry days (row mean -52, n=303) · win rate per entry day 53% (row hit 48%)
- Exits on copied/zero-volume bars: **0** of 4492 forward exits tested; 254 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+783 bps, n=46); keep me on a short leash in calm-down (-248). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+252 bps, n=339); keep me on a short leash in calm-down (-149). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+162 bps, n=98); keep me on a short leash in calm-down (-114). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+305 bps, n=375); keep me on a short leash in calm-down (-112). Status: WATCH — positive but not significant.
- STORM_DIP to the desk: my weather is storm-down (+224 bps, n=558); keep me on a short leash in storm-up (-305). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+695 bps, n=20); keep me on a short leash in calm-down (-252). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+423 bps, n=9); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (-46 bps, n=29); keep me on a short leash in calm-up (-395). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (-38 bps, n=74); keep me on a short leash in calm-up (-175). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (-7 bps, n=62); keep me on a short leash in calm-up (-222). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+391 bps, n=320); keep me on a short leash in storm-up (-72). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (-64 bps, n=32); keep me on a short leash in calm-up (-251). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
