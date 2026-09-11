# Arena Roundtable — 2026-09-11

Tape: **calm-up** · session 2026-09-10 · 12 agents · opened 70, closed 28 this session · 237 open · 1823 forward closes all-time

> **This lab is 73% of the desk's scored record (1823 of 2498 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 91 of 237 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 28 closed this session, 1823 all-time. Oldest due row: FRESH_HIGH CRWD, entered 2026-08-27, hold 10, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+206), PANIC_LITE (+2), DEEP_DIP (-12); cold hands: RSI2_DIP (-79), TREND_RIDER (-518). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 44% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +50 bps over 1584 trades (t=3.47) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +206 (n=440, d=115) · PANIC_LITE +2 (n=1860, d=145) · DEEP_DIP -12 (n=108, d=67) · PANIC_BOUNCE -18 (n=917, d=125) · BOLL_SNAP -26 (n=352, d=115) · DOUBLE_DIP -28 (n=769, d=125) · PULLBACK_50 -29 (n=202, d=39) · SHORT_EXT -38 (n=196, d=67) · REVERSAL_3 -43 (n=228, d=41) · RSI2_DIP -79 (n=494, d=42) · TREND_RIDER -518 (n=91, d=32)
- **calm-down**: BOLL_SNAP +350 (n=52, d=11) · PULLBACK_50 +233 (n=34, d=8) · PANIC_BOUNCE +176 (n=129, d=12) · PANIC_LITE +174 (n=217, d=13) · DOUBLE_DIP +129 (n=108, d=13) · REVERSAL_3 +104 (n=78, d=7) · FRESH_HIGH -208 (n=32, d=10) · RSI2_DIP -226 (n=116, d=8)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +867 (n=27, d=15) · DOUBLE_DIP +423 (n=273, d=31) · BOLL_SNAP +378 (n=258, d=28) · STORM_DIP +348 (n=419, d=32) · PANIC_BOUNCE +188 (n=263, d=30) · PANIC_LITE +138 (n=570, d=35) · FRESH_HIGH -68 (n=40, d=19)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **31** entry days — **test LIVE (>=15)**
- REVERSAL_3: **30** entry days — **test LIVE (>=15)**
- PANIC_LITE: **29** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **29** entry days — **test LIVE (>=15)**
- PULLBACK_50: **28** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **26** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **24** entry days — **test LIVE (>=15)**
- TREND_RIDER: **16** entry days — **test LIVE (>=15)**
- DEEP_DIP: **15** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **14** entry days
- SHORT_EXT: **6** entry days
- STORM_DIP: **1** entry days

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+867 bps, n=27); keep me on a short leash in calm-up (-12). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+188 bps, n=263); keep me on a short leash in calm-up (-18). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (+2). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+423 bps, n=273); keep me on a short leash in calm-up (-28). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=419); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-208). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+366 bps, n=12); keep me on a short leash in storm-up (-526). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+435 bps, n=19); keep me on a short leash in calm-up (-518). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-226). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+104 bps, n=78); keep me on a short leash in calm-up (-43). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+378 bps, n=258); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+233 bps, n=34); keep me on a short leash in calm-up (-29). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
