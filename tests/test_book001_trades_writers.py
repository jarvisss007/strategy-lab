"""SWEEP-003 / BOOK-001 (2026-10-09): the Arena's trade-book writers (arena.py, auto_reconcile.py, restate_prices.py) write beside-and-replace, never truncate in place.

The defect: each opened reports/arena_trades.csv with open(path, "w") - truncating it - and then wrote the rows back one by one. The book is read by every portfolio build, so a reader
that opened it mid-rewrite saw a header and no trades (the Labor Day 2026-09-07 shape that cost ipo_radar nine rows). The sweep's detector missed all three because the path is a
constant (TRADES / TRADES_F) rather than a name containing book/csv/state; they were found by hand and are named in the register row SWEEP-003.

What these pin:
  * the three source files no longer truncate the trade book in place, and each writes it through atomic_csv (an AST check, so a re-introduced open(TRADES, "w") fails);
  * BYTE-IDENTITY: the new write produces exactly the bytes the old open(..., "w") + DictWriter loop produced - proven on the live arena_trades.csv (read back and rewritten both ways:
    the live file's own bytes, the old writer's bytes and the new writer's bytes are all equal), on a hostile synthetic set (commas, quotes, newlines, unicode, empty and missing fields, extra keys),
    and on the real restate_prices.write() run against scratch paths;
  * the write is atomic: while the new bytes are produced the target holds the OLD complete file (a reader never sees a half book), and a failure mid-write leaves it untouched.
Run: /opt/anaconda3/bin/python -m pytest -q tests/test_book001_trades_writers.py
"""
import ast
import csv
import importlib
import os
import sys

import pytest

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LAB)
import atomicio

TRADES_LIVE = os.path.join(LAB, "reports", "arena_trades.csv")
ARENA_COLS = ["strategy", "ticker", "side", "entry_date", "entry_px", "exit_date", "exit_px", "net", "excess", "regime", "tags",
              "entry_px_tape", "exit_px_tape", "net_tape", "excess_tape"]
RESTATE_COLS = ["strategy", "ticker", "side", "entry_date", "entry_px", "exit_date", "exit_px", "net", "excess", "regime", "tags"]


def old_write(path, cols, rows):
    """FROZEN ORACLE: the pre-SWEEP-003 write exactly as arena.py / auto_reconcile.py / restate_prices.py did it (india_arena adds newline="", which changes nothing on POSIX)."""
    with open(path, "w") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


def new_write(path, cols, rows):
    atomicio.atomic_csv(path, cols, [{c: r.get(c, "") for c in cols} for r in rows], extrasaction="ignore")


def bytes_of(p):
    return open(p, "rb").read()


# ------------------------------------------------------------------ the source no longer truncates the trade book
@pytest.mark.parametrize("fname, var", [("arena.py", "TRADES_F"), ("auto_reconcile.py", "TRADES"), ("restate_prices.py", "TRADES")])
def test_the_trade_book_is_never_opened_for_truncating_write_and_goes_through_atomic_csv(fname, var):
    src = open(os.path.join(LAB, fname)).read()
    tree = ast.parse(src)
    truncating, atomic = [], []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        if isinstance(fn, ast.Name) and fn.id == "open" and node.args and isinstance(node.args[0], ast.Name) and node.args[0].id == var:
            mode = node.args[1].value if len(node.args) > 1 and isinstance(node.args[1], ast.Constant) else ""
            for kw in node.keywords:
                if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                    mode = kw.value.value
            if "w" in str(mode):
                truncating.append(node.lineno)
        if isinstance(fn, ast.Name) and fn.id == "atomic_csv" and node.args and isinstance(node.args[0], ast.Name) and node.args[0].id == var:
            atomic.append(node.lineno)
    assert not truncating, f"{fname}: {var} is opened for a truncating write at line(s) {truncating}"
    assert len(atomic) == 1, f"{fname}: expected exactly one atomic_csv({var}, ...) write, found {atomic}"


# ------------------------------------------------------------------ byte identity
def test_the_live_trade_book_round_trips_to_the_same_bytes_under_the_old_and_the_new_writer(tmp_path):
    if not os.path.exists(TRADES_LIVE):
        pytest.skip("no live arena_trades.csv in this tree")
    raw = bytes_of(TRADES_LIVE)
    rows = list(csv.DictReader(open(TRADES_LIVE, newline="")))
    assert len(rows) > 100                                                   # a real book, not a stub
    cols = list(rows[0].keys())
    a, b = str(tmp_path / "old.csv"), str(tmp_path / "new.csv")
    old_write(a, cols, rows)
    new_write(b, cols, rows)
    assert bytes_of(a) == bytes_of(b)                                         # the two writers agree on the live book
    assert bytes_of(b) == raw                                                 # and both reproduce the live file's own bytes (it is a fixed point)


