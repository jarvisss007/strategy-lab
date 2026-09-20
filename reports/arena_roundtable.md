# Arena Roundtable — 2026-09-20

Tape: **calm-up** · session 2026-09-18 · 12 agents · opened 44, closed 82 this session · 161 open · 2236 forward closes all-time

> **This lab is 71% of the desk's scored record (2236 of 3160 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 161 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 82 closed this session, 2236 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+198), PANIC_LITE (-7), PULLBACK_50 (-7); cold hands: RSI2_DIP (-71), TREND_RIDER (-408). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +37 bps over 1595 trades (t=2.59) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +198 (n=441, d=114) · PANIC_LITE -7 (n=1860, d=144) · PULLBACK_50 -7 (n=186, d=37) · SHORT_EXT -16 (n=190, d=69) · DEEP_DIP -20 (n=112, d=67) · PANIC_BOUNCE -23 (n=929, d=125) · BOLL_SNAP -31 (n=360, d=118) · DOUBLE_DIP -35 (n=774, d=126) · REVERSAL_3 -41 (n=216, d=38) · RSI2_DIP -71 (n=428, d=39) · TREND_RIDER -408 (n=93, d=31)
- **calm-down**: TREND_RIDER +344 (n=24, d=10) · BOLL_SNAP +281 (n=69, d=13) · PULLBACK_50 +155 (n=42, d=10) · PANIC_BOUNCE +136 (n=135, d=14) · PANIC_LITE +101 (n=241, d=15) · REVERSAL_3 +96 (n=86, d=8) · DOUBLE_DIP +90 (n=123, d=15) · FRESH_HIGH -193 (n=32, d=11) · RSI2_DIP -196 (n=151, d=10)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +867 (n=27, d=15) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -157 (n=34, d=18)

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

- DEEP_DIP to the desk: my weather is storm-down (+867 bps, n=27); keep me on a short leash in calm-up (-20). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-23). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (-7). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-35). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-193). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+611 bps, n=10); keep me on a short leash in storm-up (-526). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+344 bps, n=24); keep me on a short leash in calm-up (-408). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-196). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+96 bps, n=86); keep me on a short leash in calm-up (-41). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+155 bps, n=42); keep me on a short leash in calm-up (-7). Status: WATCH — positive but not significant.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
