#!/bin/bash
# Daily refresh of the trading hub — run by launchd (com.anupam.tradinghub-refresh)
# so the Trading Terminal / Stock Radar never go stale even if the app is closed.
#
# Triggered TWO ways: StartCalendarInterval (weekdays 7:05 AM, for promptness)
# AND StartInterval (every 30 min, as a catch-up net). macOS launchd silently
# SKIPS a StartCalendarInterval firing if the Mac is asleep at that exact
# minute — it does not retroactively run it on wake. Discovered 2026-07-11:
# the job had only fired once via its calendar trigger when 2-3 were expected.
# The idempotency check below makes the frequent trigger a cheap no-op once
# today's refresh has already succeeded, so it costs nothing except on the day
# it's actually needed.
#
# BUG (found 2026-07-14): a middle-of-the-night wake (Power Nap / iCloud sync)
# let the 30-min catch-up net fire at ~2 AM, stamp DONE_MARK, and then silently
# no-op every legitimate trigger for the rest of the day — including the
# intended 7:05 AM run — leaving the terminal ~17 hours stale by evening. Fix:
# a pre-market stamp doesn't count as "done" — only a mark from 6 AM or later
# (after the intended run window) satisfies the guard.
# Asia Radar COLLECTOR: hoisted here 2026-08-29 to close ASIA-008.
#
# This writes data/markets.json — the only thing that does — and it used to sit at
# L100, BELOW the once-a-day DONE_MARK guard, while its reader (predictions.py, two
# lines down) sat above it. So the reader ran every 30 minutes against a file written
# once a day. On 2026-08-28 markets.json was written at 08:40 PDT, mid-US-session, and
# predictions.py then fired 13 times between 14:07 and 20:07 asking for a SETTLED US
# close that the file could never contain. It refused all 13. Zero rows were written
# for the 2026-08-31 Asian session and, under that wiring, none could ever be written
# again on any weekday.
#
# The ASIA-005 guard shipped the day before was CORRECT — before it, predictions.py
# anchored happily to that stale 08:40 mid-session bar, which was the contamination it
# was built to stop. Fixing the symptom converted an invisible contamination into an
# invisible outage on the desk's second-largest scored book. Nothing errored; "made 0"
# reads exactly like a quiet day. The council found it by reading one line out of
# 41,000 in refresh.log.
#
# A reader hoisted above a daily guard must bring its writer with it.
#
# Literal paths, not "$PY"/"$LOG": those are defined at L112, BELOW this point. Writing
# them here would expand to an empty command and an empty redirect target — a silent
# no-op, which is precisely the failure mode this hoist exists to end. Same shape as the
# defect being fixed: a line placed above the thing it depends on.
/opt/anaconda3/bin/python /Users/anupampatil/asia-radar/collector.py >> /Users/anupampatil/strategy-lab/refresh.log 2>&1

# Asia Radar prediction engine: cheap (one Yahoo call), runs on EVERY trigger —
# it must fire after the 1 PM PT US close, which the once-a-day guard below
# would skip. It no-ops unless a new final US close has appeared.
/opt/anaconda3/bin/python /Users/anupampatil/asia-radar/predictions.py >> /Users/anupampatil/strategy-lab/refresh.log 2>&1

# Calibration Observatory census: rebuilt on EVERY trigger, immediately after the
# Asia engine writes — the OBS-004 fix the council asked for (directive 2026-08-14,
# applied 2026-08-17 by labs-morning-sweep).
#
# The bug: the pooled census was built only by the morning sweep at ~08:41, while
# asia-radar's engine writes its forecasts after the 1 PM PT US close. So the
# Observatory read Asia as 69 scored / 0 pending while six live rows sat in its
# ledger — the census was always a day behind the lab it was reporting on. Moving
# the rebuild onto this 30-minute loop means it now always runs AFTER the last lab
# writes, which is what actually closes OBS-004; rebuilding earlier cannot.
#
# Placed here, above the once-a-day DONE_MARK guard, for the same reason
# predictions.py is: the guard would skip every post-US-close firing. Cost is one
# cheap local rebuild per trigger. The sweep's own 08:41 rebuild stays as a floor.
/usr/bin/python3 /Users/anupampatil/command-center/calibration.py >> /Users/anupampatil/strategy-lab/refresh.log 2>&1

