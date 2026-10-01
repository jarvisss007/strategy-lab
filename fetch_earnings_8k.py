#!/usr/bin/env python
"""fetch_earnings_8k.py — every earnings announcement date the universe ever filed, from EDGAR.

The estate's event study dates earnings by their FOOTPRINT (a gap+volume day), which is only
knowable after the fact. A pre-announcement study needs the date known IN ADVANCE: the 8-K
carrying Item 2.02 is the results announcement itself, and its acceptanceDateTime says whether
the market saw it before or after the close. Writes data/edgar/earnings_8k.json.
SEC etiquette: the desk's UA (stock-radar/fundamentals.py), <= 8 requests a second.

EARN-004 (2026-09-29) — INCREMENTAL. The feed was built once, on 2026-09-17, and this script SKIPPED every ticker
already in the file, so no print filed afterwards ever arrived: on 2026-09-29 the newest print in the whole feed was
2026-09-10 and COST's 2026-09-24 print was missing — on the day EARN-002 made this feed the ONLY source of event counts
for the earnings screens. A stale sole source is worse than a noisy proxy: it fails silently, one quarter at a time.

  * A ticker already held costs ONE request (SEC's filings.recent) and gets only the 8-K Item 2.02 filings NEWER than the
    newest print it holds appended. A ticker not yet held is backfilled to 2010 exactly as before. (A ticker held with no
    events — the foreign filers that never file an 8-K — counts as held: it was backfilled once and found nothing.)
  * NEVER DROP OR REWRITE A PRINT. Held prints are only ever appended to, and a final invariant compares every held print
    before and after and refuses to write if one moved. A held print inside SEC's current window that SEC no longer lists
    (VANISHED) or lists with another acceptance time (CHANGED) is printed LOUD and KEPT; a human decides, never this script.
  * FAIL LOUD. If SEC answers for fewer than half the tickers the run exits 1 and writes NOTHING. Two HTTP 403/429 in a
    row mean SEC is throttling us: stop, do not hammer. Every zero states its reason.
  * ATOMIC. BOOK-001: the feed's lock is taken FIRST, the feed is read under it, and it is replaced whole (write-beside +
    os.replace). An unchanged feed is not rewritten at all, so its mtime still means "a print arrived".
  * SCHEMA IDENTICAL: {ticker: {"cik": "...", "events": [{"date": filing date, "accepted": acceptance stamp (UTC)}]}},
    ascending by date, one event per filing date — byte-for-byte what json.dump wrote before, so every reader is untouched.
  * RUN STAMP: data/edgar/earnings_8k_run.json (git-ignored) records the last SUCCESSFUL run — how many tickers SEC
    answered, the newest filing date SEC showed for the universe, the feed's newest print and sha256. A quiet week has no
    prints; this stamp is how a monitor tells "SEC was asked after the close and had nothing" from "nobody asked".

EARN-004 follow-up (2026-09-30) — THE STAMP OF A PRINT FETCHED ON ITS FILING EVENING. The 18:10 PDT run on 2026-09-30
stored MU's print as accepted 16:02:22. Every held stamp is UTC; 16:02:22 is the New York wall-clock time of that filing.
SEC's own filing header (<ACCEPTANCE-DATETIME>20260930160222) is New York time, SEC's submissions JSON read
2026-09-30T20:02:22.000Z when it was fetched again the next night, and MU's two earlier 8-Ks are held at 20:02Z. This script
stores the first 19 characters of that JSON field unchanged, and nothing else wrote the feed (its sha256 equalled the run
stamp's), so on the filing's own evening the JSON carried the New York digits with a trailing Z; SEC corrected it overnight.
The evening response itself was not captured, because this script printed no stamps — it does now, for every new print.
  * EVERY NEW PRINT IS CHECKED AGAINST THE FILING'S OWN HEADER (an immutable record made at acceptance, one extra request per
    new print). New York wall-clock -> UTC with zoneinfo, so daylight saving is right on both sides of a changeover (696 held
    prints, all 416 dated 2026 and 280 older incl. 60 in March/November, agree with this rule; MU 2026-09-30 is the one that
    does not). JSON stamp == header UTC: stored. JSON stamp == the header's New York digits (the ET-as-Z signature): the
    header's UTC is stored, the print is printed LOUD as NORMALISED and recorded in earnings_8k_corrections.json. Any other
    disagreement, or a header that cannot be read: the print is NOT written (DEFERRED, exit 2) and the run tries again next
    time; a later print is never written past a deferred one, because the feed only ever takes prints newer than its newest.
    A backfilled ticker is checked only for prints newer than FRESH_DAYS, and is held back whole if one cannot be.
  * THE DAILY PASS NO LONGER CALLS A CORRECT PRINT "CHANGED" JUST BECAUSE THE JSON STILL CARRIES THE EVENING FORM: a held
    stamp whose New York digits are what the JSON serves is the same print, and the next night's normal JSON matches exactly.
    A held stamp that is the New York digits themselves (the defect this fixes) is still CHANGED, loudly.
  * ONE-TIME CORRECTIONS ARE EXPLICIT AND NEVER SILENT: `--correct-stamps TICKER:DATE --note "why"` rewrites a held stamp
    only when it equals the filing header's New York digits AND SEC's JSON now serves the header's UTC for that exact
    filing; the daily pass never rewrites. Every correction (and every stamp normalised at write time) is appended to
    data/edgar/earnings_8k_corrections.json, a tracked append-only record with the old value, the new value and the evidence.
    The run stamp carries corrections_on_file and this run's stamp_corrected.

Exit: 0 = every ticker answered, nothing needs a human · 1 = REFUSED, nothing written (SEC unreachable, throttled, or a
book missing) · 2 = the feed is updated but a human should look (a ticker failed, a held print vanished or changed, a CIK
moved, or a new print is DEFERRED). Scheduled by ~/Library/LaunchAgents/com.anupam.edgar-8k.plist, daily 18:10 PT; that job
retries ANY non-zero exit, up to 3 attempts 10 minutes apart (a transient miss clears itself, a vanished print stays loud),
and launchd records the last.
Run: /opt/anaconda3/bin/python fetch_earnings_8k.py            # the incremental update
     /opt/anaconda3/bin/python fetch_earnings_8k.py --correct-stamps MU:2026-09-30 --note "why"   # a disclosed one-time fix
     /opt/anaconda3/bin/python fetch_earnings_8k.py --selftest # offline checks of the merge and stamp rules, writes nothing
"""
import argparse
import copy
import datetime as dt
import gzip
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from zoneinfo import ZoneInfo

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import atomicio   # BOOK-001: write-beside + os.replace, and the book's lock

