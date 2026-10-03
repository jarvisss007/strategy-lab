"""PROPOSED resolver checks for EARN-011 - handed to the session that owns the council resolver. NOT wired.

Each check returns (ok: bool, message: str) like every resolver check. Every name carries the _earn011_ / _EARN011_ prefix so it cannot collide with an
existing check or constant (helpers share the prefix and return other types; only the three below are checks). Suggested registry lines for the
CHECKS dict in resolver.py:

    "earn011_last_exit_judged": _earn011_last_exit_judged,                  # judges EARN-004's "the last run exited 2" in light of the summary line
    "earn011_fetcher_carries_the_fix": _earn011_fetcher_carries_the_fix,    # the fetcher's guard is the fixed one and its offline selftest passes
    "earn011_last_run_proves_the_fix": _earn011_last_run_proves_the_fix,    # the row's CLOSING check: a run of the fixed script exited 0 with the summary line

WIRING. EARN-011's own register row has check "" today. Put `earn011_last_run_proves_the_fix` there until it passes for the first time (the first 18:10 PT
run of the fixed script), then switch the row to `earn011_fetcher_carries_the_fix`: a permanent nightly "proves" would reopen EARN-011 on any later real alarm,
which EARN-004's own check already owns. `earn011_last_exit_judged` is a diagnostic beside EARN-004's check, not a closing check. Read-only: nothing here
writes a file or touches the network. The only subprocesses are `launchctl print` (what edgar_feed_is_current already reads) and the fetcher's offline
`--selftest` (run with -B from a neutral directory, so it writes no .pyc into the lab either).

WHY THESE CHECKS EXIST. SEC's submissions JSON now serves some registrants' acceptance stamps double-converted (the true UTC stamp read as New York
time and converted again). Before the fix the daily pass called every such held print CHANGED: the 18:10 PT run of 2026-10-02 printed 1,131 ATTENTION
CHANGED lines and exited 2 three times, and edgar_feed_is_current (EARN-004) read only the exit code. After the fix those prints are counted in ONE
summary line, `N held prints SEC serves double-converted (+4h EDT / +5h EST) in M ticker(s); a sample of K header-verified: ...`, and an exit of 2
means a real ATTENTION line (a CHANGED print, a refuted or unreadable header sample, a failed ticker, a deferred print...). So the same exit code now
reads two ways, and the summary line is what tells them apart:

  earn011_last_exit_judged. Reads ~/bin/logs/edgar-8k.log (the LAST run: its final attempt, the one launchd records) and launchd's last exit code.
    exit 0 or never exited                              -> passes (nothing to judge).
    a last attempt with no 'done' line                  -> passes while the log is fresh (a run in progress), FAILS once it has been silent for 45 minutes
                                                           (the retry loop's longest pause is 10): a run that never finished is not "in progress".
    exit 2, the attempt HAS the summary line and ATTENTION lines -> FAILS and names them: the exit is REAL, the double-conversion count is not among them.
    exit 2, the attempt HAS the summary line and NO ATTENTION line -> FAILS: the log and the exit code disagree.
    exit 2, the attempt has NO summary line and only ATTENTION CHANGED lines -> FAILS, as `EXPLAINED, NOT CURED`: this is what the script BEFORE the fix prints
      when SEC serves held prints double-converted (the 2026-10-02 18:10 run), but that script could not tell a real change from the flood, so it does not
      show that none was real; the next 18:10 run of the fixed script decides. It must not PASS: a pass means "nothing to do" and can auto-close a row, and
      the text it keys on (the absence of the summary line) is exactly what a wording change would silently turn into "explained".
    exit 2, no summary line, any other ATTENTION kind / exit 1 / any other code -> FAILS and says what it saw.
  earn011_fetcher_carries_the_fix. fetch_earnings_8k.py parses; verify_new() has NO opt-out parameter (it is (cik, prints, fetch_text): the 14-day
    cut-off that let a backfill take SEC's stamp unchecked cannot come back); FRESH_DAYS is not defined; to_double_converted, check_double and
    pick_sample exist; check_stamp knows the "doubled" verdict; main() offers --check; DOUBLE_SAMPLE is 3 to 5; and `fetch_earnings_8k.py --selftest`
    prints PASS.
  earn011_last_run_proves_the_fix. The last nightly run was made by the fixed script (its run stamp carries `double_converted`), exited 0, printed the
    summary line with the same count the run stamp holds, flagged nothing the resolver reads (vanished, changed, cik_moved, failed, deferred), and read
    the filing header of at least min(DOUBLE_SAMPLE, double_converted) doubled prints, each one agreeing with its held stamp (plus every print of a mixed
    registrant, which the fetcher always reads). Until such a run exists it FAILS with `NOT yet proven`.

WHAT THEY CANNOT SHOW. A random sample reads 4 of N doubled prints: the sample proves the RULE is holding, not that every print was looked at (the
fetcher's docstring says so, and that no registrant was mixed on 2026-10-03). The log is append-only and shared by every run; a run that died before its
'done' line is reported as in progress until the log has been silent for 45 minutes, then fails.

Run it by hand: /opt/anaconda3/bin/python PROPOSED_resolver_check_EARN-011.py             # the three checks against the live state, a report
                /opt/anaconda3/bin/python PROPOSED_resolver_check_EARN-011.py --selftest  # 37 fixture scenarios (fake log, run stamp, fetcher); no live state
"""
import ast
import json
import os
import re
import subprocess
import sys
import tempfile
import time

