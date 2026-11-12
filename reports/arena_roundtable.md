# Arena Roundtable — 2026-11-12

Tape: **calm-down** · session 2026-11-12 · 12 agents · opened 71, closed 49 this session · 157 open · 4491 forward closes all-time

> **This lab is 71% of the desk's scored record (4442 of 6230 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 157 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 49 closed this session, 4491 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-DOWN. Our pooled record in this weather — hot hands: BOLL_SNAP (+260), DOUBLE_DIP (+38), REVERSAL_3 (-13); cold hands: PANIC_BOUNCE (-104), FRESH_HIGH (-124). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -12 bps over 1831 trades (t=-0.85) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +87 (n=366, d=99) · SHORT_EXT +29 (n=172, d=62) · PANIC_LITE -56 (n=1931, d=132) · PANIC_BOUNCE -75 (n=923, d=114) · BOLL_SNAP -83 (n=427, d=110) · DOUBLE_DIP -97 (n=768, d=116) · RSI2_DIP -138 (n=302, d=33) · REVERSAL_3 -147 (n=148, d=29) · PULLBACK_50 -222 (n=125, d=29) · TREND_RIDER -224 (n=87, d=28) · DEEP_DIP -252 (n=119, d=66)
- **calm-down**: BOLL_SNAP +260 (n=122, d=21) · DOUBLE_DIP +38 (n=213, d=24) · REVERSAL_3 -13 (n=61, d=11) · TREND_RIDER -24 (n=22, d=10) · RSI2_DIP -46 (n=122, d=13) · PULLBACK_50 -54 (n=39, d=11) · PANIC_LITE -63 (n=461, d=25) · DEEP_DIP -93 (n=34, d=19) · PANIC_BOUNCE -104 (n=269, d=22) · FRESH_HIGH -124 (n=48, d=16)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +114 (n=53, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +945 (n=44, d=19) · BOLL_SNAP +462 (n=300, d=30) · DOUBLE_DIP +333 (n=344, d=33) · PANIC_BOUNCE +327 (n=309, d=31) · STORM_DIP +277 (n=498, d=34) · PANIC_LITE +175 (n=628, d=37) · RSI2_DIP +10 (n=41, d=4) · FRESH_HIGH -68 (n=41, d=22)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **76** entry days — **test LIVE (>=15)**
- PANIC_LITE: **74** entry days — **test LIVE (>=15)**
- PULLBACK_50: **69** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **68** entry days — **test LIVE (>=15)**
- REVERSAL_3: **67** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **66** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **65** entry days — **test LIVE (>=15)**
- TREND_RIDER: **51** entry days — **test LIVE (>=15)**
- DEEP_DIP: **45** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **38** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **3** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -246 bps over 45 entry days (row mean +90, n=83) · win rate per entry day 33% (row hit 47%)
- PANIC_BOUNCE: per-entry-day mean -12 bps over 68 entry days (row mean -90, n=604) · win rate per entry day 48% (row hit 44%)
- PANIC_LITE: per-entry-day mean -87 bps over 74 entry days (row mean -116, n=1055) · win rate per entry day 40% (row hit 41%)
- DOUBLE_DIP: per-entry-day mean -81 bps over 65 entry days (row mean +9, n=484) · win rate per entry day 40% (row hit 46%)
- STORM_DIP: per-entry-day mean +525 bps over 3 entry days (row mean +525, n=120) · win rate per entry day 67% (row hit 65%)
- FRESH_HIGH: per-entry-day mean -180 bps over 38 entry days (row mean -140, n=82) · win rate per entry day 40% (row hit 43%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -169 bps over 51 entry days (row mean -208, n=132) · win rate per entry day 45% (row hit 45%)
- RSI2_DIP: per-entry-day mean -58 bps over 76 entry days (row mean -66, n=777) · win rate per entry day 38% (row hit 44%)
- REVERSAL_3: per-entry-day mean -46 bps over 67 entry days (row mean -54, n=440) · win rate per entry day 39% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -12 bps over 66 entry days (row mean +124, n=381) · win rate per entry day 47% (row hit 53%)
- PULLBACK_50: per-entry-day mean -59 bps over 69 entry days (row mean -55, n=299) · win rate per entry day 52% (row hit 48%)
- Exits on copied/zero-volume bars: **0** of 4171 forward exits tested; 320 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+945 bps, n=44); keep me on a short leash in calm-up (-252). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+327 bps, n=309); keep me on a short leash in calm-down (-104). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-down (+175 bps, n=628); keep me on a short leash in calm-down (-63). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+333 bps, n=344); keep me on a short leash in calm-up (-97). Status: DEAD — loses to costs/SPY.
- STORM_DIP to the desk: my weather is storm-down (+277 bps, n=498); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+944 bps, n=14); keep me on a short leash in calm-down (-124). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+303 bps, n=9); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (-24 bps, n=22); keep me on a short leash in calm-up (-224). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+10 bps, n=41); keep me on a short leash in calm-up (-138). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (-13 bps, n=61); keep me on a short leash in calm-up (-147). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+462 bps, n=300); keep me on a short leash in calm-up (-83). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (+381 bps, n=12); keep me on a short leash in calm-up (-222). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
