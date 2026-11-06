# Arena Roundtable — 2026-11-06

Tape: **storm-down** · session 2026-11-06 · 12 agents · opened 52, closed 93 this session · 266 open · 4234 forward closes all-time

> **This lab is 70% of the desk's scored record (4141 of 5900 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 266 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 93 closed this session, 4234 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+699), BOLL_SNAP (+372), DOUBLE_DIP (+263); cold hands: FRESH_HIGH (-108), RSI2_DIP (-255). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -15 bps over 1831 trades (t=-1.09) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +64 (n=387, d=104) · SHORT_EXT +10 (n=171, d=62) · PANIC_LITE -53 (n=1974, d=136) · PANIC_BOUNCE -68 (n=951, d=118) · DOUBLE_DIP -88 (n=798, d=120) · BOLL_SNAP -90 (n=437, d=114) · REVERSAL_3 -124 (n=179, d=32) · DEEP_DIP -142 (n=119, d=68) · RSI2_DIP -153 (n=356, d=36) · PULLBACK_50 -188 (n=143, d=33) · TREND_RIDER -336 (n=92, d=32)
- **calm-down**: BOLL_SNAP +217 (n=121, d=20) · DOUBLE_DIP +44 (n=210, d=22) · REVERSAL_3 -28 (n=56, d=9) · PANIC_LITE -61 (n=432, d=22) · RSI2_DIP -64 (n=109, d=10) · PULLBACK_50 -84 (n=38, d=10) · PANIC_BOUNCE -90 (n=258, d=20) · DEEP_DIP -174 (n=29, d=17) · FRESH_HIGH -204 (n=45, d=15)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +699 (n=41, d=17) · BOLL_SNAP +372 (n=298, d=29) · DOUBLE_DIP +263 (n=330, d=32) · PANIC_BOUNCE +227 (n=308, d=31) · STORM_DIP +216 (n=495, d=33) · PANIC_LITE +136 (n=627, d=36) · FRESH_HIGH -108 (n=40, d=21) · RSI2_DIP -255 (n=23, d=3)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **72** entry days — **test LIVE (>=15)**
- PANIC_LITE: **70** entry days — **test LIVE (>=15)**
- PULLBACK_50: **65** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **64** entry days — **test LIVE (>=15)**
- REVERSAL_3: **64** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **62** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **61** entry days — **test LIVE (>=15)**
- TREND_RIDER: **48** entry days — **test LIVE (>=15)**
- DEEP_DIP: **43** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **36** entry days — **test LIVE (>=15)**
- SHORT_EXT: **19** entry days — **test LIVE (>=15)**
- STORM_DIP: **2** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -299 bps over 43 entry days (row mean +92, n=80) · win rate per entry day 33% (row hit 48%)
- PANIC_BOUNCE: per-entry-day mean -42 bps over 64 entry days (row mean -100, n=585) · win rate per entry day 47% (row hit 44%)
- PANIC_LITE: per-entry-day mean -101 bps over 70 entry days (row mean -124, n=1011) · win rate per entry day 39% (row hit 41%)
- DOUBLE_DIP: per-entry-day mean -106 bps over 61 entry days (row mean -66, n=442) · win rate per entry day 38% (row hit 41%)
- STORM_DIP: per-entry-day mean +386 bps over 2 entry days (row mean +386, n=80) · win rate per entry day 50% (row hit 54%)
- FRESH_HIGH: per-entry-day mean -163 bps over 36 entry days (row mean -135, n=79) · win rate per entry day 39% (row hit 42%)
- SHORT_EXT: per-entry-day mean +188 bps over 19 entry days (row mean +199, n=34) · win rate per entry day 58% (row hit 56%)
- TREND_RIDER: per-entry-day mean -150 bps over 48 entry days (row mean -186, n=127) · win rate per entry day 46% (row hit 46%)
- RSI2_DIP: per-entry-day mean -70 bps over 72 entry days (row mean -82, n=741) · win rate per entry day 36% (row hit 42%)
- REVERSAL_3: per-entry-day mean -62 bps over 64 entry days (row mean -60, n=432) · win rate per entry day 36% (row hit 43%)
- BOLL_SNAP: per-entry-day mean -54 bps over 62 entry days (row mean +38, n=337) · win rate per entry day 44% (row hit 48%)
- PULLBACK_50: per-entry-day mean -83 bps over 65 entry days (row mean -73, n=286) · win rate per entry day 49% (row hit 47%)
- Exits on copied/zero-volume bars: **0** of 3743 forward exits tested; 491 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+699 bps, n=41); keep me on a short leash in calm-down (-174). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+227 bps, n=308); keep me on a short leash in calm-down (-90). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+162 bps, n=98); keep me on a short leash in calm-down (-61). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+263 bps, n=330); keep me on a short leash in calm-up (-88). Status: DEAD — loses to costs/SPY.
- STORM_DIP to the desk: my weather is storm-down (+216 bps, n=495); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+1120 bps, n=12); keep me on a short leash in calm-down (-204). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is calm-up (+10 bps, n=171); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (-220 bps, n=19); keep me on a short leash in calm-up (-336). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (-64 bps, n=109); keep me on a short leash in storm-down (-255). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (-28 bps, n=56); keep me on a short leash in storm-down (-198). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+372 bps, n=298); keep me on a short leash in calm-up (-90). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (+261 bps, n=8); keep me on a short leash in calm-up (-188). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
