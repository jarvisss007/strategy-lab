#!/usr/bin/env python
"""price_integrity.py — does every recorded entry price match the tape?

Anupam, 2026-08-15, reading his own portfolio: "QBTS was $16 so many days back,
how can you buy it yesterday at that price?"

He was right. QBTS is recorded at 16.21 on 2026-08-04, 08-11 and 08-13. The real
closes were 21.83, 20.23 and 20.90 — a 26% error showing as a fake +28.7% gain on
the front page.

WHY IT HAPPENED, precisely, because the cause is not what it looks like.
arena.py is correct: it stamps entry_date from the BAR date and entry_px from
that same bar, so date and price cannot drift apart within a run. radar.json
holds the right prices TODAY. What happened is that the feed was wrong on the day
the Arena ran, the Arena faithfully recorded what it was told, and the bad number
was fossilised in a permanent record that nothing ever re-checks.

That is the gap this file closes. The desk validated benchmarks, clustering,
survivorship and effective bets — every layer of ANALYSIS — and never once
validated the raw INPUTS those layers are computed from. A wrong entry price
silently corrupts pnl_pct, excess_pct, every desk standing, the blended hit rate
and the day-clustered t-statistic, and no test anywhere would notice.

WHAT IT CHECKS
Every entry in arena_trades.csv and arena_state.json against radar.json's series
for that ticker on that bar date. A disagreement beyond TOL is reported, never
silently corrected: the recorded row is the record, and rewriting a written entry
price is a BENCH-002-shaped decision that belongs to Anupam, not to a script.

Run:  /opt/anaconda3/bin/python price_integrity.py
      /opt/anaconda3/bin/python price_integrity.py --json   # for the page/resolver
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import json
import os

HOME = os.path.expanduser("~")
HERE = os.path.dirname(os.path.abspath(__file__))
RADAR = os.path.join(HOME, "stock-radar", "data", "radar.json")
TRADES = os.path.join(HERE, "reports", "arena_trades.csv")
STATE = os.path.join(HERE, "reports", "arena_state.json")
OUT = os.path.join(HERE, "reports", "price_integrity.json")
DAY0 = dt.date(1970, 1, 1)
TOL = 0.02          # 2%. Below this is adjusted-vs-raw noise, not a wrong fill.


def _iso(t):
    return (DAY0 + dt.timedelta(days=int(t))).isoformat()


def truth():
    """{ticker: {iso_date: close}} from the feed the Arena itself trades off."""
    d = json.load(open(RADAR))
    eq = d if isinstance(d, list) else (d.get("equities") or [])
    return {e["ticker"]: {_iso(t): c
                          for t, c in zip(e.get("series_t", []), e.get("series_c", []))
                          if c}
            for e in eq if e.get("ticker")}


def audit():
    px = truth()
    rows = [dict(r, _src="closed") for r in csv.DictReader(open(TRADES))]
    rows += [dict(o, _src="open") for o in json.load(open(STATE))["open"]]
    bad, checked, unverifiable = [], 0, 0
    for r in rows:
        a = px.get(r["ticker"], {}).get(r["entry_date"])
        if a is None:
            unverifiable += 1          # off-watchlist or bar not in the feed
            continue
        checked += 1
        ep = float(r["entry_px"])
        if abs(ep - a) / a > TOL:
            bad.append({"ticker": r["ticker"], "entry_date": r["entry_date"],
                        "recorded": round(ep, 4), "feed": round(a, 4),
                        "err_pct": round(100 * (ep - a) / a, 1),
                        "strategy": r.get("strategy"), "status": r["_src"]})
    return {"checked": checked, "unverifiable": unverifiable,
            "mismatched": len(bad), "tolerance_pct": TOL * 100,
            "rows": sorted(bad, key=lambda x: -abs(x["err_pct"])),
            "generated": dt.datetime.now().strftime("%Y-%m-%d %H:%M PT")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    rep = audit()
    json.dump(rep, open(OUT, "w"), indent=1)
    if args.json:
        print(json.dumps(rep, indent=1))
        return
    print(f"\nEntry-price integrity — {rep['checked']} entries checked against radar.json"
          f", {rep['unverifiable']} unverifiable (off-feed)")
    if not rep["rows"]:
        print("  every recorded entry price matches the tape within "
              f"{rep['tolerance_pct']:.0f}%.")
        return
    by = collections.Counter(r["ticker"] for r in rep["rows"])
    print(f"  {rep['mismatched']} disagree by more than {rep['tolerance_pct']:.0f}% "
          f"({100*rep['mismatched']/rep['checked']:.1f}% of the book)\n")
    print(f"  {'ticker':<8}{'entry date':<13}{'recorded':>10}{'feed':>10}{'err':>8}  {'status'}")
    for r in rep["rows"][:20]:
        print(f"  {r['ticker']:<8}{r['entry_date']:<13}{r['recorded']:>10.2f}"
              f"{r['feed']:>10.2f}{r['err_pct']:>7.0f}%  {r['status']}")
    print(f"\n  worst offender: {by.most_common(1)[0][0]} ({by.most_common(1)[0][1]} rows)")
    print("  NOT auto-corrected. The recorded row is the record; rewriting a written")
    print("  entry price is a BENCH-002-shaped decision and belongs to Anupam.")


if __name__ == "__main__":
    main()
