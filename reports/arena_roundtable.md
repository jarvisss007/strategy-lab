# Arena Roundtable — 2026-10-13

Tape: **calm-up** · session 2026-10-12 · 12 agents · opened 95, closed 52 this session · 248 open · 2922 forward closes all-time

> **This lab is 68% of the desk's scored record (2922 of 4303 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 73 of 248 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 52 closed this session, 2922 all-time. Oldest due row: TREND_RIDER MPWR, entered 2026-09-22, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+230), PANIC_LITE (-5), PULLBACK_50 (-11); cold hands: DEEP_DIP (-66), TREND_RIDER (-282). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 43% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 83% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +22 bps over 1668 trades (t=1.62) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +230 (n=425, d=109) · PANIC_LITE -5 (n=1942, d=146) · PULLBACK_50 -11 (n=204, d=44) · PANIC_BOUNCE -15 (n=929, d=124) · SHORT_EXT -18 (n=185, d=73) · BOLL_SNAP -27 (n=398, d=119) · REVERSAL_3 -40 (n=237, d=44) · DOUBLE_DIP -53 (n=776, d=126) · RSI2_DIP -59 (n=477, d=47) · DEEP_DIP -66 (n=113, d=68) · TREND_RIDER -282 (n=110, d=37)
- **calm-down**: BOLL_SNAP +179 (n=65, d=13) · DOUBLE_DIP +93 (n=122, d=15) · REVERSAL_3 +49 (n=26, d=3) · RSI2_DIP +47 (n=59, d=4) · PANIC_BOUNCE +11 (n=119, d=14) · PANIC_LITE -12 (n=208, d=15) · FRESH_HIGH -144 (n=36, d=12)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +1084 (n=24, d=13) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -217 (n=33, d=20)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **54** entry days — **test LIVE (>=15)**
- PANIC_LITE: **51** entry days — **test LIVE (>=15)**
- REVERSAL_3: **49** entry days — **test LIVE (>=15)**
- PULLBACK_50: **49** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **46** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **44** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **44** entry days — **test LIVE (>=15)**
- TREND_RIDER: **32** entry days — **test LIVE (>=15)**
- DEEP_DIP: **28** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **25** entry days — **test LIVE (>=15)**
- SHORT_EXT: **14** entry days
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean +232 bps over 28 entry days (row mean +582, n=57) · win rate per entry day 46% (row hit 63%)
- PANIC_BOUNCE: per-entry-day mean +35 bps over 46 entry days (row mean +26, n=350) · win rate per entry day 52% (row hit 51%)
- PANIC_LITE: per-entry-day mean -8 bps over 51 entry days (row mean -20, n=710) · win rate per entry day 45% (row hit 45%)
- DOUBLE_DIP: per-entry-day mean -5 bps over 44 entry days (row mean +66, n=272) · win rate per entry day 46% (row hit 51%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -158 bps over 25 entry days (row mean -91, n=56) · win rate per entry day 44% (row hit 41%)
- SHORT_EXT: per-entry-day mean -5 bps over 14 entry days (row mean +108, n=29) · win rate per entry day 43% (row hit 48%)
- TREND_RIDER: per-entry-day mean -10 bps over 32 entry days (row mean -40, n=90) · win rate per entry day 50% (row hit 48%)
- RSI2_DIP: per-entry-day mean +10 bps over 54 entry days (row mean -6, n=570) · win rate per entry day 44% (row hit 45%)
- REVERSAL_3: per-entry-day mean +6 bps over 49 entry days (row mean +7, n=328) · win rate per entry day 41% (row hit 47%)
- BOLL_SNAP: per-entry-day mean +35 bps over 44 entry days (row mean +223, n=204) · win rate per entry day 54% (row hit 57%)
- PULLBACK_50: per-entry-day mean +26 bps over 49 entry days (row mean +61, n=216) · win rate per entry day 61% (row hit 54%)
- Exits on copied/zero-volume bars: **0** of 2805 forward exits tested; 117 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+1084 bps, n=24); keep me on a short leash in calm-up (-66). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-15). Status: WATCH — positive but not significant.
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-down (-12). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-53). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+677 bps, n=14); keep me on a short leash in storm-down (-217). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+611 bps, n=10); keep me on a short leash in calm-down (-323). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-up (-282 bps, n=110); keep me on a short leash in calm-up (-282). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (+47 bps, n=59); keep me on a short leash in calm-up (-59). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+49 bps, n=26); keep me on a short leash in calm-up (-40). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-up (-11 bps, n=204); keep me on a short leash in calm-down (-14). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
