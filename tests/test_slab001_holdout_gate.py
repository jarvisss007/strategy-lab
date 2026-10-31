"""SLAB-001 (ruled by Anupam 2026-10-31) - the survey's out-of-sample holdout is a GATE, built as PRE_REGISTRATION section 2 states the pass bar.

The defect: "survives" meant DSR >= 0.95 and PBO < 0.5 only. The 70/30 holdout was computed and shown but decided no label, while the README promised it.
The ruling: the in-sample winner's day-clustered mean excess over ITS OWN universe's buy-and-hold (SPY for SPY-only configs, the equal-weight basket for
basket configs, cash for long-short configs) must be > 2 x its standard error and > 0 after costs; no retention bar; missing or broken out-of-sample data
fails closed; `verdict` keeps its meaning (the DSR + PBO verdict, BENCH-002) and a new `gate` column records which gate judged each knowledge_base.csv row.

Offline: every price panel is synthetic and every knowledge-base write goes to a scratch directory.
Run:  /opt/anaconda3/bin/python -m pytest -q tests/test_slab001_holdout_gate.py
      LAB_UNDER_TEST=/path/to/older/lab.py ... runs the same scenarios against another lab.py (the tests are red on the pre-fix one: it calls these
      configs "survives", judges nothing against cash, and appends knowledge-base rows with no gate column)
 1 a basket config that beats SPY by more than 2 SE but not its own basket FAILS the holdout: DSR + PBO say survives, the survey says suspect
 2 a long-short config is judged against cash: its excess is its own return, it passes on a strong market it does not beat, and a retention under 0.5 decides nothing
 3 fail closed: a hole in the benchmark's prices on one out-of-sample date (a futures-only row), no price panel, a slice under 60 days, a non-finite or
   zero-variance excess, an unregistered config - each fails the gate, never passes (ann_sharpe still returns 0.0 on a broken slice; the gate never reads it)
 4 knowledge_base.csv: the pre-SLAB-001 file gains the new columns with every recorded value byte for byte, its rows marked gate=dsr_pbo; new rows carry
   gate=dsr_pbo_holdout and their verdict stays the DSR + PBO verdict even when the survey label differs; the committed file is the July record, migrated
 5 every config of every family has a registered universe (an unregistered one would fail closed)
"""
import csv
import importlib.util
import io
import os
import sys

import numpy as np
import pandas as pd
import pytest

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get("LAB_UNDER_TEST") or os.path.join(LAB, "lab.py")
_spec = importlib.util.spec_from_file_location("lab_under_test", SRC)
L = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L)

WARM = 252
OOS_DAYS = 600                      # the synthetic holdout: the last 30% of 2000 judged days
T = WARM + 2000

# the published 2026-07-07 record, exactly as committed before SLAB-001
JULY_KB = """run_date,family,n_configs,best_sharpe_annual,deflated_sharpe,pbo,min_backtest_len_years,is_sharpe,oos_sharpe,oos_retention,verdict
2026-07-07,Moving-average trend,8,1.203,1.0,0.123,1.5,1.07,1.468,1.37,survives
2026-07-07,Turn-of-month seasonality,3,1.09,0.998,0.081,0.6,1.039,1.214,1.17,survives
2026-07-07,Volatility-managed SPY,6,0.986,1.0,0.369,1.7,1.001,0.95,0.95,survives
2026-07-07,Donchian breakout,6,1.185,1.0,0.567,1.2,1.109,1.345,1.21,suspect
2026-07-07,52-week high/low,17,1.147,0.475,0.064,2.5,1.127,1.213,1.08,suspect
2026-07-07,Time-series momentum,24,1.315,0.941,0.073,2.3,1.254,1.1,0.88,suspect
2026-07-07,Cross-sectional momentum,36,0.501,0.748,0.205,18.3,0.602,0.198,0.33,suspect
2026-07-07,Short-term reversal,18,0.049,0.002,0.468,1416.2,0.325,-0.736,-2.27,suspect
2026-07-07,Day-of-week (control),5,-0.056,0.173,0.684,inf,0.138,-0.562,-4.07,OVERFIT
""".replace("\n", "\r\n")           # csv.DictWriter's line ending, as the file is written


