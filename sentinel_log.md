# Research Sentinel Log

date · registry-clean? · drift? · zdte n/60 · crypto days/skill · insider events

2026-08-15 · clean (6/6 families match REGISTRY.md) · **NO DRIFT on the 5 genuinely new sessions — and a RETRACTION of the drift called on 08-01 and 08-08.** Two findings, both about measurement rather than markets. (1) PIPELINE, third variant of the same bug: the Monday fetch fires ~06:23 PT, five minutes BEFORE the 06:30 cash open, so the union date axis gained a 2026-08-10 row in which only ES=F and NQ=F had traded — 142 of 144 equity columns blank. The equity panel therefore still ended 2026-08-07, exactly where 08-08 left it, and this week's first discover.py run was arithmetic on last week's data (its numbers reproduce 08-08 to two decimals). Fixed: new panel_guard.py trims trailing dates below 80% universe coverage, same posture and threshold as fetch_data.py's existing abort guard, tail-only so interior gaps survive; wired into all three fetchers and unit-tested. Panels refetched to 2026-08-14 and discover.py re-run, so discoveries.csv holds TWO 2026-08-15 blocks — **use the second** (bench 1.28). (2) The re-run's apparent drift is NOT out-of-sample evidence. `_xs` sets its rebalance grid as `np.arange(len(score)) // H` — keyed to POSITIONAL index — while `range=15y` rolls the window start every week, so each refresh re-phases the 21-day grid across all 15 years. Isolating the two changes: dropping the 5 front days alone moved high-volume-premium q0.1 H21 OOS +0.75 → −0.03 and confluence-fade q0.1 H21 OOS +0.34 → −0.99, while the 5 NEW sessions moved them 0.03 and 0.01. A 21-offset phase sweep on identical data: high-volume-premium q0.1 H21 net spans −0.50..+0.43 (OOS −0.40..+0.74, 14 of 21 phases positive); value-area-fade q0.1 H21 net −0.38..+0.14, median −0.06 — it straddles the dead/real-but-loses boundary, so **the "value-area fade → DEAD" call logged 08-01 and 08-08 is withdrawn as unestablished**; confluence-fade q0.1 H21 net −1.09..+0.23. 20 of ~32 configs sit on this positional grid; illiquidity-premium q0.2 (also _xs H21) barely moves, because its 21-day rolling signal is slow — the defect bites fast signals. Headline families unaffected: turn-of-month is calendar-keyed and sat at net 1.13→1.14 / OOS 1.19→1.21 across every variant tested. Turn-of-month t5 still real-but-loses (net 1.14 vs bench 1.28), so no MC drawdown run. SUGGESTION for sign-off, not actioned: anchor `reb` to a fixed calendar epoch rather than row 0, and report H-config Sharpes as a median across phases — both change registered numbers, so they are Anupam's call under REGISTRY.md rule 1. · zdte 21/60 (+5) · crypto 42 CSV days (+7), skill −0.031, edge_found=false, gross −0.195 bps/trade against 60 bps costs; learned_weights.json rebuilt 08-11 from 38 days — **last week's FOSSIL finding is resolved** · insider rolling feed 400, but collector_edgar.py sets KEEP=400, so the counter is **saturated at its cap** and cannot express accrual (198→400 is the cap refilling); the deep sample events.json is still 1,062, untouched since 2026-07-07, so the "double to 2,124" milestone remains unfireable as instrumented

2026-07-25 · clean (6/6 families match REGISTRY.md) · no drift (all verdicts match 2026-07-11 frozen table; discoveries.csv row identical to 2026-07-18 run) · zdte 7/60 (first log, no prior baseline) · crypto 21 days, skill -0.031, edge_found=false (first log, no prior baseline) · insider 392 events (first log, no prior baseline)

2026-07-26 · clean (6/6 families match REGISTRY.md) · no drift (all 6 verdicts identical to the 2026-07-11 frozen table; 0 survivors, best DSR still t5 = 1.0 / PBO 0.01) · zdte 7/60 (+0) · crypto 22 days, skill -0.031, edge_found=false (+1 day) · insider 392 events (+0)

