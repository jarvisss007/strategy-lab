#!/opt/anaconda3/bin/python
"""earnings_puts_study.py - "buy puts before every earnings report" (his claim, 2026-10-17). Pre-registered at 4521297
(research/earnings_puts/PREREG.md); the bars, cells and price model are that file's, unchanged.

Inputs: data/prices.csv (adjusted closes), data/edgar/earnings_8k.json (print sessions, EARN-006 rule),
data/eps_surprise.json (Yahoo beat/miss label only), stock-radar/data/chains_equity (real October chains),
research/earnings_puts/week_implied_<monday>.json (the coming week's implied moves).
Output: research/earnings_puts/results_<date>.json. Read-only on everything else.
"""
import csv, datetime as dt, glob, json, math, os, re, statistics as st
from bisect import bisect_left
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(HERE))
CHAINS = os.path.expanduser("~/stock-radar/data/chains_equity")
NY, UTC = ZoneInfo("America/New_York"), dt.timezone.utc
START = "2011-12-01"          # first prints with >= 60 sessions of panel history before them
HOLDS = (1, 2, 3)             # sessions held into the reaction close; primary = 2
PRIOR_N, PRIOR_MIN = 8, 4
SEASON_DAYS = 45


# ───────────── data ─────────────
def load_prices():
    rows = list(csv.DictReader(open(f"{BASE}/data/prices.csv")))
    dates = [r["date"] for r in rows]
    px = {t: [float(r[t]) if r.get(t) not in (None, "") else None for r in rows] for t in rows[0] if t != "date"}
    return dates, px


def print_session(accepted, dates):
    """Same rule as earnings_postgap_study.print_session (EARN-006): UTC stamp -> New York; before 16:00 that session."""
    et = dt.datetime.fromisoformat(accepted[:19]).replace(tzinfo=UTC).astimezone(NY)
    d, hhmm = et.strftime("%Y-%m-%d"), et.strftime("%H:%M")
    i = bisect_left(dates, d)
    if i >= len(dates):
        return None
    if dates[i] == d and hhmm < "16:00":
        return i
    return i + 1 if dates[i] == d else i


def yahoo_session(ts_iso, dates):
    """Yahoo stamps carry their own ET offset: before 16:00 on a session -> that session, else the next one."""
    et = dt.datetime.fromisoformat(ts_iso).astimezone(NY)
    d, hhmm = et.strftime("%Y-%m-%d"), et.strftime("%H:%M")
    i = bisect_left(dates, d)
    if i >= len(dates):
        return None
    if dates[i] == d and hhmm < "16:00":
        return i
    return i + 1 if dates[i] == d else i


def cr1_t(xs, groups):
    """Pooled mean with a CR1 cluster-robust SE (clusters = announcement weeks). The t of the PRINTED pooled number."""
    n = len(xs)
    if n < 3:
        return None
    m = sum(xs) / n
    S = {}
    for x, g in zip(xs, groups):
        S[g] = S.get(g, 0.0) + (x - m)
    G = len(S)
    if G < 3:
        return None
    var = (G / (G - 1)) * sum(v * v for v in S.values()) / (n * n)
    return round(m / math.sqrt(var), 2) if var > 0 else None


def week_of(d):
    y, w, _ = dt.date.fromisoformat(d).isocalendar()
    return f"{y}-W{w:02d}"


def era_of(d):
    return "2011-15" if d < "2016-01-01" else ("2016-20" if d < "2021-01-01" else "2021-26")


def cell(evs, key):
    xs = [e[key] for e in evs if e.get(key) is not None]
    gs = [week_of(e["date"]) for e in evs if e.get(key) is not None]
    if not xs:
        return {"n": 0}
    return {"n": len(xs), "mean": round(st.mean(xs), 3), "median": round(st.median(xs), 3),
            "pos_pct": round(100 * sum(1 for x in xs if x > 0) / len(xs), 1), "t_cr1": cr1_t(xs, gs)}


