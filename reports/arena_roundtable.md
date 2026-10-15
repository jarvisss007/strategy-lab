# Arena Roundtable — 2026-10-15

Tape: **calm-up** · session 2026-10-14 · 12 agents · opened 159, closed 87 this session · 303 open · 3082 forward closes all-time

> **This lab is 68% of the desk's scored record (3082 of 4511 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 37 of 303 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 87 closed this session, 3082 all-time. Oldest due row: TREND_RIDER V, entered 2026-09-24, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+205), SHORT_EXT (+0), PANIC_LITE (-16); cold hands: DEEP_DIP (-214), TREND_RIDER (-241). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 42% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 83% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +16 bps over 1700 trades (t=1.14) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +205 (n=420, d=111) · SHORT_EXT +0 (n=183, d=73) · PANIC_LITE -16 (n=1989, d=146) · PANIC_BOUNCE -30 (n=956, d=124) · BOLL_SNAP -50 (n=430, d=120) · DOUBLE_DIP -52 (n=804, d=126) · REVERSAL_3 -64 (n=254, d=44) · PULLBACK_50 -77 (n=212, d=44) · RSI2_DIP -78 (n=500, d=47) · DEEP_DIP -214 (n=117, d=69) · TREND_RIDER -241 (n=102, d=37)
- **calm-down**: BOLL_SNAP +179 (n=65, d=13) · DOUBLE_DIP +93 (n=122, d=15) · REVERSAL_3 +49 (n=26, d=3) · RSI2_DIP +47 (n=59, d=4) · PANIC_BOUNCE +11 (n=119, d=14) · PANIC_LITE -12 (n=208, d=15) · FRESH_HIGH -258 (n=33, d=12)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +1066 (n=24, d=13) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -128 (n=38, d=20)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **55** entry days — **test LIVE (>=15)**
- PANIC_LITE: **53** entry days — **test LIVE (>=15)**
- REVERSAL_3: **51** entry days — **test LIVE (>=15)**
- PULLBACK_50: **51** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **48** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **46** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **46** entry days — **test LIVE (>=15)**
- TREND_RIDER: **34** entry days — **test LIVE (>=15)**
- DEEP_DIP: **29** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **27** entry days — **test LIVE (>=15)**
- SHORT_EXT: **16** entry days — **test LIVE (>=15)**
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean +154 bps over 29 entry days (row mean +536, n=58) · win rate per entry day 45% (row hit 62%)
- PANIC_BOUNCE: per-entry-day mean +22 bps over 48 entry days (row mean -16, n=371) · win rate per entry day 52% (row hit 48%)
- PANIC_LITE: per-entry-day mean -24 bps over 53 entry days (row mean -58, n=750) · win rate per entry day 43% (row hit 43%)
- DOUBLE_DIP: per-entry-day mean -41 bps over 46 entry days (row mean +2, n=302) · win rate per entry day 44% (row hit 46%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -157 bps over 27 entry days (row mean -96, n=60) · win rate per entry day 41% (row hit 40%)
- SHORT_EXT: per-entry-day mean +110 bps over 16 entry days (row mean +160, n=31) · win rate per entry day 50% (row hit 52%)
- TREND_RIDER: per-entry-day mean -6 bps over 34 entry days (row mean -38, n=95) · win rate per entry day 50% (row hit 48%)
- RSI2_DIP: per-entry-day mean -9 bps over 55 entry days (row mean -22, n=593) · win rate per entry day 44% (row hit 44%)
- REVERSAL_3: per-entry-day mean -12 bps over 51 entry days (row mean -11, n=342) · win rate per entry day 39% (row hit 46%)
- BOLL_SNAP: per-entry-day mean +8 bps over 46 entry days (row mean +182, n=215) · win rate per entry day 52% (row hit 55%)
- PULLBACK_50: per-entry-day mean +18 bps over 51 entry days (row mean +52, n=225) · win rate per entry day 59% (row hit 53%)
- Exits on copied/zero-volume bars: **0** of 2805 forward exits tested; 277 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+1066 bps, n=24); keep me on a short leash in calm-up (-214). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-30). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (-16). Status: WATCH — positive but not significant.
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-52). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+654 bps, n=14); keep me on a short leash in calm-down (-258). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+611 bps, n=10); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-up (-241 bps, n=102); keep me on a short leash in calm-up (-241). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (+47 bps, n=59); keep me on a short leash in calm-up (-78). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+49 bps, n=26); keep me on a short leash in calm-up (-64). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (-14 bps, n=18); keep me on a short leash in calm-up (-77). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
