"""VAL-002 (+ AUDIT-013 item 5c) - FAMILY 9's forward book advances past a quarter that opens nothing, ages its 6-month exit from the formation quarter, and never prices
off a forward-filled bar. Offline: yfinance and the signal function are stubbed, every file is a scratch copy.

Run:  /opt/anaconda3/bin/python -m pytest -q ~/strategy-lab/tests/test_value_forward_val002.py
      VF_UNDER_TEST=/path/to/older/value_forward.py ... runs the same scenarios against another version of the file (the tests are red on the pre-fix one)

The defects (found by the 2026-10-02 audit): (1) a quarter counted as done only if a row named it, so a quarter with no qualifying name stayed due[0] for ever and every later
quarter, and every exit review, queued behind it; (2) age_m counted from the FILL month, so a 2026-12-31 formation filled 2027-01-04 exited after 9 months, not 6;
(5c) last_close = px.ffill().iloc[-1] priced a fill or an exit at an OLDER close when a name had no bar on the last day.
 1 a zero-pick quarter is recorded as processed and the next quarter is reviewed on the next run (the 2026-09-30 rows exit at the 2027-03-31 review: 6 months)
 2 the 6-month exit counts from the formation quarter: formed 2026-12-31, filled 2027-01-04 -> exits at the 2027-06-30 review
 3 a name with no bar on the last settled day is DEFERRED - never filled or exited at an older close - and its quarter stays due until it prints; after 28 days the quarter is
   closed with the refusal recorded
 4 BENCH-002: with nothing due the book file is byte-identical and the processed quarters are seeded from what the book evidences; the age rule agrees with the old one for every
   row filled in its formation month (all rows in the live book), at every future review
 5 a stale mark is labelled with its own date; SPY with no close at all defers the whole run
"""
import csv
import datetime as dt
import importlib.util
import json
import os
import sys
import types

import numpy as np
import pandas as pd
import pytest

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LAB)
SRC = os.environ.get("VF_UNDER_TEST") or os.path.join(LAB, "value_forward.py")
_spec = importlib.util.spec_from_file_location("value_forward_under_test", SRC)
V = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V)

D = dt.date
COLS = V.COLS


def _row(tk, q="2026-09-30", opened=None, px="100.00", spy="700.00", **kw):
    r = {"opened": opened or q, "ticker": tk, "entry_px": px, "shares": "20.0000", "spy_at_entry": spy, "review_after": "", "exited": "", "exit_px": "", "spy_at_exit": "",
         "net_pct": "", "excess_pct": "", "exit_reason": "",
         "note": f"formation {q} (filled {opened or q}, last settled close); rule frozen D<=20 F>=6 H=6m"}
    r.update(kw)
    return r


def _prices(last_day, names, nan=(), spy_nan=False, stale_from=None):
    """Daily closes for `names` + SPY ending `last_day` (a weekday): a gently rising ramp; names in `nan` have no bar ON last_day (NaN)."""
    idx = pd.bdate_range(end=pd.Timestamp(last_day), periods=60)
    df = pd.DataFrame({n: np.linspace(50, 60, len(idx)) for n in names}, index=idx)
    df["SPY"] = np.linspace(700, 720, len(idx))
    for n in nan:
        df.loc[idx[-1], n] = np.nan
    if spy_nan:
        df["SPY"] = np.nan
    return df


class Fixture:
    def __init__(self, tmp_path, monkeypatch):
        self.tmp, self.mp = tmp_path, monkeypatch
        (tmp_path / "reports").mkdir(exist_ok=True)
        self.book, self.state = str(tmp_path / "reports" / "value_book.csv"), str(tmp_path / "reports" / "value_state.json")
        monkeypatch.setattr(V, "BOOK", self.book)
        monkeypatch.setattr(V, "STATE", self.state)
        monkeypatch.setattr(V, "load_panel", lambda: {})
        monkeypatch.setattr(sys, "argv", ["value_forward.py"])

    def write_book(self, rows):
        with open(self.book, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS)
            w.writeheader()
            for r in rows:
                w.writerow({c: r.get(c, "") for c in COLS})

    def write_state(self, **kw):
        json.dump(kw, open(self.state, "w"))

    def run(self, today, prices, sig):
        """sig: {tk: (ratio, pctile, fscore)} returned for ANY date, or a callable(when) -> that dict."""
        names = [c for c in prices.columns if c != "SPY"]
        self.mp.setattr(V, "load_panel", lambda: {n: [] for n in names})
        self.mp.setattr(V, "ratios_and_f", lambda panel, nm, when, mraw: (sig(when) if callable(sig) else sig))
        self.mp.setitem(sys.modules, "yfinance", types.SimpleNamespace(download=lambda *a, **k: {"Close": prices.copy()}))
        V.main(today=today) if "today" in V.main.__code__.co_varnames[:V.main.__code__.co_argcount] else self._old_main(today)
        return self

    def _old_main(self, today):                      # the pre-fix main() takes no argument and reads dt.date.today()
        real = V.dt
        class FakeDate(dt.date):
            @classmethod
            def today(cls):
                return today
        self.mp.setattr(V, "dt", types.SimpleNamespace(date=FakeDate, timedelta=dt.timedelta, datetime=dt.datetime))
        V.main()

    def rows(self):
        return list(csv.DictReader(open(self.book)))

    def st(self):
        return json.load(open(self.state))


