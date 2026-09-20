#!/usr/bin/env python
"""earnings_postgap_study.py — does the [earnings] desk's ACTUAL traded window survive
the same 6,442-print EDGAR test that killed the unconditional post-print drift?

Written 2026-09-20 by the earnings-week agent, answering the council directive of
2026-09-18: "the earnings run-up study already convicted your window ... state which of
your 9 rows sit inside the window that study killed."

WHY A SECOND SCRIPT AND NOT A CITATION. preprint_runup_study.py measures `post5` as
close[T+1] -> close[T+5] on EVERY print, unconditionally. The earnings desk does not
trade that. Its plans, as check_plans.py executes them, are:

    trigger : |open[T] / close[T-1] - 1| >= 4%   (T = first tradeable session)
    entry   : open[T]                            (the gap-day open, not a later close)
    exit    : close[T+5]                         (check_date = trigger + 7 calendar days)

Two differences, both material: the desk's window (a) starts one full session EARLIER,
so it contains the whole gap-day open->close that `post5` discards, and (b) fires only on
a >=4% gap, which `post5` never conditions on. Firm Brain §6 — measure in the rule's OWN
units — forbids reading the desk's verdict off a window the desk does not trade.

Same event set (data/edgar/earnings_8k.json, 8-K Item 2.02), same price panel, same
SPY-excess, same announcement-week clustering, same drop-the-best-week reading.

PRIOR, WRITTEN BEFORE THE RUN. The unconditional post-print number is -0.04%/week at
t=-0.31 — no drift to inherit. The desk's 9 live rows read +3.27% mean, 7/9, on a sample
far too small to argue with. Claude expects the conditional legs to land near zero too,
with the gap-day open->close contributing most of whatever is left, and expects the
DOWN-gap leg (the desk's favourite, 5 of its 9 rows) to be the weaker of the two once
measured against SPY rather than against zero.
"""
import csv, datetime as dt, json, math, os, statistics as st
from bisect import bisect_left

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = f"{BASE}/reports/earnings_postgap_study.json"
START = "2011-01-01"
THRESH = 0.04
HOLD = 5


def load(fn):
    rows = list(csv.DictReader(open(f"{BASE}/data/{fn}")))
    dates = [r["date"] for r in rows]
    px = {t: [] for t in rows[0] if t != "date"}
    for r in rows:
        for t in px:
            v = r.get(t)
            px[t].append(float(v) if v not in (None, "") else None)
    return dates, px


def print_session(accepted, dates):
    """First session index on which the announcement could be traded (same rule as the
    run-up study, so the two are joinable event-for-event)."""
    d, hhmm = accepted[:10], accepted[11:16]
    i = bisect_left(dates, d)
    if i >= len(dates):
        return None
    if dates[i] == d and hhmm < "16:00":
        return i
    return i + 1 if (dates[i] == d) else i


def t_of(v):
    if len(v) < 3:
        return None
    s = st.pstdev(v) * math.sqrt(len(v) / (len(v) - 1))
    return round(st.mean(v) / (s / math.sqrt(len(v))), 2) if s else None


def summarise(ev):
    """ev: list of (week, excess_pct). Week-clustered, per the study it replicates."""
    if not ev:
        return {"n": 0}
    byw = {}
    for w, x in ev:
        byw.setdefault(w, []).append(x)
    wk = {w: st.mean(v) for w, v in byw.items()}
    vals = list(wk.values())
    out = {"n": len(ev), "weeks": len(vals),
           "mean_per_week": round(st.mean(vals), 3),
           "t_week": t_of(vals),
           "median_event": round(st.median([x for _, x in ev]), 3),
           "hit": round(100 * sum(1 for _, x in ev if x > 0) / len(ev), 1)}
    if len(vals) > 3:
        best = max(wk, key=lambda w: wk[w])
        rest = [v for w, v in wk.items() if w != best]
        out["drop_best_week"] = round(st.mean(rest), 3)
        out["t_drop_best"] = t_of(rest)
    return out


def main():
    dates, op = load("open.csv")
    d2, cl = load("close.csv")
    assert dates == d2, "open.csv and close.csv are not on the same date index"
    events = json.load(open(f"{BASE}/data/edgar/earnings_8k.json"))
    events = [dict(e, ticker=t) for t, v in events.items() for e in v["events"]]

    legs = {k: [] for k in ("up", "down", "all_gaps", "no_gap", "unconditional")}
    gapday = {"up": [], "down": []}
    eras = {"2011-15": {}, "2016-20": {}, "2021-26": {}}
    for e in eras:
        eras[e] = {k: [] for k in ("up", "down")}
    seen = 0
    for ev in events:
        t = ev.get("ticker")
        acc = ev.get("accepted") or ev.get("acceptedTime") or ev.get("acceptance")
        if not t or not acc or t not in op or t not in cl:
            continue
        if acc[:10] < START:
            continue
        i = print_session(acc, dates)
        if i is None or i < 1 or i + HOLD >= len(dates):
            continue
        o, pc = op[t][i], cl[t][i - 1]
        xo, xc = cl[t][i + HOLD], op["SPY"][i]
        sc = cl["SPY"][i + HOLD]
        if None in (o, pc, xo, xc, sc) or 0 in (o, pc, xc):
            continue
        seen += 1
        gap = o / pc - 1
        stock = (xo / o - 1) * 100
        spy = (sc / xc - 1) * 100
        exc = stock - spy
        wk = dt.date.fromisoformat(dates[i]).isocalendar()[:2]
        wk = f"{wk[0]}-W{wk[1]:02d}"
        legs["unconditional"].append((wk, exc))
        era = "2011-15" if dates[i] < "2016-01-01" else ("2016-20" if dates[i] < "2021-01-01" else "2021-26")
        if abs(gap) >= THRESH:
            legs["all_gaps"].append((wk, exc))
            side = "up" if gap > 0 else "down"
            legs[side].append((wk, exc))
            eras[era][side].append((wk, exc))
            gd = cl[t][i]
            if gd:
                gapday[side].append((wk, (gd / o - 1) * 100 - (cl["SPY"][i] / xc - 1) * 100))
        else:
            legs["no_gap"].append((wk, exc))

    rep = {"generated": dt.datetime.now().isoformat(timespec="seconds"),
           "events_joined": seen, "prices_through": dates[-1],
           "window": "open[T] -> close[T+5], excess vs SPY over identical dates",
           "trigger": f"|open[T]/close[T-1]-1| >= {THRESH:.0%}",
           "legs": {k: summarise(v) for k, v in legs.items()},
           "gap_day_only": {k: summarise(v) for k, v in gapday.items()},
           "eras": {e: {s: summarise(v) for s, v in d.items()} for e, d in eras.items()}}
    os.makedirs(f"{BASE}/reports", exist_ok=True)
    json.dump(rep, open(OUT, "w"), indent=1)
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
