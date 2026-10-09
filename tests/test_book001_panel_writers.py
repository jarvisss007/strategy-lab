"""SWEEP-003 / BOOK-001 (2026-10-09): fetch_ohlc.py and fetch_volume.py write the shared price panels (data/open.csv, data/close.csv, data/volume.csv) beside-and-replace.

The defect: each opened the panel with open(path, "w", newline="") - truncating a ~3.5 MB file every lab's backtest reads - and streamed the rows. A reader that opened it mid-refresh
(the Monday refresh runs minutes before the cash open) saw a header and a partial panel. The sweep's detector missed them because the path is built from f"{name}.csv" / "volume.csv"
inside os.path.join; they are named in register row SWEEP-003.
What these pin:
  * neither file opens a path for a truncating write any more, and each writes its panels through atomic_write_text (an AST check);
  * BYTE-IDENTITY: the new StringIO-then-replace write produces exactly the bytes the old open(..., "w", newline="") + csv.writer loop produced - on the live panels (read back, rewritten both ways,
    all three equal: they are fixed points of the writer) and on hostile synthetic panels.
Run: /opt/anaconda3/bin/python -m pytest -q tests/test_book001_panel_writers.py
"""
import ast
import csv
import io
import os
import sys

import pytest

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LAB)
import atomicio


def old_write(path, header, rows):
    with open(path, "w", newline="") as f:           # FROZEN ORACLE: fetch_ohlc.py / fetch_volume.py before SWEEP-003
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def new_write(path, header, rows):
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    atomicio.atomic_write_text(path, buf.getvalue())


@pytest.mark.parametrize("fname", ["fetch_ohlc.py", "fetch_volume.py"])
def test_the_panel_writers_never_open_for_truncating_write_and_use_atomic_write_text(fname):
    tree = ast.parse(open(os.path.join(LAB, fname)).read())
    truncating, atomic = [], []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        if isinstance(f, ast.Name) and f.id == "open":
            mode = node.args[1].value if len(node.args) > 1 and isinstance(node.args[1], ast.Constant) else ""
            for kw in node.keywords:
                if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                    mode = kw.value.value
            if "w" in str(mode):
                truncating.append(node.lineno)
        if isinstance(f, ast.Name) and f.id == "atomic_write_text":
            atomic.append(node.lineno)
    assert not truncating, f"{fname}: truncating open() at line(s) {truncating}"
    assert len(atomic) == 1, f"{fname}: expected one atomic_write_text call, found {atomic}"


@pytest.mark.parametrize("name", ["open.csv", "close.csv", "volume.csv"])
def test_the_live_panel_is_a_fixed_point_of_both_writers(tmp_path, name):
    live = os.path.join(LAB, "data", name)
    if not os.path.exists(live):
        pytest.skip(f"no live {name} in this tree")
    raw = open(live, "rb").read()
    rd = list(csv.reader(open(live, newline="")))
    header, rows = rd[0], rd[1:]
    assert len(rows) > 1000 and len(header) > 100                              # a real panel
    a, b = str(tmp_path / "old.csv"), str(tmp_path / "new.csv")
    old_write(a, header, rows)
    new_write(b, header, rows)
    assert open(a, "rb").read() == open(b, "rb").read() == raw


def test_hostile_panels_are_byte_identical(tmp_path):
    header = ["date", "A,B", 'C"D', "É☃"]
    rows = [["2026-10-01", 1.5, "", 3], ["2026-10-02", "", "x\ny", 0.000001234], []]
    a, b = str(tmp_path / "old.csv"), str(tmp_path / "new.csv")
    old_write(a, header, rows)
    new_write(b, header, rows)
    assert open(a, "rb").read() == open(b, "rb").read()
    assert not [f for f in os.listdir(tmp_path) if ".tmp." in f]
