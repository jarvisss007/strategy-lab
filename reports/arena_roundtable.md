# Arena Roundtable — 2026-11-25

Tape: **storm-down** · session 2026-11-24 · 12 agents · opened 107, closed 118 this session · 233 open · 5115 forward closes all-time

> **This lab is 73% of the desk's scored record (5115 of 7049 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 77 of 233 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 118 closed this session, 5115 all-time. Oldest due row: TREND_RIDER AMZN, entered 2026-11-04, hold 15, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: STORM-DOWN. Our pooled record in this weather — hot hands: DEEP_DIP (+648), BOLL_SNAP (+302), PANIC_BOUNCE (+244); cold hands: RSI2_DIP (-123), FRESH_HIGH (-222). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 44% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 81% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned -32 bps over 1894 trades (t=-2.41) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +112 (n=331, d=94) · SHORT_EXT +17 (n=156, d=56) · BOLL_SNAP -44 (n=373, d=105) · PANIC_LITE -55 (n=1783, d=126) · PANIC_BOUNCE -72 (n=836, d=109) · DOUBLE_DIP -75 (n=706, d=111) · DEEP_DIP -150 (n=118, d=63) · RSI2_DIP -220 (n=218, d=25) · REVERSAL_3 -277 (n=98, d=21) · PULLBACK_50 -395 (n=84, d=22) · TREND_RIDER -462 (n=63, d=22)
- **calm-down**: BOLL_SNAP +224 (n=125, d=23) · REVERSAL_3 +46 (n=57, d=12) · RSI2_DIP -16 (n=132, d=14) · DOUBLE_DIP -111 (n=246, d=26) · PANIC_LITE -124 (n=512, d=27) · PANIC_BOUNCE -160 (n=290, d=24) · PULLBACK_50 -238 (n=40, d=12) · FRESH_HIGH -281 (n=54, d=17) · TREND_RIDER -288 (n=28, d=11) · DEEP_DIP -318 (n=32, d=20)
- **storm-up**: PANIC_LITE +169 (n=97, d=3) · PANIC_BOUNCE +137 (n=67, d=3) · DOUBLE_DIP +130 (n=52, d=3) · BOLL_SNAP -43 (n=22, d=3) · STORM_DIP -294 (n=87, d=3)
- **storm-down**: DEEP_DIP +648 (n=50, d=20) · BOLL_SNAP +302 (n=352, d=35) · PANIC_BOUNCE +244 (n=421, d=36) · DOUBLE_DIP +129 (n=428, d=38) · PANIC_LITE +103 (n=805, d=42) · STORM_DIP +74 (n=618, d=39) · PULLBACK_50 -46 (n=42, d=10) · REVERSAL_3 -74 (n=49, d=9) · RSI2_DIP -123 (n=85, d=11) · FRESH_HIGH -222 (n=45, d=23)

## Forward entry days per strategy (coach's 15-day retirement test)

Entry DAYS, not trades — same-day entries share one regime and are one observation. The coach's standing test fires at 15.

- RSI2_DIP: **84** entry days — **test LIVE (>=15)**
- PANIC_LITE: **82** entry days — **test LIVE (>=15)**
- PANIC_BOUNCE: **76** entry days — **test LIVE (>=15)**
- REVERSAL_3: **74** entry days — **test LIVE (>=15)**
- PULLBACK_50: **74** entry days — **test LIVE (>=15)**
- DOUBLE_DIP: **73** entry days — **test LIVE (>=15)**
- BOLL_SNAP: **73** entry days — **test LIVE (>=15)**
- TREND_RIDER: **58** entry days — **test LIVE (>=15)**
- DEEP_DIP: **51** entry days — **test LIVE (>=15)**
- FRESH_HIGH: **43** entry days — **test LIVE (>=15)**
- SHORT_EXT: **21** entry days — **test LIVE (>=15)**
- STORM_DIP: **5** entry days

## One vote per entry day: council S17 / S18 / S20 (forward book)