# ───────────── events ─────────────
def build_events(dates, px):
    feed = json.load(open(f"{BASE}/data/edgar/earnings_8k.json"))
    eps = json.load(open(f"{BASE}/data/eps_surprise.json"))["tickers"] if os.path.exists(f"{BASE}/data/eps_surprise.json") else {}
    spy = px["SPY"]
    out = []
    for t, v in feed.items():
        if t not in px:
            continue
        p = px[t]
        Ts = sorted({i for i in (print_session(e["accepted"], dates) for e in v["events"] if e.get("accepted")) if i is not None})
        kept = []
        for i in Ts:                      # an amendment or a second 8-K inside 20 sessions is the same print
            if kept and i - kept[-1] < 20:
                continue
            kept.append(i)
        # Yahoo beat/miss, matched by session (+-3 sessions), nearest wins
        ylab = []
        for r in eps.get(t, []):
            j = yahoo_session(r["ts"], dates)
            if j is not None and r.get("surprise_pct") is not None:
                ylab.append((j, r["surprise_pct"]))
        prior_abs = []
        for i in kept:
            if i < 65 or i >= len(dates) or p[i] is None or p[i - 1] is None or spy[i] is None or spy[i - 1] is None:
                continue
            r0 = p[i] / p[i - 1] - 1
            ev = {"ticker": t, "T": i, "date": dates[i], "react": 100 * r0,
                  "react_x": 100 * (r0 - (spy[i] / spy[i - 1] - 1)), "era": era_of(dates[i])}
            near = [(abs(j - i), s) for j, s in ylab if abs(j - i) <= 3]
            if near:
                ev["surprise_pct"] = min(near)[1]
            usable = dates[i] >= START and len(prior_abs) >= PRIOR_MIN
            if usable:
                J = math.sqrt(math.pi / 2) * st.mean(prior_abs[-PRIOR_N:])
                ev["J"] = J
                for h in HOLDS:
                    a = i - h
                    seg = [p[k] for k in range(a - 60, a + 1)]
                    if p[a] is None or any(x is None for x in seg):
                        continue
                    lr = [math.log(seg[k + 1] / seg[k]) for k in range(len(seg) - 1)]
                    sig = st.pstdev(lr)
                    s = math.sqrt(J * J + (h - 1) * sig * sig)
                    price = 0.3989 * s
                    r = p[i] / p[a] - 1
                    ev[f"put_h{h}"] = 100 * (max(0.0, -r) / price - 1)       # % of premium
                    ev[f"price_h{h}"] = 100 * price                          # % of spot
                    ev[f"short_h{h}"] = -100 * r
                    ev[f"short_x_h{h}"] = -100 * (r - (spy[i] / spy[a] - 1))
            if dates[i] >= START:
                out.append(ev) if usable else None
            prior_abs.append(abs(r0))
    return out


# ───────────── H3: TSMC season ─────────────
def tsm_seasons(dates, px, events):
    eps = json.load(open(f"{BASE}/data/eps_surprise.json"))["tickers"].get("TSM", [])
    p, spy = px["TSM"], px["SPY"]
    rows = []
    for r in eps:
        if r.get("rep") is None:
            continue
        i = yahoo_session(r["ts"], dates)
        if i is None or i < 1 or i >= len(dates) or dates[i] < START or None in (p[i], p[i - 1]):
            continue
        x = 100 * (p[i] / p[i - 1] - 1 - (spy[i] / spy[i - 1] - 1))
        d0 = dt.date.fromisoformat(dates[i])
        lo, hi = dates[i], (d0 + dt.timedelta(days=SEASON_DAYS)).isoformat()
        season = [e["react_x"] for e in events if lo < e["date"] <= hi]
        if len(season) < 10:
            continue
        rows.append({"date": dates[i], "tsm_react_x": round(x, 2), "tsm_surprise": r.get("surprise_pct"),
                     "season_n": len(season), "season_mean_x": round(st.mean(season), 3),
                     "season_down_pct": round(100 * sum(1 for s in season if s < 0) / len(season), 1)})
    dn = [r["season_mean_x"] for r in rows if r["tsm_react_x"] < 0]
    up = [r["season_mean_x"] for r in rows if r["tsm_react_x"] > 0]
    def welch(a, b):
        if len(a) < 3 or len(b) < 3:
            return None
        se = math.sqrt(st.variance(a) / len(a) + st.variance(b) / len(b))
        return round((st.mean(a) - st.mean(b)) / se, 2) if se else None
    beat_fell = [r["season_mean_x"] for r in rows if r["tsm_react_x"] < 0 and (r["tsm_surprise"] or 0) > 0]
    return {"seasons": rows,
            "after_tsm_down": {"n": len(dn), "mean_x": round(st.mean(dn), 3) if dn else None},
            "after_tsm_up": {"n": len(up), "mean_x": round(st.mean(up), 3) if up else None},
            "after_tsm_beat_but_fell": {"n": len(beat_fell), "mean_x": round(st.mean(beat_fell), 3) if beat_fell else None},
            "diff_down_minus_up": round(st.mean(dn) - st.mean(up), 3) if dn and up else None,
            "t_welch": welch(dn, up)}


