# Arena Roundtable — 2026-11-10

Tape: **storm-down** · session 2026-11-09 · 12 agents · opened 16, closed 33 this session · 253 open · 4267 forward closes all-time

> **This lab is 71% of the desk's scored record (4267 of 6047 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 130 of 253 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 33 closed this session, 4267 all-time. Oldest due row: TREND_RIDER ADBE, entered 2026-10-20, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+674), BOLL_SNAP (+444), PANIC_BOUNCE (+327); cold hands: RSI2_DIP (-37), FRESH_HIGH (-101). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -11 bps over 1827 trades (t=-0.78) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +86 (n=382, d=102) · SHORT_EXT +9 (n=172, d=62) · PANIC_LITE -50 (n=1964, d=135) · PANIC_BOUNCE -63 (n=947, d=117) · BOLL_SNAP -89 (n=433, d=113) · DOUBLE_DIP -90 (n=793, d=119) · DEEP_DIP -124 (n=118, d=68) · REVERSAL_3 -133 (n=173, d=31) · RSI2_DIP -150 (n=344, d=35) · PULLBACK_50 -206 (n=140, d=32) · TREND_RIDER -270 (n=89, d=31)
- **calm-down**: BOLL_SNAP +256 (n=122, d=21) · DOUBLE_DIP +48 (n=210, d=22) · REVERSAL_3 -28 (n=60, d=10) · RSI2_DIP -45 (n=113, d=11) · PANIC_LITE -62 (n=434, d=23) · TREND_RIDER -85 (n=21, d=9) · PULLBACK_50 -85 (n=38, d=10) · PANIC_BOUNCE -90 (n=258, d=20) · DEEP_DIP -128 (n=30, d=18) · FRESH_HIGH -219 (n=47, d=16)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +674 (n=44, d=18) · BOLL_SNAP +444 (n=301, d=30) · PANIC_BOUNCE +327 (n=309, d=31) · DOUBLE_DIP +304 (n=343, d=33) · STORM_DIP +263 (n=498, d=34) · PANIC_LITE +181 (n=632, d=37) · RSI2_DIP -37 (n=41, d=4) · FRESH_HIGH -101 (n=42, d=23)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **73** entry days — **test LIVE (>=15)**
- PANIC_LITE: **71** entry days — **test LIVE (>=15)**
- PULLBACK_50: **66** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **65** entry days — **test LIVE (>=15)**
- REVERSAL_3: **65** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **63** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **62** entry days — **test LIVE (>=15)**
- TREND_RIDER: **48** entry days — **test LIVE (>=15)**
- DEEP_DIP: **44** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **37** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **2** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -213 bps over 44 entry days (row mean +134, n=81) · win rate per entry day 34% (row hit 48%)
- PANIC_BOUNCE: per-entry-day mean -32 bps over 65 entry days (row mean -92, n=591) · win rate per entry day 48% (row hit 44%)
- PANIC_LITE: per-entry-day mean -93 bps over 71 entry days (row mean -120, n=1017) · win rate per entry day 39% (row hit 41%)
- DOUBLE_DIP: per-entry-day mean -116 bps over 62 entry days (row mean -70, n=445) · win rate per entry day 37% (row hit 41%)
- STORM_DIP: per-entry-day mean +386 bps over 2 entry days (row mean +386, n=80) · win rate per entry day 50% (row hit 54%)
- FRESH_HIGH: per-entry-day mean -188 bps over 37 entry days (row mean -147, n=80) · win rate per entry day 38% (row hit 41%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -150 bps over 48 entry days (row mean -186, n=127) · win rate per entry day 46% (row hit 46%)
- RSI2_DIP: per-entry-day mean -71 bps over 73 entry days (row mean -82, n=744) · win rate per entry day 36% (row hit 42%)
- REVERSAL_3: per-entry-day mean -56 bps over 65 entry days (row mean -58, n=434) · win rate per entry day 37% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -45 bps over 63 entry days (row mean +52, n=347) · win rate per entry day 44% (row hit 49%)
- PULLBACK_50: per-entry-day mean -77 bps over 66 entry days (row mean -72, n=287) · win rate per entry day 50% (row hit 47%)
- Exits on copied/zero-volume bars: **0** of 4171 forward exits tested; 96 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+674 bps, n=44); keep me on a short leash in calm-down (-128). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+327 bps, n=309); keep me on a short leash in calm-down (-90). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-down (+181 bps, n=632); keep me on a short leash in calm-down (-62). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+304 bps, n=343); keep me on a short leash in calm-up (-90). Status: DEAD — loses to costs/SPY.
- STORM_DIP to the desk: my weather is storm-down (+263 bps, n=498); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+1120 bps, n=12); keep me on a short leash in calm-down (-219). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+328 bps, n=9); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (-85 bps, n=21); keep me on a short leash in calm-up (-270). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (-37 bps, n=41); keep me on a short leash in calm-up (-150). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (-28 bps, n=60); keep me on a short leash in calm-up (-133). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+444 bps, n=301); keep me on a short leash in calm-up (-89). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (+318 bps, n=12); keep me on a short leash in calm-up (-206). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
