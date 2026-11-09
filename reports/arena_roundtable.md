# Arena Roundtable — 2026-11-09

Tape: **storm-down** · session 2026-11-06 · 12 agents · opened 55, closed 93 this session · 268 open · 4234 forward closes all-time

> **This lab is 71% of the desk's scored record (4234 of 5998 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 30 of 268 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 93 closed this session, 4234 all-time. Oldest due row: DEEP_DIP CVNA, entered 2026-10-26, hold 10, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+746), BOLL_SNAP (+486), DOUBLE_DIP (+338); cold hands: RSI2_DIP (-52), FRESH_HIGH (-99). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -11 bps over 1825 trades (t=-0.8) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +85 (n=382, d=102) · SHORT_EXT +9 (n=172, d=62) · PANIC_LITE -50 (n=1964, d=135) · PANIC_BOUNCE -63 (n=947, d=117) · BOLL_SNAP -89 (n=433, d=113) · DOUBLE_DIP -90 (n=793, d=119) · DEEP_DIP -124 (n=118, d=68) · REVERSAL_3 -133 (n=173, d=31) · RSI2_DIP -150 (n=344, d=35) · PULLBACK_50 -206 (n=140, d=32) · TREND_RIDER -266 (n=89, d=31)
- **calm-down**: BOLL_SNAP +253 (n=121, d=20) · DOUBLE_DIP +48 (n=210, d=22) · REVERSAL_3 -28 (n=56, d=9) · RSI2_DIP -47 (n=109, d=10) · PANIC_LITE -61 (n=432, d=22) · PULLBACK_50 -74 (n=38, d=10) · PANIC_BOUNCE -90 (n=258, d=20) · DEEP_DIP -108 (n=29, d=17) · FRESH_HIGH -216 (n=46, d=15)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +746 (n=44, d=18) · BOLL_SNAP +486 (n=300, d=30) · DOUBLE_DIP +338 (n=343, d=33) · PANIC_BOUNCE +316 (n=309, d=31) · STORM_DIP +274 (n=498, d=34) · PANIC_LITE +176 (n=632, d=37) · RSI2_DIP -52 (n=40, d=4) · FRESH_HIGH -99 (n=42, d=23)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **72** entry days — **test LIVE (>=15)**
- PANIC_LITE: **70** entry days — **test LIVE (>=15)**
- PULLBACK_50: **65** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **64** entry days — **test LIVE (>=15)**
- REVERSAL_3: **64** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **62** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **61** entry days — **test LIVE (>=15)**
- TREND_RIDER: **48** entry days — **test LIVE (>=15)**
- DEEP_DIP: **43** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **36** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **2** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -299 bps over 43 entry days (row mean +92, n=80) · win rate per entry day 33% (row hit 48%)
- PANIC_BOUNCE: per-entry-day mean -42 bps over 64 entry days (row mean -100, n=585) · win rate per entry day 47% (row hit 44%)
- PANIC_LITE: per-entry-day mean -101 bps over 70 entry days (row mean -124, n=1011) · win rate per entry day 39% (row hit 41%)
- DOUBLE_DIP: per-entry-day mean -106 bps over 61 entry days (row mean -66, n=442) · win rate per entry day 38% (row hit 41%)
- STORM_DIP: per-entry-day mean +386 bps over 2 entry days (row mean +386, n=80) · win rate per entry day 50% (row hit 54%)
- FRESH_HIGH: per-entry-day mean -163 bps over 36 entry days (row mean -135, n=79) · win rate per entry day 39% (row hit 42%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -150 bps over 48 entry days (row mean -186, n=127) · win rate per entry day 46% (row hit 46%)
- RSI2_DIP: per-entry-day mean -70 bps over 72 entry days (row mean -82, n=741) · win rate per entry day 36% (row hit 42%)
- REVERSAL_3: per-entry-day mean -62 bps over 64 entry days (row mean -60, n=432) · win rate per entry day 36% (row hit 43%)
- BOLL_SNAP: per-entry-day mean -54 bps over 62 entry days (row mean +38, n=337) · win rate per entry day 44% (row hit 48%)
- PULLBACK_50: per-entry-day mean -83 bps over 65 entry days (row mean -73, n=286) · win rate per entry day 49% (row hit 47%)
- Exits on copied/zero-volume bars: **0** of 4139 forward exits tested; 95 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+746 bps, n=44); keep me on a short leash in calm-up (-124). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+316 bps, n=309); keep me on a short leash in calm-down (-90). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-down (+176 bps, n=632); keep me on a short leash in calm-down (-61). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+338 bps, n=343); keep me on a short leash in calm-up (-90). Status: WATCH — positive but not significant.
- STORM_DIP to the desk: my weather is storm-down (+274 bps, n=498); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+1120 bps, n=12); keep me on a short leash in calm-down (-216). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+290 bps, n=9); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (-55 bps, n=19); keep me on a short leash in calm-up (-266). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (-47 bps, n=109); keep me on a short leash in calm-up (-150). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (-28 bps, n=56); keep me on a short leash in calm-up (-133). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+486 bps, n=300); keep me on a short leash in calm-up (-89). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (+341 bps, n=12); keep me on a short leash in calm-up (-206). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
