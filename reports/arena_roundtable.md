# Arena Roundtable — 2026-09-29

Tape: **calm-up** · session 2026-09-28 · 12 agents · opened 76, closed 49 this session · 190 open · 2492 forward closes all-time

> **This lab is 69% of the desk's scored record (2492 of 3602 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 190 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 49 closed this session, 2492 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+205), DEEP_DIP (+45), PULLBACK_50 (+9); cold hands: RSI2_DIP (-49), TREND_RIDER (-254). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +36 bps over 1631 trades (t=2.53) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +205 (n=435, d=110) · DEEP_DIP +45 (n=115, d=72) · PULLBACK_50 +9 (n=170, d=36) · PANIC_LITE -7 (n=1899, d=144) · REVERSAL_3 -12 (n=204, d=37) · PANIC_BOUNCE -23 (n=933, d=125) · BOLL_SNAP -26 (n=375, d=117) · SHORT_EXT -36 (n=186, d=72) · DOUBLE_DIP -39 (n=779, d=126) · RSI2_DIP -49 (n=395, d=39) · TREND_RIDER -254 (n=91, d=30)
- **calm-down**: TREND_RIDER +338 (n=25, d=10) · BOLL_SNAP +310 (n=69, d=13) · PULLBACK_50 +138 (n=47, d=10) · PANIC_BOUNCE +126 (n=134, d=14) · DOUBLE_DIP +108 (n=123, d=15) · REVERSAL_3 +101 (n=87, d=8) · PANIC_LITE +95 (n=240, d=15) · RSI2_DIP -118 (n=174, d=10) · FRESH_HIGH -246 (n=32, d=11)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +753 (n=28, d=15) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -148 (n=36, d=19)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **44** entry days — **test LIVE (>=15)**
- PANIC_LITE: **41** entry days — **test LIVE (>=15)**
- REVERSAL_3: **40** entry days — **test LIVE (>=15)**
- PULLBACK_50: **40** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **38** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **36** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **35** entry days — **test LIVE (>=15)**
- TREND_RIDER: **24** entry days — **test LIVE (>=15)**
- DEEP_DIP: **22** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **19** entry days — **test LIVE (>=15)**
- SHORT_EXT: **10** entry days
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean +484 bps over 22 entry days (row mean +774, n=49) · win rate per entry day 59% (row hit 71%)
- PANIC_BOUNCE: per-entry-day mean +106 bps over 38 entry days (row mean +56, n=315) · win rate per entry day 58% (row hit 52%)
- PANIC_LITE: per-entry-day mean +30 bps over 41 entry days (row mean +10, n=597) · win rate per entry day 49% (row hit 47%)
- DOUBLE_DIP: per-entry-day mean +58 bps over 36 entry days (row mean +87, n=246) · win rate per entry day 47% (row hit 52%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -123 bps over 19 entry days (row mean -76, n=48) · win rate per entry day 47% (row hit 42%)
- SHORT_EXT: per-entry-day mean +110 bps over 10 entry days (row mean +244, n=23) · win rate per entry day 50% (row hit 56%)
- TREND_RIDER: per-entry-day mean -105 bps over 24 entry days (row mean -152, n=63) · win rate per entry day 42% (row hit 44%)
- RSI2_DIP: per-entry-day mean +19 bps over 44 entry days (row mean -7, n=464) · win rate per entry day 41% (row hit 43%)
- REVERSAL_3: per-entry-day mean +33 bps over 40 entry days (row mean +16, n=287) · win rate per entry day 42% (row hit 47%)
- BOLL_SNAP: per-entry-day mean +41 bps over 35 entry days (row mean +265, n=170) · win rate per entry day 54% (row hit 59%)
- PULLBACK_50: per-entry-day mean +52 bps over 40 entry days (row mean +66, n=190) · win rate per entry day 60% (row hit 53%)
- Exits on copied/zero-volume bars: **0** of 2394 forward exits tested; 98 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is calm-down (+891 bps, n=12); keep me on a short leash in calm-up (+45). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-23). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (-7). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-39). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-246). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+611 bps, n=10); keep me on a short leash in calm-up (-36). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+338 bps, n=25); keep me on a short leash in calm-up (-254). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-118). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+101 bps, n=87); keep me on a short leash in calm-up (-12). Status: WATCH — positive but not significant.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+138 bps, n=47); keep me on a short leash in calm-up (+9). Status: WATCH — positive but not significant.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
