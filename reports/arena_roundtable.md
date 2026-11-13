# Arena Roundtable — 2026-11-13

Tape: **calm-down** · session 2026-11-13 · 12 agents · opened 68, closed 27 this session · 198 open · 4518 forward closes all-time

> **This lab is 71% of the desk's scored record (4491 of 6283 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 198 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 27 closed this session, 4518 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-DOWN. Our pooled record in this weather — hot hands: BOLL_SNAP (+253), DOUBLE_DIP (+27), REVERSAL_3 (-5); cold hands: FRESH_HIGH (-144), DEEP_DIP (-202). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -5 bps over 1840 trades (t=-0.39) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +104 (n=354, d=97) · SHORT_EXT +18 (n=171, d=63) · PANIC_LITE -45 (n=1917, d=131) · PANIC_BOUNCE -62 (n=916, d=113) · BOLL_SNAP -84 (n=416, d=109) · DOUBLE_DIP -98 (n=762, d=115) · REVERSAL_3 -176 (n=135, d=27) · RSI2_DIP -186 (n=277, d=31) · PULLBACK_50 -224 (n=124, d=28) · DEEP_DIP -240 (n=119, d=65) · TREND_RIDER -249 (n=83, d=27)
- **calm-down**: BOLL_SNAP +253 (n=124, d=22) · DOUBLE_DIP +27 (n=215, d=25) · REVERSAL_3 -5 (n=63, d=12) · TREND_RIDER -14 (n=25, d=11) · RSI2_DIP -36 (n=124, d=14) · PULLBACK_50 -54 (n=41, d=12) · PANIC_LITE -70 (n=487, d=26) · PANIC_BOUNCE -114 (n=280, d=23) · FRESH_HIGH -144 (n=46, d=16) · DEEP_DIP -202 (n=36, d=20)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +114 (n=53, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +868 (n=43, d=19) · BOLL_SNAP +477 (n=306, d=30) · DOUBLE_DIP +342 (n=346, d=33) · PANIC_BOUNCE +327 (n=309, d=31) · STORM_DIP +277 (n=498, d=34) · PANIC_LITE +178 (n=630, d=37) · RSI2_DIP +10 (n=41, d=4) · FRESH_HIGH -62 (n=42, d=22)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **77** entry days — **test LIVE (>=15)**
- PANIC_LITE: **75** entry days — **test LIVE (>=15)**
- PULLBACK_50: **70** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **69** entry days — **test LIVE (>=15)**
- REVERSAL_3: **68** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **67** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **66** entry days — **test LIVE (>=15)**
- TREND_RIDER: **52** entry days — **test LIVE (>=15)**
- DEEP_DIP: **46** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **39** entry days — **test LIVE (>=15)**
- SHORT_EXT: **20** entry days — **test LIVE (>=15)**
- STORM_DIP: **3** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -262 bps over 46 entry days (row mean +30, n=88) · win rate per entry day 33% (row hit 44%)
- PANIC_BOUNCE: per-entry-day mean -29 bps over 69 entry days (row mean -94, n=606) · win rate per entry day 48% (row hit 44%)
- PANIC_LITE: per-entry-day mean -96 bps over 75 entry days (row mean -117, n=1058) · win rate per entry day 40% (row hit 41%)
- DOUBLE_DIP: per-entry-day mean -90 bps over 66 entry days (row mean +4, n=487) · win rate per entry day 39% (row hit 45%)
- STORM_DIP: per-entry-day mean +525 bps over 3 entry days (row mean +525, n=120) · win rate per entry day 67% (row hit 65%)
- FRESH_HIGH: per-entry-day mean -183 bps over 39 entry days (row mean -144, n=84) · win rate per entry day 38% (row hit 43%)
- SHORT_EXT: per-entry-day mean +161 bps over 20 entry days (row mean +169, n=36) · win rate per entry day 55% (row hit 53%)
- TREND_RIDER: per-entry-day mean -196 bps over 52 entry days (row mean -218, n=133) · win rate per entry day 44% (row hit 44%)
- RSI2_DIP: per-entry-day mean -53 bps over 77 entry days (row mean -65, n=780) · win rate per entry day 39% (row hit 44%)
- REVERSAL_3: per-entry-day mean -36 bps over 68 entry days (row mean -52, n=441) · win rate per entry day 40% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -18 bps over 67 entry days (row mean +123, n=382) · win rate per entry day 46% (row hit 53%)
- PULLBACK_50: per-entry-day mean -56 bps over 70 entry days (row mean -52, n=303) · win rate per entry day 53% (row hit 48%)
- Exits on copied/zero-volume bars: **0** of 4171 forward exits tested; 347 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+868 bps, n=43); keep me on a short leash in calm-up (-240). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+327 bps, n=309); keep me on a short leash in calm-down (-114). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-down (+178 bps, n=630); keep me on a short leash in calm-down (-70). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+342 bps, n=346); keep me on a short leash in calm-up (-98). Status: DEAD — loses to costs/SPY.
- STORM_DIP to the desk: my weather is storm-down (+277 bps, n=498); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+962 bps, n=16); keep me on a short leash in calm-down (-144). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+231 bps, n=9); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (-14 bps, n=25); keep me on a short leash in calm-up (-249). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+10 bps, n=41); keep me on a short leash in calm-up (-186). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (-5 bps, n=63); keep me on a short leash in calm-up (-176). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+477 bps, n=306); keep me on a short leash in calm-up (-84). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (+385 bps, n=12); keep me on a short leash in calm-up (-224). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
