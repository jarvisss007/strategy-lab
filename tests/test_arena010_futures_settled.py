"""ARENA-010 / ARENA-011 (built 2026-11-04): the Arena prices futures only on settled bars.

The defect: arena.py read the last bar of every radar.json series, and for ES=F / NQ=F that bar is the live Globex session at the
06:10 PT sweep, so exits and entries were written at prints that are not the settled close (25 rows by 11-04). The fix cuts a
futures series at radar.json's settled_bar (arena.settled_only) and auto_reconcile.feed() reconciles a futures fill only onto a
settled bar. Upstream, stock-radar collector.py now dates settled_bar in UTC like series_t (it used local PT, one day behind).

What these pin:
  * a futures series ends at settled_bar; a live bar after it is never read; equities are untouched;
  * no settled_bar means no futures bar at all (fail closed), and main() names those tickers on its run line;
  * auto_reconcile's feed drops unsettled futures bars, so it can never "repair" a fill onto a live print;
  * on the live radar.json, no futures series kept by settled_only ends after its own settled_bar.
Run: /opt/anaconda3/bin/python -m pytest -q tests/test_arena010_futures_settled.py
"""
import datetime as dt
import json
import os
import sys

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LAB)
import arena
import auto_reconcile


def D(iso):
    return (dt.date.fromisoformat(iso) - arena.DAY0).days


def fut(ticker="ES=F", settled="2026-11-03"):
    return {"ticker": ticker, "settled_bar": settled,
            "series_t": [D("2026-11-02"), D("2026-11-03"), D("2026-11-04")], "series_c": [7570.0, 7596.75, 7612.0]}


def test_futures_series_ends_at_settled_bar():
    s = arena.settled_only(fut())
    assert [arena.d2iso(t) for t in s["series_t"]] == ["2026-11-02", "2026-11-03"]
    assert s["series_c"] == [7570.0, 7596.75]          # the live 7612.0 print is never read


def test_settled_last_bar_is_kept():
    s = arena.settled_only(fut(settled="2026-11-04"))
    assert s["series_c"][-1] == 7612.0


def test_equities_untouched():
    e = {**fut("AAPL", settled="2026-11-03")}
    assert arena.settled_only(e) is e


def test_missing_settled_bar_fails_closed():
    s = arena.settled_only(fut(settled=""))
    assert s["series_t"] == [] and s["series_c"] == []


def test_main_names_unsettled_futures():
    src = open(arena.__file__).read()
    assert "map(settled_only, radar[\"equities\"])" in src
    assert "futures not traded this run" in src


def test_auto_reconcile_feed_drops_unsettled_futures(tmp_path, monkeypatch):
    p = tmp_path / "radar.json"
    p.write_text(json.dumps({"equities": [fut(), {**fut("AAPL", settled="2026-11-04")}], "strip": []}))
    monkeypatch.setattr(auto_reconcile, "RADAR", str(p))
    by_iso, by_t, _, _ = auto_reconcile.feed()
    assert max(by_iso["ES=F"]) == "2026-11-03"
    assert max(by_iso["AAPL"]) == "2026-11-04"


def test_live_radar_futures_never_past_settled_bar():
    radar = json.load(open(arena.RADAR))
    for e in radar["equities"]:
        if e["ticker"].endswith("=F") and e.get("settled_bar"):
            s = arena.settled_only(e)
            assert not s["series_t"] or arena.d2iso(s["series_t"][-1]) <= e["settled_bar"]
