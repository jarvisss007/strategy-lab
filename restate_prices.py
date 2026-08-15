#!/usr/bin/env python
"""restate_prices.py — put the tape's price back into rows that recorded a wrong one.

Authorised by Anupam, 2026-08-14 ("correct everything"), after price_integrity.py
found 10 entries and 4 exits that disagree with radar.json by more than 2%.

WHAT WENT WRONG, stated precisely, because it is not what DATA-001 first said.
The recorded prices are not adjusted-vs-raw noise and not a wrong fill. Each one
is a REAL CLOSE FROM AN EARLIER BAR, stamped under a later date:

    GFS 53.18, HUM 381.15, TSLA 309.22, MOH 199.48  all recorded 2026-07-29
                                                    all = their 2026-07-27 close
    QBTS 16.21 recorded 08-04, 08-11, 08-13         = its 2026-07-24 close

Four unrelated tickers landing on the same prior bar is not a dividend
adjustment. radar.json served a stale bar under a fresh date; arena.py recorded
what it was told (entry_t agrees with entry_date on all 135 open rows, so nothing
drifted inside the run) and the number fossilised. The feed has since self-healed
— 07-29 and 08-13 read correctly today — but a written row is never re-read.

WHAT THIS DOES
Rewrites entry_px/exit_px to the feed's close for that ticker on that bar date,
then recomputes net, excess and mtm with arena.py's own formulas (net_ret, COST,
spy_ret) so the restated rows are arithmetically identical to rows the Arena
would have written had the feed been right.

WHAT IT REFUSES TO DO
Touch a row inside tolerance, touch a row the feed cannot verify, or change any
strategy's logic. The three same-bar round trips (REVERSAL_3, 2026-07-29) restate
to exactly -2*COST, which is the honest P&L of opening and closing at one close;
whether REVERSAL_3 should have opened them at all is a rule question for
REGISTRY.md, not a data question, and is left alone.

Every change is appended to reports/price_restatement_log.csv with its before and
after. The record stays a record: it is amended in the open, never quietly.

Run:  /opt/anaconda3/bin/python restate_prices.py --dry-run   # show, change nothing
      /opt/anaconda3/bin/python restate_prices.py --apply
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os

HOME = os.path.expanduser("~")
HERE = os.path.dirname(os.path.abspath(__file__))
RADAR = os.path.join(HOME, "stock-radar", "data", "radar.json")
TRADES = os.path.join(HERE, "reports", "arena_trades.csv")
STATE = os.path.join(HERE, "reports", "arena_state.json")
LOG = os.path.join(HERE, "reports", "price_restatement_log.csv")
DAY0 = dt.date(1970, 1, 1)
TOL = 0.02
COST = 0.001                      # arena.py:43 — same cost model, same round trip
COLS = ["strategy", "ticker", "side", "entry_date", "entry_px",
        "exit_date", "exit_px", "net", "excess", "regime", "tags"]


def d2iso(t):
    return (DAY0 + dt.timedelta(days=int(t))).isoformat()


def net_ret(entry, exit_, side):
    return side * (exit_ / entry - 1) - 2 * COST


def load_feed():
    """(close by ticker/date, close by ticker/epoch-day, spy series) from radar.json."""
    d = json.load(open(RADAR))
    eq = d["equities"] if isinstance(d, dict) else d
    by_iso, by_t = {}, {}
    for e in eq:
        tk = e.get("ticker")
        if not tk:
            continue
        pairs = [(t, c) for t, c in zip(e.get("series_t", []), e.get("series_c", [])) if c]
        by_iso[tk] = {d2iso(t): c for t, c in pairs}
        by_t[tk] = dict(pairs)
    strip = {s["ticker"]: s for s in (d.get("strip") or [])} if isinstance(d, dict) else {}
    spy = strip.get("SPY")
    spy_by_day = dict(zip(spy["series_t"], spy["series_c"])) if spy else {}
    return by_iso, by_t, spy_by_day, sorted(spy_by_day)


def make_spy_ret(spy_by_day, spy_days):
    def spy_ret(d_in, d_out):                       # arena.py:268, verbatim
        a, b = spy_by_day.get(d_in), spy_by_day.get(d_out)
        if a is None or b is None:
            pa = [d for d in spy_days if d <= d_in]
            pb = [d for d in spy_days if d <= d_out]
            if not pa or not pb or pa[-1] == pb[-1]:
                return None
            a, b = spy_by_day[pa[-1]], spy_by_day[pb[-1]]
        return b / a - 1
    return spy_ret


def iso2t(iso):
    return (dt.date.fromisoformat(iso) - DAY0).days


def wrong(recorded, feed):
    return feed is not None and abs(recorded - feed) / feed > TOL


def restate():
    by_iso, by_t, spy_by_day, spy_days = load_feed()
    spy_ret = make_spy_ret(spy_by_day, spy_days)
    changes = []

    # ---- closed rows -------------------------------------------------------
    rows = list(csv.DictReader(open(TRADES)))
    for r in rows:
        feed = by_iso.get(r["ticker"], {})
        ep, xp = float(r["entry_px"]), float(r["exit_px"])
        fe, fx = feed.get(r["entry_date"]), feed.get(r["exit_date"])
        bad_e, bad_x = wrong(ep, fe), wrong(xp, fx)
        # On a same-bar round trip the 2% tolerance does not apply. The tolerance
        # exists to ignore adjusted-vs-raw noise between two different bars; when
        # both legs ARE the same bar, any gap between them is definitionally an
        # error, and MOH (199.48 recorded, 199.02 on the tape, its 07-27 close)
        # slipped through the band at 0.23% while booking -0.43%.
        if r["entry_date"] == r["exit_date"] and fe is not None:
            bad_e = bad_e or abs(ep - fe) / fe > 1e-9
            bad_x = bad_x or abs(xp - fe) / fe > 1e-9
        if not (bad_e or bad_x):
            continue
        new_e = fe if bad_e else ep
        new_x = fx if bad_x else xp
        side = int(r["side"])
        old_net, old_ex = r["net"], r["excess"]
        nr = net_ret(new_e, new_x, side)
        sp = spy_ret(iso2t(r["entry_date"]), iso2t(r["exit_date"]))
        r["entry_px"], r["exit_px"] = round(new_e, 4), round(new_x, 4)
        r["net"] = round(nr, 5)
        r["excess"] = round(nr - sp, 5) if sp is not None else ""
        changes.append({"scope": "closed", "strategy": r["strategy"], "ticker": r["ticker"],
                        "entry_date": r["entry_date"], "exit_date": r["exit_date"],
                        "field": "entry+exit" if (bad_e and bad_x) else
                                 ("entry" if bad_e else "exit"),
                        "old_entry_px": ep, "new_entry_px": r["entry_px"],
                        "old_exit_px": xp, "new_exit_px": r["exit_px"],
                        "old_net": old_net, "new_net": r["net"],
                        "old_excess": old_ex, "new_excess": r["excess"]})

    # ---- open rows ---------------------------------------------------------
    state = json.load(open(STATE))
    for p in state["open"]:
        feed = by_iso.get(p["ticker"], {})
        ep = float(p["entry_px"])
        fe = feed.get(p["entry_date"])
        if not wrong(ep, fe):
            continue
        series = by_t.get(p["ticker"], {})
        cur = series[max(series)] if series else None
        old_mtm = p.get("mtm")
        p["entry_px"] = round(fe, 4)
        if cur is not None:
            p["mtm"] = round(p["side"] * (cur / fe - 1) - 2 * COST, 5)
        changes.append({"scope": "open", "strategy": p["strategy"], "ticker": p["ticker"],
                        "entry_date": p["entry_date"], "exit_date": "",
                        "field": "entry", "old_entry_px": ep, "new_entry_px": p["entry_px"],
                        "old_exit_px": "", "new_exit_px": "",
                        "old_net": old_mtm, "new_net": p.get("mtm"),
                        "old_excess": "", "new_excess": ""})
    return rows, state, changes


def write(rows, state, changes):
    with open(TRADES, "w") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLS})
    json.dump(state, open(STATE, "w"), indent=1)

    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M PT")
    cols = ["restated_at", "scope", "strategy", "ticker", "entry_date", "exit_date",
            "field", "old_entry_px", "new_entry_px", "old_exit_px", "new_exit_px",
            "old_net", "new_net", "old_excess", "new_excess", "reason"]
    new = not os.path.exists(LOG)
    with open(LOG, "a") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        if new:
            w.writeheader()
        for c in changes:
            w.writerow({**c, "restated_at": stamp,
                        "reason": "stale bar recorded under a later date (DATA-001)"})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    rows, state, changes = restate()
    if not changes:
        print("Nothing to restate — every verifiable price already matches the tape.")
        return
    print(f"\n{len(changes)} rows disagree with the tape by more than {TOL:.0%}\n")
    print(f"  {'scope':<7}{'strategy':<14}{'tick':<6}{'entry':<12}{'field':<11}"
          f"{'net now':>10}{'restated':>10}")
    for c in changes:
        on = c["old_net"] if c["old_net"] not in ("", None) else 0
        print(f"  {c['scope']:<7}{c['strategy']:<14}{c['ticker']:<6}{c['entry_date']:<12}"
              f"{c['field']:<11}{100*float(on):>9.2f}%{100*float(c['new_net']):>9.2f}%")
    if not a.apply:
        print("\n  dry run — nothing written. Re-run with --apply.")
        return
    write(rows, state, changes)
    print(f"\n  written. {len(changes)} rows amended, every change logged to")
    print(f"  {os.path.relpath(LOG, HERE)} with its before and after.")


if __name__ == "__main__":
    main()
