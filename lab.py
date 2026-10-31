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

THE HOLDOUT GATE (SLAB-001, ruled by Anupam 2026-10-31). Until then "survives" meant DSR >= 0.95
and PBO < 0.5 only; the holdout was computed and shown but decided nothing. Now the in-sample
winner is also judged on the last 30% by PRE_REGISTRATION section 2's pass bar (written for the
forward book; that file is an unratified DRAFT):
  - its day-clustered mean excess return over its OWN universe's buy-and-hold must be > 2 x its
    day-clustered standard error (rows are days, so one observation per day). Section 2 names
    SPY / NIFTY as the benchmark; the own-universe rule (SPY for SPY-only configs, the
    equal-weight basket for basket configs, cash for long-short configs) is Anupam's 10-31 ruling;
  - that mean must be positive after 2 x COST per round trip - the returns are already net of
    COST per unit of turnover, which is exactly that, so this bar is implied by the first;
  - section 2's deflation bar (the carried ~35-trial budget) is NOT applied - open for Anupam.
    The survey keeps its own per-family DSR >= 0.95, deflated over each family's 3-36 configs.
No retention bar. Missing or broken out-of-sample data fails the gate (fail closed).
`verdict` keeps its meaning (the DSR + PBO verdict, BENCH-002); `survey_verdict` is the label
after every gate, and `gate` records which gate produced it (knowledge_base.csv).
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
HOLDOUT_K = 2.0       # PRE_REGISTRATION section 2: mean excess > 2 x its day-clustered standard error
HOLDOUT_MIN_DAYS = 60  # PRE_REGISTRATION section 2 ("at >= 60 entry days"; section 1) -> fewer fails closed
GATE_DSR_PBO = "dsr_pbo"            # the gate that judged every row before SLAB-001: DSR >= 0.95 and PBO < 0.5
GATE_HOLDOUT = "dsr_pbo_holdout"    # SLAB-001 (2026-10-31): those two AND the PRE_REGISTRATION section 2 holdout
KB_COLS_V1 = ["run_date", "family", "n_configs", "best_sharpe_annual", "deflated_sharpe",
              "pbo", "min_backtest_len_years", "is_sharpe", "oos_sharpe", "oos_retention", "verdict"]
# BENCH-002: new columns only; no existing column changes meaning and no recorded value is rewritten
KB_COLS = KB_COLS_V1 + ["gate", "survey_verdict", "holdout", "holdout_benchmark",
                        "holdout_excess_ann", "holdout_se_ann", "holdout_margin_ann"]


def load_prices(path=None):
    df = pd.read_csv(path or os.path.join(BASE, "data", "prices.csv"))
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


def holdout_gate(config_oos, bench_oos, problem=None, k=HOLDOUT_K, min_days=HOLDOUT_MIN_DAYS):
    """PRE_REGISTRATION section 2 on the out-of-sample slice: PASS only if the mean daily excess
    (config minus its benchmark, both net of costs) is > k x its standard error AND > 0.

    FAIL CLOSED: a stated data problem, a missing series, a slice shorter than `min_days`, any
    non-finite return or an undefined (zero) standard error returns "fail-closed", never a pass.
    (ann_sharpe returns 0.0 on a broken slice - a bar any positive result clears; the gate never
    reads it.) Annualised figures are the daily figures x PPY, as fractions (0.03 = 3%/yr)."""
    out = {"holdout": "fail-closed", "holdout_reason": None, "holdout_n_days": 0,
           "holdout_excess_ann": None, "holdout_se_ann": None, "holdout_margin_ann": None,
           "holdout_t": None}

    def closed(why):
        out["holdout_reason"] = why
        return out

    if problem:
        return closed(problem)
    if config_oos is None or bench_oos is None:
        return closed("no out-of-sample series")
    x, b = np.asarray(config_oos, float), np.asarray(bench_oos, float)
    if x.ndim != 1 or x.shape != b.shape:
        return closed(f"config and benchmark slices do not align ({x.shape} vs {b.shape})")
    n = len(x)
    out["holdout_n_days"] = n
    if n < min_days:
        return closed(f"{n} out-of-sample days, fewer than {min_days}")
    if not (np.isfinite(x).all() and np.isfinite(b).all()):
        return closed("non-finite return in the out-of-sample slice")
    ex = x - b
    m, se = float(ex.mean()), float(ex.std(ddof=1) / np.sqrt(n))
    if not (np.isfinite(se) and se > 1e-12):        # the dead-config floor judge_family uses for std
        return closed("the excess has zero variance, so its standard error is undefined")
    passed = (m > k * se) and (m > 0)
    out.update(holdout="pass" if passed else "fail",
               holdout_excess_ann=m * PPY, holdout_se_ann=se * PPY,
               holdout_margin_ann=(m - k * se) * PPY, holdout_t=m / se,
               holdout_reason=(f"mean excess {m * PPY:+.2%}/yr {'>' if passed else '<='} "
                               f"{k:g} x SE ({k * se * PPY:.2%}/yr)"))
    return out


