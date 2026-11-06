"""ARENA-012 / ARENA-014 (built 2026-11-05): a position voided while open keeps its reason when it closes.

/void-row (11-04) gave the three open futures positions a reason row in reports/arena_voids.csv with a blank exit_date. The void
tag rides into the closed row, but that row keys to (strategy, ticker, entry_date, exit_date), so PULLBACK_50 ES=F 10-29 -> 11-05
closed with no reason on file. arena.close_voids() fills the exit into the open-row reason when the position closes.

What these pin:
  * a void-tagged close fills exit_date, exit_px_recorded and net_recorded on its open-row reason and notes it in evidence;
  * an un-voided close, and a reason that already has an exit, are left alone; a second call fills nothing;
  * main() calls close_voids right after it writes arena_trades.csv.
Run: /opt/anaconda3/bin/python -m pytest -q tests/test_arena014_void_close.py
"""
import csv
import os
import sys

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LAB)
import arena

COLS = ["strategy", "ticker", "entry_date", "exit_date", "exit_px_recorded", "net_recorded", "settled_close_exit_date",
        "voided_on", "reason", "evidence", "register_row", "ruled_by"]


def reason(strategy, ticker, entry, exit_date="", px="", net=""):
    return {"strategy": strategy, "ticker": ticker, "entry_date": entry, "exit_date": exit_date, "exit_px_recorded": px,
            "net_recorded": net, "settled_close_exit_date": "", "voided_on": "2026-11-04", "reason": "r",
            "evidence": "e.", "register_row": "ARENA-011", "ruled_by": "Anupam"}


def book(tmp_path, monkeypatch, rows):
    p = tmp_path / "arena_voids.csv"
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(rows)
    monkeypatch.setattr(arena, "VOIDS_F", str(p))
    return p


def read(p):
    return list(csv.DictReader(open(p, newline="")))


def test_void_close_fills_open_reason(tmp_path, monkeypatch):
    p = book(tmp_path, monkeypatch, [reason("PULLBACK_50", "ES=F", "2026-10-29"),
                                     reason("RSI2_DIP", "ES=F", "2026-10-08", "2026-10-13", "7853.75", "0.001")])
    closed = [{"strategy": "PULLBACK_50", "ticker": "ES=F", "entry_date": "2026-10-29", "exit_date": "2026-11-05",
               "exit_px": 7370.75, "net": -0.05265, "tags": "void"}]
    assert arena.close_voids(closed, by="test") == 1
    r = read(p)
    assert (r[0]["exit_date"], r[0]["exit_px_recorded"], r[0]["net_recorded"]) == ("2026-11-05", "7370.75", "-0.05265")
    assert r[0]["evidence"].startswith("e. CLOSED 2026-11-05 at 7370.75") and "by test" in r[0]["evidence"]
    assert r[1] == reason("RSI2_DIP", "ES=F", "2026-10-08", "2026-10-13", "7853.75", "0.001")
    assert arena.close_voids(closed) == 0                      # already filled: idempotent


def test_unvoided_close_touches_nothing(tmp_path, monkeypatch):
    p = book(tmp_path, monkeypatch, [reason("TREND_RIDER", "NQ=F", "2026-10-28")])
    before = p.read_bytes()
    closed = [{"strategy": "TREND_RIDER", "ticker": "NQ=F", "entry_date": "2026-10-28", "exit_date": "2026-11-06",
               "exit_px": 1.0, "net": 0.0, "tags": "tech"}]
    assert arena.close_voids(closed) == 0
    assert p.read_bytes() == before


def test_main_calls_close_voids_after_trades_write():
    src = open(arena.__file__).read()
    assert "atomic_csv(TRADES_F, cols, out_rows, extrasaction=\"ignore\")\n    close_voids(closed_now)" in src