def panel(n_days=T, mu=0.0012, mu_spy=-0.0004, seed=7):
    """A strong equal-weight basket (10 names + SPY) and a weak SPY. Returns prices, rets and the basket's buy-and-hold return."""
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2012-01-02", periods=n_days)
    common = rng.normal(0, 0.006, n_days)
    r = {f"N{i:02d}": mu + common + rng.normal(0, 0.008, n_days) for i in range(10)}
    r["SPY"] = mu_spy + rng.normal(0, 0.005, n_days)
    prices = 100 * (1 + pd.DataFrame(r, index=idx)).cumprod()
    rets = prices.pct_change()
    return prices, rets, rets.mean(axis=1).fillna(0.0)


def judge(name, series, prices=None, rets=None):
    try:
        return L.judge_family(name, series, prices=prices, rets=rets)
    except TypeError:               # the pre-fix signature takes no panel: run it anyway, so it fails on what it CALLS the config
        return L.judge_family(name, series)


def label(res):
    return res.get("survey_verdict", res["verdict"])     # what the survey calls the family; before SLAB-001 that was `verdict`


def tstat(x):
    x = np.asarray(x, float)
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))


# ------------------------------------------------------------------ 1 own universe, not SPY
def test_basket_config_that_beats_spy_but_not_its_own_basket_fails():
    prices, rets, basket = panel()
    z = np.random.default_rng(11).normal(0, 0.004, T)            # one noise path: the configs differ only in exposure
    series = {f"MAtrend basket n{n}": e * basket + z for n, e in ((50, 0.6), (100, 0.7), (150, 0.8), (200, 0.9))}
    res = judge("Moving-average trend", series, prices, rets)

    assert res["verdict"] == "survives"                           # DSR + PBO alone would publish it as a survivor
    cfg = series[res["oos_best_config"]].iloc[-OOS_DAYS:]
    assert tstat(cfg - rets["SPY"].iloc[-OOS_DAYS:]) > 2           # it beats SPY by more than 2 SE ...
    assert tstat(cfg - basket.iloc[-OOS_DAYS:]) < 2                # ... but not the basket it holds
    assert label(res) == "suspect"                                 # before SLAB-001 the survey published it as "survives"
    assert res["holdout_benchmark"] == "basket" and res["holdout"] == "fail"
    assert res["holdout_excess_ann"] == pytest.approx((cfg - basket.iloc[-OOS_DAYS:]).mean() * 252, abs=1e-4)
    assert res["verdict"] == "survives"                            # BENCH-002: the DSR + PBO verdict is still recorded as it was


# ------------------------------------------------------------------ 2 long-short vs cash
def test_long_short_config_is_judged_against_cash_and_retention_decides_nothing():
    prices, rets, basket = panel(mu=0.0030)                        # a market far stronger than the config
    rng = np.random.default_rng(5)
    idx = prices.index
    is_part = np.arange(T) < T - OOS_DAYS

    def ls(edge_is, edge_oos):
        return pd.Series(np.where(is_part, edge_is, edge_oos) + rng.normal(0, 0.003, T), index=idx)
    series = {"XSMOM L126 skip5 q0.1 H21": ls(0.0030, 0.0006),     # the in-sample winner: keeps ~20% of its Sharpe
              "XSMOM L63 skip0 q0.2 H5": ls(0.0010, 0.0006),
              "XSMOM L252 skip0 q0.3 H21": ls(0.0005, 0.0006)}
    res = judge("Cross-sectional momentum", series, prices, rets)

    assert res["oos_best_config"] == "XSMOM L126 skip5 q0.1 H21"
    assert 0 < res["oos_retention"] < 0.5                          # a retention bar would fail it; there is none
    assert res.get("holdout_benchmark") == "cash"
    oos = series[res["oos_best_config"]].iloc[-OOS_DAYS:]
    assert res["holdout_excess_ann"] == pytest.approx(oos.mean() * 252, abs=1e-4)   # vs cash the excess is the return itself
    assert res["holdout"] == "pass"
    assert tstat(oos - basket.iloc[-OOS_DAYS:]) < 0                # against the basket it would have failed


# ------------------------------------------------------------------ 3 fail closed
def spy_family(rets):
    z = np.random.default_rng(3).normal(0, 0.002, len(rets))
    spy = rets["SPY"].fillna(0.0)
    return {f"VolMgd SPY tgt{t} lb21": spy + a + z for t, a in ((10, 0.0006), (15, 0.0010), (20, 0.0014))}