# build_hub HOISTED 2026-08-31: it lived only inside the once-a-day arena block, so the
# terminal was rebuilt at ~06:50 and then aged all day under a "DATA LIVE" badge —
# Anupam read "refreshed 1h ago" mid-morning and concluded, reasonably, that nothing
# works. The build is seconds and display-only (no pre-registration surface). Same
# hoist-the-writer lesson as ASIA-008.
/opt/anaconda3/bin/python /Users/anupampatil/strategy-lab/build_hub.py >> /Users/anupampatil/strategy-lab/refresh.log 2>&1
# tracks.html regenerated every cycle too (2026-08-31): it only rebuilt inside the
# 13:45 scorer, so on Monday morning it still claimed "first registration fires
# Monday" — a live book wearing Saturday's page.
/opt/anaconda3/bin/python /Users/anupampatil/command-center/gen_tracks_page.py >> /Users/anupampatil/strategy-lab/refresh.log 2>&1
# EV shadow scans (built 2026-08-31, Anupam: "build all"): freeze today's cohorts, score
# matured ones, refresh the EV-6 split. Self-deduping per day; computed books only.
/opt/anaconda3/bin/python /Users/anupampatil/stock-radar/evolution_scans.py >> /Users/anupampatil/strategy-lab/refresh.log 2>&1
# The evidence room is GENERATED from the census (DIAG-001); regenerating it in
# the same breath as the census is the only thing that keeps them in step.
/opt/anaconda3/bin/python /Users/anupampatil/command-center/gen_evidence_room.py >> /Users/anupampatil/strategy-lab/refresh.log 2>&1

