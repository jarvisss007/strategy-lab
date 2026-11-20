# Arena Roundtable — 2026-11-20

Tape: **storm-down** · session 2026-11-19 · 12 agents · opened 96, closed 83 this session · 261 open · 4829 forward closes all-time

> **This lab is 72% of the desk's scored record (4829 of 6696 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 83 of 261 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 83 closed this session, 4829 all-time. Oldest due row: TREND_RIDER MRK, entered 2026-10-30, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+722), BOLL_SNAP (+409), PANIC_BOUNCE (+315); cold hands: PULLBACK_50 (-83), FRESH_HIGH (-89). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 44% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 82% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -28 bps over 1879 trades (t=-2.08) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +95 (n=317, d=95) · SHORT_EXT +2 (n=167, d=59) · BOLL_SNAP -46 (n=372, d=105) · PANIC_LITE -55 (n=1785, d=127) · PANIC_BOUNCE -72 (n=836, d=109) · DOUBLE_DIP -78 (n=704, d=111) · DEEP_DIP -167 (n=116, d=62) · RSI2_DIP -217 (n=225, d=27) · PULLBACK_50 -236 (n=99, d=24) · REVERSAL_3 -281 (n=104, d=23) · TREND_RIDER -397 (n=71, d=25)
- **calm-down**: BOLL_SNAP +224 (n=125, d=23) · REVERSAL_3 +7 (n=72, d=12) · RSI2_DIP -85 (n=155, d=15) · DOUBLE_DIP -111 (n=246, d=26) · PANIC_LITE -124 (n=512, d=27) · PANIC_BOUNCE -160 (n=290, d=24) · PULLBACK_50 -175 (n=46, d=13) · TREND_RIDER -207 (n=29, d=12) · FRESH_HIGH -241 (n=54, d=17) · DEEP_DIP -328 (n=33, d=20)
- **storm-up**: FRESH_HIGH +678 (n=24, d=3) · PANIC_LITE +167 (n=99, d=4) · PANIC_BOUNCE +132 (n=70, d=4) · DOUBLE_DIP +114 (n=53, d=4) · BOLL_SNAP -72 (n=23, d=4) · STORM_DIP -296 (n=89, d=4)
- **storm-down**: DEEP_DIP +722 (n=46, d=20) · BOLL_SNAP +409 (n=355, d=34) · PANIC_BOUNCE +315 (n=377, d=35) · DOUBLE_DIP +276 (n=409, d=37) · STORM_DIP +178 (n=576, d=38) · PANIC_LITE +160 (n=766, d=41) · REVERSAL_3 -57 (n=48, d=8) · RSI2_DIP -72 (n=78, d=8) · PULLBACK_50 -83 (n=35, d=8) · FRESH_HIGH -89 (n=60, d=23)

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
- STORM_DIP: per-entry-day mean +248 bps over 4 entry days (row mean +248, n=160) · win rate per entry day 50% (row hit 52%)
- FRESH_HIGH: per-entry-day mean -180 bps over 41 entry days (row mean -156, n=93) · win rate per entry day 39% (row hit 43%)
- SHORT_EXT: per-entry-day mean +161 bps over 20 entry days (row mean +169, n=36) · win rate per entry day 55% (row hit 53%)
- TREND_RIDER: per-entry-day mean -273 bps over 56 entry days (row mean -275, n=146) · win rate per entry day 41% (row hit 42%)
- RSI2_DIP: per-entry-day mean -58 bps over 81 entry days (row mean -71, n=812) · win rate per entry day 38% (row hit 43%)
- REVERSAL_3: per-entry-day mean -35 bps over 71 entry days (row mean -51, n=454) · win rate per entry day 39% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -67 bps over 70 entry days (row mean +96, n=391) · win rate per entry day 44% (row hit 51%)
- PULLBACK_50: per-entry-day mean -67 bps over 71 entry days (row mean -57, n=305) · win rate per entry day 52% (row hit 48%)
- Exits on copied/zero-volume bars: **0** of 4492 forward exits tested; 337 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+722 bps, n=46); keep me on a short leash in calm-down (-328). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+315 bps, n=377); keep me on a short leash in calm-down (-160). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-up (+167 bps, n=99); keep me on a short leash in calm-down (-124). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+276 bps, n=409); keep me on a short leash in calm-down (-111). Status: WATCH — positive but not significant.
- STORM_DIP to the desk: my weather is storm-down (+178 bps, n=576); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+678 bps, n=24); keep me on a short leash in calm-down (-241). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+349 bps, n=10); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (-207 bps, n=29); keep me on a short leash in calm-up (-397). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (-72 bps, n=78); keep me on a short leash in calm-up (-217). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+7 bps, n=72); keep me on a short leash in calm-up (-281). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+409 bps, n=355); keep me on a short leash in storm-up (-72). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (-83 bps, n=35); keep me on a short leash in calm-up (-236). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
