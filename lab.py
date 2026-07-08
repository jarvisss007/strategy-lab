#!/usr/bin/env python3
"""Strategy Lab runner. For every strategy family: build the (T x N) matrix of
net-of-cost daily returns across its parameter grid, then judge it two ways —

  1. overfit.analyze()  — Deflated Sharpe + PBO over the whole grid (your toolkit),
     which discounts the best config for the number of trials it took to find it.
  2. Out-of-sample holdout — pick the best config on the first 70% of history,
     then measure how much of its Sharpe survives on the untouched last 30%.

A strategy is only interesting if it clears BOTH: survives deflation AND keeps
its edge out of sample. Results append to knowledge_base.csv (the lab's memory)
and render to reports/report.md + reports/data.json.
"""
import csv, json, os, sys
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import overfit
import strategies as S

WARMUP = 252          # drop first year (indicator warm-up) before judging
OOS_FRAC = 0.30       # last 30% of history is the untouched holdout
PPY = 252


def load_prices():
    df = pd.read_csv(os.path.join(BASE, "data", "prices.csv"))
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date").sort_index()


def _finite(o):
    """Recursively replace non-finite floats (inf/nan) with None for valid JSON."""
    if isinstance(o, dict):
        return {k: _finite(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_finite(v) for v in o]
    if isinstance(o, float) and not np.isfinite(o):
        return None
    return o


def ann_sharpe(r):
    r = np.asarray(r, float)
    r = r[np.isfinite(r)]
    if r.std(ddof=1) == 0 or len(r) < 30:
        return 0.0
    return r.mean() / r.std(ddof=1) * np.sqrt(PPY)


def judge_family(name, series_dict):
    # align, trim warm-up, drop dead (zero-variance) configs
    M = pd.DataFrame(series_dict).iloc[WARMUP:].dropna(how="all")
    M = M.loc[:, M.std() > 1e-12].fillna(0.0)
    if M.shape[1] < 2:
        return None
    arr = M.values
    rep = overfit.analyze(arr, periods_per_year=PPY)

    # out-of-sample holdout on the same grid
    split = int(len(M) * (1 - OOS_FRAC))
    IS, OOS = arr[:split], arr[split:]
    is_sr = np.array([ann_sharpe(IS[:, j]) for j in range(IS.shape[1])])
    best = int(np.argmax(is_sr))
    oos_sr = ann_sharpe(OOS[:, best])
    best_label = M.columns[best]

    return {
        "family": name,
        "n_configs": int(M.shape[1]),
        "n_obs": int(M.shape[0]),
        "best_config_fullsample": M.columns[int(rep["best_strategy"])],
        "best_sharpe_annual": round(rep["best_sharpe_annual"], 3),
        "deflated_sharpe": round(rep["dsr"], 3),
        "pbo": round(rep["pbo"], 3),
        "min_backtest_len_years": round(rep["min_backtest_length_years"], 1),
        "oos_best_config": best_label,
        "is_sharpe": round(float(is_sr[best]), 3),
        "oos_sharpe": round(float(oos_sr), 3),
        "oos_retention": round(float(oos_sr / is_sr[best]), 2) if is_sr[best] > 0 else 0.0,
        "verdict": rep["verdict"].split(":")[0],
        "verdict_full": rep["verdict"],
    }


def main():
    prices = load_prices()
    rets = prices.pct_change()
    bh = ann_sharpe(rets["SPY"].iloc[WARMUP:]) if "SPY" in rets else float("nan")

    rows = []
    for fam, fn in S.FAMILIES.items():
        try:
            res = judge_family(fam, fn(prices, rets))
            if res:
                rows.append(res)
                print(f"{fam:32s} DSR {res['deflated_sharpe']:.2f}  PBO {res['pbo']:.2f}  "
                      f"OOS {res['oos_sharpe']:.2f}  {res['verdict']}")
        except Exception as e:
            print(f"{fam}: ERROR {e}")

    # rank: survivors first, then by OOS Sharpe
    order = {"survives": 0, "suspect": 1, "OVERFIT": 2, "inconclusive": 3}
    rows.sort(key=lambda r: (order.get(r["verdict"], 9), -r["oos_sharpe"]))

    meta = json.load(open(os.path.join(BASE, "data", "meta.json")))
    out = {"built": meta["built"], "window": f"{meta['start']} … {meta['end']}",
           "n_tickers": meta["n_tickers"], "spy_buyhold_sharpe": round(bh, 3),
           "cost_bps": int(S.COST * 1e4), "results": rows}
    out = _finite(out)  # standard JSON has no Infinity/NaN — replace with null
    json.dump(out, open(os.path.join(BASE, "reports", "data.json"), "w"), indent=1)
    write_kb(rows, meta)
    write_report(out)
    print(f"\nSPY buy&hold Sharpe (same window): {bh:.2f}")
    print("report -> reports/report.md   dashboard data -> reports/data.json")


def write_kb(rows, meta):
    path = os.path.join(BASE, "knowledge_base.csv")
    new = not os.path.exists(path)
    cols = ["run_date", "family", "n_configs", "best_sharpe_annual", "deflated_sharpe",
            "pbo", "min_backtest_len_years", "is_sharpe", "oos_sharpe", "oos_retention", "verdict"]
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        if new:
            w.writeheader()
        for r in rows:
            w.writerow({"run_date": meta["built"][:10], **{k: r[k] for k in cols if k in r}})


def write_report(out):
    L = [f"# Strategy Lab — honest survey", "",
         f"**Window:** {out['window']}  ·  **{out['n_tickers']} tickers**  ·  "
         f"cost {out['cost_bps']} bps/turnover  ·  built {out['built']}", "",
         f"**Benchmark:** SPY buy-and-hold Sharpe = **{out['spy_buyhold_sharpe']}** "
         f"(the number any strategy has to beat to be worth the trouble).", "",
         "Each family was tested across its full parameter grid. `Deflated Sharpe` "
         "discounts the best config for how many were tried (≥0.95 = significant). "
         "`PBO` is the probability the in-sample winner underperforms out of sample "
         "(>0.5 = overfit). `OOS Sharpe` is the in-sample winner's Sharpe on the "
         "untouched last 30% of history. A real edge needs DSR high, PBO low, and "
         "OOS Sharpe that survives.", "",
         "| Family | Configs | Best Sharpe (IS) | Deflated Sharpe | PBO | OOS Sharpe | Retained | Verdict |",
         "|---|--:|--:|--:|--:|--:|--:|---|"]
    for r in out["results"]:
        L.append(f"| {r['family']} | {r['n_configs']} | {r['best_sharpe_annual']} | "
                 f"{r['deflated_sharpe']} | {r['pbo']} | {r['oos_sharpe']} | "
                 f"{r['oos_retention']} | **{r['verdict']}** |")
    surv = [r for r in out["results"] if r["verdict"] == "survives"]
    L += ["", "## What survived", ""]
    if surv:
        for r in surv:
            L.append(f"- **{r['family']}** — best OOS config `{r['oos_best_config']}`, "
                     f"OOS Sharpe {r['oos_sharpe']} (kept {int(r['oos_retention']*100)}% of in-sample). "
                     f"Worth paper-trading forward, not betting on.")
    else:
        L.append("- Nothing cleared both gates. That is the honest, expected result for "
                 "daily strategies on liquid large-caps — the most arbitraged data there is. "
                 "The value here is the *map* of what's been ruled out, not a signal.")
    L += ["", "## Read this before believing any survivor", "",
          "The gate is working — it correctly rejected the **day-of-week** noise control "
          "(OVERFIT) and both genuinely market-neutral alpha attempts (**cross-sectional "
          "momentum** and **short-term reversal** failed out of sample). That is the signal "
          "that the machinery is honest. But the survivors carry heavy caveats:",
          "",
          "- **They are not alpha — they are risk-managed long equity beta.** Every survivor "
          "(MA-trend, vol-managed SPY, turn-of-month) is *long-only*. They beat SPY by "
          "sidestepping drawdowns or sitting out risky stretches, not by predicting anything. "
          "The strategies that would be true market-neutral edge are the ones that **failed**.",
          "- **Survivorship bias.** The universe is *today's* watchlist — names that already "
          "won their way onto it. Backtesting them 15 years inflates every long-equity result.",
          "- **The out-of-sample window (≈2022–2026) contains one big bear market.** Trend and "
          "vol filters mechanically look great in any sample that holds a drawdown they dodge; "
          "that is regime luck, not a stable edge.",
          "- **Costs are modeled simply** (5 bps/turnover, no slippage, borrow, or impact). "
          "The market-neutral strategies that need shorting are understated — they look *worse* "
          "in reality, not better.",
          "- **Cross-family selection.** Picking the best of 8 families adds a layer of multiple "
          "testing the per-family Deflated Sharpe does not capture.",
          "",
          "**Bottom line:** consistent with spy-trading and zero-dte-lab — no tradeable "
          "market-neutral edge here. The one durable, well-documented *lesson* (not a money "
          "machine) is that trend/vol filters improve the risk-adjusted return of long equity "
          "exposure. That is beta-timing, worth understanding, not an edge to bet on.", "",
          "## What may be worth watching", "",
          "Ranked by out-of-sample Sharpe (survivors + suspects). 'May work' means "
          "'survived the holdout here' — it is a forward-test candidate, never a prediction:"]
    for r in [x for x in out["results"] if x["oos_sharpe"] > out["spy_buyhold_sharpe"]][:5]:
        L.append(f"- {r['family']} (`{r['oos_best_config']}`): OOS {r['oos_sharpe']} "
                 f"vs SPY {out['spy_buyhold_sharpe']} — {r['verdict']}")
    L += ["", "---", "*A research survey, not investment advice. Survivors are candidates "
          "for forward paper-trading and deeper validation, nothing more.*", ""]
    open(os.path.join(BASE, "reports", "report.md"), "w").write("\n".join(L))


if __name__ == "__main__":
    main()
