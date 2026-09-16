# Arena Roundtable — 2026-09-16

Tape: **calm-down** · session 2026-09-16 · 12 agents · opened 63, closed 96 this session · 211 open · 2118 forward closes all-time

> **This lab is 71% of the desk's scored record (2022 of 2832 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 211 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 96 closed this session, 2118 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-DOWN. Our pooled record in this weather — hot hands: TREND_RIDER (+364), BOLL_SNAP (+294), PANIC_BOUNCE (+123); cold hands: FRESH_HIGH (-183), RSI2_DIP (-284). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 44% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +38 bps over 1604 trades (t=2.64) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +202 (n=444, d=115) · SHORT_EXT -0 (n=197, d=69) · PANIC_LITE -2 (n=1882, d=145) · REVERSAL_3 -7 (n=223, d=39) · PANIC_BOUNCE -17 (n=938, d=125) · BOLL_SNAP -30 (n=361, d=117) · PULLBACK_50 -30 (n=195, d=38) · DOUBLE_DIP -32 (n=774, d=127) · RSI2_DIP -44 (n=456, d=40) · DEEP_DIP -46 (n=112, d=68) · TREND_RIDER -514 (n=93, d=32)
- **calm-down**: TREND_RIDER +364 (n=22, d=9) · BOLL_SNAP +294 (n=59, d=12) · PANIC_BOUNCE +123 (n=133, d=13) · PANIC_LITE +99 (n=234, d=14) · PULLBACK_50 +84 (n=35, d=9) · REVERSAL_3 +80 (n=78, d=7) · DOUBLE_DIP +28 (n=118, d=14) · FRESH_HIGH -183 (n=32, d=11) · RSI2_DIP -284 (n=131, d=9)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +867 (n=27, d=15) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -95 (n=33, d=17)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **35** entry days — **test LIVE (>=15)**
- PANIC_LITE: **33** entry days — **test LIVE (>=15)**
- REVERSAL_3: **33** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **32** entry days — **test LIVE (>=15)**
- PULLBACK_50: **32** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **30** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **28** entry days — **test LIVE (>=15)**
- DEEP_DIP: **18** entry days — **test LIVE (>=15)**
- TREND_RIDER: **18** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **15** entry days — **test LIVE (>=15)**
- SHORT_EXT: **7** entry days
- STORM_DIP: **1** entry days

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+867 bps, n=27); keep me on a short leash in calm-up (-46). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-17). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (-2). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-32). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-183). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+513 bps, n=12); keep me on a short leash in storm-up (-526). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+364 bps, n=22); keep me on a short leash in calm-up (-514). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-284). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+80 bps, n=78); keep me on a short leash in calm-up (-7). Status: WATCH — positive but not significant.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+84 bps, n=35); keep me on a short leash in calm-up (-30). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
