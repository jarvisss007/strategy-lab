#!/usr/bin/env python3
"""Earnings Radar — pre-earnings research with historical evidence, for the whole
universe. Three parts:

  1. EVENT STUDY (15y, per ticker): find past "event days" (overnight gap >= 4%
     with volume >= 2x its 20-day average — a free-data proxy for earnings and
     other binary events), then measure what actually happened next: the same-day
     open->close move (can you buy the gap?), and 5d / 21d post-event drift
     (the documented PEAD effect). Split by gap direction. These are the BASE
     RATES that back any pre-earnings thesis.
  2. PEER SPILLOVER: each name's top-5 return-correlated peers, and how those
     peers historically move on the name's event days — "what correlated stocks
     get affected."
  3. UPCOMING CALENDAR: next 14 days of earnings (Nasdaq free API) filtered to
     the universe, joined with each name's base rates -> a pre-earnings sheet.

Output: reports/earnings_radar.json + printed pre-earnings notes.
Honest caveats: event days are a proxy (earnings + other shocks); base rates are
averages with big variance; the universe is survivorship-biased; none of this is
advice — it is evidence to attach to falsifiable paper calls in the agent ledger.
Run: /opt/anaconda3/bin/python earnings_radar.py"""
# SESSION-001 (2026-09-05): the estate's one NYSE calendar lives in stock-radar/sessions.py;
# loaded by path (this repo runs alone), weekday-only fallback if it is unavailable.
try:
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("_sessions", "/Users/anupampatil/stock-radar/sessions.py")
    _SESS = _iu.module_from_spec(_sp); _sp.loader.exec_module(_SESS)
except Exception:
    _SESS = None
def _is_session(d):
    return _SESS.is_session(d) if _SESS else d.weekday() < 5
