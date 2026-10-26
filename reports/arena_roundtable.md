# Arena Roundtable — 2026-10-25

Tape: **calm-down** · session 2026-10-23 · 12 agents · opened 50, closed 30 this session · 206 open · 3587 forward closes all-time

> **This lab is 70% of the desk's scored record (3587 of 5146 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 206 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 30 closed this session, 3587 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+247), BOLL_SNAP (+173), DOUBLE_DIP (+70); cold hands: PANIC_LITE (-6), FRESH_HIGH (-168). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +2 bps over 1802 trades (t=0.13) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +156 (n=413, d=108) · SHORT_EXT +34 (n=176, d=67) · PANIC_LITE -33 (n=2032, d=142) · PANIC_BOUNCE -49 (n=972, d=123) · BOLL_SNAP -82 (n=463, d=120) · DOUBLE_DIP -90 (n=832, d=125) · REVERSAL_3 -120 (n=229, d=38) · RSI2_DIP -133 (n=445, d=43) · PULLBACK_50 -152 (n=194, d=39) · TREND_RIDER -202 (n=97, d=35) · DEEP_DIP -237 (n=123, d=72)
- **calm-down**: DEEP_DIP +247 (n=23, d=14) · BOLL_SNAP +173 (n=98, d=16) · DOUBLE_DIP +70 (n=139, d=18) · REVERSAL_3 +56 (n=38, d=5) · PULLBACK_50 +24 (n=28, d=7) · PANIC_BOUNCE +16 (n=179, d=16) · RSI2_DIP +14 (n=76, d=7) · PANIC_LITE -6 (n=309, d=18) · FRESH_HIGH -168 (n=35, d=13)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +728 (n=29, d=17) · DOUBLE_DIP +386 (n=265, d=30) · BOLL_SNAP +376 (n=257, d=27) · STORM_DIP +341 (n=429, d=31) · PANIC_BOUNCE +189 (n=268, d=29) · PANIC_LITE +134 (n=590, d=34) · FRESH_HIGH -157 (n=36, d=20)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **62** entry days — **test LIVE (>=15)**
- PANIC_LITE: **60** entry days — **test LIVE (>=15)**
- PULLBACK_50: **58** entry days — **test LIVE (>=15)**
- REVERSAL_3: **55** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **54** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **53** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **53** entry days — **test LIVE (>=15)**
- TREND_RIDER: **41** entry days — **test LIVE (>=15)**
- DEEP_DIP: **34** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **31** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -170 bps over 34 entry days (row mean +308, n=64) · win rate per entry day 38% (row hit 56%)
- PANIC_BOUNCE: per-entry-day mean -8 bps over 54 entry days (row mean -49, n=455) · win rate per entry day 48% (row hit 46%)
- PANIC_LITE: per-entry-day mean -59 bps over 60 entry days (row mean -79, n=850) · win rate per entry day 40% (row hit 42%)
- DOUBLE_DIP: per-entry-day mean -90 bps over 53 entry days (row mean -80, n=366) · win rate per entry day 40% (row hit 41%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -225 bps over 31 entry days (row mean -177, n=69) · win rate per entry day 36% (row hit 36%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -106 bps over 41 entry days (row mean -106, n=108) · win rate per entry day 46% (row hit 47%)
- RSI2_DIP: per-entry-day mean -37 bps over 62 entry days (row mean -57, n=658) · win rate per entry day 40% (row hit 43%)
- REVERSAL_3: per-entry-day mean -40 bps over 55 entry days (row mean -51, n=391) · win rate per entry day 38% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -40 bps over 53 entry days (row mean +60, n=286) · win rate per entry day 47% (row hit 49%)
- PULLBACK_50: per-entry-day mean -53 bps over 58 entry days (row mean -39, n=266) · win rate per entry day 52% (row hit 47%)
- Exits on copied/zero-volume bars: **0** of 3186 forward exits tested; 401 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+728 bps, n=29); keep me on a short leash in calm-up (-237). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=268); keep me on a short leash in calm-up (-49). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-up (+162 bps, n=98); keep me on a short leash in calm-up (-33). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+386 bps, n=265); keep me on a short leash in calm-up (-90). Status: WATCH — positive but not significant.
- STORM_DIP to the desk: my weather is storm-down (+341 bps, n=429); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+702 bps, n=11); keep me on a short leash in calm-down (-168). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+497 bps, n=11); keep me on a short leash in calm-down (-233). Status: WATCH — positive but not significant.
- TREND_RIDER to the desk: my weather is calm-up (-202 bps, n=97); keep me on a short leash in calm-up (-202). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (+14 bps, n=76); keep me on a short leash in calm-up (-133). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+56 bps, n=38); keep me on a short leash in calm-up (-120). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+376 bps, n=257); keep me on a short leash in calm-up (-82). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+24 bps, n=28); keep me on a short leash in calm-up (-152). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
