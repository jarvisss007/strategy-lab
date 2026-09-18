# Arena Roundtable — 2026-09-18

Tape: **calm-up** · session 2026-09-17 · 12 agents · opened 24, closed 36 this session · 198 open · 2155 forward closes all-time

> **This lab is 71% of the desk's scored record (2154 of 3030 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 198 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 36 closed this session, 2155 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+205), PANIC_LITE (-1), PANIC_BOUNCE (-17); cold hands: RSI2_DIP (-53), TREND_RIDER (-456). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +40 bps over 1608 trades (t=2.84) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +205 (n=441, d=114) · PANIC_LITE -1 (n=1881, d=144) · PANIC_BOUNCE -17 (n=938, d=125) · SHORT_EXT -22 (n=190, d=69) · PULLBACK_50 -25 (n=189, d=37) · DEEP_DIP -27 (n=113, d=68) · BOLL_SNAP -28 (n=361, d=117) · DOUBLE_DIP -31 (n=774, d=126) · REVERSAL_3 -37 (n=215, d=38) · RSI2_DIP -53 (n=449, d=39) · TREND_RIDER -456 (n=93, d=31)
- **calm-down**: TREND_RIDER +392 (n=23, d=10) · BOLL_SNAP +272 (n=69, d=13) · PULLBACK_50 +129 (n=42, d=10) · PANIC_BOUNCE +128 (n=135, d=14) · PANIC_LITE +102 (n=241, d=15) · REVERSAL_3 +78 (n=86, d=8) · DOUBLE_DIP +50 (n=123, d=15) · FRESH_HIGH -191 (n=32, d=11) · RSI2_DIP -227 (n=147, d=10)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +867 (n=27, d=15) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -117 (n=34, d=17)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **36** entry days — **test LIVE (>=15)**
- PANIC_LITE: **34** entry days — **test LIVE (>=15)**
- REVERSAL_3: **34** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **33** entry days — **test LIVE (>=15)**
- PULLBACK_50: **33** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **31** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **29** entry days — **test LIVE (>=15)**
- TREND_RIDER: **20** entry days — **test LIVE (>=15)**
- DEEP_DIP: **18** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **16** entry days — **test LIVE (>=15)**
- SHORT_EXT: **7** entry days
- STORM_DIP: **1** entry days

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+867 bps, n=27); keep me on a short leash in calm-up (-27). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-17). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (-1). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-31). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-191). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+611 bps, n=10); keep me on a short leash in storm-up (-526). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+392 bps, n=23); keep me on a short leash in calm-up (-456). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-227). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+78 bps, n=86); keep me on a short leash in calm-up (-37). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+129 bps, n=42); keep me on a short leash in calm-up (-25). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
