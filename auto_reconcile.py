#!/usr/bin/env python
"""auto_reconcile.py — every run, re-check the last session's fills against the settled feed.

DATA-002, ruled by Anupam 2026-08-15: auto-reconcile. This is the standing job
that ruling authorises, and it is deliberately built to obey BENCH-002 rather than
collide with it — because the obvious implementation collides with it every single
day, automatically, which is strictly worse than the one-off hand correction that
started all this.

THE PROBLEM IT CLOSES
radar.json is a rolling window that gets CORRECTED on later refreshes; the Arena
writes an immutable row at the instant of the run. When the feed is briefly wrong,
the Arena fossilises it and nothing ever re-reads the row. QBTS sat at 16.21 —
its 2026-07-24 close — on entries dated 08-04, 08-11 and 08-13, and the thing that
finally caught it was Anupam reading his own portfolio.

THE TWO RULES IT HOLDS AT ONCE

  OPEN rows      repaired IN PLACE. An open position has no recorded outcome for
                 BENCH-002 to protect, and marking a live position off a price
                 that never traded is precisely the DATA-001 defect. mtm is
                 recomputed with arena.py's own cost model.

  CLOSED rows    NEVER overwritten. The tape's view is written into the companion
                 columns (entry_px_tape / exit_px_tape / net_tape / excess_tape),
                 so the divergence is DECLARED the next morning instead of waiting
                 for someone to notice it eleven days later. BENCH-002: "a
                 corrected value may be added as a NEW column; a recorded outcome
                 is never overwritten."

That split is the whole design. Auto-reconciliation earns its standing permission
precisely because it can only ever ADD to a scored row.

IDEMPOTENT. Safe to run every session: a row already matching the feed, or already
carrying the same declared tape value, is left untouched and logged nothing. It
writes only when something actually changed.

Run:  /opt/anaconda3/bin/python auto_reconcile.py            # reconcile and log
      /opt/anaconda3/bin/python auto_reconcile.py --dry-run
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")
RADAR = os.path.join(HOME, "stock-radar", "data", "radar.json")
TRADES = os.path.join(HERE, "reports", "arena_trades.csv")
STATE = os.path.join(HERE, "reports", "arena_state.json")
LOG = os.path.join(HERE, "reports", "price_restatement_log.csv")
DAY0 = dt.date(1970, 1, 1)
TOL = 0.02
COST = 0.001
COLS = ["strategy", "ticker", "side", "entry_date", "entry_px",
        "exit_date", "exit_px", "net", "excess", "regime", "tags",
        "entry_px_tape", "exit_px_tape", "net_tape", "excess_tape"]


def d2iso(t):
    return (DAY0 + dt.timedelta(days=int(t))).isoformat()


def iso2t(s):
    return (dt.date.fromisoformat(s) - DAY0).days


def feed():
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
    sp = dict(zip(spy["series_t"], spy["series_c"])) if spy else {}
    return by_iso, by_t, sp, sorted(sp)


def make_spy_ret(sp, days):
    def spy_ret(a_, b_):                       # arena.py:268, verbatim
        a, b = sp.get(a_), sp.get(b_)
        if a is None or b is None:
            pa = [d for d in days if d <= a_]
            pb = [d for d in days if d <= b_]
            if not pa or not pb or pa[-1] == pb[-1]:
                return None
            a, b = sp[pa[-1]], sp[pb[-1]]
        return b / a - 1
    return spy_ret


def off(recorded, truth):
    return truth is not None and abs(float(recorded) - truth) / truth > TOL


def reconcile():
    by_iso, by_t, sp, spdays = feed()
    spy_ret = make_spy_ret(sp, spdays)
    changes = []

    # ---- OPEN: repair in place; no scored outcome exists to protect ----------
    state = json.load(open(STATE))
    for p in state["open"]:
        truth = by_iso.get(p["ticker"], {}).get(p["entry_date"])
        if not off(p["entry_px"], truth):
            continue
        old = float(p["entry_px"])
        series = by_t.get(p["ticker"], {})
        cur = series[max(series)] if series else None
        p["entry_px"] = round(truth, 4)
        if cur is not None:
            p["mtm"] = round(p["side"] * (cur / truth - 1) - 2 * COST, 5)
        changes.append({"scope": "open", "strategy": p["strategy"], "ticker": p["ticker"],
                        "entry_date": p["entry_date"], "exit_date": "",
                        "field": "entry REPAIRED in place",
                        "old_entry_px": old, "new_entry_px": p["entry_px"],
                        "old_exit_px": "", "new_exit_px": "",
                        "old_net": "", "new_net": p.get("mtm"),
                        "old_excess": "", "new_excess": ""})

    # ---- CLOSED: declare in the companion columns; never overwrite -----------
    rows = list(csv.DictReader(open(TRADES)))
    for r in rows:
        f = by_iso.get(r["ticker"], {})
        te, tx = f.get(r["entry_date"]), f.get(r["exit_date"])
        bad_e, bad_x = off(r["entry_px"], te), off(r["exit_px"], tx)
        zero_hold = r["entry_date"] == r["exit_date"] and te is not None
        if not (bad_e or bad_x or zero_hold):
            continue
        ne = round(te, 4) if (bad_e or zero_hold) else round(float(r["entry_px"]), 4)
        nx = round(te if zero_hold else (tx if bad_x else float(r["exit_px"])), 4)
        nr = int(r["side"]) * (nx / ne - 1) - 2 * COST
        s = spy_ret(iso2t(r["entry_date"]), iso2t(r["exit_date"]))
        new = {"entry_px_tape": ne, "exit_px_tape": nx, "net_tape": round(nr, 5),
               "excess_tape": round(nr - s, 5) if s is not None else ""}
        if all(str(r.get(k, "")).strip() == str(v) for k, v in new.items()):
            continue                            # already declared, identical — no-op
        old_tape = r.get("net_tape", "")
        r.update(new)
        changes.append({"scope": "closed", "strategy": r["strategy"], "ticker": r["ticker"],
                        "entry_date": r["entry_date"], "exit_date": r["exit_date"],
                        "field": "tape DECLARED (scored row untouched)",
                        "old_entry_px": r["entry_px"], "new_entry_px": ne,
                        "old_exit_px": r["exit_px"], "new_exit_px": nx,
                        "old_net": old_tape, "new_net": r["net_tape"],
                        "old_excess": "", "new_excess": r["excess_tape"]})
    return rows, state, changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    rows, state, changes = reconcile()
    if not changes:
        print("auto_reconcile: every fill agrees with the settled feed, or already "
              "declares where it differs. Nothing written.")
        return
    opened = sum(1 for c in changes if c["scope"] == "open")
    print(f"auto_reconcile: {len(changes)} row(s) — {opened} open repaired in place, "
          f"{len(changes)-opened} closed declared in *_tape")
    for c in changes:
        print(f"  {c['scope']:<7}{c['strategy']:<14}{c['ticker']:<6}{c['entry_date']:<12}{c['field']}")
    if a.dry_run:
        print("  dry run — nothing written.")
        return
    with open(TRADES, "w") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLS})
    json.dump(state, open(STATE, "w"), indent=1)
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M PT")
    fields = list(csv.DictReader(open(LOG)).fieldnames)
    with open(LOG, "a") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        for c in changes:
            w.writerow({**c, "restated_at": stamp,
                        "reason": "auto_reconcile vs settled feed (DATA-002)"})
    print(f"  written, and logged to {os.path.relpath(LOG, HERE)}")


if __name__ == "__main__":
    main()
