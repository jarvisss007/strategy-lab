#!/usr/bin/env python3
"""value_forward.py — FAMILY 9's forward paper book. The rule is frozen; this only executes it.

Registered in REGISTRY.md 2026-08-24 after the gate run (FAILS, closest miss on record:
DSR 0.79, PBO 0.52, +23.1% OOS excess). Per the CANSLIM precedent a failed family may run
FORWARD as measurement — the forward book, not the backtest, decides. The rule is the
IS-chosen config and may never be tuned: at each QUARTER-END formation, buy every universe
name whose cap-based valuation ratio (filed shares × raw close / net income, P/B where
NI<=0; facts only from filings FILED before the formation date) sits in the bottom 20% of
its OWN quarterly ratio history (>= 20 prior quarters) AND whose Piotroski F >= 6 from the
same filings. $2,000 paper units. At later quarterly reviews a holding exits when its
percentile exceeds 50 or it has been held 6 months; exits fill at the last settled close;
excess is vs SPY over the identical window, recorded per row.

First formation: 2026-09-30 (the registry's date). Running earlier marks the book and
prints the pipeline's health; it forms nothing. A formation happens on the first run ON or
AFTER a quarter-end that has no formation recorded yet — a late laptop does not skip a
quarter, it forms late and says so.

Files: reports/value_book.csv (the record), reports/value_state.json (marks for pages).
Run:  /opt/anaconda3/bin/python value_forward.py            # mark; form if a quarter-end is due
      /opt/anaconda3/bin/python value_forward.py --dry      # show today's candidates, write nothing
"""
import csv, json, os, sys, datetime as dt
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
PANEL = os.path.join(HERE, "data", "value_panel.csv")
BOOK = os.path.join(HERE, "reports", "value_book.csv")
STATE = os.path.join(HERE, "reports", "value_state.json")
D_PCT, F_MIN, HOLD_M, UNIT, MIN_HIST_Q = 20.0, 6, 6, 2000.0, 20
FIRST_FORMATION = dt.date(2026, 9, 30)
COLS = ["opened", "ticker", "entry_px", "shares", "spy_at_entry", "review_after",
        "exited", "exit_px", "spy_at_exit", "net_pct", "excess_pct", "exit_reason", "note"]

sys.path.insert(0, HERE)
from family9_gate import fscore                     # one definition of the quality floor


def quarter_ends(upto):
    q = []
    for y in range(2015, upto.year + 1):
        for m, dd in ((3, 31), (6, 30), (9, 30), (12, 31)):
            d = dt.date(y, m, dd)
            if d <= upto:
                q.append(d)
    return q


def load_panel():
    panel = {}
    for r in csv.DictReader(open(PANEL)):
        panel.setdefault(r["ticker"], []).append(r)
    for tk in panel:
        panel[tk].sort(key=lambda r: int(r["fy"]))
    return panel


def ratios_and_f(panel, names, when, mraw):
    """{tk: (ratio, own_pctile, fscore)} at date `when`, filed-date law enforced."""
    out = {}
    qs = [q for q in quarter_ends(when) if q < when]
    for tk in names:
        rows = panel.get(tk, [])
        if tk not in mraw.columns:
            continue
        def ratio_at(d):
            avail = [r for r in rows if r["filed"] and r["filed"] < d.isoformat()]
            if len(avail) < 2:
                return None, None
            cur = avail[-1]
            px_ser = mraw[tk].loc[:pd.Timestamp(d)]
            if px_ser.dropna().empty:
                return None, None
            px = float(px_ser.dropna().iloc[-1])
            try:
                sh = float(cur["shares"]); ni = float(cur["ni"]) if cur["ni"] else None
                eq = float(cur["equity"]) if cur["equity"] else None
            except ValueError:
                return None, None
            if not sh or px <= 0:
                return None, None
            cap = sh * px
            if ni and ni > 0:
                return cap / ni, avail
            if eq and eq > 0:
                return cap / eq, avail
            return None, None
        r_now, avail = ratio_at(when)
        if r_now is None:
            continue
        hist = [ratio_at(q)[0] for q in qs]
        hist = [h for h in hist if h is not None]
        if len(hist) < MIN_HIST_Q:
            continue
        pct = 100.0 * float(np.mean([h < r_now for h in hist]))
        f = fscore(avail[-1], avail[-2])
        out[tk] = (r_now, pct, f)
    return out


