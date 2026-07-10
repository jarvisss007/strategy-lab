#!/bin/bash
# Daily refresh of the trading hub — run by launchd (com.anupam.tradinghub-refresh)
# so the Trading Terminal / Stock Radar never go stale even if the app is closed.
PY=/opt/anaconda3/bin/python
LOG=/Users/anupampatil/strategy-lab/refresh.log
echo "=== refresh $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG"
"$PY" /Users/anupampatil/stock-radar/collector.py >> "$LOG" 2>&1
"$PY" /Users/anupampatil/stock-radar/check_plans.py >> "$LOG" 2>&1
"$PY" /Users/anupampatil/stock-radar/collector.py >> "$LOG" 2>&1   # re-embed ledger if a plan fired
# Mondays: re-learn the studies on the grown dataset (research stays current)
if [ "$(date +%u)" = "1" ]; then
  "$PY" /Users/anupampatil/strategy-lab/fetch_data.py >> "$LOG" 2>&1
  "$PY" /Users/anupampatil/strategy-lab/returns_matrix.py >> "$LOG" 2>&1
  "$PY" /Users/anupampatil/strategy-lab/universe_daytype.py >> "$LOG" 2>&1
  "$PY" /Users/anupampatil/strategy-lab/earnings_radar.py >> "$LOG" 2>&1
fi
"$PY" /Users/anupampatil/strategy-lab/learning_meter.py >> "$LOG" 2>&1
"$PY" /Users/anupampatil/strategy-lab/build_hub.py >> "$LOG" 2>&1
echo "done $(date '+%H:%M:%S')" >> "$LOG"