UA = {"User-Agent": "Anupam Patil research apati077@ucr.edu", "Accept-Encoding": "gzip"}
CIK_MAP = f"{BASE}/data/edgar/cik_map.json"
FEED = f"{BASE}/data/edgar/earnings_8k.json"
RUN = f"{BASE}/data/edgar/earnings_8k_run.json"
CORR = f"{BASE}/data/edgar/earnings_8k_corrections.json"
MIN_GAP_S = 0.12        # 8.3 requests a second at most: under SEC's 10/s ceiling with room for the round trip
MAX_TRIES = 3
BACKFILL_FROM = "2010-01-01"   # older submission pages are skipped for a NEW ticker, as the original build did
FRESH_DAYS = 14         # a BACKFILLED print this recent is checked against its filing header; older ones SEC settled long ago
FMT = "%Y-%m-%dT%H:%M:%S"
ET, UTC = ZoneInfo("America/New_York"), dt.timezone.utc
HDR_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{nodash}/{acc}.hdr.sgml"
ACCEPT_RE = re.compile(r"<ACCEPTANCE-DATETIME>(\d{14})")
CORR_PURPOSE = ("Every one-time correction to data/edgar/earnings_8k.json, in the order made, and every acceptance stamp "
                "normalised at write time (a new print whose JSON stamp disagreed with the filing's own header). The daily pass "
                "never rewrites a held print; a correction is made only by an explicit, noted run of fetch_earnings_8k.py. "
                "Append-only: an entry is never edited or removed.")


class Refused(Exception):
    """SEC is throttling us, or an input book is missing: stop, write nothing."""


# ---------------------------------------------------------------- SEC access
_last_request = [0.0]


def _throttle():
    wait = _last_request[0] + MIN_GAP_S - time.monotonic()
    if wait > 0:
        time.sleep(wait)
    _last_request[0] = time.monotonic()


def _fetch(url, parse):
    """One SEC document: rate-limited, gzip-aware, retried (a body that fails to parse is retried too). HTTP 404 is final
    (no such document). HTTP 403/429 twice means SEC is blocking this address — raise Refused rather than keep asking."""
    blocked, last = 0, None
    for k in range(MAX_TRIES):
        _throttle()
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40)
            raw = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            return parse(raw)
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 404:
                raise
            if e.code in (403, 429):
                blocked += 1
                if blocked >= 2:
                    raise Refused(f"SEC answered HTTP {e.code} twice running for {url} - it is throttling this address; "
                                  f"stopping instead of hammering it")
                time.sleep(30)
        except Exception as e:               # noqa: BLE001 - retried, then re-raised as the ticker's failure
            last = e
        if k < MAX_TRIES - 1:
            time.sleep(1.5 * (k + 1))
    raise last


def get(url):
    return _fetch(url, json.loads)


def get_text(url):
    return _fetch(url, lambda raw: raw.decode("utf-8", "replace"))


# ---------------------------------------------------------------- the stamp rules (pure; tested offline)
def header_times(text):
    """A filing's own SGML header: <ACCEPTANCE-DATETIME>YYYYMMDDHHMMSS is New York wall-clock time (EDGAR's clock).
    -> (et_wall, utc), both 'YYYY-MM-DDTHH:MM:SS'. zoneinfo, so daylight saving is right either side of a changeover."""
    m = ACCEPT_RE.search(text or "")
    if not m:
        raise ValueError("no <ACCEPTANCE-DATETIME> in the filing header")
    et = dt.datetime.strptime(m.group(1), "%Y%m%d%H%M%S").replace(tzinfo=ET)
    return et.strftime(FMT), et.astimezone(UTC).strftime(FMT)


def to_et_wall(utc_stamp):
    """A held UTC stamp -> the New York wall-clock digits SEC's JSON serves for the same filing on its own evening."""
    try:
        return dt.datetime.strptime(utc_stamp, FMT).replace(tzinfo=UTC).astimezone(ET).strftime(FMT)
    except (TypeError, ValueError):
        return None


def check_stamp(cik, r, fetch_text):
    """r: one new print {"date","accepted","_acc"} as SEC's JSON served it. -> (verdict, stamp_to_store, detail).
    ok          the JSON stamp equals the header's UTC
    corrected   the JSON stamp is the header's New York wall-clock digits (the ET-as-UTC signature): the header's UTC is stored
    mismatch    any other disagreement: not written
    unverifiable the header could not be fetched or read: not written"""
    acc = r.get("_acc")
    if not acc:
        return "unverifiable", None, "SEC's JSON gave no accession number for this filing"
    try:
        text = fetch_text(HDR_URL.format(cik=int(cik), nodash=acc.replace("-", ""), acc=acc))
        et_wall, utc = header_times(text)
    except Refused:
        raise
    except Exception as e:                 # noqa: BLE001 - reported as DEFERRED, never swallowed
        return "unverifiable", None, f"{type(e).__name__}: {e}"
    if r["accepted"] == utc:
        return "ok", utc, ""
    if r["accepted"] == et_wall:
        return "corrected", utc, (f"SEC's JSON served the New York wall-clock {r['accepted']} as if it were UTC; the filing "
                                  f"header says {et_wall} ET = {utc} UTC")
    return "mismatch", None, f"SEC's JSON says {r['accepted']}, the filing header says {et_wall} ET = {utc} UTC"


def clean(r):
    """The stored form of a print: the schema's two fields, never the private accession."""
    return {"date": r["date"], "accepted": r["accepted"]}


