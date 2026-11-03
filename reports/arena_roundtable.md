# Arena Roundtable — 2026-11-03

Tape: **storm-down** · session 2026-11-02 · 12 agents · opened 63, closed 45 this session · 304 open · 3896 forward closes all-time

> **This lab is 70% of the desk's scored record (3896 of 5579 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 304 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 45 closed this session, 3896 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+853), DOUBLE_DIP (+382), BOLL_SNAP (+368); cold hands: PANIC_LITE (+135), FRESH_HIGH (-137). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -9 bps over 1814 trades (t=-0.68) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +93 (n=392, d=105) · SHORT_EXT +27 (n=173, d=64) · PANIC_LITE -53 (n=1995, d=139) · PANIC_BOUNCE -66 (n=960, d=121) · BOLL_SNAP -89 (n=450, d=117) · DOUBLE_DIP -92 (n=811, d=122) · REVERSAL_3 -120 (n=199, d=35) · RSI2_DIP -120 (n=396, d=40) · PULLBACK_50 -147 (n=154, d=36) · DEEP_DIP -192 (n=127, d=79) · TREND_RIDER -259 (n=98, d=35)
- **calm-down**: DEEP_DIP +201 (n=28, d=16) · BOLL_SNAP +193 (n=114, d=19) · DOUBLE_DIP +39 (n=208, d=21) · PULLBACK_50 +15 (n=35, d=9) · PANIC_LITE -26 (n=384, d=21) · RSI2_DIP -29 (n=104, d=9) · REVERSAL_3 -32 (n=53, d=8) · PANIC_BOUNCE -47 (n=226, d=19) · FRESH_HIGH -199 (n=39, d=14)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +853 (n=34, d=16) · DOUBLE_DIP +382 (n=266, d=30) · BOLL_SNAP +368 (n=259, d=28) · STORM_DIP +341 (n=429, d=31) · PANIC_BOUNCE +187 (n=269, d=29) · PANIC_LITE +135 (n=594, d=34) · FRESH_HIGH -137 (n=46, d=21)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **68** entry days — **test LIVE (>=15)**
- PANIC_LITE: **66** entry days — **test LIVE (>=15)**
- PULLBACK_50: **61** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **60** entry days — **test LIVE (>=15)**
- REVERSAL_3: **60** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **58** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **58** entry days — **test LIVE (>=15)**
- TREND_RIDER: **46** entry days — **test LIVE (>=15)**
- DEEP_DIP: **39** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **36** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -232 bps over 39 entry days (row mean +171, n=75) · win rate per entry day 33% (row hit 49%)
- PANIC_BOUNCE: per-entry-day mean -21 bps over 60 entry days (row mean -51, n=508) · win rate per entry day 50% (row hit 47%)
- PANIC_LITE: per-entry-day mean -71 bps over 66 entry days (row mean -91, n=931) · win rate per entry day 41% (row hit 43%)
- DOUBLE_DIP: per-entry-day mean -71 bps over 58 entry days (row mean -29, n=401) · win rate per entry day 40% (row hit 44%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -184 bps over 36 entry days (row mean -151, n=80) · win rate per entry day 36% (row hit 40%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -148 bps over 46 entry days (row mean -162, n=120) · win rate per entry day 46% (row hit 46%)
- RSI2_DIP: per-entry-day mean -46 bps over 68 entry days (row mean -59, n=707) · win rate per entry day 38% (row hit 43%)
- REVERSAL_3: per-entry-day mean -50 bps over 60 entry days (row mean -51, n=412) · win rate per entry day 38% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -26 bps over 58 entry days (row mean +70, n=315) · win rate per entry day 47% (row hit 49%)
- PULLBACK_50: per-entry-day mean -35 bps over 61 entry days (row mean -28, n=273) · win rate per entry day 52% (row hit 48%)
- Exits on copied/zero-volume bars: **0** of 3759 forward exits tested; 137 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+853 bps, n=34); keep me on a short leash in calm-up (-192). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+187 bps, n=269); keep me on a short leash in calm-up (-66). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+162 bps, n=98); keep me on a short leash in calm-up (-53). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+382 bps, n=266); keep me on a short leash in calm-up (-92). Status: DEAD — loses to costs/SPY.
- STORM_DIP to the desk: my weather is storm-down (+341 bps, n=429); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+815 bps, n=17); keep me on a short leash in calm-down (-199). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+511 bps, n=8); keep me on a short leash in calm-down (-323). Status: WATCH — positive but not significant.
- TREND_RIDER to the desk: my weather is calm-down (+12 bps, n=10); keep me on a short leash in calm-up (-259). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (-29 bps, n=104); keep me on a short leash in calm-up (-120). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (-32 bps, n=53); keep me on a short leash in calm-up (-120). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+368 bps, n=259); keep me on a short leash in calm-up (-89). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+15 bps, n=35); keep me on a short leash in calm-up (-147). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
