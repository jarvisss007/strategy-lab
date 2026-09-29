#!/usr/bin/env python3
"""Pull long daily history for the Stock Radar universe + SPY benchmark from
Yahoo's free endpoint. Writes data/prices.csv (a wide close-price panel) and
data/meta.json. Run: /opt/anaconda3/bin/python fetch_data.py

SCHEDULE (ARENA-008, 2026-09-29): weekdays after the close via com.anupam.strategylab-prices
(with a bounded retry), plus the Monday branch of refresh_all.sh. Until 2026-09-29 the Monday
06:0x run was the ONLY caller, so the panel ended on the previous Friday and read one session
stale from every Monday afternoon on.

WRITES: prices.csv and meta.json are written beside and swapped in with os.replace() through
atomicio (BOOK-001) - the options desk's 15y-history gate and the Arena's universe read this
file, and open(path, "w") truncates it first.

SETTLED SESSIONS ONLY: no date after the last settled session (stock-radar/sessions.py) is ever
written - Yahoo carries the current session as a bar whose "close" is the last trade.

EXIT: 0 = the panel ends at the last settled session; 1 = ABORT, panel untouched; 3 = a panel was
written but ends BEFORE the last settled session (Yahoo's final bar is not out yet) - retry."""
import csv, io, json, os, time, urllib.request
from datetime import datetime, timedelta, timezone

from atomicio import atomic_json, atomic_write_text   # BOOK-001: never truncate a book in place
from panel_guard import report, trim_incomplete_tail

BASE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
RANGE = "15y"

# SESSION-001: the estate's one NYSE calendar is stock-radar/sessions.py, loaded by path (this repo
# is public and runs alone); a weekday/clock fallback if it is unavailable - and it says so.
try:
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("_sessions", os.path.join(os.path.expanduser("~"), "stock-radar", "sessions.py"))
    _SESS = _iu.module_from_spec(_sp); _sp.loader.exec_module(_SESS)
except Exception:
    _SESS = None


def settled_session():
    """ISO date of the last session whose close is settled (PT clock)."""
    if _SESS is not None:
        try:
            return _SESS.settled_session().isoformat()
        except Exception as e:   # e.g. CalendarExhausted past the calendar's horizon: refuse, never guess
            print(f"ABORT: cannot establish the last settled session ({type(e).__name__}: {e}) - panel untouched")
            raise SystemExit(1)
    print("WARNING: stock-radar/sessions.py unavailable - last settled session ESTIMATED from the weekday "
          "and the 13:05 PT clock (holidays unknown)")
    try:
        from zoneinfo import ZoneInfo
        now = datetime.now(ZoneInfo("America/Los_Angeles"))
    except Exception:
        now = datetime.now()
    d = now.date()
    if d.weekday() >= 5 or (now.hour, now.minute) < (13, 5):
        d -= timedelta(days=1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d.isoformat()


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
    # Read BEFORE the fetches, so it is the clock at fetch start: a cutoff crossed mid-run must
    # never admit a bar that was fetched before it.
    settled = settled_session()
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

    # SETTLED PRICES ONLY (ARENA-008, 2026-09-29). Yahoo carries the CURRENT session as a bar
    # too, and while it forms its "close" is the last trade, not a close (verified 2026-09-29
    # 08:20 PT: SPY's 09-29 bar held the live price). The coverage test below cannot see that -
    # a forming equity bar is ~100% covered - so run intraday this writer would record a forming
    # price as a settled close in the 15y panel the options desk's history gate and the Arena's
    # universe read. Nothing after the last SETTLED session is written; the first run after the
    # close picks the session up whole.
    unsettled = [d for d in all_dates if d > settled]
    if unsettled:
        all_dates = [d for d in all_dates if d <= settled]
        print(f"  UNSETTLED BAR dropped: {', '.join(unsettled)} — after the last settled session "
              f"{settled}; a forming bar is not a close")

    # Same posture, other end of the axis: a trailing bar most of the universe has
    # not traded is the clock, not new data (see panel_guard.py).
    all_dates, dropped = trim_incomplete_tail(all_dates, panel, ok)
    report(dropped)
    if not all_dates:
        print("ABORT: every fetched date was an unsettled or incomplete bar — panel untouched")
        raise SystemExit(1)

    # BOOK-001: the whole panel is built in memory and swapped in with os.replace() - a reader
    # sees the old panel or the new one, never a truncated file. CRLF row endings are kept
    # (csv.writer's default, byte-for-byte what open(..., newline="") wrote before).
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["date"] + ok)
    for dt in all_dates:
        w.writerow([dt] + [panel[s].get(dt, "") for s in ok])
    atomic_write_text(os.path.join(BASE, "data", "prices.csv"), buf.getvalue())

    atomic_json(os.path.join(BASE, "data", "meta.json"), {
        "built": datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z"),
        "range": RANGE, "n_tickers": len(ok), "n_dates": len(all_dates),
        "start": all_dates[0], "end": all_dates[-1],
        "settled_session": settled,
        "tickers": ok, "failed": fail,
    }, indent=1)
    print(f"OK {len(ok)} tickers, {len(all_dates)} dates {all_dates[0]}..{all_dates[-1]}; failed: {fail}")
    if all_dates[-1] < settled:
        # A panel that ends before the last settled session is the failure ARENA-008 exists for; a
        # scheduler must SEE it (rc 3), not read a clean zero.
        print(f"STALE: the panel ends {all_dates[-1]} but the last settled session is {settled} — Yahoo has "
              "not published that session's final bar for enough of the universe yet; wrote what is final, "
              "exiting 3 so the scheduler retries")
        raise SystemExit(3)


if __name__ == "__main__":
    main()
