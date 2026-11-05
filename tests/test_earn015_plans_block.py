"""EARN-015 (2026-11-05): refresh_all.sh's post-open check_plans pass - when it runs, when it retries, when it stamps.

Since EARN-015, check_plans.py leaves a plan whose session is still forming active instead of expiring or triggering it,
and `--exit-undecided` exits 3 while one waits. This block is the same-day pass that decides it: weekdays from 06:50 PT,
re-run on every launchd trigger until a pass exits 0 (the session settles at 13:05 PT), then stamped for the day.
The block is cut out of the live refresh_all.sh and run under bash with a stub check_plans and a fixed clock; nothing else runs.
Run: /opt/anaconda3/bin/python -m pytest -q tests/test_earn015_plans_block.py
"""
import os
import subprocess

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(LAB, "refresh_all.sh")
CALL = "/opt/anaconda3/bin/python /Users/anupampatil/stock-radar/check_plans.py --exit-undecided"


def _block():
    s = open(SCRIPT).read()
    a = s.index("# EARN-015 (2026-11-05)")
    b = s.index("DONE_MARK=/Users/anupampatil/strategy-lab/.refresh_done_", a)
    return s[a:b]


def _fire(tmp_path, minute, dow="5", rc=0):
    stub = tmp_path / "stub.sh"
    stub.write_text('#!/bin/bash\necho "$@" >> "%s"\nexit %d\n' % (tmp_path / "calls.txt", rc))
    stub.chmod(0o755)
    block = _block().replace(CALL, str(stub) + " --exit-undecided").replace("/Users/anupampatil/strategy-lab", str(tmp_path))
    harness = ("date() { case \"$1\" in '+%%Y-%%m-%%d') echo 2026-11-06;; '+%%u') echo %s;; *) echo 2026-11-06 06:50:00;; esac; }\n"
               "ARENA_MIN=%d\n" % (dow, minute)) + block
    subprocess.run(["bash", "-c", harness], check=True)
    calls = (tmp_path / "calls.txt").read_text().splitlines() if (tmp_path / "calls.txt").exists() else []
    return len(calls), (tmp_path / ".plans_open_done_2026-11-06").exists()


def test_block_is_wired_to_the_real_call():
    assert CALL in _block() and "&& touch \"$PLANS_MARK\"" in _block()


def test_not_before_0650(tmp_path):
    assert _fire(tmp_path, 409) == (0, False)


def test_retries_while_a_plan_waits_then_stamps(tmp_path):
    assert _fire(tmp_path, 410, rc=3) == (1, False)     # 06:50: a forming bar still undecided - no stamp
    assert _fire(tmp_path, 444, rc=2) == (2, False)     # stale radar refusal - no stamp
    assert _fire(tmp_path, 790, rc=0) == (3, True)      # 13:10: the session settled, every plan decided - stamped
    assert _fire(tmp_path, 824, rc=0) == (3, True)      # stamped: later triggers do not run it again


def test_weekend_never_runs(tmp_path):
    assert _fire(tmp_path, 600, dow="6") == (0, False)