def oos_coverage_problem(prices, cols, dates):
    """None when the universe's prices are whole on the out-of-sample slice (and the row before
    it, which its first return needs), else the reason it is not. A hole = a name priced before
    and after a date but not on it - pct_change() pads it into a fake 0% day, which is how a
    futures-only row or a dropped fetch would otherwise pass silently."""
    if prices is None:
        return "no price panel to build the benchmark from"
    if len(dates) == 0:
        return "empty out-of-sample slice"
    absent = [c for c in cols if c not in prices.columns]
    if absent or not cols:
        return f"not in the price panel: {', '.join(absent) or 'no columns'}"
    idx = pd.DatetimeIndex(dates)
    if not idx.isin(prices.index).all():
        return "out-of-sample dates missing from the price panel"
    pos = prices.index.get_indexer(idx)
    P = prices[cols]
    interior = P.ffill().notna() & P.bfill().notna()
    window = prices.index[max(int(pos.min()) - 1, 0): int(pos.max()) + 1]
    holes = (interior & P.isna()).loc[window]
    if holes.values.any():
        bad = holes.index[holes.any(axis=1)]
        return (f"{int(holes.values.sum())} missing prices on {len(bad)} out-of-sample dates "
                f"(first {bad[0].date()})")
    unpriced = ~P.loc[window].notna().any(axis=1)
    if unpriced.any():
        return f"no priced name on {int(unpriced.sum())} out-of-sample dates (first {unpriced.index[unpriced][0].date()})"
    return None


def judge_holdout(config, config_oos, oos_dates, prices, rets, problem=None):
    """The holdout gate for one config: its universe's benchmark, the coverage check, the bar."""
    universe = S.universe_of(config)
    if problem:
        res = holdout_gate(None, None, problem=problem)
    elif universe is None:
        res = holdout_gate(None, None, problem=f"no registered universe for config {config!r}")
    elif prices is None or rets is None:
        res = holdout_gate(None, None, problem="no price panel to build the benchmark from")
    else:
        problem = oos_coverage_problem(prices, S.universe_columns(universe, prices), oos_dates)
        bench = None
        if problem is None:
            bench = S.buy_and_hold(universe, prices, rets).reindex(pd.DatetimeIndex(oos_dates)).values
        res = holdout_gate(config_oos, bench, problem=problem)
    res["holdout_benchmark"] = universe or ""
    return res


def survey_verdict(verdict, holdout):
    """The survey's label after every gate: a DSR + PBO "survives" that fails (or cannot be judged
    on) the holdout becomes "suspect" - unproven; every other verdict stands as it is."""
    return "suspect" if verdict == "survives" and holdout != "pass" else verdict


def _r(v, nd):
    return None if v is None else round(float(v), nd)


