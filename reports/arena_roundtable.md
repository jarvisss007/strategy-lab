# Arena Roundtable — 2026-10-10

Tape: **calm-up** · session 2026-10-09 · 12 agents · opened 42, closed 62 this session · 204 open · 2868 forward closes all-time

> **This lab is 69% of the desk's scored record (2868 of 4185 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 204 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 62 closed this session, 2868 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+235), PULLBACK_50 (+27), PANIC_LITE (-1); cold hands: RSI2_DIP (-35), TREND_RIDER (-218). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 43% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 83% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +27 bps over 1657 trades (t=1.98) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +235 (n=420, d=108) · PULLBACK_50 +27 (n=192, d=42) · PANIC_LITE -1 (n=1919, d=145) · BOLL_SNAP -9 (n=387, d=118) · PANIC_BOUNCE -10 (n=914, d=123) · DEEP_DIP -21 (n=110, d=66) · REVERSAL_3 -23 (n=225, d=42) · SHORT_EXT -24 (n=184, d=71) · DOUBLE_DIP -26 (n=769, d=124) · RSI2_DIP -35 (n=459, d=45) · TREND_RIDER -218 (n=103, d=35)
- **calm-down**: BOLL_SNAP +179 (n=65, d=13) · DOUBLE_DIP +93 (n=122, d=15) · REVERSAL_3 +49 (n=27, d=4) · PULLBACK_50 +23 (n=24, d=5) · RSI2_DIP +15 (n=81, d=5) · PANIC_BOUNCE +11 (n=119, d=14) · PANIC_LITE -12 (n=208, d=15) · FRESH_HIGH -106 (n=35, d=12)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +1084 (n=24, d=13) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -202 (n=34, d=20)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **52** entry days — **test LIVE (>=15)**
- PANIC_LITE: **50** entry days — **test LIVE (>=15)**
- REVERSAL_3: **48** entry days — **test LIVE (>=15)**
- PULLBACK_50: **48** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **45** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **43** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **43** entry days — **test LIVE (>=15)**
- TREND_RIDER: **31** entry days — **test LIVE (>=15)**
- DEEP_DIP: **27** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **24** entry days — **test LIVE (>=15)**
- SHORT_EXT: **14** entry days
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean +258 bps over 27 entry days (row mean +619, n=55) · win rate per entry day 48% (row hit 66%)
- PANIC_BOUNCE: per-entry-day mean +48 bps over 45 entry days (row mean +43, n=340) · win rate per entry day 53% (row hit 52%)
- PANIC_LITE: per-entry-day mean -2 bps over 50 entry days (row mean -17, n=703) · win rate per entry day 46% (row hit 45%)
- DOUBLE_DIP: per-entry-day mean +13 bps over 43 entry days (row mean +79, n=268) · win rate per entry day 46% (row hit 52%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -186 bps over 24 entry days (row mean -102, n=55) · win rate per entry day 42% (row hit 40%)
- SHORT_EXT: per-entry-day mean -5 bps over 14 entry days (row mean +108, n=29) · win rate per entry day 43% (row hit 48%)
- TREND_RIDER: per-entry-day mean -19 bps over 31 entry days (row mean -55, n=86) · win rate per entry day 48% (row hit 49%)
- RSI2_DIP: per-entry-day mean +15 bps over 52 entry days (row mean -3, n=555) · win rate per entry day 46% (row hit 45%)
- REVERSAL_3: per-entry-day mean +7 bps over 48 entry days (row mean +8, n=322) · win rate per entry day 42% (row hit 47%)
- BOLL_SNAP: per-entry-day mean +47 bps over 43 entry days (row mean +236, n=200) · win rate per entry day 56% (row hit 58%)
- PULLBACK_50: per-entry-day mean +54 bps over 48 entry days (row mean +68, n=215) · win rate per entry day 62% (row hit 54%)
- Exits on copied/zero-volume bars: **0** of 2640 forward exits tested; 228 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+1084 bps, n=24); keep me on a short leash in calm-up (-21). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-10). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-down (-12). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-26). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in storm-down (-202). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+441 bps, n=11); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+417 bps, n=13); keep me on a short leash in calm-up (-218). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (+15 bps, n=81); keep me on a short leash in calm-up (-35). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+49 bps, n=27); keep me on a short leash in calm-up (-23). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-up (+27 bps, n=192); keep me on a short leash in calm-down (+23). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