_EARN011_HOME = os.path.expanduser("~")
_EARN011_SL = f"{_EARN011_HOME}/strategy-lab"
_EARN011_FETCHER = f"{_EARN011_SL}/fetch_earnings_8k.py"
_EARN011_RUN = f"{_EARN011_SL}/data/edgar/earnings_8k_run.json"
_EARN011_LOG = f"{_EARN011_HOME}/bin/logs/edgar-8k.log"
_EARN011_LABEL = "com.anupam.edgar-8k"
_EARN011_SUMMARY = re.compile(r"^\s+(\d+) held prints SEC serves double-converted \(\+4h EDT / \+5h EST\) in (\d+) ticker\(s\); (.*)$", re.M)
_EARN011_ATTENTION = re.compile(r"^ATTENTION (CIK MOVED|[A-Z]+)\b", re.M)
_EARN011_PYTHON = "/opt/anaconda3/bin/python" if os.path.exists("/opt/anaconda3/bin/python") else sys.executable


def _earn011_last_run(log_path=None):
    """The LAST run in the log -> dict(done=bool, exit=int|None, attempt=int, block=str, finished=str) or None when the log has no run.
    A run is one `=== edgar-8k attempt 1 ...` .. `=== edgar-8k done <time> exit N ===` stretch; its FINAL attempt is the one whose exit code launchd records."""
    try:
        text = open(log_path or _EARN011_LOG, errors="replace").read()
    except OSError:
        return None
    starts = [m for m in re.finditer(r"^=== edgar-8k attempt (\d+) ", text, re.M)]
    if not starts:
        return None
    last = starts[-1]
    tail = text[last.start():]
    done = re.search(r"^=== edgar-8k done (.+?) exit (\d+) ===", tail, re.M)
    return {"done": bool(done), "exit": int(done.group(2)) if done else None, "attempt": int(last.group(1)),
            "block": tail[:done.start()] if done else tail, "finished": done.group(1) if done else ""}


def _earn011_launchd_code():
    """launchd's `last exit code` for the nightly job as a string ('0', '2', '(never exited)'), or None when launchd cannot say."""
    try:
        p = subprocess.run(["launchctl", "print", f"gui/{os.getuid()}/{_EARN011_LABEL}"], capture_output=True, text=True, timeout=30)
    except Exception:                                  # noqa: BLE001 - reported by the caller as 'could not read'
        return None
    m = re.search(r"last exit code = (.+)", p.stdout or "")
    return m.group(1).strip() if p.returncode == 0 and m else None


def _earn011_attention_kinds(block):
    """{'CHANGED': 1131, ...}: the ATTENTION lines of one attempt by kind. The double-converted count is a summary line, never an ATTENTION."""
    kinds = {}
    for m in _EARN011_ATTENTION.finditer(block):
        kinds[m.group(1)] = kinds.get(m.group(1), 0) + 1
    return kinds


