# Arena Roundtable — 2026-09-02

Tape: **calm-up** · session 2026-09-01 · 12 agents · opened 104, closed 79 this session · 233 open · 1516 forward closes all-time

> **This lab is 79% of the desk's scored record (1516 of 1915 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 55 of 233 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 79 closed this session, 1516 all-time. Oldest due row: DEEP_DIP GLW, entered 2026-08-19, hold 10, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+194), PANIC_LITE (-0), PANIC_BOUNCE (-25); cold hands: RSI2_DIP (-110), TREND_RIDER (-631). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +46 bps over 1610 trades (t=3.23) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

- **calm-up**: FRESH_HIGH +194 (n=443) · PANIC_LITE -0 (n=1836) · PANIC_BOUNCE -25 (n=910) · SHORT_EXT -34 (n=217) · PULLBACK_50 -45 (n=197) · BOLL_SNAP -51 (n=342) · DOUBLE_DIP -56 (n=777) · DEEP_DIP -105 (n=107) · REVERSAL_3 -108 (n=233) · RSI2_DIP -110 (n=519) · TREND_RIDER -631 (n=85)
- **calm-down**: BOLL_SNAP +359 (n=48) · PANIC_BOUNCE +186 (n=118) · PANIC_LITE +172 (n=195) · DOUBLE_DIP +144 (n=93) · PULLBACK_50 +138 (n=38) · REVERSAL_3 +132 (n=71) · FRESH_HIGH -208 (n=32) · RSI2_DIP -261 (n=105)
- **storm-up**: DOUBLE_DIP +45 (n=67) · PANIC_LITE +38 (n=142) · PANIC_BOUNCE +0 (n=103) · BOLL_SNAP -201 (n=42) · STORM_DIP -296 (n=134)
- **storm-down**: DEEP_DIP +1034 (n=33) · DOUBLE_DIP +398 (n=295) · STORM_DIP +351 (n=469) · BOLL_SNAP +348 (n=291) · PANIC_BOUNCE +216 (n=307) · PANIC_LITE +152 (n=652) · FRESH_HIGH -34 (n=37)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- PANIC_LITE: **25** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **24** entry days — **test LIVE (>=15)**
- RSI2_DIP: **24** entry days — **test LIVE (>=15)**
- REVERSAL_3: **23** entry days — **test LIVE (>=15)**
- PULLBACK_50: **22** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **21** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **18** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **12** entry days
- DEEP_DIP: **12** entry days
- TREND_RIDER: **11** entry days
- SHORT_EXT: **4** entry days
- STORM_DIP: **1** entry days

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+1034 bps, n=33); keep me on a short leash in calm-up (-105). Status: WATCH — positive but not significant.
- PANIC_BOUNCE to the desk: my weather is storm-down (+216 bps, n=307); keep me on a short leash in calm-up (-25). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is calm-down (+172 bps, n=195); keep me on a short leash in calm-up (-0). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+398 bps, n=295); keep me on a short leash in calm-up (-56). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+351 bps, n=469); keep me on a short leash in storm-up (-296). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+591 bps, n=15); keep me on a short leash in calm-down (-208). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+482 bps, n=13); keep me on a short leash in storm-up (-526). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+396 bps, n=19); keep me on a short leash in calm-up (-631). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-261). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+132 bps, n=71); keep me on a short leash in calm-up (-108). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is calm-down (+359 bps, n=48); keep me on a short leash in storm-up (-201). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+138 bps, n=38); keep me on a short leash in calm-up (-45). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
