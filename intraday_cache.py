#!/usr/bin/env python3
"""Shared intraday data cache for the intraday-research suite. Pulls 15m OHLC (~1
month, ~20 sessions, 26 bars/day — good resolution) for the universe and writes
data/intraday.json = {ticker: {date: [[HHMM, open, high, low, close], ...]}}.
Feeds intraday_study.py, intraday_discover.py, and the dashboard.
Run: /opt/anaconda3/bin/python intraday_cache.py [interval] [range]"""
import csv, json, os, sys, time, urllib.request, datetime as dt
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
ITV = sys.argv[1] if len(sys.argv) > 1 else "15m"
RNG = sys.argv[2] if len(sys.argv) > 2 else "1mo"


def universe():
    wl = os.path.join(os.path.expanduser("~"), "stock-radar", "watchlist.csv")
    with open(wl) as f:
        return ["SPY"] + [r["yahoo"].strip() for r in csv.DictReader(f) if r["yahoo"].strip()]


def fetch(sym, retries=3):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={RNG}&interval={ITV}"
    for i in range(retries):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25))
            r = d["chart"]["result"][0]
            q = r["indicators"]["quote"][0]
            days = defaultdict(list)
            for t, o, h, l, c in zip(r["timestamp"], q["open"], q["high"], q["low"], q["close"]):
                if None in (o, h, l, c):
                    continue
                x = dt.datetime.fromtimestamp(t)
                days[x.strftime("%Y-%m-%d")].append([x.strftime("%H:%M"),
                    round(o, 4), round(h, 4), round(l, 4), round(c, 4)])
            return {d: b for d, b in days.items() if len(b) >= 6}
        except Exception:
            if i == retries - 1:
                return None
            time.sleep(2 * (i + 1))


def main():
    out, ok, fail = {}, [], []
    tick = list(dict.fromkeys(universe()))
    for s in tick:
        d = fetch(s)
        if d and len(d) >= 8:
            out[s] = d; ok.append(s)
        else:
            fail.append(s)
        time.sleep(0.15)
    meta = {"interval": ITV, "range": RNG, "n": len(ok),
            "built": dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z"), "failed": fail}
    json.dump({"meta": meta, "data": out}, open(os.path.join(BASE, "data", f"intraday_{ITV}.json"), "w"))
    print(f"OK {len(ok)} tickers cached ({ITV}/{RNG}); failed {len(fail)}: {fail[:8]}")


if __name__ == "__main__":
    main()