@pytest.fixture
def fx(tmp_path, monkeypatch):
    return Fixture(tmp_path, monkeypatch)


def _live_book_rows():
    return [_row(t) for t in ("LIN", "MOH", "NKE", "PEP", "TXT", "UNH")]


# ---------------------------------------------------------------- 1
def test_01_a_zero_pick_quarter_is_processed_and_the_next_review_happens(fx, capsys):
    names = ["LIN", "MOH", "NKE", "PEP", "TXT", "UNH", "AAA"]
    fx.write_book(_live_book_rows())
    low = {n: (10.0, 30.0, 7) for n in names}                    # everything sits at the 30th percentile: nothing qualifies (pct > 20), nothing exits (pct <= 50)
    fx.run(D(2027, 1, 5), _prices(D(2027, 1, 4), names), low)    # the 2026-12-31 quarter: due, forms nothing
    assert len(fx.rows()) == 6 and all(not r["exited"] for r in fx.rows())
    fx.run(D(2027, 4, 5), _prices(D(2027, 4, 5), names), low)    # the NEXT run must review 2027-03-31 (the old code re-took 2026-12-31 for ever)
    got = fx.rows()
    assert all(r["exited"] and r["exit_reason"] == "held 6m >= 6m" for r in got), [r["exit_reason"] for r in got]      # BEHAVIOUR first: the review happened
    assert fx.st()["processed_quarters"] == ["2026-09-30", "2026-12-31", "2027-03-31"], "a quarter that opened nothing must still be recorded as processed"


# ---------------------------------------------------------------- 2
def test_02_the_six_month_exit_counts_from_the_formation_quarter_not_the_fill_month(fx):
    names = ["AAA", "BBB"]
    r = _row("AAA", q="2026-12-31", opened="2027-01-04")              # formed at the 12-31 quarter-end, filled on the first Monday of January
    fx.write_book([r])
    fx.write_state(processed_quarters=["2026-09-30", "2026-12-31", "2027-03-31"])
    fx.run(D(2027, 7, 6), _prices(D(2027, 7, 6), names), {"AAA": (10.0, 10.0, 7)})           # review 2027-06-30: 6 months after the FORMATION quarter
    got = fx.rows()[0]
    assert got["exited"] and got["exit_reason"] == "held 6m >= 6m", got["exit_reason"]       # the old rule counted from the fill month and saw 5 months


# ---------------------------------------------------------------- 3
def test_03_a_name_with_no_bar_on_the_last_day_is_deferred_never_priced_at_an_older_close(fx):
    names = ["AAA", "XXX"]
    fx.write_book([])
    fx.write_state(processed_quarters=["2026-09-30"])
    sig = {"AAA": (5.0, 10.0, 8), "XXX": (5.0, 5.0, 8)}                                     # both qualify
    fx.run(D(2027, 1, 5), _prices(D(2027, 1, 4), names, nan=["XXX"]), sig)                  # XXX has no bar on 2027-01-04
    rows = fx.rows()
    assert [r["ticker"] for r in rows] == ["AAA"], "XXX must not be filled at an older close"
    s = fx.st()
    assert "2026-12-31" not in s["processed_quarters"] and s["deferred"] == ["fill XXX"]
    fx.run(D(2027, 1, 12), _prices(D(2027, 1, 11), names), sig)                             # the bar prints a week later: the deferred fill happens, once
    assert sorted(r["ticker"] for r in fx.rows()) == ["AAA", "XXX"]
    assert "2026-12-31" in fx.st()["processed_quarters"] and fx.st()["deferred"] == []
    assert sum(1 for r in fx.rows() if r["ticker"] == "AAA") == 1                           # AAA was not formed twice
    # an exit with no bar is deferred too
    fx.write_book([_row("YYY", q="2026-09-30")])
    fx.write_state(processed_quarters=["2026-09-30", "2026-12-31"])
    fx.run(D(2027, 4, 5), _prices(D(2027, 4, 5), ["YYY", "AAA"], nan=["YYY"]), {"YYY": (10.0, 10.0, 7)})
    assert not fx.rows()[0]["exited"] and fx.st()["deferred"] == ["exit YYY"] and "2027-03-31" not in fx.st()["processed_quarters"]


