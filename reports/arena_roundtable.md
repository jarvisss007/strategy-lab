# Arena Roundtable — 2026-09-10

Tape: **calm-up** · session 2026-09-09 · 12 agents · opened 77, closed 29 this session · 195 open · 1795 forward closes all-time

> **This lab is 73% of the desk's scored record (1795 of 2455 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 27 of 195 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 29 closed this session, 1795 all-time. Oldest due row: TREND_RIDER MRVL, entered 2026-08-19, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+205), PANIC_LITE (+4), PANIC_BOUNCE (-16); cold hands: RSI2_DIP (-87), TREND_RIDER (-530). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 85% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +55 bps over 1592 trades (t=3.83) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +205 (n=440, d=115) · PANIC_LITE +4 (n=1860, d=145) · PANIC_BOUNCE -16 (n=917, d=125) · DOUBLE_DIP -29 (n=769, d=125) · BOLL_SNAP -30 (n=352, d=115) · PULLBACK_50 -32 (n=205, d=40) · SHORT_EXT -33 (n=200, d=66) · DEEP_DIP -43 (n=107, d=66) · REVERSAL_3 -46 (n=229, d=42) · RSI2_DIP -87 (n=501, d=43) · TREND_RIDER -530 (n=95, d=33)
- **calm-down**: BOLL_SNAP +359 (n=48, d=10) · PULLBACK_50 +254 (n=26, d=7) · PANIC_BOUNCE +186 (n=118, d=11) · PANIC_LITE +172 (n=195, d=12) · DOUBLE_DIP +144 (n=93, d=12) · REVERSAL_3 +112 (n=68, d=6) · FRESH_HIGH -208 (n=32, d=10) · RSI2_DIP -299 (n=100, d=7)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +1259 (n=31, d=16) · DOUBLE_DIP +439 (n=284, d=32) · BOLL_SNAP +396 (n=287, d=29) · STORM_DIP +381 (n=462, d=32) · PANIC_BOUNCE +256 (n=300, d=30) · PANIC_LITE +183 (n=630, d=35) · FRESH_HIGH -67 (n=40, d=20)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **30** entry days — **test LIVE (>=15)**
- PANIC_LITE: **28** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **28** entry days — **test LIVE (>=15)**
- REVERSAL_3: **28** entry days — **test LIVE (>=15)**
- PULLBACK_50: **27** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **25** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **23** entry days — **test LIVE (>=15)**
- DEEP_DIP: **15** entry days — **test LIVE (>=15)**
- TREND_RIDER: **15** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **14** entry days
- SHORT_EXT: **5** entry days
- STORM_DIP: **1** entry days

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+1259 bps, n=31); keep me on a short leash in calm-up (-43). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_BOUNCE to the desk: my weather is storm-down (+256 bps, n=300); keep me on a short leash in calm-up (-16). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-down (+183 bps, n=630); keep me on a short leash in calm-up (+4). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+439 bps, n=284); keep me on a short leash in calm-up (-29). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+381 bps, n=462); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-208). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+366 bps, n=12); keep me on a short leash in storm-up (-526). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+406 bps, n=17); keep me on a short leash in calm-up (-530). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-299). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+112 bps, n=68); keep me on a short leash in calm-up (-46). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+396 bps, n=287); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+254 bps, n=26); keep me on a short leash in calm-up (-32). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
