#!/usr/bin/env python3
"""Pull 15y daily OHLC for the universe and write split/dividend-adjusted OPEN and
CLOSE panels — needed for structural/friction strategies (overnight vs intraday).
Adjusted open = open * (adjclose/close), so overnight gaps aren't polluted by splits.
Writes data/open.csv and data/close.csv. Run: /opt/anaconda3/bin/python fetch_ohlc.py"""
import csv, json, os, time, urllib.request
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
RANGE = "15y"


def universe():
    wl = os.path.join(os.path.expanduser("~"), "stock-radar", "watchlist.csv")
    tick = ["SPY"]
    with open(wl) as f:
        for r in csv.DictReader(f):
            y = r["yahoo"].strip()
            if y and y not in tick:
                tick.append(y)
    return tick


def fetch(sym, retries=3):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={RANGE}&interval=1d"
    for i in range(retries):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25))
            r = d["chart"]["result"][0]
            ts = r["timestamp"]
            q = r["indicators"]["quote"][0]
            adj = r["indicators"].get("adjclose", [{}])[0].get("adjclose")
            o, c = q["open"], q["close"]
            adj = adj if adj else c
            out = {}
            for t, oo, cc, ac in zip(ts, o, c, adj):
                if oo and cc and ac:
                    day = datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d")
                    factor = ac / cc
                    out[day] = (round(oo * factor, 4), round(ac, 4))   # (adj_open, adj_close)
            return out
        except Exception:
            if i == retries - 1:
                return None
            time.sleep(2 * (i + 1))


def main():
    tick = universe()
    opens, closes, ok = {}, {}, []
    for s in tick:
        d = fetch(s)
        if d and len(d) > 200:
            opens[s] = {k: v[0] for k, v in d.items()}
            closes[s] = {k: v[1] for k, v in d.items()}
            ok.append(s)
        time.sleep(0.2)
    dates = sorted({dt for d in closes.values() for dt in d})
    for name, panel in (("open", opens), ("close", closes)):
        with open(os.path.join(BASE, "data", f"{name}.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["date"] + ok)
            for dt in dates:
                w.writerow([dt] + [panel[s].get(dt, "") for s in ok])
    print(f"OK {len(ok)} tickers, {len(dates)} dates {dates[0]}..{dates[-1]}")


if __name__ == "__main__":
    main()
