#!/usr/bin/env python3
"""Intraday day-type RECORDER — the accumulation engine. Runs after the close each
weekday, computes the full day-type + intraday-strategy outcomes for every active
name, and APPENDS one row per name to daytype_log.csv. Over months this turns the
~20 sessions Yahoo hands us into a real dataset where the intraday tests become
conclusive. Idempotent: won't double-log a date. Run after ~1:10pm PT.
Run: /opt/anaconda3/bin/python record_daytype.py"""
import csv, json, os, time, urllib.request, datetime as dt
from collections import defaultdict
import numpy as np
import intraday_discover as ID

BASE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0"}
LOG = os.path.join(BASE, "daytype_log.csv")
COLS = ["date", "ticker", "open", "close", "net_pct", "path_pct", "eff", "regime",
        "swing_count", "or_breakout_ret", "open_fade_ret", "first_hour_dir", "closed_dir"]


def active_names():
    try:
        d = json.load(open(os.path.join(BASE, "reports", "universe_daytype.json")))
        return [r["ticker"] for r in d["rows"] if r["character"] != "QUIET"]
    except Exception:
        wl = os.path.join(os.path.expanduser("~"), "stock-radar", "watchlist.csv")
        return [r["yahoo"].strip() for r in csv.DictReader(open(wl)) if r["yahoo"].strip()]


def today_bars(sym):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=5d&interval=15m"
    try:
        d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25))
        r = d["chart"]["result"][0]; q = r["indicators"]["quote"][0]
        days = defaultdict(list)
        for t, o, h, l, c in zip(r["timestamp"], q["open"], q["high"], q["low"], q["close"]):
            if None not in (o, h, l, c):
                x = dt.datetime.fromtimestamp(t)
                days[x.strftime("%Y-%m-%d")].append([x.strftime("%H:%M"), o, h, l, c])
        if not days:
            return None, None
        last = max(days)
        return last, days[last]
    except Exception:
        return None, None


def analyze(bars):
    px = [b[4] for b in bars]
    o, c = bars[0][1], px[-1]
    net = c - o
    path = sum(abs(px[i] - px[i - 1]) for i in range(1, len(px)))
    eff = abs(net) / path if path else 0.0
    swings = sum(1 for i in range(1, len(px)) if (px[i] - px[i - 1]) * (px[i - 1] - px[i - 2]) < 0
                 for _ in [0]) if len(px) > 2 else 0
    regime = "TREND" if eff >= 0.40 else "CHOP" if eff < 0.20 else "MIXED"
    return {"open": round(o, 2), "close": round(c, 2), "net_pct": round(net / o * 100, 2),
            "path_pct": round(path / o * 100, 1), "eff": round(eff, 3), "regime": regime,
            "swing_count": swings,
            "or_breakout_ret": round((ID.or_breakout(bars) or 0) * 100, 3),
            "open_fade_ret": round((ID.open_fade(bars) or 0) * 100, 3),
            "first_hour_dir": int(np.sign(bars[4][4] - o)) if len(bars) > 4 else 0,
            "closed_dir": int(np.sign(net))}


def already_logged(date):
    if not os.path.exists(LOG):
        return False
    with open(LOG) as f:
        return any(row["date"] == date for row in csv.DictReader(f))


def main():
    names = active_names()
    rows, logdate = [], None
    for s in names:
        date, bars = today_bars(s)
        if bars and len(bars) >= 8:
            logdate = date
            rows.append({"date": date, "ticker": s, **analyze(bars)})
        time.sleep(0.15)
    if not rows:
        print("no intraday data (market closed/holiday?) — nothing recorded")
        return
    if already_logged(logdate):
        print(f"{logdate} already recorded ({len(rows)} names would duplicate) — skipping")
        return
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        if new:
            w.writeheader()
        w.writerows(rows)
    total = sum(1 for _ in open(LOG)) - 1
    print(f"recorded {len(rows)} names for {logdate}. daytype_log.csv now has {total} rows.")


if __name__ == "__main__":
    main()