def verify_new(cik, prints, must, fetch_text):
    """prints: new prints ascending by date. must(r): does this print need its header checked?
    -> (to_store, fixes, deferred). Stops at the FIRST print that cannot be verified and defers it and every later one: the feed
    only ever takes prints newer than its newest, so writing a later print past a deferred one would lose it for good."""
    store, fixes, deferred = [], [], []
    for i, r in enumerate(prints):
        if not must(r):
            store.append(clean(r))
            continue
        verdict, stamp, detail = check_stamp(cik, r, fetch_text)
        if verdict in ("ok", "corrected"):
            store.append({"date": r["date"], "accepted": stamp})
            if verdict == "corrected":
                fixes.append({"date": r["date"], "accession": r["_acc"], "json_stamp": r["accepted"], "stored": stamp,
                              "detail": detail})
            continue
        for p in prints[i:]:
            deferred.append((p["date"], verdict if p is r else "behind a print that cannot be verified",
                             detail if p is r else f"{r['date']} must be written first"))
        break
    return store, fixes, deferred


# ---------------------------------------------------------------- the merge rules (pure; tested offline)
def pull(rec):
    """8-K filings carrying Item 2.02 in one SEC filings block -> [{"date", "accepted", "_acc"}] in SEC's order (the original
    build's rule: exact form '8-K', '2.02' in items, accepted = the first 19 characters of acceptanceDateTime). _acc is the
    accession number, used only to check the stamp against the filing's header; it is never stored."""
    accs = rec.get("accessionNumber") or [None] * len(rec["form"])
    rows = []
    for i, form in enumerate(rec["form"]):
        if form == "8-K" and "2.02" in (rec["items"][i] or ""):
            rows.append({"date": rec["filingDate"][i], "accepted": rec["acceptanceDateTime"][i][:19], "_acc": accs[i]})
    return rows


def dedupe(rows):
    """One event per filing date, ascending — the original build's rule (the last row SEC listed for a date wins)."""
    return sorted({r["date"]: r for r in rows}.values(), key=lambda r: r["date"])


def merge_incremental(held, rec):
    """held: this ticker's events in the feed (never modified here). rec: SEC's filings.recent block.
    -> (new, vanished, changed)
       new      prints filed AFTER the newest one held, deduped exactly as a full rebuild would dedupe them (still carrying _acc)
       vanished held prints inside SEC's window that SEC no longer lists at all
       changed  held prints whose filing date SEC still lists but not with the acceptance stamp held. A held stamp whose
                New York wall-clock digits are what the JSON serves is NOT changed: that is the same print seen on its own
                evening, when the JSON carries the New York digits; the next night's JSON matches the held UTC exactly.
    The window is filing dates strictly after the OLDEST date in the block: recent is cut at a count, so its oldest day can
    be partial and a print dated on it must not be called vanished."""
    prints = pull(rec)
    stamps = {}
    for r in prints:
        stamps.setdefault(r["date"], set()).add(r["accepted"])
    newest = max((e["date"] for e in held), default="")
    new = [r for r in dedupe(prints) if r["date"] > newest]
    floor = min(rec["filingDate"]) if rec["filingDate"] else "9999-12-31"
    inside = [e for e in held if e["date"] > floor]
    vanished = [e for e in inside if e["date"] not in stamps]
    changed = [e for e in inside if e["date"] in stamps and e["accepted"] not in stamps[e["date"]]
               and to_et_wall(e["accepted"]) not in stamps[e["date"]]]
    return new, vanished, changed


def update(feed, cik_map, fetch, fetch_text, today):
    """Apply one incremental pass. feed is MUTATED IN PLACE (appends only) and returned with a report.
    fetch(url) -> parsed SEC JSON; fetch_text(url) -> a filing header; today: a date. A ticker's failure is recorded and
    never aborts the pass."""
    rep = {"attempted": len(cik_map), "answered": 0, "failed": [], "new": {}, "backfilled": [], "vanished": [],
           "changed": [], "cik_moved": [], "not_in_cik_map": sorted(set(feed) - set(cik_map)), "sec_newest_filing": "",
           "stamp_corrected": [], "deferred": []}
    cutoff = (today - dt.timedelta(days=FRESH_DAYS)).isoformat()
    for tk, c in sorted(cik_map.items()):
        held = feed.get(tk)
        if held is not None and held.get("cik") != c:
            rep["cik_moved"].append(f"{tk} (feed {held.get('cik')} vs cik_map {c})")
            continue                                   # two companies must never share one ticker's history
        try:
            d = fetch(f"https://data.sec.gov/submissions/CIK{c}.json")
            recent = d["filings"]["recent"]
            if held is not None:
                new, vanished, changed = merge_incremental(held["events"], recent)
                must = lambda r: True                  # every print an incremental pass would write is checked
            else:                                      # a ticker never held: the full backfill, as the original build did
                rows = pull(recent)
                for f in d["filings"].get("files", []):
                    if f["filingTo"] >= BACKFILL_FROM:
                        rows += pull(fetch(f"https://data.sec.gov/submissions/{f['name']}"))
                new, vanished, changed = dedupe(rows), [], []
                must = lambda r: r["date"] >= cutoff   # only the prints SEC may not have settled yet
            new, fixes, deferred = verify_new(c, new, must, fetch_text)
        except Refused:
            raise
        except Exception as e:                         # noqa: BLE001 - one ticker's failure is reported, not fatal
            rep["failed"].append(f"{tk} ({type(e).__name__})")
            continue
        if held is None and deferred:                  # a half-verified backfill would be permanent: hold the ticker back whole
            rep["failed"].append(f"{tk} (backfill held back: {deferred[0][1]}: {deferred[0][2]})")
            continue
        rep["answered"] += 1
        if recent["filingDate"]:
            rep["sec_newest_filing"] = max(rep["sec_newest_filing"], max(recent["filingDate"]))
        if held is None:
            feed[tk] = {"cik": c, "events": new}
            rep["backfilled"].append(tk)
        elif new:
            held["events"].extend(new)                 # append only: existing prints are never touched
        if new:
            rep["new"][tk] = [r["date"] for r in new]
        rep["vanished"] += [(tk, e["date"], e["accepted"]) for e in vanished]
        rep["changed"] += [(tk, e["date"], e["accepted"]) for e in changed]
        rep["stamp_corrected"] += [dict(f, ticker=tk) for f in fixes]
        rep["deferred"] += [(tk,) + x for x in deferred]
    return feed, rep


