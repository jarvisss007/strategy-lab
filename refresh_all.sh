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
if [ "$(date +%u)" = "1" ]; then
  "$PY" /Users/anupampatil/strategy-lab/fetch_data.py >> "$LOG" 2>&1
  "$PY" /Users/anupampatil/strategy-lab/returns_matrix.py >> "$LOG" 2>&1
  "$PY" /Users/anupampatil/strategy-lab/universe_daytype.py >> "$LOG" 2>&1
  "$PY" /Users/anupampatil/strategy-lab/earnings_radar.py >> "$LOG" 2>&1
fi
"$PY" /Users/anupampatil/strategy-lab/learning_meter.py >> "$LOG" 2>&1
"$PY" /Users/anupampatil/strategy-lab/build_hub.py >> "$LOG" 2>&1
echo "window.LAST_REFRESH=\"$(date '+%Y-%m-%dT%H:%M:%S')\";" > /Users/anupampatil/command-center/freshness.js
echo "done $(date '+%H:%M:%S')" >> "$LOG"
touch "$DONE_MARK"
find /Users/anupampatil/strategy-lab -maxdepth 1 -name ".refresh_done_*" -mtime +2 -delete