def test_03b_a_quarter_stuck_for_28_days_is_closed_and_the_refusal_is_recorded(fx):
    names = ["AAA", "XXX"]
    fx.write_book([])
    fx.write_state(processed_quarters=["2026-09-30"])
    sig = {"XXX": (5.0, 5.0, 8)}
    fx.run(D(2027, 1, 25), _prices(D(2027, 1, 22), names, nan=["XXX"]), sig)                # 25 days after the quarter-end: still retried
    assert "2026-12-31" not in fx.st()["processed_quarters"]
    fx.run(D(2027, 2, 2), _prices(D(2027, 1, 29), names, nan=["XXX"]), sig)                 # 33 days: closed, said so
    s = fx.st()
    assert "2026-12-31" in s["processed_quarters"] and s["refused"] == {"2026-12-31": ["fill XXX"]} and fx.rows() == []


# ---------------------------------------------------------------- 4
def test_04_nothing_due_leaves_the_book_byte_identical_and_seeds_the_processed_quarters(fx):
    fx.write_book(_live_book_rows())
    before = open(fx.book, "rb").read()
    names = ["LIN", "MOH", "NKE", "PEP", "TXT", "UNH"]
    fx.run(D(2026, 10, 8), _prices(D(2026, 10, 8), names), {})                              # 2026-12-31 is not due yet
    assert open(fx.book, "rb").read() == before
    assert fx.st()["processed_quarters"] == ["2026-09-30"]                                  # seeded from the six rows that name it
    assert fx.st()["open_n"] == 6


def test_04b_the_age_rule_agrees_with_the_old_one_for_rows_filled_in_their_formation_month():
    path = os.path.join(LAB, "reports", "value_book.csv")
    if not os.path.exists(path):
        pytest.skip("no live book")
    rows = [r for r in csv.DictReader(open(path)) if r["note"].startswith("formation ")]
    same = [r for r in rows if r["opened"][:7] == V._FORM_Q.search(r["note"]).group(1)[:7]]
    assert same, "no row of the live book was filled in its formation month"
    old = lambda r, q: (q.year - dt.date.fromisoformat(r["opened"]).year) * 12 + (q.month - dt.date.fromisoformat(r["opened"]).month)
    for r in same:
        for q in V.quarter_ends(D(2032, 12, 31)):
            assert V.age_months(r, q) == old(r, q), (r["ticker"], q)


def test_04c_a_book_with_no_state_seeds_only_what_the_rows_evidence(fx):
    assert V.processed_from_rows([]) == set()
    assert V.processed_from_rows([_row("A", q="2026-09-30"), _row("B", q="2026-12-31", opened="2027-01-04")]) == {"2026-09-30", "2026-12-31"}


# ---------------------------------------------------------------- 5
def test_05_a_stale_mark_carries_its_own_date_and_spy_with_no_close_defers_the_run(fx, capsys):
    fx.write_book([_row("AAA"), _row("BBB")])
    fx.write_state(processed_quarters=["2026-09-30"])
    px = _prices(D(2026, 10, 8), ["AAA", "BBB"], nan=["BBB"])
    fx.run(D(2026, 10, 8), px, {})
    marks = {m["ticker"]: m for m in fx.st()["open"]}
    assert "asof" not in marks["AAA"] and marks["BBB"]["asof"] == str(px["BBB"].dropna().index[-1].date())
    fx.write_book([_row("AAA")])
    before = open(fx.book, "rb").read()
    fx.run(D(2027, 1, 5), _prices(D(2027, 1, 4), ["AAA"], spy_nan=True), {"AAA": (10, 10, 7)})
    assert "DEFER - SPY has no close at all" in capsys.readouterr().out and open(fx.book, "rb").read() == before