# ───────────── real October chains ─────────────
OCC = re.compile(r"^([A-Z.]+)(\d{6})([CP])(\d{8})$")


def chain_puts(path):
    d = json.load(open(path))
    puts = {}
    for o in d["options"]:
        m = OCC.match(o["option"])
        if not m or m.group(3) != "P":
            continue
        exp = dt.datetime.strptime(m.group(2), "%y%m%d").date().isoformat()
        puts[(exp, int(m.group(4)) / 1000)] = o
    return d["spot"], puts


def real_october(dates, events):
    rows = []
    for e in events:
        if not ("2026-09-24" <= e["date"] <= "2026-10-16"):
            continue
        i = e["T"]
        din, dout = dates[i - 2], dates[i]
        fin, fout = f"{CHAINS}/{e['ticker']}_{din}.json", f"{CHAINS}/{e['ticker']}_{dout}.json"
        if not (os.path.exists(fin) and os.path.exists(fout)):
            continue
        spot, pin = chain_puts(fin)
        _, pout = chain_puts(fout)
        exps = sorted({k[0] for k in pin if k[0] >= dout})
        if not exps:
            continue
        exp = exps[0]
        ks = sorted(k[1] for k in pin if k[0] == exp)
        K = min(ks, key=lambda k: abs(k - spot))
        a, b = pin[(exp, K)], pout.get((exp, K))
        if not b or not a.get("ask") or a["ask"] <= 0:
            continue
        mid_in = (a["bid"] + a["ask"]) / 2 if a.get("bid") else a["ask"]
        rows.append({"ticker": e["ticker"], "report_session": dout, "bought": din, "expiry": exp, "strike": K,
                     "spot_in": round(spot, 2), "ask_in": a["ask"], "mid_in": round(mid_in, 2), "bid_out": b.get("bid"),
                     "pnl_pct_ask_bid": round(100 * ((b.get("bid") or 0) / a["ask"] - 1), 1),
                     "pnl_pct_mid_mid": round(100 * ((((b.get("bid") or 0) + (b.get("ask") or 0)) / 2) / mid_in - 1), 1) if mid_in else None,
                     "put_cost_pct_spot": round(100 * mid_in / spot, 2),
                     "model_price_pct_spot": round(e["price_h2"], 2) if e.get("price_h2") else None,
                     "k_real": round((100 * mid_in / spot) / e["price_h2"], 2) if e.get("price_h2") else None,
                     "stock_move_pct": round(-e["short_h2"], 2) if e.get("short_h2") is not None else None,
                     "react_pct": round(e["react"], 2), "surprise_pct": e.get("surprise_pct")})
    return rows


