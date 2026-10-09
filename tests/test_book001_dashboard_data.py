"""SWEEP-003 / BOOK-001 (2026-10-09): returns_matrix.py, universe_daytype.py and intraday_cache.py write their dashboard / cache data beside-and-replace, never truncating in place.

The defect: returns.html and daytype.html load reports/returns_matrix.js and reports/universe_daytype.js, the labs read data/intraday_*.json, and each writer opened its file with open(path, "w") -
a reader that opened it mid-write saw a half-written file. The sweep saw one of the seven writes (the others build the path inside os.path.join or are the .js / .csv twins of a .json).
What these pin: no truncating open() of any of those paths remains and each is written through atomicio (AST on the path argument's source); the new write is byte-identical to the old one on every live file
(each is a fixed point of its writer) and on hostile payloads (json.dump chunked into a file equals json.dumps; csv rows through atomic_csv equal the DictWriter loop).
Run: /opt/anaconda3/bin/python -m pytest -q tests/test_book001_dashboard_data.py
"""
import ast
import csv
import glob
import io
import json
import os
import sys

import pytest

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LAB)
import atomicio

TARGETS = {"returns_matrix.py": ("returns_matrix.json", "returns_matrix.js"),
           "universe_daytype.py": ("universe_daytype.json", "universe_daytype.js", "universe_daytype.csv"),
           "intraday_cache.py": ("intraday_",)}


@pytest.mark.parametrize("fname", sorted(TARGETS))
def test_no_truncating_open_and_each_data_file_goes_through_atomicio(fname):
    tree = ast.parse(open(os.path.join(LAB, fname)).read())
    trunc, atomic = [], []
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        arg0 = ast.unparse(n.args[0]) if n.args else ""
        hit = any(t in arg0 for t in TARGETS[fname])
        if isinstance(n.func, ast.Name) and n.func.id == "open" and hit:
            mode = n.args[1].value if len(n.args) > 1 and isinstance(n.args[1], ast.Constant) else ""
            if "w" in str(mode):
                trunc.append((n.lineno, arg0))
        if isinstance(n.func, ast.Name) and n.func.id in ("atomic_json", "atomic_write_text", "atomic_csv") and hit:
            atomic.append(arg0)
        # the old shape: json.dump(obj, open(<path>, "w"))
        if isinstance(n.func, ast.Attribute) and n.func.attr == "dump" and len(n.args) > 1 and isinstance(n.args[1], ast.Call) and getattr(n.args[1].func, "id", "") == "open":
            trunc.append((n.lineno, "json.dump(..., open(...))"))
    assert not trunc, trunc
    assert len(atomic) == len(TARGETS[fname]), (fname, atomic)


def old_dump(path, obj, **kw):
    with open(path, "w") as f:
        json.dump(obj, f, **kw)


def old_js_chunked(path, prefix, obj, suffix):
    with open(path, "w") as f:                       # the old universe_daytype.js writer: prefix, json.dump into the file, suffix
        f.write(prefix)
        json.dump(obj, f, indent=1)
        f.write(suffix)


HOSTILE = {"a": [1, 2.5, None, True], "ünï": "ÅÉ☃ \"q\"\nline", "n": float("nan"), "z": {"b": {}}, "m": []}


def test_json_and_js_writes_are_byte_identical_on_hostile_payloads(tmp_path):
    a, b = str(tmp_path / "old"), str(tmp_path / "new")
    for kw in ({"indent": 1}, {}):
        old_dump(a, HOSTILE, **kw)
        atomicio.atomic_json(b, HOSTILE, **kw)
        assert open(a, "rb").read() == open(b, "rb").read()
    old_js_chunked(a, "window.DAYTYPE_DATA = ", HOSTILE, ";\n")
    atomicio.atomic_write_text(b, "window.DAYTYPE_DATA = " + json.dumps(HOSTILE, indent=1) + ";\n")
    assert open(a, "rb").read() == open(b, "rb").read()
    with open(a, "w") as f:                          # the old returns_matrix.js writer
        f.write("window.RETURNS_DATA = " + json.dumps(HOSTILE, indent=1) + ";")
    atomicio.atomic_write_text(b, "window.RETURNS_DATA = " + json.dumps(HOSTILE, indent=1) + ";")
    assert open(a, "rb").read() == open(b, "rb").read()
    assert not [f for f in os.listdir(tmp_path) if ".tmp." in f]


def test_csv_rows_are_byte_identical_through_atomic_csv(tmp_path):
    rows = [{"ticker": "A,B", "x": 1.5, "y": None, "z": 'q"q'}, {"ticker": "ÅÉ", "x": "", "y": 0, "z": "multi\nline"}]
    cols = list(rows[0].keys())
    a, b = str(tmp_path / "old.csv"), str(tmp_path / "new.csv")
    with open(a, "w", newline="") as f:              # the old universe_daytype.csv writer
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(rows)
    atomicio.atomic_csv(b, cols, rows)
    assert open(a, "rb").read() == open(b, "rb").read()


@pytest.mark.parametrize("rel", ["reports/returns_matrix.json", "reports/universe_daytype.json", "data/intraday_15m.json", "data/intraday_60m.json"])
def test_the_live_json_is_a_fixed_point_of_its_writer(tmp_path, rel):
    live = os.path.join(LAB, rel)
    if not os.path.exists(live):
        pytest.skip(f"no live {rel}")
    raw = open(live, "rb").read().decode()
    obj = json.loads(raw)
    kw = {} if "intraday_" in rel else {"indent": 1}
    b = str(tmp_path / "new.json")
    atomicio.atomic_json(b, obj, **kw)
    assert open(b).read() == raw


def test_the_live_js_and_csv_are_fixed_points_of_their_writers(tmp_path):
    p = os.path.join(LAB, "reports", "returns_matrix.js")
    if os.path.exists(p):
        raw = open(p).read()
        pre = "window.RETURNS_DATA = "
        assert raw.startswith(pre)
        assert pre + json.dumps(json.loads(raw[len(pre):].rstrip(";")), indent=1) + ";" == raw
    p = os.path.join(LAB, "reports", "universe_daytype.js")
    if os.path.exists(p):
        raw = open(p).read()
        pre = "window.DAYTYPE_DATA = "
        assert raw.startswith(pre)
        assert pre + json.dumps(json.loads(raw[len(pre):].rstrip().rstrip(";")), indent=1) + ";\n" == raw
    p = os.path.join(LAB, "reports", "universe_daytype.csv")
    if os.path.exists(p):
        raw = open(p, "rb").read()
        rows = list(csv.DictReader(open(p, newline="")))
        b = str(tmp_path / "new.csv")
        atomicio.atomic_csv(b, list(rows[0].keys()), rows)
        assert open(b, "rb").read() == raw
