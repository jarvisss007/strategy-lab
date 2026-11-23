# Arena Roundtable — 2026-11-23

Tape: **storm-down** · session 2026-11-20 · 12 agents · opened 132, closed 83 this session · 310 open · 4912 forward closes all-time

> **This lab is 72% of the desk's scored record (4912 of 6823 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 85 of 310 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 83 closed this session, 4912 all-time. Oldest due row: DEEP_DIP BABA, entered 2026-11-09, hold 10, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+760), BOLL_SNAP (+409), PANIC_BOUNCE (+374); cold hands: REVERSAL_3 (-96), FRESH_HIGH (-238). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 81% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -24 bps over 1881 trades (t=-1.83) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +105 (n=343, d=95) · SHORT_EXT +28 (n=159, d=57) · BOLL_SNAP -47 (n=373, d=106) · PANIC_LITE -55 (n=1787, d=127) · PANIC_BOUNCE -72 (n=836, d=109) · DOUBLE_DIP -75 (n=708, d=112) · DEEP_DIP -150 (n=118, d=63) · PULLBACK_50 -201 (n=97, d=23) · RSI2_DIP -205 (n=230, d=26) · REVERSAL_3 -269 (n=104, d=22) · TREND_RIDER -408 (n=69, d=24)
- **calm-down**: BOLL_SNAP +224 (n=125, d=23) · REVERSAL_3 +17 (n=53, d=11) · RSI2_DIP -67 (n=122, d=14) · DOUBLE_DIP -111 (n=246, d=26) · PANIC_LITE -124 (n=512, d=27) · TREND_RIDER -152 (n=27, d=11) · PANIC_BOUNCE -160 (n=290, d=24) · PULLBACK_50 -238 (n=40, d=12) · DEEP_DIP -263 (n=32, d=20) · FRESH_HIGH -266 (n=53, d=17)
- **storm-up**: PANIC_LITE +169 (n=97, d=3) · PANIC_BOUNCE +137 (n=67, d=3) · DOUBLE_DIP +130 (n=52, d=3) · BOLL_SNAP -43 (n=22, d=3) · STORM_DIP -294 (n=87, d=3)
- **storm-down**: DEEP_DIP +760 (n=49, d=19) · BOLL_SNAP +409 (n=349, d=34) · PANIC_BOUNCE +374 (n=412, d=35) · DOUBLE_DIP +324 (n=426, d=37) · STORM_DIP +245 (n=616, d=38) · PANIC_LITE +171 (n=779, d=41) · PULLBACK_50 -74 (n=41, d=9) · RSI2_DIP -94 (n=83, d=9) · REVERSAL_3 -96 (n=49, d=9) · FRESH_HIGH -238 (n=42, d=22)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **82** entry days — **test LIVE (>=15)**
- PANIC_LITE: **80** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **74** entry days — **test LIVE (>=15)**
- REVERSAL_3: **72** entry days — **test LIVE (>=15)**
- PULLBACK_50: **72** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **71** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **71** entry days — **test LIVE (>=15)**
- TREND_RIDER: **57** entry days — **test LIVE (>=15)**
- DEEP_DIP: **50** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **42** entry days — **test LIVE (>=15)**
- SHORT_EXT: **21** entry days — **test LIVE (>=15)**
- STORM_DIP: **4** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -332 bps over 50 entry days (row mean -38, n=97) · win rate per entry day 32% (row hit 43%)
- PANIC_BOUNCE: per-entry-day mean -70 bps over 74 entry days (row mean -140, n=674) · win rate per entry day 45% (row hit 42%)
- PANIC_LITE: per-entry-day mean -119 bps over 80 entry days (row mean -150, n=1160) · win rate per entry day 38% (row hit 39%)
- DOUBLE_DIP: per-entry-day mean -148 bps over 71 entry days (row mean -69, n=531) · win rate per entry day 37% (row hit 42%)
- STORM_DIP: per-entry-day mean +248 bps over 4 entry days (row mean +248, n=160) · win rate per entry day 50% (row hit 52%)
- FRESH_HIGH: per-entry-day mean -203 bps over 42 entry days (row mean -178, n=95) · win rate per entry day 38% (row hit 42%)
- SHORT_EXT: per-entry-day mean +221 bps over 21 entry days (row mean +235, n=38) · win rate per entry day 57% (row hit 55%)
- TREND_RIDER: per-entry-day mean -287 bps over 57 entry days (row mean -280, n=147) · win rate per entry day 40% (row hit 42%)
- RSI2_DIP: per-entry-day mean -64 bps over 82 entry days (row mean -80, n=830) · win rate per entry day 38% (row hit 42%)
- REVERSAL_3: per-entry-day mean -40 bps over 72 entry days (row mean -62, n=468) · win rate per entry day 39% (row hit 43%)
- BOLL_SNAP: per-entry-day mean -79 bps over 71 entry days (row mean +67, n=402) · win rate per entry day 44% (row hit 50%)
- PULLBACK_50: per-entry-day mean -81 bps over 72 entry days (row mean -74, n=310) · win rate per entry day 51% (row hit 47%)
- Exits on copied/zero-volume bars: **0** of 4807 forward exits tested; 105 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+760 bps, n=49); keep me on a short leash in calm-down (-263). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+374 bps, n=412); keep me on a short leash in calm-down (-160). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-down (+171 bps, n=779); keep me on a short leash in calm-down (-124). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+324 bps, n=426); keep me on a short leash in calm-down (-111). Status: WATCH — positive but not significant.
- STORM_DIP to the desk: my weather is storm-down (+245 bps, n=616); keep me on a short leash in storm-up (-294). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+954 bps, n=10); keep me on a short leash in calm-down (-266). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+535 bps, n=10); keep me on a short leash in calm-up (+28). Status: WATCH — positive but not significant.
- TREND_RIDER to the desk: my weather is calm-down (-152 bps, n=27); keep me on a short leash in calm-up (-408). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (-67 bps, n=122); keep me on a short leash in calm-up (-205). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+17 bps, n=53); keep me on a short leash in calm-up (-269). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+409 bps, n=349); keep me on a short leash in calm-up (-47). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (-74 bps, n=41); keep me on a short leash in calm-down (-238). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
