# Arena Roundtable — 2026-10-07

Tape: **calm-up** · session 2026-10-06 · 12 agents · opened 34, closed 28 this session · 120 open · 2752 forward closes all-time

> **This lab is 68% of the desk's scored record (2752 of 4021 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 120 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 28 closed this session, 2752 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+234), DEEP_DIP (+40), PULLBACK_50 (+26); cold hands: RSI2_DIP (-36), TREND_RIDER (-174). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 42% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +36 bps over 1611 trades (t=2.59) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +234 (n=421, d=110) · DEEP_DIP +40 (n=108, d=69) · PULLBACK_50 +26 (n=176, d=39) · PANIC_LITE +6 (n=1870, d=145) · SHORT_EXT -2 (n=183, d=70) · BOLL_SNAP -6 (n=381, d=118) · PANIC_BOUNCE -6 (n=901, d=123) · REVERSAL_3 -12 (n=209, d=39) · DOUBLE_DIP -21 (n=745, d=124) · RSI2_DIP -36 (n=416, d=42) · TREND_RIDER -174 (n=96, d=34)
- **calm-down**: PULLBACK_50 +215 (n=33, d=7) · BOLL_SNAP +179 (n=65, d=13) · DOUBLE_DIP +93 (n=122, d=15) · PANIC_BOUNCE +11 (n=119, d=14) · PANIC_LITE -12 (n=208, d=15) · RSI2_DIP -41 (n=120, d=7) · REVERSAL_3 -47 (n=58, d=5) · FRESH_HIGH -145 (n=33, d=12)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +869 (n=26, d=14) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -190 (n=34, d=19)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **49** entry days — **test LIVE (>=15)**
- PANIC_LITE: **47** entry days — **test LIVE (>=15)**
- REVERSAL_3: **45** entry days — **test LIVE (>=15)**
- PULLBACK_50: **45** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **42** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **41** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **40** entry days — **test LIVE (>=15)**
- TREND_RIDER: **29** entry days — **test LIVE (>=15)**
- DEEP_DIP: **25** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **22** entry days — **test LIVE (>=15)**
- SHORT_EXT: **12** entry days
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean +367 bps over 25 entry days (row mean +700, n=52) · win rate per entry day 52% (row hit 67%)
- PANIC_BOUNCE: per-entry-day mean +86 bps over 42 entry days (row mean +54, n=331) · win rate per entry day 57% (row hit 53%)
- PANIC_LITE: per-entry-day mean +22 bps over 47 entry days (row mean +5, n=656) · win rate per entry day 49% (row hit 47%)
- DOUBLE_DIP: per-entry-day mean +41 bps over 41 entry days (row mean +84, n=266) · win rate per entry day 49% (row hit 52%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -163 bps over 22 entry days (row mean -89, n=53) · win rate per entry day 46% (row hit 42%)
- SHORT_EXT: per-entry-day mean +17 bps over 12 entry days (row mean +189, n=25) · win rate per entry day 42% (row hit 52%)
- TREND_RIDER: per-entry-day mean -55 bps over 29 entry days (row mean -68, n=83) · win rate per entry day 48% (row hit 48%)
- RSI2_DIP: per-entry-day mean +31 bps over 49 entry days (row mean +6, n=536) · win rate per entry day 49% (row hit 46%)
- REVERSAL_3: per-entry-day mean +23 bps over 45 entry days (row mean +18, n=310) · win rate per entry day 44% (row hit 48%)
- BOLL_SNAP: per-entry-day mean +47 bps over 40 entry days (row mean +245, n=193) · win rate per entry day 58% (row hit 58%)
- PULLBACK_50: per-entry-day mean +67 bps over 45 entry days (row mean +74, n=207) · win rate per entry day 62% (row hit 55%)
- Exits on copied/zero-volume bars: **0** of 2640 forward exits tested; 112 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+869 bps, n=26); keep me on a short leash in calm-up (+40). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-6). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-down (-12). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-21). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in storm-down (-190). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+441 bps, n=11); keep me on a short leash in calm-down (-436). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+288 bps, n=17); keep me on a short leash in calm-up (-174). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+450 bps, n=9); keep me on a short leash in calm-down (-41). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-up (-12 bps, n=209); keep me on a short leash in calm-down (-47). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+215 bps, n=33); keep me on a short leash in calm-up (+26). Status: WATCH — positive but not significant.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
