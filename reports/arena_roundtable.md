# Arena Roundtable — 2026-09-10

Tape: **calm-down** · session 2026-09-10 · 12 agents · opened 70, closed 28 this session · 237 open · 1822 forward closes all-time

> **This lab is 73% of the desk's scored record (1795 of 2455 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 237 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 28 closed this session, 1822 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-DOWN. Our pooled record in this weather — hot hands: BOLL_SNAP (+359), PULLBACK_50 (+254), PANIC_BOUNCE (+186); cold hands: FRESH_HIGH (-208), RSI2_DIP (-299). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 44% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +48 bps over 1569 trades (t=3.3) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +204 (n=440, d=115) · PANIC_LITE +2 (n=1860, d=145) · DEEP_DIP -18 (n=108, d=67) · PANIC_BOUNCE -18 (n=917, d=125) · DOUBLE_DIP -30 (n=769, d=125) · BOLL_SNAP -30 (n=352, d=115) · SHORT_EXT -32 (n=196, d=67) · PULLBACK_50 -38 (n=202, d=39) · REVERSAL_3 -46 (n=228, d=41) · RSI2_DIP -84 (n=494, d=42) · TREND_RIDER -562 (n=91, d=32)
- **calm-down**: BOLL_SNAP +359 (n=48, d=10) · PULLBACK_50 +254 (n=26, d=7) · PANIC_BOUNCE +186 (n=118, d=11) · PANIC_LITE +172 (n=195, d=12) · DOUBLE_DIP +144 (n=93, d=12) · REVERSAL_3 +112 (n=68, d=6) · FRESH_HIGH -208 (n=32, d=10) · RSI2_DIP -299 (n=100, d=7)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +867 (n=27, d=15) · DOUBLE_DIP +423 (n=273, d=31) · BOLL_SNAP +378 (n=260, d=29) · STORM_DIP +348 (n=419, d=32) · PANIC_BOUNCE +188 (n=263, d=30) · PANIC_LITE +138 (n=570, d=35) · FRESH_HIGH -68 (n=40, d=19)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **31** entry days — **test LIVE (>=15)**
- PANIC_LITE: **29** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **29** entry days — **test LIVE (>=15)**
- REVERSAL_3: **29** entry days — **test LIVE (>=15)**
- PULLBACK_50: **28** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **26** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **24** entry days — **test LIVE (>=15)**
- TREND_RIDER: **16** entry days — **test LIVE (>=15)**
- DEEP_DIP: **15** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **14** entry days
- SHORT_EXT: **6** entry days
- STORM_DIP: **1** entry days

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+867 bps, n=27); keep me on a short leash in calm-up (-18). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+188 bps, n=263); keep me on a short leash in calm-up (-18). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (+2). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+423 bps, n=273); keep me on a short leash in calm-up (-30). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=419); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-208). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+366 bps, n=12); keep me on a short leash in storm-up (-526). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+469 bps, n=17); keep me on a short leash in calm-up (-562). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-299). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+112 bps, n=68); keep me on a short leash in calm-up (-46). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+378 bps, n=260); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+254 bps, n=26); keep me on a short leash in calm-up (-38). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
