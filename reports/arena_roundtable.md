# Arena Roundtable — 2026-11-18

Tape: **storm-down** · session 2026-11-17 · 12 agents · opened 49, closed 23 this session · 295 open · 4616 forward closes all-time

> **This lab is 71% of the desk's scored record (4616 of 6458 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 295 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 23 closed this session, 4616 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+774), BOLL_SNAP (+436), DOUBLE_DIP (+299); cold hands: REVERSAL_3 (-74), FRESH_HIGH (-117). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 81% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -23 bps over 1849 trades (t=-1.73) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +101 (n=352, d=96) · SHORT_EXT +26 (n=170, d=61) · BOLL_SNAP -35 (n=410, d=107) · PANIC_LITE -53 (n=1864, d=129) · PANIC_BOUNCE -64 (n=886, d=111) · DOUBLE_DIP -64 (n=737, d=113) · DEEP_DIP -177 (n=119, d=64) · RSI2_DIP -205 (n=266, d=29) · REVERSAL_3 -221 (n=128, d=25) · PULLBACK_50 -232 (n=114, d=26) · TREND_RIDER -361 (n=77, d=25)
- **calm-down**: BOLL_SNAP +225 (n=125, d=23) · REVERSAL_3 -7 (n=62, d=12) · RSI2_DIP -85 (n=138, d=15) · DOUBLE_DIP -94 (n=246, d=26) · PULLBACK_50 -122 (n=46, d=13) · PANIC_LITE -124 (n=512, d=27) · TREND_RIDER -131 (n=27, d=12) · PANIC_BOUNCE -160 (n=290, d=24) · FRESH_HIGH -189 (n=48, d=17) · DEEP_DIP -244 (n=34, d=20)
- **storm-up**: PANIC_LITE +167 (n=99, d=4) · PANIC_BOUNCE +132 (n=70, d=4) · DOUBLE_DIP +114 (n=53, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +774 (n=45, d=19) · BOLL_SNAP +436 (n=301, d=31) · DOUBLE_DIP +299 (n=366, d=34) · PANIC_BOUNCE +275 (n=334, d=32) · STORM_DIP +234 (n=553, d=35) · PANIC_LITE +157 (n=658, d=38) · RSI2_DIP -4 (n=48, d=5) · REVERSAL_3 -74 (n=21, d=5) · FRESH_HIGH -117 (n=44, d=22)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **79** entry days — **test LIVE (>=15)**
- PANIC_LITE: **77** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **71** entry days — **test LIVE (>=15)**
- PULLBACK_50: **70** entry days — **test LIVE (>=15)**
- REVERSAL_3: **69** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **68** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **68** entry days — **test LIVE (>=15)**
- TREND_RIDER: **54** entry days — **test LIVE (>=15)**
- DEEP_DIP: **48** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **40** entry days — **test LIVE (>=15)**
- SHORT_EXT: **20** entry days — **test LIVE (>=15)**
- STORM_DIP: **3** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -345 bps over 48 entry days (row mean -56, n=92) · win rate per entry day 31% (row hit 42%)
- PANIC_BOUNCE: per-entry-day mean -50 bps over 71 entry days (row mean -125, n=632) · win rate per entry day 46% (row hit 43%)
- PANIC_LITE: per-entry-day mean -108 bps over 77 entry days (row mean -141, n=1098) · win rate per entry day 39% (row hit 40%)
- DOUBLE_DIP: per-entry-day mean -130 bps over 68 entry days (row mean -7, n=491) · win rate per entry day 38% (row hit 45%)
- STORM_DIP: per-entry-day mean +525 bps over 3 entry days (row mean +525, n=120) · win rate per entry day 67% (row hit 65%)
- FRESH_HIGH: per-entry-day mean -170 bps over 40 entry days (row mean -128, n=87) · win rate per entry day 40% (row hit 45%)
- SHORT_EXT: per-entry-day mean +161 bps over 20 entry days (row mean +169, n=36) · win rate per entry day 55% (row hit 53%)
- TREND_RIDER: per-entry-day mean -221 bps over 54 entry days (row mean -248, n=140) · win rate per entry day 43% (row hit 44%)
- RSI2_DIP: per-entry-day mean -58 bps over 79 entry days (row mean -67, n=790) · win rate per entry day 38% (row hit 44%)
- REVERSAL_3: per-entry-day mean -37 bps over 69 entry days (row mean -52, n=443) · win rate per entry day 39% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -35 bps over 68 entry days (row mean +116, n=384) · win rate per entry day 46% (row hit 52%)
- PULLBACK_50: per-entry-day mean -56 bps over 70 entry days (row mean -52, n=303) · win rate per entry day 53% (row hit 48%)
- Exits on copied/zero-volume bars: **0** of 4492 forward exits tested; 124 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+774 bps, n=45); keep me on a short leash in calm-down (-244). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+275 bps, n=334); keep me on a short leash in calm-down (-160). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+167 bps, n=99); keep me on a short leash in calm-down (-124). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+299 bps, n=366); keep me on a short leash in calm-down (-94). Status: DEAD — loses to costs/SPY.
- STORM_DIP to the desk: my weather is storm-down (+234 bps, n=553); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+962 bps, n=16); keep me on a short leash in calm-down (-189). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+244 bps, n=10); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (-131 bps, n=27); keep me on a short leash in calm-up (-361). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (-4 bps, n=48); keep me on a short leash in calm-up (-205). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (-7 bps, n=62); keep me on a short leash in calm-up (-221). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+436 bps, n=301); keep me on a short leash in storm-up (-72). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (+212 bps, n=19); keep me on a short leash in calm-up (-232). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
