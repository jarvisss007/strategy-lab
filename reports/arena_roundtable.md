# Arena Roundtable — 2026-10-13

Tape: **calm-up** · session 2026-10-13 · 12 agents · opened 59, closed 75 this session · 231 open · 2995 forward closes all-time

> **This lab is 68% of the desk's scored record (2922 of 4304 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 231 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 75 closed this session, 2995 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+228), PULLBACK_50 (+5), PANIC_LITE (-2); cold hands: DEEP_DIP (-143), TREND_RIDER (-265). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 43% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 83% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +24 bps over 1667 trades (t=1.75) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +228 (n=418, d=110) · PULLBACK_50 +5 (n=201, d=43) · PANIC_LITE -2 (n=1942, d=145) · PANIC_BOUNCE -12 (n=929, d=123) · SHORT_EXT -15 (n=184, d=73) · BOLL_SNAP -24 (n=398, d=119) · REVERSAL_3 -26 (n=235, d=43) · DOUBLE_DIP -44 (n=775, d=125) · RSI2_DIP -48 (n=475, d=46) · DEEP_DIP -143 (n=113, d=65) · TREND_RIDER -265 (n=109, d=37)
- **calm-down**: BOLL_SNAP +179 (n=65, d=13) · DOUBLE_DIP +93 (n=122, d=15) · REVERSAL_3 +49 (n=26, d=3) · RSI2_DIP +47 (n=59, d=4) · PANIC_BOUNCE +11 (n=119, d=14) · PANIC_LITE -12 (n=208, d=15) · FRESH_HIGH -187 (n=36, d=12)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +1084 (n=24, d=13) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -194 (n=34, d=20)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **54** entry days — **test LIVE (>=15)**
- PANIC_LITE: **52** entry days — **test LIVE (>=15)**
- REVERSAL_3: **50** entry days — **test LIVE (>=15)**
- PULLBACK_50: **50** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **47** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **45** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **45** entry days — **test LIVE (>=15)**
- TREND_RIDER: **33** entry days — **test LIVE (>=15)**
- DEEP_DIP: **28** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **26** entry days — **test LIVE (>=15)**
- SHORT_EXT: **15** entry days — **test LIVE (>=15)**
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean +232 bps over 28 entry days (row mean +582, n=57) · win rate per entry day 46% (row hit 63%)
- PANIC_BOUNCE: per-entry-day mean +41 bps over 47 entry days (row mean +29, n=353) · win rate per entry day 53% (row hit 51%)
- PANIC_LITE: per-entry-day mean -9 bps over 52 entry days (row mean -21, n=715) · win rate per entry day 44% (row hit 45%)
- DOUBLE_DIP: per-entry-day mean -16 bps over 45 entry days (row mean +18, n=298) · win rate per entry day 44% (row hit 47%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -155 bps over 26 entry days (row mean -91, n=57) · win rate per entry day 42% (row hit 40%)
- SHORT_EXT: per-entry-day mean +36 bps over 15 entry days (row mean +125, n=30) · win rate per entry day 47% (row hit 50%)
- TREND_RIDER: per-entry-day mean -16 bps over 33 entry days (row mean -46, n=93) · win rate per entry day 48% (row hit 47%)
- RSI2_DIP: per-entry-day mean +9 bps over 54 entry days (row mean -10, n=586) · win rate per entry day 44% (row hit 45%)
- REVERSAL_3: per-entry-day mean +1 bps over 50 entry days (row mean +1, n=336) · win rate per entry day 40% (row hit 47%)
- BOLL_SNAP: per-entry-day mean +22 bps over 45 entry days (row mean +200, n=210) · win rate per entry day 53% (row hit 56%)
- PULLBACK_50: per-entry-day mean +22 bps over 50 entry days (row mean +56, n=220) · win rate per entry day 60% (row hit 54%)
- Exits on copied/zero-volume bars: **0** of 2805 forward exits tested; 190 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+1084 bps, n=24); keep me on a short leash in calm-up (-143). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-12). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-down (-12). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-44). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+677 bps, n=14); keep me on a short leash in storm-down (-194). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+611 bps, n=10); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-up (-265 bps, n=109); keep me on a short leash in calm-up (-265). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (+47 bps, n=59); keep me on a short leash in calm-up (-48). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+49 bps, n=26); keep me on a short leash in calm-up (-26). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-up (+5 bps, n=201); keep me on a short leash in calm-down (-14). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
