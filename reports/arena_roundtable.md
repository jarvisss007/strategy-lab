# Arena Roundtable — 2026-10-19

Tape: **calm-down** · session 2026-10-19 · 12 agents · opened 37, closed 71 this session · 267 open · 3333 forward closes all-time

> **This lab is 69% of the desk's scored record (3262 of 4724 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 267 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 71 closed this session, 3333 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-DOWN. Our pooled record in this weather — hot hands: BOLL_SNAP (+168), DOUBLE_DIP (+99), REVERSAL_3 (+66); cold hands: PANIC_LITE (-6), FRESH_HIGH (-277). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 43% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +8 bps over 1796 trades (t=0.63) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +194 (n=425, d=109) · SHORT_EXT +2 (n=184, d=74) · PANIC_LITE -26 (n=2056, d=144) · PANIC_BOUNCE -46 (n=975, d=124) · BOLL_SNAP -68 (n=468, d=122) · DOUBLE_DIP -84 (n=836, d=125) · REVERSAL_3 -104 (n=250, d=41) · RSI2_DIP -107 (n=488, d=45) · PULLBACK_50 -132 (n=208, d=43) · DEEP_DIP -214 (n=132, d=78) · TREND_RIDER -302 (n=105, d=37)
- **calm-down**: BOLL_SNAP +168 (n=85, d=14) · DOUBLE_DIP +99 (n=128, d=16) · REVERSAL_3 +66 (n=36, d=4) · PULLBACK_50 +55 (n=25, d=5) · RSI2_DIP +45 (n=60, d=4) · PANIC_BOUNCE +23 (n=141, d=15) · PANIC_LITE -6 (n=249, d=16) · FRESH_HIGH -277 (n=36, d=13)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +1022 (n=25, d=15) · DOUBLE_DIP +386 (n=265, d=30) · BOLL_SNAP +376 (n=257, d=27) · STORM_DIP +341 (n=429, d=31) · PANIC_BOUNCE +189 (n=268, d=29) · PANIC_LITE +134 (n=590, d=34) · FRESH_HIGH -98 (n=44, d=21)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **58** entry days — **test LIVE (>=15)**
- PANIC_LITE: **56** entry days — **test LIVE (>=15)**
- PULLBACK_50: **54** entry days — **test LIVE (>=15)**
- REVERSAL_3: **53** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **51** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **49** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **49** entry days — **test LIVE (>=15)**
- TREND_RIDER: **37** entry days — **test LIVE (>=15)**
- DEEP_DIP: **31** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **29** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -21 bps over 31 entry days (row mean +433, n=60) · win rate per entry day 42% (row hit 60%)
- PANIC_BOUNCE: per-entry-day mean +0 bps over 51 entry days (row mean -62, n=412) · win rate per entry day 49% (row hit 45%)
- PANIC_LITE: per-entry-day mean -48 bps over 56 entry days (row mean -83, n=795) · win rate per entry day 41% (row hit 42%)
- DOUBLE_DIP: per-entry-day mean -89 bps over 49 entry days (row mean -74, n=336) · win rate per entry day 41% (row hit 42%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -197 bps over 29 entry days (row mean -134, n=63) · win rate per entry day 38% (row hit 38%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -23 bps over 37 entry days (row mean -37, n=100) · win rate per entry day 49% (row hit 49%)
- RSI2_DIP: per-entry-day mean -41 bps over 58 entry days (row mean -64, n=628) · win rate per entry day 41% (row hit 42%)
- REVERSAL_3: per-entry-day mean -37 bps over 53 entry days (row mean -57, n=368) · win rate per entry day 38% (row hit 43%)
- BOLL_SNAP: per-entry-day mean -24 bps over 49 entry days (row mean +84, n=255) · win rate per entry day 49% (row hit 49%)
- PULLBACK_50: per-entry-day mean -29 bps over 54 entry days (row mean -12, n=242) · win rate per entry day 56% (row hit 50%)
- Exits on copied/zero-volume bars: **0** of 3186 forward exits tested; 147 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+1022 bps, n=25); keep me on a short leash in calm-up (-214). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=268); keep me on a short leash in calm-up (-46). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-up (+162 bps, n=98); keep me on a short leash in calm-up (-26). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+386 bps, n=265); keep me on a short leash in calm-up (-84). Status: WATCH — positive but not significant.
- STORM_DIP to the desk: my weather is storm-down (+341 bps, n=429); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+654 bps, n=14); keep me on a short leash in calm-down (-277). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+611 bps, n=10); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-up (-302 bps, n=105); keep me on a short leash in calm-up (-302). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (+45 bps, n=60); keep me on a short leash in calm-up (-107). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+66 bps, n=36); keep me on a short leash in calm-up (-104). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+376 bps, n=257); keep me on a short leash in storm-up (-72). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+55 bps, n=25); keep me on a short leash in calm-up (-132). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
