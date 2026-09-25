# Arena Roundtable — 2026-09-25

Tape: **calm-up** · session 2026-09-24 · 12 agents · opened 57, closed 55 this session · 191 open · 2392 forward closes all-time

> **This lab is 69% of the desk's scored record (2392 of 3450 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 49 of 191 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 55 closed this session, 2392 all-time. Oldest due row: TREND_RIDER IOT, entered 2026-09-03, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+212), DEEP_DIP (+34), PULLBACK_50 (+25); cold hands: SHORT_EXT (-39), TREND_RIDER (-180). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 43% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +39 bps over 1633 trades (t=2.77) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +212 (n=436, d=111) · DEEP_DIP +34 (n=117, d=71) · PULLBACK_50 +25 (n=185, d=38) · RSI2_DIP +2 (n=444, d=40) · PANIC_LITE -3 (n=1901, d=145) · REVERSAL_3 -16 (n=212, d=38) · PANIC_BOUNCE -21 (n=933, d=125) · BOLL_SNAP -23 (n=378, d=119) · DOUBLE_DIP -37 (n=781, d=127) · SHORT_EXT -39 (n=192, d=76) · TREND_RIDER -180 (n=92, d=32)
- **calm-down**: TREND_RIDER +341 (n=25, d=10) · BOLL_SNAP +310 (n=69, d=13) · PULLBACK_50 +155 (n=44, d=10) · PANIC_BOUNCE +136 (n=135, d=14) · DOUBLE_DIP +108 (n=123, d=15) · PANIC_LITE +101 (n=241, d=15) · REVERSAL_3 +93 (n=85, d=8) · RSI2_DIP -227 (n=141, d=10) · FRESH_HIGH -243 (n=32, d=11)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +753 (n=28, d=15) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -148 (n=36, d=19)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **41** entry days — **test LIVE (>=15)**
- PANIC_LITE: **39** entry days — **test LIVE (>=15)**
- REVERSAL_3: **39** entry days — **test LIVE (>=15)**
- PULLBACK_50: **38** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **36** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **35** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **33** entry days — **test LIVE (>=15)**
- TREND_RIDER: **22** entry days — **test LIVE (>=15)**
- DEEP_DIP: **20** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **17** entry days — **test LIVE (>=15)**
- SHORT_EXT: **9** entry days
- STORM_DIP: **1** entry days

## Notes to the desk

- DEEP_DIP to the desk: my weather is calm-down (+921 bps, n=12); keep me on a short leash in calm-up (+34). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-21). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (-3). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-37). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-243). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+611 bps, n=10); keep me on a short leash in calm-up (-39). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+341 bps, n=25); keep me on a short leash in calm-up (-180). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-227). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+93 bps, n=85); keep me on a short leash in calm-up (-16). Status: WATCH — positive but not significant.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+155 bps, n=44); keep me on a short leash in calm-up (+25). Status: WATCH — positive but not significant.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
