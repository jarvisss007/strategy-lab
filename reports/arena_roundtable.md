# Arena Roundtable — 2026-09-09

Tape: **calm-up** · session 2026-09-08 · 12 agents · opened 65, closed 40 this session · 149 open · 1765 forward closes all-time

> **This lab is 74% of the desk's scored record (1765 of 2385 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 29 of 149 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 40 closed this session, 1765 all-time. Oldest due row: TREND_RIDER BRK-B, entered 2026-08-18, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+208), PANIC_LITE (+6), PANIC_BOUNCE (-16); cold hands: RSI2_DIP (-82), TREND_RIDER (-505). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 44% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +55 bps over 1579 trades (t=3.78) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +208 (n=439, d=115) · PANIC_LITE +6 (n=1836, d=144) · PANIC_BOUNCE -16 (n=911, d=124) · DEEP_DIP -18 (n=106, d=64) · SHORT_EXT -22 (n=203, d=70) · BOLL_SNAP -24 (n=348, d=114) · DOUBLE_DIP -27 (n=765, d=124) · PULLBACK_50 -28 (n=190, d=39) · REVERSAL_3 -51 (n=212, d=41) · RSI2_DIP -82 (n=485, d=42) · TREND_RIDER -505 (n=94, d=34)
- **calm-down**: BOLL_SNAP +359 (n=48, d=10) · TREND_RIDER +321 (n=20, d=8) · PANIC_BOUNCE +186 (n=118, d=11) · PANIC_LITE +172 (n=195, d=12) · PULLBACK_50 +167 (n=41, d=8) · REVERSAL_3 +166 (n=79, d=7) · DOUBLE_DIP +144 (n=93, d=12) · FRESH_HIGH -208 (n=32, d=10) · RSI2_DIP -210 (n=121, d=8)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +1224 (n=32, d=17) · DOUBLE_DIP +432 (n=286, d=33) · BOLL_SNAP +386 (n=288, d=30) · STORM_DIP +372 (n=462, d=33) · PANIC_BOUNCE +249 (n=300, d=31) · PANIC_LITE +166 (n=631, d=36) · FRESH_HIGH -36 (n=40, d=20)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **28** entry days — **test LIVE (>=15)**
- PANIC_LITE: **27** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **27** entry days — **test LIVE (>=15)**
- REVERSAL_3: **27** entry days — **test LIVE (>=15)**
- PULLBACK_50: **26** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **25** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **22** entry days — **test LIVE (>=15)**
- DEEP_DIP: **15** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **14** entry days
- TREND_RIDER: **14** entry days
- SHORT_EXT: **5** entry days
- STORM_DIP: **1** entry days

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+1224 bps, n=32); keep me on a short leash in calm-up (-18). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_BOUNCE to the desk: my weather is storm-down (+249 bps, n=300); keep me on a short leash in calm-up (-16). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (+6). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+432 bps, n=286); keep me on a short leash in calm-up (-27). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+372 bps, n=462); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-208). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+264 bps, n=13); keep me on a short leash in storm-up (-526). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+321 bps, n=20); keep me on a short leash in calm-up (-505). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-210). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+166 bps, n=79); keep me on a short leash in calm-up (-51). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+386 bps, n=288); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+167 bps, n=41); keep me on a short leash in calm-up (-28). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
