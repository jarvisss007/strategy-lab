# Arena Roundtable — 2026-09-21

Tape: **calm-up** · session 2026-09-18 · 12 agents · opened 44, closed 82 this session · 161 open · 2236 forward closes all-time

> **This lab is 71% of the desk's scored record (2236 of 3160 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 52 of 161 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 82 closed this session, 2236 all-time. Oldest due row: TREND_RIDER WFC, entered 2026-08-28, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+185), DEEP_DIP (+14), PULLBACK_50 (+1); cold hands: RSI2_DIP (-67), TREND_RIDER (-207). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +39 bps over 1604 trades (t=2.77) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +185 (n=441, d=112) · DEEP_DIP +14 (n=115, d=70) · PULLBACK_50 +1 (n=187, d=37) · PANIC_LITE -4 (n=1872, d=144) · PANIC_BOUNCE -22 (n=932, d=125) · BOLL_SNAP -30 (n=364, d=118) · REVERSAL_3 -34 (n=218, d=38) · DOUBLE_DIP -36 (n=772, d=127) · SHORT_EXT -39 (n=189, d=73) · RSI2_DIP -67 (n=424, d=39) · TREND_RIDER -207 (n=89, d=30)
- **calm-down**: TREND_RIDER +364 (n=24, d=10) · BOLL_SNAP +302 (n=69, d=13) · PULLBACK_50 +163 (n=42, d=10) · PANIC_BOUNCE +136 (n=135, d=14) · DOUBLE_DIP +108 (n=123, d=15) · PANIC_LITE +101 (n=241, d=15) · REVERSAL_3 +95 (n=86, d=8) · RSI2_DIP -184 (n=153, d=10) · FRESH_HIGH -192 (n=32, d=11)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +867 (n=27, d=15) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -168 (n=35, d=19)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **37** entry days — **test LIVE (>=15)**
- PANIC_LITE: **35** entry days — **test LIVE (>=15)**
- REVERSAL_3: **35** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **34** entry days — **test LIVE (>=15)**
- PULLBACK_50: **34** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **32** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **30** entry days — **test LIVE (>=15)**
- TREND_RIDER: **20** entry days — **test LIVE (>=15)**
- DEEP_DIP: **18** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **17** entry days — **test LIVE (>=15)**
- SHORT_EXT: **8** entry days
- STORM_DIP: **1** entry days

## Notes to the desk

- DEEP_DIP to the desk: my weather is calm-down (+964 bps, n=11); keep me on a short leash in calm-up (+14). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-22). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (-4). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-36). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-192). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+611 bps, n=10); keep me on a short leash in calm-up (-39). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+364 bps, n=24); keep me on a short leash in calm-up (-207). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-184). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+95 bps, n=86); keep me on a short leash in calm-up (-34). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+163 bps, n=42); keep me on a short leash in calm-up (+1). Status: WATCH — positive but not significant.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
