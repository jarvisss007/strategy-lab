#!/usr/bin/env python
"""rot_restate.py — ROT-001 restatement (Anupam, 2026-09-08): replay the rotation arm and the exit
overlays over SESSION-dated rows only, with the registered rules unchanged.

Why: rotation_arm.py and exit_overlays.py compounded once per RUN, not per SESSION, so a weekend
or a holiday re-applied the previous session's return (the same Friday return four times over
Labor Day weekend); 63% of the rotation arm's published gap accrued on days no market traded, and
the culls and boosts that fired on those days changed the weights, so dropping the rows is not a
restatement — the rules have to be re-run. Inputs are the arena's own record (reports/arena_trades.csv
+ reports/arena_state.json) and settled closes BY DATE from stock-radar/data/radar.json.

Faithful to the live code, quirks included (they are the registered rules; changing them resets
the record): daily returns ignore side; a position entering on session d earns d's full return;
a position the arena closes on d leaves both books before d's return; the first session anchors
without a return. Outputs beside the originals — nothing is edited in place:
  reports/rotation_log.csv            <- restated series (the live writer appends to it from 09-08)
  reports/rotation_log.pre-ROT-001.csv     the series as published, kept
  reports/exit_overlays_log.csv       <- restated;  reports/exit_overlays_log.pre-ROT-001.csv kept
  reports/rotation_book.json / exit_overlays.json   re-based to the restated 2026-09-04 state
  reports/rot_restate_note.json       old vs restated, by date
"""
import csv, json, os, sys, shutil, datetime as dt, importlib.util as _iu
HERE = os.path.dirname(os.path.abspath(__file__)); REP = os.path.join(HERE, "reports")
RADAR = "/Users/anupampatil/stock-radar/data/radar.json"
_sp = _iu.spec_from_file_location("_sessions", "/Users/anupampatil/stock-radar/sessions.py"); S = _iu.module_from_spec(_sp); _sp.loader.exec_module(S)
COST, CULL_AT, STOP, TP = 0.001, -0.02, -0.05, 0.10
ROT_START, OVL_START, END = dt.date(2026, 8, 17), dt.date(2026, 8, 18), dt.date(2026, 9, 4)
APPLY = "--apply" in sys.argv

def key(p): return f"{p['strategy']}|{p['ticker']}|{p['entry_date']}"

# ---- closes by (ticker, date) from the radar's dated series ----------------------------------
radar = json.load(open(RADAR)); PX = {}
for e in radar.get("equities", []):
    for t, c in zip(e.get("series_t", []), e.get("series_c", [])):
        if c: PX[(e["ticker"], dt.date(1970, 1, 1) + dt.timedelta(days=int(t)))] = c

# ---- every arena position, open or closed -----------------------------------------------------
pos = []
for r in csv.DictReader(open(os.path.join(REP, "arena_trades.csv"))):
    pos.append({"strategy": r["strategy"], "ticker": r["ticker"], "side": int(float(r["side"] or 1)), "entry_date": r["entry_date"],
                "entry_px": float(r["entry_px"]), "exit_date": r["exit_date"] or None})
for p in json.load(open(os.path.join(REP, "arena_state.json")))["open"]:
    pos.append({"strategy": p["strategy"], "ticker": p["ticker"], "side": int(p.get("side", 1)), "entry_date": p["entry_date"],
                "entry_px": float(p["entry_px"]), "exit_date": None})

def open_on(d):
    """the arena's open book AFTER its run on session d (positions closed on d have left)"""
    iso = d.isoformat(); cur = {}
    for p in pos:
        if p["entry_date"] <= iso and (p["exit_date"] is None or p["exit_date"] > iso):
            cur[key(p)] = p
    return cur

def rets_for(cur, d, prev):
    out = {}
    for k, p in cur.items():
        a, b = PX.get((p["ticker"], prev)), PX.get((p["ticker"], d))
        if a and b: out[k] = b / a - 1
    return out

def marks_for(cur, d):
    return {k: (p["side"] * (PX[(p["ticker"], d)] / p["entry_px"] - 1) if (p["ticker"], d) in PX else 0.0) for k, p in cur.items()}

sessions = [d for d in (ROT_START + dt.timedelta(days=i) for i in range((END - ROT_START).days + 1)) if S.is_session(d)]

