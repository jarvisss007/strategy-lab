# Arena Roundtable — 2026-11-22

Tape: **storm-down** · session 2026-11-20 · 12 agents · opened 132, closed 83 this session · 310 open · 4912 forward closes all-time

> **This lab is 72% of the desk's scored record (4912 of 6782 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 310 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 83 closed this session, 4912 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+713), BOLL_SNAP (+326), PANIC_BOUNCE (+194); cold hands: FRESH_HIGH (-219), PULLBACK_50 (-221). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 44% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 81% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -41 bps over 1868 trades (t=-3.02) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +95 (n=321, d=95) · SHORT_EXT +13 (n=163, d=60) · BOLL_SNAP -43 (n=369, d=105) · PANIC_LITE -55 (n=1786, d=127) · PANIC_BOUNCE -72 (n=836, d=109) · DOUBLE_DIP -75 (n=706, d=111) · DEEP_DIP -150 (n=118, d=63) · PULLBACK_50 -185 (n=102, d=24) · RSI2_DIP -212 (n=243, d=27) · REVERSAL_3 -265 (n=111, d=23) · TREND_RIDER -397 (n=71, d=25)
- **calm-down**: BOLL_SNAP +224 (n=125, d=23) · REVERSAL_3 +17 (n=53, d=11) · RSI2_DIP -75 (n=118, d=14) · DOUBLE_DIP -111 (n=246, d=26) · PANIC_LITE -124 (n=512, d=27) · PANIC_BOUNCE -160 (n=290, d=24) · PULLBACK_50 -223 (n=38, d=12) · FRESH_HIGH -246 (n=60, d=17) · DEEP_DIP -344 (n=32, d=20) · TREND_RIDER -355 (n=27, d=11)
- **storm-up**: FRESH_HIGH +537 (n=35, d=3) · PANIC_LITE +164 (n=100, d=4) · PANIC_BOUNCE +132 (n=70, d=4) · DOUBLE_DIP +94 (n=56, d=4) · BOLL_SNAP -109 (n=26, d=4) · STORM_DIP -296 (n=90, d=4)
- **storm-down**: DEEP_DIP +713 (n=43, d=18) · BOLL_SNAP +326 (n=320, d=33) · PANIC_BOUNCE +194 (n=341, d=34) · DOUBLE_DIP +156 (n=364, d=36) · STORM_DIP +107 (n=537, d=37) · PANIC_LITE +68 (n=718, d=40) · RSI2_DIP -143 (n=78, d=8) · REVERSAL_3 -146 (n=48, d=8) · FRESH_HIGH -219 (n=37, d=21) · PULLBACK_50 -221 (n=35, d=8)

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
- Exits on copied/zero-volume bars: **0** of 4492 forward exits tested; 420 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+713 bps, n=43); keep me on a short leash in calm-down (-344). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+194 bps, n=341); keep me on a short leash in calm-down (-160). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+164 bps, n=100); keep me on a short leash in calm-down (-124). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+156 bps, n=364); keep me on a short leash in calm-down (-111). Status: DEAD — loses to costs/SPY.
- STORM_DIP to the desk: my weather is storm-down (+107 bps, n=537); keep me on a short leash in storm-up (-296). Status: WATCH — positive but not significant.
- FRESH_HIGH to the desk: my weather is storm-up (+537 bps, n=35); keep me on a short leash in calm-down (-246). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+360 bps, n=10); keep me on a short leash in calm-up (+13). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (-355 bps, n=27); keep me on a short leash in calm-up (-397). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (-75 bps, n=118); keep me on a short leash in calm-up (-212). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+17 bps, n=53); keep me on a short leash in calm-up (-265). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+326 bps, n=320); keep me on a short leash in storm-up (-109). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-up (-185 bps, n=102); keep me on a short leash in calm-down (-223). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