# ───────────── coming week ─────────────
def coming_week(dates, px, events):
    fs = sorted(glob.glob(f"{HERE}/week_implied_*.json"))
    if not fs:
        return None
    wk = json.load(open(fs[-1]))
    byt = {}
    for e in events:
        byt.setdefault(e["ticker"], []).append(e)
    rows = []
    for r in wk["earnings"]:
        if r.get("error") or not r.get("straddle"):
            rows.append({"name": r["name"], "report_et": r["report_et"], "when": r["when"], "error": r.get("error", "no chain")})
            continue
        put_pct = r["move_pct"] / 2                  # ATM put ~ half the ATM straddle
        hist = byt.get(r["name"], [])
        reacts = [e["react"] for e in hist]
        moves2 = [-e["short_h2"] for e in hist if e.get("short_h2") is not None]
        row = {"name": r["name"], "desc": r.get("desc"), "cap_b": r["cap_b"], "report_et": r["report_et"], "when": r["when"],
               "expiry": r["exp"], "implied_move_pct": r["move_pct"], "atm_put_pct": round(put_pct, 2),
               "put_breakeven_drop_pct": round(put_pct, 2), "atm_iv": r.get("atm_iv"), "n_past_prints": len(hist)}
        if reacts:
            row.update({"past_mean_abs_react": round(st.mean(abs(x) for x in reacts), 2),
                        "past_down_pct": round(100 * sum(1 for x in reacts if x < 0) / len(reacts), 1),
                        "past_drop_beyond_breakeven_pct": round(100 * sum(1 for x in moves2 if x < -put_pct) / len(moves2), 1) if moves2 else None,
                        "past_model_put_mean_pct": round(st.mean(e["put_h2"] for e in hist if e.get("put_h2") is not None), 1)})
        rows.append(row)
    return {"fetched_pt": wk["fetched_pt"], "week": wk["week"], "min_cap_b": wk["min_cap"] / 1e9, "names": rows}


