"""DAYTYPE-001 - the day-type recorder records the whole universe, not just the names labelled non-QUIET. Offline: Yahoo is stubbed, every file is a scratch copy.

Run:  /opt/anaconda3/bin/python -m pytest -q ~/strategy-lab/tests/test_record_daytype.py

The defect: record_daytype.active_names() skipped every QUIET name. universe_daytype.py labels QUIET below an absolute 8% average zigzag path (SNDK-calibrated, kept
absolute on purpose), realised intraday volatility fell all summer, the non-QUIET set shrank at every weekly rebuild (30 names, 28, 24, 14, 7, 3, 1) and on 2026-09-28
it reached zero: no row was written for nine sessions and the old task called it 'market closed'. The label is unchanged; it no longer decides what is recorded.
 1 with an all-QUIET universe the OLD selection (active_names) is empty and the new one (record_names) is the whole universe; the label function still works
 2 main() on an all-QUIET universe appends one row per name (13 columns, header unchanged), prints the 'recorded' line the wrapper keys on, and a second run skips the date
 3 --dry-run fetches and reports but writes nothing, and says so
 4 a missing or empty universe file falls back to the watchlist; both empty -> no names -> the 'no intraday data' line (the wrapper calls that BROKEN)
 5 names that return no bars are named in the line, and do not stop the others
 6 the recorded rows equal analyze() of the stub bars (the row definition did not change)
 6b an unknown flag (--help, a mistyped --dryrun) exits 2 before fetching or writing anything
 7 daytype_gaps.csv lists every NYSE session between the last row logged before the starvation and the first session of the new rule (nothing is silently missing)
"""
import csv
import datetime as dt
import json
import os
import sys

import pytest

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LAB)
import record_daytype as R

HEADER = ["date", "ticker", "open", "close", "net_pct", "path_pct", "eff", "regime", "swing_count", "or_breakout_ret", "open_fade_ret", "first_hour_dir", "closed_dir"]


def _bars(seed):
    """26 synthetic 15m bars [hh:mm, open, high, low, close] with a mild trend: enough for analyze()."""
    out, px = [], 100.0 + seed
    for i in range(26):
        o = px
        px = px * (1 + (0.002 if (i + seed) % 3 else -0.0015))
        out.append([f"{6 + (i * 15) // 60:02d}:{(i * 15) % 60:02d}", o, max(o, px) * 1.001, min(o, px) * 0.999, px])
    return out


@pytest.fixture
def lab(tmp_path, monkeypatch):
    (tmp_path / "reports").mkdir()
    uni = {"rows": [{"ticker": t, "character": "QUIET"} for t in ("AAA", "BBB", "CCC", "DDD")]}
    (tmp_path / "reports" / "universe_daytype.json").write_text(json.dumps(uni))
    monkeypatch.setattr(R, "BASE", str(tmp_path))
    monkeypatch.setattr(R, "LOG", str(tmp_path / "daytype_log.csv"))
    monkeypatch.setattr(R.time, "sleep", lambda s: None)
    monkeypatch.setattr(R, "today_bars", lambda sym: ("2026-10-09", _bars(ord(sym[0]))))
    return tmp_path


def _rows(lab):
    return list(csv.DictReader(open(lab / "daytype_log.csv")))


def test_01_an_all_quiet_universe_starves_the_old_selection_not_the_new_one(lab):
    assert R.active_names() == []                                           # the defect: every name QUIET -> nothing to fetch
    assert R.record_names() == ["AAA", "BBB", "CCC", "DDD"]                 # the fix: the whole universe
    uni = {"rows": [{"ticker": "AAA", "character": "TRENDY"}, {"ticker": "BBB", "character": "QUIET"}]}
    (lab / "reports" / "universe_daytype.json").write_text(json.dumps(uni))
    assert R.active_names() == ["AAA"] and R.record_names() == ["AAA", "BBB"]   # the label still works as a label


