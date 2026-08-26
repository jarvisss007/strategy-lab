# Arena Roundtable — 2026-08-26

Tape: **calm-up** · session 2026-08-25 · 12 agents · opened 0, closed 0 this session · 237 open · 1186 forward closes all-time

> **This lab is 81% of the desk's scored record (1186 of 1465 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 161 of 237 open rows read `days_left <= 0`; 77 of those are PAST due (negative). 0 closed this session, 1186 all-time. Oldest due row: TREND_RIDER PLTR, entered 2026-08-04, hold 15, days_left -1. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+179), PANIC_LITE (+12), PANIC_BOUNCE (-10); cold hands: DEEP_DIP (-145), TREND_RIDER (-469). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 46% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 85% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +52 bps over 1595 trades (t=3.59) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

- **calm-up**: FRESH_HIGH +179 (n=454) · PANIC_LITE +12 (n=1835) · PANIC_BOUNCE -10 (n=920) · PULLBACK_50 -18 (n=195) · BOLL_SNAP -47 (n=349) · DOUBLE_DIP -50 (n=781) · SHORT_EXT -53 (n=217) · RSI2_DIP -100 (n=479) · REVERSAL_3 -133 (n=192) · DEEP_DIP -145 (n=104) · TREND_RIDER -469 (n=85)
- **calm-down**: BOLL_SNAP +359 (n=48) · PANIC_BOUNCE +186 (n=118) · PANIC_LITE +172 (n=195) · PULLBACK_50 +150 (n=39) · DOUBLE_DIP +144 (n=93) · REVERSAL_3 +132 (n=71) · FRESH_HIGH -208 (n=32) · RSI2_DIP -260 (n=106)
- **storm-up**: PANIC_LITE +75 (n=131) · PANIC_BOUNCE +36 (n=97) · DOUBLE_DIP +16 (n=71) · BOLL_SNAP -185 (n=41) · STORM_DIP -296 (n=134)
- **storm-down**: DEEP_DIP +1034 (n=33) · DOUBLE_DIP +395 (n=295) · STORM_DIP +351 (n=469) · BOLL_SNAP +345 (n=292) · PANIC_BOUNCE +215 (n=309) · PANIC_LITE +153 (n=657) · FRESH_HIGH -52 (n=36)

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+1034 bps, n=33); keep me on a short leash in calm-up (-145). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+215 bps, n=309); keep me on a short leash in calm-up (-10). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is calm-down (+172 bps, n=195); keep me on a short leash in calm-up (+12). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+395 bps, n=295); keep me on a short leash in calm-up (-50). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+351 bps, n=469); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+591 bps, n=15); keep me on a short leash in calm-down (-208). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+482 bps, n=13); keep me on a short leash in storm-up (-526). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+396 bps, n=19); keep me on a short leash in calm-up (-469). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-260). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+132 bps, n=71); keep me on a short leash in calm-up (-133). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is calm-down (+359 bps, n=48); keep me on a short leash in storm-up (-185). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+150 bps, n=39); keep me on a short leash in calm-up (-18). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
