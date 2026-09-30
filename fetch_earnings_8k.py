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

Exit: 0 = every ticker answered, nothing needs a human · 1 = REFUSED, nothing written (SEC unreachable, throttled, or a
book missing) — the launchd job retries it · 2 = the feed is updated but a human should look (a ticker failed, a held print
vanished or changed, or a CIK moved). Scheduled by ~/Library/LaunchAgents/com.anupam.edgar-8k.plist, daily 18:10 PT.
Run: /opt/anaconda3/bin/python fetch_earnings_8k.py            # the incremental update
     /opt/anaconda3/bin/python fetch_earnings_8k.py --selftest # offline checks of the merge rules, writes nothing
"""
import datetime as dt
import gzip
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import atomicio   # BOOK-001: write-beside + os.replace, and the book's lock

UA = {"User-Agent": "Anupam Patil research apati077@ucr.edu", "Accept-Encoding": "gzip"}
CIK_MAP = f"{BASE}/data/edgar/cik_map.json"
FEED = f"{BASE}/data/edgar/earnings_8k.json"
RUN = f"{BASE}/data/edgar/earnings_8k_run.json"
MIN_GAP_S = 0.12        # 8.3 requests a second at most: under SEC's 10/s ceiling with room for the round trip
MAX_TRIES = 3
BACKFILL_FROM = "2010-01-01"   # older submission pages are skipped for a NEW ticker, as the original build did


class Refused(Exception):
    """SEC is throttling us, or an input book is missing: stop, write nothing."""


# ---------------------------------------------------------------- SEC access
_last_request = [0.0]


def _throttle():
    wait = _last_request[0] + MIN_GAP_S - time.monotonic()
    if wait > 0:
        time.sleep(wait)
    _last_request[0] = time.monotonic()


def get(url):
    """One SEC JSON document: rate-limited, gzip-aware, retried. HTTP 404 is final (no such document). HTTP 403/429 twice
    means SEC is blocking this address — raise Refused rather than keep asking."""
    blocked, last = 0, None
    for k in range(MAX_TRIES):
        _throttle()
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40)
            raw = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            return json.loads(raw)
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


# ---------------------------------------------------------------- the merge rules (pure; tested offline)
def pull(rec):
    """8-K filings carrying Item 2.02 in one SEC filings block -> [{"date", "accepted"}] in SEC's order (unchanged from the
    original build: exact form '8-K', '2.02' in items, accepted = the first 19 characters of acceptanceDateTime)."""
    rows = []
    for i, form in enumerate(rec["form"]):
        if form == "8-K" and "2.02" in (rec["items"][i] or ""):
            rows.append({"date": rec["filingDate"][i], "accepted": rec["acceptanceDateTime"][i][:19]})
    return rows


def dedupe(rows):
    """One event per filing date, ascending — the original build's rule (the last row SEC listed for a date wins)."""
    return sorted({r["date"]: r for r in rows}.values(), key=lambda r: r["date"])


def merge_incremental(held, rec):
    """held: this ticker's events in the feed (never modified here). rec: SEC's filings.recent block.
    -> (new, vanished, changed)
       new      prints filed AFTER the newest one held, deduped exactly as a full rebuild would dedupe them
       vanished held prints inside SEC's window that SEC no longer lists at all
       changed  held prints whose filing date SEC still lists but not with the acceptance stamp held
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
    changed = [e for e in inside if e["date"] in stamps and e["accepted"] not in stamps[e["date"]]]
    return new, vanished, changed


def update(feed, cik_map, fetch):
    """Apply one incremental pass. feed is MUTATED IN PLACE (appends only) and returned with a report.
    fetch(url) -> parsed SEC JSON. A ticker's failure is recorded and never aborts the pass."""
    rep = {"attempted": len(cik_map), "answered": 0, "failed": [], "new": {}, "backfilled": [], "vanished": [],
           "changed": [], "cik_moved": [], "not_in_cik_map": sorted(set(feed) - set(cik_map)), "sec_newest_filing": ""}
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
            else:                                      # a ticker never held: the full backfill, as the original build did
                rows = pull(recent)
                for f in d["filings"].get("files", []):
                    if f["filingTo"] >= BACKFILL_FROM:
                        rows += pull(fetch(f"https://data.sec.gov/submissions/{f['name']}"))
                new, vanished, changed = dedupe(rows), [], []
        except Refused:
            raise
        except Exception as e:                         # noqa: BLE001 - one ticker's failure is reported, not fatal
            rep["failed"].append(f"{tk} ({type(e).__name__})")
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
    return feed, rep


