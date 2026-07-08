#!/usr/bin/env python3
"""Intraday discovery engine — tests intraday day-trading hypotheses HONESTLY, by
entering at the actual signal price (not the open) and exiting at the close, net of
costs. This is where the opening-range-breakout "90% hold rate" gets its reckoning:
you only capture the move FROM the break TO the close, not the whole day.

Hypotheses: opening-range breakout, opening-range fade, first-hour momentum, first-
hour reversal, open-fade. Per trade it reports avg return, hit rate, and a t-stat;
per strategy a basket Sharpe. Logs to intraday_discoveries.csv.
Honest caveat: ~20 sessions/name — treat t-stats as suggestive, not proof (name-days
on the same date are correlated). The recorder is what makes this conclusive.
Run: /opt/anaconda3/bin/python intraday_discover.py"""
import csv, json, os
from collections import defaultdict
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
COST = 0.0005            # per trade; a round trip (enter+exit) = 2x
ROUND_TRIP = 2 * COST


def load():
    cache = json.load(open(os.path.join(BASE, "data", "intraday_15m.json")))
    try:
        dt = json.load(open(os.path.join(BASE, "reports", "universe_daytype.json")))
        active = [r["ticker"] for r in dt["rows"] if r["character"] != "QUIET"]
    except Exception:
        active = list(cache["data"].keys())
    return cache["data"], [t for t in active if t in cache["data"]]


# each strategy: given a day's bars, return the trade return (net) or None (no trade)
def or_breakout(bars, fade=False):
    if len(bars) < 8:
        return None
    or_hi = max(b[2] for b in bars[:2]); or_lo = min(b[3] for b in bars[:2])
    close = bars[-1][4]
    for b in bars[2:]:
        if b[2] > or_hi:                      # upside break: enter long at the level
            r = close / or_hi - 1
            return (-r if fade else r) - ROUND_TRIP
        if b[3] < or_lo:                      # downside break: enter short at the level
            r = or_lo / close - 1
            return (-r if fade else r) - ROUND_TRIP
    return None                                # no break -> no trade


def first_hour(bars, reverse=False):
    if len(bars) < 8:
        return None
    entry = bars[4][4]; close = bars[-1][4]; o = bars[0][1]
    d = np.sign(entry - o)
    if d == 0:
        return None
    r = d * (close / entry - 1)
    return (-r if reverse else r) - ROUND_TRIP


def open_fade(bars):
    """Short the opening pop: enter short at first-bar close, cover 30 min later."""
    if len(bars) < 4:
        return None
    entry = bars[0][4]; exitp = bars[2][4]
    return (entry / exitp - 1) - ROUND_TRIP    # short: profit if price fell


STRATS = {
    "opening-range breakout": lambda b: or_breakout(b, fade=False),
    "opening-range fade": lambda b: or_breakout(b, fade=True),
    "first-hour momentum": lambda b: first_hour(b, reverse=False),
    "first-hour reversal": lambda b: first_hour(b, reverse=True),
    "open-fade (short the pop)": open_fade,
}


def main():
    data, names = load()
    rows = []
    print(f"=== Intraday discovery — {len(names)} names, ~20 sessions each ===")
    print("(enter at signal price, exit at close, net of ~10bps round trip)\n")
    print(f"{'strategy':28s} {'trades':>6s} {'avg%':>7s} {'hit%':>6s} {'t-stat':>7s} {'bktSharpe':>9s}  read")
    for label, fn in STRATS.items():
        per_trade, by_day = [], defaultdict(list)
        for t in names:
            for day, bars in data[t].items():
                r = fn(bars)
                if r is not None:
                    per_trade.append(r); by_day[day].append(r)
        if len(per_trade) < 30:
            continue
        a = np.array(per_trade)
        avg = a.mean() * 100
        hit = (a > 0).mean() * 100
        tstat = a.mean() / a.std(ddof=1) * np.sqrt(len(a)) if a.std() else 0
        daily = np.array([np.mean(v) for v in by_day.values()])
        bkt = daily.mean() / daily.std(ddof=1) * np.sqrt(252) if daily.std() else 0
        read = ("positive, but needs recorder to confirm" if avg > 0 and tstat > 2
                else "no edge" if abs(tstat) < 2 else "negative")
        rows.append({"strategy": label, "trades": len(a), "avg_pct": round(avg, 3),
                     "hit_pct": round(hit, 1), "tstat": round(float(tstat), 2),
                     "basket_sharpe": round(float(bkt), 2), "read": read})
        print(f"{label:28s} {len(a):6d} {avg:7.3f} {hit:6.1f} {tstat:7.2f} {bkt:9.2f}  {read}")

    with open(os.path.join(BASE, "intraday_discoveries.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["strategy", "trades", "avg_pct", "hit_pct", "tstat", "basket_sharpe", "read"])
        w.writeheader(); w.writerows(rows)
    json.dump({"strategies": rows, "note": "~20 sessions/name; enter-at-signal exit-at-close net of costs"},
              open(os.path.join(BASE, "reports", "intraday_discover.json"), "w"), indent=1)
    print("\nThe opening-range 'break closes in direction ~90%' collapses here: you enter at the")
    print("break, so you only get break->close, minus costs. Whatever's left is the real story.")
    print("~20 sessions can't be conclusive — the recorder grows the sample. -> intraday_discoveries.csv")


if __name__ == "__main__":
    main()
