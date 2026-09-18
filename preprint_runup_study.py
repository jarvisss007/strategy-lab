#!/usr/bin/env python
"""preprint_runup_study.py — is there a move INTO earnings worth taking, weeks before the print?

Anupam, 2026-09-17: "we are only taking based upon after and before the print - to capture the
move that happens way earlier, how can we build to achieve that?"

MEASUREMENT ONLY. Every earnings announcement the universe filed as an 8-K Item 2.02 (EDGAR,
data/edgar/earnings_8k.json), joined to the 15-year adjusted close panel (data/prices.csv).
For each event the PRINT SESSION is the first session on which the market could trade the news
(an 8-K accepted after 16:00 ET lands on the next session). Windows, all close-to-close:

  run-up 20   T-20 -> T-1     twenty sessions ending at the last close BEFORE the print lands
  run-up 10   T-10 -> T-1     the same, ten sessions
  event       T-1  -> T+1     the announcement itself (never traded here; shown so the reader
                              can see where the premium actually sits)
  post 5      T+1  -> T+5     what the earnings desk already trades

Each window is measured as the stock's return minus SPY over the identical dates. Events are
CLUSTERED BY ANNOUNCEMENT WEEK (companies report in the same weeks, so 40 prints in one week
are one market week, not 40 draws). Reported: mean per week, week-clustered t, hit rate, the
same by era, and the drop-the-best-week reading.

THE PRIOR, WRITTEN BEFORE THE RUN: the literature's earnings-announcement premium sits in the
announcement window itself (T-1 to T+1), not in the weeks before; pre-announcement drift is
weak and unstable across eras; and a run-up long is also a long on the market during reporting
season, which is why the excess is measured against SPY on the same dates. Claude expects the
run-up windows to read near zero and the event window to carry whatever premium exists.
"""
import csv, datetime as dt, json, math, os, statistics as st
from bisect import bisect_left

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = f"{BASE}/reports/preprint_runup_study.json"
START = "2011-01-01"

def load_prices():
    rows = list(csv.DictReader(open(f"{BASE}/data/prices.csv")))
    dates = [r["date"] for r in rows]
    px = {t: [] for t in rows[0] if t != "date"}
    for r in rows:
        for t in px:
            v = r.get(t)
            px[t].append(float(v) if v not in (None, "") else None)
    return dates, px

def print_session(accepted, dates):
    """First session index on which the announcement could be traded."""
    d, hhmm = accepted[:10], accepted[11:16]
    i = bisect_left(dates, d)
    if i >= len(dates):
        return None
    if dates[i] == d and hhmm < "16:00":
        return i
    return i + 1 if (dates[i] == d) else i        # after the close or a non-session -> next session

def ret(series, a, b):
    if a < 0 or b >= len(series) or series[a] is None or series[b] is None or series[a] <= 0:
        return None
    return (series[b] / series[a] - 1) * 100

def t_of(v):
    if len(v) < 3:
        return None
    sd = st.stdev(v)
    return st.mean(v) / (sd / math.sqrt(len(v))) if sd else None

def main():
    dates, px = load_prices()
    ek = json.load(open(f"{BASE}/data/edgar/earnings_8k.json"))
    WIN = {"runup20": (-20, -1), "runup10": (-10, -1), "event": (-1, 1), "post5": (1, 5)}
    events = []
    for tk, rec in ek.items():
        if tk not in px:
            continue
        for e in rec["events"]:
            if e["date"] < START:
                continue
            p = print_session(e["accepted"], dates)
            if p is None or p - 21 < 0 or p + 5 >= len(dates):
                continue
            row = {"ticker": tk, "print": dates[p], "week": (dt.date.fromisoformat(dates[p]) - dt.timedelta(days=dt.date.fromisoformat(dates[p]).weekday())).isoformat()}
            ok = True
            for k, (a, b) in WIN.items():
                s, m = ret(px[tk], p + a, p + b), ret(px["SPY"], p + a, p + b)
                if s is None or m is None:
                    ok = False; break
                row[k] = round(s - m, 3); row[k + "_raw"] = round(s, 3)
            if ok:
                events.append(row)
    print(f"{len(events)} announcements with full price windows, {len({e['ticker'] for e in events})} names, "
          f"{len({e['week'] for e in events})} announcement weeks, {events[0]['print'][:4]}-{events[-1]['print'][:4]}\n")

    def summarise(ev, key):
        by = {}
        for e in ev:
            by.setdefault(e["week"], []).append(e[key])
        weeks = [st.mean(v) for v in by.values()]
        raw = [e[key] for e in ev]
        best = max(by, key=lambda w: st.mean(by[w])) if by else None
        rest = [st.mean(v) for w, v in by.items() if w != best]
        return dict(n=len(ev), weeks=len(weeks), mean_per_week=round(st.mean(weeks), 3) if weeks else None,
                    t_week=round(t_of(weeks), 2) if t_of(weeks) is not None else None,
                    median_event=round(st.median(raw), 3) if raw else None,
                    hit=round(sum(1 for x in raw if x > 0) / len(raw) * 100, 1) if raw else None,
                    drop_best_week=round(st.mean(rest), 3) if rest else None,
                    t_drop_best=round(t_of(rest), 2) if t_of(rest) is not None else None)

    report = {"generated": dt.datetime.now().isoformat(timespec="seconds"), "events": len(events),
              "prices_through": dates[-1], "windows": {}, "eras": {}, "note": __doc__.split("THE PRIOR")[1].strip()}
    print(f"{'window':<10}{'events':>7}{'weeks':>7}{'mean/wk':>9}{'t(wk)':>7}{'median':>8}{'hit%':>6}{'drop best wk':>14}{'t':>6}")
    for k in WIN:
        s = summarise(events, k); report["windows"][k] = s
        print(f"{k:<10}{s['n']:>7}{s['weeks']:>7}{s['mean_per_week']:>+9.2f}{s['t_week']:>7.2f}{s['median_event']:>+8.2f}{s['hit']:>6.0f}{s['drop_best_week']:>+14.2f}{s['t_drop_best']:>6.2f}")
    print("\nby era (excess vs SPY, mean per announcement week / week-clustered t):")
    for era, (a, b) in {"2011-15": ("2011", "2015"), "2016-20": ("2016", "2020"), "2021-26": ("2021", "2026")}.items():
        ev = [e for e in events if a <= e["print"][:4] <= b]
        line = f"  {era:<8}"
        report["eras"][era] = {}
        for k in WIN:
            s = summarise(ev, k); report["eras"][era][k] = s
            line += f"  {k} {s['mean_per_week']:+.2f} (t {s['t_week']:+.2f}, n {s['n']})"
        print(line)
    json.dump({**report, "rows": events}, open(OUT, "w"), indent=0)
    print(f"\nwritten {os.path.relpath(OUT, BASE)} · prices through {dates[-1]}")

if __name__ == "__main__":
    main()
