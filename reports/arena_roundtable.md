# Arena Roundtable — 2026-09-22

Tape: **calm-up** · session 2026-09-21 · 12 agents · opened 31, closed 52 this session · 140 open · 2288 forward closes all-time

> **This lab is 69% of the desk's scored record (2288 of 3298 scored rows in the Calibration Observatory).** Any pooled desk statistic is therefore mostly a statement about the Arena, not about the desk. Read the other labs' standings on their own n.

**Drain (ARENA-003).** 43 of 140 open rows read `days_left <= 0`; 0 of those are PAST due (negative). 52 closed this session, 2288 all-time. Oldest due row: PULLBACK_50 KO, entered 2026-09-15, hold 5, days_left 0. Exits are suppressed during market hours by the fill-integrity gate, so a due row right now is waiting for the next non-intraday pass, not stuck.

- Tape today: CALM-UP. Our pooled record in this weather — hot hands: FRESH_HIGH (+183), DEEP_DIP (+15), PULLBACK_50 (+1); cold hands: RSI2_DIP (-71), TREND_RIDER (-190). (History, not prophecy.)
- FRESH_HIGH and SHORT_EXT enter on the same bar 45% of the time — one trade, two directions. The pooled ledger says the long side wins that argument; the skeptic keeps paying for the lesson.
- PANIC_LITE contains 84% of PANIC_BOUNCE's entries; stripped to the −3%…−5% band alone (PANIC_LITE entries too shallow for PANIC_BOUNCE), it still earned +39 bps over 1608 trades (t=2.75) — the bounce is not only in the extreme tail.
- Desk rule we all share: reading each other's regime stats and gating ourselves in hindsight is selection bias — STORM_DIP is the only pre-registered regime gate; any new gate goes to REGISTRY.md with a thesis BEFORE it trades.

## Playbook by regime (avg bps/trade, n>=20)

_Read n_events, not n: `n` counts rows, `d` counts the distinct entry DAYS behind them. Rows on one day share a regime and are one observation, not many (Firm Brain #4)._

- **calm-up**: FRESH_HIGH +183 (n=445, d=113) · DEEP_DIP +15 (n=115, d=70) · PULLBACK_50 +1 (n=192, d=38) · PANIC_LITE -3 (n=1876, d=145) · PANIC_BOUNCE -21 (n=932, d=125) · BOLL_SNAP -32 (n=364, d=118) · DOUBLE_DIP -37 (n=772, d=127) · REVERSAL_3 -38 (n=220, d=39) · SHORT_EXT -39 (n=190, d=74) · RSI2_DIP -71 (n=427, d=40) · TREND_RIDER -190 (n=93, d=31)
- **calm-down**: TREND_RIDER +382 (n=24, d=10) · BOLL_SNAP +310 (n=69, d=13) · PULLBACK_50 +145 (n=42, d=10) · PANIC_BOUNCE +136 (n=135, d=14) · DOUBLE_DIP +108 (n=123, d=15) · PANIC_LITE +101 (n=241, d=15) · REVERSAL_3 +95 (n=86, d=8) · RSI2_DIP -183 (n=153, d=10) · FRESH_HIGH -199 (n=32, d=11)
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

- DEEP_DIP to the desk: my weather is calm-down (+993 bps, n=11); keep me on a short leash in calm-up (+15). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_BOUNCE to the desk: my weather is storm-down (+189 bps, n=262); keep me on a short leash in calm-up (-21). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PANIC_LITE to the desk: my weather is storm-up (+174 bps, n=95); keep me on a short leash in calm-up (-3). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- DOUBLE_DIP to the desk: my weather is storm-down (+393 bps, n=256); keep me on a short leash in calm-up (-37). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- STORM_DIP to the desk: my weather is storm-down (+348 bps, n=418); keep me on a short leash in storm-up (-291). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- FRESH_HIGH to the desk: my weather is storm-up (+688 bps, n=13); keep me on a short leash in calm-down (-199). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- SHORT_EXT to the desk: my weather is storm-down (+611 bps, n=10); keep me on a short leash in calm-up (-39). Status: DEAD — loses to costs/SPY.
- TREND_RIDER to the desk: my weather is calm-down (+382 bps, n=24); keep me on a short leash in calm-up (-190). Status: DEAD — loses to costs/SPY.
- RSI2_DIP to the desk: my weather is storm-down (+497 bps, n=9); keep me on a short leash in calm-down (-183). Status: DEAD — loses to costs/SPY.
- REVERSAL_3 to the desk: my weather is calm-down (+95 bps, n=86); keep me on a short leash in calm-up (-38). Status: DEAD — loses to costs/SPY.
- BOLL_SNAP to the desk: my weather is storm-down (+384 bps, n=247); keep me on a short leash in storm-up (-74). Status: UNPROVEN — FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474).
- PULLBACK_50 to the desk: my weather is calm-down (+145 bps, n=42); keep me on a short leash in calm-up (+1). Status: WATCH — positive but not significant.

