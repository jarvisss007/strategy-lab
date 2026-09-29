# Arena Roundtable — 2026-09-29

Tape: **calm-up** · session 2026-09-29 · 12 agents · opened 43, closed 66 this session · 169 open · 2556 forward closes all-time

> **This lab is 69% of the desk's scored record (2492 of 3604 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 169 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 66 closed this session, 2556 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+202), DEEP_DIP (+25), PULLBACK_50 (+12); cold hands: RSI2_DIP (-45), TREND_RIDER (-227). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 44% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +38 bps over 1648 trades (t=2.73) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +202 (n=428, d=108) · DEEP_DIP +25 (n=115, d=71) · PULLBACK_50 +12 (n=172, d=37) · PANIC_LITE -4 (n=1916, d=144) · REVERSAL_3 -12 (n=204, d=38) · PANIC_BOUNCE -19 (n=937, d=125) · BOLL_SNAP -29 (n=379, d=118) · SHORT_EXT -32 (n=185, d=72) · DOUBLE_DIP -37 (n=784, d=125) · RSI2_DIP -45 (n=408, d=40) · TREND_RIDER -227 (n=93, d=31)
- **calm-down**: BOLL_SNAP +310 (n=69, d=13) · TREND_RIDER +298 (n=23, d=9) · PANIC_BOUNCE +156 (n=137, d=14) · PANIC_LITE +120 (n=247, d=15) · PULLBACK_50 +119 (n=45, d=10) · DOUBLE_DIP +108 (n=123, d=15) · REVERSAL_3 +36 (n=79, d=8) · RSI2_DIP -212 (n=151, d=10) · FRESH_HIGH -250 (n=32, d=11)
- **storm-up**: PANIC_LITE +174 (n=95, d=4) · PANIC_BOUNCE +142 (n=67, d=4) · DOUBLE_DIP +138 (n=51, d=4) · BOLL_SNAP -74 (n=21, d=4) · STORM_DIP -291 (n=87, d=4)
- **storm-down**: DEEP_DIP +845 (n=27, d=15) · DOUBLE_DIP +393 (n=256, d=30) · BOLL_SNAP +384 (n=247, d=27) · STORM_DIP +348 (n=418, d=31) · PANIC_BOUNCE +189 (n=262, d=29) · PANIC_LITE +137 (n=567, d=34) · FRESH_HIGH -148 (n=36, d=19)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **44** entry days — **test LIVE (>=15)**
- PANIC_LITE: **42** entry days — **test LIVE (>=15)**
- REVERSAL_3: **41** entry days — **test LIVE (>=15)**
- PULLBACK_50: **41** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **39** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **37** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **36** entry days — **test LIVE (>=15)**
- TREND_RIDER: **25** entry days — **test LIVE (>=15)**
- DEEP_DIP: **23** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **20** entry days — **test LIVE (>=15)**
- SHORT_EXT: **10** entry days
- STORM_DIP: **1** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean +440 bps over 23 entry days (row mean +748, n=50) · win rate per entry day 56% (row hit 70%)
- PANIC_BOUNCE: per-entry-day mean +115 bps over 39 entry days (row mean +58, n=316) · win rate per entry day 59% (row hit 52%)
- PANIC_LITE: per-entry-day mean +22 bps over 42 entry days (row mean +5, n=607) · win rate per entry day 48% (row hit 46%)
- DOUBLE_DIP: per-entry-day mean +59 bps over 37 entry days (row mean +87, n=254) · win rate per entry day 49% (row hit 52%)
- STORM_DIP: per-entry-day mean +1217 bps over 1 entry day - one event, no inference (row mean +1217, n=40) · win rate per entry day 100% (row hit 90%)
- FRESH_HIGH: per-entry-day mean -171 bps over 20 entry days (row mean -97, n=49) · win rate per entry day 45% (row hit 41%)
- SHORT_EXT: per-entry-day mean +110 bps over 10 entry days (row mean +244, n=23) · win rate per entry day 50% (row hit 56%)
- TREND_RIDER: per-entry-day mean -86 bps over 25 entry days (row mean -93, n=71) · win rate per entry day 44% (row hit 48%)
- RSI2_DIP: per-entry-day mean +21 bps over 44 entry days (row mean -4, n=488) · win rate per entry day 43% (row hit 44%)
- REVERSAL_3: per-entry-day mean +22 bps over 41 entry days (row mean +13, n=289) · win rate per entry day 42% (row hit 47%)
- BOLL_SNAP: per-entry-day mean +40 bps over 36 entry days (row mean +259, n=174) · win rate per entry day 56% (row hit 59%)
- PULLBACK_50: per-entry-day mean +53 bps over 41 entry days (row mean +67, n=195) · win rate per entry day 61% (row hit 53%)
- Exits on copied/zero-volume bars: **0** of 2394 forward exits tested; 162 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is calm-down (+881 bps, n=12); keep me on a short leash in calm-up (+25). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-19). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (-4). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-37). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-250). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+611 bps, n=10); keep me on a short leash in calm-up (-32). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+298 bps, n=23); keep me on a short leash in calm-up (-227). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-212). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+36 bps, n=79); keep me on a short leash in calm-up (-12). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+119 bps, n=45); keep me on a short leash in calm-up (+12). Status: WATCH — positive but not significant.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
