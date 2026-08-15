#!/usr/bin/env python
"""bench002_restore.py — put the scored numbers back, and carry the tape alongside.

BENCH-002, ruled by Anupam 2026-08-12:

    NO. A closed row keeps the number it was scored with. A corrected value may be
    added as a NEW column; a recorded outcome is never overwritten.

On 2026-08-14 I restated 14 rows to the tape on Anupam's "correct everything", and
9 of them were CLOSED rows whose `net` and `excess` I overwrote. That is the thing
this ruling forbids, and neither he nor I checked it against the register at the
time. The council's edition the same day says the same of the 07-29 trio.

This restores the ruling's own remedy rather than arguing with it. Every closed row
gets back the exact number it was scored with, and the tape's version is carried in
NEW columns beside it:

    entry_px / exit_px / net / excess              what the row was scored on
    entry_px_tape / exit_px_tape / net_tape /      what the tape says it should
    excess_tape                                     have been

Nothing is lost either way: the scored record is intact for anyone auditing what
the desk actually claimed, and the corrected figure is one column away for anyone
asking what was true. A reader can compute the desk's standings on either basis and
say which they used.

WHAT IS NOT REVERTED, and why. The 3 OPEN rows keep their corrected entry price.
An open position has no recorded outcome — nothing has been scored — so BENCH-002
does not reach it, and marking a live position off a price that never traded is the
error DATA-001 was raised for. One of those three (DOUBLE_DIP QBTS) has since closed
at 21.17 against the corrected 20.23 entry; it was scored on the corrected number,
never on the wrong one, so it is left exactly as it is.

Reversible in one line the other way: if Anupam rules that a false INPUT is not a
"recorded outcome" and DATA-001 is an exception to BENCH-002, restate_prices.py
--apply reapplies the tape values and this file records why.

Run:  /opt/anaconda3/bin/python bench002_restore.py --dry-run
      /opt/anaconda3/bin/python bench002_restore.py --apply
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TRADES = os.path.join(HERE, "reports", "arena_trades.csv")
LOG = os.path.join(HERE, "reports", "price_restatement_log.csv")
COLS = ["strategy", "ticker", "side", "entry_date", "entry_px",
        "exit_date", "exit_px", "net", "excess", "regime", "tags",
        # BENCH-002 companion columns: the tape's view, never the scored view
        "entry_px_tape", "exit_px_tape", "net_tape", "excess_tape"]
KEY = ("strategy", "ticker", "entry_date", "exit_date")


def restore():
    amendments = [r for r in csv.DictReader(open(LOG)) if r["scope"] == "closed"]
    rows = list(csv.DictReader(open(TRADES)))
    index = {tuple(r[k] for k in KEY): r for r in rows}
    done, missing = [], []
    for a in amendments:
        r = index.get((a["strategy"], a["ticker"], a["entry_date"], a["exit_date"]))
        if r is None:
            missing.append(a)
            continue
        # the tape's view moves into the companion columns …
        r["entry_px_tape"] = a["new_entry_px"]
        r["exit_px_tape"] = a["new_exit_px"]
        r["net_tape"] = a["new_net"]
        r["excess_tape"] = a["new_excess"]
        # … and the scored row goes back to the number it was scored with
        r["entry_px"], r["exit_px"] = a["old_entry_px"], a["old_exit_px"]
        r["net"], r["excess"] = a["old_net"], a["old_excess"]
        done.append((r, a))
    return rows, done, missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    rows, done, missing = restore()
    print(f"\nBENCH-002 restore — {len(done)} closed row(s) return to their scored number")
    print(f"  {'strategy':<14}{'tick':<6}{'entry':<12}{'scored':>10}{'tape':>10}")
    for r, am in done:
        print(f"  {r['strategy']:<14}{r['ticker']:<6}{r['entry_date']:<12}"
              f"{100*float(r['net']):>9.2f}%{100*float(r['net_tape']):>9.2f}%")
    if missing:
        print(f"\n  {len(missing)} amendment(s) had no matching row — NOT applied:")
        for m in missing:
            print(f"    {m['strategy']} {m['ticker']} {m['entry_date']}")
    if not a.apply:
        print("\n  dry run — nothing written. Re-run with --apply.")
        return
    with open(TRADES, "w") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLS})
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M PT")
    with open(LOG, "a") as f:
        w = csv.DictWriter(f, fieldnames=list(csv.DictReader(open(LOG)).fieldnames),
                           extrasaction="ignore")
        for r, am in done:
            w.writerow({"restated_at": stamp, "scope": "closed", "strategy": r["strategy"],
                        "ticker": r["ticker"], "entry_date": r["entry_date"],
                        "exit_date": r["exit_date"], "field": "REVERTED to scored value",
                        "old_entry_px": am["new_entry_px"], "new_entry_px": am["old_entry_px"],
                        "old_exit_px": am["new_exit_px"], "new_exit_px": am["old_exit_px"],
                        "old_net": am["new_net"], "new_net": am["old_net"],
                        "old_excess": am["new_excess"], "new_excess": am["old_excess"],
                        "reason": "BENCH-002: a closed row keeps the number it was scored "
                                  "with; tape value moved to *_tape columns"})
    print(f"\n  written. {len(done)} rows restored, tape values carried in "
          f"entry_px_tape/exit_px_tape/net_tape/excess_tape.")
    print("  The reversion itself is logged in price_restatement_log.csv.")


if __name__ == "__main__":
    main()
