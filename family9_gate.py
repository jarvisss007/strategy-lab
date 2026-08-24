#!/usr/bin/env python3
"""family9_gate.py — FAMILY 9 (own-history value + quality floor) through the deflation gate.

REGISTRY.md FAMILY 9, registered 2026-08-24 BEFORE this file or its data existed; the desk's
forecast (VAL-F9, p=0.20) is on file. Grid, bars, benchmark and data law are the registry's:

  At each quarter-end t, for each name: the latest annual filing with filed < t gives net
  income, equity and diluted shares. Market cap = filed shares × RAW close at t (same-era
  bases — the GRML lesson, applied in advance), so P/E = cap / NI (NI>0; P/B where NI<=0).
  A name qualifies when its ratio sits in the bottom D-percentile of its OWN quarterly
  ratio history (expanding window, >= 20 prior quarters required) AND its Piotroski F-score
  from the same filings is >= Q. Equal weight, quarterly rebalance, hold until the name's
  percentile exceeds 50 or H months pass; 10 bp per side. Returns use ADJUSTED prices;
  benchmark SPY over identical windows. Grid: D in {10,20} x Q in {6,7} x H in {6,12} = 8.
  Bars: DSR >= 0.95 over the 8-grid on the first 70% of months; PBO < 0.5; positive net
  OOS EXCESS on the untouched final 30%.

Run: /opt/anaconda3/bin/python family9_gate.py  ->  reports/family9_gate.{json,md}
"""
import csv, json, os, sys, datetime as dt
import numpy as np, pandas as pd
import warnings; warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.expanduser("~/backtest-overfitting"))
import overfit

PANEL = os.path.join(HERE, "data", "value_panel.csv")
GRID = [(D, Q, H) for D in (10, 20) for Q in (6, 7) for H in (6, 12)]
COST, IS_FRAC, MIN_HIST_Q = 10 / 1e4, 0.70, 20


def fscore(cur, prev):
    """Piotroski from two consecutive FY rows (both already filed at decision time)."""
    def f(r, k):
        try: return float(r[k])
        except (ValueError, TypeError, KeyError): return None
    ni, ni0 = f(cur, "ni"), f(prev, "ni")
    a, a0 = f(cur, "assets"), f(prev, "assets")
    cfo = f(cur, "cfo")
    ltd, ltd0 = f(cur, "ltd") or 0.0, f(prev, "ltd") or 0.0
    ac, lc = f(cur, "assets_cur"), f(cur, "liab_cur")
    ac0, lc0 = f(prev, "assets_cur"), f(prev, "liab_cur")
    sh, sh0 = f(cur, "shares"), f(prev, "shares")
    rev, rev0 = f(cur, "revenue"), f(prev, "revenue")
    g, g0 = f(cur, "gross"), f(prev, "gross")
    s = 0
    if ni is not None and a: s += ni / a > 0
    if cfo is not None: s += cfo > 0
    if None not in (ni, a, ni0, a0) and a and a0: s += ni / a > ni0 / a0
    if None not in (cfo, ni): s += cfo > ni
    if a and a0: s += ltd / a <= ltd0 / a0
    if None not in (ac, lc, ac0, lc0) and lc and lc0: s += ac / lc > ac0 / lc0
    if None not in (sh, sh0) and sh0: s += sh <= sh0 * 1.02
    if None not in (g, rev, g0, rev0) and rev and rev0: s += g / rev > g0 / rev0
    if None not in (rev, a, rev0, a0) and a and a0: s += rev / a > rev0 / a0
    return s


