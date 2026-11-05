# Arena Roundtable — 2026-11-05

Tape: **calm-down** · session 2026-11-04 · 12 agents · opened 107, closed 140 this session · 217 open · 4099 forward closes all-time

> **This lab is 70% of the desk's scored record (4099 of 5837 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 217 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 140 closed this session, 4099 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-DOWN. Our pooled record in this weather — hot hands: BOLL_SNAP (+224), DEEP_DIP (+178), DOUBLE_DIP (+47); cold hands: RSI2_DIP (-36), FRESH_HIGH (-193). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -11 bps over 1801 trades (t=-0.82) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +45 (n=391, d=104) · SHORT_EXT +20 (n=172, d=65) · PANIC_LITE -54 (n=1990, d=138) · PANIC_BOUNCE -67 (n=956, d=120) · BOLL_SNAP -85 (n=447, d=116) · DOUBLE_DIP -93 (n=810, d=121) · DEEP_DIP -119 (n=120, d=69) · REVERSAL_3 -121 (n=186, d=34) · RSI2_DIP -128 (n=372, d=38) · PULLBACK_50 -173 (n=148, d=34) · TREND_RIDER -234 (n=94, d=34)
- **calm-down**: BOLL_SNAP +224 (n=114, d=19) · DEEP_DIP +178 (n=26, d=16) · DOUBLE_DIP +47 (n=208, d=21) · PULLBACK_50 +17 (n=35, d=9) · PANIC_LITE +5 (n=384, d=21) · PANIC_BOUNCE +2 (n=226, d=19) · REVERSAL_3 -2 (n=53, d=8) · RSI2_DIP -36 (n=104, d=9) · FRESH_HIGH -193 (n=40, d=14)
- **storm-up**: FRESH_HIGH +715 (n=21, d=3) · PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +900 (n=30, d=15) · BOLL_SNAP +379 (n=247, d=28) · DOUBLE_DIP +332 (n=287, d=31) · STORM_DIP +320 (n=439, d=32) · PANIC_BOUNCE +192 (n=255, d=30) · PANIC_LITE +129 (n=567, d=35) · FRESH_HIGH -173 (n=45, d=20)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **70** entry days — **test LIVE (>=15)**
- PANIC_LITE: **68** entry days — **test LIVE (>=15)**
- PULLBACK_50: **63** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **62** entry days — **test LIVE (>=15)**
- REVERSAL_3: **62** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **60** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **60** entry days — **test LIVE (>=15)**
- TREND_RIDER: **47** entry days — **test LIVE (>=15)**
- DEEP_DIP: **41** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **36** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **2** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -247 bps over 41 entry days (row mean +153, n=77) · win rate per entry day 34% (row hit 49%)
- PANIC_BOUNCE: per-entry-day mean -25 bps over 62 entry days (row mean -60, n=548) · win rate per entry day 48% (row hit 46%)
- PANIC_LITE: per-entry-day mean -73 bps over 68 entry days (row mean -93, n=971) · win rate per entry day 40% (row hit 42%)
- DOUBLE_DIP: per-entry-day mean -91 bps over 60 entry days (row mean -64, n=441) · win rate per entry day 38% (row hit 42%)
- STORM_DIP: per-entry-day mean +386 bps over 2 entry days (row mean +386, n=80) · win rate per entry day 50% (row hit 54%)
- FRESH_HIGH: per-entry-day mean -163 bps over 36 entry days (row mean -135, n=79) · win rate per entry day 39% (row hit 42%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -137 bps over 47 entry days (row mean -158, n=121) · win rate per entry day 47% (row hit 46%)
- RSI2_DIP: per-entry-day mean -62 bps over 70 entry days (row mean -73, n=719) · win rate per entry day 37% (row hit 42%)
- REVERSAL_3: per-entry-day mean -54 bps over 62 entry days (row mean -56, n=424) · win rate per entry day 37% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -43 bps over 60 entry days (row mean +50, n=328) · win rate per entry day 45% (row hit 48%)
- PULLBACK_50: per-entry-day mean -50 bps over 63 entry days (row mean -38, n=277) · win rate per entry day 51% (row hit 48%)
- Exits on copied/zero-volume bars: **0** of 3743 forward exits tested; 356 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+900 bps, n=30); keep me on a short leash in calm-up (-119). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+192 bps, n=255); keep me on a short leash in calm-up (-67). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+162 bps, n=98); keep me on a short leash in calm-up (-54). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+332 bps, n=287); keep me on a short leash in calm-up (-93). Status: DEAD — loses to costs/SPY.
- STORM_DIP to the desk: my weather is storm-down (+320 bps, n=439); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+715 bps, n=21); keep me on a short leash in calm-down (-193). Status: DEAD — loses to costs/SPY.
- SHORT_EXT to the desk: my weather is calm-up (+20 bps, n=172); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (-11 bps, n=10); keep me on a short leash in calm-up (-234). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+68 bps, n=19); keep me on a short leash in calm-up (-128). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is storm-down (+16 bps, n=11); keep me on a short leash in calm-up (-121). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+379 bps, n=247); keep me on a short leash in calm-up (-85). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+17 bps, n=35); keep me on a short leash in calm-up (-173). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
