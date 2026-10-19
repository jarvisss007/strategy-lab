# Arena Roundtable — 2026-10-19

Tape: **calm-up** · session 2026-10-16 · 12 agents · opened 132, closed 145 this session · 301 open · 3262 forward closes all-time

> **This lab is 69% of the desk's scored record (3262 of 4723 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 71 of 301 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 145 closed this session, 3262 all-time. Oldest due row: TREND_RIDER KLAC, entered 2026-09-28, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+195), SHORT_EXT (+2), PANIC_LITE (-26); cold hands: DEEP_DIP (-200), TREND_RIDER (-290). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 43% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +10 bps over 1796 trades (t=0.76) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +195 (n=425, d=109) · SHORT_EXT +2 (n=184, d=74) · PANIC_LITE -26 (n=2056, d=144) · PANIC_BOUNCE -46 (n=975, d=124) · BOLL_SNAP -58 (n=468, d=122) · DOUBLE_DIP -79 (n=836, d=125) · REVERSAL_3 -102 (n=250, d=41) · RSI2_DIP -104 (n=488, d=45) · PULLBACK_50 -120 (n=208, d=43) · DEEP_DIP -200 (n=132, d=78) · TREND_RIDER -290 (n=105, d=37)
- **calm-down**: BOLL_SNAP +195 (n=85, d=14) · DOUBLE_DIP +102 (n=128, d=16) · REVERSAL_3 +88 (n=36, d=4) · PULLBACK_50 +51 (n=25, d=5) · RSI2_DIP +45 (n=60, d=4) · PANIC_BOUNCE +35 (n=141, d=15) · PANIC_LITE +7 (n=249, d=16) · FRESH_HIGH -276 (n=36, d=13)
- **storm-up**: PANIC_LITE +162 (n=98, d=4) · PANIC_BOUNCE +123 (n=69, d=4) · DOUBLE_DIP +110 (n=54, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +1022 (n=25, d=15) · DOUBLE_DIP +386 (n=265, d=30) · BOLL_SNAP +376 (n=257, d=27) · STORM_DIP +341 (n=429, d=31) · PANIC_BOUNCE +189 (n=268, d=29) · PANIC_LITE +134 (n=590, d=34) · FRESH_HIGH -98 (n=44, d=21)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **57** entry days — **test LIVE (>=15)**
- PANIC_LITE: **55** entry days — **test LIVE (>=15)**
- REVERSAL_3: **53** entry days — **test LIVE (>=15)**
- PULLBACK_50: **53** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **50** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **48** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **48** entry days — **test LIVE (>=15)**
- TREND_RIDER: **36** entry days — **test LIVE (>=15)**
- DEEP_DIP: **30** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **28** entry days — **test LIVE (>=15)**
- SHORT_EXT: **18** entry days — **test LIVE (>=15)**
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean +81 bps over 30 entry days (row mean +493, n=59) · win rate per entry day 43% (row hit 61%)
- PANIC_BOUNCE: per-entry-day mean +3 bps over 50 entry days (row mean -62, n=411) · win rate per entry day 50% (row hit 46%)
- PANIC_LITE: per-entry-day mean -43 bps over 55 entry days (row mean -82, n=790) · win rate per entry day 42% (row hit 42%)
- DOUBLE_DIP: per-entry-day mean -80 bps over 48 entry days (row mean -47, n=317) · win rate per entry day 42% (row hit 44%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -163 bps over 28 entry days (row mean -100, n=61) · win rate per entry day 39% (row hit 39%)
- SHORT_EXT: per-entry-day mean +149 bps over 18 entry days (row mean +179, n=33) · win rate per entry day 56% (row hit 54%)
- TREND_RIDER: per-entry-day mean +10 bps over 36 entry days (row mean -25, n=99) · win rate per entry day 50% (row hit 50%)
- RSI2_DIP: per-entry-day mean -35 bps over 57 entry days (row mean -60, n=620) · win rate per entry day 42% (row hit 43%)
- REVERSAL_3: per-entry-day mean -37 bps over 53 entry days (row mean -57, n=368) · win rate per entry day 38% (row hit 43%)
- BOLL_SNAP: per-entry-day mean -15 bps over 48 entry days (row mean +136, n=231) · win rate per entry day 50% (row hit 53%)
- PULLBACK_50: per-entry-day mean -12 bps over 53 entry days (row mean +23, n=233) · win rate per entry day 57% (row hit 52%)
- Exits on copied/zero-volume bars: **0** of 3186 forward exits tested; 76 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+1022 bps, n=25); keep me on a short leash in calm-up (-200). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=268); keep me on a short leash in calm-up (-46). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-up (+162 bps, n=98); keep me on a short leash in calm-up (-26). Status: WATCH — positive but not significant.
- DOUBLE_DIP to the desk: my weather is storm-down (+386 bps, n=265); keep me on a short leash in calm-up (-79). Status: WATCH — positive but not significant.
- STORM_DIP to the desk: my weather is storm-down (+341 bps, n=429); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+654 bps, n=14); keep me on a short leash in calm-down (-276). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+611 bps, n=10); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-up (-290 bps, n=105); keep me on a short leash in calm-up (-290). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (+45 bps, n=60); keep me on a short leash in calm-up (-104). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+88 bps, n=36); keep me on a short leash in calm-up (-102). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+376 bps, n=257); keep me on a short leash in storm-up (-72). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+51 bps, n=25); keep me on a short leash in calm-up (-120). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
