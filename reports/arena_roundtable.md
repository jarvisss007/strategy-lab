# Arena Roundtable — 2026-08-28

Tape: **calm-up** · session 2026-08-27 · 12 agents · opened 30, closed 32 this session · 118 open · 1380 forward closes all-time

> **This lab is 81% of the desk's scored record (1380 of 1696 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 31 of 118 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 32 closed this session, 1380 all-time. Oldest due row: TREND_RIDER MS, entered 2026-08-07, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+179), PANIC_LITE (+2), PULLBACK_50 (-24); cold hands: REVERSAL_3 (-122), TREND_RIDER (-557). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +50 bps over 1581 trades (t=3.46) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

- **calm-up**: FRESH_HIGH +179 (n=459) · PANIC_LITE +2 (n=1792) · PULLBACK_50 -24 (n=193) · PANIC_BOUNCE -26 (n=892) · SHORT_EXT -44 (n=219) · BOLL_SNAP -56 (n=331) · DOUBLE_DIP -60 (n=764) · DEEP_DIP -78 (n=102) · RSI2_DIP -82 (n=495) · REVERSAL_3 -122 (n=201) · TREND_RIDER -557 (n=84)
- **calm-down**: BOLL_SNAP +359 (n=48) · PANIC_BOUNCE +186 (n=118) · PANIC_LITE +172 (n=195) · PULLBACK_50 +150 (n=39) · DOUBLE_DIP +144 (n=93) · REVERSAL_3 +132 (n=71) · FRESH_HIGH -208 (n=32) · RSI2_DIP -261 (n=105)
- **storm-up**: PANIC_LITE +65 (n=132) · DOUBLE_DIP +50 (n=66) · PANIC_BOUNCE +26 (n=98) · BOLL_SNAP -166 (n=39) · STORM_DIP -296 (n=134)
- **storm-down**: DEEP_DIP +1034 (n=33) · DOUBLE_DIP +394 (n=296) · STORM_DIP +351 (n=469) · BOLL_SNAP +345 (n=292) · PANIC_BOUNCE +216 (n=308) · PANIC_LITE +153 (n=657) · FRESH_HIGH -51 (n=34)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- PANIC_LITE: **22** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **22** entry days — **test LIVE (>=15)**
- RSI2_DIP: **22** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **21** entry days — **test LIVE (>=15)**
- REVERSAL_3: **20** entry days — **test LIVE (>=15)**
- PULLBACK_50: **20** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **16** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **10** entry days
- DEEP_DIP: **10** entry days
- TREND_RIDER: **10** entry days
- SHORT_EXT: **3** entry days
- STORM_DIP: **1** entry days

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+1034 bps, n=33); keep me on a short leash in calm-up (-78). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+216 bps, n=308); keep me on a short leash in calm-up (-26). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is calm-down (+172 bps, n=195); keep me on a short leash in calm-up (+2). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+394 bps, n=296); keep me on a short leash in calm-up (-60). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+351 bps, n=469); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+591 bps, n=15); keep me on a short leash in calm-down (-208). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+482 bps, n=13); keep me on a short leash in storm-up (-526). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+396 bps, n=19); keep me on a short leash in calm-up (-557). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-261). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+132 bps, n=71); keep me on a short leash in calm-up (-122). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is calm-down (+359 bps, n=48); keep me on a short leash in storm-up (-166). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+150 bps, n=39); keep me on a short leash in calm-up (-24). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
