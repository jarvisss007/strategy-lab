# Arena Roundtable — 2026-09-16

Tape: **calm-up** · session 2026-09-15 · 12 agents · opened 59, closed 43 this session · 244 open · 2022 forward closes all-time

> **This lab is 71% of the desk's scored record (2022 of 2832 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 96 of 244 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 43 closed this session, 2022 all-time. Oldest due row: DEEP_DIP BABA, entered 2026-09-01, hold 10, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+202), PANIC_LITE (+0), PANIC_BOUNCE (-14); cold hands: RSI2_DIP (-55), TREND_RIDER (-532). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +40 bps over 1605 trades (t=2.8) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +202 (n=446, d=116) · PANIC_LITE +0 (n=1883, d=146) · PANIC_BOUNCE -14 (n=938, d=125) · PULLBACK_50 -15 (n=195, d=39) · SHORT_EXT -23 (n=196, d=69) · BOLL_SNAP -26 (n=361, d=117) · DOUBLE_DIP -32 (n=774, d=127) · DEEP_DIP -40 (n=112, d=68) · REVERSAL_3 -52 (n=223, d=40) · RSI2_DIP -55 (n=462, d=41) · TREND_RIDER -532 (n=96, d=32)
- **calm-down**: TREND_RIDER +369 (n=22, d=9) · BOLL_SNAP +310 (n=59, d=12) · PANIC_BOUNCE +125 (n=133, d=13) · PANIC_LITE +106 (n=234, d=14) · PULLBACK_50 +106 (n=35, d=9) · REVERSAL_3 +80 (n=78, d=7) · DOUBLE_DIP +37 (n=118, d=14) · FRESH_HIGH -177 (n=32, d=11) · RSI2_DIP -271 (n=130, d=9)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +867 (n=27, d=15) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -95 (n=33, d=17)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **34** entry days — **test LIVE (>=15)**
- PANIC_LITE: **32** entry days — **test LIVE (>=15)**
- REVERSAL_3: **32** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **31** entry days — **test LIVE (>=15)**
- PULLBACK_50: **31** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **29** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **27** entry days — **test LIVE (>=15)**
- TREND_RIDER: **18** entry days — **test LIVE (>=15)**
- DEEP_DIP: **17** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **15** entry days — **test LIVE (>=15)**
- SHORT_EXT: **7** entry days
- STORM_DIP: **1** entry days

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+867 bps, n=27); keep me on a short leash in calm-up (-40). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-14). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (+0). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-32). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-177). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+513 bps, n=12); keep me on a short leash in storm-up (-526). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+369 bps, n=22); keep me on a short leash in calm-up (-532). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-271). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+80 bps, n=78); keep me on a short leash in calm-up (-52). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+106 bps, n=35); keep me on a short leash in calm-up (-15). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