Calibration experiment, not advice. Forward book + deflation gate decide; the replay only suggests.

## ARENA-007 — S17 and S18 answered (labs-morning-sweep, 2026-09-22)

- **S17 (one vote per entry day): answered — the row denominator inflates this book's t by 3.89×.** The 2,288 closed rows are **39 entry days**; row-weighted mean excess **+31.1 bps, t = +2.13**, but one vote per entry day gives **+21.9 bps, t = +0.55** — nothing. Per rule (rows / days / row bps / day bps / day t): RSI2_DIP 431/38 −33.9/−7.0/−0.14 · PANIC_LITE 531/36 −20.1/+0.6/+0.01 · REVERSAL_3 269/36 +8.9/+26.0/+0.56 · PULLBACK_50 173/35 +37.2/+16.6/+0.24 · PANIC_BOUNCE 297/34 +25.1/+72.8/+0.64 · DOUBLE_DIP 241/33 +43.6/+47.5/+0.67 · BOLL_SNAP 144/31 **+207.3 → +22.3**/+0.32 · TREND_RIDER 56/21 −282.1/−217.9/−1.55 · DEEP_DIP 42/18 +539.5/+289.6/+1.20 · FRESH_HIGH 44/17 −181.7/−247.5/−1.71 · SHORT_EXT 20/9 +379.7/+194.6/+0.75 · **STORM_DIP 40/1 +829.9/+829.9/t = nan — one entry day has no standard error at all.** Not one rule clears |t| = 2 on its own entry days.
- **S18 (exits on copied / zero rows): answered — small but real, and the signature is copied prices, not zero moves.** **5 of 2,288** closed rows exit at **exactly** their entry price (PANIC_BOUNCE/PANIC_LITE QBTS 16.21 08-11→08-13, PANIC_BOUNCE/PANIC_LITE CTMX 3.29 08-20→08-24, PANIC_LITE SOUN 5.93 09-16→09-18), each booking net −0.002, i.e. pure cost against a price that did not move. The louder finding is **7 ticker+exit-price pairs that recur on different exit dates** — **QBTS at 16.21 on 08-03, 08-11, 08-13 and 08-17**, plus IREN 39.75, CTMX 3.32, CTMX 3.29, XYZ 79.07, ABBV 261.70. An identical print on four separate exit dates is the carry-forward signature of **Firm Brain §18 — a later bar is not a traded bar** — and the exit loader does not check whether the exit bar traded. **0.2% of rows by count**; no rule's sign turns on it.
- **NEW THREAD, proposed only — a rule with a single entry day does not belong in the live forward book.** STORM_DIP has **1 entry day** carrying 40 rows and **+829.9 bps**, and its day-clustered t is literally `nan`: one observation cannot produce a standard error, so no amount of further rows from that day can ever make it readable. That is the same condition EVO-010 proposes for EV-13/EV-15 — **structurally unreadable**, not merely unproven. SHORT_EXT (9 entry days, already `DEAD — loses to costs/SPY`) is the nearest neighbour. **Proposal, not a change: record STORM_DIP as structurally unreadable and quote it with `n_events = 1` wherever its P&L appears. No rule frozen, retired, paused or re-registered by this run** — that is Anupam's ruling.
- **Disclosure about this section itself:** `arena_roundtable.md` is regenerated by `arena.py` on every run, so these three lines are erased the next time the arena fires. Making the answer durable means teaching the generator to emit it, which is a change to a registered lab's reporting and therefore a ruling, not a sweep's side effect (REG-PP-001). Reported, not made.
