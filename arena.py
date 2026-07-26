#!/usr/bin/env python3
"""Paper Arena — the agents actually take trades (paper) and learn their own
rhythm by market condition.

Eight fixed rules (registered in REGISTRY.md 2026-07-25 with theses — never
tuned after registration) run two ways over the Stock Radar universe:

  1. BACKTEST: full 1y replay, every trade kept with dates + regime tag.
  2. FORWARD:  every daily refresh opens/closes live paper positions and logs
     them to reports/arena_trades.csv — the record that counts.

Every trade is tagged with the REGIME at entry:
  calm/storm  = VIX below / at-or-above 20
  up/down     = SPY above / below its 50-day MA
so each agent accumulates a per-condition record ("my rhythm") and writes a
first-person journal entry from its own numbers — no invented narrative.

Conventions (identical both modes): entry/exit at signal close · 10 bps per
side · one open position per ticker per rule · max 25 concurrent per rule in
forward mode · every trade benchmarked vs SPY over the identical window.

Run: /opt/anaconda3/bin/python arena.py            (after stock-radar collector)
"""
import csv, json, math, os
from datetime import date, timedelta

HOME = os.path.expanduser("~")
LAB = os.path.join(HOME, "strategy-lab")
RADAR = os.path.join(HOME, "stock-radar", "data", "radar.json")
REPORTS = os.path.join(LAB, "reports")
STATE_F = os.path.join(REPORTS, "arena_state.json")
TRADES_F = os.path.join(REPORTS, "arena_trades.csv")
COST = 0.001
MAX_OPEN = 25

STRATS = {
    "DEEP_DIP":     {"hold": 10, "side": 1,  "desc": "fresh −40% off 52w high → buy 10d",
                     "voice": "the bargain hunter"},
    "PANIC_BOUNCE": {"hold": 2,  "side": 1,  "desc": "1d ≤ −5% → buy 2d",
                     "voice": "the flush fader"},
    "PANIC_LITE":   {"hold": 2,  "side": 1,  "desc": "1d ≤ −3% → buy 2d",
                     "voice": "the busy fader"},
    "DOUBLE_DIP":   {"hold": 3,  "side": 1,  "desc": "2 down days ≤ −6% total → buy 3d",
                     "voice": "the washout buyer"},
    "STORM_DIP":    {"hold": 3,  "side": 1,  "desc": "1d ≤ −4% in VIX ≥ 20 tape → buy 3d",
                     "voice": "the storm chaser"},
    "FRESH_HIGH":   {"hold": 10, "side": 1,  "desc": "new 52w high → buy 10d",
                     "voice": "the momentum rider"},
    "SHORT_EXT":    {"hold": 5,  "side": -1, "desc": "new high & ≥2× 52w low → short 5d",
                     "voice": "the skeptic"},
    "TREND_RIDER":  {"hold": 15, "side": 1,  "desc": "cross above 50MA, above 200MA → buy 15d",
                     "voice": "the trend follower"},
}
DAY0 = date(1970, 1, 1)


def d2iso(epoch_day):
    return (DAY0 + timedelta(days=int(epoch_day))).isoformat()


def signals_at(c, i, storm):
    """Strategies triggering on bar i of close series c (needs i ≥ 51).
    `storm` = VIX ≥ 20 on that bar's date."""
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
    if r1 <= -0.03:
        out.append("PANIC_LITE")
    if r1 < 0 and r_prev < 0 and (c[i] / c[i - 2] - 1) <= -0.06:
        out.append("DOUBLE_DIP")
    if r1 <= -0.04 and storm:
        out.append("STORM_DIP")
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
    return side * (exit_ / entry - 1) - 2 * COST


def stats(trades):
    if not trades:
        return {"n": 0}
    rs = [t["net"] for t in trades]
    ex = [t["excess"] for t in trades if t.get("excess") is not None]
    n = len(rs); mean = sum(rs) / n
    sd = math.sqrt(sum((r - mean) ** 2 for r in rs) / n) if n > 1 else 0
    t = mean / (sd / math.sqrt(n)) if sd > 0 else 0
    return {"n": n, "avg_bps": round(mean * 1e4, 1),
            "hit_pct": round(100 * sum(1 for r in rs if r > 0) / n, 1),
            "avg_excess_bps": round(sum(ex) / len(ex) * 1e4, 1) if ex else None,
            "t_stat": round(t, 2), "total_pct": round(sum(rs) * 100, 1)}


def verdict(s):
    if s["n"] < 10:
        return "too few trades"
    if s["avg_bps"] <= 0 or (s["avg_excess_bps"] or -1) <= 0:
        return "DEAD — loses to costs/SPY"
    if s["t_stat"] >= 2:
        return "CANDIDATE — send to the deflation gate"
    return "WATCH — positive but not significant"