def judge_family(name, series_dict, prices=None, rets=None, oos_start=None):
    """`prices`/`rets` build each config's holdout benchmark; without them the holdout fails closed.
    `oos_start` (replays only) starts the holdout slice on that date instead of at the last 30%."""
    # align, trim warm-up, drop dead (zero-variance) configs
    M = pd.DataFrame(series_dict).iloc[WARMUP:].dropna(how="all")
    M = M.loc[:, M.std() > 1e-12]
    gaps = M.isna()                 # before the 0-fill: a config return that never existed
    M = M.fillna(0.0)
    if M.shape[1] < 2:
        return None
    arr = M.values
    rep = overfit.analyze(arr, periods_per_year=PPY)

    # out-of-sample holdout on the same grid
    split = (int(M.index.searchsorted(pd.Timestamp(oos_start))) if oos_start
             else int(len(M) * (1 - OOS_FRAC)))
    IS, OOS = arr[:split], arr[split:]
    is_sr = np.array([ann_sharpe(IS[:, j]) for j in range(IS.shape[1])])
    best = int(np.argmax(is_sr))
    oos_sr = ann_sharpe(OOS[:, best])
    best_label = M.columns[best]

    # the holdout gate (SLAB-001): the in-sample winner vs its own universe on the same dates
    oos_dates = M.index[split:]
    n_gaps = int(gaps[best_label].iloc[split:].sum())
    hold = judge_holdout(best_label, OOS[:, best], oos_dates, prices, rets,
                         problem=f"{n_gaps} out-of-sample days with no config return" if n_gaps else None)
    verdict = rep["verdict"].split(":")[0]

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
        "verdict": verdict,                      # the DSR + PBO verdict - its meaning is unchanged (BENCH-002)
        "verdict_full": rep["verdict"],
        "gate": GATE_HOLDOUT,
        "survey_verdict": survey_verdict(verdict, hold["holdout"]),
        "holdout": hold["holdout"],
        "holdout_reason": hold["holdout_reason"],
        "holdout_benchmark": hold["holdout_benchmark"],
        "holdout_window": f"{oos_dates[0].date()} … {oos_dates[-1].date()}" if len(oos_dates) else None,
        "holdout_n_days": hold["holdout_n_days"],
        "holdout_excess_ann": _r(hold["holdout_excess_ann"], 4),
        "holdout_se_ann": _r(hold["holdout_se_ann"], 4),
        "holdout_margin_ann": _r(hold["holdout_margin_ann"], 4),
        "holdout_t": _r(hold["holdout_t"], 2),
    }


def _args(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="Strategy Lab survey (lab.py). A replay prints and writes nothing.")
    ap.add_argument("--prices", help="price panel to read (default data/prices.csv)")
    ap.add_argument("--universe-from", dest="universe_from",
                    help="replay: a meta.json whose 'tickers' list is the universe (e.g. an earlier run's)")
    ap.add_argument("--end", help="replay: last date of the panel")
    ap.add_argument("--oos-start", dest="oos_start",
                    help="replay: first date of the holdout slice instead of the last 30%%")
    ap.add_argument("--replay", action="store_true",
                    help="print only: no report, dashboard or knowledge-base row (implied by the replay options)")
    a = ap.parse_args(argv)
    a.replay = a.replay or bool(a.universe_from or a.end or a.oos_start)
    return a


def _holdout_line(r):
    if r["holdout"] == "fail-closed":
        return f"holdout vs {r['holdout_benchmark'] or '?'}: FAIL-CLOSED ({r['holdout_reason']})"
    return (f"holdout vs {r['holdout_benchmark']}: excess {r['holdout_excess_ann']:+.2%}/yr, "
            f"SE {r['holdout_se_ann']:.2%}, margin {r['holdout_margin_ann']:+.2%}, "
            f"t {r['holdout_t']:+.2f} -> {r['holdout']}")