def assert_nothing_moved(before, after):
    """The invariant behind 'never drop or rewrite a print': every ticker and print held before is still there, unchanged."""
    for tk, v in before.items():
        w = after.get(tk)
        if w is None or w["cik"] != v["cik"] or w["events"][:len(v["events"])] != v["events"]:
            raise AssertionError(f"INVARIANT BROKEN: {tk}'s held prints changed during the merge - nothing is written")


# ---------------------------------------------------------------- run
def stats(feed):
    dates = [e["date"] for v in feed.values() for e in v["events"]]
    return len(dates), max(dates) if dates else ""


def main(argv):
    if "--selftest" in argv:
        return 0 if selftest() else 1
    if not os.path.exists(CIK_MAP):
        print(f"REFUSED: {CIK_MAP} is missing - nothing to fetch for; nothing written")
        return 1
    atomicio.hold_book(FEED)                           # BOOK-001: the lock FIRST, then the read
    cik_map = json.load(open(CIK_MAP))
    feed = json.load(open(FEED)) if os.path.exists(FEED) else {}
    before = json.loads(json.dumps(feed))              # an independent copy for the invariant
    n0, newest0 = stats(feed)
    try:
        feed, rep = update(feed, cik_map, get)
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
    if n_new or rep["backfilled"]:
        atomicio.atomic_write_text(FEED, json.dumps(feed))   # the format the feed always had: json.dump defaults, no newline
    n1, newest1 = stats(feed)
    run = {"finished_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
           "attempted": rep["attempted"], "answered": rep["answered"], "failed": rep["failed"],
           "sec_newest_filing": rep["sec_newest_filing"], "new_prints": n_new, "tickers_with_new": len(rep["new"]),
           "backfilled": rep["backfilled"], "vanished": rep["vanished"], "changed": rep["changed"],
           "cik_moved": rep["cik_moved"], "prints_before": n0, "prints_total": n1, "newest_print": newest1,
           "feed_sha256": hashlib.sha256(open(FEED, "rb").read()).hexdigest()}
    atomicio.atomic_write_text(RUN, json.dumps(run, indent=1) + "\n")
    print(f"earnings_8k: SEC answered {rep['answered']}/{rep['attempted']} tickers (its index shows filings through "
          f"{rep['sec_newest_filing']}); {n_new} new print(s) in {len(rep['new'])} ticker(s); "
          f"{n0} -> {n1} prints, newest {newest0} -> {newest1}"
          + ("" if n_new else " · nothing new: the feed is unchanged and was not rewritten"))
    for tk, ds in sorted(rep["new"].items()):
        print(f"  new  {tk}: {', '.join(ds)}")
    attention = 0
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
        """rows: (filingDate, form, items, accepted19) -> a filings.recent block, newest first like SEC's."""
        rows = sorted(rows, reverse=True)
        return {"filingDate": [r[0] for r in rows], "form": [r[1] for r in rows], "items": [r[2] for r in rows],
                "acceptanceDateTime": [r[3] + ".000Z" for r in rows]}

    E = lambda d, t="20:17:37": {"date": d, "accepted": f"{d}T{t}"}
    R = lambda d, f="8-K", i="2.02,9.01", t="20:17:37": (d, f, i, f"{d}T{t}")
    # 1. an incremental pass appends only what is newer, filters to 8-K + 2.02, and never touches a held print
    held = [E("2026-03-05"), E("2026-05-28")]
    rec = block([R("2026-09-24"), R("2026-09-25", i="5.02"), R("2026-09-26", f="8-K/A"), R("2026-05-28"), R("2026-03-05"),
                 R("2026-01-15", i="7.01"), R("2025-01-02")])
    new, vanished, changed = merge_incremental(held, rec)
    check([r["date"] for r in new] == ["2026-09-24"] and not vanished and not changed, "new 2.02 print appended; non-2.02 and 8-K/A ignored")
    check(new[0] == {"date": "2026-09-24", "accepted": "2026-09-24T20:17:37"}, "the print carries the schema's date/accepted, accepted cut to 19 chars")
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
    check(dedupe([{"date": "d1", "accepted": "a"}, {"date": "d1", "accepted": "b"}, {"date": "d0", "accepted": "c"}])
          == [{"date": "d0", "accepted": "c"}, {"date": "d1", "accepted": "b"}], "dedupe: ascending, last row per date wins")
    # 6. update(): held ticker incremental, new ticker backfilled through its older pages, empty-held ticker incremental, failure isolated
    pages = {"https://data.sec.gov/submissions/CIK0000000001.json": {"filings": {"recent": block([R("2026-09-24"), R("2026-05-28")]), "files": []}},
             "https://data.sec.gov/submissions/CIK0000000002.json": {"filings": {"recent": block([R("2026-08-01")]), "files": [
                 {"name": "old-001.json", "filingTo": "2015-01-01"}, {"name": "ancient.json", "filingTo": "2009-12-31"}]}},
             "https://data.sec.gov/submissions/old-001.json": block([R("2014-06-01"), R("2012-01-05")]),
             "https://data.sec.gov/submissions/CIK0000000003.json": {"filings": {"recent": block([R("2026-09-10")]), "files": []}}}
    calls = []

    def fake(url):
        calls.append(url)
        if url.endswith("CIK0000000004.json"):
            raise ConnectionError("dead")
        return pages[url]
    feed = {"AAA": {"cik": "0000000001", "events": [E("2026-05-28")]}, "EMPTY": {"cik": "0000000003", "events": []}}
    before = json.loads(json.dumps(feed))
    cmap = {"AAA": "0000000001", "NEW": "0000000002", "EMPTY": "0000000003", "DEAD": "0000000004"}
    out, rep = update(feed, cmap, fake)
    assert_nothing_moved(before, out)
    check([e["date"] for e in out["AAA"]["events"]] == ["2026-05-28", "2026-09-24"], "held ticker: old print first, new appended")
    check([e["date"] for e in out["NEW"]["events"]] == ["2012-01-05", "2014-06-01", "2026-08-01"], "new ticker backfilled, pre-2010 page skipped")
    check([e["date"] for e in out["EMPTY"]["events"]] == ["2026-09-10"], "a ticker held with no events picks up a first print incrementally")
    check(not any("ancient" in u for u in calls) and sum(1 for u in calls if "CIK0000000001" in u) == 1, "a held ticker costs one request; pre-2010 pages are not fetched")
    check(rep["answered"] == 3 and rep["attempted"] == 4 and rep["failed"] == ["DEAD (ConnectionError)"], "a failing ticker is recorded, not fatal")
    check(rep["sec_newest_filing"] == "2026-09-24", "the newest filing date SEC showed is recorded")
    # 7. the invariant catches a rewrite, a drop and a lost ticker
    for name, mutate in (("rewrite", lambda f: f["AAA"]["events"][0].update(accepted="x")), ("drop", lambda f: f["AAA"]["events"].pop(0)),
                         ("lost ticker", lambda f: f.pop("AAA"))):
        f2 = json.loads(json.dumps(before)); mutate(f2)
        try:
            assert_nothing_moved(before, f2); check(False, f"the invariant missed a {name}")
        except AssertionError:
            pass
    # 8. a moved CIK is never fetched and never merged
    f3 = {"AAA": {"cik": "0000000009", "events": [E("2026-05-28")]}}
    out3, rep3 = update(f3, {"AAA": "0000000001"}, fake)
    check(rep3["cik_moved"] and out3["AAA"]["events"] == [E("2026-05-28")] and rep3["answered"] == 0, "a moved CIK is reported and left alone")
    # 9. the throttle keeps under SEC's 10 requests a second
    check(MIN_GAP_S >= 0.1, "request spacing is at least 0.1s (<= 10/s)")
    check(json.dumps({"a": [1]}) == '{"a": [1]}', "json.dumps default format is the feed's format")
    print("fetch_earnings_8k selftest: " + ("PASS" if not bad else "FAIL"))
    for b in bad:
        print("  FAIL:", b)
    return not bad


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
