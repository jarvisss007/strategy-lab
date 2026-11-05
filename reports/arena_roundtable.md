# Arena Roundtable — 2026-11-05

Tape: **storm-down** · session 2026-11-05 · 12 agents · opened 130, closed 42 this session · 304 open · 4141 forward closes all-time

> **This lab is 70% of the desk's scored record (4099 of 5846 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 304 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 42 closed this session, 4141 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+753), BOLL_SNAP (+355), DOUBLE_DIP (+234); cold hands: PANIC_LITE (+127), FRESH_HIGH (-163). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -22 bps over 1812 trades (t=-1.58) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +38 (n=394, d=105) · SHORT_EXT +9 (n=173, d=64) · PANIC_LITE -55 (n=1979, d=137) · PANIC_BOUNCE -68 (n=953, d=119) · DOUBLE_DIP -87 (n=798, d=121) · BOLL_SNAP -88 (n=441, d=115) · REVERSAL_3 -125 (n=182, d=33) · RSI2_DIP -146 (n=361, d=37) · DEEP_DIP -155 (n=118, d=69) · PULLBACK_50 -194 (n=148, d=34) · TREND_RIDER -342 (n=93, d=33)
- **calm-down**: BOLL_SNAP +163 (n=121, d=20) · DOUBLE_DIP +44 (n=210, d=22) · REVERSAL_3 -28 (n=56, d=9) · RSI2_DIP -68 (n=109, d=10) · PULLBACK_50 -94 (n=38, d=10) · PANIC_LITE -118 (n=432, d=22) · PANIC_BOUNCE -151 (n=258, d=20) · FRESH_HIGH -186 (n=44, d=15) · DEEP_DIP -243 (n=29, d=17)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +753 (n=36, d=18) · BOLL_SNAP +355 (n=247, d=28) · DOUBLE_DIP +234 (n=287, d=31) · STORM_DIP +219 (n=439, d=32) · PANIC_BOUNCE +190 (n=255, d=30) · PANIC_LITE +127 (n=567, d=35) · FRESH_HIGH -163 (n=40, d=21)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **71** entry days — **test LIVE (>=15)**
- PANIC_LITE: **69** entry days — **test LIVE (>=15)**
- PULLBACK_50: **64** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **63** entry days — **test LIVE (>=15)**
- REVERSAL_3: **63** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **61** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **60** entry days — **test LIVE (>=15)**
- TREND_RIDER: **48** entry days — **test LIVE (>=15)**
- DEEP_DIP: **42** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **36** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **2** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -281 bps over 42 entry days (row mean +107, n=79) · win rate per entry day 33% (row hit 48%)
- PANIC_BOUNCE: per-entry-day mean -32 bps over 63 entry days (row mean -62, n=550) · win rate per entry day 48% (row hit 46%)
- PANIC_LITE: per-entry-day mean -90 bps over 69 entry days (row mean -98, n=975) · win rate per entry day 39% (row hit 42%)
- DOUBLE_DIP: per-entry-day mean -91 bps over 60 entry days (row mean -64, n=441) · win rate per entry day 38% (row hit 42%)
- STORM_DIP: per-entry-day mean +386 bps over 2 entry days (row mean +386, n=80) · win rate per entry day 50% (row hit 54%)
- FRESH_HIGH: per-entry-day mean -163 bps over 36 entry days (row mean -135, n=79) · win rate per entry day 39% (row hit 42%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -150 bps over 48 entry days (row mean -186, n=127) · win rate per entry day 46% (row hit 46%)
- RSI2_DIP: per-entry-day mean -68 bps over 71 entry days (row mean -80, n=732) · win rate per entry day 37% (row hit 42%)
- REVERSAL_3: per-entry-day mean -57 bps over 63 entry days (row mean -58, n=429) · win rate per entry day 36% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -52 bps over 61 entry days (row mean +40, n=333) · win rate per entry day 44% (row hit 48%)
- PULLBACK_50: per-entry-day mean -69 bps over 64 entry days (row mean -60, n=282) · win rate per entry day 50% (row hit 48%)
- Exits on copied/zero-volume bars: **0** of 3743 forward exits tested; 398 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+753 bps, n=36); keep me on a short leash in calm-down (-243). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+190 bps, n=255); keep me on a short leash in calm-down (-151). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+162 bps, n=98); keep me on a short leash in calm-down (-118). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+234 bps, n=287); keep me on a short leash in calm-up (-87). Status: DEAD — loses to costs/SPY.
- STORM_DIP to the desk: my weather is storm-down (+219 bps, n=439); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+814 bps, n=18); keep me on a short leash in calm-down (-186). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is calm-up (+9 bps, n=173); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (-274 bps, n=18); keep me on a short leash in calm-up (-342). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (-68 bps, n=109); keep me on a short leash in storm-down (-296). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (-28 bps, n=56); keep me on a short leash in storm-down (-200). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+355 bps, n=247); keep me on a short leash in calm-up (-88). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (-94 bps, n=38); keep me on a short leash in calm-up (-194). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