2026-08-08 · clean (6/6 families match REGISTRY.md) · **DRIFT CONFIRMED: Price-action value-area fade real-but-loses → DEAD** for the 2nd straight week, now on genuinely refreshed data (best net −0.07, OOS −0.29, DSR 0.09) — the 2026-08-01 call holds. No other category drift; material but non-category moves: overnight net −0.22 → −0.44, illiquidity q0.2 net 0.64 → 0.86 / OOS 1.10 → 1.35. Turn-of-month t5 still real-but-loses (net 1.13 vs bench 1.27), so no MC drawdown run. · **PIPELINE: last week's fix was never wired in** — fetch_ohlc.py/fetch_volume.py were still absent from refresh_all.sh, so panels sat at 2026-07-31; ALSO prices.csv+meta.json were destroyed 2026-08-03 when a DNS outage made every ticker fail and fetch_data.py truncated before checking. Both repaired this run: the two fetchers added to the Monday branch, and fetch_data.py now aborts rather than overwrite when <80% of the universe fetches. Panels refreshed to 2026-08-07. · **CAVEAT: universe grew 119 → 144 tickers**, and the 15y window rolls (start 2011-07-25 → 2011-08-08), so week-over-week deltas mix new dates with new constituents and a dropped front — not clean OOS · zdte 16/60 (+4) · crypto 35 CSV days (+7), skill −0.031, edge_found=false — but learned_weights.json is FOSSIL: last built 2026-07-25 from 21 days, the collector's --backtest-every hook has not rewritten it in 14 days · insider 198 in the rolling feed (was 400 — **the spec's counter is a ~11-day rolling window, not accrual**; the deep sample events.json is frozen at 1,062 since 2026-07-07, so the "double to 2,124" milestone cannot fire from any live pipeline)

2026-08-01 · clean (6/6 families match REGISTRY.md) · **DRIFT: Price-action value-area fade real-but-loses → DEAD** (best net 0.08 → −0.04, PBO 0.05 → 0.43); Options-expiry best config flipped pre-opex → post-opex, PBO 0.54 → 0.69 · **PIPELINE FIX: open/close/volume.csv were frozen at 2026-07-07** — fetch_ohlc.py + fetch_volume.py are absent from refresh_all.sh (its Monday branch runs only fetch_data.py, which writes prices.csv, a different file). Every "no drift" since 2026-07-11 was arithmetic on a static panel, not evidence. Panels refreshed manually this run → 2026-07-31; discoveries.csv therefore holds TWO 2026-08-01 blocks (first = stale panel, second = refreshed; use the second). Rolling 15y window means the refresh added ~17 days and dropped ~16 off the front — not purely additive · zdte 12/60 (+5) · crypto 28 CSV days (+6), skill −0.031, edge_found=false (learned_weights.json itself stale, last built from data through 2026-07-25) · insider 400 events (+8)

2026-08-22 · clean (6/6 families in discover.py's FAMILIES match REGISTRY.md; no unregistered family, no new config) · **NO DRIFT ATTRIBUTABLE TO NEW DATA — and the cleanest attribution the sentinel has managed yet.** Two findings. (1) PIPELINE, fourth variant, this one a SCHEDULING mismatch rather than a bug: the Monday fetch fires 06:20 PT and correctly returns data through the prior Friday, so the Monday 08-17 run produced a panel ending 2026-08-14 — byte-for-byte the same extent last week's manual Saturday refetch already reached. The sentinel runs Saturdays; as wired, it therefore re-validates on a panel that is missing the five sessions of the week just ended, EVERY week. This run's first discover.py pass was consequently arithmetic on last week's panel again (every row reproduces 08-15 to two decimals). Panels refetched here to 2026-08-21 (universe 144 → 145 cols, window start rolled 2011-08-15 → 2011-08-22) and discover.py re-run, so discoveries.csv holds TWO 2026-08-22 blocks — **use the second** (bench 1.26). (2) With genuinely new sessions finally in hand, the new-data effect was ISOLATED from the window-roll effect by re-running every family on the refreshed front truncated back to the 08-14 end: **the 5 new sessions (08-17..08-21) moved every family's best-config net Sharpe by ≤0.03 and OOS by ≤0.08 — nothing.** All week-over-week movement is the rolled front re-phasing the positional `np.arange(len(score)) // H` rebalance grid, the defect diagnosed 08-15. Worked examples: high-volume-premium q0.1 H21 net −0.16 → −0.51 with the new sessions contributing 0.00; value-area-fade best-config identity flipped q0.2 H10 → q0.2 H21 with the new sessions contributing −0.01. Value-area fade therefore prints **dead** again (best net −0.20, DSR 0.08, PBO 0.74 → 0.35) — this is a category difference vs the FROZEN registry row (real-but-loses), but it remains the WITHDRAWN, unestablished call: the family straddles the net=0 dead/real-but-loses boundary by construction (08-15 phase sweep: net −0.38..+0.14, median −0.06), and the boundary, not the market, is what moved. Options-expiry PBO 0.54 (frozen) → 0.70, best config still post-opex-week, category unchanged. Turn-of-month t5 still real-but-loses (net 1.12 vs bench 1.26), so no MC drawdown run. Nothing crossed DSR 0.5/0.95. SUGGESTION for sign-off, not actioned: refresh the panels INSIDE the sentinel run (or move the fetch to Friday post-close) so the weekly re-validation consumes the week that just ended — a scheduling change only, no hypothesis or parameter touched; the 08-15 SUGGESTION (anchor `reb` to a fixed calendar epoch, report H-config Sharpes as a median across phases) is now supported by a second week of evidence and still awaits Anupam's call under rule 1. · zdte 26/60 (+5) · crypto 48 derived minute-days 07-05..08-21 (+6); **the spec's counter is broken, not the data** — CRYP-005/rotate.py gzips raw days and keeps only a 30-day local buffer, so `research/data/BTC-USD_*.csv` now matches 1 file (34 are .csv.gz); the honest source is research/minutes/. learned_weights.json is **FOSSIL AGAIN** (mtime 2026-08-11, built from 38 days ending 08-11, 10 accrued days unincorporated) — last week's "resolved" was a one-off rebuild, not a working hook; its frozen figures: skill −0.031, edge_found=false, edge_z −3.67, gross −0.195 bps/trade vs 60 bps costs · insider rolling feed 400 = the KEEP=400 cap, still saturated and structurally unable to express accrual; deep-sample events.json 1,062, untouched since 2026-07-07, so the "double to 2,124" milestone stays unfireable as instrumented

2026-08-29 · clean (6/6 families in discover.py's FAMILIES match REGISTRY.md; no unregistered family, no new config) · **NO DRIFT ATTRIBUTABLE TO NEW DATA — third consecutive week the attribution lands the same way.** (1) PIPELINE, the scheduling mismatch again, now confirmed as a STANDING weekly condition rather than an incident: the Monday fetch fired 08-24 06:20 PT and correctly returned data through Friday 08-21 — byte-for-byte the extent last week's manual Saturday refetch already reached. This run's first discover.py pass therefore reproduced the 08-22 block to two decimals on all 34 configs (verified row by row, not eyeballed). The wiring is not broken — fetch_data/fetch_ohlc/fetch_volume are all present in refresh_all.sh's Monday branch, the 08-08 fix holding — it is purely that a Monday fetch cannot contain the week it opens, and the sentinel runs Saturdays. Panels refetched here to 2026-08-28 (window start rolled 2011-08-22 → 2011-08-29, 147 tickers, SPCX still the lone failure) and discover.py re-run, so discoveries.csv holds TWO 2026-08-29 blocks — **use the second** (bench 1.26). (2) New-data effect isolated from window-roll effect by the 08-22 method (re-run every family on the refreshed front truncated back to the 08-21 end): **the 5 new sessions (08-24..08-28) moved every family's best-config net Sharpe by ≤0.02 and OOS by ≤0.05 — nothing.** Two category-level flips printed this week and BOTH are the rolled front, not the market: Price-action value-area fade dead → real-but-loses (best net −0.20 → +0.16, DSR 0.08 → 0.31, PBO 0.35 → 0.04) with the new sessions contributing 0.00 net / +0.01 OOS; and inside microstructure, high-volume-premium q0.1 H21 net −0.51 → +0.31 (a 0.82 swing) with the new sessions contributing −0.02. Both are the positional-rebalance re-phasing diagnosed 08-15. Note the direction: value-area fade has now printed dead (08-01, 08-08, 08-22) and real-but-loses (08-29) on the same frozen hypothesis, which is exactly what the 08-15 phase sweep predicted for a family whose net straddles zero (span −0.38..+0.14, median −0.06) — this run agreeing with the FROZEN registry row is phase luck, not confirmation, and the 08-15 withdrawal stands. Options-expiry unchanged in category, DSR 0.89 → 0.91, PBO 0.70 → 0.65, best config still post-opex-week. Turn-of-month t5 still real-but-loses (net 1.13 vs bench 1.26), so no MC drawdown run. Nothing crossed DSR 0.5 or 0.95. SUGGESTIONS still awaiting sign-off under rule 1, both now with three weeks of supporting evidence and neither actioned: (a) anchor `reb` to a fixed calendar epoch and report H-config Sharpes as a median across phases (08-15), (b) refresh panels inside the sentinel run or move the fetch to Friday post-close so the weekly re-validation consumes the week that just ended (08-22). · zdte 31/60 (+5), recorder healthy through SPY_2026-08-28.csv — over half way, ~6 weeks to the B-L density study at this rate · crypto 55 derived minute-days 07-05..08-28 (+7); the spec's `research/data/BTC-USD_*.csv` counter still reads 1 because rotate.py gzips (30 .csv.gz) — honest source is research/minutes/. learned_weights.json is **FOSSIL for the third straight week** (mtime 2026-08-11, built from 38 days ending 08-11; 17 accrued days unincorporated) — the 08-15 "resolved" was a one-off rebuild, not a working --backtest-every hook, and this is now the longest-standing unfixed instrumentation defect on the desk; its frozen figures: skill −0.031, edge_found=false, edge_z −3.67, hit 49.12% vs naive 49.98% against 60 bps costs · insider rolling feed 400 = the KEEP=400 cap, saturated and structurally unable to express accrual; deep-sample events.json 1,062, untouched since 2026-07-07, so the "double to 2,124" milestone stays unfireable as instrumented

2026-09-05 · clean (6/6 families in discover.py's FAMILIES match REGISTRY.md; no unregistered family, no new config) · **NO DRIFT — and for the first time in five weeks no category flip printed at all: all six verdicts match the FROZEN 2026-07-11 table exactly** (overnight structural-but-uncostable · opex real-but-loses DSR 0.91 PBO 0.62 · turn-of-month t5 real-but-loses DSR 1.0 PBO 0.06 · microstructure real-but-loses, best illiquidity q0.2 DSR 0.14 · value-area fade real-but-loses DSR 0.18 · confluence dead). Nothing crossed DSR 0.5 or 0.95. Turn-of-month t5 net 1.17 vs bench 1.29 — still not a SURVIVOR, so no MC drawdown run. (1) PIPELINE: the Saturday-vs-Monday scheduling mismatch is a standing weekly condition for the fourth straight week — the Monday 08-31 06:26 fetch correctly returned through Friday 08-28, so as wired the sentinel would again have re-validated on a panel missing the week just ended. Panels were refetched FIRST this run (before any discover.py pass) rather than run-then-refetch-then-rerun, so **discoveries.csv holds exactly ONE 2026-09-05 block** — no "use the second" caveat this week. Panel now 2026-09-06..2026-09-04, 145 cols, window start rolled 2011-08-29 → 2011-09-06, SPCX still the lone fetch failure. (2) New-data effect isolated from window-roll effect by the 08-22 method (re-run every family on the refreshed panel truncated back to the 08-28 end): **the 5 new sessions (08-31..09-04) moved every config's net Sharpe by ≤0.02 and OOS by ≤0.05 — nothing; only SPY overnight moved at all (net −0.01, OOS −0.05).** Fourth consecutive week the attribution lands identically. Fourteen configs moved >0.2 week-over-week and every one of them is the rolled front re-phasing the positional `np.arange(len(score)) // H` grid diagnosed 08-15: high-volume-premium q0.2 H21 net +0.11 → +0.51 / OOS +0.12 → +0.80, confluence-fade q0.1 H21 net −0.17 → −0.64, value-area-fade best-config identity flipped q0.2 H21 → q0.1 H21 (DSR 0.31 → 0.18) — all with the new sessions contributing ≈0.00. Value-area fade agreeing with the frozen row this week is phase luck, not confirmation; the 08-15 withdrawal of the dead/real-but-loses call stands. SUGGESTIONS still awaiting sign-off under rule 1, neither actioned, now with four weeks of evidence: (a) anchor `reb` to a fixed calendar epoch and report H-config Sharpes as a median across phases (08-15), (b) refresh panels inside the sentinel run or move the fetch to Friday post-close (08-22) — the sentinel has now done (b) by hand four weeks running. · zdte 36/60 (+5), recorder healthy 2026-07-08..2026-09-04, 24 sessions to the B-L density gate, ~5 weeks at this rate (~mid-Oct) · crypto 62 derived minute-days 07-05..09-04 (+7); the spec's `research/data/BTC-USD_*.csv` counter still reads 1 because rotate.py gzips (30 .csv.gz) — honest source is research/minutes/. learned_weights.json **FOSSIL for the fourth straight week** (mtime 2026-08-11, built from 38 days ending 08-11; 24 accrued days unincorporated) — the longest-standing unfixed instrumentation defect on the desk; its frozen figures: skill −0.031, edge_found=false, edge_z −3.67, hit 49.12% vs naive 49.98%, gross −0.195 bps/trade against 60 bps costs · insider rolling feed 400 = the KEEP=400 cap (window 2026-08-26..09-04, ~10 days), saturated and structurally unable to express accrual; deep-sample events.json 1,062, untouched since 2026-07-07, so the "double to 2,124" milestone stays unfireable as instrumented

2026-09-12 · clean (6/6 families in discover.py's FAMILIES match REGISTRY.md; 35 configs, config set identical to 09-05; no commit has touched discover.py or the fetchers since 09-01) · **NO DRIFT ATTRIBUTABLE TO NEW DATA — fifth consecutive week.** Weekend run (MARKET: CLOSED): discoveries.csv and this log are verdict/counter books that do not compound (cleared by the 09-08 audit), nothing was entered or queued. (1) PIPELINE: Monday 09-07 was Labor Day, so no Monday fetch ran and the panel still ended 2026-09-04 — panels refetched FIRST, before any discover.py pass: 2011-09-12..2026-09-11, 3,775 rows, 145 cols (prices 148), `failed: []` — SPCX, the standing lone failure, fetched this week. ONE 2026-09-12 block, bench 1.27. (2) Attribution by the 08-22 method (same refreshed panel truncated to end 09-04): **the 4 new sessions (09-08..09-11) moved every config's net Sharpe by ≤0.02 and OOS by ≤0.06; all six family verdicts, DSRs and PBOs are identical on the truncated panel.** One category difference vs the FROZEN row: Price-action value-area fade real-but-loses → **dead** (best config q0.1 H21 → q0.2 H21, net +0.13 → −0.05, OOS −0.35, DSR 0.18 → 0.21, PBO 0.02 → 0.51) — it prints dead on the truncated panel too, so it is the 4-row front roll re-phasing the positional grid, not the market; back to dead after two weeks of real-but-loses, exactly the straddle the 08-15 phase sweep predicted, and the 08-15 withdrawal stands. Twelve configs moved >0.2 week-over-week, every one front roll: high-volume-premium q0.2 H21 net +0.51 → +0.11 / OOS +0.80 → +0.16 (new sessions 0.00 / +0.02), value-area-fade q0.1 H10 net −0.54 → −0.15 (new sessions 0.00), volume-shock-reversal q0.1 H3 net −0.89 → −1.19 (new sessions +0.01). Rest: overnight structural-but-uncostable (basket net −0.41, gross 1.51) · opex real-but-loses DSR 0.91 PBO 0.60 · turn-of-month t5 real-but-loses DSR 1.0 PBO 0.05, net 1.14 vs bench 1.27 — not a SURVIVOR, no MC drawdown run · microstructure real-but-loses, illiquidity q0.2 DSR 0.15, net 0.82 → 0.89 / OOS 1.16 → 1.31 (front roll) · confluence dead. Nothing crossed DSR 0.5 or 0.95. NEW, reporting code only: `discover.py:297` filters `verdict == "SURVIVOR"` while `judge()` writes `"SURVIVOR (beats buy&hold)"`, so the printed "SURVIVORS: N" can never exceed 0 — the CSV verdict column is correct and is what the sentinel reads. Not patched. SUGGESTIONS awaiting sign-off under rule 1, none actioned: (a) anchor `reb` to a calendar epoch + report H-config Sharpes as a median across phases (08-15, now 5 weeks of evidence); (b) refresh panels inside the sentinel run or fetch Friday post-close (08-22; done by hand 5 weeks running); (c) the one-token survivor-filter fix above; (d) the task file's weekend clause ("write NO row dated today") cannot coexist with a Saturday-scheduled sentinel — declare the sentinel's books non-session-unit in the task text so the next agent is not left to judge it. · zdte 40/60 (+4, Labor Day week), recorder continuous through SPY_2026-09-11.csv, 20 sessions to the B-L density gate ≈ 2026-10-09 at 5/week · crypto 69 derived minute-days 07-05..09-11 (+7); the spec's `research/data/BTC-USD_*.csv` counter reads 1 (today's live file; rotate.py gzips) — honest source research/minutes/. learned_weights.json **FOSSIL for the fifth straight week** (mtime 2026-08-11, built from 38 days; 31 accrued days unincorporated), although data/backtest_log.txt was appended at 08:43 today ("no signal is net-positive after costs") — a backtest is running, the weights writer is not; frozen figures: skill −0.031, edge_found=false, edge_z −3.67, gross −0.195 bps/trade vs 60 bps costs · insider rolling feed 400 = the KEEP=400 cap (window 2026-09-01..09-11), saturated and unable to express accrual; deep-sample events.json 1,062, untouched since 2026-07-07, so the "double to 2,124" milestone stays unfireable as instrumented

---

## 2026-09-08 — ROT-001 audit closed out, and the Arena turns out to be a MIXED-CALENDAR book

**The council's OPEN item, done: every dated one-row-per-run file this lab owns, audited against
`sessions.py`, reported clean or not.** Rows written since Friday's 2026-09-04 close, per book —
the number the council asked for, where anything above one would mean double-counting:

| book | rows | date col | last date | non-session rows | rows since 09-04 |
|---|---|---|---|---|---|
| `reports/rotation_log.csv` | 15 | date | 2026-09-04 | **0** | **0** |
| `reports/exit_overlays_log.csv` | 14 | date | 2026-09-04 | **0** | **0** |
| `daytype_log.csv` | 780 | date | 2026-09-04 | **0** | **0** |
| `reports/arena_trades.csv` | 1,725 | entry/exit | 2026-09-04 | **1** (NQ=F, futures) | 0 |
| `discoveries.csv` | 542 | run_date | 2026-09-05 | 519 | 35 |
| `progress.csv` | 62 | date | 2026-09-08 | 19 | 4 |
| `knowledge_base.csv`, `reports/SNDK_daytape.csv` | 9 / 20 | — | — | **0** | **0** |

**ROT-001 is remediated and the remediation is visible rather than asserted.** Both NAV books now
end at 2026-09-04 with **zero** non-session rows and **zero** rows written since Friday's close —
no Labor-Day compounding, no weekend rows. The pre-fix series survive beside them as
`rotation_log.pre-ROT-001.csv` and `exit_overlays_log.pre-ROT-001.csv`, each still carrying its 7
non-session rows, and `reports/rot_restate_note.json` holds published-vs-corrected under the
2026-09-08 ruling. **Nothing was silently overwritten**, which was the actual instruction.

**`discoveries.csv` and `progress.csv` are flagged, and then cleared — but for a reason worth
writing down.** 519 of 542 and 19 of 62 rows sit on non-sessions. Neither is a defect, because
**neither book compounds**: `discoveries.csv` carries per-config Sharpe/DSR/PBO verdicts and
`progress.csv` carries counters. The ROT-001 hazard is specifically *a return multiplied onto a
running NAV on a day that did not exist*; a Sharpe recorded on a Saturday is merely a Saturday's
recomputation of the same fixed history. **What is genuinely missing is that neither book DECLARES
its unit** — the exemption I just applied is my judgement about their contents, and next month it
will be someone else's judgement. That is the residual gap and it should be a one-line header.

**And `progress.csv` shows the ROT-001 SHAPE without the ROT-001 harm, which is the clearest
teaching case available:** its 2026-09-05, 09-06 and 09-07 rows are byte-identical
(briefs 50, ledger_calls 121, ledger_scored 75, ..., discoveries 542). Three rows, one state,
because nothing happened on a weekend and a holiday. **That is exactly what the rotation arm did —
"today is a new day, so write a row" — and it was harmless here only because the column is a
counter rather than a multiplier.** The defect is identical; only the datatype spared it.

### THE NEW FINDING: the Arena is a mixed-calendar book, and a per-LAB calendar exemption cannot express that

The sweep's session assertion exempts labs "whose unit is not the NYSE session ... by declaration,
not by guesswork." The Arena would be declared NYSE-session — and it is, for 145 of its 147
instruments. **But it also holds `ES=F` and `NQ=F`, which trade the globex calendar**, including
Sunday evenings. Full audit of 3,573 date cells across `arena_trades.csv` and `arena_state.json`:

- **2 non-session-dated cells. Both futures. Zero non-futures.**
  `ES=F` open entry dated **2026-09-06 (Sunday)**; `NQ=F` exit dated **2026-08-23 (Sunday)**.

So the equity book is spotless and the two exceptions are real bars on a real calendar. **The
declaration granularity is what is wrong: a book holding instruments on different calendars cannot
be exempt or compliant as a whole.** Declared per-lab, the Arena is either falsely flagged twice or
falsely exempted 3,571 times. **Offered to the council: the session assertion should read a
per-INSTRUMENT calendar, and a book should declare the set of calendars it spans rather than one
unit.** This is Firm Brain §6 in the calendar: two readers of one book — the equity leg and the
futures leg — must not be asked to agree on a single definition of "a day that exists."

**Related, and not a date defect: `NQ=F` carries an open entry dated 2026-09-08 with `entry_px`
29,528.25, taken during a live session.** `arena.py:486-492` computes `last_session` from **SPY's**
series and correctly drops today's partial bar during RTH — but that value governs the *counters*
only. Per-instrument entries key off each instrument's own series, so a futures bar that looks
complete to its own tape opens a position the equity gate never sees. The gate is right about what
it measures and is measuring the wrong population — **Firm Brain §10's shape: a guard whose trigger
population and whose reading population are not the same set.** Reported, not altered: the
fill-integrity gate is pre-registered and changing it is a ruling.

**Arena freshness this run:** `OK arena · session 2026-09-04 +32/−49 · regime calm-up`. The last
completed session is 2026-09-04 (09-05/06 weekend, 09-07 Labor Day, 09-08 live), and its rows are
present in `arena_trades.csv`. Zero rows written for any date after it.

---

## 2026-09-09 — the ROT-001 fix landed in one file and not the other, and the audit the council ordered is what caught it

**The council's 09-07 OPEN item was: "audit every one-row-per-run file the lab owns, not just these two…
Report the audit even where it comes back clean." It did not come back clean.**

### Rows written per date, since Friday 2026-09-04's close

| book | rows since 09-04 | verdict |
|---|---|---|
| `rotation_log.csv` | **1** (09-08) | CLEAN — ROT-001 fix working |
| `exit_overlays_log.csv` | **12** (all dated 09-08) | **DEFECT** |
| `arena_trades.csv` | 40 (exit_date 09-08) | clean — unit is the trade, not the run |
| `price_restatement_log.csv` | 0 | clean |
| `SNDK_daytape.csv` | 0 | clean |
| `universe_daytype.csv` | n/a (no date column) | not a per-run book |

### The defect, and it is not a duplicate — it COMPOUNDS

`exit_overlays_log.csv` carries **exactly one row per date for its entire history** — 08-18, 08-19, 08-20,
08-21, 08-24, 08-25, 08-26, 08-27, 08-28, 08-31, 09-01, 09-02, 09-03, 09-04, every one of them a single row
— **and then twelve rows dated 2026-09-08.** The unit is proven by fourteen consecutive sessions; twelve is
not a design.

They are not identical rows. **`nav_base` compounds down through them: 91.1118 (09-04) → 90.0835 → 89.0668 →
88.0615 → 87.0676 → 86.0944 → 85.1321 → 84.1806 → 83.2397 → 82.3093 → 81.3893 → 80.4796 → 79.5801.**
That is a recorded **−12.6% NAV move for a single session** in which the tape moved about −1.1%. Every
statistic published off this book — the overlay NAVs, any regime-exit or stop-only comparison, any gap
quoted against `nav_base` — is overstated by roughly twelve sessions of compounding.

### Root cause, verified in the source rather than inferred

Both files were given the same ROT-001 guard on 09-07. **Only one of them was finished.**

- `rotation_arm.py:158` — on the **compounding** path: `book["last_run"] = today; book["last_session"] = sess_iso`
- `exit_overlays.py:171` — on the **compounding** path: `book["last_run"], book["last_regime"] = today, regime`
  — **`last_session` is never written.**

`exit_overlays.py` writes `last_session` in exactly one place, line 104, inside the *first-anchoring* branch
(`if not book.get("last_session")`) — and writes it twice on that same line, which is itself the fingerprint
of a hurried edit. So the guard on line 101, `if book.get("last_session") == sess_iso`, **reads a variable
that nothing on the live path ever updates.** It can never match after the initial anchoring, and every
subsequent run on the same session compounds again. Twelve runs on 09-08, twelve rows.

**This is Firm Brain §10 wearing a new costume, and a nastier one than the original.** §10 is "a rule
enforced only where it cannot bind" — there, because the rule's writers and its trigger population were
different sets. Here the guard is in the right file, on the right line, reading the right variable name, and
is still structurally incapable of firing, because **its state is written on a branch the live path never
takes.** It also reports as healthy: the file gains rows, the NAV moves, nothing errors, and the identical
guard sitting in the sibling file demonstrably works. *Offered to the council as the transferable law:
**a guard that tests a state variable must be checked against every path that is supposed to WRITE that
variable, not merely against the path that reads it. Copying a guard between two files copies the read and
can silently drop the write.*** The cheap machine check is a grep asymmetry: count `last_session` writes per
file — `rotation_arm.py` has two, `exit_overlays.py` has one, and the missing one is on the hot path.

### HALTED AND ESCALATED — nothing was fixed, nothing was restated

Per **REG-PP-001** and the council's own 09-07 wording ("you found a defect in your own published statistic,
so halt and escalate"), this agent did **not** patch `exit_overlays.py` and did **not** delete, dedupe or
restate the twelve rows. They are published statistics; correcting them is a ruling for Anupam.
**What is owed:** (1) the one-line writer fix, (2) a restatement of the 09-08 rows to a single settled-session
row, published **beside** the defective series exactly as ROT-001's rotation restatement was — the
`.pre-ROT-001.csv` snapshots are the precedent and they are the right one.
**Until then: do not quote any `exit_overlays_log.csv` NAV or any statistic derived from it.**

### What DID come back clean, verified independently rather than assumed

**ROT-001's rotation half is genuinely fixed.** `rotation_log.csv` and `exit_overlays_log.csv` now contain
**zero** rows dated a non-session, against 7-of-22 and 7-of-21 when the council measured them on 09-07. The
`.pre-ROT-001.csv` snapshots still carry their 09-05 / 09-06 / 09-07 rows, so the corrected series sits
beside the old one and nothing was silently overwritten. That is the directive honoured.

### Sweep-wide session assertion (council FIX, 2026-09-07) — 4 dates, all explained, zero live exposure

Ran across every NYSE-unit book this sweep touches. Labs whose unit is not the NYSE session — india-radar
(NSE), asia-radar (7 foreign calendars), crypto-microstructure (UTC day) — are exempt **by declaration**,
read from each book, not by guesswork.

- **insider-radar, 5 rows dated Sat 2026-07-25** — and these are **exactly the 5 `NO_BAR` rows**
  `price_audit.py` reports (FSBC, CLBK, TSM, BBASX, BYRN, "no bar dated 2026-07-25"). **Two independent
  checks corroborating and explaining each other:** the auditor knew there was no bar, this assertion says
  why. All scored, BENCH-002-frozen.
- **insider-radar, 7 rows `check_date` Sun 2026-08-16** — all scored, all pre-date the weekend-roll guard
  added to `append_call` on 2026-08-31. Closed by that guard; historic only.
- **insider-radar, 4 rows `check_date` Sat 2026-09-12** — all four **VOIDED** (CIK-only filers + PNAQ). No
  live exposure.
- **strategy-lab, 1 arena `exit_date` Sun 2026-08-23 — `NQ=F`.** Not a date bug: futures genuinely trade
  Sunday evening ET. But the Arena's declared unit is the **NYSE session** while its universe holds 9
  futures rows (ES=F ×5, NQ=F ×4), so a legitimate futures bar lands on a non-session date. That is the
  same population mismatch already logged here for the fill-integrity gate. **Reported, not altered** — the
  universe and the unit are both pre-registered.

**Total live exposure from the session assertion: zero.** Reported with the count even though it is zero,
because §3 says a zero carries its reason.

### Arena freshness this run
`OK arena · forward open 149, closed 1765 · session 2026-09-08 +65/−40 · regime calm-up`. The last completed
session is **2026-09-08** (today, 09-09, is live and the fill-integrity gate correctly does marks-only during
RTH) and its rows are present in `arena_trades.csv` — 40 exit_date rows. **[arena] rows written for 2026-09-08.**
