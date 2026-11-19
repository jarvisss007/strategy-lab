# Arena Roundtable — 2026-11-19

Tape: **storm-down** · session 2026-11-19 · 12 agents · opened 95, closed 82 this session · 261 open · 4828 forward closes all-time

> **This lab is 72% of the desk's scored record (4746 of 6613 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 261 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 82 closed this session, 4828 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+727), BOLL_SNAP (+421), PANIC_BOUNCE (+327); cold hands: RSI2_DIP (-88), REVERSAL_3 (-96). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 44% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -21 bps over 1836 trades (t=-1.57) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +73 (n=314, d=95) · SHORT_EXT +19 (n=160, d=59) · BOLL_SNAP -48 (n=371, d=106) · PANIC_LITE -57 (n=1761, d=127) · PANIC_BOUNCE -75 (n=820, d=108) · DOUBLE_DIP -79 (n=692, d=111) · DEEP_DIP -180 (n=114, d=61) · RSI2_DIP -208 (n=222, d=28) · PULLBACK_50 -241 (n=97, d=23) · REVERSAL_3 -276 (n=101, d=24) · TREND_RIDER -397 (n=71, d=25)
- **calm-down**: BOLL_SNAP +218 (n=124, d=23) · REVERSAL_3 +6 (n=71, d=12) · RSI2_DIP -93 (n=152, d=15) · DOUBLE_DIP -112 (n=241, d=26) · PANIC_LITE -114 (n=505, d=27) · TREND_RIDER -144 (n=29, d=12) · PANIC_BOUNCE -149 (n=284, d=24) · PULLBACK_50 -161 (n=46, d=13) · FRESH_HIGH -253 (n=54, d=17) · DEEP_DIP -274 (n=32, d=19)
- **storm-up**: FRESH_HIGH +598 (n=23, d=3) · PANIC_LITE +167 (n=99, d=4) · PANIC_BOUNCE +126 (n=69, d=4) · DOUBLE_DIP +106 (n=52, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -305 (n=88, d=4)
- **storm-down**: DEEP_DIP +727 (n=46, d=20) · BOLL_SNAP +421 (n=344, d=33) · PANIC_BOUNCE +327 (n=359, d=34) · DOUBLE_DIP +308 (n=390, d=35) · STORM_DIP +183 (n=558, d=37) · PANIC_LITE +182 (n=722, d=40) · FRESH_HIGH -61 (n=59, d=23) · PULLBACK_50 -85 (n=32, d=7) · RSI2_DIP -88 (n=74, d=7) · REVERSAL_3 -96 (n=37, d=7)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **81** entry days — **test LIVE (>=15)**
- PANIC_LITE: **79** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **73** entry days — **test LIVE (>=15)**
- REVERSAL_3: **71** entry days — **test LIVE (>=15)**
- PULLBACK_50: **71** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **70** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **70** entry days — **test LIVE (>=15)**
- TREND_RIDER: **56** entry days — **test LIVE (>=15)**
- DEEP_DIP: **49** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **41** entry days — **test LIVE (>=15)**
- SHORT_EXT: **20** entry days — **test LIVE (>=15)**
- STORM_DIP: **4** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -328 bps over 49 entry days (row mean -33, n=96) · win rate per entry day 33% (row hit 44%)
- PANIC_BOUNCE: per-entry-day mean -62 bps over 73 entry days (row mean -136, n=669) · win rate per entry day 45% (row hit 42%)
- PANIC_LITE: per-entry-day mean -112 bps over 79 entry days (row mean -139, n=1138) · win rate per entry day 38% (row hit 39%)
- DOUBLE_DIP: per-entry-day mean -144 bps over 70 entry days (row mean -68, n=529) · win rate per entry day 37% (row hit 42%)
- STORM_DIP: per-entry-day mean +301 bps over 4 entry days (row mean +306, n=159) · win rate per entry day 50% (row hit 53%)
- FRESH_HIGH: per-entry-day mean -180 bps over 41 entry days (row mean -156, n=93) · win rate per entry day 39% (row hit 43%)
- SHORT_EXT: per-entry-day mean +161 bps over 20 entry days (row mean +169, n=36) · win rate per entry day 55% (row hit 53%)
- TREND_RIDER: per-entry-day mean -273 bps over 56 entry days (row mean -275, n=146) · win rate per entry day 41% (row hit 42%)
- RSI2_DIP: per-entry-day mean -58 bps over 81 entry days (row mean -71, n=812) · win rate per entry day 38% (row hit 43%)
- REVERSAL_3: per-entry-day mean -35 bps over 71 entry days (row mean -51, n=454) · win rate per entry day 39% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -67 bps over 70 entry days (row mean +96, n=391) · win rate per entry day 44% (row hit 51%)
- PULLBACK_50: per-entry-day mean -67 bps over 71 entry days (row mean -57, n=305) · win rate per entry day 52% (row hit 48%)
- Exits on copied/zero-volume bars: **0** of 4492 forward exits tested; 336 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+727 bps, n=46); keep me on a short leash in calm-down (-274). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+327 bps, n=359); keep me on a short leash in calm-down (-149). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-down (+182 bps, n=722); keep me on a short leash in calm-down (-114). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+308 bps, n=390); keep me on a short leash in calm-down (-112). Status: WATCH — positive but not significant.
- STORM_DIP to the desk: my weather is storm-down (+183 bps, n=558); keep me on a short leash in storm-up (-305). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+598 bps, n=23); keep me on a short leash in calm-down (-253). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+424 bps, n=9); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (-144 bps, n=29); keep me on a short leash in calm-up (-397). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (-88 bps, n=74); keep me on a short leash in calm-up (-208). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+6 bps, n=71); keep me on a short leash in calm-up (-276). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+421 bps, n=344); keep me on a short leash in storm-up (-72). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (-85 bps, n=32); keep me on a short leash in calm-up (-241). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
