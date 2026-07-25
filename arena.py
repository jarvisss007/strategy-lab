#!/usr/bin/env python3
"""Paper Arena — the agent actually takes trades (paper), so the strategies can
be judged by experience instead of stared at.

Six fixed rule-based strategies (parameters set a priori, never optimized here)
run two ways over the Stock Radar universe (~120 names, 1y daily):

  1. BACKTEST: replay the full year of history for instant analysis.
  2. FORWARD:  every daily refresh, open/close live paper positions and log
     them to reports/arena_trades.csv — the honest out-of-sample record.

Strategies (LONG unless noted):
  DEEP_DIP      fresh cross below −40% off the 52w high → buy, hold 10 sessions
                 (Anupam's hypothesis: "very low from the year's high → buy")
  PANIC_BOUNCE  1-day return ≤ −5% → buy, hold 2 sessions
  DOUBLE_DIP    two consecutive down days totaling ≤ −6% → buy, hold 3
  FRESH_HIGH    new 52w high → buy, hold 10 (momentum continuation)
  SHORT_EXT     new 52w high while ≥ +100% above the 52w low → SHORT, hold 5
                 (Anupam's hypothesis: "very high from the year's low → sell")
  TREND_RIDER   close crosses above the 50d MA while above the 200d MA → buy,
                 hold 15

Conventions (identical in backtest and forward so they are comparable):
entry/exit at the signal close · 10 bps cost per side · one open position per
ticker per strategy · max 10 concurrent per strategy in forward mode · every
trade benchmarked against SPY over the identical window.

Run: /opt/anaconda3/bin/python arena.py            (after stock-radar collector)
"""
import csv, json, math, os
from datetime import date

HOME = os.path.expanduser("~")
LAB = os.path.join(HOME, "strategy-lab")
RADAR = os.path.join(HOME, "stock-radar", "data", "radar.json")
REPORTS = os.path.join(LAB, "reports")
STATE_F = os.path.join(REPORTS, "arena_state.json")
TRADES_F = os.path.join(REPORTS, "arena_trades.csv")
COST = 0.001            # 10 bps per side
MAX_OPEN = 10           # forward-mode cap per strategy

STRATS = {
    "DEEP_DIP":     {"hold": 10, "side": 1,
                     "desc": "fresh −40% off 52w high → buy 10d"},
    "PANIC_BOUNCE": {"hold": 2,  "side": 1,
                     "desc": "1d ≤ −5% → buy 2d"},
    "DOUBLE_DIP":   {"hold": 3,  "side": 1,
                     "desc": "2 down days ≤ −6% total → buy 3d"},
    "FRESH_HIGH":   {"hold": 10, "side": 1,
                     "desc": "new 52w high → buy 10d"},
    "SHORT_EXT":    {"hold": 5,  "side": -1,
                     "desc": "new high & ≥2× 52w low → short 5d"},
    "TREND_RIDER":  {"hold": 15, "side": 1,
                     "desc": "cross above 50MA, above 200MA → buy 15d"},
}


def signals_at(c, i):
    """Which strategies trigger on bar i of close series c (needs i ≥ 51)."""
    out = []
    hi = max(c[:i + 1]); lo = min(c[:i + 1])
    off_hi = c[i] / hi - 1
    off_hi_prev = c[i - 1] / max(c[:i]) - 1
    r1 = c[i] / c[i - 1] - 1
    r_prev = c[i - 1] / c[i - 2] - 1
    if off_hi <= -0.40 and off_hi_prev > -0.40:
        out.append("DEEP_DIP")
    if r1 <= -0.05:
        out.append("PANIC_BOUNCE")
    if r1 < 0 and r_prev < 0 and (c[i] / c[i - 2] - 1) <= -0.06:
        out.append("DOUBLE_DIP")
    new_hi = c[i] >= hi * 0.9999
    if new_hi:
        out.append("FRESH_HIGH")
        if c[i] / lo - 1 >= 1.0:
            out.append("SHORT_EXT")
    if i >= 200:
        ma50 = sum(c[i - 49:i + 1]) / 50
        ma50p = sum(c[i - 50:i]) / 50
        ma200 = sum(c[i - 199:i + 1]) / 200
        if c[i] > ma50 and c[i - 1] <= ma50p and c[i] > ma200:
            out.append("TREND_RIDER")
    return out


def net_ret(entry, exit_, side):
    gross = side * (exit_ / entry - 1)
    return gross - 2 * COST


def spy_ret(spy_by_day, d_in, d_out):
    a, b = spy_by_day.get(d_in), spy_by_day.get(d_out)
    return (b / a - 1) if a and b else None


def stats(trades):
    if not trades:
        return {"n": 0}
    rs = [t["net"] for t in trades]
    ex = [t["excess"] for t in trades if t["excess"] is not None]
    n = len(rs); mean = sum(rs) / n
    sd = math.sqrt(sum((r - mean) ** 2 for r in rs) / n) if n > 1 else 0
    t = mean / (sd / math.sqrt(n)) if sd > 0 else 0
    return {"n": n,
            "avg_bps": round(mean * 1e4, 1),
            "hit_pct": round(100 * sum(1 for r in rs if r > 0) / n, 1),
            "avg_excess_bps": round(sum(ex) / len(ex) * 1e4, 1) if ex else None,
            "t_stat": round(t, 2),
            "total_pct": round(sum(rs) * 100, 1)}


def verdict(s):
    if s["n"] < 10:
        return "too few trades"
    if s["avg_bps"] <= 0 or (s["avg_excess_bps"] or -1) <= 0:
        return "DEAD — loses to costs/SPY"
    if s["t_stat"] >= 2:
        return "CANDIDATE — send to the deflation gate"
    return "WATCH — positive but not significant"


