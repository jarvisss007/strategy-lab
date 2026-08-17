#!/usr/bin/env python
"""rotation_arm.py — Anupam's cull-losers-feed-winners overlay, run as a paper arm.

Registered in REGISTRY.md 2026-08-17 BEFORE this file first ran, with the desk's
prediction on the record: the overlay UNDERPERFORMS the base book (p≈0.65),
because this book's losers are mid-dip by design, because paper_account's own
"size up on wins" arm already trails its flat arm, and because
accumulate-the-winner is a months-horizon effect applied here at days. His idea
deserves a real test, not agreement — and if it wins past day-clustered noise,
the desk says so.

THE RULE (frozen; changing it resets the record):
  · Each post-close run, take the Arena's open book and its mtm marks.
  · CULL any position with mtm < −2%: it exits the overlay at the current mark.
  · Its weight is reallocated equally across the TOP QUARTILE of open positions
    by mtm ("accumulate in the position which is doing good").
  · New Arena entries arrive at weight 1.0. Positions the Arena itself closes
    leave both books at the same mark.
  · Every forced exit and every re-entry pays COST each way, same model as the
    Arena (arena.py:43) — rotation is not free.

SCORING: overlay NAV vs base NAV (same open set, equal weight, held to expiry),
both from 100. Daily rows in reports/rotation_log.csv; state in
reports/rotation_book.json. Day-clustered by construction — one row per session.

This file changes NOTHING in the Arena. It reads arena_state.json and radar.json
and writes only its own two files. The frozen agents' record stays theirs.

Run:  /opt/anaconda3/bin/python rotation_arm.py       (wired into refresh_all.sh)
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import os

HOME = os.path.expanduser("~")
HERE = os.path.dirname(os.path.abspath(__file__))
RADAR = os.path.join(HOME, "stock-radar", "data", "radar.json")
STATE = os.path.join(HERE, "reports", "arena_state.json")
BOOK = os.path.join(HERE, "reports", "rotation_book.json")
LOG = os.path.join(HERE, "reports", "rotation_log.csv")
COST = 0.001                 # arena.py:43
CULL_AT = -0.02              # mtm below this is a loser, per the registered rule
DAY0 = dt.date(1970, 1, 1)


def key(p):
    return f"{p['strategy']}|{p['ticker']}|{p['entry_date']}"


def last_two_closes():
    d = json.load(open(RADAR))
    out = {}
    for e in d.get("equities", []):
        c = [x for x in e.get("series_c", []) if x]
        if len(c) >= 2 and e.get("ticker"):
            out[e["ticker"]] = (c[-2], c[-1])
    return out


def main():
    opens = json.load(open(STATE))["open"]
    px = last_two_closes()
    today = dt.date.today().isoformat()

    book = {"start": today, "nav_base": 100.0, "nav_rot": 100.0,
            "weights": {}, "last_run": None}
    if os.path.exists(BOOK):
        book = json.load(open(BOOK))
    if book.get("last_run") == today:
        print("rotation_arm: already ran today — one row per session, refusing a second")
        return

    cur = {key(p): p for p in opens}

    # ---- daily return of each open position (yesterday close -> today close) --
    rets = {}
    for k, p in cur.items():
        pr = px.get(p["ticker"])
        if pr and pr[0]:
            rets[k] = pr[1] / pr[0] - 1

    w = book["weights"]
    # positions the Arena closed leave both books; new entries arrive at 1.0
    w = {k: v for k, v in w.items() if k in cur}
    for k in cur:
        w.setdefault(k, 1.0)

    # ---- NAV update on the day's returns (skip day one: no held period yet) ---
    if book.get("last_run") and rets:
        held = [k for k in rets if k in w]
        if held:
            base_r = sum(rets[k] for k in held) / len(held)
            tot = sum(w[k] for k in held)
            rot_r = sum(w[k] * rets[k] for k in held) / tot if tot else 0.0
            book["nav_base"] = round(book["nav_base"] * (1 + base_r), 4)
            book["nav_rot"] = round(book["nav_rot"] * (1 + rot_r), 4)

    # ---- the registered rule: cull losers, feed the top quartile -------------
    marks = {k: cur[k].get("mtm", 0.0) for k in cur}
    culled = [k for k in w if marks.get(k, 0.0) < CULL_AT]
    survivors = [k for k in w if k not in culled]
    boosted = []
    if culled and survivors:
        ranked = sorted(survivors, key=lambda k: -marks.get(k, 0.0))
        top = ranked[:max(1, len(ranked) // 4)]
        freed = sum(w[k] for k in culled)
        # each forced exit and each re-entry pays its way
        friction = freed * COST + freed * COST
        add = max(freed - friction * 100 / book["nav_rot"], 0.0) / len(top)
        for k in top:
            w[k] = round(w[k] + add, 4)
        boosted = top
        for k in culled:
            del w[k]
    elif culled:                      # nothing left to feed — hold the cash flat
        for k in culled:
            del w[k]

    book["weights"] = w
    book["last_run"] = today
    json.dump(book, open(BOOK, "w"), indent=1)

    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="") as f:
        wcsv = csv.writer(f)
        if new:
            wcsv.writerow(["date", "nav_base", "nav_rot", "gap_pct", "n_open",
                           "n_culled", "n_boosted", "culled", "boosted"])
        wcsv.writerow([today, book["nav_base"], book["nav_rot"],
                       round(book["nav_rot"] - book["nav_base"], 4), len(w),
                       len(culled), len(boosted),
                       ";".join(k.split("|")[1] for k in culled),
                       ";".join(k.split("|")[1] for k in boosted)])
    print(f"rotation_arm {today}: base {book['nav_base']:.2f} · overlay "
          f"{book['nav_rot']:.2f} · gap {book['nav_rot']-book['nav_base']:+.2f} · "
          f"culled {len(culled)}, boosted {len(boosted)} of {len(w)} open")


if __name__ == "__main__":
    main()
