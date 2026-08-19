#!/usr/bin/env python
"""exit_overlays.py — REGIME_EXIT and STOP_ONLY, run as registered paper arms.

Registered in REGISTRY.md 2026-08-18 before this file first ran. Anupam asked
for agents that "exit beforehand" in a downturn; beforehand does not exist, so
this tests the honest version — exit one day AFTER the regime measurably flips,
by rule — alongside the coach's long-requested stop-only rule (EXIT-001).

Mechanics mirror rotation_arm.py exactly: same entries as the Arena, each arm's
NAV vs the base book from 100, weights per position (exited = weight to cash),
one row per session, 2×COST charged on every overlay-forced exit. The arms never
touch the Arena itself.

  REGIME_EXIT  on a regime flip, exit positions whose family's recorded avg bps
               in the NEW regime is negative (frozen replay table, arena.json).
  STOP_ONLY    exit any position at mtm <= -5%. Nothing else.

Run:  /opt/anaconda3/bin/python exit_overlays.py     (daily, after rotation_arm)
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
ARENA = os.path.join(HERE, "reports", "arena.json")
BOOK = os.path.join(HERE, "reports", "exit_overlays.json")
LOG = os.path.join(HERE, "reports", "exit_overlays_log.csv")
COST = 0.001
STOP = -0.05


def key(p):
    return f"{p['strategy']}|{p['ticker']}|{p['entry_date']}"


def last_two(tk, d):
    e = next((x for x in d if x.get("ticker") == tk), None)
    if not e:
        return None
    c = [x for x in e.get("series_c", []) if x]
    return (c[-2], c[-1]) if len(c) >= 2 else None


def main():
    radar = json.load(open(RADAR))
    arena = json.load(open(ARENA))
    opens = json.load(open(STATE))["open"]
    today = dt.date.today().isoformat()
    regime = arena.get("current_regime", "unknown")

    # family -> avg bps in each regime, from the FROZEN replay table
    reg_bps = {}
    for fam, b in (arena.get("backtest") or {}).items():
        for rg, st in (b.get("by_regime") or {}).items():
            if st and st.get("avg_bps") is not None:
                reg_bps[(fam, rg)] = st["avg_bps"]

    book = {"start": today, "last_run": None, "last_regime": regime,
            "arms": {"REGIME_EXIT": {"nav": 100.0, "weights": {}},
                     "STOP_ONLY": {"nav": 100.0, "weights": {}}},
            "nav_base": 100.0}
    if os.path.exists(BOOK):
        book = json.load(open(BOOK))
    if book.get("last_run") == today:
        print("exit_overlays: already ran today")
        return

    cur = {key(p): p for p in opens}
    eq = radar.get("equities", [])
    rets = {}
    for k, p in cur.items():
        pr = last_two(p["ticker"], eq)
        if pr and pr[0]:
            rets[k] = pr[1] / pr[0] - 1

    # ---- NAV update on the day's returns (held sets from yesterday) ----------
    if book.get("last_run") and rets:
        held_all = [k for k in rets if k in cur]
        if held_all:
            base_r = sum(rets[k] for k in held_all) / len(held_all)
            book["nav_base"] = round(book["nav_base"] * (1 + base_r), 4)
        for arm, st in book["arms"].items():
            w = st["weights"]
            held = [k for k in held_all if w.get(k, 1.0) > 0]
            n_slots = len(held_all)
            if n_slots:
                arm_r = sum(rets[k] for k in held) / n_slots   # exited slots sit in cash
                st["nav"] = round(st["nav"] * (1 + arm_r), 4)

    # ---- sync position sets: departures leave, new entries join at weight 1 --
    for arm, st in book["arms"].items():
        st["weights"] = {k: v for k, v in st["weights"].items() if k in cur}
        for k in cur:
            st["weights"].setdefault(k, 1.0)

    flipped = regime != book.get("last_regime")
    marks = {k: cur[k].get("mtm", 0.0) for k in cur}
    actions = {"REGIME_EXIT": [], "STOP_ONLY": []}

    # REGIME_EXIT: on a flip, exit families negative in the NEW regime
    w = book["arms"]["REGIME_EXIT"]["weights"]
    if flipped:
        for k in list(w):
            if w[k] <= 0:
                continue
            fam = cur[k]["strategy"]
            if reg_bps.get((fam, regime), 0) < 0:
                w[k] = 0.0
                book["arms"]["REGIME_EXIT"]["nav"] = round(
                    book["arms"]["REGIME_EXIT"]["nav"] * (1 - 2 * COST / max(len(w), 1)), 4)
                actions["REGIME_EXIT"].append(cur[k]["ticker"])

    # STOP_ONLY: exit anything at or through -5%
    w = book["arms"]["STOP_ONLY"]["weights"]
    for k in list(w):
        if w[k] > 0 and marks.get(k, 0.0) <= STOP:
            w[k] = 0.0
            book["arms"]["STOP_ONLY"]["nav"] = round(
                book["arms"]["STOP_ONLY"]["nav"] * (1 - 2 * COST / max(len(w), 1)), 4)
            actions["STOP_ONLY"].append(cur[k]["ticker"])

    book["last_run"], book["last_regime"] = today, regime
    json.dump(book, open(BOOK, "w"), indent=1)

    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="") as f:
        wcsv = csv.writer(f)
        if new:
            wcsv.writerow(["date", "regime", "flipped", "nav_base", "nav_regime_exit",
                           "nav_stop_only", "regime_exits", "stop_exits"])
        wcsv.writerow([today, regime, int(flipped), book["nav_base"],
                       book["arms"]["REGIME_EXIT"]["nav"],
                       book["arms"]["STOP_ONLY"]["nav"],
                       ";".join(actions["REGIME_EXIT"]),
                       ";".join(actions["STOP_ONLY"])])
    print(f"exit_overlays {today} [{regime}{' FLIP' if flipped else ''}]: "
          f"base {book['nav_base']:.2f} · regime-exit "
          f"{book['arms']['REGIME_EXIT']['nav']:.2f} "
          f"({len(actions['REGIME_EXIT'])} exits) · stop-only "
          f"{book['arms']['STOP_ONLY']['nav']:.2f} ({len(actions['STOP_ONLY'])} exits)")


if __name__ == "__main__":
    main()
