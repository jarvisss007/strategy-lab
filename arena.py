#!/usr/bin/env python3
"""Paper Arena — the agents actually take trades (paper) and learn their own
rhythm by market condition.

Twelve fixed rules (registered in REGISTRY.md 2026-07-25 with theses — never
tuned after registration; the 4-rule tempo tier added the same day, registered
before first run) run two ways over the Stock Radar universe:

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

Date semantics — dates are bar dates, not run dates (corrected 2026-08-06):
entry_date/exit_date are the date of the completed session whose close the row
is priced at, never the wall-clock date the refresh happened to run. Regime
tags are looked up on that same bar date, and the roundtable's opened/closed
counters refer to the latest completed session. Before 2026-08-06 forward
entries were stamped with the run date (one session late vs their price);
existing rows were migrated by matching each row's price to the dated bar
series.

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
MAX_OPEN = 40      # raised 25→40 on 2026-07-25 (tempo sign-off in REGISTRY.md)

# TAG-001, 2026-08-11. Every rule declares its own [tech]/[fund] tag HERE, at the
# lab's end. Until now the Calibration Observatory inferred the Arena's tag from a
# regex over a thesis string that calibration.py::read_arena BUILT ITSELF, so the
# Arena could not have declared even if it wanted to — 622 rows, 73% of the whole
# census, carried a downstream guess. The guess happened to be right, which is
# exactly why it went unnoticed for a month.
#
# `tech` here is a statement of fact, not a classification call: every trigger below
# is a price or volatility condition — 52-week highs and lows, daily percentage
# moves, moving averages, RSI(2), Bollinger bands, a VIX regime gate. Not one reads
# a financial statement. A future rule that does must set its own tag on this line;
# that is the whole point of putting it here rather than in a shared default.
STRATS = {
    "DEEP_DIP":     {"hold": 10, "side": 1, "tags": "tech",  "desc": "fresh −40% off 52w high → buy 10d",
                     "voice": "the bargain hunter"},
    "PANIC_BOUNCE": {"hold": 2,  "side": 1, "tags": "tech",  "desc": "1d ≤ −5% → buy 2d",
                     "voice": "the flush fader"},
    "PANIC_LITE":   {"hold": 2,  "side": 1, "tags": "tech",  "desc": "1d ≤ −3% → buy 2d",
                     "voice": "the busy fader"},
    "DOUBLE_DIP":   {"hold": 3,  "side": 1, "tags": "tech",  "desc": "2 down days ≤ −6% total → buy 3d",
                     "voice": "the washout buyer"},
    "STORM_DIP":    {"hold": 3,  "side": 1, "tags": "tech",  "desc": "1d ≤ −4% in VIX ≥ 20 tape → buy 3d",
                     "voice": "the storm chaser"},
    "FRESH_HIGH":   {"hold": 10, "side": 1, "tags": "tech",  "desc": "new 52w high → buy 10d",
                     "voice": "the momentum rider"},
    "SHORT_EXT":    {"hold": 5,  "side": -1, "tags": "tech", "desc": "new high & ≥2× 52w low → short 5d",
                     "voice": "the skeptic"},
    "TREND_RIDER":  {"hold": 15, "side": 1, "tags": "tech",  "desc": "cross above 50MA, above 200MA → buy 15d",
                     "voice": "the trend follower"},
    # tempo tier — registered 2026-07-25 PM (REGISTRY.md), higher signal frequency
    "RSI2_DIP":     {"hold": 3,  "side": 1, "tags": "tech",  "desc": "RSI(2) < 10 above 200MA → buy 3d",
                     "voice": "the twitchy scalper"},
    "REVERSAL_3":   {"hold": 2,  "side": 1, "tags": "tech",  "desc": "3 straight down closes above 200MA → buy 2d",
                     "voice": "the three-day contrarian"},
    "BOLL_SNAP":    {"hold": 3,  "side": 1, "tags": "tech",  "desc": "close < 20d MA − 2σ → buy 3d",
                     "voice": "the rubber-band trader"},
    "PULLBACK_50":  {"hold": 5,  "side": 1, "tags": "tech",  "desc": "uptrend, first close below 20d MA → buy 5d",
                     "voice": "the dip-in-trend buyer"},
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
    ma20 = sum(c[i - 19:i + 1]) / 20
    sd20 = math.sqrt(sum((x - ma20) ** 2 for x in c[i - 19:i + 1]) / 20)
    if c[i] < ma20 - 2 * sd20:
        out.append("BOLL_SNAP")
    if i >= 200:
        ma50 = sum(c[i - 49:i + 1]) / 50
        ma50p = sum(c[i - 50:i]) / 50
        ma200 = sum(c[i - 199:i + 1]) / 200
        if c[i] > ma50 and c[i - 1] <= ma50p and c[i] > ma200:
            out.append("TREND_RIDER")
        if c[i] > ma200:
            d1 = c[i] - c[i - 1]; d2 = c[i - 1] - c[i - 2]
            g = (max(d1, 0) + max(d2, 0)) / 2
            l = (max(-d1, 0) + max(-d2, 0)) / 2
            rsi2 = 100.0 if l == 0 else 100 - 100 / (1 + g / l)
            if rsi2 < 10:
                out.append("RSI2_DIP")
            if c[i] < c[i - 1] < c[i - 2] < c[i - 3]:
                out.append("REVERSAL_3")
            ma20p = sum(c[i - 20:i]) / 20
            if c[i] < ma20 and c[i - 1] >= ma20p:
                out.append("PULLBACK_50")
    return out


def net_ret(entry, exit_, side):
    return side * (exit_ / entry - 1) - 2 * COST


# CLUSTER-001, 2026-08-27. `n` counts TRADES; inference needs EVENTS. On 2026-07-29
# a single flush opened all 40 of STORM_DIP's forward positions at once, and three
# sessions later the V-bottom paid every one of them: n=40, t=4.8, +830 bps vs SPY.
# Read as 40 observations that is overwhelming; it is ONE observation of one tape,
# taken 40 ways. The same day carries 87% of the whole forward book's summed P&L,
# and the book's vs-SPY mean flips from +68 bps (t=+3.3) to -58 bps (t=-2.8) when
# the 07-28..07-31 window is dropped. Nothing in the Arena said so: STORM_DIP's own
# journal called n=40 a "small sample", which is the right instinct attached to the
# wrong number.
#
# So every stat block now carries `n_events` (distinct entry dates) beside `n`, and
# `t_clustered` — the t-stat on the per-event MEAN, which is the coarsest honest
# unit when trades that share an entry date share a shock. It is deliberately the
# conservative reading: events inside one drawdown are themselves correlated, so
# t_clustered is an upper bound on significance, never a floor. `None` when a rule
# has fired on one date only, because one event supports no inference at all — and
# a missing number a reader must notice beats a number that flatters.
#
# t_stat is unchanged and still reported: this ADDS the honest denominator, it does
# not restate a published figure (BENCH-002).
def stats(trades):
    if not trades:
        return {"n": 0}
    rs = [t["net"] for t in trades]
    ex = [t["excess"] for t in trades
          if isinstance(t.get("excess"), (int, float))]
    n = len(rs); mean = sum(rs) / n
    sd = math.sqrt(sum((r - mean) ** 2 for r in rs) / n) if n > 1 else 0
    t = mean / (sd / math.sqrt(n)) if sd > 0 else 0
    ev = {}
    for tr in trades:
        day = tr.get("entry_date")
        if day:
            ev.setdefault(day, []).append(tr["net"])
    k = len(ev)
    tc = None
    if k > 1:
        em = [sum(v) / len(v) for v in ev.values()]
        m2 = sum(em) / k
        s2 = math.sqrt(sum((x - m2) ** 2 for x in em) / (k - 1))
        if s2 > 0:
            tc = round(m2 / (s2 / math.sqrt(k)), 2)
    return {"n": n, "avg_bps": round(mean * 1e4, 1),
            "hit_pct": round(100 * sum(1 for r in rs if r > 0) / n, 1),
            "avg_excess_bps": round(sum(ex) / len(ex) * 1e4, 1) if ex else None,
            "t_stat": round(t, 2), "total_pct": round(sum(rs) * 100, 1),
            "n_events": k, "t_clustered": tc}


# The gate was RUN on 2026-08-08 (arena_gate.py) and the whole slate failed it:
# DSR 0.233 against a best-of-12 benchmark of 2.18 ann. Sharpe, PBO 0.474, IS→OOS slope
# −0.568, and 198 sessions against the 1.5 YEARS this many trials requires. So no rule
# may wear the word CANDIDATE any more — "send to the gate" was a promise that has now
# been kept, and the answer was no. Verdicts below carry the gate's result, not the
# per-trade t-stat's opinion. Re-run arena_gate.py after any material data growth and
# update GATE_VERDICT here; never soften this string because a rule looks good again.
GATE_VERDICT = "FAILED the deflation gate 2026-08-08 (DSR 0.233, PBO 0.474)"


def verdict(s):
    if s["n"] < 10:
        return "too few trades"
    if s["avg_bps"] <= 0 or (s["avg_excess_bps"] or -1) <= 0:
        return "DEAD — loses to costs/SPY"
    if s["t_stat"] >= 2:
        return f"UNPROVEN — {GATE_VERDICT}"
    return "WATCH — positive but not significant"


def journal(name, cfg, st, by_regime, open_n, fwd, closed_recent, live=None):
    """First-person agent note, strictly from the numbers."""
    L = [f"I'm {name} — {cfg['voice']}. My rule: {cfg['desc']}, "
         f"{'short' if cfg['side'] < 0 else 'long'} side, no discretion allowed."]
    if st.get("n"):
        L.append(f"This past year I took {st['n']} trades on {st.get('n_events', 0)} separate "
                 f"days: {st['avg_bps']:+.0f} bps per trade "
                 f"({st['avg_excess_bps']:+.0f} vs SPY), hit rate {st['hit_pct']:.0f}%, "
                 f"t-stat {st['t_stat']}"
                 + (f" — but {st['t_clustered']} once same-day trades are counted as the one "
                    f"event they are" if st.get("t_clustered") is not None else "")
                 + f". Verdict on me so far: {verdict(st)}.")
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
                 + (f" — but off only {fwd['n_events']} entry day"
                    + ("s" if fwd["n_events"] != 1 else "")
                    + (", so there is one event here and no inference to draw from it"
                       if fwd["n_events"] == 1
                       else f", clustered t {fwd['t_clustered']}"
                            if fwd.get("t_clustered") is not None else "")
                    if fwd.get("n_events") else "")
                 + (f", last exits: " + ", ".join(
                     f"{r['ticker']} {float(r['net'])*100:+.1f}%" for r in closed_recent[:3])
                    if closed_recent else "") + ".")
    else:
        L.append(f"Forward book: {open_n} positions open, nothing closed yet — "
                 "judge me only on what gets scored.")

    live = live or {}
    # what I actually did this refresh
    od, cd = live.get("opened_today") or [], live.get("closed_today") or []
    if od or cd:
        parts = []
        if od:
            parts.append("opened " + ", ".join(od[:6]) + ("…" if len(od) > 6 else ""))
        if cd:
            parts.append("closed " + ", ".join(
                f"{t['ticker']} {t['net'] * 100:+.1f}%" for t in cd[:4]))
        L.append("Today I " + " and ".join(parts) + ".")
    # where I'm struggling right now
    w = live.get("worst_open")
    if w and w.get("mtm", 0) <= -0.03:
        L.append(f"My sore spot: {w['ticker']} is {w['mtm'] * 100:+.1f}% against me with "
                 f"{w.get('days_left', '?')} sessions left — logged, not excused.")
    if live.get("losing_streak", 0) >= 3:
        L.append(f"I'm {live['losing_streak']} forward losses deep in a streak. "
                 "The rule doesn't change; the record just gets uglier honestly.")
    # early forward rhythm, once any regime has 5 scored closes
    fr = {r: v for r, v in (live.get("fwd_by_regime") or {}).items()
          if v.get("n", 0) >= 5 and r != "unknown"}
    if fr:
        b = max(fr, key=lambda r: fr[r]["avg_bps"])
        L.append(f"Forward rhythm forming: my real closes cluster best in {b} "
                 f"({fr[b]['avg_bps']:+.0f} bps, n={fr[b]['n']} trades over "
                 f"{fr[b].get('n_events', 0)} entry day"
                 + ("s" if fr[b].get("n_events") != 1 else "")
                 + ") — "
                 + ("that is ONE event dressed as a sample; hold me to nothing yet."
                    if fr[b].get("n_events") == 1
                    else "small sample, hold me to it."))
    # what I took from the last roundtable (awareness only; rules stay frozen)
    pb = live.get("prior_playbook") or []
    peers = [p for p in pb if p["agent"] != name]
    if peers:
        p0 = peers[0]
        mine = next((p for p in pb if p["agent"] == name), None)
        L.append(f"From the roundtable: {p0['agent']} owns this {live.get('cur_reg', '?')} tape "
                 f"({p0['avg_bps']:+.0f} bps, n={p0['n']})"
                 + (f"; my own mark here is {mine['avg_bps']:+.0f}" if mine else "")
                 + ". My rule stays frozen — but now I know whose weather this is.")
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
                bt[s].append({"strategy": s, "ticker": e["ticker"], "net": nr,
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
    for p in state["open"]:          # backfill regime for pre-tagging entries
        if not p.get("regime") or p["regime"] == "unknown":
            p["regime"] = regime(p["entry_t"])[0]
    px = {e["ticker"]: dict(zip(e["series_t"], e["series_c"])) for e in eq}
    today = date.today().isoformat()

    # Fill-integrity gate: the registered convention is entry/exit AT THE CLOSE.
    # A refresh during RTH sees a partial bar (e.g. BE 2026-07-25: −15% intraday
    # print, fully recovered by the close), so intraday runs only mark to market
    # — no opens, no closes. Post-close and weekend runs trade normally.
    import datetime as _dt
    try:
        from zoneinfo import ZoneInfo
        now_pt = _dt.datetime.now(ZoneInfo("America/Los_Angeles"))
    except Exception:
        now_pt = _dt.datetime.now()
    intraday = now_pt.weekday() < 5 and (6, 30) <= (now_pt.hour, now_pt.minute) < (13, 5)

    closed_now, still_open = [], []
    for p in state["open"]:
        tk = p["ticker"]
        days = sorted(px.get(tk, {}))
        if not days:
            still_open.append(p); continue
        elapsed = sum(1 for d in days if d > p["entry_t"])
        cur = px[tk][days[-1]]
        if elapsed >= p["hold"] and not intraday:
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
    # STALE-BAR GATE (DATA-002, ruled 2026-08-15). The Arena opens at c[len(c)-1],
    # the freshest and therefore least-settled bar in the feed, so a collector that
    # re-serves one cached value writes a permanent row at a price that never
    # traded — QBTS sat at 16.21, its 07-24 close, on entries dated 08-04, 08-11
    # and 08-13. Three identical consecutive closes is the signature of that stall
    # and, measured over the actual feed, of nothing else: across 147 tickers and
    # ~251 bars each (~36,900 bars) there are 90 runs of exactly two and ZERO runs
    # of three or more, ever. So this refuses only what is provably frozen and has
    # never once fired on real data.
    #
    # It gates ENTRIES only, never exits — refusing to close a position because its
    # feed looks odd would strand it, which is a worse failure than a wrong mark.
    # Same class as the intraday fill-integrity gate above: a data-integrity
    # refusal, not a strategy gate. It selects on whether the price is real, never
    # on whether the trade looks good, so it needs no REGISTRY thesis.
    def frozen(c):
        return len(c) >= 3 and c[-1] == c[-2] == c[-3]

    skipped_frozen = []
    for e in (eq if not intraday else []):
        c = e["series_c"]; i = len(c) - 1
        if i < 51:
            continue
        if frozen(c):
            skipped_frozen.append(e["ticker"])
            continue
        reg, storm = regime(e["series_t"][i])
        for s in signals_at(c, i, storm):
            if (s, e["ticker"]) in held or count.get(s, 0) >= MAX_OPEN:
                continue
            cfg = STRATS[s]
            still_open.append({"strategy": s, "ticker": e["ticker"],
                               "side": cfg["side"], "hold": cfg["hold"],
                               "entry_date": d2iso(e["series_t"][i]),   # bar date, not run date
                               "entry_t": e["series_t"][i],
                               "entry_px": c[i], "mtm": 0.0,
                               "days_left": cfg["hold"], "regime": reg})
            held.add((s, e["ticker"])); count[s] = count.get(s, 0) + 1

    os.makedirs(REPORTS, exist_ok=True)
    json.dump({"open": still_open}, open(STATE_F, "w"), indent=1)
    # The *_tape columns carry what the tape says a row's prices should have been,
    # beside the numbers it was actually scored on. BENCH-002 (ruled 2026-08-12):
    # a closed row keeps the number it was scored with, and a correction may be
    # ADDED as a new column but never overwritten. They must be listed here or the
    # DictWriter below drops them silently on the next run — a rewrite that erases
    # a correction is worse than never having recorded one.
    cols = ["strategy", "ticker", "side", "entry_date", "entry_px",
            "exit_date", "exit_px", "net", "excess", "regime", "tags",
            "entry_px_tape", "exit_px_tape", "net_tape", "excess_tape"]
    old = list(csv.DictReader(open(TRADES_F))) if os.path.exists(TRADES_F) else []
    with open(TRADES_F, "w") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in old + closed_now:
            row = {c: r.get(c, "") for c in cols}
            # Declared from the rule's own definition, never from the row. The tag is a
            # property of the STRATEGY, so it is deterministic and carries no knowledge
            # of how the trade turned out.
            row["tags"] = STRATS.get(r.get("strategy"), {}).get("tags", "")
            w.writerow(row)

    cur_reg, _ = regime(spy["series_t"][-1])

    # last run's roundtable — the shared report each agent reads before speaking
    prior_rt = {}
    arena_f = os.path.join(REPORTS, "arena.json")
    if os.path.exists(arena_f):
        try:
            prior_rt = json.load(open(arena_f)).get("roundtable", {})
        except Exception:
            prior_rt = {}

    # latest completed session (bar date) — counters key off this, not the
    # wall-clock run date (date-semantics fix 2026-08-06)
    last_session = d2iso(spy["series_t"][-1])
    if intraday and last_session == today:      # partial same-day bar during RTH
        prior = [t for t in spy["series_t"] if d2iso(t) < today]
        if prior:
            last_session = d2iso(prior[-1])

    fwd_trades = list(csv.DictReader(open(TRADES_F)))

    opened_today_by, closed_today_by = {}, {}
    for p in still_open:
        if p["entry_date"] == last_session:
            opened_today_by.setdefault(p["strategy"], []).append(p["ticker"])
    for r in fwd_trades:
        if r["exit_date"] == last_session:
            closed_today_by.setdefault(r["strategy"], []).append(
                {"ticker": r["ticker"], "net": float(r["net"])})
    fwd_stats, fwd_rhythm, journals = {}, {}, {}
    for k, cfg in STRATS.items():
        # entry_date is carried, not dropped: stats() needs it to count EVENTS
        # (CLUSTER-001). Without it the forward book reports n_events 0 and every
        # clustered t-stat comes back null — the exact silence this was built to end.
        rows = [{"net": float(r["net"]),
                 "excess": float(r["excess"]) if r["excess"] else None,
                 "entry_date": r["entry_date"]}
                for r in fwd_trades if r["strategy"] == k]
        fwd_stats[k] = stats(rows)
        by_reg_rows = {}
        for r in fwd_trades:
            if r["strategy"] == k:
                by_reg_rows.setdefault(r.get("regime") or "unknown", []).append(
                    {"net": float(r["net"]),
                     "excess": float(r["excess"]) if r["excess"] else None,
                     "entry_date": r["entry_date"]})
        fwd_rhythm[k] = {rr: stats(v) for rr, v in by_reg_rows.items()}
        recent = [r for r in fwd_trades if r["strategy"] == k][::-1]
        streak = 0
        for r in recent:
            if float(r["net"]) < 0:
                streak += 1
            else:
                break
        opens_k = [p for p in still_open if p["strategy"] == k and "mtm" in p]
        journals[k] = journal(
            k, cfg, backtest.get(k, {}), backtest[k]["by_regime"],
            count.get(k, 0), fwd_stats[k], recent,
            live={"opened_today": opened_today_by.get(k),
                  "closed_today": closed_today_by.get(k),
                  "worst_open": min(opens_k, key=lambda p: p["mtm"]) if opens_k else None,
                  "losing_streak": streak,
                  "fwd_by_regime": fwd_rhythm[k],
                  "prior_playbook": (prior_rt.get("playbook") or {}).get(cur_reg),
                  "cur_reg": cur_reg})

    # ---------------- 3 · the Roundtable: one desk, shared lessons ------------
    # Every agent's experience pooled into a single report the others (and the
    # human) read: who owns which regime, who overlaps whom, what the marginal
    # band is worth. All computed, nothing invented.
    entries = {k: {(t["ticker"], t["entry_date"]) for t in bt[k]} for k in STRATS}
    overlaps = []
    keys = list(STRATS)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if not entries[a] or not entries[b]:
                continue
            inter = len(entries[a] & entries[b])
            share = inter / min(len(entries[a]), len(entries[b]))
            if share >= 0.25 and inter >= 20:
                overlaps.append({"a": a, "b": b, "n": inter,
                                 "share_pct": round(100 * share)})
    overlaps.sort(key=lambda o: -o["share_pct"])

    band = entries["PANIC_LITE"] - entries["PANIC_BOUNCE"]
    band_trades = [t for t in bt["PANIC_LITE"] if (t["ticker"], t["entry_date"]) in band]
    marginal = {**stats(band_trades),
                "desc": "the −3%…−5% band alone (PANIC_LITE entries too shallow "
                        "for PANIC_BOUNCE)"} if band_trades else None

    playbook = {}
    for r in ("calm-up", "calm-down", "storm-up", "storm-down"):
        rank = [(k, backtest[k]["by_regime"][r]) for k in STRATS
                if backtest[k]["by_regime"][r].get("n", 0) >= 20]
        rank.sort(key=lambda kv: -kv[1]["avg_bps"])
        playbook[r] = [{"agent": k, "avg_bps": v["avg_bps"], "n": v["n"],
                        "hit_pct": v["hit_pct"]} for k, v in rank]

    notes = []
    for k in STRATS:
        regs = {r: v for r, v in backtest[k]["by_regime"].items() if v.get("n", 0) >= 8}
        if not regs:
            continue
        best = max(regs, key=lambda r: regs[r]["avg_bps"])
        worst = min(regs, key=lambda r: regs[r]["avg_bps"])
        notes.append(f"{k} to the desk: my weather is {best} "
                     f"({regs[best]['avg_bps']:+.0f} bps, n={regs[best]['n']}); keep me "
                     f"on a short leash in {worst} ({regs[worst]['avg_bps']:+.0f}). "
                     f"Status: {backtest[k]['verdict']}.")

    lines = []
    pb_now = playbook.get(cur_reg, [])
    if pb_now:
        top = ", ".join(f"{p['agent']} ({p['avg_bps']:+.0f})" for p in pb_now[:3])
        rest = pb_now[3:]
        cold = ", ".join(f"{p['agent']} ({p['avg_bps']:+.0f})" for p in rest[-2:])
        lines.append(f"Tape today: {cur_reg.upper()}. Our pooled record in this weather — "
                     f"hot hands: {top}"
                     + (f"; cold hands: {cold}" if cold else
                        "; the rest of us have too little history in this weather to speak")
                     + ". (History, not prophecy.)")
    fh_se = next((o for o in overlaps if {o['a'], o['b']} == {"FRESH_HIGH", "SHORT_EXT"}), None)
    if fh_se:
        lines.append(f"FRESH_HIGH and SHORT_EXT enter on the same bar {fh_se['share_pct']}% "
                     "of the time — one trade, two directions. The pooled ledger says the "
                     "long side wins that argument; the skeptic keeps paying for the lesson.")
    pl_pb = next((o for o in overlaps if {o['a'], o['b']} == {"PANIC_LITE", "PANIC_BOUNCE"}), None)
    if pl_pb and marginal and marginal.get("n"):
        lines.append(f"PANIC_LITE contains {pl_pb['share_pct']}% of PANIC_BOUNCE's entries; "
                     f"stripped to {marginal['desc']}, it still earned "
                     f"{marginal['avg_bps']:+.0f} bps over {marginal['n']} trades "
                     f"(t={marginal['t_stat']}) — the bounce is not only in the extreme tail.")
    lines.append("Desk rule we all share: reading each other's regime stats and gating "
                 "ourselves in hindsight is selection bias — STORM_DIP is the only "
                 "pre-registered regime gate; any new gate goes to REGISTRY.md with a "
                 "thesis BEFORE it trades.")
    tempo = {"session": last_session,
             "opened_today": sum(len(v) for v in opened_today_by.values()),
             "closed_today": sum(len(v) for v in closed_today_by.values()),
             "open_total": len(still_open),
             "closed_total": len(fwd_trades),
             "agents": len(STRATS)}
    roundtable = {"regime": cur_reg, "playbook": playbook, "overlaps": overlaps,
                  "marginal": marginal, "notes": notes, "lines": lines,
                  "tempo": tempo}

    # Council FIX (strategy-lab-arena directive, 2026-08-13): the Arena is the large
    # majority of the desk's scored rows, so ANY pooled Observatory number is mostly a
    # statement about this one lab. The council wrote that caveat every session; it
    # belongs at the source instead. Read the share from the Observatory's own output
    # rather than hardcoding it — a frozen "88%" goes stale the day after it is written.
    share = None
    try:
        with open(os.path.expanduser("~/command-center/calibration.js")) as cf:
            _c = json.loads(cf.read().split("=", 1)[1].strip().rstrip(";"))
        _tot = _c["pooled"]["scored"]
        _mine = next(l["scored"] for l in _c["labs"] if l["lab"] == "Paper Arena")
        if _tot:
            share = (_mine, _tot, round(100 * _mine / _tot))
    except Exception:
        share = None  # Observatory not built yet — say nothing rather than guess

    # single-place report for every agent (and human) to read
    with open(os.path.join(REPORTS, "arena_roundtable.md"), "w") as f:
        f.write(f"# Arena Roundtable — {today}\n\nTape: **{cur_reg}** · "
                f"session {tempo['session']} · {tempo['agents']} agents · "
                f"opened {tempo['opened_today']}, closed {tempo['closed_today']} "
                f"this session · {tempo['open_total']} open · "
                f"{tempo['closed_total']} forward closes all-time\n\n")
        if share:
            f.write(f"> **This lab is {share[2]}% of the desk's scored record "
                    f"({share[0]} of {share[1]} scored rows in the Calibration "
                    f"Observatory).** Any pooled desk statistic is therefore mostly a "
                    f"statement about the Arena, not about the desk. Read the other "
                    f"labs' standings on their own n.\n\n")
        # Council directive (strategy-lab-arena, 2026-08-19): ARENA-003 asks whether the
        # open book's due column actually drains, or whether rows sit on it forever. The
        # council was wrong about India Arena on 08-17 for exactly this reason — an open
        # book with a due column that nothing visibly empties LOOKS stuck whether or not
        # it is. So publish the mechanism every run rather than answering the question by
        # hand each time: how many rows are due, how many are actually past due, how many
        # closed this session, and the oldest due row on the book. Exits are suppressed
        # while `intraday` (fill integrity), so a due row during market hours is waiting
        # for the next non-intraday pass by design, not stuck.
        _due = [p for p in still_open if p.get("days_left", 99) <= 0]
        _past = [p for p in _due if p.get("days_left", 0) < 0]
        _oldest = min(_due, key=lambda p: p["entry_date"]) if _due else None
        f.write(f"**Drain (ARENA-003).** {len(_due)} of {len(still_open)} open rows read "
                f"`days_left <= 0`; {len(_past)} of those are PAST due (negative). "
                f"{tempo['closed_today']} closed this session, {tempo['closed_total']} "
                f"all-time. ")
        if _oldest:
            f.write(f"Oldest due row: {_oldest['strategy']} {_oldest['ticker']}, entered "
                    f"{_oldest['entry_date']}, hold {_oldest['hold']}, days_left "
                    f"{_oldest['days_left']}. ")
        else:
            f.write("No due rows on the book. ")
        f.write("Exits are suppressed during market hours by the fill-integrity gate, so a "
                "due row right now is waiting for the next non-intraday pass, not stuck.\n\n"
                if intraday else
                "This pass ran outside market hours, so every due row was eligible to "
                "close.\n\n")

        for ln in lines:
            f.write(f"- {ln}\n")
        f.write("\n## Playbook by regime (avg bps/trade, n>=20)\n\n")
        for r, ps in playbook.items():
            f.write(f"- **{r}**: " + " · ".join(
                f"{p['agent']} {p['avg_bps']:+.0f} (n={p['n']})" for p in ps) + "\n")
        # ARENA / council directive 2026-08-27: the coach's standing retirement test is
        # "arena reaching 15 ENTRY DAYS" for a strategy, and until now that number lived in
        # the coach's memory rather than on the page it reads. Surfaced per strategy, from
        # the forward book only (closed rows with a real entry_date), so the test has a
        # number to fire on. This publishes a count; it changes no bar, retires nothing, and
        # is not itself a gate.
        _ed = {}
        for _t in fwd_trades:
            _d = _t.get("entry_date")
            if _d:
                _ed.setdefault(_t["strategy"], set()).add(_d)
        if _ed:
            f.write("\n## Forward entry days per strategy (coach's 15-day retirement test)\n\n")
            f.write("Entry DAYS, not trades — same-day entries share one regime and are one "
                    "observation. The coach's standing test fires at 15.\n\n")
            for _k, _v in sorted(_ed.items(), key=lambda kv: -len(kv[1])):
                f.write(f"- {_k}: **{len(_v)}** entry days"
                        + (" — **test LIVE (>=15)**\n" if len(_v) >= 15 else "\n"))
        f.write("\n## Notes to the desk\n\n")
        for n_ in notes:
            f.write(f"- {n_}\n")
        f.write("\nCalibration experiment, not advice. Forward book + deflation gate "
                "decide; the replay only suggests.\n")

    out = {
        "roundtable": roundtable,
        "updated": radar.get("updated", ""),
        "universe": len(eq),
        "current_regime": cur_reg,
        "max_open": MAX_OPEN,
        "conventions": "entry/exit at signal close (intraday refreshes mark to market "
                       "only — no fills on partial bars) · 10 bps/side · vs-SPY benchmark · "
                       "regime tags: calm/storm = VIX </≥ 20, up/down = SPY vs 50d MA · "
                       f"{len(STRATS)} rules registered in REGISTRY.md, parameters frozen",
        # The forward book's two standing caveats, published on its own face rather
        # than left for a reader to discover: what the record is missing (ARENA-006)
        # and what it is really made of (CLUSTER-001). Both are permanent facts about
        # this book, so they belong beside its numbers, not in a register nobody opens.
        "honesty": f"{len(STRATS)} rules tested at once — the best backtest flatters "
                   "itself. Only the forward record + the Strategy Lab deflation gate "
                   "promote a rule. · Read n_events, not n: entry date 2026-07-29 alone "
                   "carries ~87% of this book's summed P&L, and its vs-SPY mean flips "
                   "from +68 bps (t=+3.3) to −58 bps (t=−2.8) when the 07-28..07-31 "
                   "window is dropped. · Two sessions are missing and cannot be "
                   "recovered — 2026-08-12 and 2026-08-25 had 60 and 45 signals and "
                   "the Arena entered nothing, because its only daily pass then landed "
                   "inside the intraday window where it must refuse to fill "
                   "(ARENA-006, scheduling fixed 2026-08-27).",
        "backtest": backtest,
        "journals": journals,
        "blotter_backtest": sorted((t for v in bt.values() for t in v),
                                   key=lambda t: t["exit_date"], reverse=True),
        "forward": {"open": sorted(still_open, key=lambda p: p["strategy"]),
                    "stats": fwd_stats,
                    "by_regime": fwd_rhythm,
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
          + f" · forward open {len(still_open)}, closed {len(fwd_trades)}"
          + f" · session {tempo['session']} +{tempo['opened_today']}/−{tempo['closed_today']}"
          + f" · regime {cur_reg}"
          # a refusal that prints nothing is a refusal nobody audits
          + (f" · SKIPPED {len(skipped_frozen)} frozen-bar name(s): "
             + ", ".join(sorted(skipped_frozen)) if skipped_frozen else ""))


if __name__ == "__main__":
    main()
