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

DONE_MARK=/Users/anupampatil/strategy-lab/.refresh_done_$(date '+%Y-%m-%d')
if [ -f "$DONE_MARK" ] && [ "$(date +%u)" -le 5 ] && [ "$(date -r "$DONE_MARK" '+%H')" -ge 6 ]; then
  exit 0
fi
PY=/opt/anaconda3/bin/python
LOG=/Users/anupampatil/strategy-lab/refresh.log
echo "=== refresh $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG"
"$PY" /Users/anupampatil/stock-radar/collector.py >> "$LOG" 2>&1
"$PY" /Users/anupampatil/stock-radar/check_plans.py >> "$LOG" 2>&1
"$PY" /Users/anupampatil/stock-radar/collector.py >> "$LOG" 2>&1   # re-embed ledger if a plan fired
# Asia Radar: cross-market web (US·India·China·HK·Korea·Japan·Taiwan)
"$PY" /Users/anupampatil/asia-radar/collector.py >> "$LOG" 2>&1
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
