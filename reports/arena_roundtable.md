# Arena Roundtable — 2026-09-28

Tape: **calm-up** · session 2026-09-25 · 12 agents · opened 23, closed 49 this session · 164 open · 2442 forward closes all-time

> **This lab is 70% of the desk's scored record (2442 of 3513 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 48 of 164 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 49 closed this session, 2442 all-time. Oldest due row: TREND_RIDER NBIS, entered 2026-09-04, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+204), DEEP_DIP (+46), PULLBACK_50 (+12); cold hands: RSI2_DIP (-51), TREND_RIDER (-272). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +36 bps over 1631 trades (t=2.54) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +204 (n=435, d=110) · DEEP_DIP +46 (n=115, d=72) · PULLBACK_50 +12 (n=170, d=36) · PANIC_LITE -7 (n=1899, d=144) · REVERSAL_3 -11 (n=204, d=37) · PANIC_BOUNCE -23 (n=933, d=125) · BOLL_SNAP -25 (n=375, d=117) · SHORT_EXT -34 (n=186, d=72) · DOUBLE_DIP -39 (n=779, d=126) · RSI2_DIP -51 (n=395, d=39) · TREND_RIDER -272 (n=91, d=30)
- **calm-down**: TREND_RIDER +342 (n=25, d=10) · BOLL_SNAP +310 (n=69, d=13) · PULLBACK_50 +138 (n=47, d=10) · PANIC_BOUNCE +126 (n=134, d=14) · DOUBLE_DIP +108 (n=123, d=15) · REVERSAL_3 +101 (n=87, d=8) · PANIC_LITE +95 (n=240, d=15) · RSI2_DIP -118 (n=174, d=10) · FRESH_HIGH -247 (n=32, d=11)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +753 (n=28, d=15) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -148 (n=36, d=19)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **42** entry days — **test LIVE (>=15)**
- PANIC_LITE: **40** entry days — **test LIVE (>=15)**
- REVERSAL_3: **40** entry days — **test LIVE (>=15)**
- PULLBACK_50: **39** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **37** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **35** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **34** entry days — **test LIVE (>=15)**
- TREND_RIDER: **23** entry days — **test LIVE (>=15)**
- DEEP_DIP: **21** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **18** entry days — **test LIVE (>=15)**
- SHORT_EXT: **9** entry days
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean +471 bps over 21 entry days (row mean +774, n=45) · win rate per entry day 57% (row hit 69%)
- PANIC_BOUNCE: per-entry-day mean +115 bps over 37 entry days (row mean +59, n=312) · win rate per entry day 60% (row hit 53%)
- PANIC_LITE: per-entry-day mean +36 bps over 40 entry days (row mean +12, n=590) · win rate per entry day 50% (row hit 47%)
- DOUBLE_DIP: per-entry-day mean +76 bps over 35 entry days (row mean +92, n=244) · win rate per entry day 49% (row hit 52%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -181 bps over 18 entry days (row mean -119, n=46) · win rate per entry day 44% (row hit 39%)
- SHORT_EXT: per-entry-day mean +156 bps over 9 entry days (row mean +326, n=20) · win rate per entry day 56% (row hit 60%)
- TREND_RIDER: per-entry-day mean -120 bps over 23 entry days (row mean -158, n=62) · win rate per entry day 39% (row hit 44%)
- RSI2_DIP: per-entry-day mean +22 bps over 42 entry days (row mean -6, n=453) · win rate per entry day 43% (row hit 44%)
- REVERSAL_3: per-entry-day mean +34 bps over 40 entry days (row mean +17, n=284) · win rate per entry day 45% (row hit 48%)
- BOLL_SNAP: per-entry-day mean +45 bps over 34 entry days (row mean +284, n=161) · win rate per entry day 56% (row hit 60%)
- PULLBACK_50: per-entry-day mean +51 bps over 39 entry days (row mean +65, n=185) · win rate per entry day 59% (row hit 51%)
- Exits on copied/zero-volume bars: **0** of 2394 forward exits tested; 48 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is calm-down (+898 bps, n=12); keep me on a short leash in calm-up (+46). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-23). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (-7). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-39). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-247). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+611 bps, n=10); keep me on a short leash in calm-up (-34). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+342 bps, n=25); keep me on a short leash in calm-up (-272). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-118). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+101 bps, n=87); keep me on a short leash in calm-up (-11). Status: WATCH — positive but not significant.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+138 bps, n=47); keep me on a short leash in calm-up (+12). Status: WATCH — positive but not significant.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