# ---- rotation arm -------------------------------------------------------------------------------
rot_rows = []; book = {"start": sessions[0].isoformat(), "nav_base": 100.0, "nav_rot": 100.0, "weights": {}, "last_run": None}
prev = None
for d in sessions:
    cur = open_on(d); rets = rets_for(cur, d, prev) if prev else {}
    w = {k: v for k, v in book["weights"].items() if k in cur}
    for k in cur: w.setdefault(k, 1.0)
    if book["last_run"] and rets:
        held = [k for k in rets if k in w]
        if held:
            base_r = sum(rets[k] for k in held) / len(held); tot = sum(w[k] for k in held)
            rot_r = sum(w[k] * rets[k] for k in held) / tot if tot else 0.0
            book["nav_base"] = round(book["nav_base"] * (1 + base_r), 4); book["nav_rot"] = round(book["nav_rot"] * (1 + rot_r), 4)
    marks = marks_for(cur, d)
    culled = [k for k in w if marks.get(k, 0.0) < CULL_AT]; survivors = [k for k in w if k not in culled]; boosted = []
    if culled and survivors:
        ranked = sorted(survivors, key=lambda k: -marks.get(k, 0.0)); top = ranked[:max(1, len(ranked) // 4)]
        freed = sum(w[k] for k in culled); friction = freed * COST + freed * COST
        add = max(freed - friction * 100 / book["nav_rot"], 0.0) / len(top)
        for k in top: w[k] = round(w[k] + add, 4)
        boosted = top
        for k in culled: del w[k]
    elif culled:
        for k in culled: del w[k]
    book["weights"] = w; book["last_run"] = d.isoformat(); book["last_session"] = d.isoformat()
    rot_rows.append([d.isoformat(), book["nav_base"], book["nav_rot"], round(book["nav_rot"] - book["nav_base"], 4), len(w), len(culled), len(boosted),
                     ";".join(k.split("|")[1] for k in culled), ";".join(k.split("|")[1] for k in boosted)])
    prev = d
rot_book = book

# ---- exit overlays ----------------------------------------------------------------------------
old_ovl = {r["date"]: r for r in csv.DictReader(open(os.path.join(REP, "exit_overlays_log.csv")))}
regime_of = lambda d: (old_ovl.get(d.isoformat()) or {}).get("regime") or "calm-up"
ovl_rows = []; ob = {"start": OVL_START.isoformat(), "last_run": None, "last_regime": regime_of(OVL_START), "nav_base": 100.0,
                    "arms": {"REGIME_EXIT": {"nav": 100.0, "weights": {}}, "STOP_ONLY": {"nav": 100.0, "weights": {}}, "TAKE_PROFIT": {"nav": 100.0, "weights": {}}}}
prev = None
for d in [x for x in sessions if x >= OVL_START]:
    cur = open_on(d); rets = rets_for(cur, d, prev) if prev else {}; regime = regime_of(d)
    if ob["last_run"] and rets:
        held_all = [k for k in rets if k in cur]
        if held_all:
            ob["nav_base"] = round(ob["nav_base"] * (1 + sum(rets[k] for k in held_all) / len(held_all)), 4)
        for arm, st in ob["arms"].items():
            wts = st["weights"]; held = [k for k in held_all if wts.get(k, 1.0) > 0]; n_slots = len(held_all)
            if n_slots: st["nav"] = round(st["nav"] * (1 + sum(rets[k] for k in held) / n_slots), 4)
    for arm, st in ob["arms"].items():
        st["weights"] = {k: v for k, v in st["weights"].items() if k in cur}
        for k in cur: st["weights"].setdefault(k, 1.0)
    flipped = regime != ob.get("last_regime"); marks = marks_for(cur, d); acts = {"REGIME_EXIT": [], "STOP_ONLY": [], "TAKE_PROFIT": []}
    # REGIME_EXIT never fired in the window (no flip on any session); replayed as the live rule would
    w = ob["arms"]["TAKE_PROFIT"]["weights"]
    for k in list(w):
        if w[k] > 0 and marks.get(k, 0.0) >= TP:
            w[k] = 0.0; ob["arms"]["TAKE_PROFIT"]["nav"] = round(ob["arms"]["TAKE_PROFIT"]["nav"] * (1 - 2 * COST / max(len(w), 1)), 4); acts["TAKE_PROFIT"].append(cur[k]["ticker"])
    w = ob["arms"]["STOP_ONLY"]["weights"]
    for k in list(w):
        if w[k] > 0 and marks.get(k, 0.0) <= STOP:
            w[k] = 0.0; ob["arms"]["STOP_ONLY"]["nav"] = round(ob["arms"]["STOP_ONLY"]["nav"] * (1 - 2 * COST / max(len(w), 1)), 4); acts["STOP_ONLY"].append(cur[k]["ticker"])
    ob["last_run"], ob["last_regime"], ob["last_session"] = d.isoformat(), regime, d.isoformat()
    ovl_rows.append([d.isoformat(), regime, int(flipped), ob["nav_base"], ob["arms"]["REGIME_EXIT"]["nav"], ob["arms"]["STOP_ONLY"]["nav"],
                     ";".join(acts["REGIME_EXIT"]), ";".join(acts["STOP_ONLY"]), ob["arms"]["TAKE_PROFIT"]["nav"], ";".join(acts["TAKE_PROFIT"])])
    prev = d

# ---- compare and (optionally) apply ---------------------------------------------------------
old_rot = {r["date"]: r for r in csv.DictReader(open(os.path.join(REP, "rotation_log.csv")))}
last = rot_rows[-1]; o = old_rot.get(last[0], {})
print(f"ROTATION at {last[0]}: published base {o.get('nav_base')} rot {o.get('nav_rot')} gap {o.get('gap_pct')}  →  restated base {last[1]} rot {last[2]} gap {last[3]}   (published 09-07 gap {old_rot.get('2026-09-07',{}).get('gap_pct')})")
lo = ovl_rows[-1]; oo = old_ovl.get(lo[0], {})
print(f"OVERLAYS at {lo[0]}: published base {oo.get('nav_base')} stop {oo.get('nav_stop_only')} tp {oo.get('nav_take_profit')}  →  restated base {lo[3]} stop {lo[5]} tp {lo[8]}")
print(f"sessions replayed: {len(rot_rows)} (published log had {len(old_rot)} rows, {sum(1 for k in old_rot if not S.is_session(k))} of them non-sessions)")
note = {"as_of": dt.date.today().isoformat(), "ruling": "ROT-001 (Anupam 2026-09-08)", "rotation": {"published": {k: {c: v for c, v in r.items() if c in ('nav_base','nav_rot','gap_pct')} for k, r in old_rot.items()},
        "restated": {r[0]: {"nav_base": r[1], "nav_rot": r[2], "gap_pct": r[3]} for r in rot_rows}},
        "overlays": {"published": {k: {c: v for c, v in r.items() if c in ('nav_base','nav_stop_only','nav_take_profit')} for k, r in old_ovl.items()},
        "restated": {r[0]: {"nav_base": r[3], "nav_stop_only": r[5], "nav_take_profit": r[8]} for r in ovl_rows}}}
json.dump(note, open(os.path.join(REP, "rot_restate_note.json"), "w"), indent=1)
if APPLY:
    for name, rows, hdr in (("rotation_log.csv", rot_rows, ["date","nav_base","nav_rot","gap_pct","n_open","n_culled","n_boosted","culled","boosted"]),
                            ("exit_overlays_log.csv", ovl_rows, ["date","regime","flipped","nav_base","nav_regime_exit","nav_stop_only","regime_exits","stop_exits","nav_take_profit","tp_exits"])):
        src = os.path.join(REP, name); keep = src.replace(".csv", ".pre-ROT-001.csv")
        if not os.path.exists(keep): shutil.copy(src, keep)
        tmp = src + ".tmp"
        with open(tmp, "w", newline="") as f:
            w = csv.writer(f); w.writerow(hdr); w.writerows(rows)
        os.replace(tmp, src)
    rot_book["restated"] = "ROT-001 2026-09-08: re-based to the session-only replay at 2026-09-04"
    json.dump(rot_book, open(os.path.join(REP, "rotation_book.json"), "w"), indent=1)
    ob["restated"] = rot_book["restated"]; json.dump(ob, open(os.path.join(REP, "exit_overlays.json"), "w"), indent=1)
    print("APPLIED: restated logs in place (originals kept as *.pre-ROT-001.csv); books re-based to 2026-09-04")
else:
    print("dry run — pass --apply to write")