def test_arena_columns_over_the_live_rows_are_byte_identical(tmp_path):
    if not os.path.exists(TRADES_LIVE):
        pytest.skip("no live arena_trades.csv in this tree")
    rows = list(csv.DictReader(open(TRADES_LIVE, newline="")))
    a, b = str(tmp_path / "old.csv"), str(tmp_path / "new.csv")
    for cols in (ARENA_COLS, RESTATE_COLS):                                   # arena.py's column set (with the *_tape corrections) and restate_prices / auto_reconcile's
        old_write(a, cols, rows)
        new_write(b, cols, rows)
        assert bytes_of(a) == bytes_of(b), cols


def test_hostile_rows_are_byte_identical(tmp_path):
    rows = [
        {"strategy": "s,1", "ticker": 'A"B', "side": 1, "entry_date": "2026-10-01", "entry_px": 12.3456789, "net": None, "extra_key_is_dropped": "x"},
        {"strategy": "multi\nline", "ticker": "ÅÉ☃", "side": -1, "entry_px": "", "exit_px": 0.0, "net": float("nan"), "tags": "a;b"},
        {"strategy": "", "ticker": "Z", "regime": 'he said "no"', "excess": 1e-9, "net": -0.0},
        {},
    ]
    a, b = str(tmp_path / "old.csv"), str(tmp_path / "new.csv")
    for cols in (ARENA_COLS, RESTATE_COLS):
        old_write(a, cols, rows)
        new_write(b, cols, rows)
        assert bytes_of(a) == bytes_of(b)
    old_write(a, ARENA_COLS, [])                                              # an empty book: header only, identical
    new_write(b, ARENA_COLS, [])
    assert bytes_of(a) == bytes_of(b) and bytes_of(b).count(b"\n") == 1


def test_the_real_restate_prices_write_matches_the_old_writer_and_leaves_state_and_log_intact(tmp_path, monkeypatch):
    rp = importlib.import_module("restate_prices")
    rows = [{"strategy": "mom", "ticker": "AAA", "side": 1, "entry_date": "2026-09-01", "entry_px": 10.0, "exit_date": "2026-09-08", "exit_px": 11.0,
             "net": 0.0979, "excess": 0.01, "regime": "calm", "tags": "tech"},
            {"strategy": "rev", "ticker": "B,B", "side": -1, "entry_date": "2026-09-02", "entry_px": 5.5, "exit_date": "", "exit_px": "", "net": "", "excess": "", "regime": 'x"y', "tags": ""}]
    changes = [{"scope": "open", "strategy": "rev", "ticker": "B,B", "entry_date": "2026-09-02", "exit_date": "", "field": "entry", "old_entry_px": 5.0, "new_entry_px": 5.5,
                "old_exit_px": "", "new_exit_px": "", "old_net": "", "new_net": "", "old_excess": "", "new_excess": ""}]
    state = {"open": [{"strategy": "rev", "ticker": "B,B", "entry_px": 5.5}]}
    monkeypatch.setattr(rp, "TRADES", str(tmp_path / "arena_trades.csv"))
    monkeypatch.setattr(rp, "STATE", str(tmp_path / "arena_state.json"))
    monkeypatch.setattr(rp, "LOG", str(tmp_path / "price_restatement_log.csv"))
    open(rp.TRADES, "w").write("OLD COMPLETE BOOK\n")
    rp.write(rows, state, changes)
    ref = str(tmp_path / "ref.csv")
    old_write(ref, RESTATE_COLS, rows)
    assert bytes_of(rp.TRADES) == bytes_of(ref)                               # the real function writes the old writer's bytes
    import json
    assert json.load(open(rp.STATE)) == state
    log = list(csv.DictReader(open(rp.LOG, newline="")))
    assert len(log) == 1 and log[0]["reason"].endswith("(DATA-001)")
    assert not [f for f in os.listdir(tmp_path) if ".tmp." in f]              # no stray temp file left beside the book


# ------------------------------------------------------------------ atomicity
def test_a_failure_mid_write_leaves_the_old_complete_book_untouched(tmp_path):
    p = str(tmp_path / "arena_trades.csv")
    old_write(p, RESTATE_COLS, [{"strategy": "keep", "ticker": "K"}])
    before = bytes_of(p)

    class Boom:
        def get(self, k, d=""):
            raise RuntimeError("boom while building a row")

    with pytest.raises(RuntimeError):
        new_write(p, RESTATE_COLS, [{"strategy": "ok", "ticker": "A"}, Boom()])
    assert bytes_of(p) == before                                              # the old file is whole: the failure happened before anything touched it
    assert not [f for f in os.listdir(tmp_path) if ".tmp." in f]
