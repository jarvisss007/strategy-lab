"""AUDIT_2026-10-26_jobs item 5 (fix pass item 2): FAMILY 9's weekly run lost 15-22 names every Monday to a threaded
yfinance download inside the 13:40-13:58 job cluster, and said only "74 scoreable". value_forward.download_closes()
downloads with threads=False, retries every empty name once, and prints a BROKEN line naming any name still missing.
Offline: yfinance is a stub.

Run:  /opt/anaconda3/bin/python -m pytest -q ~/strategy-lab/tests/test_audit_20261026_value_download.py
"""
import importlib.util
import os
import sys
import types

import numpy as np
import pandas as pd

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LAB)
_spec = importlib.util.spec_from_file_location("value_forward_dl_test", os.path.join(LAB, "value_forward.py"))
V = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V)

IDX = pd.bdate_range(end="2026-10-26", periods=30)


def _frame(names, empty=()):
    df = pd.DataFrame({n: np.linspace(10, 20, len(IDX)) for n in names}, index=IDX)
    for n in empty:
        df[n] = np.nan
    return df


class Stub:
    """First call: the names in `fail_first` come back all-NaN. Later calls: the names in `fail_always` stay all-NaN."""

    def __init__(self, fail_first=(), fail_always=()):
        self.calls, self.fail_first, self.fail_always = [], set(fail_first), set(fail_always)

    def download(self, tks, **kw):
        self.calls.append((list(tks), kw))
        bad = (self.fail_first | self.fail_always) if len(self.calls) == 1 else self.fail_always
        return {"Close": _frame(list(tks), empty=[t for t in tks if t in bad])}


def test_threads_off_and_no_retry_when_complete(capsys):
    st = Stub()
    px, miss = V.download_closes(st, ["AAA", "BBB", "SPY"])
    assert miss == [] and len(st.calls) == 1
    assert st.calls[0][1].get("threads") is False
    assert "BROKEN" not in capsys.readouterr().out


def test_failed_names_retried_once_and_recovered(capsys):
    st = Stub(fail_first=["BBB", "CCC"])
    px, miss = V.download_closes(st, ["AAA", "BBB", "CCC", "SPY"])
    assert miss == []
    assert len(st.calls) == 2 and sorted(st.calls[1][0]) == ["BBB", "CCC"]
    assert st.calls[1][1].get("threads") is False
    for n in ("AAA", "BBB", "CCC", "SPY"):
        assert px[n].notna().all()
    out = capsys.readouterr().out
    assert "retry recovered 2" in out and "BROKEN" not in out


def test_name_still_missing_is_a_loud_broken_line(capsys):
    st = Stub(fail_first=["BBB"], fail_always=["CCC"])
    px, miss = V.download_closes(st, ["AAA", "BBB", "CCC", "SPY"], label="value_screen")
    assert miss == ["CCC"]
    assert len(st.calls) == 2          # one retry, never more
    out = capsys.readouterr().out
    assert "BROKEN: value_screen: 1 of 4 names have no prices after one retry" in out and "CCC" in out
    assert px["BBB"].notna().all()


def test_value_screen_uses_the_shared_downloader():
    src = open(os.path.join(LAB, "value_screen.py")).read()
    assert "download_closes(yf, names" in src and "yf.download(" not in src
    vf = open(os.path.join(LAB, "value_forward.py")).read()
    assert vf.count("yf.download(") == 1 and "threads=False" in vf     # the one call is inside download_closes
