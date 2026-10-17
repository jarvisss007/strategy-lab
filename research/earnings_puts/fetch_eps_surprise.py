#!/usr/bin/env python
"""fetch_eps_surprise.py - Yahoo EPS estimate / reported / surprise per print, for the earnings-puts study (2026-10-17).

Reads the tickers of data/edgar/earnings_8k.json plus TSM (the bellwether), writes data/eps_surprise.json.
Yahoo is used ONLY for the beat/miss label; the print DATE and session come from the EDGAR feed (filing header truth).
"""
import json, os, sys, time, datetime as dt
import yfinance as yf

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = f"{BASE}/data/eps_surprise.json"
tickers = sorted(json.load(open(f"{BASE}/data/edgar/earnings_8k.json")).keys()) + ["TSM"]
out = {"fetched_utc": dt.datetime.utcnow().isoformat(timespec="seconds"), "source": "yfinance get_earnings_dates(limit=100)", "tickers": {}}
for i, t in enumerate(tickers):
    for attempt in range(3):
        try:
            df = yf.Ticker(t).get_earnings_dates(limit=100)
            rows = []
            if df is not None:
                for ts, r in df.iterrows():
                    rows.append({"ts": ts.isoformat(), "est": None if r.isna()["EPS Estimate"] else float(r["EPS Estimate"]),
                                 "rep": None if r.isna()["Reported EPS"] else float(r["Reported EPS"]),
                                 "surprise_pct": None if r.isna()["Surprise(%)"] else float(r["Surprise(%)"])})
            out["tickers"][t] = rows
            break
        except Exception as ex:
            print(t, "attempt", attempt, ex, file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    time.sleep(0.6)
    if i % 20 == 0:
        print(i, t, len(out["tickers"].get(t, [])), flush=True)
json.dump(out, open(OUT + ".tmp", "w"))
os.replace(OUT + ".tmp", OUT)
print("wrote", OUT, sum(len(v) for v in out["tickers"].values()), "rows", len(out["tickers"]), "tickers")
