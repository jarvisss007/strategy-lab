# Arena Roundtable — 2026-11-10

Tape: **calm-down** · session 2026-11-10 · 12 agents · opened 41, closed 130 this session · 164 open · 4397 forward closes all-time

> **This lab is 71% of the desk's scored record (4267 of 6047 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 164 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 130 closed this session, 4397 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-DOWN. Our pooled record in this weather — hot hands: BOLL_SNAP (+258), DOUBLE_DIP (+48), REVERSAL_3 (-20); cold hands: PANIC_BOUNCE (-90), FRESH_HIGH (-213). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -13 bps over 1817 trades (t=-0.92) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +86 (n=381, d=100) · SHORT_EXT +9 (n=172, d=62) · PANIC_LITE -57 (n=1945, d=134) · PANIC_BOUNCE -76 (n=936, d=116) · BOLL_SNAP -89 (n=432, d=112) · DOUBLE_DIP -98 (n=779, d=118) · REVERSAL_3 -130 (n=170, d=30) · RSI2_DIP -143 (n=335, d=34) · DEEP_DIP -194 (n=117, d=70) · PULLBACK_50 -226 (n=131, d=32) · TREND_RIDER -256 (n=88, d=30)
- **calm-down**: BOLL_SNAP +258 (n=122, d=21) · DOUBLE_DIP +48 (n=210, d=22) · REVERSAL_3 -20 (n=60, d=10) · DEEP_DIP -31 (n=30, d=19) · RSI2_DIP -41 (n=113, d=11) · TREND_RIDER -57 (n=21, d=9) · PANIC_LITE -63 (n=434, d=23) · PULLBACK_50 -70 (n=38, d=10) · PANIC_BOUNCE -90 (n=258, d=20) · FRESH_HIGH -213 (n=47, d=16)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +669 (n=48, d=20) · BOLL_SNAP +461 (n=300, d=30) · PANIC_BOUNCE +327 (n=309, d=31) · DOUBLE_DIP +323 (n=343, d=33) · STORM_DIP +276 (n=498, d=34) · PANIC_LITE +181 (n=632, d=37) · RSI2_DIP -6 (n=41, d=4) · FRESH_HIGH -95 (n=42, d=23)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **74** entry days — **test LIVE (>=15)**
- PANIC_LITE: **72** entry days — **test LIVE (>=15)**
- PULLBACK_50: **67** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **66** entry days — **test LIVE (>=15)**
- REVERSAL_3: **66** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **64** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **63** entry days — **test LIVE (>=15)**
- TREND_RIDER: **49** entry days — **test LIVE (>=15)**
- DEEP_DIP: **44** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **37** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **3** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -213 bps over 44 entry days (row mean +134, n=81) · win rate per entry day 34% (row hit 48%)
- PANIC_BOUNCE: per-entry-day mean -18 bps over 66 entry days (row mean -87, n=594) · win rate per entry day 48% (row hit 45%)
- PANIC_LITE: per-entry-day mean -89 bps over 72 entry days (row mean -118, n=1027) · win rate per entry day 40% (row hit 41%)
- DOUBLE_DIP: per-entry-day mean -99 bps over 63 entry days (row mean +6, n=481) · win rate per entry day 38% (row hit 45%)
- STORM_DIP: per-entry-day mean +525 bps over 3 entry days (row mean +525, n=120) · win rate per entry day 67% (row hit 65%)
- FRESH_HIGH: per-entry-day mean -188 bps over 37 entry days (row mean -147, n=80) · win rate per entry day 38% (row hit 41%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -163 bps over 49 entry days (row mean -191, n=128) · win rate per entry day 45% (row hit 45%)
- RSI2_DIP: per-entry-day mean -62 bps over 74 entry days (row mean -75, n=752) · win rate per entry day 36% (row hit 43%)
- REVERSAL_3: per-entry-day mean -49 bps over 66 entry days (row mean -55, n=437) · win rate per entry day 38% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -30 bps over 64 entry days (row mean +111, n=373) · win rate per entry day 45% (row hit 52%)
- PULLBACK_50: per-entry-day mean -70 bps over 67 entry days (row mean -67, n=290) · win rate per entry day 51% (row hit 47%)
- Exits on copied/zero-volume bars: **0** of 4171 forward exits tested; 226 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+669 bps, n=48); keep me on a short leash in calm-up (-194). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+327 bps, n=309); keep me on a short leash in calm-down (-90). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-down (+181 bps, n=632); keep me on a short leash in calm-down (-63). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+323 bps, n=343); keep me on a short leash in calm-up (-98). Status: DEAD — loses to costs/SPY.
- STORM_DIP to the desk: my weather is storm-down (+276 bps, n=498); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+1120 bps, n=12); keep me on a short leash in calm-down (-213). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+315 bps, n=9); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (-57 bps, n=21); keep me on a short leash in calm-up (-256). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (-6 bps, n=41); keep me on a short leash in calm-up (-143). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (-20 bps, n=60); keep me on a short leash in calm-up (-130). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+461 bps, n=300); keep me on a short leash in calm-up (-89). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (+363 bps, n=12); keep me on a short leash in calm-up (-226). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
