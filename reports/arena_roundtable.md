# Arena Roundtable — 2026-11-16

Tape: **storm-down** · session 2026-11-16 · 12 agents · opened 144, closed 75 this session · 268 open · 4593 forward closes all-time

> **This lab is 71% of the desk's scored record (4518 of 6329 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 268 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 75 closed this session, 4593 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+778), BOLL_SNAP (+440), PANIC_BOUNCE (+338); cold hands: RSI2_DIP (+10), FRESH_HIGH (-78). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -18 bps over 1840 trades (t=-1.32) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +96 (n=355, d=96) · SHORT_EXT +27 (n=171, d=62) · PANIC_LITE -56 (n=1866, d=130) · PANIC_BOUNCE -69 (n=886, d=112) · BOLL_SNAP -89 (n=413, d=108) · DOUBLE_DIP -103 (n=751, d=114) · DEEP_DIP -183 (n=120, d=65) · RSI2_DIP -206 (n=272, d=30) · PULLBACK_50 -217 (n=122, d=27) · REVERSAL_3 -221 (n=128, d=26) · TREND_RIDER -308 (n=80, d=26)
- **calm-down**: BOLL_SNAP +238 (n=125, d=23) · REVERSAL_3 -7 (n=63, d=12) · DOUBLE_DIP -72 (n=246, d=26) · RSI2_DIP -72 (n=136, d=15) · PULLBACK_50 -92 (n=46, d=13) · PANIC_LITE -122 (n=512, d=27) · TREND_RIDER -128 (n=26, d=12) · FRESH_HIGH -136 (n=51, d=17) · PANIC_BOUNCE -156 (n=290, d=24) · DEEP_DIP -204 (n=34, d=20)
- **storm-up**: PANIC_LITE +167 (n=99, d=4) · PANIC_BOUNCE +132 (n=70, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +778 (n=44, d=19) · BOLL_SNAP +440 (n=292, d=30) · PANIC_BOUNCE +338 (n=312, d=31) · DOUBLE_DIP +294 (n=328, d=33) · STORM_DIP +277 (n=498, d=34) · PANIC_LITE +200 (n=640, d=37) · RSI2_DIP +10 (n=41, d=4) · FRESH_HIGH -78 (n=41, d=22)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **78** entry days — **test LIVE (>=15)**
- PANIC_LITE: **76** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **70** entry days — **test LIVE (>=15)**
- PULLBACK_50: **70** entry days — **test LIVE (>=15)**
- REVERSAL_3: **69** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **67** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **67** entry days — **test LIVE (>=15)**
- TREND_RIDER: **53** entry days — **test LIVE (>=15)**
- DEEP_DIP: **47** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **40** entry days — **test LIVE (>=15)**
- SHORT_EXT: **20** entry days — **test LIVE (>=15)**
- STORM_DIP: **3** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -292 bps over 47 entry days (row mean -26, n=91) · win rate per entry day 32% (row hit 43%)
- PANIC_BOUNCE: per-entry-day mean -43 bps over 70 entry days (row mean -120, n=624) · win rate per entry day 47% (row hit 43%)
- PANIC_LITE: per-entry-day mean -105 bps over 76 entry days (row mean -140, n=1095) · win rate per entry day 40% (row hit 40%)
- DOUBLE_DIP: per-entry-day mean -116 bps over 67 entry days (row mean -3, n=489) · win rate per entry day 39% (row hit 45%)
- STORM_DIP: per-entry-day mean +525 bps over 3 entry days (row mean +525, n=120) · win rate per entry day 67% (row hit 65%)
- FRESH_HIGH: per-entry-day mean -170 bps over 40 entry days (row mean -128, n=87) · win rate per entry day 40% (row hit 45%)
- SHORT_EXT: per-entry-day mean +161 bps over 20 entry days (row mean +169, n=36) · win rate per entry day 55% (row hit 53%)
- TREND_RIDER: per-entry-day mean -201 bps over 53 entry days (row mean -225, n=137) · win rate per entry day 43% (row hit 44%)
- RSI2_DIP: per-entry-day mean -55 bps over 78 entry days (row mean -66, n=786) · win rate per entry day 38% (row hit 44%)
- REVERSAL_3: per-entry-day mean -37 bps over 69 entry days (row mean -52, n=443) · win rate per entry day 39% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -18 bps over 67 entry days (row mean +123, n=382) · win rate per entry day 46% (row hit 53%)
- PULLBACK_50: per-entry-day mean -56 bps over 70 entry days (row mean -52, n=303) · win rate per entry day 53% (row hit 48%)
- Exits on copied/zero-volume bars: **0** of 4492 forward exits tested; 101 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+778 bps, n=44); keep me on a short leash in calm-down (-204). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+338 bps, n=312); keep me on a short leash in calm-down (-156). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-down (+200 bps, n=640); keep me on a short leash in calm-down (-122). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+294 bps, n=328); keep me on a short leash in calm-up (-103). Status: DEAD — loses to costs/SPY.
- STORM_DIP to the desk: my weather is storm-down (+277 bps, n=498); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+962 bps, n=16); keep me on a short leash in calm-down (-136). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+231 bps, n=9); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (-128 bps, n=26); keep me on a short leash in calm-up (-308). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+10 bps, n=41); keep me on a short leash in calm-up (-206). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (-7 bps, n=63); keep me on a short leash in calm-up (-221). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+440 bps, n=292); keep me on a short leash in calm-up (-89). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (+385 bps, n=12); keep me on a short leash in calm-up (-217). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
