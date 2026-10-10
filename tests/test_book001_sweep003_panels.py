"""SWEEP-003 / BOOK-001 (2026-10-09, second wave): the writers the Sweep could not see because their path is a constant, or because a report is written next to the book.

The detector (command-center/lesson_sweep.py) now follows open(CONST, "w"); this wave converted the strategy-lab writers it then listed:
bench002_restore.py (the Arena's trade book), learning_meter.py (progress.csv), value_history.py (value_panel.csv), value_forward.py (the header-only value_book.csv),
rot_restate.py (rotation_book.json, exit_overlays.json, the note), intraday_discover.py, intraday_study.py, family9_gate.py, fib_zone_study.py, price_integrity.py,
value_screen.py, day_type.py. Each used json.dump(obj, open(path, "w"), indent=1) or a DictWriter loop into open(path, "w") - truncate, then write.

Pinned here:
  * AST GUARD: none of these files truncates a file in place any more (a write-mode open() whose path is not a .tmp is a failure), so a re-introduced one fails CI;
  * BYTE-IDENTITY: the new write equals the frozen old writer's bytes, on a hostile synthetic set (unicode, NaN, quotes, newlines, empty and missing fields, extra keys) and,
    where the file exists on this machine, on the live file read back and rewritten both ways (all three byte strings equal: the live file is a fixed point of both writers);
  * the real bench002_restore.main(--apply) run on scratch copies produces the same ledger bytes as the pre-conversion main() (frozen in this file).
Run: /opt/anaconda3/bin/python -m pytest -q tests/test_book001_sweep003_panels.py
"""
import ast
import csv
import io
import json
import os
import sys

import pytest

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LAB)
import atomicio

FILES = ["bench002_restore.py", "learning_meter.py", "value_history.py", "value_forward.py", "rot_restate.py", "intraday_discover.py",
         "intraday_study.py", "family9_gate.py", "fib_zone_study.py", "price_integrity.py", "value_screen.py", "day_type.py"]


def truncating_opens(src):
    out = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "open":
            mode = n.args[1] if len(n.args) > 1 else next((k.value for k in n.keywords if k.arg == "mode"), None)
            if isinstance(mode, ast.Constant) and isinstance(mode.value, str) and mode.value.startswith("w"):
                if "tmp" not in ast.unparse(n.args[0]):
                    out.append(n.lineno)
    return out


@pytest.mark.parametrize("name", FILES)
def test_no_converted_file_truncates_in_place(name):
    assert truncating_opens(open(os.path.join(LAB, name)).read()) == []


HOSTILE = {"a": 1.5, "b": [1, 2, {"c": None}], "d": "café — \"quoted\"\nnewline", "e": float("nan"), "f": {"z": 1, "y": 2}, "g": True}
HOSTILE_ROWS = [{"k": "x,y", "v": 'he said "hi"', "extra": "dropped"}, {"k": "café", "v": "line1\nline2"}, {"k": "", "v": ""}, {"k": "only"}]


@pytest.mark.parametrize("kw", [dict(indent=1), dict(), dict(indent=2, ensure_ascii=False), dict(indent=1, sort_keys=True, default=str)])
def test_atomic_json_is_json_dump_byte_for_byte(tmp_path, kw):
    old, new = tmp_path / "old.json", tmp_path / "new.json"
    with open(old, "w") as f:
        json.dump(HOSTILE, f, **kw)
    atomicio.atomic_json(str(new), HOSTILE, **kw)
    assert old.read_bytes() == new.read_bytes()
    assert sorted(os.listdir(tmp_path)) == ["new.json", "old.json"]            # no .tmp left behind


@pytest.mark.parametrize("kw,newline", [(dict(extrasaction="ignore"), None), (dict(extrasaction="ignore"), ""), (dict(restval="-", extrasaction="ignore"), "")])
def test_atomic_csv_is_the_dictwriter_loop_byte_for_byte(tmp_path, kw, newline):
    old, new = tmp_path / "old.csv", tmp_path / "new.csv"
    cols = ["k", "v"]
    with open(old, "w", newline=newline) as f:
        w = csv.DictWriter(f, fieldnames=cols, **kw)
        w.writeheader()
        for r in HOSTILE_ROWS:
            w.writerow(r)
    atomicio.atomic_csv(str(new), cols, HOSTILE_ROWS, **kw)
    assert old.read_bytes() == new.read_bytes()


def test_the_header_only_book_is_byte_identical(tmp_path):
    cols = ["strategy", "ticker", "side", "entry_date"]
    with open(tmp_path / "old.csv", "w", newline="") as f:
        csv.DictWriter(f, fieldnames=cols).writeheader()
    atomicio.atomic_csv(str(tmp_path / "new.csv"), cols, [])
    assert (tmp_path / "old.csv").read_bytes() == (tmp_path / "new.csv").read_bytes()


LIVE_JSON = ["reports/rot_restate_note.json", "reports/rotation_book.json", "reports/exit_overlays.json", "reports/intraday_discover.json",
             "reports/intraday_study.json", "reports/family9_gate.json", "reports/fib_zone_study.json", "reports/price_integrity.json", "reports/value_screen.json"]
