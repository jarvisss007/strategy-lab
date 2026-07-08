#!/usr/bin/env python3
"""Intraday pattern study on the cached 15m data, focused on the high-opportunity
names. Answers three descriptive questions:
  1. Time-of-day profile — WHEN during the day do these names actually move?
  2. Opening range — does the first 30 min's high/low get broken, and does the
     breakout direction stick to the close?
  3. First hour -> rest of day — does the open forecast the day's direction?
Writes reports/intraday_study.json. Honest caveat: ~20 sessions, descriptive only.
Run: /opt/anaconda3/bin/python intraday_study.py"""
import json, os
from collections import defaultdict
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))


def load():
    cache = json.load(open(os.path.join(BASE, "data", "intraday_15m.json")))
    try:
        dt = json.load(open(os.path.join(BASE, "reports", "universe_daytype.json")))
        active = [r["ticker"] for r in dt["rows"] if r["character"] != "QUIET"]
    except Exception:
        active = list(cache["data"].keys())
    return cache["data"], active


def main():
    data, active = load()
    names = [t for t in active if t in data]

    # 1. time-of-day profile: avg % move in each intraday slot, across names & days
    slot = defaultdict(list)
    for t in names:
        for day, bars in data[t].items():
            for i, b in enumerate(bars):
                tm, o, h, l, c = b
                r = (c / o - 1) if i == 0 else (c / bars[i - 1][4] - 1)
                slot[tm].append(r * 100)
    profile = [{"time": tm, "avg_move_pct": round(float(np.mean(v)), 3),
                "abs_move_pct": round(float(np.mean(np.abs(v))), 3), "n": len(v)}
               for tm, v in sorted(slot.items())]

    # 2. opening range (first 2 bars = 30 min): break + continuation to close
    orb = {"upside_break_days": 0, "downside_break_days": 0, "no_break": 0,
           "up_break_closed_up": 0, "down_break_closed_down": 0, "total": 0}
    for t in names:
        for day, bars in data[t].items():
            if len(bars) < 8:
                continue
            orb["total"] += 1
            or_hi = max(b[2] for b in bars[:2]); or_lo = min(b[3] for b in bars[:2])
            rest = bars[2:]
            broke_up = any(b[2] > or_hi for b in rest)
            broke_dn = any(b[3] < or_lo for b in rest)
            close = bars[-1][4]; open0 = bars[0][1]
            if broke_up and not broke_dn:
                orb["upside_break_days"] += 1
                orb["up_break_closed_up"] += (close > open0)
            elif broke_dn and not broke_up:
                orb["downside_break_days"] += 1
                orb["down_break_closed_down"] += (close < open0)
            elif not broke_up and not broke_dn:
                orb["no_break"] += 1

    # 3. first hour (first 4 bars) direction -> rest of day
    cont, hi_eff_trend, base_trend, n = 0, [], [], 0
    for t in names:
        for day, bars in data[t].items():
            if len(bars) < 8:
                continue
            n += 1
            o, e, c = bars[0][1], bars[4][4], bars[-1][4]
            path = sum(abs(bars[i][4] - bars[i - 1][4]) for i in range(1, len(bars)))
            net = abs(c - o)
            full_eff = net / path if path else 0
            early_path = sum(abs(bars[i][4] - bars[i - 1][4]) for i in range(1, 5))
            early_eff = abs(e - o) / early_path if early_path else 0
            cont += (np.sign(e - o) == np.sign(c - e))
            base_trend.append(full_eff >= 0.4)
            if early_eff >= 0.4:
                hi_eff_trend.append(full_eff >= 0.4)

    orb["up_break_hold_rate"] = round(orb["up_break_closed_up"] / max(1, orb["upside_break_days"]) * 100, 1)
    orb["down_break_hold_rate"] = round(orb["down_break_closed_down"] / max(1, orb["downside_break_days"]) * 100, 1)
    out = {"n_names": len(names), "names": names, "sessions_per_name": "~20 (15m/1mo)",
           "time_of_day": profile, "opening_range": orb,
           "first_hour": {"n": n, "continuation_pct": round(cont / max(1, n) * 100, 1),
                          "trend_given_clean_open_pct": round(float(np.mean(hi_eff_trend)) * 100, 1) if hi_eff_trend else None,
                          "base_trend_pct": round(float(np.mean(base_trend)) * 100, 1)}}
    json.dump(out, open(os.path.join(BASE, "reports", "intraday_study.json"), "w"), indent=1)

    print(f"=== Intraday study — {len(names)} high-opportunity names, ~20 sessions each ===\n")
    print("1. TIME-OF-DAY PROFILE (avg signed move per 15-min slot; * = biggest abs slots)")
    mx = max(p["abs_move_pct"] for p in profile)
    for p in profile:
        bar = "#" * int(p["abs_move_pct"] / mx * 30)
        star = " *" if p["abs_move_pct"] > 0.7 * mx else ""
        print(f"   {p['time']}  {p['avg_move_pct']:+6.3f}%  |{bar:<30}| {p['abs_move_pct']:.2f}%abs{star}")
    print(f"\n2. OPENING RANGE (first 30 min), {orb['total']} name-days")
    print(f"   upside breaks: {orb['upside_break_days']}  (closed up {orb['up_break_hold_rate']}%)")
    print(f"   downside breaks: {orb['downside_break_days']}  (closed down {orb['down_break_hold_rate']}%)")
    print(f"   no break (range-bound): {orb['no_break']}")
    fh = out["first_hour"]
    print(f"\n3. FIRST HOUR -> REST ({fh['n']} name-days)")
    print(f"   direction continues: {fh['continuation_pct']}%  (50% = no edge)")
    print(f"   P(trend day | clean open): {fh['trend_given_clean_open_pct']}%  vs base {fh['base_trend_pct']}%")
    print("\n~20 sessions/name — describes, does not prove. The recorder grows this.")


if __name__ == "__main__":
    main()