def test_a_hole_in_the_benchmark_prices_fails_closed():
    prices, rets, _ = panel()
    intact = judge("Volatility-managed SPY", spy_family(rets), prices, rets)
    assert intact["verdict"] == "survives"

    holed = prices.copy()
    holed.iloc[-200, holed.columns.get_loc("SPY")] = np.nan        # one OOS date with no SPY price (a futures-only row)
    hrets = holed.pct_change(fill_method="pad")                    # pct_change pads it into a fake 0% day
    res = judge("Volatility-managed SPY", spy_family(hrets), holed, hrets)
    assert res["verdict"] == "survives"
    assert label(res) == "suspect"                                 # before SLAB-001: "survives" on a broken benchmark
    assert intact["holdout"] == "pass"                             # the same config on whole data passes ...
    assert res["holdout"] == "fail-closed"                         # ... and on the holed panel cannot
    assert "missing prices" in res["holdout_reason"]


def test_no_panel_and_a_short_slice_fail_closed():
    prices, rets, _ = panel()
    res = judge("Volatility-managed SPY", spy_family(rets))       # no panel to build the benchmark from
    assert res.get("holdout") == "fail-closed" and label(res) == "suspect"

    short_p, short_r, _ = panel(n_days=WARM + 150)                 # 45 holdout days < 60
    res = judge("Volatility-managed SPY", spy_family(short_r), short_p, short_r)
    assert res.get("holdout") == "fail-closed"
    assert "fewer than 60" in res["holdout_reason"]


def test_gate_function_fails_closed_on_broken_slices():
    g = L.holdout_gate
    good = np.full(100, 0.001) + np.random.default_rng(0).normal(0, 0.001, 100)
    assert g(good, np.zeros(100))["holdout"] == "pass"
    bench_nan = np.zeros(100); bench_nan[10] = np.nan
    assert g(good, bench_nan)["holdout"] == "fail-closed"
    assert g(good, good)["holdout"] == "fail-closed"               # zero-variance excess: SE undefined
    assert g(good + 0.01, good)["holdout"] == "fail-closed"        # a constant excess: SE undefined, never "infinitely significant"
    assert g(np.array([]), np.array([]))["holdout"] == "fail-closed"
    assert g(good, None)["holdout"] == "fail-closed"
    assert g(good, np.zeros(99))["holdout"] == "fail-closed"
    assert g(good, np.zeros(100), problem="benchmark broken")["holdout"] == "fail-closed"
    assert L.ann_sharpe(np.full(100, np.nan)) == 0.0               # the fail-open path the gate never reads
    res = L.judge_holdout("Mystery config n9", good, pd.bdate_range("2020-01-01", periods=100), None, None)
    assert res["holdout"] == "fail-closed" and "no registered universe" in res["holdout_reason"]


def test_margin_is_mean_minus_two_se():
    x = np.random.default_rng(1).normal(0.0008, 0.01, 1000)
    r = L.holdout_gate(x, np.zeros(1000))
    se = x.std(ddof=1) / np.sqrt(1000)
    assert r["holdout_excess_ann"] == pytest.approx(x.mean() * 252)
    assert r["holdout_se_ann"] == pytest.approx(se * 252)
    assert r["holdout_margin_ann"] == pytest.approx((x.mean() - 2 * se) * 252)
    assert r["holdout"] == ("pass" if x.mean() > 2 * se else "fail")


# ------------------------------------------------------------------ 4 knowledge_base.csv (BENCH-002)
def read(path):
    with open(path, newline="") as f:
        rd = csv.DictReader(f)
        return rd.fieldnames, list(rd)


def new_row(family, verdict, survey, holdout):
    return {"family": family, "n_configs": 3, "best_sharpe_annual": 1.0, "deflated_sharpe": 0.99, "pbo": 0.1,
            "min_backtest_len_years": 1.0, "is_sharpe": 1.0, "oos_sharpe": 0.9, "oos_retention": 0.9, "verdict": verdict,
            "gate": "dsr_pbo_holdout", "survey_verdict": survey, "holdout": holdout, "holdout_benchmark": "basket",
            "holdout_excess_ann": -0.02, "holdout_se_ann": 0.05, "holdout_margin_ann": -0.12, "verdict_full": "x"}