def main():
    radar = json.load(open(RADAR))
    spy = next((s for s in radar["strip"] if s["ticker"] == "SPY"), None)
    spy_by_day = dict(zip(spy["series_t"], spy["series_c"])) if spy else {}
    eq = [e for e in radar["equities"] if len(e.get("series_c", [])) > 60]

    # ---------------- 1 · backtest the full year ----------------------------
    bt = {k: [] for k in STRATS}
    for e in eq:
        c, tdays = e["series_c"], e["series_t"]
        open_until = {k: -1 for k in STRATS}   # no overlapping trades per name
        for i in range(51, len(c)):
            for s in signals_at(c, i):
                cfg = STRATS[s]
                if i <= open_until[s]:
                    continue
                j = min(i + cfg["hold"], len(c) - 1)
                if j <= i:
                    continue
                nr = net_ret(c[i], c[j], cfg["side"])
                sp = spy_ret(spy_by_day, tdays[i], tdays[j])
                bt[s].append({"ticker": e["ticker"], "net": nr,
                              "excess": nr - sp if sp is not None else None})
                open_until[s] = j
    backtest = {k: {**stats(v), "desc": STRATS[k]["desc"],
                    "side": "SHORT" if STRATS[k]["side"] < 0 else "LONG"}
                for k, v in bt.items()}
    for k in backtest:
        backtest[k]["verdict"] = verdict(backtest[k]) if backtest[k]["n"] else "no trades"

    # ---------------- 2 · forward paper book --------------------------------
    state = {"open": []}
    if os.path.exists(STATE_F):
        state = json.load(open(STATE_F))
    px = {e["ticker"]: dict(zip(e["series_t"], e["series_c"])) for e in eq}
    last_day = {e["ticker"]: e["series_t"][-1] for e in eq}
    today = date.today().isoformat()

    closed_now = []
    still_open = []
    for p in state["open"]:
        tk = p["ticker"]
        days = sorted(px.get(tk, {}))
        if not days:
            still_open.append(p); continue
        elapsed = sum(1 for d in days if d > p["entry_t"])
        cur = px[tk][days[-1]]
        if elapsed >= p["hold"]:
            nr = net_ret(p["entry_px"], cur, p["side"])
            sp = spy_ret(spy_by_day, p["entry_t"], days[-1])
            row = {**p, "exit_date": today, "exit_px": cur, "net": round(nr, 5),
                   "excess": round(nr - sp, 5) if sp is not None else ""}
            closed_now.append(row)
        else:
            p["mtm"] = round(p["side"] * (cur / p["entry_px"] - 1) - 2 * COST, 5)
            p["days_left"] = p["hold"] - elapsed
            still_open.append(p)

    # new entries on the latest bar
    held = {(p["strategy"], p["ticker"]) for p in still_open}
    count = {k: sum(1 for p in still_open if p["strategy"] == k) for k in STRATS}
    for e in eq:
        c = e["series_c"]; i = len(c) - 1
        if i < 51:
            continue
        for s in signals_at(c, i):
            if (s, e["ticker"]) in held or count.get(s, 0) >= MAX_OPEN:
                continue
            cfg = STRATS[s]
            still_open.append({"strategy": s, "ticker": e["ticker"],
                               "side": cfg["side"], "hold": cfg["hold"],
                               "entry_date": today, "entry_t": e["series_t"][i],
                               "entry_px": c[i], "mtm": 0.0,
                               "days_left": cfg["hold"]})
            held.add((s, e["ticker"])); count[s] = count.get(s, 0) + 1

    # persist
    os.makedirs(REPORTS, exist_ok=True)
    json.dump({"open": still_open}, open(STATE_F, "w"), indent=1)
    cols = ["strategy", "ticker", "side", "entry_date", "entry_px",
            "exit_date", "exit_px", "net", "excess"]
    new_file = not os.path.exists(TRADES_F)
    with open(TRADES_F, "a") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        if new_file:
            w.writeheader()
        for r in closed_now:
            w.writerow(r)

    fwd_trades = list(csv.DictReader(open(TRADES_F))) if os.path.exists(TRADES_F) else []
    fwd_stats = {}
    for k in STRATS:
        rows = [{"net": float(r["net"]),
                 "excess": float(r["excess"]) if r["excess"] else None}
                for r in fwd_trades if r["strategy"] == k]
        fwd_stats[k] = stats(rows)

    out = {
        "updated": radar.get("updated", ""),
        "universe": len(eq),
        "conventions": "entry/exit at signal close · 10 bps/side · benchmarked vs SPY "
                       "over the identical window · parameters fixed a priori, never tuned here",
        "honesty": "Six rules tested at once — expect the best backtest to flatter itself "
                   "(selection effect). Nothing here is tradeable until it also survives the "
                   "Strategy Lab deflation + PBO gate AND its forward record.",
        "backtest": backtest,
        "forward": {"open": sorted(still_open, key=lambda p: p["strategy"]),
                    "stats": fwd_stats,
                    "closed_total": len(fwd_trades),
                    "closed_recent": fwd_trades[-25:][::-1]},
    }
    json.dump(out, open(os.path.join(REPORTS, "arena.json"), "w"))
    print(f"OK arena: backtest " +
          ", ".join(f"{k}:{backtest[k]['n']}" for k in STRATS) +
          f" · forward open {len(still_open)}, closed {len(fwd_trades)}")


if __name__ == "__main__":
    main()
