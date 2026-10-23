# Arena Roundtable — 2026-10-22

Tape: **calm-down** · session 2026-10-22 · 12 agents · opened 98, closed 53 this session · 186 open · 3557 forward closes all-time

> **This lab is 70% of the desk's scored record (3504 of 5039 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 186 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 53 closed this session, 3557 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+322), BOLL_SNAP (+192), DOUBLE_DIP (+79); cold hands: PANIC_LITE (-3), FRESH_HIGH (-158). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +5 bps over 1795 trades (t=0.39) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +167 (n=414, d=110) · SHORT_EXT +25 (n=177, d=68) · PANIC_LITE -29 (n=2051, d=143) · PANIC_BOUNCE -48 (n=976, d=124) · BOLL_SNAP -77 (n=467, d=121) · DOUBLE_DIP -86 (n=835, d=126) · REVERSAL_3 -117 (n=233, d=39) · RSI2_DIP -135 (n=456, d=45) · PULLBACK_50 -155 (n=194, d=40) · DEEP_DIP -214 (n=125, d=73) · TREND_RIDER -282 (n=104, d=35)
- **calm-down**: DEEP_DIP +322 (n=20, d=13) · BOLL_SNAP +192 (n=87, d=15) · DOUBLE_DIP +79 (n=135, d=17) · REVERSAL_3 +56 (n=38, d=5) · PANIC_BOUNCE +33 (n=141, d=15) · PULLBACK_50 +25 (n=26, d=6) · RSI2_DIP +22 (n=67, d=5) · PANIC_LITE -3 (n=253, d=17) · FRESH_HIGH -158 (n=35, d=13)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +729 (n=30, d=17) · DOUBLE_DIP +386 (n=265, d=30) · BOLL_SNAP +376 (n=257, d=27) · STORM_DIP +341 (n=429, d=31) · PANIC_BOUNCE +189 (n=268, d=29) · PANIC_LITE +134 (n=590, d=34) · FRESH_HIGH -157 (n=36, d=20)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **61** entry days — **test LIVE (>=15)**
- PANIC_LITE: **59** entry days — **test LIVE (>=15)**
- PULLBACK_50: **57** entry days — **test LIVE (>=15)**
- REVERSAL_3: **55** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **53** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **52** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **52** entry days — **test LIVE (>=15)**
- TREND_RIDER: **40** entry days — **test LIVE (>=15)**
- DEEP_DIP: **33** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **30** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -79 bps over 33 entry days (row mean +363, n=63) · win rate per entry day 39% (row hit 57%)
- PANIC_BOUNCE: per-entry-day mean -6 bps over 53 entry days (row mean -48, n=452) · win rate per entry day 49% (row hit 46%)
- PANIC_LITE: per-entry-day mean -54 bps over 59 entry days (row mean -77, n=843) · win rate per entry day 41% (row hit 42%)
- DOUBLE_DIP: per-entry-day mean -89 bps over 52 entry days (row mean -80, n=365) · win rate per entry day 40% (row hit 41%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -229 bps over 30 entry days (row mean -181, n=66) · win rate per entry day 37% (row hit 36%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -86 bps over 40 entry days (row mean -91, n=106) · win rate per entry day 48% (row hit 48%)
- RSI2_DIP: per-entry-day mean -36 bps over 61 entry days (row mean -57, n=655) · win rate per entry day 41% (row hit 43%)
- REVERSAL_3: per-entry-day mean -40 bps over 55 entry days (row mean -51, n=391) · win rate per entry day 38% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -26 bps over 52 entry days (row mean +69, n=283) · win rate per entry day 48% (row hit 49%)
- PULLBACK_50: per-entry-day mean -53 bps over 57 entry days (row mean -39, n=259) · win rate per entry day 53% (row hit 48%)
- Exits on copied/zero-volume bars: **0** of 3186 forward exits tested; 371 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+729 bps, n=30); keep me on a short leash in calm-up (-214). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=268); keep me on a short leash in calm-up (-48). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-up (+162 bps, n=98); keep me on a short leash in calm-up (-29). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+386 bps, n=265); keep me on a short leash in calm-up (-86). Status: WATCH — positive but not significant.
- STORM_DIP to the desk: my weather is storm-down (+341 bps, n=429); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+702 bps, n=11); keep me on a short leash in calm-down (-158). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+611 bps, n=10); keep me on a short leash in calm-down (-233). Status: WATCH — positive but not significant.
- TREND_RIDER to the desk: my weather is calm-up (-282 bps, n=104); keep me on a short leash in calm-up (-282). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (+22 bps, n=67); keep me on a short leash in calm-up (-135). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+56 bps, n=38); keep me on a short leash in calm-up (-117). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+376 bps, n=257); keep me on a short leash in calm-up (-77). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+25 bps, n=26); keep me on a short leash in calm-up (-155). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
