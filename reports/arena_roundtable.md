# Arena Roundtable — 2026-10-03

Tape: **calm-up** · session 2026-10-02 · 12 agents · opened 20, closed 43 this session · 116 open · 2692 forward closes all-time

> **This lab is 70% of the desk's scored record (2692 of 3870 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 116 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 43 closed this session, 2692 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+231), PULLBACK_50 (+28), DEEP_DIP (+11); cold hands: RSI2_DIP (-36), TREND_RIDER (-180). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 42% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +42 bps over 1627 trades (t=3.0) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +231 (n=418, d=109) · PULLBACK_50 +28 (n=173, d=37) · DEEP_DIP +11 (n=107, d=71) · PANIC_LITE +6 (n=1858, d=143) · SHORT_EXT -2 (n=183, d=69) · PANIC_BOUNCE -5 (n=899, d=122) · BOLL_SNAP -10 (n=380, d=117) · REVERSAL_3 -12 (n=208, d=38) · DOUBLE_DIP -16 (n=751, d=124) · RSI2_DIP -36 (n=410, d=40) · TREND_RIDER -180 (n=90, d=31)
- **calm-down**: TREND_RIDER +355 (n=24, d=9) · BOLL_SNAP +315 (n=76, d=14) · PANIC_BOUNCE +178 (n=142, d=15) · PANIC_LITE +121 (n=255, d=16) · PULLBACK_50 +111 (n=44, d=9) · DOUBLE_DIP +109 (n=125, d=16) · REVERSAL_3 -9 (n=67, d=7) · FRESH_HIGH -163 (n=33, d=12) · RSI2_DIP -217 (n=139, d=9)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +868 (n=27, d=15) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -190 (n=34, d=19)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **47** entry days — **test LIVE (>=15)**
- PANIC_LITE: **45** entry days — **test LIVE (>=15)**
- REVERSAL_3: **44** entry days — **test LIVE (>=15)**
- PULLBACK_50: **43** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **41** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **40** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **38** entry days — **test LIVE (>=15)**
- TREND_RIDER: **27** entry days — **test LIVE (>=15)**
- DEEP_DIP: **24** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **21** entry days — **test LIVE (>=15)**
- SHORT_EXT: **11** entry days
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean +394 bps over 24 entry days (row mean +720, n=51) · win rate per entry day 54% (row hit 69%)
- PANIC_BOUNCE: per-entry-day mean +96 bps over 41 entry days (row mean +57, n=329) · win rate per entry day 58% (row hit 53%)
- PANIC_LITE: per-entry-day mean +21 bps over 45 entry days (row mean +6, n=646) · win rate per entry day 49% (row hit 47%)
- DOUBLE_DIP: per-entry-day mean +37 bps over 40 entry days (row mean +83, n=265) · win rate per entry day 48% (row hit 52%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -174 bps over 21 entry days (row mean -100, n=50) · win rate per entry day 43% (row hit 40%)
- SHORT_EXT: per-entry-day mean +76 bps over 11 entry days (row mean +223, n=24) · win rate per entry day 46% (row hit 54%)
- TREND_RIDER: per-entry-day mean -64 bps over 27 entry days (row mean -72, n=76) · win rate per entry day 48% (row hit 50%)
- RSI2_DIP: per-entry-day mean +25 bps over 47 entry days (row mean +2, n=522) · win rate per entry day 47% (row hit 45%)
- REVERSAL_3: per-entry-day mean +21 bps over 44 entry days (row mean +17, n=305) · win rate per entry day 43% (row hit 48%)
- BOLL_SNAP: per-entry-day mean +38 bps over 38 entry days (row mean +247, n=185) · win rate per entry day 55% (row hit 57%)
- PULLBACK_50: per-entry-day mean +58 bps over 43 entry days (row mean +69, n=199) · win rate per entry day 60% (row hit 54%)
- Exits on copied/zero-volume bars: **0** of 2394 forward exits tested; 298 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+868 bps, n=27); keep me on a short leash in calm-up (+11). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-5). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (+6). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-16). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in storm-down (-190). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+441 bps, n=11); keep me on a short leash in calm-down (-299). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+355 bps, n=24); keep me on a short leash in calm-up (-180). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-217). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (-9 bps, n=67); keep me on a short leash in calm-up (-12). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+111 bps, n=44); keep me on a short leash in calm-up (+28). Status: WATCH — positive but not significant.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
