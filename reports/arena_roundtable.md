# Arena Roundtable — 2026-09-08

Tape: **calm-up** · session 2026-09-04 · 12 agents · opened 32, closed 49 this session · 123 open · 1725 forward closes all-time

> **This lab is 74% of the desk's scored record (1725 of 2324 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 40 of 123 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 49 closed this session, 1725 all-time. Oldest due row: TREND_RIDER LRCX, entered 2026-08-17, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+204), PANIC_LITE (+6), DEEP_DIP (-3); cold hands: RSI2_DIP (-74), TREND_RIDER (-515). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 44% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +53 bps over 1574 trades (t=3.65) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +204 (n=438, d=115) · PANIC_LITE +6 (n=1828, d=143) · DEEP_DIP -3 (n=106, d=63) · PANIC_BOUNCE -16 (n=908, d=123) · PULLBACK_50 -24 (n=187, d=39) · BOLL_SNAP -24 (n=342, d=113) · DOUBLE_DIP -27 (n=761, d=123) · SHORT_EXT -30 (n=207, d=73) · REVERSAL_3 -39 (n=221, d=41) · RSI2_DIP -74 (n=482, d=42) · TREND_RIDER -515 (n=87, d=34)
- **calm-down**: BOLL_SNAP +359 (n=48, d=10) · TREND_RIDER +321 (n=20, d=8) · PANIC_BOUNCE +186 (n=118, d=11) · PANIC_LITE +172 (n=195, d=12) · PULLBACK_50 +167 (n=41, d=8) · DOUBLE_DIP +144 (n=93, d=12) · REVERSAL_3 +132 (n=71, d=7) · FRESH_HIGH -208 (n=32, d=10) · RSI2_DIP -248 (n=108, d=8)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +1205 (n=33, d=18) · DOUBLE_DIP +395 (n=294, d=33) · BOLL_SNAP +365 (n=291, d=32) · STORM_DIP +349 (n=467, d=34) · PANIC_BOUNCE +217 (n=303, d=32) · PANIC_LITE +146 (n=634, d=37) · FRESH_HIGH -8 (n=40, d=21)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- PANIC_LITE: **27** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **27** entry days — **test LIVE (>=15)**
- RSI2_DIP: **27** entry days — **test LIVE (>=15)**
- REVERSAL_3: **26** entry days — **test LIVE (>=15)**
- PULLBACK_50: **25** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **24** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **21** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **14** entry days
- DEEP_DIP: **14** entry days
- TREND_RIDER: **13** entry days
- SHORT_EXT: **5** entry days
- STORM_DIP: **1** entry days

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+1205 bps, n=33); keep me on a short leash in calm-up (-3). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_BOUNCE to the desk: my weather is storm-down (+217 bps, n=303); keep me on a short leash in calm-up (-16). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (+6). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+395 bps, n=294); keep me on a short leash in calm-up (-27). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+349 bps, n=467); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-208). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+264 bps, n=13); keep me on a short leash in storm-up (-526). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+321 bps, n=20); keep me on a short leash in calm-up (-515). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-248). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+132 bps, n=71); keep me on a short leash in calm-up (-39). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+365 bps, n=291); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+167 bps, n=41); keep me on a short leash in calm-up (-24). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