def main():
    panel = {}
    for r in csv.DictReader(open(PANEL)):
        panel.setdefault(r["ticker"], []).append(r)
    for tk in panel:
        panel[tk].sort(key=lambda r: int(r["fy"]))
    names = sorted(panel)
    print(f"panel: {len(names)} names")

    import yfinance as yf
    raw = yf.download(names + ["SPY"], start="2009-01-01", auto_adjust=False, progress=False)["Close"]
    adj = yf.download(names + ["SPY"], start="2009-01-01", auto_adjust=True, progress=False)["Close"]
    raw.index = raw.index.tz_localize(None); adj.index = adj.index.tz_localize(None)
    mraw = raw.resample("ME").last(); madj = adj.resample("ME").last()
    months = [m for m in mraw.index if m >= pd.Timestamp("2010-01-31")]
    qends = [m for m in months if m.month in (3, 6, 9, 12)]

    # point-in-time ratio + F per name per quarter-end
    ratio = pd.DataFrame(index=qends, columns=names, dtype=float)
    fsc = pd.DataFrame(index=qends, columns=names, dtype=float)
    for tk in names:
        rows = panel[tk]
        for q in qends:
            avail = [r for r in rows if r["filed"] and r["filed"] < q.strftime("%Y-%m-%d")]
            if len(avail) < 2:
                continue
            cur, prev = avail[-1], avail[-2]
            try:
                sh = float(cur["shares"]); px = mraw.at[q, tk]
                if not sh or not np.isfinite(px):
                    continue
                cap = sh * px
                ni = float(cur["ni"]) if cur["ni"] else None
                eq = float(cur["equity"]) if cur["equity"] else None
                if ni and ni > 0:
                    ratio.at[q, tk] = cap / ni
                elif eq and eq > 0:
                    ratio.at[q, tk] = cap / eq
                else:
                    continue
                fsc.at[q, tk] = fscore(cur, prev)
            except (ValueError, KeyError, TypeError):
                continue

    # own-history percentile (expanding, min 20 prior quarters)
    pct = pd.DataFrame(index=qends, columns=names, dtype=float)
    for tk in names:
        s = ratio[tk]
        for i, q in enumerate(qends):
            hist = s.iloc[:i].dropna()
            if len(hist) < MIN_HIST_Q or not np.isfinite(s.iloc[i]):
                continue
            pct.at[q, tk] = 100.0 * (hist < s.iloc[i]).mean()

    mret = madj[names].pct_change()
    spy = madj["SPY"].pct_change()

    def run(D, Q, H):
        held = {}                                        # tk -> months held
        out = []
        w_prev = pd.Series(0.0, index=names)
        for m in months[1:]:
            if m in qends[:-1] or (held and m in qends):
                q = m
                keep = {}
                for tk, age in held.items():
                    p = pct.at[q, tk] if q in pct.index else np.nan
                    if age < H and not (np.isfinite(p) and p > 50):
                        keep[tk] = age
                new = [tk for tk in names
                       if np.isfinite(pct.at[q, tk] if q in pct.index else np.nan)
                       and pct.at[q, tk] <= D
                       and np.isfinite(fsc.at[q, tk] if q in fsc.index else np.nan)
                       and fsc.at[q, tk] >= Q and tk not in keep]
                held = {**keep, **{tk: 0 for tk in new}}
            w = pd.Series(0.0, index=names)
            if held:
                w[list(held)] = 1.0 / len(held)
            r = float((w_prev * mret.loc[m].fillna(0.0)).sum())
            cost = float((w - w_prev).abs().sum()) * COST
            out.append((m, r - cost - (float(spy.loc[m]) if np.isfinite(spy.loc[m]) else 0.0) * float(w_prev.sum() > 0)))
            held = {tk: a + 1 for tk, a in held.items()}
            w_prev = w
        s = pd.Series(dict(out))
        return s

    rets = {c: run(*c) for c in GRID}
    idx = rets[GRID[0]].index
    cut = int(len(idx) * IS_FRAC); is_idx, oos_idx = idx[:cut], idx[cut:]
    M = np.column_stack([rets[c].loc[is_idx].values for c in GRID])
    M = M[~(np.abs(M).sum(axis=1) == 0)]
    rep = overfit.analyze(M, periods_per_year=12, n_splits=16)
    best = GRID[rep["best_strategy"]]
    def ann(x):
        x = np.asarray(x, float); x = x[~np.isnan(x)]
        return float(x.mean() / x.std() * np.sqrt(12)) if len(x) > 2 and x.std() > 0 else float("nan")
    oos_sr = ann(rets[best].loc[oos_idx])
    oos_tot = float((1 + pd.Series(rets[best].loc[oos_idx])).prod() - 1)
    bars = {"1_dsr_ge_0.95": bool(rep["dsr"] >= 0.95), "2_pbo_lt_0.5": bool(rep["pbo"] < 0.5),
            "3_oos_excess_gt_0": bool(oos_tot > 0)}
    table = [{"D": c[0], "Q": c[1], "H": c[2], "is_sharpe_xs": round(ann(rets[c].loc[is_idx]), 3),
              "oos_sharpe_xs": round(ann(rets[c].loc[oos_idx]), 3)} for c in GRID]
    out = {"run": dt.datetime.now().strftime("%Y-%m-%d %H:%M PT"), "hypothesis": "FAMILY 9 own-history value + quality floor",
           "names": len(names), "months": len(idx), "is_range": [str(is_idx[0].date()), str(is_idx[-1].date())],
           "oos_range": [str(oos_idx[0].date()), str(oos_idx[-1].date())],
           "best_config": {"D": best[0], "Q": best[1], "H": best[2]},
           "is_best_sharpe_excess": round(rep["best_sharpe_annual"], 3),
           "deflated_benchmark": round(rep["deflated_benchmark_sharpe_annual"], 3),
           "dsr": round(rep["dsr"], 4), "pbo": round(rep["pbo"], 4),
           "oos_sharpe_excess": round(oos_sr, 3), "oos_total_excess_pct": round(100 * oos_tot, 1),
           "bars": bars, "verdict": "SURVIVES the gate" if all(bars.values()) else "FAILS the gate",
           "toolkit_verdict": rep["verdict"], "grid": table,
           "caveats": ["survivorship-tilted, growth-heavy universe (bias against value in-sample, stated at registration)",
                       "annual filings only; quarterly TTM would react faster", "one 70/30 split; n=1 experiment"]}
    os.makedirs(os.path.join(HERE, "reports"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "reports", "family9_gate.json"), "w"), indent=1)
    md = [f"# FAMILY 9 — own-history value + quality floor · {out['run']}", "",
          f"{out['names']} names · monthly excess vs SPY · IS {out['is_range'][0]}→{out['is_range'][1]} · OOS {out['oos_range'][0]}→{out['oos_range'][1]}", "",
          f"**Verdict: {out['verdict']}**", "", "| bar | value | pass |", "|---|---|---|",
          f"| 1 · DSR ≥ 0.95 (best of 8, IS) | {out['dsr']} | {'✅' if bars['1_dsr_ge_0.95'] else '❌'} |",
          f"| 2 · PBO < 0.5 | {out['pbo']} | {'✅' if bars['2_pbo_lt_0.5'] else '❌'} |",
          f"| 3 · OOS total excess > 0 | {out['oos_total_excess_pct']}% | {'✅' if bars['3_oos_excess_gt_0'] else '❌'} |", "",
          f"Best IS config D={best[0]}th pctile, F≥{best[1]}, hold {best[2]}m: IS excess Sharpe {out['is_best_sharpe_excess']} vs deflated benchmark {out['deflated_benchmark']}. Toolkit: {rep['verdict']}.", "",
          "Caveats: " + " · ".join(out["caveats"]), "", "| D | Q | H | IS xs Sharpe | OOS xs Sharpe |", "|---|---|---|---|---|"]
    md += [f"| {t['D']} | {t['Q']} | {t['H']} | {t['is_sharpe_xs']} | {t['oos_sharpe_xs']} |" for t in table]
    open(os.path.join(HERE, "reports", "family9_gate.md"), "w").write("\n".join(md) + "\n")
    print(json.dumps({k: out[k] for k in ("best_config", "is_best_sharpe_excess", "deflated_benchmark", "dsr", "pbo", "oos_sharpe_excess", "oos_total_excess_pct", "bars", "verdict")}, indent=1))


if __name__ == "__main__":
    main()
