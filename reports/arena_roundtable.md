# Arena Roundtable — 2026-10-01

Tape: **calm-up** · session 2026-10-01 · 12 agents · opened 23, closed 41 this session · 139 open · 2649 forward closes all-time

> **This lab is 69% of the desk's scored record (2608 of 3772 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 139 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 41 closed this session, 2649 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+214), PULLBACK_50 (+24), DEEP_DIP (+20); cold hands: RSI2_DIP (-39), TREND_RIDER (-218). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 42% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +38 bps over 1626 trades (t=2.73) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +214 (n=423, d=108) · PULLBACK_50 +24 (n=177, d=37) · DEEP_DIP +20 (n=110, d=70) · SHORT_EXT +3 (n=182, d=68) · PANIC_LITE -1 (n=1882, d=143) · REVERSAL_3 -10 (n=211, d=38) · PANIC_BOUNCE -16 (n=918, d=123) · BOLL_SNAP -18 (n=382, d=117) · DOUBLE_DIP -28 (n=779, d=124) · RSI2_DIP -39 (n=420, d=40) · TREND_RIDER -218 (n=88, d=32)
- **calm-down**: TREND_RIDER +360 (n=24, d=9) · BOLL_SNAP +295 (n=73, d=14) · DOUBLE_DIP +111 (n=125, d=16) · PULLBACK_50 +83 (n=43, d=9) · PANIC_BOUNCE +56 (n=129, d=15) · PANIC_LITE +48 (n=236, d=16) · REVERSAL_3 -31 (n=65, d=7) · FRESH_HIGH -191 (n=33, d=12) · RSI2_DIP -257 (n=131, d=9)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +845 (n=27, d=15) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -190 (n=34, d=19)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **46** entry days — **test LIVE (>=15)**
- PANIC_LITE: **44** entry days — **test LIVE (>=15)**
- REVERSAL_3: **43** entry days — **test LIVE (>=15)**
- PULLBACK_50: **43** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **40** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **39** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **37** entry days — **test LIVE (>=15)**
- TREND_RIDER: **26** entry days — **test LIVE (>=15)**
- DEEP_DIP: **23** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **21** entry days — **test LIVE (>=15)**
- SHORT_EXT: **11** entry days
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean +440 bps over 23 entry days (row mean +748, n=50) · win rate per entry day 56% (row hit 70%)
- PANIC_BOUNCE: per-entry-day mean +114 bps over 40 entry days (row mean +59, n=328) · win rate per entry day 60% (row hit 53%)
- PANIC_LITE: per-entry-day mean +19 bps over 44 entry days (row mean +5, n=639) · win rate per entry day 48% (row hit 47%)
- DOUBLE_DIP: per-entry-day mean +39 bps over 39 entry days (row mean +84, n=263) · win rate per entry day 49% (row hit 52%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -174 bps over 21 entry days (row mean -100, n=50) · win rate per entry day 43% (row hit 40%)
- SHORT_EXT: per-entry-day mean +76 bps over 11 entry days (row mean +223, n=24) · win rate per entry day 46% (row hit 54%)
- TREND_RIDER: per-entry-day mean -76 bps over 26 entry days (row mean -90, n=72) · win rate per entry day 46% (row hit 49%)
- RSI2_DIP: per-entry-day mean +25 bps over 46 entry days (row mean +1, n=504) · win rate per entry day 46% (row hit 45%)
- REVERSAL_3: per-entry-day mean +20 bps over 43 entry days (row mean +15, n=298) · win rate per entry day 42% (row hit 47%)
- BOLL_SNAP: per-entry-day mean +43 bps over 37 entry days (row mean +254, n=182) · win rate per entry day 57% (row hit 58%)
- PULLBACK_50: per-entry-day mean +58 bps over 43 entry days (row mean +69, n=199) · win rate per entry day 60% (row hit 54%)
- Exits on copied/zero-volume bars: **0** of 2394 forward exits tested; 255 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+845 bps, n=27); keep me on a short leash in calm-up (+20). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-16). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (-1). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-28). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-191). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+441 bps, n=11); keep me on a short leash in calm-down (-265). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+360 bps, n=24); keep me on a short leash in calm-up (-218). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-257). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-up (-10 bps, n=211); keep me on a short leash in calm-down (-31). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+83 bps, n=43); keep me on a short leash in calm-up (+24). Status: WATCH — positive but not significant.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