def main(argv=None):
    args = _args(argv)
    prices = load_prices(args.prices)
    if args.universe_from:
        tickers = json.load(open(args.universe_from))["tickers"]
        absent = [t for t in tickers if t not in prices.columns]
        if absent:
            raise SystemExit(f"ABORT: the replayed universe is not in the panel: {absent}")
        prices = prices[tickers]
    if args.end:
        prices = prices.loc[:args.end]
    if args.replay:
        prices = prices.dropna(how="all")      # a row with no price for any replayed name is not a session
    rets = prices.pct_change()
    bh = ann_sharpe(rets["SPY"].iloc[WARMUP:]) if "SPY" in rets else float("nan")

    rows = []
    for fam, fn in S.FAMILIES.items():
        try:
            res = judge_family(fam, fn(prices, rets), prices, rets, oos_start=args.oos_start)
            if res:
                rows.append(res)
                print(f"{fam:32s} DSR {res['deflated_sharpe']:.2f}  PBO {res['pbo']:.2f}  "
                      f"OOS {res['oos_sharpe']:.2f}  {res['verdict']} -> {res['survey_verdict']}  "
                      f"[{res['oos_best_config']}] {_holdout_line(res)}")
        except Exception as e:
            print(f"{fam}: ERROR {e}")

    # rank: survivors first (after every gate), then by OOS Sharpe
    order = {"survives": 0, "suspect": 1, "OVERFIT": 2, "inconclusive": 3}
    rows.sort(key=lambda r: (order.get(r["survey_verdict"], 9), -r["oos_sharpe"]))

    if args.replay:
        w = rows[0]["holdout_window"] if rows else None
        print(f"\nREPLAY - nothing written. Panel {prices.index[0].date()} … {prices.index[-1].date()}, "
              f"{prices.shape[1]} tickers; holdout {w}; SPY buy&hold Sharpe (same window): {bh:.3f}")
        return rows

    meta = json.load(open(os.path.join(BASE, "data", "meta.json")))
    out = {"built": meta["built"], "window": f"{meta['start']} … {meta['end']}",
           "n_tickers": meta["n_tickers"], "spy_buyhold_sharpe": round(bh, 3),
           "holdout_gate": ("PRE_REGISTRATION section 2 on the last 30%: the in-sample winner's mean daily "
                            "excess over its own universe's buy-and-hold (SPY / equal-weight basket / cash for "
                            "long-short), net of costs, must be > 2 x its standard error and > 0; missing or "
                            "broken data fails closed. survey_verdict = verdict (DSR + PBO) after this gate."),
           "cost_bps": int(S.COST * 1e4), "results": rows}
    out = _finite(out)  # standard JSON has no Infinity/NaN — replace with null
    write_dashboard_data(out)
    write_kb(rows, meta)
    write_report(out)
    print(f"\nSPY buy&hold Sharpe (same window): {bh:.2f}")
    print("report -> reports/report.md   dashboard data -> reports/data.json + reports/data.js")
    return rows



def write_dashboard_data(out):
    """reports/data.json for readers of JSON, and reports/data.js for index.html: a page opened from disk (file://) may not
    fetch() its own files, so the dashboard loads the data as a script (CARD-009, 2026-09-27). Both written atomically (BOOK-001)."""
    import atomicio
    atomicio.atomic_json(os.path.join(BASE, "reports", "data.json"), out, indent=1)
    atomicio.atomic_write_text(os.path.join(BASE, "reports", "data.js"), "window.STRATEGY_LAB_DATA = " + json.dumps(out) + ";\n")

def write_kb(rows, meta):
    """Append this run's rows to knowledge_base.csv. BENCH-002: a file still on the pre-SLAB-001
    header gains the new columns - each old row keeps every recorded value byte for byte, and is
    marked gate=dsr_pbo with survey_verdict = its verdict (the label that gate gave it). An unknown
    header is refused, never guessed at. Read-modify-write under the book's lock, written beside
    and swapped in (BOOK-001)."""
    import atomicio
    path = os.path.join(BASE, "knowledge_base.csv")
    old = []
    if os.path.exists(path):
        atomicio.hold_book(path)
        with open(path, newline="") as f:
            rd = csv.DictReader(f)
            header, old = list(rd.fieldnames or []), list(rd)
        if header == KB_COLS_V1:
            for r in old:
                r.update({c: "" for c in KB_COLS if c not in r})
                r["gate"], r["survey_verdict"] = GATE_DSR_PBO, r["verdict"]
        elif header != KB_COLS:
            raise SystemExit(f"REFUSED: knowledge_base.csv has an unrecognised header {header} - "
                             "not rewriting it (BENCH-002)")
    new = [{"run_date": meta["built"][:10], **{k: r.get(k) for k in KB_COLS if k != "run_date"}}
           for r in rows]
    atomicio.atomic_csv(path, KB_COLS, old + new)