# ── PAPER ARENA POST-CLOSE PASS (SCHED-ARENA, 2026-08-27) ────────────────────
# ARENA-005 found the Arena's exit drain stuck and blamed the fire time. That was
# right and it was only half of it. The Arena refuses to open OR close on intraday
# prices (6:30–13:05 PT), and its only invocation lives BELOW the once-a-day guard,
# in a body whose intended trigger is 7:05 AM PT — dead centre in the window where
# the Arena must say no. So on a normal weekday the Arena is structurally incapable
# of trading: the 7:05 pass no-ops it and then stamps DONE_MARK, which turns every
# later trigger that day into an early `exit 0`. It has been trading only by
# accident — on the nights the Mac happened to wake before 6:30 AM.
#
# A stuck EXIT is recoverable; the row is still open and closes on the next good
# pass, which is why ARENA-005 could be closed on "no past-due rows". A missed
# ENTRY is not. The Arena only ever reads the LAST bar (c[len(c)-1]), so a session
# that goes by without a non-intraday pass is gone from the forward record forever.
# Two already are: 2026-08-12 (60 signals) and 2026-08-25 (45) have zero entries in
# arena_trades.csv and never will. That is 2 of 19 August sessions — ~10% of the
# record that the desk calls "the exam that counts" — lost with no error, no
# past-due row, and nothing in the register watching the entry side at all.
#
# Fixed here rather than by re-timing the whole refresh, because the rest of the
# body is correct at 7:05 and only the Arena chain needs the close. Placed ABOVE
# the guard for the same reason predictions.py and calibration.py are: the guard
# would skip every post-close firing. Own stamp, so it fires exactly once a day, on
# the first 30-min trigger after 13:05 PT — the same boundary arena.py enforces
# internally, quoted from the same clock. Repeated non-intraday passes on one bar
# are idempotent (a held position blocks its own re-entry), so a double fire costs
# nothing; a missed one costs a session.
ARENA_MARK=/Users/anupampatil/strategy-lab/.arena_done_$(date '+%Y-%m-%d')
ARENA_MIN=$((10#$(date '+%H') * 60 + 10#$(date '+%M')))
if [ ! -f "$ARENA_MARK" ] && [ "$ARENA_MIN" -ge 785 ]; then
  echo "=== arena post-close $(date '+%Y-%m-%d %H:%M:%S') ===" >> /Users/anupampatil/strategy-lab/refresh.log
  # the settled close the Arena will price the session at — it reads radar.json
  /opt/anaconda3/bin/python /Users/anupampatil/stock-radar/collector.py >> /Users/anupampatil/strategy-lab/refresh.log 2>&1
  /opt/anaconda3/bin/python /Users/anupampatil/strategy-lab/arena.py >> /Users/anupampatil/strategy-lab/refresh.log 2>&1
  # same integrity chain the morning body runs, in the same order and for the same
  # reason (DATA-002 then BENCH-002): reconcile the fills, then report on them.
  /opt/anaconda3/bin/python /Users/anupampatil/strategy-lab/auto_reconcile.py >> /Users/anupampatil/strategy-lab/refresh.log 2>&1
  /opt/anaconda3/bin/python /Users/anupampatil/strategy-lab/price_integrity.py >> /Users/anupampatil/strategy-lab/refresh.log 2>&1
  /opt/anaconda3/bin/python /Users/anupampatil/strategy-lab/build_hub.py >> /Users/anupampatil/strategy-lab/refresh.log 2>&1
  touch "$ARENA_MARK"
  find /Users/anupampatil/strategy-lab -maxdepth 1 -name ".arena_done_*" -mtime +2 -delete
fi

DONE_MARK=/Users/anupampatil/strategy-lab/.refresh_done_$(date '+%Y-%m-%d')
if [ -f "$DONE_MARK" ] && [ "$(date +%u)" -le 5 ] && [ "$(date -r "$DONE_MARK" '+%H')" -ge 6 ]; then
  exit 0
fi
PY=/opt/anaconda3/bin/python
LOG=/Users/anupampatil/strategy-lab/refresh.log
echo "=== refresh $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG"
"$PY" /Users/anupampatil/stock-radar/collector.py >> "$LOG" 2>&1
"$PY" /Users/anupampatil/stock-radar/check_plans.py >> "$LOG" 2>&1
# BRIEF v2 renderer feed (build queue item, built 2026-08-19)
"$PY" /Users/anupampatil/stock-radar/embed_brief.py >> "$LOG" 2>&1
"$PY" /Users/anupampatil/stock-radar/collector.py >> "$LOG" 2>&1   # re-embed ledger if a plan fired
# Asia Radar: cross-market web (US·India·China·HK·Korea·Japan·Taiwan)
# collector.py moved ABOVE the daily guard (ASIA-008, 2026-08-29) — it runs on every
# trigger now, so calling it again here would be a duplicate fetch, not a safety net.
"$PY" /Users/anupampatil/asia-radar/analyze.py >> "$LOG" 2>&1
"$PY" /Users/anupampatil/asia-radar/briefing.py >> "$LOG" 2>&1
# Mondays: re-learn the studies on the grown dataset (research stays current)
#
# BUG (found 2026-08-01 by the sentinel, fixed 2026-08-08): only fetch_data.py
# ran here, and it writes data/prices.csv. discover.py reads open.csv/close.csv/
# volume.csv, which nothing refreshed — so those panels sat frozen at 2026-07-07
# and every weekly "no drift" verdict was arithmetic on a static dataset, not
# out-of-sample evidence. fetch_ohlc.py + fetch_volume.py now run alongside it.
if [ "$(date +%u)" = "1" ]; then
  "$PY" /Users/anupampatil/strategy-lab/fetch_data.py >> "$LOG" 2>&1
  "$PY" /Users/anupampatil/strategy-lab/fetch_ohlc.py >> "$LOG" 2>&1
  "$PY" /Users/anupampatil/strategy-lab/fetch_volume.py >> "$LOG" 2>&1
  "$PY" /Users/anupampatil/strategy-lab/returns_matrix.py >> "$LOG" 2>&1
  "$PY" /Users/anupampatil/strategy-lab/universe_daytype.py >> "$LOG" 2>&1
  "$PY" /Users/anupampatil/strategy-lab/earnings_radar.py >> "$LOG" 2>&1
  # IPO desk (IPO_DESK.md): EDGAR pipeline + Anthropic watch + observation book
  "$PY" /Users/anupampatil/stock-radar/ipo_radar.py >> "$LOG" 2>&1
fi
"$PY" /Users/anupampatil/strategy-lab/arena.py >> "$LOG" 2>&1        # paper arena: takes/closes rule trades
# Check the fills the moment they are written, not whenever someone remembers.
# The Arena opens at c[len(c)-1] — the freshest, least-settled bar in the feed —
# so a stale refresh writes a wrong price into a permanent row (DATA-001: QBTS
# recorded at its 07-24 close on three later dates). The feed self-heals; a
# written row does not. Running the check here means a bad fill is caught on the
# next pass instead of surviving until Anupam reads his own portfolio.
# DATA-002 (ruled 2026-08-15): re-check the last session's fills against the feed
# as it has since SETTLED. radar.json is a rolling window that gets corrected on
# later refreshes; a written row never is. Open rows are repaired in place; closed
# rows only ever gain a *_tape column, never lose their scored number (BENCH-002).
# Runs BEFORE the integrity check so the check reports the reconciled state.
"$PY" /Users/anupampatil/strategy-lab/auto_reconcile.py >> "$LOG" 2>&1
"$PY" /Users/anupampatil/strategy-lab/price_integrity.py >> "$LOG" 2>&1
# Rotation overlay (REGISTRY.md 2026-08-17): Anupam's cull-losers-feed-winners
# rule as a pre-registered paper arm scored against the same open set held flat.
# Runs after the integrity chain so it marks off reconciled prices.
"$PY" /Users/anupampatil/strategy-lab/rotation_arm.py >> "$LOG" 2>&1
"$PY" /Users/anupampatil/strategy-lab/learning_meter.py >> "$LOG" 2>&1
"$PY" /Users/anupampatil/strategy-lab/build_hub.py >> "$LOG" 2>&1
echo "window.LAST_REFRESH=\"$(date '+%Y-%m-%dT%H:%M:%S')\";" > /Users/anupampatil/command-center/freshness.js
echo "done $(date '+%H:%M:%S')" >> "$LOG"
touch "$DONE_MARK"
find /Users/anupampatil/strategy-lab -maxdepth 1 -name ".refresh_done_*" -mtime +2 -delete
# Firm-wide positions view: assemble positions.js after all books have moved.
"$PY" /Users/anupampatil/command-center/positions_data.py >> "$LOG" 2>&1
# Exit overlays (REGISTRY.md 2026-08-18): REGIME_EXIT + STOP_ONLY as registered
# paper arms — the honest test of "exit intelligently", after rotation.
"$PY" /Users/anupampatil/strategy-lab/exit_overlays.py >> "$LOG" 2>&1
# CANSLIM-approx (REGISTRY.md 2026-08-20): O'Neil's system with native exits
"$PY" /Users/anupampatil/stock-radar/canslim.py >> "$LOG" 2>&1