def main():
    dates, px = load_prices()
    ev = build_events(dates, px)
    beats = [e for e in ev if (e.get("surprise_pct") or 0) > 0]
    misses = [e for e in ev if e.get("surprise_pct") is not None and e["surprise_pct"] < 0]
    labelled = [e for e in ev if e.get("surprise_pct") is not None]
    res = {"generated": dt.datetime.now().isoformat(timespec="seconds"), "prereg": "4521297", "prices_through": dates[-1],
           "n_prints": len(ev), "n_tickers": len({e["ticker"] for e in ev}), "n_with_eps_label": len(labelled),
           "first_print": min(e["date"] for e in ev), "last_print": max(e["date"] for e in ev)}
    res["H1"] = {"beats_react": cell(beats, "react"), "beats_react_x": cell(beats, "react_x"),
                 "misses_react": cell(misses, "react"), "misses_react_x": cell(misses, "react_x"),
                 "all_react": cell(ev, "react"), "all_react_x": cell(ev, "react_x"),
                 "beat_share_pct": round(100 * len(beats) / len(labelled), 1) if labelled else None,
                 "big_beats_gt5_react": cell([e for e in beats if e["surprise_pct"] > 5], "react")}
    h2 = {}
    for h in HOLDS:
        h2[f"h{h}"] = {"all": cell(ev, f"put_h{h}"), "beats": cell(beats, f"put_h{h}"), "misses": cell(misses, f"put_h{h}"),
                       "eras": {er: cell([e for e in ev if e["era"] == er], f"put_h{h}") for er in ("2011-15", "2016-20", "2021-26")},
                       "y2025_26": cell([e for e in ev if e["date"] >= "2025-01-01"], f"put_h{h}"),
                       "price_pct_spot_median": round(st.median(e[f"price_h{h}"] for e in ev if e.get(f"price_h{h}")), 2)}
    res["H2"] = h2
    res["short_stock_h2"] = {"raw": cell(ev, "short_h2"), "vs_spy": cell(ev, "short_x_h2"),
                             "y2025_26_raw": cell([e for e in ev if e["date"] >= "2025-01-01"], "short_h2")}
    res["H3"] = tsm_seasons(dates, px, ev)
    oc = real_october(dates, ev)
    res["real_october"] = {"rows": oc, "n": len(oc),
                           "mean_pnl_ask_bid": round(st.mean(r["pnl_pct_ask_bid"] for r in oc), 1) if oc else None,
                           "mean_pnl_mid_mid": round(st.mean(r["pnl_pct_mid_mid"] for r in oc if r["pnl_pct_mid_mid"] is not None), 1) if oc else None,
                           "winners": sum(1 for r in oc if r["pnl_pct_ask_bid"] > 0),
                           "k_real_median": round(st.median(r["k_real"] for r in oc if r["k_real"]), 2) if oc else None}
    k = res["real_october"]["k_real_median"]
    # bid/ask cost, in points of premium, measured on the same real October round trips (closing quotes)
    spread = round(st.mean(r["pnl_pct_mid_mid"] - r["pnl_pct_ask_bid"] for r in oc if r["pnl_pct_mid_mid"] is not None), 1) if oc else None
    res["real_october"]["spread_cost_pts"] = spread
    if k:   # every hold repriced at the real-market surcharge: payoff/(k*price) - 1, then less the measured spread
        for h in HOLDS:
            xs = [(e[f"put_h{h}"] / 100 + 1) / k * 100 - 100 for e in ev if e.get(f"put_h{h}") is not None]
            gs = [week_of(e["date"]) for e in ev if e.get(f"put_h{h}") is not None]
            m = st.mean(xs)
            res["H2"][f"h{h}"]["at_k_real"] = {"k": k, "mean": round(m, 3), "t_cr1": cr1_t(xs, gs),
                                               "after_spread": round(m - spread, 1) if spread is not None else None}
    years = {}
    for e in ev:
        if e.get("put_h2") is not None:
            years.setdefault(e["date"][:4], []).append(e["put_h2"])
    res["H2"]["h2"]["by_year"] = {y: {"n": len(v), "mean": round(st.mean(v), 1)} for y, v in sorted(years.items()) if len(v) >= 30}
    res["H1"]["beats_fell_pct"] = round(100 * sum(1 for e in beats if e["react"] < 0) / len(beats), 1)
    # TSMC's own put this week, same model (its prints dated by Yahoo; TSM files 6-Ks, not 8-Ks)
    teps = json.load(open(f"{BASE}/data/eps_surprise.json"))["tickers"].get("TSM", [])
    tT = sorted({yahoo_session(r["ts"], dates) for r in teps if r.get("rep") is not None} - {None})
    tp = px["TSM"]
    i15 = dates.index("2026-10-15")
    prior = [abs(tp[i] / tp[i - 1] - 1) for i in tT if 0 < i < i15][-PRIOR_N:]
    J = math.sqrt(math.pi / 2) * st.mean(prior)
    seg = [tp[j] for j in range(i15 - 2 - 60, i15 - 1)]
    sig = st.pstdev([math.log(seg[j + 1] / seg[j]) for j in range(60)])
    price = 0.3989 * math.sqrt(J * J + sig * sig)
    r2 = tp[i15] / tp[i15 - 2] - 1
    tre = [tp[i] / tp[i - 1] - 1 for i in tT if 0 < i <= i15 and dates[i] >= START]
    res["tsm_put"] = {"price_pct_spot": round(100 * price, 2), "result_pct_premium": round(100 * (max(0, -r2) / price - 1), 1),
                      "surprise_pct": next((r["surprise_pct"] for r in teps if r["ts"].startswith("2026-10-15")), None),
                      "past_prints": len(tre), "past_down": sum(1 for x in tre if x < 0)}
    # TSMC this week, in the same units
    p, sp = px["TSM"], px["SPY"]
    i = dates.index("2026-10-15")
    res["tsm_2026_10"] = {d: round(p[dates.index(d)], 2) for d in ("2026-10-12", "2026-10-13", "2026-10-14", "2026-10-15", "2026-10-16")}
    res["tsm_2026_10"].update({"react_pct": round(100 * (p[i] / p[i - 1] - 1), 2), "spy_react_pct": round(100 * (sp[i] / sp[i - 1] - 1), 2),
                               "two_day_hold_pct": round(100 * (p[i] / p[i - 2] - 1), 2),
                               "tue_to_fri_pct": round(100 * (p[i + 1] / p[i - 2] - 1), 2)})
    peers = ("NVDA", "AMD", "ASML", "AVGO", "MU", "SPY")
    res["peers_tue_to_fri_pct"] = {t: round(100 * (px[t][i + 1] / px[t][i - 2] - 1), 2) for t in peers}
    res["coming_week"] = coming_week(dates, px, ev)
    out = f"{HERE}/results_{dt.date.today().isoformat()}.json"
    json.dump(res, open(out + ".tmp", "w"), indent=1)
    os.replace(out + ".tmp", out)
    print(json.dumps({k: v for k, v in res.items() if k not in ("real_october", "coming_week", "H3")}, indent=1))
    print("H3", json.dumps({k: v for k, v in res["H3"].items() if k != "seasons"}))
    print("real_october", json.dumps({k: v for k, v in res["real_october"].items() if k != "rows"}))
    print("wrote", out)


if __name__ == "__main__":
    main()
