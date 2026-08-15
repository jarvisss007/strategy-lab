#!/usr/bin/env python
"""price_integrity.py — does every recorded entry price match the tape?

Anupam, 2026-08-15, reading his own portfolio: "QBTS was $16 so many days back,
how can you buy it yesterday at that price?"

He was right. QBTS is recorded at 16.21 on 2026-08-04, 08-11 and 08-13. The real
closes were 21.83, 20.23 and 20.90 — a 26% error showing as a fake +28.7% gain on
the front page.

WHY IT HAPPENED, precisely, because the cause is not what it looks like.
arena.py is correct: it stamps entry_date from the BAR date and entry_px from
that same bar, so date and price cannot drift apart within a run (entry_t agrees
with entry_date on all 135 open rows). radar.json holds the right prices TODAY.
What happened is that the feed served a STALE BAR under a fresh date, the Arena
faithfully recorded what it was told, and the bad number was fossilised in a
permanent record that nothing ever re-checks.

The signature is unmistakable once you look for it: every wrong price is a real
close from an EARLIER bar. GFS 53.18, HUM 381.15, TSLA 309.22 and MOH 199.48 are
all recorded on 2026-07-29 and are all exactly their 2026-07-27 close; QBTS 16.21,
recorded on 08-04, 08-11 and 08-13, is its 2026-07-24 close. Four unrelated
tickers landing on the same prior bar is not adjusted-vs-raw noise — it is one
stale refresh. Which also means arena.py enters on the least-settled bar it has:
it opens at c[len(c)-1], the freshest and therefore most provisional price in the
feed.

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
COST = 0.001        # arena.py:43 — a zero-hold trade can only ever cost 2*COST.


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
    """Both legs of every trade, plus the trades that never had two legs.

    Extended 2026-08-14: the first version checked entries only, and the exit leg
    was carrying the single largest error in the book — STORM_DIP QBTS booked
    -0.01% where the tape says +23.3%, because its EXIT was stamped 16.21. Half a
    trade validated is not a validated trade.
    """
    px = truth()
    rows = [dict(r, _src="closed") for r in csv.DictReader(open(TRADES))]
    rows += [dict(o, _src="open") for o in json.load(open(STATE))["open"]]
    bad, checked, unverifiable, zero_hold, disclosed = [], 0, 0, [], 0
    for r in rows:
        legs = [("entry", r["entry_date"], r["entry_px"])]
        if r["_src"] == "closed":
            legs.append(("exit", r["exit_date"], r["exit_px"]))
        for leg, date, recorded in legs:
            a = px.get(r["ticker"], {}).get(date)
            if a is None:
                unverifiable += 1      # off-watchlist or bar not in the feed
                continue
            checked += 1
            p = float(recorded)
            if abs(p - a) / a > TOL:
                # BENCH-002 (ruled 2026-08-12) forbids overwriting the number a
                # CLOSED row was scored with, so on those rows "matches the tape"
                # is the wrong thing to demand — it is unreachable by design. What
                # is reachable, and what actually matters, is that the divergence
                # be DECLARED: the row must carry the tape's price in its companion
                # column. A closed row that disagrees with the tape and says so is
                # an honest record. One that disagrees silently is the defect.
                # Open rows have no scored outcome and must still match outright —
                # marking a live position off a price that never traded is exactly
                # what DATA-001 was raised for.
                if r["_src"] == "closed" and str(r.get(f"{leg}_px_tape", "")).strip():
                    disclosed += 1
                    continue
                bad.append({"ticker": r["ticker"], "leg": leg, "date": date,
                            "entry_date": r["entry_date"],
                            "recorded": round(p, 4), "feed": round(a, 4),
                            "err_pct": round(100 * (p - a) / a, 1),
                            "strategy": r.get("strategy"), "status": r["_src"]})
        # A position opened and closed on the same close cannot have made or lost
        # anything but its costs. Non-zero P&L on a zero-hold row means one of the
        # two prices did not come from the bar it claims.
        if r["_src"] == "closed" and r["entry_date"] == r["exit_date"]:
            net = float(r["net"]) if r["net"] not in ("", None) else 0.0
            # Same BENCH-002 carve-out as above: the scored number stays, so an
            # impossible zero-hold P&L is only a defect while it goes UNDECLARED.
            # Once net_tape carries what the round trip could actually have paid,
            # the row is an honest record of a bad fill rather than a hidden one.
            if str(r.get("net_tape", "")).strip():
                disclosed += 1
            elif abs(net) > 2 * COST + 1e-9:
                zero_hold.append({"ticker": r["ticker"], "strategy": r.get("strategy"),
                                  "date": r["entry_date"], "net_pct": round(100 * net, 2)})
    return {"checked": checked, "unverifiable": unverifiable,
            "mismatched": len(bad), "tolerance_pct": TOL * 100,
            "disclosed_divergences": disclosed,
            "zero_hold_mispriced": len(zero_hold), "zero_hold_rows": zero_hold,
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
    print(f"\nFill integrity — {rep['checked']} prices (both legs) checked against "
          f"radar.json, {rep['unverifiable']} unverifiable (off-feed)")
    if rep["disclosed_divergences"]:
        print(f"  {rep['disclosed_divergences']} closed-row divergence(s) declared in "
              "*_px_tape columns (BENCH-002: scored number kept, tape carried beside it)")
    if not rep["rows"] and not rep["zero_hold_mispriced"]:
        print("  every price either matches the tape within "
              f"{rep['tolerance_pct']:.0f}% or declares where it differs, and no "
              "zero-hold row books more than costs.")
        return
    if rep["rows"]:
        by = collections.Counter(r["ticker"] for r in rep["rows"])
        print(f"  {rep['mismatched']} disagree by more than {rep['tolerance_pct']:.0f}% "
              f"({100*rep['mismatched']/rep['checked']:.1f}% of the book)\n")
        print(f"  {'ticker':<8}{'leg':<7}{'bar date':<13}{'recorded':>10}{'feed':>10}"
              f"{'err':>8}  {'status'}")
        for r in rep["rows"][:20]:
            print(f"  {r['ticker']:<8}{r['leg']:<7}{r['date']:<13}{r['recorded']:>10.2f}"
                  f"{r['feed']:>10.2f}{r['err_pct']:>7.0f}%  {r['status']}")
        print(f"\n  worst offender: {by.most_common(1)[0][0]} ({by.most_common(1)[0][1]} rows)")
    for z in rep["zero_hold_rows"]:
        print(f"  zero-hold: {z['strategy']} {z['ticker']} {z['date']} books "
              f"{z['net_pct']:+.2f}% on a same-bar round trip")
    print("\n  NOT auto-corrected here. This file only ever reports. Restating a written")
    print("  row is a BENCH-002-shaped decision that belongs to Anupam, and when he")
    print("  makes it, restate_prices.py --apply does it and logs every before/after.")


if __name__ == "__main__":
    main()
