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
