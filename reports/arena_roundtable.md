# Arena Roundtable — 2026-11-12

Tape: **calm-down** · session 2026-11-11 · 12 agents · opened 16, closed 45 this session · 135 open · 4442 forward closes all-time

> **This lab is 71% of the desk's scored record (4442 of 6229 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 49 of 135 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 45 closed this session, 4442 all-time. Oldest due row: TREND_RIDER JNJ, entered 2026-10-22, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-DOWN. Our pooled record in this weather — hot hands: BOLL_SNAP (+265), DOUBLE_DIP (+42), TREND_RIDER (+40); cold hands: PANIC_BOUNCE (-91), FRESH_HIGH (-130). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 47% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -11 bps over 1834 trades (t=-0.82) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +82 (n=370, d=99) · SHORT_EXT +18 (n=172, d=61) · PANIC_LITE -58 (n=1937, d=133) · PANIC_BOUNCE -76 (n=928, d=115) · BOLL_SNAP -86 (n=432, d=111) · DOUBLE_DIP -98 (n=776, d=117) · RSI2_DIP -113 (n=326, d=33) · REVERSAL_3 -124 (n=163, d=29) · DEEP_DIP -196 (n=115, d=66) · PULLBACK_50 -217 (n=129, d=30) · TREND_RIDER -220 (n=88, d=29)
- **calm-down**: BOLL_SNAP +265 (n=122, d=21) · DOUBLE_DIP +42 (n=213, d=24) · TREND_RIDER +40 (n=22, d=10) · DEEP_DIP -12 (n=32, d=19) · REVERSAL_3 -16 (n=61, d=11) · RSI2_DIP -39 (n=121, d=13) · PANIC_LITE -47 (n=461, d=25) · PULLBACK_50 -50 (n=39, d=11) · PANIC_BOUNCE -91 (n=269, d=22) · FRESH_HIGH -130 (n=47, d=16)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +114 (n=53, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +802 (n=45, d=18) · BOLL_SNAP +462 (n=300, d=30) · DOUBLE_DIP +335 (n=343, d=33) · PANIC_BOUNCE +327 (n=309, d=31) · STORM_DIP +277 (n=498, d=34) · PANIC_LITE +179 (n=631, d=37) · RSI2_DIP +10 (n=41, d=4) · FRESH_HIGH -85 (n=44, d=23)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **75** entry days — **test LIVE (>=15)**
- PANIC_LITE: **73** entry days — **test LIVE (>=15)**
- PULLBACK_50: **68** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **67** entry days — **test LIVE (>=15)**
- REVERSAL_3: **67** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **65** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **64** entry days — **test LIVE (>=15)**
- TREND_RIDER: **50** entry days — **test LIVE (>=15)**
- DEEP_DIP: **44** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **37** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **3** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -213 bps over 44 entry days (row mean +134, n=81) · win rate per entry day 34% (row hit 48%)
- PANIC_BOUNCE: per-entry-day mean -7 bps over 67 entry days (row mean -86, n=595) · win rate per entry day 49% (row hit 45%)
- PANIC_LITE: per-entry-day mean -88 bps over 73 entry days (row mean -117, n=1030) · win rate per entry day 41% (row hit 41%)
- DOUBLE_DIP: per-entry-day mean -86 bps over 64 entry days (row mean +8, n=482) · win rate per entry day 39% (row hit 45%)
- STORM_DIP: per-entry-day mean +525 bps over 3 entry days (row mean +525, n=120) · win rate per entry day 67% (row hit 65%)
- FRESH_HIGH: per-entry-day mean -188 bps over 37 entry days (row mean -147, n=80) · win rate per entry day 38% (row hit 41%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -184 bps over 50 entry days (row mean -214, n=131) · win rate per entry day 44% (row hit 44%)
- RSI2_DIP: per-entry-day mean -59 bps over 75 entry days (row mean -66, n=776) · win rate per entry day 37% (row hit 44%)
- REVERSAL_3: per-entry-day mean -46 bps over 67 entry days (row mean -54, n=440) · win rate per entry day 39% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -15 bps over 65 entry days (row mean +124, n=379) · win rate per entry day 46% (row hit 52%)
- PULLBACK_50: per-entry-day mean -68 bps over 68 entry days (row mean -65, n=294) · win rate per entry day 52% (row hit 47%)
- Exits on copied/zero-volume bars: **0** of 4171 forward exits tested; 271 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+802 bps, n=45); keep me on a short leash in calm-up (-196). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+327 bps, n=309); keep me on a short leash in calm-down (-91). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-down (+179 bps, n=631); keep me on a short leash in calm-up (-58). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+335 bps, n=343); keep me on a short leash in calm-up (-98). Status: DEAD — loses to costs/SPY.
- STORM_DIP to the desk: my weather is storm-down (+277 bps, n=498); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+1120 bps, n=12); keep me on a short leash in calm-down (-130). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+328 bps, n=9); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+40 bps, n=22); keep me on a short leash in calm-up (-220). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+10 bps, n=41); keep me on a short leash in calm-up (-113). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (-16 bps, n=61); keep me on a short leash in calm-up (-124). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+462 bps, n=300); keep me on a short leash in calm-up (-86). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (+412 bps, n=12); keep me on a short leash in calm-up (-217). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
