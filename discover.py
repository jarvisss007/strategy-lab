#!/usr/bin/env python3
"""Discovery engine — the autonomous strategy hunter, pointed at STRUCTURAL FRICTIONS
instead of price prediction. It generates hypotheses about *when* returns accrue and
*flow-driven* calendar windows (not "predict the price"), tests each through the
deflation + PBO gate with an out-of-sample holdout AND walk-forward folds, then logs
every verdict to discoveries.csv — the knowledge base that grows each run (the
learning). Reports both GROSS (is the structural pattern real?) and NET of costs (can
you actually trade it?), because for frictions the answer is usually "real but eaten
by the very costs that create the friction."

Run: /opt/anaconda3/bin/python discover.py
"""
import csv, os, sys
from datetime import datetime, timezone
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import overfit

COST = 0.0005       # 5 bps per trade
WARMUP = 20
PPY = 252
FOLDS = 5


def load():
    o = pd.read_csv(os.path.join(BASE, "data", "open.csv"), parse_dates=["date"]).set_index("date").sort_index()
    c = pd.read_csv(os.path.join(BASE, "data", "close.csv"), parse_dates=["date"]).set_index("date").sort_index()
    common = o.columns.intersection(c.columns)
    return o[common], c[common]


def ann_sharpe(r):
    r = np.asarray(r, float); r = r[np.isfinite(r)]
    if len(r) < 30 or r.std(ddof=1) == 0:
        return 0.0
    return r.mean() / r.std(ddof=1) * np.sqrt(PPY)


# ------------------------------------------------------------ friction families
def overnight_intraday(o, c):
    """The structural centerpiece: split each day into overnight (prev close -> open)
    and intraday (open -> close). Holding either leg means a full round-trip EVERY day
    (2 trades/day), so costs are brutal — that gap is the whole story."""
    overnight = (o / c.shift(1) - 1)
    intraday = (c / o - 1)
    out = {}
    legs = {"overnight": overnight, "intraday": intraday}
    for who in ("basket", "SPY"):
        for name, leg in legs.items():
            g = leg[["SPY"]].mean(axis=1) if who == "SPY" else leg.mean(axis=1)
            net = g - 2 * COST                       # enter + exit once per day
            out[f"{who} {name}"] = (g, net)
        # dollar-neutral structural: long overnight, short intraday
        gn = (overnight[["SPY"]] if who == "SPY" else overnight).mean(axis=1) - \
             (intraday[["SPY"]] if who == "SPY" else intraday).mean(axis=1)
        out[f"{who} overnight-minus-intraday"] = (gn, gn - 4 * COST)
    return out


def _third_friday(idx):
    return pd.Series([(d.weekday() == 4 and 15 <= d.day <= 21) for d in idx], index=idx)


def opex(o, c):
    """Options-expiration flow: monthly expiry = 3rd Friday. Test holding the basket in
    the expiry week, the week after (post-OpEx drift), and quad-witching months only."""
    daily = c.pct_change().mean(axis=1)
    idx = c.index
    tf = _third_friday(idx)
    out = {}
    # position windows relative to each 3rd Friday
    for lbl, lo, hi in [("opex-week", -4, 0), ("post-opex-week", 1, 5), ("pre-opex-week", -9, -5)]:
        pos = pd.Series(0.0, index=idx)
        fri_locs = np.where(tf.values)[0]
        for f in fri_locs:
            a, b = max(0, f + lo), min(len(idx) - 1, f + hi)
            pos.iloc[a:b + 1] = 1.0
        out[lbl] = _trade(pos, daily)
    # quad-witching months only (Mar/Jun/Sep/Dec), post-expiry week
    posq = pd.Series(0.0, index=idx)
    for f in np.where(tf.values)[0]:
        if idx[f].month in (3, 6, 9, 12):
            b = min(len(idx) - 1, f + 5)
            posq.iloc[f + 1:b + 1] = 1.0
    out["post-quadwitch-week"] = _trade(posq, daily)
    return out


def turn_of_month(o, c):
    """Month-end index/pension flow window: last t and first t trading days."""
    daily = c.pct_change().mean(axis=1)
    idx = c.index
    month = pd.Series(idx.to_period("M"), index=idx)
    is_last = (month != month.shift(-1)).values
    is_first = (month != month.shift(1)).values
    out = {}
    for t in (1, 3, 5):
        pos = np.zeros(len(idx))
        last_locs = np.where(is_last)[0]
        first_locs = np.where(is_first)[0]
        for f in last_locs:
            pos[max(0, f - t + 1):f + 1] = 1.0
        for f in first_locs:
            pos[f:min(len(idx), f + t)] = 1.0
        out[f"turn-of-month t{t}"] = _trade(pd.Series(pos, index=idx), daily)
    return out


def _trade(pos, daily):
    """Given a 0/1 position series and the basket's close-to-close return, return
    (gross, net) daily return series. Turnover charged on entering/exiting the window."""
    pos = pos.fillna(0.0)
    gross = pos.shift(1).fillna(0.0) * daily
    turnover = pos.diff().abs().fillna(0.0)
    return gross, gross - turnover * COST