def write_report(out):
    L = [f"# Strategy Lab — honest survey", "",
         f"**Window:** {out['window']}  ·  **{out['n_tickers']} tickers**  ·  "
         f"cost {out['cost_bps']} bps/turnover  ·  built {out['built']}", "",
         f"**SPY buy-and-hold Sharpe (full window):** {out['spy_buyhold_sharpe']} - context only; "
         f"it is not a bar. The holdout gate below judges each config against its own universe.", "",
         "Each family was tested across its full parameter grid. `Deflated Sharpe` "
         "discounts the best config for how many were tried (≥0.95 = significant). "
         "`PBO` is the probability the in-sample winner underperforms out of sample "
         "(>0.5 = overfit). `OOS Sharpe` is the in-sample winner's Sharpe on the "
         "untouched last 30% of history. A real edge needs DSR high, PBO low, and a "
         "pass on the holdout gate below: excess return over its own universe above "
         "twice its standard error.", "",
         f"**Holdout gate (SLAB-001):** {out.get('holdout_gate', '')}", "",
         "| Family | Configs | Best Sharpe (IS) | Deflated Sharpe | PBO | OOS Sharpe | Retained | "
         "Verdict (DSR+PBO) | Holdout vs own universe | Survey verdict |",
         "|---|--:|--:|--:|--:|--:|--:|---|---|---|"]
    for r in out["results"]:
        hold = (f"{r['holdout_benchmark'] or '?'}: fail-closed ({r['holdout_reason']})"
                if r["holdout"] == "fail-closed" else
                f"{r['holdout_benchmark']}: {r['holdout_excess_ann']:+.1%} ± {r['holdout_se_ann']:.1%}/yr "
                f"(margin {r['holdout_margin_ann']:+.1%}) → {r['holdout']}")
        L.append(f"| {r['family']} | {r['n_configs']} | {r['best_sharpe_annual']} | "
                 f"{r['deflated_sharpe']} | {r['pbo']} | {r['oos_sharpe']} | "
                 f"{r['oos_retention']} | {r['verdict']} | {hold} | **{r['survey_verdict']}** |")
    surv = [r for r in out["results"] if r["survey_verdict"] == "survives"]
    L += ["", "## What survived", ""]
    if surv:
        for r in surv:
            L.append(f"- **{r['family']}** — best OOS config `{r['oos_best_config']}`, "
                     f"OOS Sharpe {r['oos_sharpe']} (kept {int(r['oos_retention']*100)}% of in-sample). "
                     f"Worth paper-trading forward, not betting on.")
    else:
        L.append("- Nothing cleared every gate. That is the honest, expected result for "
                 "daily strategies on liquid large-caps — the most arbitraged data there is. "
                 "The value here is the *map* of what's been ruled out, not a signal.")
    L += ["", "## Read this before believing any survivor", "",
          "The gate is working — it correctly rejected the **day-of-week** noise control "
          "(OVERFIT) and both genuinely market-neutral alpha attempts (**cross-sectional "
          "momentum** and **short-term reversal** failed out of sample). That is the signal "
          "that the machinery is honest. But the survivors carry heavy caveats:",
          "",
          "- **A long-only survivor is not alpha — it is risk-managed long equity beta.** Any "
          "edge it shows comes from sidestepping drawdowns or sitting out risky stretches, not "
          "from predicting anything. The strategies that would be true market-neutral edge are "
          "the ones that **failed**.",
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
          "## On the original sheet's idea (\"% off high\")", "",
          "The 52-week high/low family tested both directions. In this universe the "
          "**dip-buy direction won**: long-only screens that buy names deep off their high "
          "had the best OOS Sharpe (1.2–1.5), and even the market-neutral revert version "
          "(long most-off-high, short near-high) was mildly positive — while academic "
          "near-high momentum (George–Hwang) *lost money* here. So the sheet's instinct was "
          "directionally right on this data. **But** the family still failed deflation "
          "(DSR ≈ 0.47 — not significant once you count the configs tried), and this is the "
          "single result most poisoned by survivorship bias: in a universe of *today's* "
          "winners, 'buy the biggest dips' always looks brilliant because the names that "
          "dipped and never recovered were deleted from the universe before the test began. "
          "Verdict: interesting, not proven. A point-in-time universe (incl. delisted names) "
          "is the test that would make or break it.", "",
          "## What may be worth watching", "",
          "Families whose in-sample winner passed the holdout gate, whatever their DSR + PBO "
          "verdict. 'May work' means 'passed the holdout here' — it is a forward-test "
          "candidate, never a prediction:"]
    watch = [x for x in out["results"] if x["holdout"] == "pass"][:5]
    for r in watch:
        L.append(f"- {r['family']} (`{r['oos_best_config']}`): excess {r['holdout_excess_ann']:+.1%}/yr "
                 f"vs {r['holdout_benchmark']} (SE {r['holdout_se_ann']:.1%}) — {r['survey_verdict']}")
    if not watch:
        L.append("- None passed the holdout gate this run.")
    L += ["", "---", "*A research survey, not investment advice. Survivors are candidates "
          "for forward paper-trading and deeper validation, nothing more.*", ""]
    open(os.path.join(BASE, "reports", "report.md"), "w").write("\n".join(L))


if __name__ == "__main__":
    main()
