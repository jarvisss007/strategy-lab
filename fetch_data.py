#!/usr/bin/env python3
"""Pull long daily history for the Stock Radar universe + SPY benchmark from
Yahoo's free endpoint. Writes data/prices.csv (a wide close-price panel) and
data/meta.json. Run: /opt/anaconda3/bin/python fetch_data.py"""
import csv, json, os, time, urllib.request
from datetime import datetime, timezone

from panel_guard import report, trim_incomplete_tail

BASE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
RANGE = "15y"


def universe():
    wl = os.path.join(os.path.expanduser("~"), "stock-radar", "watchlist.csv")
    tick = ["SPY"]
    with open(wl) as f:
        for row in csv.DictReader(f):
            y = row["yahoo"].strip()
            if y and y not in tick:
                tick.append(y)
    return tick


def fetch(sym, retries=3):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={RANGE}&interval=1d"
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            d = json.load(urllib.request.urlopen(req, timeout=25))
            r = d["chart"]["result"][0]
            ts = r["timestamp"]
            # adjusted close preferred (splits/divs); fall back to raw close
            adj = r["indicators"].get("adjclose", [{}])[0].get("adjclose")
            close = r["indicators"]["quote"][0]["close"]
            series = adj if adj else close
            return {
                datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d"): c
                for t, c in zip(ts, series) if c is not None
            }
        except Exception:
            if i == retries - 1:
                return None
            time.sleep(2 * (i + 1))


def main():
    tick = universe()
    panel, ok, fail = {}, [], []
    for s in tick:
        d = fetch(s)
        if d and len(d) > 60:
            panel[s] = d
            ok.append(s)
        else:
            fail.append(s)
        time.sleep(0.2)

    # union of all dates, sorted
    all_dates = sorted({dt for d in panel.values() for dt in d})

    # Refuse to overwrite a good panel with a bad fetch. On 2026-08-03 the Mac
    # had no DNS at refresh time, every ticker failed, and this function
    # truncated prices.csv to a bare header and meta.json to 0 bytes (IndexError
    # on all_dates[0]) — destroying 15y of panel over a transient outage. A
    # fetch that lost most of the universe is a network problem, not new data:
    # leave the last good file in place and exit non-zero so the log shows it.
    if len(ok) < 0.8 * len(tick) or not all_dates:
        print(f"ABORT: only {len(ok)}/{len(tick)} tickers fetched — keeping the "
              f"existing panel untouched; failed: {fail[:10]}")
        raise SystemExit(1)

    # Same posture, other end of the axis: a trailing bar most of the universe has
    # not traded is the clock, not new data (see panel_guard.py).
    all_dates, dropped = trim_incomplete_tail(all_dates, panel, ok)
    report(dropped)
    if not all_dates:
        print("ABORT: every fetched date was an incomplete bar — panel untouched")
        raise SystemExit(1)

    with open(os.path.join(BASE, "data", "prices.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date"] + ok)
        for dt in all_dates:
            w.writerow([dt] + [panel[s].get(dt, "") for s in ok])

    with open(os.path.join(BASE, "data", "meta.json"), "w") as f:
        json.dump({
            "built": datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z"),
            "range": RANGE, "n_tickers": len(ok), "n_dates": len(all_dates),
            "start": all_dates[0], "end": all_dates[-1],
            "tickers": ok, "failed": fail,
        }, f, indent=1)
    print(f"OK {len(ok)} tickers, {len(all_dates)} dates {all_dates[0]}..{all_dates[-1]}; failed: {fail}")


if __name__ == "__main__":
    main()