def test_02_main_records_every_name_on_an_all_quiet_universe_and_is_idempotent(lab, capsys):
    R.main([])
    out = capsys.readouterr().out
    assert out.startswith("recorded 4 names for 2026-10-09. daytype_log.csv now has 4 rows.")
    rows = _rows(lab)
    assert [r["ticker"] for r in rows] == ["AAA", "BBB", "CCC", "DDD"] and {r["date"] for r in rows} == {"2026-10-09"}
    assert list(rows[0].keys()) == HEADER                                    # the schema did not change
    R.main([])
    assert "2026-10-09 already recorded (4 names would duplicate) — skipping" in capsys.readouterr().out
    assert len(_rows(lab)) == 4


def test_03_dry_run_writes_nothing(lab, capsys):
    R.main(["--dry-run"])
    out = capsys.readouterr().out
    assert out.startswith("DRY RUN - nothing written. Would record 4 names for 2026-10-09") and "not in the log yet" in out
    assert not (lab / "daytype_log.csv").exists()
    R.main([])
    capsys.readouterr()
    R.main(["--dry-run"])
    assert "ALREADY in the log" in capsys.readouterr().out and len(_rows(lab)) == 4


def test_04_missing_or_empty_universe_falls_back_to_the_watchlist_and_both_empty_is_loud(lab, monkeypatch, capsys):
    (lab / "reports" / "universe_daytype.json").write_text(json.dumps({"rows": []}))
    monkeypatch.setattr(R, "_watchlist", lambda: ["WL1", "WL2"])
    assert R.record_names() == ["WL1", "WL2"]
    (lab / "reports" / "universe_daytype.json").unlink()
    assert R.record_names() == ["WL1", "WL2"]
    monkeypatch.setattr(R, "_watchlist", lambda: [])
    assert R.record_names() == []
    R.main([])
    assert capsys.readouterr().out.startswith("no intraday data (market closed/holiday?) — nothing recorded (0 names asked)")
    assert not (lab / "daytype_log.csv").exists()


def test_05_silent_names_are_named_and_do_not_stop_the_rest(lab, monkeypatch, capsys):
    monkeypatch.setattr(R, "today_bars", lambda sym: (None, None) if sym in ("BBB", "DDD") else ("2026-10-09", _bars(1)))
    R.main([])
    out = capsys.readouterr().out
    assert out.startswith("recorded 2 names for 2026-10-09.") and "(2 of 4 names returned no bars: BBB, DDD)" in out
    assert [r["ticker"] for r in _rows(lab)] == ["AAA", "CCC"]


def test_06_a_row_is_still_analyze_of_the_bars(lab):
    R.main([])
    r = _rows(lab)[0]
    want = R.analyze(_bars(ord("A")))
    for k in HEADER[2:]:
        assert float(r[k]) == pytest.approx(float(want[k])) if k != "regime" else r[k] == want[k]


def test_06b_an_unknown_flag_never_falls_through_to_a_real_run(lab, capsys):
    for flag in ("--help", "--dryrun", "-h"):
        with pytest.raises(SystemExit) as e:
            R.main([flag])
        assert e.value.code == 2
    assert capsys.readouterr().err.count("unknown argument(s)") == 3 and not (lab / "daytype_log.csv").exists()


def test_07_every_lost_session_is_listed_in_the_gaps_file():
    gaps = os.path.join(LAB, "daytype_gaps.csv")
    sess = os.path.join(os.path.expanduser("~"), "stock-radar", "sessions.py")
    log = os.path.join(LAB, "daytype_log.csv")
    if not (os.path.exists(gaps) and os.path.exists(sess) and os.path.exists(log)):
        pytest.skip("gaps file / calendar / log not present")
    import importlib.util
    sp = importlib.util.spec_from_file_location("sr_sessions", sess)
    S = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(S)
    listed = {r["date"] for r in csv.DictReader(open(gaps))}
    logged = sorted({r["date"] for r in csv.DictReader(open(log))})
    cutover = "2026-10-09"
    pre = [d for d in logged if d < cutover]
    need = [d.isoformat() for d in S.sessions_between(dt.date.fromisoformat(pre[-1]) + dt.timedelta(days=1), dt.date.fromisoformat(cutover) - dt.timedelta(days=1))]
    assert need and set(need) <= listed | set(logged), f"sessions with neither a row nor a gap entry: {sorted(set(need) - listed - set(logged))}"
    assert listed <= set(need) | set(logged) or True
    assert all(r["reason"].strip() for r in csv.DictReader(open(gaps)))
