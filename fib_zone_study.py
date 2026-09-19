#!/usr/bin/env python
"""fib_zone_study.py — does WHERE a pullback turns (its Fibonacci depth) tell you anything?

Anupam, 2026-09-19, after a trading-contest video in which the winner bought "the 61.8%" and
another trader's whole method is "the 50-61.8% zone". MEASUREMENT ONLY, rules fixed before the run:

  swing      10-bar pivots on daily closes; a pivot is only KNOWN 10 bars later, and that is when we act
  up-swing   pivot low L -> pivot high H with H/L-1 >= 10%; the pullback ends at the next pivot low P
             before any close above H. depth = (H-P)/(H-L). Mirror image for down-swings.
  entry      the close of the bar that CONFIRMS P (10 bars after it) - no hindsight
  outcome    21- and 63-session return minus SPY on identical dates (sign flipped for the short side),
             and whether price went on to take out the swing extreme H (or L) within 63 sessions
  buckets    <23.6 | 23.6-38.2 | 38.2-50 | 50-61.8 | 61.8-78.6 | 78.6-100 | >100 (swing failed)
  clustering by confirmation WEEK. Every bucket lives in the same survivor universe, so the
             comparison BETWEEN buckets is clean even though the level of all of them is flattered.
If the ratios matter, 50-61.8 should stand out from its neighbours. If they do not, depth is just a
smooth dial from "shallow = strong trend" to "deep = broken trend".
"""
import csv, datetime as dt, json, math, statistics as st
K, MINMOVE = 10, 0.10
rows = list(csv.DictReader(open("data/prices.csv"))); dates = [r["date"] for r in rows]
px = {t: [float(r[t]) if r[t] not in ("", None) else None for r in rows] for t in rows[0] if t != "date"}
spy = px["SPY"]
def wk(d): x = dt.date.fromisoformat(d); return (x - dt.timedelta(days=x.weekday())).isoformat()
def pivots(c):
    out = []
    for i in range(K, len(c) - K):
        w = c[i - K:i + K + 1]
        if c[i] is None or any(v is None for v in w): continue
        if c[i] == max(w): out.append((i, "H"))
        elif c[i] == min(w): out.append((i, "L"))
    return out
BUCKETS = [(0, .236, "<23.6%"), (.236, .382, "23.6-38.2%"), (.382, .5, "38.2-50%"), (.5, .618, "50-61.8%"),
           (.618, .786, "61.8-78.6%"), (.786, 1.0001, "78.6-100%"), (1.0001, 9, ">100% (failed)")]
ev = []
for t, c in px.items():
    if t in ("SPY", "ES=F", "NQ=F"): continue
    p = pivots(c)
    for a, b, d_ in zip(p, p[1:], p[2:]):
        (i0, k0), (i1, k1), (i2, k2) = a, b, d_
        if k0 == k1 or k1 == k2: continue
        e = i2 + K                                   # the bar on which the turn is KNOWN
        if e + 63 >= len(c) or c[e] is None or c[e + 63] is None or spy[e] is None or spy[e+63] is None or c[e+21] is None: continue
        if k0 == "L":                                # up-swing L->H, pullback to P (long side)
            L, H, P = c[i0], c[i1], c[i2]
            if H / L - 1 < MINMOVE or max(x for x in c[i1:e + 1] if x) > H: continue
            depth, side = (H - P) / (H - L), 1
            took = any(x and x > H for x in c[e + 1:e + 64])
        else:                                        # down-swing H->L, bounce to P (short side)
            H, L, P = c[i0], c[i1], c[i2]
            if 1 - L / H < MINMOVE or min(x for x in c[i1:e + 1] if x) < L: continue
            depth, side = (P - L) / (H - L), -1
            took = any(x and x < L for x in c[e + 1:e + 64])
        f21 = side * ((c[e + 21] / c[e] - 1) - (spy[e + 21] / spy[e] - 1)) * 100
        f63 = side * ((c[e + 63] / c[e] - 1) - (spy[e + 63] / spy[e] - 1)) * 100
        ev.append(dict(t=t, side=side, depth=depth, wk=wk(dates[e]), f21=f21, f63=f63, took=took))
def t_of(v):
    return st.mean(v) / (st.stdev(v) / math.sqrt(len(v))) if len(v) > 2 and st.stdev(v) else float("nan")
def table(side, label):
    sub = [e for e in ev if e["side"] == side]
    print(f"\n{label}: {len(sub)} pullbacks · entry on the confirming bar · excess vs SPY, week-clustered")
    print(f"  {'depth of the turn':<18}{'n':>6}{'weeks':>7}{'21s exc':>9}{'t':>7}{'63s exc':>9}{'t':>7}{'beat SPY':>10}{'took out the extreme':>22}")
    out = []
    for lo, hi, name in BUCKETS:
        g = [e for e in sub if lo <= e["depth"] < hi]
        if len(g) < 20: continue
        by = {}
        for e in g: by.setdefault(e["wk"], []).append(e)
        w21 = [st.mean(x["f21"] for x in v) for v in by.values()]; w63 = [st.mean(x["f63"] for x in v) for v in by.values()]
        r = dict(bucket=name, n=len(g), weeks=len(by), f21=st.mean(w21), t21=t_of(w21), f63=st.mean(w63), t63=t_of(w63),
                 hit=sum(1 for e in g if e["f63"] > 0) / len(g) * 100, took=sum(1 for e in g if e["took"]) / len(g) * 100)
        out.append(r)
        print(f"  {name:<18}{r['n']:>6}{r['weeks']:>7}{r['f21']:>+8.2f}%{r['t21']:>+7.2f}{r['f63']:>+8.2f}%{r['t63']:>+7.2f}{r['hit']:>9.0f}%{r['took']:>21.0f}%")
    return out
res = {"long_side_pullbacks_in_uptrends": table(1, "PULLBACKS IN UP-SWINGS (the long setup)"),
       "short_side_bounces_in_downtrends": table(-1, "BOUNCES IN DOWN-SWINGS (the short setup)")}
json.dump(dict(generated=dt.datetime.now().isoformat(timespec="seconds"), pivot_bars=K, min_swing=MINMOVE, prices_through=dates[-1], **res),
          open("reports/fib_zone_study.json", "w"), indent=1)
