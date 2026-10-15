# Arena Roundtable — 2026-10-15

Tape: **calm-up** · session 2026-10-15 · 12 agents · opened 43, closed 37 this session · 309 open · 3119 forward closes all-time

> **This lab is 68% of the desk's scored record (3082 of 4512 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 309 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 37 closed this session, 3119 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+210), SHORT_EXT (+5), PANIC_LITE (-10); cold hands: DEEP_DIP (-200), TREND_RIDER (-267). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 43% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 83% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +19 bps over 1697 trades (t=1.37) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +210 (n=418, d=110) · SHORT_EXT +5 (n=184, d=74) · PANIC_LITE -10 (n=1986, d=145) · PANIC_BOUNCE -22 (n=956, d=124) · BOLL_SNAP -29 (n=430, d=120) · DOUBLE_DIP -52 (n=797, d=125) · REVERSAL_3 -59 (n=250, d=43) · PULLBACK_50 -63 (n=211, d=43) · RSI2_DIP -77 (n=492, d=46) · DEEP_DIP -200 (n=118, d=68) · TREND_RIDER -267 (n=99, d=38)
- **calm-down**: BOLL_SNAP +179 (n=65, d=13) · DOUBLE_DIP +93 (n=122, d=15) · REVERSAL_3 +49 (n=26, d=3) · RSI2_DIP +47 (n=59, d=4) · PANIC_BOUNCE +11 (n=119, d=14) · PANIC_LITE -12 (n=208, d=15) · FRESH_HIGH -258 (n=33, d=12)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +1012 (n=24, d=14) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -113 (n=41, d=20)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **56** entry days — **test LIVE (>=15)**
- PANIC_LITE: **54** entry days — **test LIVE (>=15)**
- REVERSAL_3: **52** entry days — **test LIVE (>=15)**
- PULLBACK_50: **52** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **49** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **47** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **47** entry days — **test LIVE (>=15)**
- TREND_RIDER: **35** entry days — **test LIVE (>=15)**
- DEEP_DIP: **29** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **27** entry days — **test LIVE (>=15)**
- SHORT_EXT: **17** entry days — **test LIVE (>=15)**
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean +154 bps over 29 entry days (row mean +536, n=58) · win rate per entry day 45% (row hit 62%)
- PANIC_BOUNCE: per-entry-day mean +14 bps over 49 entry days (row mean -19, n=374) · win rate per entry day 51% (row hit 48%)
- PANIC_LITE: per-entry-day mean -34 bps over 54 entry days (row mean -61, n=755) · win rate per entry day 43% (row hit 43%)
- DOUBLE_DIP: per-entry-day mean -59 bps over 47 entry days (row mean -10, n=306) · win rate per entry day 43% (row hit 46%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -157 bps over 27 entry days (row mean -96, n=60) · win rate per entry day 41% (row hit 40%)
- SHORT_EXT: per-entry-day mean +134 bps over 17 entry days (row mean +171, n=32) · win rate per entry day 53% (row hit 53%)
- TREND_RIDER: per-entry-day mean +14 bps over 35 entry days (row mean -23, n=97) · win rate per entry day 51% (row hit 50%)
- RSI2_DIP: per-entry-day mean -20 bps over 56 entry days (row mean -25, n=596) · win rate per entry day 43% (row hit 44%)
- REVERSAL_3: per-entry-day mean -25 bps over 52 entry days (row mean -15, n=344) · win rate per entry day 38% (row hit 46%)
- BOLL_SNAP: per-entry-day mean +1 bps over 47 entry days (row mean +157, n=226) · win rate per entry day 51% (row hit 54%)
- PULLBACK_50: per-entry-day mean +3 bps over 52 entry days (row mean +31, n=231) · win rate per entry day 58% (row hit 52%)
- Exits on copied/zero-volume bars: **0** of 2805 forward exits tested; 314 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+1012 bps, n=24); keep me on a short leash in calm-up (-200). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-22). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-down (-12). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-52). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+654 bps, n=14); keep me on a short leash in calm-down (-258). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+611 bps, n=10); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-up (-267 bps, n=99); keep me on a short leash in calm-up (-267). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (+47 bps, n=59); keep me on a short leash in calm-up (-77). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+49 bps, n=26); keep me on a short leash in calm-up (-59). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (-14 bps, n=18); keep me on a short leash in calm-up (-63). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
