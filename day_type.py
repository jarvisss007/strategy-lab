#!/usr/bin/env python3
"""Automated SNDK-style intraday day-type analyzer — the full RAW_TAPE sheet, filled
by code instead of by hand. For each session it detects intraday swings (zigzag),
then computes every column of the original sheet:

  swings (start/end time+price) · Move1..N signed · AbsMove · Total Path · Net Move ·
  Efficiency · Regime · Swing Count · Avg Swing Size · Largest Swing ·
  Move Order Dominance · Today Mode · When To Trade

Decision rules reverse-engineered from the hand sheet + its legend:
  Regime:      TREND eff>=0.40 · CHOP eff<0.20 · else MIXED
  Today Mode:  TREND DAY if eff>=0.45 · MEAN REVERSION DAY if eff<0.20 & path%>=tradeable
               · else OBSERVE / LIGHT
  When Trade:  TREND->6:30-7:15 · CHOP->AFTER 7:15 · MIXED->WAIT FOR EXTREMES
  Legend:      "Total Path >= 80 = tradeable" — re-expressed as % of price so it works
               at any price level (the hand sheet was tuned when SNDK was ~$500).

Also runs the one honest, tradeable test: does the first hour predict the rest of
the day? Usage: python day_type.py [TICKER] [--csv]
"""
import csv, json, sys, urllib.request, datetime as dt
from collections import defaultdict
import numpy as np

UA = {"User-Agent": "Mozilla/5.0"}
TREND_EFF, CHOP_EFF = 0.40, 0.20
TRADEABLE_PATH_PCT = 12.0   # total path >= 12% of price = "enough opportunity" (scale-free)
ZIGZAG_PCT = 0.015          # a reversal >=1.5% starts a new swing (tunable)


def intraday(sym, rng="1mo", itv="15m"):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng}&interval={itv}"
    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25))
    r = d["chart"]["result"][0]
    closes = r["indicators"]["quote"][0]["close"]
    bars = defaultdict(list)
    for t, c in zip(r["timestamp"], closes):
        if c is not None:
            d0 = dt.datetime.fromtimestamp(t)
            bars[d0.date()].append((d0, c))
    return bars


def zigzag(series, pct=ZIGZAG_PCT):
    """Return the list of (time, price) pivots — the intraday turning points. A new
    swing is confirmed when price reverses >= pct from the running leg extreme."""
    t = [x[0] for x in series]; p = [x[1] for x in series]
    piv = [(t[0], p[0])]
    direction = 0                 # 0 = seeking first leg, +1 = up leg, -1 = down leg
    ext_t, ext_p = t[0], p[0]
    for i in range(1, len(p)):
        pi = p[i]
        if direction == 0:
            chg = (pi - p[0]) / p[0] if p[0] else 0
            if chg >= pct:
                direction = 1; ext_t, ext_p = t[i], pi
            elif chg <= -pct:
                direction = -1; ext_t, ext_p = t[i], pi
        elif direction == 1:                       # up leg: track the high
            if pi > ext_p:
                ext_t, ext_p = t[i], pi
            elif (ext_p - pi) / ext_p >= pct:       # reversed down -> confirm the high
                piv.append((ext_t, ext_p)); direction = -1; ext_t, ext_p = t[i], pi
        else:                                       # down leg: track the low
            if pi < ext_p:
                ext_t, ext_p = t[i], pi
            elif (pi - ext_p) / ext_p >= pct:       # reversed up -> confirm the low
                piv.append((ext_t, ext_p)); direction = 1; ext_t, ext_p = t[i], pi
    if (ext_t, ext_p) != piv[-1]:
        piv.append((ext_t, ext_p))
    out = [piv[0]]
    for x in piv[1:]:
        if x[1] != out[-1][1]:
            out.append(x)
    return out