def _earn011_last_exit_judged():
    """Judges EARN-004's 'the last edgar-8k run exited 2' in light of the EARN-011 summary line (see the module docstring for the table)."""
    run = _earn011_last_run()
    code = _earn011_launchd_code()
    if run is None:
        return False, f"{_EARN011_LOG} holds no edgar-8k run to judge"
    if not run["done"]:
        try:
            idle = (time.time() - os.path.getmtime(_EARN011_LOG)) / 60
        except OSError:
            idle = 0.0
        if idle > 45:                                  # the retry loop's longest silence is its 10-minute sleep
            return False, (f"attempt {run['attempt']} of the last run has no 'done' line and the log has been silent for {idle:.0f} minutes: "
                           f"a run that never finished")
        return True, f"attempt {run['attempt']} of the last run has no 'done' line yet: a run is in progress, not judged"
    if run["exit"] == 0:
        s = _EARN011_SUMMARY.search(run["block"])
        return True, (f"the last run finished {run['finished']} exit 0" + (f"; summary line: {s.group(1)} double-converted in {s.group(2)} ticker(s)" if s
                                                                           else " (no EARN-011 summary line: a run of the script before the fix)"))
    if code is not None and code != str(run["exit"]):
        return False, f"launchd records last exit code {code} but the log's last run says exit {run['exit']}: read {_EARN011_LOG}"
    kinds = _earn011_attention_kinds(run["block"])
    s = _EARN011_SUMMARY.search(run["block"])
    listed = ", ".join(f"{n} {k}" for k, n in sorted(kinds.items())) or "no ATTENTION line"
    if run["exit"] == 2 and s and kinds:
        return False, (f"the last run (finished {run['finished']}) exited 2 for a REAL reason: {listed}. It printed the EARN-011 summary line "
                       f"({s.group(1)} held prints SEC serves double-converted), so the double conversion is not what raised them: read {_EARN011_LOG}")
    if run["exit"] == 2 and s:
        return False, f"the last run exited 2 and printed the EARN-011 summary line but no ATTENTION line: the log and the exit code disagree ({_EARN011_LOG})"
    if run["exit"] == 2 and kinds and set(kinds) == {"CHANGED"}:
        return False, (f"EXPLAINED, NOT CURED: the last run (finished {run['finished']}) exited 2 with {kinds['CHANGED']} ATTENTION CHANGED line(s) and no "
                       f"EARN-011 summary line, which is what the script BEFORE the fix prints when SEC serves held prints double-converted. That script "
                       f"cannot tell a real change from the flood, so this does not show that none is real; the next 18:10 PT run of the fixed script decides")
    return False, (f"the last run (finished {run['finished']}) exited {run['exit']} with {listed} and no EARN-011 summary line: "
                   f"not the EARN-011 flood, read {_EARN011_LOG}")


