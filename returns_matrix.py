#!/usr/bin/env python3
"""Multi-horizon returns across the WHOLE universe — the thing the sheets tracked for
every ticker (1d/2d/5d/10d ...). Two parts:

  1. Snapshot: latest 1d/2d/5d/10d/21d/63d return for every name -> dashboard.
  2. Honest pattern test on 15y of data: do those returns actually predict the next
     move? For each horizon it measures return autocorrelation (momentum vs reversal)
     and the sign-hit-rate, pooled across all names — the rigorous version of
     "I think I see patterns." Plus: what happens the day/week AFTER a big move.

Reads stock-radar-style prices.csv. Output: reports/returns_matrix.json + prints the
pattern test. A correlation is NOT a tradeable edge — costs and survivorship bias
still apply (see the Strategy Lab verdict).
"""
import json, os
import numpy as np
import pandas as pd
from scipy import stats

BASE = os.path.dirname(os.path.abspath(__file__))
HORIZONS = [1, 2, 5, 10, 21, 63]


def load():
    df = pd.read_csv(os.path.join(BASE, "data", "prices.csv"), parse_dates=["date"]).set_index("date")
    return df.sort_index()


def snapshot(prices):
    rows = []
    for t in prices.columns:
        s = prices[t].dropna()
        if len(s) < 64:
            continue
        rec = {"ticker": t}
        for h in HORIZONS:
            rec[f"r{h}d"] = round((s.iloc[-1] / s.iloc[-1 - h] - 1) * 100, 2)
        rows.append(rec)
    return rows


def pattern_test(prices):
    """For each horizon: pool (past h-day return, next h-day return) across all tickers
    and all time, and measure the correlation + sign agreement."""
    out = []
    for h in HORIZONS:
        ret = prices.pct_change(h)
        past = ret
        fwd = ret.shift(-h)                    # the NEXT non-overlapping h-day return
        P, F = [], []
        for t in prices.columns:
            a, b = past[t], fwd[t]
            m = a.notna() & b.notna()
            # de-overlap: take every h-th observation so windows don't overlap
            idx = np.where(m.values)[0][::h]
            P.extend(a.values[idx]); F.extend(b.values[idx])
        P, F = np.array(P), np.array(F)
        ok = np.isfinite(P) & np.isfinite(F)
        P, F = P[ok], F[ok]
        r, p = stats.pearsonr(P, F)
        same = np.mean(np.sign(P) == np.sign(F)) * 100
        out.append({"horizon": h, "n": len(P), "corr": round(float(r), 4),
                    "pvalue": float(p), "sign_hit": round(float(same), 1),
                    "kind": "momentum" if r > 0 else "reversal"})
    return out


def big_move_test(prices):
    """After a big 1-day move (top/bottom decile), what does the next 1d and 5d do?"""
    r1 = prices.pct_change(1)
    n1 = prices.pct_change(1).shift(-1)     # next day
    n5 = prices.pct_change(5).shift(-5)     # next 5 days
    a, d1, d5 = [], [], []
    for t in prices.columns:
        x, y1, y5 = r1[t], n1[t], n5[t]
        m = x.notna() & y1.notna() & y5.notna()
        a.extend(x[m]); d1.extend(y1[m]); d5.extend(y5[m])
    a, d1, d5 = np.array(a), np.array(d1), np.array(d5)
    hi = a >= np.nanpercentile(a, 90)       # biggest up days
    lo = a <= np.nanpercentile(a, 10)       # biggest down days
    return {
        "after_big_up_next1d": round(float(np.mean(d1[hi]) * 100), 3),
        "after_big_up_next5d": round(float(np.mean(d5[hi]) * 100), 3),
        "after_big_down_next1d": round(float(np.mean(d1[lo]) * 100), 3),
        "after_big_down_next5d": round(float(np.mean(d5[lo]) * 100), 3),
        "baseline_next1d": round(float(np.mean(d1) * 100), 3),
        "baseline_next5d": round(float(np.mean(d5) * 100), 3),
    }


def main():
    prices = load()
    snap = snapshot(prices)
    pat = pattern_test(prices)
    big = big_move_test(prices)
    json.dump({"n_tickers": len(snap), "horizons": HORIZONS, "snapshot": snap,
               "pattern": pat, "big_move": big},
              open(os.path.join(BASE, "reports", "returns_matrix.json"), "w"), indent=1)

    print("=== Return autocorrelation, pooled over 15y & all names (non-overlapping) ===")
    print(f"{'horizon':>7s} {'n':>8s} {'corr':>8s} {'p-value':>9s} {'sign-hit':>8s}  read")
    for r in pat:
        flag = "" if r["pvalue"] < 0.01 else "  (not sig.)"
        print(f"{r['horizon']:6d}d {r['n']:8d} {r['corr']:8.4f} {r['pvalue']:9.1e} "
              f"{r['sign_hit']:7.1f}%  {r['kind']}{flag}")
    print("\n=== What happens AFTER a big 1-day move (top/bottom decile) ===")
    print(f"  after big UP  : next 1d {big['after_big_up_next1d']:+.3f}%   next 5d {big['after_big_up_next5d']:+.3f}%")
    print(f"  after big DOWN: next 1d {big['after_big_down_next1d']:+.3f}%   next 5d {big['after_big_down_next5d']:+.3f}%")
    print(f"  baseline      : next 1d {big['baseline_next1d']:+.3f}%   next 5d {big['baseline_next5d']:+.3f}%")
    print("\nNote: a nonzero correlation is a *pattern*, not an *edge*. These are gross of")
    print("costs and use today's (survivor) universe — the Strategy Lab already showed the")
    print("tradeable versions don't survive deflation. Descriptive, not a signal.")


if __name__ == "__main__":
    main()