_Rows that share an entry date share one tape (Firm Brain #4). S17: each entry day's mean counts once, however many rows it opened. S20: the share of entry days that made money, beside the row hit rate. S18: forward exits priced on a copied or zero-volume bar (open = close = the prior close, or no volume: a carry-forward print, Firm Brain #18)._

- DEEP_DIP: per-entry-day mean -361 bps over 51 entry days (row mean -57, n=98) · win rate per entry day 31% (row hit 43%)
- PANIC_BOUNCE: per-entry-day mean -62 bps over 76 entry days (row mean -113, n=715) · win rate per entry day 46% (row hit 44%)
- PANIC_LITE: per-entry-day mean -111 bps over 82 entry days (row mean -136, n=1202) · win rate per entry day 39% (row hit 40%)
- DOUBLE_DIP: per-entry-day mean -150 bps over 73 entry days (row mean -78, n=558) · win rate per entry day 37% (row hit 41%)
- STORM_DIP: per-entry-day mean +139 bps over 5 entry days (row mean +172, n=186) · win rate per entry day 40% (row hit 51%)
- FRESH_HIGH: per-entry-day mean -209 bps over 43 entry days (row mean -181, n=96) · win rate per entry day 37% (row hit 42%)
- SHORT_EXT: per-entry-day mean +221 bps over 21 entry days (row mean +235, n=38) · win rate per entry day 57% (row hit 55%)
- TREND_RIDER: per-entry-day mean -296 bps over 58 entry days (row mean -287, n=149) · win rate per entry day 40% (row hit 42%)
- RSI2_DIP: per-entry-day mean -65 bps over 84 entry days (row mean -80, n=846) · win rate per entry day 37% (row hit 42%)
- REVERSAL_3: per-entry-day mean -33 bps over 74 entry days (row mean -55, n=484) · win rate per entry day 40% (row hit 44%)
- BOLL_SNAP: per-entry-day mean -82 bps over 73 entry days (row mean +58, n=420) · win rate per entry day 42% (row hit 49%)
- PULLBACK_50: per-entry-day mean -92 bps over 74 entry days (row mean -90, n=323) · win rate per entry day 50% (row hit 46%)
- Exits on copied/zero-volume bars: **0** of 4892 forward exits tested; 223 exit(s) have no bar in data/open, close and volume.csv to test, counted untested, not clean

## Notes to the desk

- DEEP_DIP to the desk: my weather is storm-down (+648 bps, n=50); keep me on a short leash in calm-down (-318). Status: DEAD — loses to costs/SPY.
- PANIC_BOUNCE to the desk: my weather is storm-down (+244 bps, n=421); keep me on a short leash in calm-down (-160). Status: DEAD — loses to costs/SPY.
- PANIC_LITE to the desk: my weather is storm-up (+169 bps, n=97); keep me on a short leash in calm-down (-124). Status: DEAD — loses to costs/SPY.
- DOUBLE_DIP to the desk: my weather is storm-up (+130 bps, n=52); keep me on a short leash in calm-down (-111). Status: DEAD — loses to costs/SPY.
- STORM_DIP to the desk: my weather is storm-down (+74 bps, n=618); keep me on a short leash in storm-up (-294). Status: WATCH — positive but not significant.
- FRESH_HIGH to the desk: my weather is storm-up (+954 bps, n=10); keep me on a short leash in calm-down (-281). Status: WATCH — positive but not significant.
- SHORT_EXT to the desk: my weather is storm-down (+522 bps, n=10); keep me on a short leash in calm-up (+17). Status: WATCH — positive but not significant.
- TREND_RIDER to the desk: my weather is calm-down (-288 bps, n=28); keep me on a short leash in calm-up (-462). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is calm-down (-16 bps, n=132); keep me on a short leash in calm-up (-220). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+46 bps, n=57); keep me on a short leash in calm-up (-277). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+302 bps, n=352); keep me on a short leash in calm-up (-44). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is storm-down (-46 bps, n=42); keep me on a short leash in calm-up (-395). Status: DEAD — loses to costs/SPY.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.
