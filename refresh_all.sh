#!/bin/bash
# Daily refresh of the trading hub — run by launchd (com.anupam.tradinghub-refresh)
# so the Trading Terminal / Stock Radar never go stale even if the app is closed.
PY=/opt/anaconda3/bin/python
LOG=/Users/anupampatil/strategy-lab/refresh.log
echo "=== refresh $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG"
"$PY" /Users/anupampatil/stock-radar/collector.py >> "$LOG" 2>&1
"$PY" /Users/anupampatil/strategy-lab/build_hub.py >> "$LOG" 2>&1
echo "done $(date '+%H:%M:%S')" >> "$LOG"
