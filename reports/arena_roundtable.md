# Arena Roundtable — 2026-09-14

Tape: **calm-up** · session 2026-09-14 · 12 agents · opened 104, closed 62 this session · 228 open · 1979 forward closes all-time

> **This lab is 72% of the desk's scored record (1917 of 2664 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 228 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 62 closed this session, 1979 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+195), PANIC_LITE (+2), PULLBACK_50 (-17); cold hands: RSI2_DIP (-78), TREND_RIDER (-585). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +42 bps over 1583 trades (t=2.89) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +195 (n=449, d=116) · PANIC_LITE +2 (n=1861, d=146) · PULLBACK_50 -17 (n=199, d=39) · PANIC_BOUNCE -18 (n=917, d=125) · BOLL_SNAP -26 (n=355, d=117) · SHORT_EXT -26 (n=194, d=68) · DOUBLE_DIP -31 (n=773, d=126) · DEEP_DIP -35 (n=109, d=68) · REVERSAL_3 -44 (n=227, d=40) · RSI2_DIP -78 (n=482, d=41) · TREND_RIDER -585 (n=92, d=31)
- **calm-down**: TREND_RIDER +408 (n=20, d=8) · BOLL_SNAP +339 (n=52, d=11) · PANIC_BOUNCE +126 (n=129, d=12) · PANIC_LITE +109 (n=217, d=13) · REVERSAL_3 +82 (n=78, d=7) · PULLBACK_50 +78 (n=34, d=8) · DOUBLE_DIP +58 (n=108, d=13) · FRESH_HIGH -223 (n=31, d=10) · RSI2_DIP -293 (n=117, d=8)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +867 (n=27, d=15) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -75 (n=34, d=17)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **33** entry days — **test LIVE (>=15)**
- PANIC_LITE: **31** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **31** entry days — **test LIVE (>=15)**
- REVERSAL_3: **31** entry days — **test LIVE (>=15)**
- PULLBACK_50: **30** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **28** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **26** entry days — **test LIVE (>=15)**
- TREND_RIDER: **17** entry days — **test LIVE (>=15)**
- DEEP_DIP: **16** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **15** entry days — **test LIVE (>=15)**
- SHORT_EXT: **7** entry days
- STORM_DIP: **1** entry days

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+867 bps, n=27); keep me on a short leash in calm-up (-35). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-18). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (+2). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-31). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-223). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+513 bps, n=12); keep me on a short leash in storm-up (-526). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+408 bps, n=20); keep me on a short leash in calm-up (-585). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-293). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+82 bps, n=78); keep me on a short leash in calm-up (-44). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+78 bps, n=34); keep me on a short leash in calm-up (-17). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