def analyze_day(series):
    if len(series) < 4:
        return None
    piv = zigzag(series)
    moves = [(piv[i + 1][1] - piv[i][1]) for i in range(len(piv) - 1)]
    if not moves:
        return None
    absm = [abs(m) for m in moves]
    o, c = series[0][1], series[-1][1]
    net = c - o
    path = sum(absm)
    eff = abs(net) / path if path else 0.0
    path_pct = path / o * 100 if o else 0.0
    regime = "TREND" if eff >= TREND_EFF else "CHOP" if eff < CHOP_EFF else "MIXED"
    if eff >= 0.45:
        mode = "TREND DAY"
    elif eff < CHOP_EFF and path_pct >= TRADEABLE_PATH_PCT:
        mode = "MEAN REVERSION DAY"
    else:
        mode = "OBSERVE / LIGHT"
    when = {"TREND": "6:30-7:15 AM", "CHOP": "AFTER 7:15 AM", "MIXED": "WAIT FOR EXTREMES"}[regime]
    dom = int(np.argmax(absm)) + 1
    return {
        "open": round(o, 2), "close": round(c, 2), "net": round(net, 2),
        "path": round(path, 2), "path_pct": round(path_pct, 1), "eff": round(eff, 3),
        "regime": regime, "swing_count": len(moves), "avg_swing": round(np.mean(absm), 2),
        "largest_swing": round(max(absm), 2), "dominance": f"Move{dom}",
        "today_mode": mode, "when_to_trade": when,
        "moves": [round(m, 2) for m in moves],
        "pivots": [(t.strftime("%H:%M"), round(pp, 2)) for t, pp in piv],
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sym = args[0] if args else "SNDK"
    want_csv = "--csv" in sys.argv
    bars = intraday(sym, "1mo", "15m")
    days = sorted(bars)
    rows = []
    print(f"=== {sym} — automated RAW_TAPE (last {len(days)} sessions, 15m bars) ===\n")
    print(f"{'date':11s} {'open':>8s} {'close':>8s} {'net':>7s} {'path':>7s} {'path%':>5s} "
          f"{'eff':>5s} {'reg':6s} {'sw':>2s} {'domi':5s} {'today mode':18s} when")
    for day in days:
        a = analyze_day(sorted(bars[day]))
        if not a:
            continue
        a["date"] = str(day)
        rows.append(a)
        print(f"{str(day):11s} {a['open']:8.2f} {a['close']:8.2f} {a['net']:7.2f} "
              f"{a['path']:7.2f} {a['path_pct']:5.1f} {a['eff']:5.2f} {a['regime']:6s} "
              f"{a['swing_count']:2d} {a['dominance']:5s} {a['today_mode']:18s} {a['when_to_trade']}")

    reg = defaultdict(int); mode = defaultdict(int); dom = defaultdict(int)
    for r in rows:
        reg[r["regime"]] += 1; mode[r["today_mode"]] += 1; dom[r["dominance"]] += 1
    print(f"\nRegime mix: {dict(reg)}")
    print(f"Today-mode mix: {dict(mode)}")
    print(f"Move-order dominance: {dict(dom)}  (Move1 = big move came early)")
    print(f"Avg efficiency {np.mean([r['eff'] for r in rows]):.2f} · avg path% "
          f"{np.mean([r['path_pct'] for r in rows]):.1f}% · avg swing count "
          f"{np.mean([r['swing_count'] for r in rows]):.1f} · avg largest swing "
          f"${np.mean([r['largest_swing'] for r in rows]):.2f}")

    # honest test: first-hour (first 4x15m bars) direction vs rest of day
    cont, hi_trend, base_trend, n = 0, [], [], 0
    for day in days:
        s = sorted(bars[day])
        if len(s) < 8:
            continue
        n += 1
        o, e, c = s[0][1], s[4][1], s[-1][1]
        early_path = sum(abs(s[i][1] - s[i - 1][1]) for i in range(1, 5))
        early_eff = abs(e - o) / early_path if early_path else 0
        full = analyze_day(s)
        cont += (np.sign(e - o) == np.sign(c - e))
        base_trend.append(full["regime"] == "TREND")
        if early_eff >= TREND_EFF:
            hi_trend.append(full["regime"] == "TREND")
    if n:
        print(f"\n--- Honest test ({n} sessions) ---")
        print(f"First-hour direction continues into rest of day: {cont/n*100:.0f}%  (50% = no edge)")
        pt = np.mean(hi_trend) * 100 if hi_trend else float('nan')
        print(f"P(trend day | clean first hour): {pt:.0f}%  vs base rate {np.mean(base_trend)*100:.0f}%")
        print(f"\n{n} sessions is far too few to trust. This DESCRIBES the day well; it does not "
              f"forecast it. A daily recorder is the only way to a real sample.")

    if want_csv:
        import os
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports", f"{sym}_daytape.csv")
        cols = ["date", "open", "close", "net", "path", "path_pct", "eff", "regime",
                "swing_count", "avg_swing", "largest_swing", "dominance", "today_mode", "when_to_trade"]
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow(r)
        print(f"\nCSV -> reports/{sym}_daytape.csv")


if __name__ == "__main__":
    main()