def journal(name, cfg, st, by_regime, open_n, fwd, closed_recent):
    """First-person agent note, strictly from the numbers."""
    L = [f"I'm {name} — {cfg['voice']}. My rule: {cfg['desc']}, "
         f"{'short' if cfg['side'] < 0 else 'long'} side, no discretion allowed."]
    if st.get("n"):
        L.append(f"This past year I took {st['n']} trades: {st['avg_bps']:+.0f} bps per trade "
                 f"({st['avg_excess_bps']:+.0f} vs SPY), hit rate {st['hit_pct']:.0f}%, "
                 f"t-stat {st['t_stat']}. Verdict on me so far: {verdict(st)}.")
    regs = {k: v for k, v in by_regime.items() if v.get("n", 0) >= 8}
    if len(regs) >= 2:
        best = max(regs, key=lambda k: regs[k]["avg_bps"])
        worst = min(regs, key=lambda k: regs[k]["avg_bps"])
        if best != worst:
            L.append(f"My rhythm: I do my best work in {best} tape "
                     f"({regs[best]['avg_bps']:+.0f} bps over {regs[best]['n']} trades) and "
                     f"I bleed in {worst} ({regs[worst]['avg_bps']:+.0f} bps over "
                     f"{regs[worst]['n']}). Watch me in the current regime accordingly.")
    if fwd.get("n"):
        L.append(f"Forward (the exam that counts): {fwd['n']} closed at {fwd['avg_bps']:+.0f} bps"
                 + (f", last exits: " + ", ".join(
                     f"{r['ticker']} {float(r['net'])*100:+.1f}%" for r in closed_recent[:3])
                    if closed_recent else "") + ".")
    else:
        L.append(f"Forward book: {open_n} positions open, nothing closed yet — "
                 "judge me only on what gets scored.")
    return " ".join(L)