LIVE_CSV = [("reports/arena_trades.csv", dict(extrasaction="ignore")), ("progress.csv", {}), ("data/value_panel.csv", {}), ("reports/value_book.csv", {}),
            ("intraday_discoveries.csv", {})]


@pytest.mark.parametrize("rel", LIVE_JSON)
def test_live_json_is_a_fixed_point_of_old_and_new(tmp_path, rel):
    live = os.path.join(LAB, rel)
    if not os.path.exists(live):
        pytest.skip("not on this machine")
    obj = json.load(open(live))
    with open(tmp_path / "old", "w") as f:
        json.dump(obj, f, indent=1)
    atomicio.atomic_json(str(tmp_path / "new"), obj, indent=1)
    assert open(live, "rb").read() == (tmp_path / "old").read_bytes() == (tmp_path / "new").read_bytes()


@pytest.mark.parametrize("rel,kw", LIVE_CSV)
def test_live_csv_is_a_fixed_point_of_old_and_new(tmp_path, rel, kw):
    live = os.path.join(LAB, rel)
    if not os.path.exists(live):
        pytest.skip("not on this machine")
    with open(live, newline="") as f:
        rd = csv.DictReader(f)
        cols, rows = rd.fieldnames, list(rd)
    with open(tmp_path / "old", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, **kw)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    atomicio.atomic_csv(str(tmp_path / "new"), cols, rows, **kw)
    assert open(live, "rb").read() == (tmp_path / "old").read_bytes() == (tmp_path / "new").read_bytes()


def test_bench002_restore_main_writes_the_same_ledger_bytes_as_before(tmp_path, monkeypatch):
    """the real main(--apply) on a synthetic ledger + restatement log in a scratch dir, against the frozen pre-conversion write.
    (Not the live copies: the BENCH-002 restore was applied long ago and main() now stops on the live log's blank old_net before it writes anything.)"""
    import bench002_restore as br
    trades, log = tmp_path / "arena_trades.csv", tmp_path / "price_restatement_log.csv"
    base = {"strategy": "S", "side": "long", "regime": "r", "tags": "t", "excess": "0.01", "net": "0.02", "entry_px": "10", "exit_px": "11",
            "entry_px_tape": "", "exit_px_tape": "", "net_tape": "", "excess_tape": ""}
    rows = [dict(base, ticker="AAA", entry_date="2026-07-01", exit_date="2026-07-02"),
            dict(base, ticker="B,B", entry_date="2026-07-03", exit_date="2026-07-04", tags='q"uote')]
    with open(trades, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=br.COLS); w.writeheader(); w.writerows(rows)
    hdr = ["restated_at", "scope", "strategy", "ticker", "entry_date", "exit_date", "field", "old_entry_px", "new_entry_px", "old_exit_px", "new_exit_px",
           "old_net", "new_net", "old_excess", "new_excess", "reason"]
    with open(log, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=hdr); w.writeheader()
        for r in rows:
            w.writerow({"scope": "closed", "strategy": "S", "ticker": r["ticker"], "entry_date": r["entry_date"], "exit_date": r["exit_date"],
                        "old_entry_px": "9", "new_entry_px": "10", "old_exit_px": "12", "new_exit_px": "11", "old_net": "0.05", "new_net": "0.02",
                        "old_excess": "0.04", "new_excess": "0.01"})
    monkeypatch.setattr(br, "TRADES", str(trades)); monkeypatch.setattr(br, "LOG", str(log))
    monkeypatch.setattr(sys, "argv", ["bench002_restore.py", "--apply"])
    expect_rows, done, _missing = br.restore()
    assert len(done) == 2
    old = tmp_path / "old.csv"
    with open(old, "w") as f:                                             # FROZEN ORACLE: the pre-conversion write
        w = csv.DictWriter(f, fieldnames=br.COLS, extrasaction="ignore")
        w.writeheader()
        for r in expect_rows:
            w.writerow({c: r.get(c, "") for c in br.COLS})
    br.main()
    assert trades.read_bytes() == old.read_bytes()
    assert not [p for p in os.listdir(tmp_path) if ".tmp." in p]

ROOT_DIR = __import__("pathlib").Path(LAB)
LOADABLE = ["bench002_restore.py", "learning_meter.py", "value_history.py", "value_forward.py", "intraday_discover.py", "intraday_study.py", "family9_gate.py", "price_integrity.py", "value_screen.py", "day_type.py"]


def test_each_converted_module_loads_by_path_from_any_cwd(tmp_path):
    """a resolver check, a bin script or another repo may load these with spec_from_file_location and no sys.path help: the atomicio import must not depend on the
    caller's path (found by loading every converted module from cwd=/ on 2026-10-09; a bare `from atomicio import` failed for most of them)."""
    import subprocess
    code = "import importlib.util as u,sys; s=u.spec_from_file_location('probe', sys.argv[1]); m=u.module_from_spec(s); s.loader.exec_module(m)"
    for name in LOADABLE:
        r = subprocess.run([sys.executable, "-c", code, str(ROOT_DIR / name)], cwd=tmp_path, capture_output=True, text=True, timeout=180)
        assert r.returncode == 0, (name, r.stderr[-300:])