def assert_nothing_moved(before, after):
    """The invariant behind 'never drop or rewrite a print': every ticker and print held before is still there, unchanged."""
    for tk, v in before.items():
        w = after.get(tk)
        if w is None or w["cik"] != v["cik"] or w["events"][:len(v["events"])] != v["events"]:
            raise AssertionError(f"INVARIANT BROKEN: {tk}'s held prints changed during the merge - nothing is written")


def assert_only_stamps_changed(before, after, specs):
    """An explicit stamp correction touches the `accepted` of the listed (ticker, date) prints and nothing else, anywhere."""
    want = set(specs)
    if set(before) != set(after):
        raise AssertionError("INVARIANT BROKEN: the set of tickers changed during a stamp correction - nothing is written")
    for tk, v in before.items():
        w = after[tk]
        if w["cik"] != v["cik"] or [e["date"] for e in w["events"]] != [e["date"] for e in v["events"]]:
            raise AssertionError(f"INVARIANT BROKEN: {tk}'s ciks or dates changed during a stamp correction - nothing is written")
        for a, b in zip(v["events"], w["events"]):
            if a != b and (tk, a["date"]) not in want:
                raise AssertionError(f"INVARIANT BROKEN: {tk} {a['date']} changed but was not listed - nothing is written")


def correct_stamps(feed, specs, fetch, fetch_text):
    """A one-time, disclosed correction of held stamps — never part of the daily pass. specs: [(ticker, date)]. A stamp is
    corrected ONLY when all hold: the print is held exactly once; the held stamp equals the New York wall-clock digits of the
    filing's own header (the known ET-as-UTC signature); exactly one 8-K Item 2.02 filing of that date matches; and SEC's JSON
    now serves the header's UTC for it. Anything else raises ValueError and nothing is written. feed is changed in place at
    those `accepted` fields only. -> entries for earnings_8k_corrections.json."""
    entries = []
    for tk, date in specs:
        v = feed.get(tk)
        if v is None:
            raise ValueError(f"{tk} is not in the feed")
        held = [e for e in v["events"] if e["date"] == date]
        if len(held) != 1:
            raise ValueError(f"{tk} holds {len(held)} prints dated {date}, not exactly one")
        e = held[0]
        was = e["accepted"]
        d = fetch(f"https://data.sec.gov/submissions/CIK{v['cik']}.json")
        blocks = [d["filings"]["recent"]] + [fetch(f"https://data.sec.gov/submissions/{p['name']}") for p in d["filings"].get("files", [])
                                             if p.get("filingFrom", "") <= date <= p.get("filingTo", "")]
        cands = [r for b in blocks for r in pull(b) if r["date"] == date]
        match = []
        for r in cands:
            et_wall, utc = header_times(fetch_text(HDR_URL.format(cik=int(v["cik"]), nodash=r["_acc"].replace("-", ""), acc=r["_acc"])))
            if et_wall == was:
                match.append((r, et_wall, utc))
        if len(match) != 1:
            raise ValueError(f"{tk} {date}: {len(match)} of SEC's {len(cands)} filings that day have a header whose New York time "
                             f"equals the held stamp {was}; refusing to guess")
        r, et_wall, utc = match[0]
        if r["accepted"] != utc:
            raise ValueError(f"{tk} {date}: SEC's JSON serves {r['accepted']}, not the header's UTC {utc} - not corrected")
        e["accepted"] = utc
        entries.append({"kind": "stamp", "ticker": tk, "date": date, "accession": r["_acc"], "was": was, "now": utc,
                        "evidence": f"filing header <ACCEPTANCE-DATETIME> {et_wall} New York = {utc} UTC; SEC's JSON serves {r['accepted']}"})
    return entries


# ---------------------------------------------------------------- the corrections record
def corrections_on_file():
    try:
        return len(json.load(open(CORR)).get("corrections", []))
    except (OSError, ValueError):
        return 0


def append_corrections(entries):
    """Append-only, under the record's own lock, replaced whole. The feed is written first; if this fails the caller says so LOUD."""
    if not entries:
        return
    atomicio.hold_book(CORR)
    doc = json.load(open(CORR)) if os.path.exists(CORR) else {"purpose": CORR_PURPOSE, "corrections": []}
    doc["corrections"].extend(entries)
    atomicio.atomic_write_text(CORR, json.dumps(doc, indent=1) + "\n")


# ---------------------------------------------------------------- run
def stats(feed):
    dates = [e["date"] for v in feed.values() for e in v["events"]]
    return len(dates), max(dates) if dates else ""


