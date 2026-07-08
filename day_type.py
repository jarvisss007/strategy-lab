#!/usr/bin/env python3
"""SNDK-style intraday day-type analyzer — the automated version of the hand-built
"SNDK analysis" sheet. Pulls intraday bars, and per day computes:
  net move, total path (sum of |bar-to-bar moves|), efficiency = |net|/path,
  regime (TREND / MIXED / CHOP), swing stats — exactly the sheet's columns, but
  filled by code instead of by hand.

Then it runs the ONE honest, tradeable test: does the FIRST HOUR predict the rest
of the day? The efficiency ratio is only known at the close, so it is hindsight —
the sheet's "trade the 6:30-7:15 open" thesis only works if early action forecasts
the day. This measures whether it does. Usage: python day_type.py [TICKER]
"""
import json, sys, urllib.request
from collections import defaultdict
import numpy as np

UA = {"User-Agent": "Mozilla/5.0"}
TREND, CHOP = 0.40, 0.20   # efficiency thresholds (from the sheet's own regime cuts)


def intraday(sym, rng, itv):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng}&interval={itv}"
    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25))
    r = d["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    import datetime as dt
    bars = defaultdict(list)
    for t, c in zip(r["timestamp"], q["close"]):
        if c is not None:
            d0 = dt.datetime.fromtimestamp(t)
            bars[d0.date()].append((d0, c))
    return bars


def analyze_day(series):
    px = [c for _, c in series]
    if len(px) < 4:
        return None
    net = px[-1] - px[0]
    path = sum(abs(px[i] - px[i - 1]) for i in range(1, len(px)))
    eff = abs(net) / path if path else 0.0
    swings = [px[i] - px[i - 1] for i in range(1, len(px))]
    regime = "TREND" if eff >= TREND else "CHOP" if eff < CHOP else "MIXED"
    return {"open": px[0], "close": px[-1], "net": net, "path": path,
            "eff": eff, "regime": regime, "max_swing": max(abs(s) for s in swings),
            "n_bars": len(px)}


def early_vs_rest(bars, early_bars=4):
    """early_bars = number of opening bars treated as 'first hour' (4x15m = 1h)."""
    rows = []
    for day in sorted(bars):
        s = sorted(bars[day])
        if len(s) < early_bars + 3:
            continue
        px = [c for _, c in s]
        o = px[0]
        e = px[early_bars]          # price at end of early window
        c = px[-1]
        early_net = e - o
        rest_net = c - e            # what you could actually trade after the open
        early_path = sum(abs(px[i] - px[i - 1]) for i in range(1, early_bars + 1))
        early_eff = abs(early_net) / early_path if early_path else 0.0
        full = analyze_day(s)
        rows.append({"day": day, "early_dir": np.sign(early_net), "rest_dir": np.sign(rest_net),
                     "early_eff": early_eff, "full_eff": full["eff"], "full_regime": full["regime"],
                     "full_net": full["net"], "max_swing": full["max_swing"]})
    return rows


def main():
    sym = sys.argv[1] if len(sys.argv) > 1 else "SNDK"
    bars = intraday(sym, "3mo", "60m")   # ~62 days, coarse; most day-samples available
    print(f"=== {sym} automated day-type table (last {len(bars)} sessions, 60m bars) ===")
    print(f"{'date':12s} {'open':>8s} {'close':>8s} {'net':>7s} {'path':>7s} {'eff':>5s}  regime  maxSwing")
    days = sorted(bars)
    stats = []
    for day in days:
        a = analyze_day(sorted(bars[day]))
        if a:
            stats.append(a)
            print(f"{str(day):12s} {a['open']:8.2f} {a['close']:8.2f} {a['net']:7.2f} "
                  f"{a['path']:7.2f} {a['eff']:5.2f}  {a['regime']:6s}  {a['max_swing']:.2f}")

    effs = [a["eff"] for a in stats]
    regimes = defaultdict(int)
    for a in stats:
        regimes[a["regime"]] += 1
    print(f"\nAvg efficiency {np.mean(effs):.2f}  |  regime mix: {dict(regimes)}")
    print(f"Avg |net move| {np.mean([abs(a['net']) for a in stats]):.2f}  "
          f"Avg total path {np.mean([a['path'] for a in stats]):.2f}  "
          f"Avg max intraday swing {np.mean([a['max_swing'] for a in stats]):.2f}")

    # honest test: does the first hour predict the rest of the day?
    rows = early_vs_rest(bars, early_bars=1)  # 60m bars: 1 bar = first hour
    n = len(rows)
    cont = np.mean([r["early_dir"] == r["rest_dir"] for r in rows]) if n else float("nan")
    # does a high-efficiency open predict a trend day?
    hi = [r for r in rows if r["early_eff"] >= TREND]
    trend_given_hi = np.mean([r["full_regime"] == "TREND" for r in hi]) if hi else float("nan")
    base_trend = np.mean([r["full_regime"] == "TREND" for r in rows]) if n else float("nan")
    print(f"\n--- Honest test ({n} sessions) ---")
    print(f"Open direction continues into rest of day: {cont*100:.0f}% of days "
          f"(50% = coin flip, no edge)")
    print(f"P(trend day | high-efficiency open): {trend_given_hi*100:.0f}%   "
          f"vs base rate P(trend day): {base_trend*100:.0f}%")
    print(f"\nSample is only {n} sessions — nowhere near enough to trust. This measures, "
          f"it does not prove. A recorder that logs this daily is the way to a real sample.")


if __name__ == "__main__":
    main()
