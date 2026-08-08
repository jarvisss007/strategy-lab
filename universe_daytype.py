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

TRADEABLE_PATH_PCT 12->10 + unusual_pct column added 2026-08-08, Anupam's Review #1
decision per daytype_threshold_brief_2026-08-05. `unusual_pct` = % of eval-window
sessions whose total zigzag path >= 1.5x that name's own trailing ~60d median session
path (the brief's K=1.5 relative design). It is a separate, additional signal — it
does NOT feed the character labels or gate anything.
"""
import csv, json, os, time
from collections import defaultdict
import numpy as np
import day_type as DT

BASE = os.path.dirname(os.path.abspath(__file__))
WL = os.path.join(os.path.expanduser("~"), "stock-radar", "watchlist.csv")

EVAL_SESSIONS = 21      # eval window: last ~1mo of sessions (matches the old "1mo" fetch)
UNUSUAL_K = 1.5         # unusual day = path >= 1.5x own trailing median (brief's K=1.5)
MIN_BASELINE = 10       # need this many trailing sessions to compute a baseline median


def profile(sym):
    # 60d fetch: the last EVAL_SESSIONS sessions are the eval window (same ~1mo the
    # builder always profiled); the ~39 sessions before them are that name's own
    # trailing baseline for the relative unusual_pct column.
    try:
        bars = DT.intraday(sym, "60d", "15m")
    except Exception:
        return None
    days = [d for d in sorted(bars) if len(bars[d]) >= 8]
    if len(days) < 8:
        return None
    stats = []                       # (day-analysis, hi-lo range%) for every full session
    for d in days:
        s = sorted(bars[d])
        a = DT.analyze_day(s)
        if not a:
            continue
        px = [c for _, c in s]
        stats.append((a, (max(px) - min(px)) / px[0] * 100 if px[0] else 0))
    if len(stats) < 8:
        return None
    ev = stats[-EVAL_SESSIONS:]      # eval window — all headline metrics come from here
    base = stats[:-EVAL_SESSIONS]    # trailing baseline — feeds unusual_pct only
    effs = [a["eff"] for a, _ in ev]
    paths = [a["path_pct"] for a, _ in ev]
    larg = [a["largest_swing"] / a["open"] * 100 if a["open"] else 0 for a, _ in ev]
    ranges = [r for _, r in ev]
    reg = defaultdict(int)
    for a, _ in ev:
        reg[a["regime"]] += 1
    n = len(effs)
    if n < 8:
        return None
    avg_eff = float(np.mean(effs))
    avg_path = float(np.mean(paths))
    # QUIET names don't move enough to register swings — their efficiency is a sparse-swing
    # artifact, not real trending. Only classify trend/chop above an opportunity floor.
    # This floor stays ABSOLUTE by design: daytype_threshold_brief_2026-08-05 showed a
    # relative label floor fabricates 41 fake TRENDY names out of exactly this artifact.
    if avg_path < 8.0:
        char = "QUIET"
    else:
        char = "TRENDY" if avg_eff >= 0.45 else "CHOPPY" if avg_eff < 0.30 else "BALANCED"
    # unusual_pct: % of eval sessions with path >= UNUSUAL_K x own trailing median path.
    # Separate signal ("moving more than usual for THIS name"); feeds no label, gates nothing.
    base_paths = [a["path_pct"] for a, _ in base]
    unusual = None
    if len(base_paths) >= MIN_BASELINE:
        med = float(np.median(base_paths))
        if med > 0:
            unusual = round(np.mean([p >= UNUSUAL_K * med for p in paths]) * 100, 1)
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
        "unusual_pct": unusual,      # relative signal; None when baseline too thin
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
    out = {"built_note": f"15m bars, 60d fetch; last {EVAL_SESSIONS} sessions = eval window",
           "n": len(rows),
           "tradeable_path_pct": DT.TRADEABLE_PATH_PCT,
           "unusual_note": f"unusual_pct = % of eval sessions with path >= {UNUSUAL_K}x own "
                           f"trailing ~60d median path; separate signal, feeds no label",
           "rows": rows, "failed": failed}
    json.dump(out, open(os.path.join(BASE, "reports", "universe_daytype.json"), "w"), indent=1)
    # .js wrapper for daytype.html over file:// (fetch() is blocked there — commit a5eab35
    # intended this emit but it was never wired in; the .js had been stale since Jul 8)
    with open(os.path.join(BASE, "reports", "universe_daytype.js"), "w") as f:
        f.write("window.DAYTYPE_DATA = ")
        json.dump(out, f, indent=1)
        f.write(";\n")
    cols = list(rows[0].keys())
    with open(os.path.join(BASE, "reports", "universe_daytype.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(rows)

    print(f"\n=== Intraday opportunity ranking ({len(rows)} names, top 20) ===")
    print(f"{'tick':6s} {'char':9s} {'eff':>5s} {'path%':>6s} {'range%':>6s} "
          f"{'lgSwg%':>6s} {'trend%':>6s} {'chop%':>6s} {'tradeable%':>9s} {'unusual%':>8s}")
    for r in rows[:20]:
        u = f"{r['unusual_pct']:8.1f}" if r["unusual_pct"] is not None else "       -"
        print(f"{r['ticker']:6s} {r['character']:9s} {r['avg_eff']:5.2f} {r['avg_path_pct']:6.1f} "
              f"{r['avg_range_pct']:6.1f} {r['avg_largest_swing_pct']:6.1f} {r['pct_trend']:6.1f} "
              f"{r['pct_chop']:6.1f} {r['tradeable_pct']:9.1f} {u}")
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