import json, os, urllib.request
import datetime as dt
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36", "Accept": "application/json, text/plain, */*",
      "Origin": "https://www.nasdaq.com", "Referer": "https://www.nasdaq.com/"}
GAP, VOLX = 0.04, 2.0


def load():
    rd = lambda n: pd.read_csv(os.path.join(BASE, "data", n), parse_dates=["date"]).set_index("date").sort_index()
    o, c, v = rd("open.csv"), rd("close.csv"), rd("volume.csv")
    common = o.columns.intersection(c.columns).intersection(v.columns)
    return o[common], c[common], v[common]


def _nanmean(xs):
    """Mean in pct, ignoring missing bars; None if nothing usable."""
    a = np.asarray(xs, float)
    a = a[np.isfinite(a)]
    return round(float(a.mean() * 100), 2) if a.size else None


def event_study(o, c, v):
    gap = o / c.shift(1) - 1
    relvol = v / v.rolling(20).mean()
    rets = c.pct_change()
    out = {}
    for t in c.columns:
        ev = gap[t][(gap[t].abs() >= GAP) & (relvol[t] >= VOLX)].dropna()
        if len(ev) < 8:
            continue
        rec = {"n_events": len(ev), "avg_abs_gap": round(float(ev.abs().mean() * 100), 2),
               "pct_gap_up": round(float((ev > 0).mean() * 100), 1)}
        for lbl, mask in (("up", ev > 0), ("down", ev < 0)):
            days = ev[mask].index
            if len(days) < 4:
                rec[lbl] = None
                continue
            oc = (c[t].loc[days] / o[t].loc[days] - 1)          # buyable same-day open->close
            d5, d21 = [], []
            for d in days:
                i = c.index.get_loc(d)
                if i + 5 < len(c):
                    d5.append(c[t].iloc[i + 5] / c[t].iloc[i] - 1)
                if i + 21 < len(c):
                    d21.append(c[t].iloc[i + 21] / c[t].iloc[i] - 1)
            rec[lbl] = {"n": len(days), "avg_gap": round(float(ev[mask].mean() * 100), 2),
                        "same_day_oc": round(float(oc.mean() * 100), 2),
                        "oc_hit": round(float((oc > 0).mean() * 100), 1),
                        # nanmean: a single missing bar in the price series used to poison the
                        # whole leg (and then the universe average) with NaN — 14 legs on the
                        # 2026-08-09 build, incl. the printed headline. Skip the gap, keep the leg.
                        "drift_5d": _nanmean(d5), "drift_21d": _nanmean(d21)}
        # peer spillover
        corr = rets.corrwith(rets[t]).drop(t).dropna().sort_values(ascending=False)
        peers = list(corr.head(5).index)
        spill = {}
        for lbl, mask in (("up", ev > 0), ("down", ev < 0)):
            days = ev[mask].index
            if len(days) >= 4 and peers:
                same = rets.loc[days, peers].mean(axis=1)
                nxt = rets.shift(-1).loc[days, peers].mean(axis=1)
                spill[lbl] = {"same_day": round(float(same.mean() * 100), 2),
                              "next_day": round(float(nxt.mean() * 100), 2)}
        rec["peers"] = [(p, round(float(corr[p]), 2)) for p in peers]
        rec["peer_spillover"] = spill
        out[t] = rec
    return out


def upcoming(days=14):
    cal, ok, err = [], 0, 0
    today = dt.date.today()
    for k in range(days):
        d = today + dt.timedelta(days=k)
        if not _is_session(d):
            continue
        try:
            url = f"https://api.nasdaq.com/api/calendar/earnings?date={d}"
            j = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=15))
            for r in (j.get("data") or {}).get("rows") or []:
                cal.append({"date": str(d), "ticker": r.get("symbol"), "when": r.get("time", "")})
            ok += 1
        except Exception:
            err += 1
            continue
    # honest status: an all-days-failed fetch is FAILED (unknown), never "zero reporters"
    status = "ok" if ok > 0 else "failed"
    return cal, status, ok, err


def main():
    o, c, v = load()
    study = event_study(o, c, v)
    cal, cal_status, cal_ok, cal_err = upcoming()
    uni = set(c.columns)
    ours = [r for r in cal if r["ticker"] in uni]
    out = {"built": dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z"),
           "gap_threshold": GAP, "vol_threshold": VOLX,
           "event_study": study, "upcoming_universe": ours, "upcoming_all_count": len(cal), "calendar_status": cal_status, "calendar_days_ok": cal_ok, "calendar_days_err": cal_err}
    json.dump(out, open(os.path.join(BASE, "reports", "earnings_radar.json"), "w"), indent=1)

    print(f"=== Earnings Radar — event study on {len(study)} names (15y) ===\n")
    # aggregate PEAD read
    up5 = [s["up"]["drift_5d"] for s in study.values() if s.get("up") and s["up"]["drift_5d"] is not None]
    dn5 = [s["down"]["drift_5d"] for s in study.values() if s.get("down") and s["down"]["drift_5d"] is not None]
    up_oc = [s["up"]["same_day_oc"] for s in study.values() if s.get("up")]
    dn_oc = [s["down"]["same_day_oc"] for s in study.values() if s.get("down")]
    print(f"Universe base rates (avg across names):")
    print(f"  after a BIG UP gap:   same-day open->close {np.mean(up_oc):+.2f}%   5d drift {np.mean(up5):+.2f}%")
    print(f"  after a BIG DOWN gap: same-day open->close {np.mean(dn_oc):+.2f}%   5d drift {np.mean(dn5):+.2f}%")
    print(f"\n=== Upcoming earnings in the universe (next 14 days): {len(ours)} ===")
    for r in ours:
        s = study.get(r["ticker"], {})
        line = f"  {r['date']} {r['ticker']:6s} {r['when']:18s}"
        if s:
            line += (f" | history: {s['n_events']} events, avg |gap| {s['avg_abs_gap']}%, "
                     f"{s['pct_gap_up']}% up")
            if s.get("up"):
                line += f" | up-gap 5d drift {s['up']['drift_5d']}%"
            if s.get("down"):
                line += f" | down-gap 5d drift {s['down']['drift_5d']}%"
        print(line)
        if s.get("peers"):
            print(f"           peers: {', '.join(p for p,_ in s['peers'])}")
    print("\nBase rates, not advice. The earnings agent turns these into falsifiable paper")
    print("calls in the shared ledger — scored later, comparable against analysts/StockTrak.")


if __name__ == "__main__":
    main()