def main(argv):
    ap = argparse.ArgumentParser(description="Incremental EDGAR 8-K Item 2.02 feed (EARN-004).")
    ap.add_argument("--selftest", action="store_true", help="offline checks, writes nothing")
    ap.add_argument("--correct-stamps", metavar="TICKER:DATE[,TICKER:DATE]",
                    help="one-time, disclosed correction of held ET-as-UTC stamps (needs --note)")
    ap.add_argument("--note", default="", help="why: written to earnings_8k_corrections.json with the correction")
    args = ap.parse_args(argv)
    if args.selftest:
        return 0 if selftest() else 1
    specs = []
    if args.correct_stamps:
        try:
            specs = [tuple(s.strip().split(":")) for s in args.correct_stamps.split(",") if s.strip()]
            assert specs and all(len(s) == 2 for s in specs)
        except AssertionError:
            print("REFUSED: --correct-stamps wants TICKER:DATE[,TICKER:DATE]")
            return 1
        if not args.note.strip():
            print("REFUSED: a correction must carry --note \"why\": it is written to earnings_8k_corrections.json and is never silent")
            return 1
    if not os.path.exists(CIK_MAP):
        print(f"REFUSED: {CIK_MAP} is missing - nothing to fetch for; nothing written")
        return 1
    atomicio.hold_book(FEED)                           # BOOK-001: the lock FIRST, then the read
    cik_map = json.load(open(CIK_MAP))
    feed = json.load(open(FEED)) if os.path.exists(FEED) else {}
    explicit = []
    try:
        if specs:
            asked = copy.deepcopy(feed)
            explicit = correct_stamps(feed, specs, get, get_text)
            assert_only_stamps_changed(asked, feed, specs)
    except (ValueError, AssertionError) as e:
        print(f"REFUSED: {e}. Nothing written.")
        return 1
    except Refused as e:
        print(f"REFUSED: {e}. Nothing written.")
        return 1
    before = copy.deepcopy(feed)                       # AFTER an explicit correction: the invariant guards the daily pass that follows
    n0, newest0 = stats(feed)
    try:
        feed, rep = update(feed, cik_map, get, get_text, dt.date.today())
        assert_nothing_moved(before, feed)
    except Refused as e:
        print(f"REFUSED: {e}. Nothing written.")
        return 1
    except AssertionError as e:
        print(f"REFUSED: {e}")
        return 1
    if rep["attempted"] == 0 or rep["answered"] * 2 < rep["attempted"]:
        print(f"REFUSED: SEC answered for {rep['answered']} of {rep['attempted']} tickers - fewer than half. "
              f"Nothing written; the feed is exactly as it was ({n0} prints, newest {newest0}). "
              f"Failed: {', '.join(rep['failed'][:12]) or 'none listed (empty ticker map)'}")
        return 1
    n_new = sum(len(v) for v in rep["new"].values())
    if n_new or rep["backfilled"] or explicit:
        atomicio.atomic_write_text(FEED, json.dumps(feed))   # the format the feed always had: json.dump defaults, no newline
    n1, newest1 = stats(feed)
    sha = hashlib.sha256(open(FEED, "rb").read()).hexdigest()
    at = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    ledger = [dict(e, at=at, note=args.note.strip(), feed_sha256_after=sha) for e in explicit]
    ledger += [{"kind": "stamp_at_write", "ticker": f["ticker"], "date": f["date"], "accession": f["accession"],
                "was": f["json_stamp"], "now": f["stored"], "evidence": f["detail"], "at": at,
                "note": "normalised at write time: the new print's JSON stamp was the filing header's New York wall-clock", "feed_sha256_after": sha}
               for f in rep["stamp_corrected"]]
    ledger_failed = None
    try:
        append_corrections(ledger)
    except Exception as e:                             # noqa: BLE001 - the feed is already written: say so LOUD, never swallow
        ledger_failed = f"{type(e).__name__}: {e}"
    run = {"finished_at": at, "attempted": rep["attempted"], "answered": rep["answered"], "failed": rep["failed"],
           "sec_newest_filing": rep["sec_newest_filing"], "new_prints": n_new, "tickers_with_new": len(rep["new"]),
           "backfilled": rep["backfilled"], "vanished": rep["vanished"], "changed": rep["changed"],
           "cik_moved": rep["cik_moved"], "deferred": rep["deferred"], "stamp_corrected": rep["stamp_corrected"],
           "corrections_this_run": explicit, "corrections_on_file": corrections_on_file(),
           "prints_before": n0, "prints_total": n1, "newest_print": newest1, "feed_sha256": sha}
    atomicio.atomic_write_text(RUN, json.dumps(run, indent=1) + "\n")
    print(f"earnings_8k: SEC answered {rep['answered']}/{rep['attempted']} tickers (its index shows filings through "
          f"{rep['sec_newest_filing']}); {n_new} new print(s) in {len(rep['new'])} ticker(s); "
          f"{n0} -> {n1} prints, newest {newest0} -> {newest1}"
          + ("" if (n_new or explicit) else " · nothing new: the feed is unchanged and was not rewritten"))
    for tk, ds in sorted(rep["new"].items()):
        print(f"  new  {tk}: {', '.join(ds)}  (each stamp checked against the filing's own header)")
    attention = 0
    for e in explicit:
        print(f"  CORRECTED (explicit, noted) {e['ticker']} {e['date']}: {e['was']} -> {e['now']}  [{e['evidence']}]")
    for f in rep["stamp_corrected"]:
        print(f"  NOTE STAMP NORMALISED {f['ticker']} {f['date']}: {f['detail']}; stored {f['stored']} (recorded in earnings_8k_corrections.json)")
    for tk in rep["backfilled"]:
        print(f"  backfilled a ticker not previously held: {tk}")
    for tk, d, a in rep["vanished"]:
        attention += 1
        print(f"ATTENTION VANISHED {tk} {d} (accepted {a}): held in the feed but absent from SEC's current filing list "
              f"for that window - KEPT, not deleted. Look at it.")
    for tk, d, a in rep["changed"]:
        attention += 1
        print(f"ATTENTION CHANGED {tk} {d}: the feed holds accepted {a}, SEC lists that date with another stamp - KEPT as held.")
    for x in rep["cik_moved"]:
        attention += 1
        print(f"ATTENTION CIK MOVED {x}: not fetched - two companies must not share one ticker's history.")
    for x in rep["failed"]:
        attention += 1
        print(f"ATTENTION FAILED {x}: SEC did not answer for this ticker; its prints are as held.")
    for tk, d, verdict, detail in rep["deferred"]:
        attention += 1
        print(f"ATTENTION DEFERRED {tk} {d}: NOT written ({verdict}: {detail}); it is retried on the next run.")
    if ledger_failed:
        attention += 1
        print(f"ATTENTION LEDGER: the feed was written but earnings_8k_corrections.json could not be ({ledger_failed}) - "
              f"record these by hand now: {json.dumps(ledger)}")
    for tk in rep["not_in_cik_map"]:
        print(f"  note: {tk} is in the feed but not in cik_map.json - kept, not fetched")
    return 2 if attention else 0


