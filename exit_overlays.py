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
  TAKE_PROFIT  exit any position at mtm >= +10% (registered 2026-08-20 after
               the +$3,074 round trip; predicted to underperform -- it amputates
               the right tail that funds a dip-buying book -- and tested
               honestly because prediction is not knowledge).

Run:  /opt/anaconda3/bin/python exit_overlays.py     (daily, after rotation_arm)
"""
from __future__ import annotations
# ROT-001 / SESSION-001 (2026-09-07): NAV compounds once per SESSION, never per run. The estate's one
# NYSE calendar is stock-radar/sessions.py, loaded by path (this repo is public and runs alone);
# weekday-only fallback if unavailable. Bars are picked by DATE (series_t, epoch days), never by position.
try:
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("_sessions", "/Users/anupampatil/stock-radar/sessions.py")
    _SESS = _iu.module_from_spec(_sp); _sp.loader.exec_module(_SESS)
except Exception:
    _SESS = None
def _settled_session():
    import datetime as _dt
    if _SESS: return _SESS.settled_session()
    now = _dt.datetime.now(); d = now.date()
    if d.weekday() >= 5 or (now.hour, now.minute) < (13, 5):
        d -= _dt.timedelta(days=1)
        while d.weekday() >= 5: d -= _dt.timedelta(days=1)
    return d
def _closes_for_session(e, sess):
    """(prev_close, close) for the bar dated `sess` and the bar before it, by DATE; None if the
    series has no bar for that session (radar not refreshed) — then nothing compounds."""
    import datetime as _dt
    ts = e.get("series_t", []) or []; cs = e.get("series_c", []) or []
    bars = [(_dt.date(1970, 1, 1) + _dt.timedelta(days=int(t)), c) for t, c in zip(ts, cs) if c]
    idx = [i for i, (d, _) in enumerate(bars) if d == sess]
    if not idx or idx[0] < 1: return None
    return (bars[idx[0] - 1][1], bars[idx[0]][1])

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


def last_two(tk, d, sess):
    """Closes for session `sess` and the one before, by date (ROT-001)."""
    e = next((x for x in d if x.get("ticker") == tk), None)
    return _closes_for_session(e, sess) if e else None


def main():
    radar = json.load(open(RADAR))
    arena = json.load(open(ARENA))
    opens = json.load(open(STATE))["open"]
    today = dt.date.today().isoformat()
    sess = _settled_session(); sess_iso = sess.isoformat()
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
    # an arm registered after the book was born initializes mid-flight at 100
    book["arms"].setdefault("TAKE_PROFIT", {"nav": 100.0, "weights": {}})
    if book.get("last_session") == sess_iso:   # ROT-001: one compounding per settled session
        print(f"exit_overlays: session {sess_iso} already compounded — refusing a second row"); return
    if not book.get("last_session"):
        book["last_session"] = sess_iso; book["last_run"] = today
        json.dump(book, open(BOOK, "w"), indent=1)
        print(f"exit_overlays: anchored to session {sess_iso} without compounding (ROT-001); rows resume at the next settled session"); return

    cur = {key(p): p for p in opens}
    eq = radar.get("equities", [])
    rets = {}
    for k, p in cur.items():
        pr = last_two(p["ticker"], eq, sess)
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
    actions = {"REGIME_EXIT": [], "STOP_ONLY": [], "TAKE_PROFIT": []}

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

    # TAKE_PROFIT: bank anything at or through +10% (REGISTRY.md 2026-08-20)
    w = book["arms"]["TAKE_PROFIT"]["weights"]
    for k in list(w):
        if w[k] > 0 and marks.get(k, 0.0) >= 0.10:
            w[k] = 0.0
            book["arms"]["TAKE_PROFIT"]["nav"] = round(
                book["arms"]["TAKE_PROFIT"]["nav"] * (1 - 2 * COST / max(len(w), 1)), 4)
            actions.setdefault("TAKE_PROFIT", []).append(cur[k]["ticker"])

    # STOP_ONLY: exit anything at or through -5%
    w = book["arms"]["STOP_ONLY"]["weights"]
    for k in list(w):
        if w[k] > 0 and marks.get(k, 0.0) <= STOP:
            w[k] = 0.0
            book["arms"]["STOP_ONLY"]["nav"] = round(
                book["arms"]["STOP_ONLY"]["nav"] * (1 - 2 * COST / max(len(w), 1)), 4)
            actions["STOP_ONLY"].append(cur[k]["ticker"])

    book["last_run"], book["last_regime"] = today, regime
    # ROT-001 REGRESSION (2026-09-10, Claude's own defect): the 09-07 fix set last_session with a
    # broad string replace that matched only the anchor block, not this tuple assignment, so a run
    # compounded, appended a row, and never advanced last_session — every 30-minute refresh then
    # compounded the SAME session again (12 rows for 09-08, 4 for 09-09). This is the line that ends it.
    book["last_session"] = sess_iso
    json.dump(book, open(BOOK, "w"), indent=1)

    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="") as f:
        wcsv = csv.writer(f)
        if new:
            wcsv.writerow(["date", "regime", "flipped", "nav_base", "nav_regime_exit",
                           "nav_stop_only", "regime_exits", "stop_exits",
                           "nav_take_profit", "tp_exits"])
        wcsv.writerow([sess_iso, regime, int(flipped), book["nav_base"],
                       book["arms"]["REGIME_EXIT"]["nav"],
                       book["arms"]["STOP_ONLY"]["nav"],
                       ";".join(actions["REGIME_EXIT"]),
                       ";".join(actions["STOP_ONLY"]),
                       book["arms"]["TAKE_PROFIT"]["nav"],
                       ";".join(actions.get("TAKE_PROFIT", []))])
    print(f"exit_overlays {today} [{regime}{' FLIP' if flipped else ''}]: "
          f"base {book['nav_base']:.2f} · regime-exit "
          f"{book['arms']['REGIME_EXIT']['nav']:.2f} "
          f"({len(actions['REGIME_EXIT'])} exits) · stop-only "
          f"{book['arms']['STOP_ONLY']['nav']:.2f} ({len(actions['STOP_ONLY'])} exits)")


if __name__ == "__main__":
    main()
