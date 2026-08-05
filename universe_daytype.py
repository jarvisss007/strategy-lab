#!/usr/bin/env python3
"""Run the SNDK day-type framework across the WHOLE watchlist, not just SNDK.
For every ticker it pulls intraday bars, computes each session's day-type
(efficiency, regime, total path, swings), then aggregates to a per-ticker profile:
how trendy vs choppy the name is, and how much intraday opportunity it offers.

Answers: which of my names behave like SNDK? Output: reports/universe_daytype.json
+ .csv, ranked by intraday opportunity. Run: python universe_daytype.py

DATA-DEFECT AUDIT 2026-08-05 (verdict: REAL, no bug). The position agent flagged the
2026-08-03 rebuild ("tradeable_pct 0.0 on nearly every name, 80/108 QUIET") as a
suspected pipeline defect. Investigated: this is the file's normal state, not a
regression. Every git-tracked version shows the same shape — QUIET counts 71/74/77/80
across the four prior builds (the 2026-07-31 build was also exactly 80 QUIET), and
49-62 names at tradeable_pct 0.0 in each. The 08-03 build actually has FEWER zeros (49)
than any predecessor. Fresh Yahoo fetches on 2026-08-05 reproduce the stored numbers
(HOOD avg_path 6.8% / tradeable 0.0 both stored and fresh; SNDK 16.6%->16.0% within
one-day drift), so the 08-03 null-bar glitch left no residue — this script fetches
live per run and uses no intraday cache. tradeable_pct 0.0 is the honest reading:
most large-cap names never accumulate >=12% intraday zigzag path in a session; the
12% bar (day_type.TRADEABLE_PATH_PCT) is intentionally SNDK-calibrated and high.
No thresholds or computations were changed by this audit.
"""
import csv, json, os, time
from collections import defaultdict
import numpy as np
import day_type as DT

BASE = os.path.dirname(os.path.abspath(__file__))
WL = os.path.join(os.path.expanduser("~"), "stock-radar", "watchlist.csv")


def profile(sym):
    try:
        bars = DT.intraday(sym, "1mo", "15m")
    except Exception:
        return None
    days = [d for d in sorted(bars) if len(bars[d]) >= 8]
    if len(days) < 8:
        return None
    effs, paths, larg, ranges = [], [], [], []
    reg = defaultdict(int)
    for d in days:
        s = sorted(bars[d])
        a = DT.analyze_day(s)
        if not a:
            continue
        effs.append(a["eff"]); paths.append(a["path_pct"]); reg[a["regime"]] += 1
        larg.append(a["largest_swing"] / a["open"] * 100 if a["open"] else 0)
        px = [c for _, c in s]
        ranges.append((max(px) - min(px)) / px[0] * 100 if px[0] else 0)
    n = len(effs)
    if n < 8:
        return None
    avg_eff = float(np.mean(effs))
    avg_path = float(np.mean(paths))
    # QUIET names don't move enough to register swings — their efficiency is a sparse-swing
    # artifact, not real trending. Only classify trend/chop above an opportunity floor.
    if avg_path < 8.0:
        char = "QUIET"
    else:
        char = "TRENDY" if avg_eff >= 0.45 else "CHOPPY" if avg_eff < 0.30 else "BALANCED"
    return {
        "ticker": sym, "n_days": n,
        "avg_eff": round(avg_eff, 3),
        "pct_trend": round(reg["TREND"] / n * 100, 1),
        "pct_chop": round(reg["CHOP"] / n * 100, 1),
        "pct_mixed": round(reg["MIXED"] / n * 100, 1),
        "avg_path_pct": round(float(np.mean(paths)), 1),      # intraday opportunity
        "avg_range_pct": round(float(np.mean(ranges)), 1),    # daily hi-lo range
        "avg_largest_swing_pct": round(float(np.mean(larg)), 1),
        "tradeable_pct": round(np.mean([p >= DT.TRADEABLE_PATH_PCT for p in paths]) * 100, 1),
        "character": char,
    }


def main():
    with open(WL) as f:
        tickers = [r["yahoo"].strip() for r in csv.DictReader(f) if r["yahoo"].strip()]
    rows, failed = [], []
    for i, sym in enumerate(tickers):
        p = profile(sym)
        if p:
            rows.append(p)
        else:
            failed.append(sym)
        if (i + 1) % 20 == 0:
            print(f"  {i+1}/{len(tickers)} done")
        time.sleep(0.15)
    rows.sort(key=lambda r: -r["avg_path_pct"])   # most intraday opportunity first
    out = {"built_note": "15m bars, ~1mo per name", "n": len(rows),
           "tradeable_path_pct": DT.TRADEABLE_PATH_PCT, "rows": rows, "failed": failed}
    json.dump(out, open(os.path.join(BASE, "reports", "universe_daytype.json"), "w"), indent=1)
    cols = list(rows[0].keys())
    with open(os.path.join(BASE, "reports", "universe_daytype.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(rows)

    print(f"\n=== Intraday opportunity ranking ({len(rows)} names, top 20) ===")
    print(f"{'tick':6s} {'char':9s} {'eff':>5s} {'path%':>6s} {'range%':>6s} "
          f"{'lgSwg%':>6s} {'trend%':>6s} {'chop%':>6s} {'tradeable%':>9s}")
    for r in rows[:20]:
        print(f"{r['ticker']:6s} {r['character']:9s} {r['avg_eff']:5.2f} {r['avg_path_pct']:6.1f} "
              f"{r['avg_range_pct']:6.1f} {r['avg_largest_swing_pct']:6.1f} {r['pct_trend']:6.1f} "
              f"{r['pct_chop']:6.1f} {r['tradeable_pct']:9.1f}")
    # where does SNDK land + character split
    for i, r in enumerate(rows):
        if r["ticker"] == "SNDK":
            print(f"\nSNDK ranks #{i+1}/{len(rows)} by opportunity (path% {r['avg_path_pct']}, {r['character']})")
    chars = defaultdict(int)
    for r in rows:
        chars[r["character"]] += 1
    print("Character mix across universe:", dict(chars))
    print(f"failed (no intraday): {failed}")
    print("\njson/csv -> reports/universe_daytype.{json,csv}")


if __name__ == "__main__":
    main()
