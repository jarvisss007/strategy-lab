# Arena Roundtable — 2026-09-04

Tape: **calm-up** · session 2026-09-03 · 12 agents · opened 18, closed 105 this session · 138 open · 1676 forward closes all-time

> **This lab is 79% of the desk's scored record (1676 of 2124 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 49 of 138 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 105 closed this session, 1676 all-time. Oldest due row: TREND_RIDER RDDT, entered 2026-08-14, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+207), PANIC_LITE (+6), PULLBACK_50 (-7); cold hands: REVERSAL_3 (-90), TREND_RIDER (-538). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +54 bps over 1596 trades (t=3.78) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

- **calm-up**: FRESH_HIGH +207 (n=440) · PANIC_LITE +6 (n=1828) · PULLBACK_50 -7 (n=197) · PANIC_BOUNCE -15 (n=906) · BOLL_SNAP -21 (n=355) · DOUBLE_DIP -25 (n=778) · DEEP_DIP -36 (n=105) · SHORT_EXT -48 (n=212) · RSI2_DIP -88 (n=512) · REVERSAL_3 -90 (n=226) · TREND_RIDER -538 (n=89)
- **calm-down**: BOLL_SNAP +359 (n=48) · PANIC_BOUNCE +186 (n=118) · PANIC_LITE +172 (n=195) · DOUBLE_DIP +144 (n=93) · PULLBACK_50 +138 (n=38) · REVERSAL_3 +132 (n=71) · FRESH_HIGH -208 (n=32) · RSI2_DIP -261 (n=105)
- **storm-up**: PANIC_LITE +174 (n=95) · PANIC_BOUNCE +142 (n=67) · DOUBLE_DIP +138 (n=51) · BOLL_SNAP -74 (n=21) · STORM_DIP -291 (n=87)
- **storm-down**: DEEP_DIP +958 (n=35) · DOUBLE_DIP +384 (n=295) · BOLL_SNAP +333 (n=293) · STORM_DIP +310 (n=474) · PANIC_BOUNCE +212 (n=314) · PANIC_LITE +152 (n=665) · FRESH_HIGH -8 (n=38)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- PANIC_LITE: **27** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **26** entry days — **test LIVE (>=15)**
- RSI2_DIP: **26** entry days — **test LIVE (>=15)**
- REVERSAL_3: **25** entry days — **test LIVE (>=15)**
- PULLBACK_50: **24** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **23** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **20** entry days — **test LIVE (>=15)**
- DEEP_DIP: **14** entry days
- FRESH_HIGH: **13** entry days
- TREND_RIDER: **12** entry days
- SHORT_EXT: **5** entry days
- STORM_DIP: **1** entry days

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+958 bps, n=35); keep me on a short leash in calm-up (-36). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_BOUNCE to the desk: my weather is storm-down (+212 bps, n=314); keep me on a short leash in calm-up (-15). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (+6). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+384 bps, n=295); keep me on a short leash in calm-up (-25). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+310 bps, n=474); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-208). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+360 bps, n=12); keep me on a short leash in storm-up (-526). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+396 bps, n=19); keep me on a short leash in calm-up (-538). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-261). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+132 bps, n=71); keep me on a short leash in calm-up (-90). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is calm-down (+359 bps, n=48); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+138 bps, n=38); keep me on a short leash in calm-up (-7). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
