# Arena Roundtable — 2026-11-27

Tape: **storm-down** · session 2026-11-27 · 12 agents · opened 5, closed 89 this session · 102 open · 5283 forward closes all-time

> **This lab is 73% of the desk's scored record (5194 of 7155 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 102 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 89 closed this session, 5283 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+820), BOLL_SNAP (+358), PANIC_BOUNCE (+270); cold hands: FRESH_HIGH (-83), RSI2_DIP (-89). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 81% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -16 bps over 1887 trades (t=-1.2) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +95 (n=306, d=91) · SHORT_EXT +17 (n=153, d=56) · BOLL_SNAP -39 (n=365, d=103) · PANIC_LITE -47 (n=1735, d=124) · PANIC_BOUNCE -61 (n=806, d=107) · DOUBLE_DIP -77 (n=681, d=109) · DEEP_DIP -171 (n=114, d=61) · RSI2_DIP -212 (n=229, d=24) · REVERSAL_3 -270 (n=100, d=21) · PULLBACK_50 -388 (n=85, d=22) · TREND_RIDER -437 (n=64, d=22)
- **calm-down**: BOLL_SNAP +224 (n=125, d=23) · REVERSAL_3 -22 (n=45, d=10) · DOUBLE_DIP -111 (n=246, d=26) · PANIC_LITE -124 (n=512, d=27) · PANIC_BOUNCE -160 (n=290, d=24) · RSI2_DIP -162 (n=88, d=12) · FRESH_HIGH -186 (n=53, d=17) · DEEP_DIP -241 (n=31, d=20) · PULLBACK_50 -299 (n=30, d=10) · TREND_RIDER -452 (n=21, d=9)
- **storm-up**: PANIC_LITE +169 (n=97, d=3) · PANIC_BOUNCE +137 (n=67, d=3) · DOUBLE_DIP +130 (n=52, d=3) · BOLL_SNAP -43 (n=22, d=3) · STORM_DIP -294 (n=87, d=3)
- **storm-down**: DEEP_DIP +820 (n=51, d=21) · BOLL_SNAP +358 (n=356, d=34) · PANIC_BOUNCE +270 (n=439, d=38) · DOUBLE_DIP +247 (n=454, d=39) · STORM_DIP +165 (n=618, d=39) · PANIC_LITE +148 (n=840, d=43) · PULLBACK_50 +89 (n=42, d=10) · REVERSAL_3 -71 (n=50, d=10) · FRESH_HIGH -83 (n=58, d=23) · RSI2_DIP -89 (n=86, d=12)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **86** entry days — **test LIVE (>=15)**
- PANIC_LITE: **83** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **77** entry days — **test LIVE (>=15)**
- PULLBACK_50: **76** entry days — **test LIVE (>=15)**
- REVERSAL_3: **75** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **75** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **75** entry days — **test LIVE (>=15)**
- TREND_RIDER: **59** entry days — **test LIVE (>=15)**
- DEEP_DIP: **52** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **43** entry days — **test LIVE (>=15)**
- SHORT_EXT: **21** entry days — **test LIVE (>=15)**
- STORM_DIP: **6** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -373 bps over 52 entry days (row mean -75, n=100) · win rate per entry day 31% (row hit 43%)
- PANIC_BOUNCE: per-entry-day mean -54 bps over 77 entry days (row mean -80, n=754) · win rate per entry day 47% (row hit 46%)
- PANIC_LITE: per-entry-day mean -105 bps over 83 entry days (row mean -120, n=1241) · win rate per entry day 40% (row hit 42%)
- DOUBLE_DIP: per-entry-day mean -134 bps over 75 entry days (row mean -62, n=573) · win rate per entry day 39% (row hit 42%)
- STORM_DIP: per-entry-day mean +180 bps over 6 entry days (row mean +187, n=200) · win rate per entry day 50% (row hit 52%)
- FRESH_HIGH: per-entry-day mean -209 bps over 43 entry days (row mean -181, n=96) · win rate per entry day 37% (row hit 42%)
- SHORT_EXT: per-entry-day mean +221 bps over 21 entry days (row mean +235, n=38) · win rate per entry day 57% (row hit 55%)
- TREND_RIDER: per-entry-day mean -300 bps over 59 entry days (row mean -299, n=156) · win rate per entry day 39% (row hit 41%)
- RSI2_DIP: per-entry-day mean -56 bps over 86 entry days (row mean -74, n=861) · win rate per entry day 38% (row hit 43%)
- REVERSAL_3: per-entry-day mean -28 bps over 75 entry days (row mean -54, n=485) · win rate per entry day 41% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -71 bps over 75 entry days (row mean +80, n=445) · win rate per entry day 44% (row hit 51%)
- PULLBACK_50: per-entry-day mean -86 bps over 76 entry days (row mean -83, n=334) · win rate per entry day 51% (row hit 46%)
- Exits on copied/zero-volume bars: **0** of 4892 forward exits tested; 391 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+820 bps, n=51); keep me on a short leash in calm-down (-241). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+270 bps, n=439); keep me on a short leash in calm-down (-160). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+169 bps, n=97); keep me on a short leash in calm-down (-124). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+247 bps, n=454); keep me on a short leash in calm-down (-111). Status: DEAD — loses to costs/SPY.
- STORM_DIP to the desk: my weather is storm-down (+165 bps, n=618); keep me on a short leash in storm-up (-294). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+954 bps, n=10); keep me on a short leash in calm-down (-186). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+615 bps, n=9); keep me on a short leash in calm-up (+17). Status: WATCH — positive but not significant.
- TREND_RIDER to the desk: my weather is storm-down (+49 bps, n=13); keep me on a short leash in calm-down (-452). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (-89 bps, n=86); keep me on a short leash in calm-up (-212). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (-22 bps, n=45); keep me on a short leash in calm-up (-270). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+358 bps, n=356); keep me on a short leash in storm-up (-43). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (+89 bps, n=42); keep me on a short leash in calm-up (-388). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