FAMILIES = {
    "Overnight vs intraday": overnight_intraday,
    "Options-expiry flow": opex,
    "Turn-of-month flow": turn_of_month,
}


# ------------------------------------------------------------ the gate
def walk_forward(net):
    """Sign-consistency of Sharpe across FOLDS equal time slices (robustness)."""
    a = np.asarray(net, float); a = a[np.isfinite(a)]
    if len(a) < FOLDS * 40:
        return 0
    chunks = np.array_split(a, FOLDS)
    return int(sum(ann_sharpe(ch) > 0 for ch in chunks))


def judge(name, configs, bench):
    labels = list(configs.keys())
    gross = pd.DataFrame({k: v[0] for k, v in configs.items()}).iloc[WARMUP:]
    net = pd.DataFrame({k: v[1] for k, v in configs.items()}).iloc[WARMUP:]
    net = net.loc[:, net.std() > 1e-12].fillna(0.0)
    gross = gross[net.columns].fillna(0.0)
    if net.shape[1] < 2:
        return []
    rep = overfit.analyze(net.values, periods_per_year=PPY)
    split = int(len(net) * 0.6)
    rows = []
    for col in net.columns:
        g_sr = ann_sharpe(gross[col].values)
        n_sr = ann_sharpe(net[col].values)
        oos = ann_sharpe(net[col].values[split:])
        wf = walk_forward(net[col].values)
        rows.append({"family": name, "config": col, "gross_sharpe": round(g_sr, 2),
                     "net_sharpe": round(n_sr, 2), "oos_net_sharpe": round(oos, 2),
                     "walk_forward": f"{wf}/{FOLDS}"})
    # family-level verdict on the best NET config, from the gate
    rows.sort(key=lambda r: -r["net_sharpe"])
    rows[0]["family_dsr"] = round(rep["dsr"], 2)
    rows[0]["family_pbo"] = round(rep["pbo"], 2)
    best = rows[0]
    best["benchmark_bh"] = round(bench, 2)
    # honest bar: must clear deflation, low overfitting, walk-forward, AND beat simply
    # holding the basket (buy&hold) net of costs — not merely beat zero.
    survive = (rep["dsr"] >= 0.95 and rep["pbo"] < 0.5 and int(best["walk_forward"][0]) >= 4
               and best["net_sharpe"] > bench and best["oos_net_sharpe"] > bench)
    best["verdict"] = ("SURVIVOR (beats buy&hold)" if survive else
                       "real-but-loses-to-buy&hold" if best["net_sharpe"] > 0 else
                       "structural-but-uncostable" if best["gross_sharpe"] > 0.5 else "dead")
    return rows


def main():
    o, c = load()
    bench = ann_sharpe(c.pct_change().mean(axis=1).iloc[WARMUP:].values)  # buy&hold the basket
    kb = os.path.join(BASE, "discoveries.csv")
    new = not os.path.exists(kb)
    stamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")
    cols = ["run_date", "family", "config", "gross_sharpe", "net_sharpe", "oos_net_sharpe",
            "walk_forward", "family_dsr", "family_pbo", "benchmark_bh", "verdict"]
    all_rows = []
    print("=== Discovery engine — structural / friction hypotheses ===")
    print(f"(gross = is the pattern real? · net = tradeable after costs? · bar to beat = "
          f"basket buy&hold Sharpe {bench:.2f})\n")
    for fam, fn in FAMILIES.items():
        rows = judge(fam, fn(o, c), bench)
        if not rows:
            continue
        v = rows[0].get("verdict", "")
        print(f"{fam}")
        for r in rows:
            tag = f"   [{r.get('verdict')}] DSR {r.get('family_dsr')} PBO {r.get('family_pbo')}" if "verdict" in r else ""
            print(f"   {r['config']:32s} gross {r['gross_sharpe']:5.2f}  net {r['net_sharpe']:5.2f}  "
                  f"OOSnet {r['oos_net_sharpe']:5.2f}  wf {r['walk_forward']}{tag}")
        print()
        all_rows.extend(rows)

    with open(kb, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        if new:
            w.writeheader()
        for r in all_rows:
            w.writerow({"run_date": stamp, **r})

    surv = [r for r in all_rows if r.get("verdict") == "SURVIVOR"]
    struct = [r for r in all_rows if r.get("verdict") == "structural-but-uncostable"]
    print("=" * 60)
    print(f"SURVIVORS (real + tradeable net of costs): {len(surv)}")
    for r in surv:
        print(f"  ✓ {r['family']} — {r['config']}: net {r['net_sharpe']}, OOS {r['oos_net_sharpe']}, wf {r['walk_forward']}")
    print(f"REAL BUT UNCOSTABLE (structural pattern exists, costs eat it): {len(struct)}")
    for r in struct:
        print(f"  ~ {r['family']} — {r['config']}: gross {r['gross_sharpe']} but net {r['net_sharpe']}")
    if not surv:
        print("\nNo tradeable structural edge survived. Where a gross pattern is real but net is")
        print("negative, the friction (per-trade cost) is exactly what makes it untradeable —")
        print("that IS the honest finding, logged to discoveries.csv.")


if __name__ == "__main__":
    main()