def _earn011_fetcher_carries_the_fix():
    """The guard in fetch_earnings_8k.py is the fixed one (static) and its offline selftest passes."""
    try:
        source = open(_EARN011_FETCHER).read()
        tree = ast.parse(source)
    except (OSError, SyntaxError) as e:
        return False, f"{_EARN011_FETCHER} cannot be read or parsed: {type(e).__name__}: {e}"
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    consts = {t.id: n.value for n in tree.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name)}
    missing = [f for f in ("to_double_converted", "check_double", "pick_sample", "verify_new", "check_stamp", "merge_incremental", "update", "main") if f not in funcs]
    if missing:
        return False, f"fetch_earnings_8k.py is missing {', '.join(missing)}: the EARN-011 fix is not in the file"
    args = [a.arg for a in funcs["verify_new"].args.args]
    if args != ["cik", "prints", "fetch_text"]:
        return False, f"verify_new takes {args}, not (cik, prints, fetch_text): an opt-out for the header check has come back"
    if "FRESH_DAYS" in consts:
        return False, "FRESH_DAYS is defined again: the age cut-off that let a backfill take SEC's stamp unchecked"
    src = ast.get_source_segment(source, funcs["check_stamp"]) or ""
    if not re.search(r"""["']doubled["']""", src) or "to_double_converted" not in src:
        return False, "check_stamp does not know the doubled form: a new print from a switched registrant would be DEFERRED every night"
    ds = consts.get("DOUBLE_SAMPLE")
    if not (isinstance(ds, ast.Constant) and isinstance(ds.value, int) and 3 <= ds.value <= 5):
        return False, "DOUBLE_SAMPLE is not an integer constant from 3 to 5"
    if "--check" not in (ast.get_source_segment(source, funcs["main"]) or ""):
        return False, "main() no longer offers --check (the dry run)"
    try:
        p = subprocess.run([_EARN011_PYTHON, "-B", _EARN011_FETCHER, "--selftest"], capture_output=True, text=True, timeout=600, cwd=tempfile.gettempdir())
    except Exception as e:                             # noqa: BLE001 - reported
        return False, f"fetch_earnings_8k.py --selftest could not be run: {type(e).__name__}: {e}"
    if p.returncode != 0 or "selftest: PASS" not in (p.stdout or ""):
        return False, f"fetch_earnings_8k.py --selftest did not pass (exit {p.returncode}): {(p.stdout or p.stderr or '').strip()[-300:]}"
    return True, f"the fetcher carries the EARN-011 guard (verify_new has no opt-out, DOUBLE_SAMPLE {ds.value}) and its offline selftest passes"


def _earn011_last_run_proves_the_fix():
    """The closing proof: a nightly run of the FIXED script exited 0, printed the summary line, flagged nothing and read the header sample."""
    try:
        stamp = json.load(open(_EARN011_RUN))
    except (OSError, ValueError) as e:
        return False, f"NOT yet proven: the run stamp cannot be read ({type(e).__name__})"
    if "double_converted" not in stamp:
        return False, (f"NOT yet proven: the last run stamp ({stamp.get('finished_at', '?')[:16]}) was written by the script before the fix "
                       f"(it has no double_converted field); the first 18:10 PT run of the fixed script has not happened yet")
    run = _earn011_last_run()
    if run is None or not run["done"]:
        return False, "NOT yet proven: the log has no finished run"
    if run["exit"] != 0:
        return False, f"the last run of the fixed script exited {run['exit']}, not 0: {_earn011_last_exit_judged()[1]}"
    s = _EARN011_SUMMARY.search(run["block"])
    if not s:
        return False, "the last run exited 0 but its attempt printed no EARN-011 summary line (the stamp says it is the fixed script): the log and the stamp disagree"
    n, tk = int(s.group(1)), int(s.group(2))
    if n != stamp["double_converted"] or tk != stamp.get("double_converted_tickers"):
        return False, f"the summary line says {n} in {tk} ticker(s), the run stamp says {stamp['double_converted']} in {stamp.get('double_converted_tickers')}"
    flagged = [k for k in ("vanished", "changed", "cik_moved", "failed", "deferred") if stamp.get(k)]
    if flagged:
        return False, f"the run stamp lists {', '.join(flagged)}"
    sample = stamp.get("double_sample") or []
    try:
        ds_src = re.search(r"^DOUBLE_SAMPLE\s*=\s*(\d+)", open(_EARN011_FETCHER).read(), re.M)
    except OSError:
        ds_src = None
    need = min(int(ds_src.group(1)) if ds_src else 4, n)
    if len(sample) < need or any(v != "ok" for _, _, v, _ in sample):
        return False, (f"the header sample was {len(sample)} print(s) with verdicts {sorted({v for _, _, v, _ in sample})}; "
                       f"it must be at least {need}, every one ok")
    return True, (f"the last run ({stamp['finished_at'][:16]}) exited 0 with the summary line: {n} held prints SEC serves double-converted in {tk} ticker(s), "
                  f"{len(sample)} header-verified, all agreeing with the held stamp; nothing flagged")