# ---------------------------------------------------------------- selftest (offline)
def selftest():
    bad = []

    def check(cond, msg):
        if not cond:
            bad.append(msg)

    def block(rows):
        """rows: (filingDate, form, items, accepted19[, accession]) -> a filings.recent block, newest first like SEC's."""
        rows = [r if len(r) == 5 else r + (f"0000000000-26-{k:06d}",) for k, r in enumerate(rows)]
        rows.sort(key=lambda r: (r[0], r[3]), reverse=True)
        return {"filingDate": [r[0] for r in rows], "form": [r[1] for r in rows], "items": [r[2] for r in rows],
                "acceptanceDateTime": [r[3] + ".000Z" for r in rows], "accessionNumber": [r[4] for r in rows]}

    E = lambda d, t="20:17:37": {"date": d, "accepted": f"{d}T{t}"}
    R = lambda d, f="8-K", i="2.02,9.01", t="20:17:37", acc=None: (d, f, i, f"{d}T{t}") + ((acc,) if acc else ())
    TODAY = dt.date(2026, 9, 30)
    hdr = lambda digits: f"<SEC-HEADER>x\n<ACCEPTANCE-DATETIME>{digits}\n<ACCESSION-NUMBER>y\n"
    # 1. an incremental pass appends only what is newer, filters to 8-K + 2.02, and never touches a held print
    held = [E("2026-03-05"), E("2026-05-28")]
    rec = block([R("2026-09-24"), R("2026-09-25", i="5.02"), R("2026-09-26", f="8-K/A"), R("2026-05-28"), R("2026-03-05"),
                 R("2026-01-15", i="7.01"), R("2025-01-02")])
    new, vanished, changed = merge_incremental(held, rec)
    check([r["date"] for r in new] == ["2026-09-24"] and not vanished and not changed, "new 2.02 print appended; non-2.02 and 8-K/A ignored")
    check(clean(new[0]) == {"date": "2026-09-24", "accepted": "2026-09-24T20:17:37"} and "_acc" not in clean(new[0]),
          "the stored print carries the schema's date/accepted only, accepted cut to 19 chars, never the accession")
    # 2. a held print SEC no longer lists inside its window is VANISHED, and an older one outside the window is not judged
    held2 = [E("2024-06-01"), E("2026-03-05"), E("2026-05-28")]
    rec2 = block([R("2026-05-28"), R("2025-10-01", i="9.01")])            # window starts 2025-10-01; 2026-03-05 missing
    n2, v2, c2 = merge_incremental(held2, rec2)
    check([e["date"] for e in v2] == ["2026-03-05"], "a held print missing from SEC's window is VANISHED")
    check("2024-06-01" not in [e["date"] for e in v2 + c2], "a held print older than SEC's window is not judged")
    # 3. the oldest day of the window may be partial: a print dated ON it is not called vanished
    n3, v3, c3 = merge_incremental([E("2025-10-01")], block([R("2026-05-28"), R("2025-10-01", i="9.01")]))
    check(not v3, "a held print on the window's oldest day is not called vanished")
    # 4. CHANGED: same date, other acceptance stamp; a second filing the same day is not a change
    n4, v4, c4 = merge_incremental([E("2026-05-28", "20:17:37")], block([R("2026-05-28", t="21:00:00"), R("2026-05-27")]))
    check([e["date"] for e in c4] == ["2026-05-28"], "a held date SEC lists with another stamp is CHANGED")
    n5, v5, c5 = merge_incremental([E("2026-05-28", "20:17:37")], block([R("2026-05-28", t="20:17:37"), R("2026-05-28", t="21:00:00"), R("2026-05-27")]))
    check(not c5 and not n5, "two filings on one date with the held stamp among them: not changed, nothing new")
    # 5. same-date dedupe is the original build's: the last row SEC lists wins
    check([clean(x) for x in dedupe([{"date": "d1", "accepted": "a"}, {"date": "d1", "accepted": "b"}, {"date": "d0", "accepted": "c"}])]
          == [{"date": "d0", "accepted": "c"}, {"date": "d1", "accepted": "b"}], "dedupe: ascending, last row per date wins")
    # 6. the stamp rules: the header is New York wall-clock; zoneinfo gets both sides of daylight saving right
    check(header_times(hdr("20260930160222")) == ("2026-09-30T16:02:22", "2026-09-30T20:02:22"), "summer filing: 16:02:22 ET is 20:02:22 UTC")
    check(header_times(hdr("20260105160222"))[1] == "2026-01-05T21:02:22", "winter filing: 16:02:22 ET is 21:02:22 UTC")
    check(header_times(hdr("20260308013000"))[1] == "2026-03-08T06:30:00" and header_times(hdr("20260308033000"))[1] == "2026-03-08T07:30:00",
          "either side of the March changeover")
    check(header_times(hdr("20261101003000"))[1] == "2026-11-01T04:30:00" and header_times(hdr("20261102093000"))[1] == "2026-11-02T14:30:00",
          "either side of the November changeover")
    check(to_et_wall("2026-09-30T20:02:22") == "2026-09-30T16:02:22" and to_et_wall("garbage") is None, "a held UTC stamp's New York digits")
    try:
        header_times("no header here"); check(False, "a header without ACCEPTANCE-DATETIME must raise")
    except ValueError:
        pass
    # 7. check_stamp: ok / corrected (the ET-as-Z signature) / mismatch / unverifiable
    P = lambda t: {"date": "2026-09-30", "accepted": f"2026-09-30T{t}", "_acc": "0000723125-26-000018"}
    ftext = lambda url: hdr("20260930160222")
    check(check_stamp("0000723125", P("20:02:22"), ftext)[0] == "ok", "JSON stamp equal to the header's UTC is ok")
    v, s, det = check_stamp("0000723125", P("16:02:22"), ftext)
    check(v == "corrected" and s == "2026-09-30T20:02:22" and "New York wall-clock" in det, "JSON stamp equal to the header's New York digits is corrected to UTC")
    check(check_stamp("0000723125", P("18:00:00"), ftext)[0] == "mismatch", "any other disagreement is a mismatch, not guessed at")
    check(check_stamp("0000723125", dict(P("20:02:22"), _acc=None), ftext)[0] == "unverifiable", "no accession: unverifiable")

    def dead(url):
        raise ConnectionError("dead")
    check(check_stamp("0000723125", P("20:02:22"), dead)[0] == "unverifiable", "a header that cannot be fetched is unverifiable")
    # 8. verify_new: a deferred print holds back every later one (the feed only takes prints newer than its newest)
    seq = [{"date": "2026-09-28", "accepted": "2026-09-28T20:00:00", "_acc": "A-1"}, {"date": "2026-09-29", "accepted": "2026-09-29T20:00:00", "_acc": "A-2"},
           {"date": "2026-09-30", "accepted": "2026-09-30T20:00:00", "_acc": "A-3"}]
    heads = {"A-1": hdr("20260928160000"), "A-3": hdr("20260930160000")}          # A-2's header is missing

    def ft(url):
        for k, v in heads.items():
            if url.endswith(f"/{k}.hdr.sgml"):
                return v
        raise KeyError(url)
    store, fixes, deferred = verify_new("0000000001", seq, lambda r: True, ft)
    check([s["date"] for s in store] == ["2026-09-28"] and [d[0] for d in deferred] == ["2026-09-29", "2026-09-30"],
          "the first unverifiable print and every later one are deferred")
    # 9. update(): held ticker incremental, new ticker backfilled through its older pages, empty-held ticker incremental, failure isolated
    pages = {"https://data.sec.gov/submissions/CIK0000000001.json": {"filings": {"recent": block([R("2026-09-24", acc="A-24"), R("2026-05-28")]), "files": []}},
             "https://data.sec.gov/submissions/CIK0000000002.json": {"filings": {"recent": block([R("2026-08-01")]), "files": [
                 {"name": "old-001.json", "filingTo": "2015-01-01"}, {"name": "ancient.json", "filingTo": "2009-12-31"}]}},
             "https://data.sec.gov/submissions/old-001.json": block([R("2014-06-01"), R("2012-01-05")]),
             "https://data.sec.gov/submissions/CIK0000000003.json": {"filings": {"recent": block([R("2026-09-10", acc="A-10")]), "files": []}}}
    calls, hdr_calls = [], []

    def fake(url):
        calls.append(url)
        if url.endswith("CIK0000000004.json"):
            raise ConnectionError("dead")
        return pages[url]

    def fake_text(url):
        hdr_calls.append(url)
        return hdr("20260924161737") if "A24" in url or "A-24" in url else hdr("20260910161737")
    feed = {"AAA": {"cik": "0000000001", "events": [E("2026-05-28")]}, "EMPTY": {"cik": "0000000003", "events": []}}
    before = json.loads(json.dumps(feed))
    cmap = {"AAA": "0000000001", "NEW": "0000000002", "EMPTY": "0000000003", "DEAD": "0000000004"}
    out, rep = update(feed, cmap, fake, fake_text, TODAY)
    assert_nothing_moved(before, out)
    check([e["date"] for e in out["AAA"]["events"]] == ["2026-05-28", "2026-09-24"], "held ticker: old print first, new appended")
    check(all(set(e) == {"date", "accepted"} for v in out.values() for e in v["events"]), "no private key ever reaches the feed")
    check([e["date"] for e in out["NEW"]["events"]] == ["2012-01-05", "2014-06-01", "2026-08-01"], "new ticker backfilled, pre-2010 page skipped")
    check([e["date"] for e in out["EMPTY"]["events"]] == ["2026-09-10"], "a ticker held with no events picks up a first print incrementally")
    check(not any("ancient" in u for u in calls) and sum(1 for u in calls if "CIK0000000001" in u) == 1, "a held ticker costs one request; pre-2010 pages are not fetched")
    check(len(hdr_calls) == 2, "headers fetched only for the two incremental prints; the backfilled prints are all older than FRESH_DAYS")
    check(rep["answered"] == 3 and rep["attempted"] == 4 and rep["failed"] == ["DEAD (ConnectionError)"], "a failing ticker is recorded, not fatal")
    check(rep["sec_newest_filing"] == "2026-09-24" and not rep["stamp_corrected"] and not rep["deferred"], "newest filing date recorded; nothing corrected or deferred")
    # 10. THE SAME-EVENING PATH: SEC's JSON serves the New York digits with a Z for MU's print; the header says otherwise
    mu_hdr = lambda url: hdr("20260930160222") if "26-000018" in url else hdr("20260624160201")
    evening = {"https://data.sec.gov/submissions/CIK0000723125.json": {"filings": {"recent": block([
        R("2026-09-30", t="16:02:22", acc="0000723125-26-000018"), R("2026-06-24", t="20:02:01", acc="0000723125-26-000013")]), "files": []}}}
    mu_feed = {"MU": {"cik": "0000723125", "events": [E("2026-06-24", "20:02:01")]}}
    o10, r10 = update(mu_feed, {"MU": "0000723125"}, lambda u: evening[u], mu_hdr, TODAY)
    check(o10["MU"]["events"][-1] == {"date": "2026-09-30", "accepted": "2026-09-30T20:02:22"}, "the evening print is stored with the UTC stamp, not the New York digits")
    check(len(r10["stamp_corrected"]) == 1 and r10["stamp_corrected"][0]["json_stamp"] == "2026-09-30T16:02:22"
          and r10["stamp_corrected"][0]["stored"] == "2026-09-30T20:02:22" and r10["stamp_corrected"][0]["accession"] == "0000723125-26-000018",
          "the normalisation is recorded with both values and the accession, never silent")
    # ... a SECOND run the same evening (a retry, a kickstart): the JSON still serves the New York digits; the held UTC print is the same print
    o10b, r10b = update(copy.deepcopy(o10), {"MU": "0000723125"}, lambda u: evening[u], mu_hdr, TODAY)
    check(not r10b["changed"] and not r10b["new"], "same evening, second run: the correctly stored print is not CHANGED")
    # ... the next night SEC's JSON is normal and matches exactly
    nextday = {"https://data.sec.gov/submissions/CIK0000723125.json": {"filings": {"recent": block([
        R("2026-09-30", t="20:02:22", acc="0000723125-26-000018"), R("2026-06-24", t="20:02:01", acc="0000723125-26-000013")]), "files": []}}}
    o10c, r10c = update(copy.deepcopy(o10), {"MU": "0000723125"}, lambda u: nextday[u], mu_hdr, TODAY)
    check(not r10c["changed"] and not r10c["new"], "next night, normal JSON: unchanged")
    # ... and the DEFECT itself still shows: a held New York digits stamp against the normal JSON is CHANGED, loudly
    wrong = {"MU": {"cik": "0000723125", "events": [E("2026-06-24", "20:02:01"), {"date": "2026-09-30", "accepted": "2026-09-30T16:02:22"}]}}
    o10d, r10d = update(wrong, {"MU": "0000723125"}, lambda u: nextday[u], mu_hdr, TODAY)
    check([c[1] for c in r10d["changed"]] == ["2026-09-30"] and o10d["MU"]["events"][-1]["accepted"] == "2026-09-30T16:02:22",
          "the held wrong stamp is flagged CHANGED and KEPT (the daily pass never rewrites)")
    # 11. an unreadable header defers the print: not written, newest not advanced, SEC's answer still counted
    o11, r11 = update({"MU": {"cik": "0000723125", "events": [E("2026-06-24", "20:02:01")]}}, {"MU": "0000723125"}, lambda u: evening[u], dead, TODAY)
    check(len(o11["MU"]["events"]) == 1 and [d[1] for d in r11["deferred"]] == ["2026-09-30"] and r11["answered"] == 1, "unverifiable print is deferred, not written")
    # 12. a backfill checks only prints newer than FRESH_DAYS and holds the ticker back whole if one cannot be checked
    bf = {"https://data.sec.gov/submissions/CIK0000000009.json": {"filings": {"recent": block([R("2026-09-29", acc="A-29"), R("2026-03-01")]), "files": []}}}
    o12, r12 = update({}, {"BF": "0000000009"}, lambda u: bf[u], lambda u: hdr("20260929161737"), TODAY)
    check([e["date"] for e in o12["BF"]["events"]] == ["2026-03-01", "2026-09-29"], "backfill with a verifiable fresh print")
    o12b, r12b = update({}, {"BF": "0000000009"}, lambda u: bf[u], dead, TODAY)
    check("BF" not in o12b and r12b["answered"] == 0 and r12b["failed"] and "held back" in r12b["failed"][0], "a backfill with an unverifiable fresh print is held back whole")
    # 13. the invariants catch a rewrite, a drop and a lost ticker; the stamp-correction invariant catches anything not listed
    for name, mutate in (("rewrite", lambda f: f["AAA"]["events"][0].update(accepted="x")), ("drop", lambda f: f["AAA"]["events"].pop(0)),
                         ("lost ticker", lambda f: f.pop("AAA"))):
        f2 = json.loads(json.dumps(before)); mutate(f2)
        try:
            assert_nothing_moved(before, f2); check(False, f"the invariant missed a {name}")
        except AssertionError:
            pass
    base = {"AAA": {"cik": "1", "events": [E("2026-05-28"), E("2026-06-01")]}}
    ok_f = copy.deepcopy(base); ok_f["AAA"]["events"][0]["accepted"] = "2026-05-28T16:17:37"
    assert_only_stamps_changed(base, ok_f, [("AAA", "2026-05-28")])
    for name, mutate in (("a stamp that was not listed", lambda f: f["AAA"]["events"][1].update(accepted="x")),
                         ("a dropped print", lambda f: f["AAA"]["events"].pop()), ("a date change", lambda f: f["AAA"]["events"][1].update(date="2026-06-02"))):
        f3 = copy.deepcopy(ok_f); mutate(f3)
        try:
            assert_only_stamps_changed(base, f3, [("AAA", "2026-05-28")]); check(False, f"the correction invariant missed {name}")
        except AssertionError:
            pass
    # 14. correct_stamps: only the ET-as-UTC signature, only when SEC's JSON now agrees with the header, exactly one match
    now_ok = {"https://data.sec.gov/submissions/CIK0000723125.json": {"filings": {"recent": block([R("2026-09-30", t="20:02:22", acc="0000723125-26-000018")]), "files": []}}}
    cf = {"MU": {"cik": "0000723125", "events": [E("2026-06-24", "20:02:01"), {"date": "2026-09-30", "accepted": "2026-09-30T16:02:22"}]}}
    asked = copy.deepcopy(cf)
    ent = correct_stamps(cf, [("MU", "2026-09-30")], lambda u: now_ok[u], mu_hdr)
    assert_only_stamps_changed(asked, cf, [("MU", "2026-09-30")])
    check(cf["MU"]["events"][-1]["accepted"] == "2026-09-30T20:02:22" and len(ent) == 1 and ent[0]["was"] == "2026-09-30T16:02:22"
          and ent[0]["now"] == "2026-09-30T20:02:22" and "New York" in ent[0]["evidence"], "the signature is corrected and described")
    for name, feed_x, pages_x, hdr_x in (
            ("SEC's JSON still serves the New York digits", {"MU": {"cik": "0000723125", "events": [{"date": "2026-09-30", "accepted": "2026-09-30T16:02:22"}]}}, evening, mu_hdr),
            ("the held stamp is not the header's New York digits", {"MU": {"cik": "0000723125", "events": [{"date": "2026-09-30", "accepted": "2026-09-30T18:00:00"}]}}, now_ok, mu_hdr),
            ("the print is not held", {"MU": {"cik": "0000723125", "events": [E("2026-06-24")]}}, now_ok, mu_hdr),
            ("an unknown ticker", {}, now_ok, mu_hdr)):
        try:
            correct_stamps(copy.deepcopy(feed_x), [("MU", "2026-09-30")], lambda u, p=pages_x: p[u], hdr_x); check(False, f"correct_stamps must refuse when {name}")
        except ValueError:
            pass
    # 15. the throttle keeps under SEC's 10 requests a second; the feed's format is json.dumps defaults
    check(MIN_GAP_S >= 0.1, "request spacing is at least 0.1s (<= 10/s)")
    check(json.dumps({"a": [1]}) == '{"a": [1]}', "json.dumps default format is the feed's format")
    print("fetch_earnings_8k selftest: " + ("PASS" if not bad else "FAIL"))
    for b in bad:
        print("  FAIL:", b)
    return not bad


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
