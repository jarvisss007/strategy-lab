# Arena Roundtable — 2026-09-22

Tape: **calm-up** · session 2026-09-21 · 12 agents · opened 31, closed 52 this session · 140 open · 2288 forward closes all-time

> **This lab is 70% of the desk's scored record (2288 of 3289 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 43 of 140 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 52 closed this session, 2288 all-time. Oldest due row: PULLBACK_50 KO, entered 2026-09-15, hold 5, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+183), DEEP_DIP (+20), PULLBACK_50 (+2); cold hands: RSI2_DIP (-69), TREND_RIDER (-165). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +39 bps over 1608 trades (t=2.74) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +183 (n=445, d=113) · DEEP_DIP +20 (n=115, d=70) · PULLBACK_50 +2 (n=192, d=38) · PANIC_LITE -4 (n=1876, d=145) · PANIC_BOUNCE -21 (n=932, d=125) · BOLL_SNAP -30 (n=364, d=118) · REVERSAL_3 -36 (n=220, d=39) · DOUBLE_DIP -37 (n=772, d=127) · SHORT_EXT -40 (n=190, d=74) · RSI2_DIP -69 (n=427, d=40) · TREND_RIDER -165 (n=93, d=31)
- **calm-down**: TREND_RIDER +378 (n=24, d=10) · BOLL_SNAP +310 (n=69, d=13) · PULLBACK_50 +155 (n=42, d=10) · PANIC_BOUNCE +136 (n=135, d=14) · DOUBLE_DIP +108 (n=123, d=15) · PANIC_LITE +101 (n=241, d=15) · REVERSAL_3 +95 (n=86, d=8) · RSI2_DIP -183 (n=153, d=10) · FRESH_HIGH -197 (n=32, d=11)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +867 (n=27, d=15) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -168 (n=35, d=19)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **38** entry days — **test LIVE (>=15)**
- PANIC_LITE: **36** entry days — **test LIVE (>=15)**
- REVERSAL_3: **36** entry days — **test LIVE (>=15)**
- PULLBACK_50: **35** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **34** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **33** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **31** entry days — **test LIVE (>=15)**
- TREND_RIDER: **21** entry days — **test LIVE (>=15)**
- DEEP_DIP: **18** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **17** entry days — **test LIVE (>=15)**
- SHORT_EXT: **9** entry days
- STORM_DIP: **1** entry days

## Notes to the desk

- DEEP_DIP to the desk: my weather is calm-down (+986 bps, n=11); keep me on a short leash in calm-up (+20). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-21). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (-4). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-37). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-197). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+611 bps, n=10); keep me on a short leash in calm-up (-40). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+378 bps, n=24); keep me on a short leash in calm-up (-165). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-183). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+95 bps, n=86); keep me on a short leash in calm-up (-36). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+155 bps, n=42); keep me on a short leash in calm-up (+2). Status: WATCH — positive but not significant.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
