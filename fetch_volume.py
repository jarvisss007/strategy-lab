#!/usr/bin/env python3
"""Pull 15y daily VOLUME for the universe (for microstructure/liquidity hypotheses).
Writes data/volume.csv. Run: /opt/anaconda3/bin/python fetch_volume.py"""
import csv, json, os, time, urllib.request
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


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
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=15y&interval=1d"
    for i in range(retries):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25))
            r = d["chart"]["result"][0]
            v = r["indicators"]["quote"][0]["volume"]
            return {datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d"): vv
                    for t, vv in zip(r["timestamp"], v) if vv is not None}
        except Exception:
            if i == retries - 1:
                return None
            time.sleep(2 * (i + 1))


def main():
    vol, ok = {}, []
    for s in universe():
        d = fetch(s)
        if d and len(d) > 200:
            vol[s] = d; ok.append(s)
        time.sleep(0.2)
    dates = sorted({dt for d in vol.values() for dt in d})
    with open(os.path.join(BASE, "data", "volume.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date"] + ok)
        for dt in dates:
            w.writerow([dt] + [vol[s].get(dt, "") for s in ok])
    print(f"OK {len(ok)} tickers, {len(dates)} dates {dates[0]}..{dates[-1]}")


if __name__ == "__main__":
    main()
