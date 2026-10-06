# Arena Roundtable — 2026-10-06

Tape: **calm-up** · session 2026-10-05 · 12 agents · opened 29, closed 30 this session · 115 open · 2724 forward closes all-time

> **This lab is 69% of the desk's scored record (2724 of 3967 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 115 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 30 closed this session, 2724 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+236), PULLBACK_50 (+35), DEEP_DIP (+29); cold hands: RSI2_DIP (-32), TREND_RIDER (-173). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 42% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +43 bps over 1629 trades (t=3.06) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +236 (n=416, d=108) · PULLBACK_50 +35 (n=175, d=38) · DEEP_DIP +29 (n=109, d=72) · PANIC_LITE +7 (n=1861, d=143) · SHORT_EXT +2 (n=183, d=70) · PANIC_BOUNCE -4 (n=900, d=122) · BOLL_SNAP -8 (n=376, d=117) · REVERSAL_3 -11 (n=208, d=38) · DOUBLE_DIP -21 (n=743, d=123) · RSI2_DIP -32 (n=412, d=41) · TREND_RIDER -173 (n=94, d=33)
- **calm-down**: TREND_RIDER +469 (n=20, d=8) · BOLL_SNAP +336 (n=81, d=14) · DOUBLE_DIP +204 (n=132, d=16) · PANIC_BOUNCE +178 (n=142, d=15) · PULLBACK_50 +139 (n=39, d=8) · PANIC_LITE +132 (n=256, d=16) · REVERSAL_3 -42 (n=61, d=6) · FRESH_HIGH -163 (n=34, d=13) · RSI2_DIP -262 (n=130, d=8)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +868 (n=27, d=15) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -190 (n=34, d=19)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **48** entry days — **test LIVE (>=15)**
- PANIC_LITE: **46** entry days — **test LIVE (>=15)**
- REVERSAL_3: **45** entry days — **test LIVE (>=15)**
- PULLBACK_50: **44** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **41** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **41** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **39** entry days — **test LIVE (>=15)**
- TREND_RIDER: **28** entry days — **test LIVE (>=15)**
- DEEP_DIP: **24** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **22** entry days — **test LIVE (>=15)**
- SHORT_EXT: **11** entry days
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean +394 bps over 24 entry days (row mean +720, n=51) · win rate per entry day 54% (row hit 69%)
- PANIC_BOUNCE: per-entry-day mean +96 bps over 41 entry days (row mean +57, n=329) · win rate per entry day 58% (row hit 53%)
- PANIC_LITE: per-entry-day mean +25 bps over 46 entry days (row mean +7, n=649) · win rate per entry day 50% (row hit 47%)
- DOUBLE_DIP: per-entry-day mean +41 bps over 41 entry days (row mean +84, n=266) · win rate per entry day 49% (row hit 52%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -163 bps over 22 entry days (row mean -89, n=53) · win rate per entry day 46% (row hit 42%)
- SHORT_EXT: per-entry-day mean +76 bps over 11 entry days (row mean +223, n=24) · win rate per entry day 46% (row hit 54%)
- TREND_RIDER: per-entry-day mean -67 bps over 28 entry days (row mean -77, n=81) · win rate per entry day 46% (row hit 48%)
- RSI2_DIP: per-entry-day mean +26 bps over 48 entry days (row mean +3, n=531) · win rate per entry day 48% (row hit 46%)
- REVERSAL_3: per-entry-day mean +23 bps over 45 entry days (row mean +18, n=310) · win rate per entry day 44% (row hit 48%)
- BOLL_SNAP: per-entry-day mean +40 bps over 39 entry days (row mean +244, n=189) · win rate per entry day 56% (row hit 58%)
- PULLBACK_50: per-entry-day mean +66 bps over 44 entry days (row mean +72, n=201) · win rate per entry day 61% (row hit 54%)
- Exits on copied/zero-volume bars: **0** of 2640 forward exits tested; 84 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+868 bps, n=27); keep me on a short leash in calm-up (+29). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-4). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (+7). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-21). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in storm-down (-190). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+441 bps, n=11); keep me on a short leash in calm-down (-363). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+469 bps, n=20); keep me on a short leash in calm-up (-173). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-up (-32 bps, n=412); keep me on a short leash in calm-down (-262). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-up (-11 bps, n=208); keep me on a short leash in calm-down (-42). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+139 bps, n=39); keep me on a short leash in calm-up (+35). Status: WATCH — positive but not significant.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
