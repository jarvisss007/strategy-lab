# Arena Roundtable — 2026-09-26

Tape: **calm-up** · session 2026-09-25 · 12 agents · opened 23, closed 49 this session · 165 open · 2441 forward closes all-time

> **This lab is 70% of the desk's scored record (2441 of 3502 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 165 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 49 closed this session, 2441 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: SHORT_EXT (+68), FRESH_HIGH (+56), REVERSAL_3 (+20); cold hands: DEEP_DIP (-148), TREND_RIDER (-349). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 52% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 81% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +6 bps over 638 trades (t=0.27) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: SHORT_EXT +68 (n=39, d=34) · FRESH_HIGH +56 (n=179, d=82) · REVERSAL_3 +20 (n=84, d=35) · BOLL_SNAP -19 (n=171, d=87) · PANIC_BOUNCE -32 (n=419, d=97) · PULLBACK_50 -40 (n=62, d=29) · PANIC_LITE -51 (n=783, d=130) · RSI2_DIP -52 (n=151, d=37) · DOUBLE_DIP -71 (n=318, d=100) · DEEP_DIP -148 (n=40, d=36) · TREND_RIDER -349 (n=31, d=22)
- **calm-down**: BOLL_SNAP +386 (n=27, d=10) · DOUBLE_DIP +190 (n=45, d=13) · PANIC_LITE +178 (n=89, d=14) · PANIC_BOUNCE +160 (n=49, d=10) · REVERSAL_3 -67 (n=26, d=8) · RSI2_DIP -171 (n=56, d=10)
- **storm-up**: PANIC_LITE +54 (n=30, d=3) · STORM_DIP -327 (n=32, d=3)
- **storm-down**: DOUBLE_DIP +442 (n=119, d=24) · STORM_DIP +381 (n=176, d=25) · BOLL_SNAP +294 (n=112, d=25) · PANIC_LITE +93 (n=216, d=31) · PANIC_BOUNCE +60 (n=106, d=24) · FRESH_HIGH -151 (n=20, d=16)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **42** entry days — **test LIVE (>=15)**
- PANIC_LITE: **40** entry days — **test LIVE (>=15)**
- REVERSAL_3: **39** entry days — **test LIVE (>=15)**
- PULLBACK_50: **39** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **37** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **35** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **34** entry days — **test LIVE (>=15)**
- TREND_RIDER: **23** entry days — **test LIVE (>=15)**
- DEEP_DIP: **21** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **18** entry days — **test LIVE (>=15)**
- SHORT_EXT: **9** entry days
- STORM_DIP: **1** entry days

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+1340 bps, n=10); keep me on a short leash in calm-up (-148). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is calm-down (+160 bps, n=49); keep me on a short leash in storm-up (-60). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is calm-down (+178 bps, n=89); keep me on a short leash in calm-up (-51). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+442 bps, n=119); keep me on a short leash in calm-up (-71). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+381 bps, n=176); keep me on a short leash in storm-up (-327). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is calm-up (+56 bps, n=179); keep me on a short leash in calm-down (-320). Status: DEAD — loses to costs/SPY.
- SHORT_EXT to the desk: my weather is calm-up (+68 bps, n=39); keep me on a short leash in calm-up (+68). Status: WATCH — positive but not significant.
- TREND_RIDER to the desk: my weather is calm-up (-349 bps, n=31); keep me on a short leash in calm-up (-349). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-up (-52 bps, n=151); keep me on a short leash in calm-down (-171). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-up (+20 bps, n=84); keep me on a short leash in calm-down (-67). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is calm-down (+386 bps, n=27); keep me on a short leash in storm-up (-88). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+47 bps, n=17); keep me on a short leash in calm-up (-40). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