def main():
    dry = "--dry" in sys.argv
    today = dt.date.today()
    import yfinance as yf
    panel = load_panel()
    names = sorted(panel)
    px = yf.download(names + ["SPY"], start="2015-01-01", auto_adjust=False, progress=False)["Close"]
    px.index = px.index.tz_localize(None)
    mraw = px.resample("ME").last()
    last_close = px.ffill().iloc[-1]
    last_day = px.index[-1].date()

    rows = list(csv.DictReader(open(BOOK))) if os.path.exists(BOOK) else []
    open_rows = [r for r in rows if not (r.get("exited") or "").strip()]

    # ---- mark ---------------------------------------------------------------
    marks = []
    for r in open_rows:
        p = last_close.get(r["ticker"])
        if p is not None and np.isfinite(p):
            marks.append({"ticker": r["ticker"], "entry_px": float(r["entry_px"]),
                          "now_px": round(float(p), 2),
                          "pnl_pct": round(100 * (float(p) / float(r["entry_px"]) - 1), 2),
                          "opened": r["opened"]})

    # ---- reviews and formation at a due quarter-end -------------------------
    formed, exited = [], []
    done_qs = {r["opened"] for r in rows} | {r.get("note", "") for r in rows}
    due = [q for q in quarter_ends(today) if q >= FIRST_FORMATION
           and not any(r["opened"] == q.isoformat() or f"formation {q.isoformat()}" in (r.get("note") or "") for r in rows)]
    if due and not dry:
        q = due[0]
        sig = ratios_and_f(panel, names, min(q, last_day), mraw)
        # reviews first: exits at this quarter's signal
        for r in open_rows:
            age_m = (q.year - dt.date.fromisoformat(r["opened"]).year) * 12 + (q.month - dt.date.fromisoformat(r["opened"]).month)
            s = sig.get(r["ticker"])
            reason = None
            if age_m >= HOLD_M:
                reason = f"held {age_m}m >= {HOLD_M}m"
            elif s and s[1] > 50:
                reason = f"own-history percentile {s[1]:.0f} > 50"
            if reason:
                p = float(last_close.get(r["ticker"], np.nan)); spy1 = float(last_close["SPY"])
                if np.isfinite(p):
                    r["exited"] = last_day.isoformat(); r["exit_px"] = f"{p:.2f}"
                    r["spy_at_exit"] = f"{spy1:.2f}"
                    net = p / float(r["entry_px"]) - 1
                    spyr = spy1 / float(r["spy_at_entry"]) - 1
                    r["net_pct"] = f"{100*net:.2f}"; r["excess_pct"] = f"{100*(net-spyr):.2f}"
                    r["exit_reason"] = reason
                    exited.append(f"{r['ticker']} {r['net_pct']}% ({r['excess_pct']}% xs) — {reason}")
        held = {r["ticker"] for r in rows if not (r.get("exited") or "").strip()}
        picks = sorted([tk for tk, (ratio, pct, f) in sig.items() if pct <= D_PCT and f >= F_MIN and tk not in held])
        for tk in picks:
            p = float(last_close.get(tk, np.nan))
            if not np.isfinite(p):
                continue
            rows.append({"opened": last_day.isoformat(), "ticker": tk, "entry_px": f"{p:.2f}",
                         "shares": f"{UNIT/p:.4f}", "spy_at_entry": f"{float(last_close['SPY']):.2f}",
                         "review_after": (q + dt.timedelta(days=92)).isoformat(),
                         "exited": "", "exit_px": "", "spy_at_exit": "", "net_pct": "", "excess_pct": "",
                         "exit_reason": "", "note": f"formation {q.isoformat()} (filled {last_day}, last settled close); rule frozen D<=20 F>=6 H=6m"})
            formed.append(tk)
        os.makedirs(os.path.dirname(BOOK), exist_ok=True)
        with open(BOOK, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS); w.writeheader()
            for r in rows: w.writerow({c: r.get(c, "") for c in COLS})

    # An empty book must EXIST. Until 2026-08-30 the file was written only inside the
    # formation branch, so with zero positions formed (next formation 2026-09-30) it
    # simply was not there — and coverage_ratchet flagged the check that reads it as "a
    # light wired to nothing". A missing artifact is indistinguishable from a runner that
    # never ran, which is the failure mode this desk keeps rediscovering. An empty book
    # with headers is a statement: the runner ran and formed nothing.
    if not dry and not os.path.exists(BOOK):
        os.makedirs(os.path.dirname(BOOK), exist_ok=True)
        with open(BOOK, "w", newline="") as f:
            csv.DictWriter(f, fieldnames=COLS).writeheader()

    if dry:
        sig = ratios_and_f(panel, names, last_day, mraw)
        picks = sorted([(tk, round(pct), f) for tk, (ratio, pct, f) in sig.items() if pct <= D_PCT and f >= F_MIN])
        print(f"DRY {today}: {len(sig)} names scoreable; {len(picks)} would qualify today: "
              + ", ".join(f"{t}(p{p},F{f})" for t, p, f in picks[:15]) + ("…" if len(picks) > 15 else ""))
        return

    closed = [r for r in rows if (r.get("exited") or "").strip()]
    xs = [float(r["excess_pct"]) for r in closed if r.get("excess_pct")]
    state = {"generated": dt.datetime.now().strftime("%Y-%m-%d %H:%M PT"), "open": marks,
             "open_n": len([r for r in rows if not (r.get('exited') or '').strip()]),
             "closed_n": len(closed), "avg_excess_pct": round(sum(xs)/len(xs), 2) if xs else None,
             "next_formation": next((q.isoformat() for q in quarter_ends(dt.date(2035,1,1)) if q >= max(today, FIRST_FORMATION)), None),
             "rule": "FAMILY 9 frozen: own-history valuation pctile <= 20 (>=20 prior quarters) AND Piotroski F >= 6; $2,000 units; exit at pctile > 50 or 6 months; excess vs SPY"}
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(state, open(STATE, "w"), indent=1)
    print(f"value_forward {today}: book {state['open_n']} open / {state['closed_n']} closed"
          + (f" · FORMED {len(formed)}: {', '.join(formed)}" if formed else "")
          + (f" · EXITED {len(exited)}" if exited else "")
          + f" · next formation {state['next_formation']}")
    for e in exited: print("  exit: " + e)


if __name__ == "__main__":
    main()