def _earn011_selftest():
    """Every branch of the three checks against fixtures in a temp directory: a fake edgar-8k log, run stamp and fetcher. Touches no live file."""
    g = globals()
    names = ("_EARN011_LOG", "_EARN011_RUN", "_EARN011_FETCHER", "_EARN011_SL", "_earn011_launchd_code")
    saved = {n: g[n] for n in names}
    bad = []
    d = tempfile.mkdtemp(prefix="earn011_")

    def check(cond, msg):
        if not cond:
            bad.append(msg)

    def head(n):
        return f"=== edgar-8k attempt {n} 2026-10-02 18:10:00 PDT ===\n"
    summ = lambda n=1743, t=68, tail="a sample of 4 header-verified: 4 equal the held stamp": f"  {n} held prints SEC serves double-converted (+4h EDT / +5h EST) in {t} ticker(s); {tail}\n"
    chg = "".join(f"ATTENTION CHANGED V 2022-0{k}-27: the feed holds accepted 2022-0{k}-27T21:08:07, SEC lists that date with another stamp - KEPT as held.\n" for k in (1, 2, 3))
    done = lambda rc: f"--- attempt 1 exit {rc}\n=== edgar-8k done 2026-10-02 18:31:21 PDT exit {rc} ===\n"
    older = head(1) + "earnings_8k: SEC answered 144/144 tickers\n" + done(0)               # an earlier, clean run: the judged run is always the LAST

    def run_exp(log, code):
        g["_EARN011_LOG"] = os.path.join(d, "log.txt")
        open(g["_EARN011_LOG"], "w").write(log) if log is not None else (os.path.exists(g["_EARN011_LOG"]) and os.remove(g["_EARN011_LOG"]))
        g["_earn011_launchd_code"] = lambda: code
        return _earn011_last_exit_judged()
    try:
        ok, m = run_exp(older + head(1) + "x\n" + summ() + done(0), "0")
        check(ok and "1743 double-converted in 68 ticker(s)" in m, "exit 0 with the summary line passes and quotes it")
        ok, m = run_exp(older + head(1) + "x\n" + done(0), "0")
        check(ok and "script before the fix" in m, "exit 0 without a summary line (an old run) passes")
        ok, m = run_exp(older + head(1) + chg + done(2), "2")
        check(not ok and "EXPLAINED, NOT CURED" in m and "3 ATTENTION CHANGED" in m and "cannot tell a real change" in m,
              "exit 2, no summary, only CHANGED: the pre-fix flood is explained but FAILS (a pass could auto-close a row)")
        ok, m = run_exp(older + head(1) + summ() + chg + done(2), "2")
        check(not ok and "REAL reason: 3 CHANGED" in m and "1743" in m, "exit 2 WITH the summary line and CHANGED lines is real")
        ok, m = run_exp(older + head(1) + summ() + done(2), "2")
        check(not ok and "disagree" in m, "exit 2 with the summary line and no ATTENTION line: the log and the exit disagree")
        ok, m = run_exp(older + head(1) + chg + "ATTENTION FAILED AAPL (ConnectionError): SEC did not answer\n" + done(2), "2")
        check(not ok and "1 CHANGED" not in m and "3 CHANGED, 1 FAILED" in m and "not the EARN-011 flood" in m, "exit 2, no summary, CHANGED plus another kind: not the flood")
        ok, m = run_exp(older + head(1) + "ATTENTION DEFERRED AAPL 2026-10-02: NOT written\n" + done(2), "2")
        check(not ok and "1 DEFERRED" in m, "exit 2, no summary, DEFERRED only: not the flood")
        ok, m = run_exp(older + head(1) + "ATTENTION CIK MOVED AAPL (feed 1 vs cik_map 2): not fetched\n" + done(2), "2")
        check(not ok and "1 CIK MOVED" in m, "a two-word ATTENTION kind is named whole")
        ok, m = run_exp(older + head(1) + "REFUSED: SEC answered for 3 of 144 tickers\n" + done(1), "1")
        check(not ok and "exited 1" in m, "exit 1 (REFUSED) fails")
        ok, m = run_exp(older + head(1) + "earnings_8k: SEC answered\n", None)
        check(ok and "in progress" in m, "a last attempt with no 'done' line and a fresh log is in progress: not judged")
        three_hours_ago = time.time() - 3 * 3600
        os.utime(g["_EARN011_LOG"], (three_hours_ago, three_hours_ago))
        ok, m = _earn011_last_exit_judged()
        check(not ok and "never finished" in m and "silent for 180 minutes" in m, "...and a log silent for 3 hours means a run that never finished: FAILS")
        ok, m = run_exp(older + head(1) + summ() + chg + done(2), "0")
        check(not ok and "launchd records last exit code 0" in m, "launchd and the log disagreeing is reported")
        ok, m = run_exp(head(1) + chg + done(2) + head(1) + "x\n" + summ() + done(0), "0")
        check(ok and "exit 0" in m, "only the LAST run is judged: an old flood before a clean run is history")
        ok, m = run_exp(head(1) + chg + "--- attempt 1 exit 2\n" + head(2) + chg + "--- attempt 2 exit 2\n" + head(3) + summ() + done(0), "0")
        check(ok, "only the FINAL attempt counts: floods in attempts 1 and 2, a clean attempt 3")
        ok, m = run_exp(None, "0")
        check(not ok and "holds no edgar-8k run" in m, "a missing log fails loud")
        # ---- the closing proof
        g["_EARN011_RUN"] = os.path.join(d, "run.json")
        g["_EARN011_FETCHER"] = os.path.join(d, "fetch.py")
        open(g["_EARN011_FETCHER"], "w").write("DOUBLE_SAMPLE = 4\n")
        good = {"finished_at": "2026-10-03T18:12:00-07:00", "double_converted": 1743, "double_converted_tickers": 68, "vanished": [], "changed": [], "cik_moved": [],
                "failed": [], "deferred": [], "double_sample": [["ASTS", "2024-05-15", "ok", "x"], ["CAT", "2022-10-27", "ok", "x"], ["NOC", "2026-04-21", "ok", "x"], ["OKTA", "2021-03-03", "ok", "x"]]}

        def prove(stamp, log, code="0"):
            json.dump(stamp, open(g["_EARN011_RUN"], "w")) if stamp is not None else (os.path.exists(g["_EARN011_RUN"]) and os.remove(g["_EARN011_RUN"]))
            run_exp(log, code)                          # sets the log and the launchd stub
            return _earn011_last_run_proves_the_fix()
        clean = older + head(1) + summ() + done(0)
        ok, m = prove(good, clean)
        check(ok and "1743 held prints" in m and "4 header-verified" in m, "a fixed run, exit 0, summary line, 4 ok samples: PROVEN")
        ok, m = prove({k: v for k, v in good.items() if k not in ("double_converted", "double_converted_tickers")}, clean)
        check(not ok and "NOT yet proven" in m, "a run stamp written before the fix is not proof")
        ok, m = prove(None, clean)
        check(not ok and "NOT yet proven" in m, "no run stamp: not proven")
        ok, m = prove(good, older + head(1) + chg + done(2), "2")
        check(not ok and "exited 2" in m, "the fixed script's last run exited 2: not proven, and says why")
        ok, m = prove(good, older + head(1) + done(0))
        check(not ok and "no EARN-011 summary line" in m, "exit 0 but no summary line while the stamp says fixed: the log and the stamp disagree")
        ok, m = prove(good, older + head(1) + summ(n=1000) + done(0))
        check(not ok and "1000" in m and "1743" in m, "the summary line's count must equal the run stamp's")
        ok, m = prove(dict(good, changed=[["AAPL", "2026-01-01", "x"]]), clean)
        check(not ok and "changed" in m, "a run stamp that lists a changed print is not proof")
        ok, m = prove(dict(good, failed=["AAPL (ConnectionError)"]), clean)
        check(not ok and "failed" in m, "a run stamp that lists a failed ticker is not proof")
        ok, m = prove(dict(good, double_sample=good["double_sample"][:3] + [["OKTA", "2021-03-03", "mismatch", "x"]]), clean)
        check(not ok and "mismatch" in m, "a sample print that did not agree is not proof")
        ok, m = prove(dict(good, double_sample=good["double_sample"][:2]), clean)
        check(not ok and "at least 4" in m, "a sample smaller than DOUBLE_SAMPLE is not proof")
        ok, m = prove(dict(good, double_converted=2, double_sample=good["double_sample"][:2]), older + head(1) + summ(n=2, t=1) + done(0))
        check(not ok, "(tickers in the summary line differ from the stamp's) is not proof")
        ok, m = prove(dict(good, double_converted=2, double_converted_tickers=1, double_sample=good["double_sample"][:2]), older + head(1) + summ(n=2, t=1) + done(0))
        check(ok, "with fewer doubled prints than the sample, reading all of them is enough")
        ok, m = prove(dict(good, double_converted=0, double_converted_tickers=0, double_sample=[]), older + head(1) + summ(n=0, t=0, tail="no header sample needed") + done(0))
        check(ok and "0 held prints" in m, "SEC serving true stamps again (nothing doubled) is proven too")
        # ---- the fetcher's guard
        base = ("import sys\nDOUBLE_SAMPLE = 4\ndef to_double_converted(x):\n    return x\ndef check_double(a, b, c):\n    return 1\ndef pick_sample(a, b, c):\n    return 1\n"
                "def check_stamp(cik, r, f):\n    return 'doubled', to_double_converted(r)\ndef merge_incremental(h, r):\n    return 1\ndef update(a, b, c, d):\n    return 1\n"
                "def verify_new(cik, prints, fetch_text):\n    return 1\ndef main(argv):\n    return '--check'\n"
                "if __name__ == '__main__':\n    print('fetch_earnings_8k selftest: ' + ('PASS' if '--selftest' in sys.argv else '?'))\n")
        g["_EARN011_SL"] = d

        def fetcher(src):
            open(g["_EARN011_FETCHER"], "w").write(src)
            return _earn011_fetcher_carries_the_fix()
        ok, m = fetcher(base)
        check(ok and "DOUBLE_SAMPLE 4" in m, "a fetcher with the guard and a passing selftest: carries the fix")
        ok, m = fetcher(base.replace("def verify_new(cik, prints, fetch_text)", "def verify_new(cik, prints, must, fetch_text)"))
        check(not ok and "opt-out" in m, "verify_new with a must() opt-out fails")
        ok, m = fetcher(base.replace("DOUBLE_SAMPLE = 4\n", "DOUBLE_SAMPLE = 4\nFRESH_DAYS = 14\n"))
        check(not ok and "FRESH_DAYS" in m, "FRESH_DAYS defined again fails")
        ok, m = fetcher(base.replace("'doubled', ", "'ok', "))
        check(not ok and "doubled form" in m, "a check_stamp that does not know the doubled verdict fails")
        ok, m = fetcher(base.replace("DOUBLE_SAMPLE = 4", "DOUBLE_SAMPLE = 9"))
        check(not ok and "3 to 5" in m, "DOUBLE_SAMPLE outside 3 to 5 fails")
        ok, m = fetcher(base.replace("return '--check'", "return 0"))
        check(not ok and "--check" in m, "a main() without --check fails")
        ok, m = fetcher(base.replace("def pick_sample(a, b, c):\n    return 1\n", ""))
        check(not ok and "missing pick_sample" in m, "a missing function fails")
        ok, m = fetcher(base.replace("'PASS' if '--selftest' in sys.argv else '?'", "'FAIL'"))
        check(not ok and "selftest did not pass" in m, "a selftest that does not print PASS fails")
        ok, m = fetcher("def broken(:\n")
        check(not ok and "cannot be read or parsed" in m, "a fetcher that does not parse fails")
    finally:
        g.update(saved)
    print("PROPOSED_resolver_check_EARN-011 selftest: " + ("PASS" if not bad else "FAIL"))
    for b in bad:
        print("  FAIL:", b)
    return not bad


if __name__ == "__main__" and "--selftest" in sys.argv:
    sys.exit(0 if _earn011_selftest() else 1)

if __name__ == "__main__":
    results = []
    for fn in (_earn011_last_exit_judged, _earn011_fetcher_carries_the_fix, _earn011_last_run_proves_the_fix):
        ok, msg = fn()
        results.append(ok)
        print(f"{'PASS' if ok else 'FAIL'}  {fn.__name__}: {msg}")
    print(f"{sum(results)} of {len(results)} pass (a report, not a gate: exit status is always 0)")