def main():
    radar = json.load(open(RADAR))
    strip = {s["ticker"]: s for s in radar["strip"]}
    spy = strip.get("SPY"); vix = strip.get("VIX")
    spy_by_day = dict(zip(spy["series_t"], spy["series_c"])) if spy else {}
    spy_days = sorted(spy_by_day)

    # regime lookup: for any epoch day, last-known VIX level + SPY vs 50d MA
    vix_by_day = dict(zip(vix["series_t"], vix["series_c"])) if vix else {}
    vix_days = sorted(vix_by_day)
    spy_ma = {}
    sc = spy["series_c"]; st_ = spy["series_t"]
    for i in range(len(sc)):
        spy_ma[st_[i]] = sc[i] > sum(sc[max(0, i - 49):i + 1]) / min(50, i + 1)

    def regime(day):
        pv = [d for d in vix_days if d <= day]
        pu = [d for d in spy_days if d <= day]
        if not pv or not pu:
            return "unknown", False
        storm = vix_by_day[pv[-1]] >= 20
        up = spy_ma.get(pu[-1], True)
        return ("storm" if storm else "calm") + "-" + ("up" if up else "down"), storm

    def spy_ret(d_in, d_out):
        a, b = spy_by_day.get(d_in), spy_by_day.get(d_out)
        if a is None or b is None:
            pa = [d for d in spy_days if d <= d_in]
            pb = [d for d in spy_days if d <= d_out]
            if not pa or not pb or pa[-1] == pb[-1]:
                return None
            a, b = spy_by_day[pa[-1]], spy_by_day[pb[-1]]
        return b / a - 1

    eq = [e for e in radar["equities"] if len(e.get("series_c", [])) > 60]

    # ---------------- 1 · backtest: full replay, every trade kept -------------
    bt = {k: [] for k in STRATS}
    for e in eq:
        c, tdays = e["series_c"], e["series_t"]
        open_until = {k: -1 for k in STRATS}
        for i in range(51, len(c)):
            reg, storm = regime(tdays[i])
            for s in signals_at(c, i, storm):
                cfg = STRATS[s]
                if i <= open_until[s]:
                    continue
                j = min(i + cfg["hold"], len(c) - 1)
                if j <= i:
                    continue
                nr = net_ret(c[i], c[j], cfg["side"])
                sp = spy_ret(tdays[i], tdays[j])
                bt[s].append({"ticker": e["ticker"], "net": nr,
                              "excess": nr - sp if sp is not None else None,
                              "entry_date": d2iso(tdays[i]), "exit_date": d2iso(tdays[j]),
                              "regime": reg})
                open_until[s] = j

    backtest = {}
    for k, trades in bt.items():
        by_reg = {}
        for r in ("calm-up", "calm-down", "storm-up", "storm-down"):
            by_reg[r] = stats([t for t in trades if t["regime"] == r])
        cum, eqc = 0.0, []
        for idx, t in enumerate(sorted(trades, key=lambda t: t["exit_date"])):
            cum += t["net"]
            eqc.append(round(cum * 100, 2))
        step = max(1, len(eqc) // 100)
        backtest[k] = {**stats(trades), "desc": STRATS[k]["desc"],
                       "side": "SHORT" if STRATS[k]["side"] < 0 else "LONG",
                       "by_regime": by_reg, "equity": eqc[::step]}
        backtest[k]["verdict"] = verdict(backtest[k]) if backtest[k]["n"] else "no trades"

    # ---------------- 2 · forward paper book ----------------------------------
    state = {"open": []}
    if os.path.exists(STATE_F):
        state = json.load(open(STATE_F))
    px = {e["ticker"]: dict(zip(e["series_t"], e["series_c"])) for e in eq}
    today = date.today().isoformat()

    closed_now, still_open = [], []
    for p in state["open"]:
        tk = p["ticker"]
        days = sorted(px.get(tk, {}))
        if not days:
            still_open.append(p); continue
        elapsed = sum(1 for d in days if d > p["entry_t"])
        cur = px[tk][days[-1]]
        if elapsed >= p["hold"]:
            nr = net_ret(p["entry_px"], cur, p["side"])
            sp = spy_ret(p["entry_t"], days[-1])
            closed_now.append({**p, "exit_date": d2iso(days[-1]), "exit_px": cur,
                               "net": round(nr, 5),
                               "excess": round(nr - sp, 5) if sp is not None else "",
                               "regime": p.get("regime", "unknown")})
        else:
            p["mtm"] = round(p["side"] * (cur / p["entry_px"] - 1) - 2 * COST, 5)
            p["days_left"] = p["hold"] - elapsed
            still_open.append(p)

    held = {(p["strategy"], p["ticker"]) for p in still_open}
    count = {k: sum(1 for p in still_open if p["strategy"] == k) for k in STRATS}
    for e in eq:
        c = e["series_c"]; i = len(c) - 1
        if i < 51:
            continue
        reg, storm = regime(e["series_t"][i])
        for s in signals_at(c, i, storm):
            if (s, e["ticker"]) in held or count.get(s, 0) >= MAX_OPEN:
                continue
            cfg = STRATS[s]
            still_open.append({"strategy": s, "ticker": e["ticker"],
                               "side": cfg["side"], "hold": cfg["hold"],
                               "entry_date": today, "entry_t": e["series_t"][i],
                               "entry_px": c[i], "mtm": 0.0,
                               "days_left": cfg["hold"], "regime": reg})
            held.add((s, e["ticker"])); count[s] = count.get(s, 0) + 1

    os.makedirs(REPORTS, exist_ok=True)
    json.dump({"open": still_open}, open(STATE_F, "w"), indent=1)
    cols = ["strategy", "ticker", "side", "entry_date", "entry_px",
            "exit_date", "exit_px", "net", "excess", "regime"]
    old = list(csv.DictReader(open(TRADES_F))) if os.path.exists(TRADES_F) else []
    with open(TRADES_F, "w") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in old + closed_now:
            w.writerow({c: r.get(c, "") for c in cols})

    fwd_trades = list(csv.DictReader(open(TRADES_F)))
    fwd_stats, journals = {}, {}
    for k, cfg in STRATS.items():
        rows = [{"net": float(r["net"]),
                 "excess": float(r["excess"]) if r["excess"] else None}
                for r in fwd_trades if r["strategy"] == k]
        fwd_stats[k] = stats(rows)
        recent = [r for r in fwd_trades if r["strategy"] == k][::-1]
        journals[k] = journal(k, cfg, backtest.get(k, {}), backtest[k]["by_regime"],
                              count.get(k, 0), fwd_stats[k], recent)

    cur_reg, _ = regime(spy["series_t"][-1])
    out = {
        "updated": radar.get("updated", ""),
        "universe": len(eq),
        "current_regime": cur_reg,
        "max_open": MAX_OPEN,
        "conventions": "entry/exit at signal close · 10 bps/side · vs-SPY benchmark · "
                       "regime tags: calm/storm = VIX </≥ 20, up/down = SPY vs 50d MA · "
                       "8 rules registered in REGISTRY.md, parameters frozen",
        "honesty": "Eight rules tested at once — the best backtest flatters itself. Only "
                   "the forward record + the Strategy Lab deflation gate promote a rule.",
        "backtest": backtest,
        "journals": journals,
        "blotter_backtest": sorted((t for v in bt.values() for t in v),
                                   key=lambda t: t["exit_date"], reverse=True),
        "forward": {"open": sorted(still_open, key=lambda p: p["strategy"]),
                    "stats": fwd_stats,
                    "closed_total": len(fwd_trades),
                    "closed_all": fwd_trades[::-1]},
    }
    # keep blotter payload sane for the browser
    for t in out["blotter_backtest"]:
        t["net"] = round(t["net"], 5)
        if t["excess"] is not None:
            t["excess"] = round(t["excess"], 5)
    json.dump(out, open(os.path.join(REPORTS, "arena.json"), "w"))
    print("OK arena: backtest " + ", ".join(f"{k}:{backtest[k]['n']}" for k in STRATS)
          + f" · forward open {len(still_open)}, closed {len(fwd_trades)} · regime {cur_reg}")


if __name__ == "__main__":
    main()