def test_knowledge_base_gains_the_gate_column_and_keeps_every_recorded_value(tmp_path, monkeypatch):
    kb = tmp_path / "knowledge_base.csv"
    kb.write_bytes(JULY_KB.encode())
    monkeypatch.setattr(L, "BASE", str(tmp_path))
    meta = {"built": "2026-10-31 13:30 PDT"}
    L.write_kb([new_row("Moving-average trend", "survives", "suspect", "fail")], meta)

    header, rows = read(kb)
    assert "gate" in header and header[:11] == JULY_KB.split("\r\n")[0].split(",")
    old_lines = JULY_KB.split("\r\n")[1:-1]
    new_lines = kb.read_bytes().decode().split("\r\n")[1:-1]
    assert len(new_lines) == len(old_lines) + 1
    for old, new in zip(old_lines, new_lines):
        assert new.startswith(old + ",")                           # every recorded value, byte for byte
    july = rows[:9]
    assert [r["verdict"] for r in july] == [l.split(",")[-1] for l in old_lines]
    assert all(r["gate"] == "dsr_pbo" and r["survey_verdict"] == r["verdict"] and r["holdout"] == "" for r in july)
    added = rows[9]
    assert added["run_date"] == "2026-10-31" and added["gate"] == "dsr_pbo_holdout"
    assert added["verdict"] == "survives" and added["survey_verdict"] == "suspect" and added["holdout"] == "fail"

    before = kb.read_bytes()                                       # a second run appends; nothing earlier moves
    L.write_kb([new_row("Donchian breakout", "suspect", "suspect", "fail")], meta)
    assert kb.read_bytes().startswith(before)


def test_knowledge_base_refuses_an_unknown_header(tmp_path, monkeypatch):
    kb = tmp_path / "knowledge_base.csv"
    kb.write_text("run_date,family,verdict,mystery\r\n2026-07-07,X,survives,1\r\n")
    monkeypatch.setattr(L, "BASE", str(tmp_path))
    with pytest.raises(SystemExit):
        L.write_kb([new_row("X", "survives", "suspect", "fail")], {"built": "2026-10-31"})
    assert kb.read_bytes().endswith(b"survives,1\r\n")


def test_committed_knowledge_base_is_the_july_record_marked_by_its_gate():
    header, rows = read(os.path.join(LAB, "knowledge_base.csv"))
    assert header == L.KB_COLS
    old_lines = JULY_KB.split("\r\n")[1:-1]
    with open(os.path.join(LAB, "knowledge_base.csv"), newline="") as f:
        lines = f.read().split("\r\n")[1:]
    for old, line in zip(old_lines, lines):
        assert line.startswith(old + ",")
    for r in rows[:9]:
        assert r["gate"] == "dsr_pbo" and r["survey_verdict"] == r["verdict"]


# ------------------------------------------------------------------ 5 every config has a universe
def test_every_config_of_every_family_has_a_registered_universe():
    rng = np.random.default_rng(2)
    n = 320
    idx = pd.bdate_range("2020-01-01", periods=n)
    cols = ["SPY"] + [f"N{i:02d}" for i in range(12)]
    prices = 100 * (1 + pd.DataFrame(rng.normal(0.0005, 0.01, (n, len(cols))), index=idx, columns=cols)).cumprod()
    rets = prices.pct_change()
    want = {"Time-series momentum": None, "Cross-sectional momentum": {"cash"}, "Short-term reversal": {"cash"},
            "52-week high/low": {"cash", "basket"}, "Moving-average trend": {"basket", "SPY"}, "Donchian breakout": {"basket"},
            "Volatility-managed SPY": {"SPY"}, "Turn-of-month seasonality": {"basket"}, "Day-of-week (control)": {"SPY"}}
    for fam, fn in L.S.FAMILIES.items():
        got = {cfg: L.S.universe_of(cfg) for cfg in fn(prices, rets)}
        assert None not in got.values(), (fam, [c for c, u in got.items() if u is None])
        if fam == "Time-series momentum":
            assert all(u == ("basket" if c.endswith(" long") else "cash") for c, u in got.items())
        else:
            assert set(got.values()) == want[fam], (fam, got)
    for cfg in ("52wHigh-mom q0.1 H5", "52wHigh-revert q0.2 H21"):
        assert L.S.universe_of(cfg) == "cash"
    for cfg in ("NearHigh-long within5pct", "DeepDip-long off19pct", "MAtrend basket n200"):
        assert L.S.universe_of(cfg) == "basket"
