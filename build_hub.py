#!/usr/bin/env python3
"""Assemble every dataset into ONE file (hub_data.js) so the Trading Terminal shows
everything in one place — and loads via <script src> so it works from a plain
file:// double-click (no server, no CORS). Pulls together:
  Stock Radar monitor · Returns Matrix · Day-Type Radar · Strategy Lab survey.
Run: /opt/anaconda3/bin/python build_hub.py
"""
import json, os

HOME = os.path.expanduser("~")
LAB = os.path.join(HOME, "strategy-lab")
RADAR = os.path.join(HOME, "stock-radar")


def load(path, default=None):
    try:
        return json.load(open(path))
    except Exception:
        return default if default is not None else {}


def _csv(path):
    import csv
    try:
        with open(path) as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def _recorder_live(path):
    """Live out-of-sample tracker: the recorder logs per-day returns for the intraday
    strategies; this is their running forward-test (backtest said 'no edge')."""
    rows = _csv(path)
    if not rows:
        return None
    def stat(col):
        vals = [float(r[col]) for r in rows if r.get(col) not in (None, "", "nan")]
        if not vals:
            return None
        m = sum(vals) / len(vals)
        return {"n": len(vals), "avg_pct": round(m, 3),
                "hit_pct": round(100 * sum(1 for v in vals if v > 0) / len(vals), 1)}
    return {"sessions": len({r["date"] for r in rows}), "namedays": len(rows),
            "or_breakout": stat("or_breakout_ret"), "open_fade": stat("open_fade_ret")}


def _latest_md(briefs_dir, kind="morning"):
    """Newest brief file. kind: 'morning' (plain YYYY-MM-DD.md), 'earnings'
    (earnings-*.md), or 'coach' (coach-*.md)."""
    try:
        allmd = [f for f in os.listdir(briefs_dir) if f.endswith(".md")]
        if kind == "morning":
            names = [f for f in allmd if not f.startswith(("earnings-", "coach-"))]
        else:
            names = [f for f in allmd if f.startswith(kind + "-")]
        if not names:
            return None
        latest = sorted(names)[-1]
        return {"file": latest, "text": open(os.path.join(briefs_dir, latest)).read()}
    except Exception:
        return None


def main():
    radar = load(os.path.join(RADAR, "data", "radar.json"))
    hub = {
        "built": radar.get("updated", ""),
        "monitor": {
            "strip": radar.get("strip", []),
            "equities": radar.get("equities", []),
        },
        "returns": load(os.path.join(LAB, "reports", "returns_matrix.json")),
        "daytype": load(os.path.join(LAB, "reports", "universe_daytype.json")),
        "strategies": load(os.path.join(LAB, "reports", "data.json")),
        "intraday_study": load(os.path.join(LAB, "reports", "intraday_study.json")),
        "intraday_discover": load(os.path.join(LAB, "reports", "intraday_discover.json")),
        "earnings": load(os.path.join(LAB, "reports", "earnings_radar.json")),
        "plans": _csv(os.path.join(RADAR, "agent", "plans.csv")),
        "ledger": radar.get("ledger", []),
        "brief": _latest_md(os.path.join(RADAR, "agent", "briefs"), "morning"),
        "earnings_note": _latest_md(os.path.join(RADAR, "agent", "briefs"), "earnings"),
        "coach_note": _latest_md(os.path.join(RADAR, "agent", "briefs"), "coach"),
        "coach_report": load(os.path.join(RADAR, "agent", "coach_report.json")),
        "coach_log": _csv(os.path.join(RADAR, "agent", "coach_log.csv")),
        "progress": _csv(os.path.join(LAB, "progress.csv")),
        "recorder_live": _recorder_live(os.path.join(LAB, "daytype_log.csv")),
        # Graham Quality Gate (stock-radar/graham_gate.py, weekly task) — per-ticker
        # value screen for the terminal's ticker drawer
        "graham": load(os.path.join(RADAR, "data", "graham.json"), {}),
        # Position Agent's paper book (stock-radar/agent/positions.csv, weekly task)
        "positions": _csv(os.path.join(RADAR, "agent", "positions.csv")),
        # Paper Arena (arena.py, daily): rule strategies that actually take
        # paper trades — 1y backtest + live forward book, benchmarked vs SPY
        "arena": load(os.path.join(LAB, "reports", "arena.json"), {}),
        "position_report": load(os.path.join(RADAR, "agent", "position_report.json"), {}),
    }
    out = os.path.join(LAB, "hub_data.js")
    with open(out, "w") as f:
        f.write("window.HUB = " + json.dumps(hub) + ";")
    print(f"hub_data.js built: monitor {len(hub['monitor']['equities'])} names · "
          f"returns {hub['returns'].get('n_tickers','?')} · "
          f"daytype {hub['daytype'].get('n','?')} · "
          f"strategies {len(hub['strategies'].get('results',[]))} families · "
          f"intraday {len(hub['intraday_study'].get('time_of_day',[]))} slots")


if __name__ == "__main__":
    main()
