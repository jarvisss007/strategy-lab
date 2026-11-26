# Arena Roundtable — 2026-11-26

Tape: **storm-down** · session 2026-11-25 · 12 agents · opened 32, closed 79 this session · 186 open · 5194 forward closes all-time

> **This lab is 73% of the desk's scored record (5194 of 7134 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 0 of 186 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 79 closed this session, 5194 all-time. No due rows on the book. This pass ran outside market hours, so every due row was eligible to close.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+767), BOLL_SNAP (+361), PANIC_BOUNCE (+260); cold hands: RSI2_DIP (-100), FRESH_HIGH (-214). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 81% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -23 bps over 1895 trades (t=-1.77) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +104 (n=330, d=92) · SHORT_EXT +14 (n=154, d=56) · BOLL_SNAP -42 (n=373, d=104) · PANIC_LITE -51 (n=1771, d=125) · PANIC_BOUNCE -68 (n=823, d=108) · DOUBLE_DIP -78 (n=702, d=110) · DEEP_DIP -162 (n=117, d=62) · RSI2_DIP -220 (n=218, d=25) · REVERSAL_3 -277 (n=98, d=21) · PULLBACK_50 -390 (n=85, d=22) · TREND_RIDER -462 (n=63, d=22)
- **calm-down**: BOLL_SNAP +224 (n=125, d=23) · REVERSAL_3 +50 (n=54, d=11) · RSI2_DIP -66 (n=117, d=13) · DOUBLE_DIP -111 (n=246, d=26) · PANIC_LITE -124 (n=512, d=27) · PANIC_BOUNCE -160 (n=290, d=24) · PULLBACK_50 -228 (n=37, d=11) · DEEP_DIP -276 (n=32, d=20) · FRESH_HIGH -299 (n=55, d=17) · TREND_RIDER -303 (n=25, d=10)
- **storm-up**: PANIC_LITE +169 (n=97, d=3) · PANIC_BOUNCE +137 (n=67, d=3) · DOUBLE_DIP +130 (n=52, d=3) · BOLL_SNAP -43 (n=22, d=3) · STORM_DIP -294 (n=87, d=3)
- **storm-down**: DEEP_DIP +767 (n=51, d=21) · BOLL_SNAP +361 (n=350, d=34) · PANIC_BOUNCE +260 (n=425, d=36) · DOUBLE_DIP +222 (n=428, d=38) · STORM_DIP +164 (n=618, d=39) · PANIC_LITE +129 (n=811, d=42) · PULLBACK_50 +30 (n=42, d=10) · REVERSAL_3 -74 (n=49, d=9) · RSI2_DIP -100 (n=85, d=11) · FRESH_HIGH -214 (n=44, d=23)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **85** entry days — **test LIVE (>=15)**
- PANIC_LITE: **82** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **76** entry days — **test LIVE (>=15)**
- REVERSAL_3: **75** entry days — **test LIVE (>=15)**
- PULLBACK_50: **75** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **74** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **74** entry days — **test LIVE (>=15)**
- TREND_RIDER: **59** entry days — **test LIVE (>=15)**
- DEEP_DIP: **51** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **43** entry days — **test LIVE (>=15)**
- SHORT_EXT: **21** entry days — **test LIVE (>=15)**
- STORM_DIP: **6** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -361 bps over 51 entry days (row mean -57, n=98) · win rate per entry day 31% (row hit 43%)
- PANIC_BOUNCE: per-entry-day mean -62 bps over 76 entry days (row mean -113, n=715) · win rate per entry day 46% (row hit 44%)
- PANIC_LITE: per-entry-day mean -111 bps over 82 entry days (row mean -136, n=1202) · win rate per entry day 39% (row hit 40%)
- DOUBLE_DIP: per-entry-day mean -141 bps over 74 entry days (row mean -63, n=572) · win rate per entry day 38% (row hit 42%)
- STORM_DIP: per-entry-day mean +180 bps over 6 entry days (row mean +187, n=200) · win rate per entry day 50% (row hit 52%)
- FRESH_HIGH: per-entry-day mean -209 bps over 43 entry days (row mean -181, n=96) · win rate per entry day 37% (row hit 42%)
- SHORT_EXT: per-entry-day mean +221 bps over 21 entry days (row mean +235, n=38) · win rate per entry day 57% (row hit 55%)
- TREND_RIDER: per-entry-day mean -300 bps over 59 entry days (row mean -299, n=156) · win rate per entry day 39% (row hit 41%)
- RSI2_DIP: per-entry-day mean -60 bps over 85 entry days (row mean -74, n=859) · win rate per entry day 38% (row hit 43%)
- REVERSAL_3: per-entry-day mean -28 bps over 75 entry days (row mean -54, n=485) · win rate per entry day 41% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -74 bps over 74 entry days (row mean +80, n=443) · win rate per entry day 43% (row hit 51%)
- PULLBACK_50: per-entry-day mean -88 bps over 75 entry days (row mean -84, n=330) · win rate per entry day 51% (row hit 46%)
- Exits on copied/zero-volume bars: **0** of 4892 forward exits tested; 302 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+767 bps, n=51); keep me on a short leash in calm-down (-276). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+260 bps, n=425); keep me on a short leash in calm-down (-160). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+169 bps, n=97); keep me on a short leash in calm-down (-124). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-down (+222 bps, n=428); keep me on a short leash in calm-down (-111). Status: DEAD — loses to costs/SPY.
- STORM_DIP to the desk: my weather is storm-down (+164 bps, n=618); keep me on a short leash in storm-up (-294). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+954 bps, n=10); keep me on a short leash in calm-down (-299). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+615 bps, n=9); keep me on a short leash in calm-up (+14). Status: WATCH — positive but not significant.
- TREND_RIDER to the desk: my weather is storm-down (-158 bps, n=11); keep me on a short leash in calm-up (-462). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (-66 bps, n=117); keep me on a short leash in calm-up (-220). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+50 bps, n=54); keep me on a short leash in calm-up (-277). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+361 bps, n=350); keep me on a short leash in storm-up (-43). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (+30 bps, n=42); keep me on a short leash in calm-up (-390). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
