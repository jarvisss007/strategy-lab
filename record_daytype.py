#!/usr/bin/env python3
"""Intraday day-type RECORDER — the accumulation engine. Runs after the close each
weekday, computes the full day-type + intraday-strategy outcomes for every active
name, and APPENDS one row per name to daytype_log.csv. Over months this turns the
~20 sessions Yahoo hands us into a real dataset where the intraday tests become
conclusive. Idempotent: won't double-log a date. Run after ~1:10pm PT.
Run: /opt/anaconda3/bin/python record_daytype.py

DAYTYPE-001 (2026-10-09): THE RECORDER NO LONGER GATES ON THE QUIET LABEL. It used to fetch only the names universe_daytype.json labels non-QUIET (trailing-21-session
average zigzag path >= an absolute 8%, a floor calibrated on SNDK that the 2026-08-05 audit kept ABSOLUTE on purpose). As realised intraday volatility fell across
August and September the set shrank with every weekly rebuild - 30 names a day in July, 28, 24, 14, 7, 3, 1 - and on 2026-09-28 it reached zero, so no row was
written for nine sessions (2026-09-28..10-08) while the old task reported "market closed". The measurements were right (fresh 15m bars, 26 a day, current to
2026-10-08; the session hi-lo range of the same names, a measure independent of the zigzag path, fell in step: NBIS 7.3% -> 4.0% over 21-session means): the
market really was quiet by that floor. The defect was
the coupling: a LABEL used as a collection GATE, so the dataset stopped accumulating in exactly the calm regimes any intraday test needs for contrast, and
conditioning on trailing volatility stamped a regime onto the sample. The label stays as it was (a threshold is Anupam's call, not this file's); it just
no longer decides what is recorded. record_names() = every ticker the universe profiled (QUIET included), or the watchlist when that file is missing or empty.
Rows already in the log hold only the names that were non-QUIET at that week's rebuild; from 2026-10-09 the log holds the whole universe, so a reader that pools
across the boundary mixes two sampling rules (filter on the earlier tickers, or on the date).
THE GAP IS RECORDED, NOT BACKFILLED. The 15m bars for 2026-09-28..10-08 are still on Yahoo's 60-day window, but a replay is NOT what a live run writes: replaying
the 743 logged name-days still inside the window reproduces 112 of them exactly (15%) - the live run at 13:15 PT reads a last bar that is still forming (AMD
2026-08-04 logged close 518.58, replayed 526.00; INFQ 2026-09-25 logged 14.51, replayed 14.52). Rows written now would be a different instrument from the rows
already in the file, so the nine sessions are listed in daytype_gaps.csv instead (one row per lost session, with the reason).
Flags: --dry-run  fetch and print what WOULD be recorded (names, date, regime counts); write nothing."""
import csv, json, os, sys, time, urllib.request, datetime as dt
from collections import defaultdict
import numpy as np
import intraday_discover as ID

BASE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0"}
LOG = os.path.join(BASE, "daytype_log.csv")
COLS = ["date", "ticker", "open", "close", "net_pct", "path_pct", "eff", "regime",
        "swing_count", "or_breakout_ret", "open_fade_ret", "first_hour_dir", "closed_dir"]


def _universe_rows():
    """The universe profiler's rows, or None when the file is missing, unreadable or has no rows."""
    try:
        rows = json.load(open(os.path.join(BASE, "reports", "universe_daytype.json")))["rows"]
        return rows or None
    except Exception:
        return None


def active_names():
    """The names the universe labels non-QUIET. A LABEL, kept for the dashboard and for readers; since DAYTYPE-001 it no longer decides what is recorded."""
    rows = _universe_rows()
    if rows is not None:
        return [r["ticker"] for r in rows if r["character"] != "QUIET"]
    return _watchlist()


def _watchlist():
    wl = os.path.join(os.path.expanduser("~"), "stock-radar", "watchlist.csv")
    try:
        return [r["yahoo"].strip() for r in csv.DictReader(open(wl)) if r["yahoo"].strip()]
    except Exception:
        return []


def record_names():
    """DAYTYPE-001. Every name to record each session: the whole universe the profiler rated (QUIET included), else the watchlist. Never gated on the label."""
    rows = _universe_rows()
    if rows is not None:
        return [r["ticker"] for r in rows]
    return _watchlist()


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


def main(argv=None):
    dry = "--dry-run" in (sys.argv[1:] if argv is None else argv)
    names = record_names()
    rows, logdate, nodata = [], None, []
    for s in names:
        date, bars = today_bars(s)
        if bars and len(bars) >= 8:
            logdate = date
            rows.append({"date": date, "ticker": s, **analyze(bars)})
        else:
            nodata.append(s)
        time.sleep(0.15)
    if not rows:
        print(f"no intraday data (market closed/holiday?) — nothing recorded ({len(names)} names asked)")
        return
    miss = f" ({len(nodata)} of {len(names)} names returned no bars: {', '.join(nodata[:12])}{' ...' if len(nodata) > 12 else ''})" if nodata else ""
    if dry:
        from collections import Counter
        mix = dict(Counter(r["regime"] for r in rows))
        dup = already_logged(logdate)
        print(f"DRY RUN - nothing written. Would record {len(rows)} names for {logdate}{miss}; regimes {mix}; "
              f"{'that date is ALREADY in the log, so a real run would skip it' if dup else 'that date is not in the log yet'}.")
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
    print(f"recorded {len(rows)} names for {logdate}. daytype_log.csv now has {total} rows.{miss}")


if __name__ == "__main__":
    main()
