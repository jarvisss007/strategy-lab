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
    [SUPERSEDED by EARN-011 below: no age cut-off remains; every print that enters the feed is checked.]
  * THE DAILY PASS NO LONGER CALLS A CORRECT PRINT "CHANGED" JUST BECAUSE THE JSON STILL CARRIES THE EVENING FORM: a held
    stamp whose New York digits are what the JSON serves is the same print, and the next night's normal JSON matches exactly.
    A held stamp that is the New York digits themselves (the defect this fixes) is still CHANGED, loudly.
    [NARROWED by EARN-011 below: against a JSON that serves the TRUE stamp, that held stamp now looks like SEC's double conversion
    and can be found only by the header sample (always, when its registrant is mixed), not by the CHANGED test.]
  * ONE-TIME CORRECTIONS ARE EXPLICIT AND NEVER SILENT: `--correct-stamps TICKER:DATE --note "why"` rewrites a held stamp
    only when it equals the filing header's New York digits AND SEC's JSON now serves the header's UTC for that exact
    filing; the daily pass never rewrites. Every correction (and every stamp normalised at write time) is appended to
    data/edgar/earnings_8k_corrections.json, a tracked append-only record with the old value, the new value and the evidence.
    The run stamp carries corrections_on_file and this run's stamp_corrected.

EARN-004 follow-up (2026-10-01) — A REGISTRANT SUCCESSION SPLITS ONE ISSUER'S HISTORY (class (d) input correction; prereg-reviewer
APPROVE WITH CHANGES). cik_map.json maps each ticker to ONE registrant, and the feed's "cik" is the registrant the daily job polls,
not the lineage of every print. When a company reorganises under a holding company (SEC Rule 12g-3, Form 8-K12B) the successor gets a
new CIK and the predecessor's 8-K Item 2.02 prints stay under the old one: XOM maps to ExxonMobil Holdings Corp (CIK 2115436,
successor registrant since 2026-07-01) and held 1 print, while Exxon Mobil Corp (CIK 34088) holds 118 by the same page rule (82
dated 2011 or later) with no date in common. Under EARN-002 that one issuer could never clear S1.
  * cik_map.json is NOT changed (stock-radar/listing_dates.py and others expect one CIK string per ticker). data/edgar/
    cik_predecessors.json lists, per ADOPTED ticker, the successor it was reviewed against, its predecessor CIKs, the reason and the
    sha256 of the exact set of prints that was reviewed; keys starting with "_" are notes (verified, not adopted). One loader,
    load_predecessors(), serves this script and the resolver's check; an entry whose successor is no longer cik_map.json's CIK for
    the ticker is refused, so a later cik_map change invalidates it.
  * `--adopt-predecessors TICKER --note "why"` INSERTS the predecessors' prints (the same rule as a full backfill) into the ticker's
    events in date order. It names its tickers explicitly (a ticker not in cik_predecessors.json is refused; there is no "all"), is
    human-invoked and never part of the daily pass (which keeps polling only the successor), and refuses unless the set SEC serves
    serialises to the pinned sha256. EVERY adopted print is checked against its own filing header, not only fresh ones: for some
    registrants SEC's submissions JSON serves the New York wall-clock digits with a Z on EVERY filing, years after the fact (Broadcom Pte.
    Ltd. and Avago Technologies, 36 of 36 prints, found 2026-10-01; unlike MU's one-evening quirk, SEC never settled these), so the
    header's UTC is stored and each normalisation is listed (with its accession) in the record's stamps_normalised; any other disagreement
    refuses. It also refuses, writing nothing, an adoption whose prints the daily pass would call VANISHED or CHANGED against the successor's own SEC
    window every night (AVGO: Broadcom Inc.'s window opens 2018-02-06, Broadcom Pte.'s last print is 2018-03-15); it exempts nothing from the pass.
    It never rewrites or drops a held print (a date the ticker already holds is skipped). Its OWN
    invariant (the daily one is positional and cannot hold across an insertion) asserts: same tickers and ciks, every held print
    identical, the new dates exactly the predecessor's dates minus the held ones, ascending and unique, each carrying only {date,
    accepted}, the inserted set hashing to the pin, every other ticker untouched. The insertion is appended to
    earnings_8k_corrections.json (kind "predecessor", every inserted date and the set's sha256) after the feed is written.
    Re-running it inserts nothing and records nothing.
  * `--unadopt-predecessors TICKER --note "why"` is the way back: it removes exactly the dates the latest "predecessor" record lists,
    only if those events still hash to what was inserted, and records a "predecessor_reversed" entry. The feed is one JSON line, so
    a git diff cannot show an insertion; the record is the audit trail, and this run, not `git revert`, is the reversal.
  * `--predecessor-label` is READ-ONLY (EARN-009, stock-radar/agent/EARNINGS_AGENT.md): it prints the ONE line the earnings agent puts in every
    brief, naming each ticker whose count in this feed includes prints filed by an adopted predecessor registrant (`XOM 118 of 119 (EXXON
    MOBIL CORP)`), computed by replaying the append-only record against the feed as it stands. It carries no verdict and gates nothing.

EARN-011 (2026-10-03) — SEC'S JSON SERVES WHOLE REGISTRANTS' ACCEPTANCE STAMPS DOUBLE-CONVERTED (class (d): the pass's own rule, "a held stamp is
CHANGED only when SEC really lists it differently", was defeated by a change of representation on SEC's side, not by a change in any print).
The 18:10 PT run of 2026-10-02 flagged 1,131 held prints CHANGED and exited 2 on all three attempts; none of them had changed.
  * WHAT SEC SERVES (measured 2026-10-03 against the filings' own headers: 1,748 prints, none unreadable). For a registrant SEC has switched,
    EVERY acceptanceDateTime in its submissions JSON is the true UTC stamp read as New York wall-clock and converted to UTC again: held + 4h
    while New York is on daylight time, + 5h on standard time (1,192 of the 1,748 at +4h, 556 at +5h). "The UTC digits read as New York time"
    and "plus the New York offset" agree on every one of the 1,743 in SEC's live window, 103 of them within three days of a changeover. The held
    stamp equals the header's UTC on all 1,748. It is per registrant (68 of the 133 judged, 65 still serve the true stamp; 47 had switched when
    the 10-02 run read them, 21 more by the next day), never per request and never mixed inside a registrant's recent block, and it is not about
    a print's age: TSLA's print was served true when the 10-02 run took it and shifted by the next day. 969 of the 1,748 have their shifted
    stamp on the NEXT UTC calendar day. No committed reader takes that date without converting to New York time first (EARN-006), so this is a
    hazard for a future reader, not an effect seen in any study.
  * A JSON STAMP THAT IS THE HELD STAMP DOUBLE-CONVERTED (to_double_converted) IS THE SAME PRINT. merge_incremental() returns those as `doubled`,
    not `changed`; main() counts them in ONE summary line (`N held prints SEC serves double-converted (+4h EDT / +5h EST); a sample of K
    header-verified ...`), never per print, and they alone never raise ATTENTION or exit 2. A date SEC lists with a stamp that is neither the
    held one, nor its evening form, nor its double conversion is still CHANGED, loudly, exactly as before.
  * THE RULE IS CHECKED, NOT TRUSTED. Each run reads the filing header of EVERY doubled print of a MIXED registrant (one SEC serves both ways;
    at most MIXED_CAP) and of DOUBLE_SAMPLE (4) other doubled prints: those with the lowest sha256(salt|ticker|date), the salt drawn from a seed
    that is the calendar date. A print's rank does not depend on the other prints, so the sample differs from day to day, but a print that joins
    the feed, or a registrant that turns mixed, between the job's three attempts changes it by at most one print (about 4 in the population
    size): a refuted print does not clear itself on the retry. A mixed registrant is the only place a wrong held stamp (the New York digits
    EARN-004 fixed) looks exactly like SEC's shift. As measured 2026-10-03 NO registrant is mixed (0 of 133), so today the sample is the uniform
    draw alone, and a registrant with one judged print (SPCX, XOM) cannot be told mixed. A refuted print raises ATTENTION on the nights it is
    read and is not remembered from night to night. A sample print whose header UTC is not the held stamp is ATTENTION CHANGED (exit 2) and says
    the other doubled prints rest on that sample; one whose header cannot be read is ATTENTION FAILED; doubled prints with no sample at all are
    ATTENTION too. The held stamp is never rewritten. What the sample cannot do: find ONE wrong print among thousands on a given night (4 of
    1,743 is 0.2%). Unchanged and also silent: a held stamp that is the true stamp + the offset, against a JSON serving the true stamp, passes
    as the evening form below; no such print can now arrive, since every print that enters the feed is header-checked.
  * EVERY PRINT THAT ENTERS THE FEED IS CHECKED AGAINST ITS HEADER, WHATEVER ITS AGE (new, backfilled, adopted): verify_new() no longer has an
    opt-out, so the 14-day cut-off that let a backfill take SEC's stamp unchecked is gone (a new ticker's backfill now costs one header request
    per historical print, about 8 seconds per 60 prints, and one unreadable header holds the whole ticker back). A JSON stamp that is the
    header's UTC double-converted is the `doubled` verdict of check_stamp(): the header's UTC is stored and the print is recorded in
    earnings_8k_corrections.json as a stamp_at_write entry like the New York case. Without it a new print that SEC serves double-converted, as
    it serves every existing print of JPM, BAC, GS, MS and WFC, would be DEFERRED and the feed would stop at its last print (not yet seen for
    a brand-new print: TSLA's was served true on its filing evening).
  * `--check` is a DRY RUN: the whole pass against live SEC, the same output and the same exit code, but no lock is held and nothing is
    written (no feed, no run stamp, no corrections record). It refuses to start while the nightly writer holds the feed's lock (two passes
    at once would double the request rate against SEC), and it cannot be combined with an explicit correction, adoption or reversal.

Exit: 0 = every ticker answered, nothing needs a human · 1 = REFUSED, nothing written (SEC unreachable, throttled, or a
book missing) · 2 = the feed is updated but a human should look (a ticker failed, a held print vanished or changed, a CIK
moved, a new print is DEFERRED, or a header-sample print disagrees with its held stamp). Scheduled by
~/Library/LaunchAgents/com.anupam.edgar-8k.plist, daily 18:10 PT; that job
retries ANY non-zero exit, up to 3 attempts 10 minutes apart (a transient miss clears itself, a vanished print stays loud),
and launchd records the last.
Run: /opt/anaconda3/bin/python fetch_earnings_8k.py            # the incremental update
     /opt/anaconda3/bin/python fetch_earnings_8k.py --correct-stamps MU:2026-09-30 --note "why"   # a disclosed one-time fix
     /opt/anaconda3/bin/python fetch_earnings_8k.py --adopt-predecessors XOM --note "why"   # a disclosed one-time succession backfill
     /opt/anaconda3/bin/python fetch_earnings_8k.py --unadopt-predecessors XOM --note "why" # its reversal
     /opt/anaconda3/bin/python fetch_earnings_8k.py --predecessor-label   # the EARN-009 line, read-only
     /opt/anaconda3/bin/python fetch_earnings_8k.py --check    # EARN-011: the whole pass against live SEC as a DRY RUN, writes nothing, takes no lock
     /opt/anaconda3/bin/python fetch_earnings_8k.py --selftest # offline checks of the merge and stamp rules, writes nothing
"""
import argparse
import copy
import datetime as dt
import fcntl
import gzip
import hashlib
import json
import os
import random
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
PRED = f"{BASE}/data/edgar/cik_predecessors.json"
MIN_GAP_S = 0.12        # 8.3 requests a second at most: under SEC's 10/s ceiling with room for the round trip
MAX_TRIES = 3
BACKFILL_FROM = "2010-01-01"   # older submission pages are skipped for a NEW ticker, as the original build did
DOUBLE_SAMPLE = 4       # EARN-011: held prints SEC serves double-converted, other than a mixed registrant's, whose filing header is read each run (3-5)
MIXED_CAP = 100         # EARN-011: at most this many doubled prints of mixed registrants have their header read each run (every one, up to this)
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


def to_double_converted(utc_stamp):
    """EARN-011. What SEC's submissions JSON serves, for a registrant it has switched, for a filing whose true stamp is `utc_stamp`: the UTC digits
    read as New York wall-clock and converted to UTC again, so held + 4h while New York is on daylight time and + 5h on standard time (1,748
    prints checked against their filing headers on 2026-10-03, no exception). The opposite direction to to_et_wall.
    -> 'YYYY-MM-DDTHH:MM:SS', or None for a stamp that does not parse."""
    try:
        return dt.datetime.strptime(utc_stamp, FMT).replace(tzinfo=ET).astimezone(UTC).strftime(FMT)
    except (TypeError, ValueError):
        return None


def check_stamp(cik, r, fetch_text):
    """r: one print about to enter the feed {"date","accepted","_acc"} as SEC's JSON served it. -> (verdict, stamp_to_store, detail).
    ok          the JSON stamp equals the header's UTC
    corrected   the JSON stamp is the header's New York wall-clock digits (the ET-as-UTC signature): the header's UTC is stored
    doubled     the JSON stamp is the header's UTC double-converted (EARN-011, how SEC serves a switched registrant): the header's UTC is stored
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
        return "ok", utc, f"JSON {r['accepted']} = header {et_wall} ET = {utc} UTC"
    if r["accepted"] == et_wall:
        return "corrected", utc, (f"SEC's JSON served the New York wall-clock {r['accepted']} as if it were UTC; the filing "
                                  f"header says {et_wall} ET = {utc} UTC")
    if r["accepted"] == to_double_converted(utc):
        return "doubled", utc, (f"SEC's JSON served the double-converted {r['accepted']} (the filing header's UTC read as New York time and "
                                f"converted to UTC again, EARN-011); the filing header says {et_wall} ET = {utc} UTC")
    return "mismatch", None, f"SEC's JSON says {r['accepted']}, the filing header says {et_wall} ET = {utc} UTC"


def check_double(cik, e, fetch_text):
    """EARN-011. e: a HELD print whose date SEC lists with the held stamp double-converted: {"date","accepted" (held),"json" (what SEC serves),"_acc"}.
    The filing's own header says whether that is SEC's shift or a wrong held stamp. -> (verdict, detail)
    ok           the header's UTC is the held stamp: the feed is right and SEC's JSON is the shifted one
    mismatch     the header's UTC is not the held stamp: the premise of the rule fails for this print
    unverifiable no accession number, or the header could not be fetched or read"""
    acc = e.get("_acc")
    if not acc:
        return "unverifiable", "SEC's JSON gave no accession number for this filing"
    try:
        et_wall, utc = header_times(fetch_text(HDR_URL.format(cik=int(cik), nodash=acc.replace("-", ""), acc=acc)))
    except Refused:
        raise
    except Exception as ex:                # noqa: BLE001 - reported as ATTENTION, never swallowed
        return "unverifiable", f"{type(ex).__name__}: {ex}"
    if utc == e["accepted"]:
        return "ok", f"held {e['accepted']} = header {et_wall} ET = {utc} UTC; SEC's JSON serves {e['json']} (the held stamp double-converted)"
    why = ""
    if e["accepted"] == et_wall and e["json"] == utc:
        why = " - the HELD stamp is the header's New York wall-clock and SEC's JSON is right (EARN-004's defect; --correct-stamps fixes it)"
    return "mismatch", f"the filing header says {et_wall} ET = {utc} UTC, not the held {e['accepted']}{why}"


def pick_sample(doubled, k, rng, cap=MIXED_CAP):
    """EARN-011. Which held prints SEC serves double-converted have their filing header read this run: EVERY doubled print of a MIXED registrant (see
    merge_incremental; at most `cap`), and the k others ranked lowest by sha256(salt|ticker|date), salt = rng.getrandbits(64) (all of them when there
    are fewer than k). A print's rank does not depend on the other prints, so a print that joins the population, or a registrant that turns mixed,
    between the job's attempts changes the sample by at most one print per newcomer: a refuted print cannot clear itself on the retry by not being
    drawn again. rng: a random.Random."""
    salt = rng.getrandbits(64)
    rank = lambda x: hashlib.sha256(f"{salt}|{x['ticker']}|{x['date']}".encode()).hexdigest()
    return (sorted((x for x in doubled if x.get("mixed")), key=rank)[:cap]
            + sorted((x for x in doubled if not x.get("mixed")), key=rank)[:k])


def clean(r):
    """The stored form of a print: the schema's two fields, never the private accession."""
    return {"date": r["date"], "accepted": r["accepted"]}


def verify_new(cik, prints, fetch_text):
    """prints: the prints about to enter the feed, ascending by date. EVERY one is checked against its own filing header, whatever its age: this
    function takes no opt-out (EARN-011: an age cut-off for a backfill let SEC's stamp in unchecked, and SEC now serves some registrants' stamps
    shifted). -> (to_store, fixes, deferred, seen). seen lists (date, verdict, evidence) for every print whose header was read, so the log
    records what SEC's JSON served against the filing's own header each time, not only when they disagree. Stops at the FIRST
    print that cannot be verified and defers it and every later one: the feed only ever takes prints newer than its newest, so
    writing a later print past a deferred one would lose it for good. fixes: the prints stored as the header's UTC because the JSON's stamp
    was another form of it, each with `how` ("ny_wall_clock" or "double_converted")."""
    store, fixes, deferred, seen = [], [], [], []
    for i, r in enumerate(prints):
        verdict, stamp, detail = check_stamp(cik, r, fetch_text)
        seen.append((r["date"], verdict, detail))
        if verdict in ("ok", "corrected", "doubled"):
            store.append({"date": r["date"], "accepted": stamp})
            if verdict != "ok":
                fixes.append({"date": r["date"], "accession": r["_acc"], "json_stamp": r["accepted"], "stored": stamp,
                              "detail": detail, "how": "ny_wall_clock" if verdict == "corrected" else "double_converted"})
            continue
        for p in prints[i:]:
            deferred.append((p["date"], verdict if p is r else "behind a print that cannot be verified",
                             detail if p is r else f"{r['date']} must be written first"))
        break
    return store, fixes, deferred, seen


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
    -> (new, vanished, changed, doubled)
       new      prints filed AFTER the newest one held, deduped exactly as a full rebuild would dedupe them (still carrying _acc)
       vanished held prints inside SEC's window that SEC no longer lists at all
       changed  held prints whose filing date SEC still lists but with none of the forms of the held stamp. A held stamp whose
                New York wall-clock digits are what the JSON serves is NOT changed: that is the same print seen on its own
                evening, when the JSON carries the New York digits; the next night's JSON matches the held UTC exactly. Nor is
                one whose double conversion (to_double_converted) is what the JSON serves: see doubled.
       doubled  EARN-011: held prints whose date SEC lists with the held stamp DOUBLE-CONVERTED and with neither of the other forms: the
                same print, served the way SEC serves a switched registrant. Each is {"date", "accepted" (the held stamp), "json" (the
                stamp SEC serves), "_acc" (that filing's accession number), "mixed"}; mixed is true when the registrant also has held
                prints in the window that SEC serves unshifted. A wrong held stamp (the New York digits EARN-004 fixed) against a JSON that
                serves the TRUE stamp looks exactly like this, and only the filing header tells the two apart, so pick_sample draws those first.
    The window is filing dates strictly after the OLDEST date in the block: recent is cut at a count, so its oldest day can
    be partial and a print dated on it must not be called vanished."""
    prints = pull(rec)
    stamps = {}                                        # date -> {the acceptance stamp SEC lists for that date: that filing's accession number}
    for r in prints:
        stamps.setdefault(r["date"], {})[r["accepted"]] = r["_acc"]
    newest = max((e["date"] for e in held), default="")
    new = [r for r in dedupe(prints) if r["date"] > newest]
    floor = min(rec["filingDate"]) if rec["filingDate"] else "9999-12-31"
    inside = [e for e in held if e["date"] > floor]
    vanished = [e for e in inside if e["date"] not in stamps]
    changed, doubled, unshifted = [], [], 0
    for e in inside:
        got = stamps.get(e["date"])
        if got is None:
            continue                                   # vanished, above
        if e["accepted"] in got or to_et_wall(e["accepted"]) in got:
            unshifted += 1                             # the held stamp itself, or the same print on its own evening
            continue
        j = to_double_converted(e["accepted"])
        if j in got:
            doubled.append({"date": e["date"], "accepted": e["accepted"], "json": j, "_acc": got[j]})
        else:
            changed.append(e)
    for x in doubled:
        x["mixed"] = unshifted > 0
    return new, vanished, changed, doubled


def update(feed, cik_map, fetch, fetch_text, rng=None):
    """Apply one incremental pass. feed is MUTATED IN PLACE (appends only) and returned with a report.
    fetch(url) -> parsed SEC JSON; fetch_text(url) -> a filing header; rng: the random.Random that draws the header sample of the held prints
    SEC serves double-converted (EARN-011; main() seeds it with the calendar date), an unseeded one when omitted. A ticker's failure is
    recorded and never aborts the pass."""
    rep = {"attempted": len(cik_map), "answered": 0, "failed": [], "new": {}, "backfilled": [], "vanished": [],
           "changed": [], "cik_moved": [], "not_in_cik_map": sorted(set(feed) - set(cik_map)), "sec_newest_filing": "",
           "stamp_corrected": [], "deferred": [], "checked": [], "doubled": [], "double_sample": []}
    for tk, c in sorted(cik_map.items()):
        held = feed.get(tk)
        if held is not None and held.get("cik") != c:
            rep["cik_moved"].append(f"{tk} (feed {held.get('cik')} vs cik_map {c})")
            continue                                   # two companies must never share one ticker's history
        try:
            d = fetch(f"https://data.sec.gov/submissions/CIK{c}.json")
            recent = d["filings"]["recent"]
            if held is not None:
                new, vanished, changed, doubled = merge_incremental(held["events"], recent)
            else:                                      # a ticker never held: the full backfill, as the original build did
                rows = pull(recent)
                for f in d["filings"].get("files", []):
                    if f["filingTo"] >= BACKFILL_FROM:
                        rows += pull(fetch(f"https://data.sec.gov/submissions/{f['name']}"))
                new, vanished, changed, doubled = dedupe(rows), [], [], []
            new, fixes, deferred, seen = verify_new(c, new, fetch_text)   # EVERY print that would enter the feed, whatever its age
        except Refused:
            raise
        except Exception as e:                         # noqa: BLE001 - one ticker's failure is reported, not fatal
            rep["failed"].append(f"{tk} ({type(e).__name__})")
            continue
        if held is None and deferred:                  # a half-verified backfill would be permanent: hold the ticker back whole
            rep["failed"].append(f"{tk} (backfill held back: {deferred[0][0]} {deferred[0][1]}: {deferred[0][2]})")
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
        rep["checked"] += [(tk,) + x for x in seen]
        rep["doubled"] += [dict(x, ticker=tk, cik=c) for x in doubled]
    # EARN-011: the rule "SEC serves the held stamp double-converted, so it is the same print" is CHECKED each run against the filing's own header
    # for a random few of those prints (those of a mixed registrant first). A print whose header does not say the held stamp is a CHANGED print;
    # one whose header cannot be read is a FAILED one: both are ATTENTION, and neither rewrites anything.
    for x in pick_sample(rep["doubled"], DOUBLE_SAMPLE, rng or random.Random()):
        verdict, detail = check_double(x["cik"], x, fetch_text)
        rep["double_sample"].append({"ticker": x["ticker"], "date": x["date"], "held": x["accepted"], "json": x["json"], "accession": x["_acc"],
                                     "mixed": x["mixed"], "verdict": verdict, "detail": detail})
        if verdict == "mismatch":
            rep["changed"].append((x["ticker"], x["date"], x["accepted"]))
        elif verdict == "unverifiable":
            rep["failed"].append(f"{x['ticker']} (header sample for {x['date']} unreadable: {detail})")
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


def load_predecessors(cik_map):
    """{ticker: {"successor", "predecessors", "pinned_sha256", "reason"}} from data/edgar/cik_predecessors.json: the ONE loader for this
    script and the resolver's check. Keys starting with "_" are notes (verified, not adopted), never tickers. A malformed or STALE entry
    raises: the successor named must still be cik_map.json's CIK for the ticker, the predecessors are 10-digit CIKs other than it, the
    pin is a sha256 and a reason is given. A wrong predecessor would put another company's prints into this ticker's history."""
    if not os.path.exists(PRED):
        return {}
    out = {}
    for tk, v in json.load(open(PRED)).items():
        if tk.startswith("_"):
            continue
        ok = (isinstance(v, dict) and tk in cik_map and v.get("successor") == cik_map[tk]
              and isinstance(v.get("predecessors"), list) and v["predecessors"]
              and all(isinstance(p, str) and re.fullmatch(r"\d{10}", p) and p != cik_map[tk] for p in v["predecessors"])
              and isinstance(v.get("pinned_sha256"), str) and re.fullmatch(r"[0-9a-f]{64}", v["pinned_sha256"])
              and isinstance(v.get("reason"), str) and v["reason"].strip())
        if not ok:
            raise ValueError(f"cik_predecessors.json: {tk} is malformed or stale (needs its successor to equal cik_map.json's CIK, a list of "
                             f"10-digit predecessor CIKs other than it, a sha256 pin and a reason)")
        out[tk] = {k: v[k] for k in ("successor", "predecessors", "pinned_sha256", "reason")}
    return out


def inserted_sha(events):
    """The pin: sha256 of json.dumps (default format) of the inserted events, ascending by date."""
    return hashlib.sha256(json.dumps(events).encode()).hexdigest()


# The EARN-009 line. It must not contain the word EDGAR: the EARN-002 resolver check passes any brief that names EDGAR beside S1-S6, and this
# line is a disclosure that must not make that check vacuous (the EARN-005 line is built the same way).
LABEL_MARK = "EARN-009 counts include predecessor-registrant prints (8-K Item 2.02 prints in earnings_8k.json):"


def predecessor_label(feed, doc):
    """The EARN-009 line. Replays the append-only corrections record in order: a "predecessor" entry makes its inserted dates and registrant
    names active for the ticker, a "predecessor_reversed" entry takes the latest active adoption away again. A ticker is listed with
    k = how many of its CURRENT prints are dates an active adoption inserted and n = its current prints, so the line states what the feed
    holds now, not what a record once said; a ticker with k == 0 is not listed. -> MARK + "<TICKER> <k> of <n> (<NAME>[; <NAME>]), ..." or
    MARK + " none"."""
    active = {}
    for r in (doc or {}).get("corrections", []):
        tk = r.get("ticker")
        if r.get("kind") == "predecessor":
            active.setdefault(tk, []).append(r)
        elif r.get("kind") == "predecessor_reversed" and active.get(tk):
            active[tk].pop()
    parts = []
    for tk in sorted(active):
        if tk not in feed:
            continue
        dates = {d for r in active[tk] for d in r["inserted_dates"]}
        k = sum(1 for e in feed[tk]["events"] if e["date"] in dates)
        if not k:
            continue
        names = list(dict.fromkeys(re.sub(r"[()]", "", str(n)).strip() for r in active[tk] for n in r["predecessor_names"]))
        parts.append(f"{tk} {k} of {len(feed[tk]['events'])} ({'; '.join(names)})")
    return f"{LABEL_MARK} {', '.join(parts) or 'none'}"


def adopt_predecessors(feed, preds, tickers, fetch, fetch_text):
    """Insert each named ticker's predecessor registrants' 8-K Item 2.02 prints (the same rule as a full backfill: recent plus the
    submission pages filed in 2010 or later) into its events, ascending by date. A date the ticker already holds is skipped, so a held
    print is never touched and a second run finds nothing to insert. EVERY print it would add is checked against its filing header
    (New York wall-clock -> UTC); a JSON stamp that is the header's New York digits, or the header's UTC double-converted (EARN-011), is
    stored as the header's UTC and listed in the entry's stamps_normalised (date, accession, the JSON's stamp, the stored one). Raises ValueError, writing nothing, when a ticker is not
    listed, the feed's cik is not the reviewed successor, a print cannot be verified, the set SEC serves does not hash to the pin, or the daily
    pass would call an adopted print VANISHED or CHANGED against the successor's own SEC window (refusal only). -> entries (kind
    "predecessor") for the corrections record."""
    entries = []
    for tk in tickers:
        if tk not in preds:
            raise ValueError(f"{tk} is not listed in cik_predecessors.json - refusing (adoption names its tickers; there is no 'all')")
        p = preds[tk]
        v = feed.get(tk)
        if v is None:
            raise ValueError(f"{tk} is not in the feed")
        if v["cik"] != p["successor"]:
            raise ValueError(f"{tk}: the feed's cik {v['cik']} is not the reviewed successor {p['successor']}")
        held_dates = {e["date"] for e in v["events"]}
        got, names, normalised = {}, [], []
        for c in p["predecessors"]:
            d = fetch(f"https://data.sec.gov/submissions/CIK{c}.json")
            names.append(d.get("name"))
            rows = pull(d["filings"]["recent"])
            for f in d["filings"].get("files", []):
                if f["filingTo"] >= BACKFILL_FROM:
                    rows += pull(fetch(f"https://data.sec.gov/submissions/{f['name']}"))
            fresh = [r for r in dedupe(rows) if r["date"] not in held_dates and r["date"] not in got]
            store, fixes, deferred, seen = verify_new(c, fresh, fetch_text)
            if deferred:
                raise ValueError(f"{tk}: predecessor {c} print {deferred[0][0]} cannot be verified ({deferred[0][1]}: {deferred[0][2]}) - nothing is written")
            for e in store:
                got[e["date"]] = e
            normalised += [{"date": f["date"], "accession": f["accession"], "json_stamp": f["json_stamp"], "stored": f["stored"]} for f in fixes]
        store = [got[d] for d in sorted(got)]
        if not store:
            continue                                   # already adopted: nothing to insert, nothing to record
        sha = inserted_sha(store)
        if sha != p["pinned_sha256"]:
            raise ValueError(f"{tk}: the {len(store)} predecessor prints SEC serves now hash to {sha}, not the reviewed {p['pinned_sha256']} - nothing is written")
        # REFUSAL ONLY. main() runs the daily pass right after an adoption, and the daily pass reads the successor's CURRENT window: an adopted
        # print inside it that the successor's own list does not carry would be called VANISHED (or CHANGED) every night (exit 2, and the feed-current
        # check red) until the window rolls past it. AVGO would trip this: Broadcom Inc.'s window opens 2018-02-06 and Broadcom Pte.'s last print is
        # 2018-03-15. XOM and GOOG do not: their successors' windows open after the last predecessor print. Nothing is exempted from the daily pass here.
        inserted_dates = {e["date"] for e in store}
        _, gone, moved, _ = merge_incremental(sorted(v["events"] + store, key=lambda e: e["date"]),
                                           fetch(f"https://data.sec.gov/submissions/CIK{p['successor']}.json")["filings"]["recent"])
        flagged = sorted(e["date"] for e in gone + moved if e["date"] in inserted_dates)
        if flagged:
            raise ValueError(f"{tk}: the daily pass would call {len(flagged)} of these predecessor prints VANISHED or CHANGED against the successor's own "
                             f"SEC window every night ({', '.join(flagged[:4])}{'...' if len(flagged) > 4 else ''}); they are refused until a separate review "
                             f"decides how the pass should treat adopted dates - nothing is written")
        held_before = len(v["events"])
        v["events"] = sorted(v["events"] + store, key=lambda e: e["date"])           # held events stay the very same objects
        entries.append({"kind": "predecessor", "ticker": tk, "successor": p["successor"], "predecessor_ciks": p["predecessors"],
                        "predecessor_names": names, "inserted": len(store), "inserted_2011_or_later": sum(1 for e in store if e["date"] >= "2011-01-01"),
                        "first": store[0]["date"], "last": store[-1]["date"], "inserted_dates": [e["date"] for e in store],
                        "inserted_sha256": sha, "stamps_normalised": sorted(normalised, key=lambda f: f["date"]),
                        "held_before": held_before, "held_after": len(v["events"]), "evidence": p["reason"]})
    return entries


def assert_adopted(before, after, entries):
    """The adoption invariant (the daily one is positional and cannot hold across an insertion). For every ticker adopted: the cik is
    unchanged, no inserted date was already held or is repeated, the new dates are exactly held plus inserted, ascending and unique,
    every held print is identical, each inserted print carries only {date, accepted} and the inserted set hashes to its record. Every
    other ticker is untouched, and the set of tickers is unchanged."""
    if set(before) != set(after):
        raise AssertionError("INVARIANT BROKEN: the set of tickers changed during a succession backfill - nothing is written")
    listed = {e["ticker"]: e for e in entries}
    for tk, v in before.items():
        w = after[tk]
        if w["cik"] != v["cik"]:
            raise AssertionError(f"INVARIANT BROKEN: {tk}'s cik changed - nothing is written")
        if tk not in listed:
            if w["events"] != v["events"]:
                raise AssertionError(f"INVARIANT BROKEN: {tk} was not adopted but its prints changed - nothing is written")
            continue
        ins = listed[tk]["inserted_dates"]
        held = [e["date"] for e in v["events"]]
        if len(set(ins)) != len(ins) or set(ins) & set(held):
            raise AssertionError(f"INVARIANT BROKEN: {tk}: an inserted date was already held or repeated - nothing is written")
        if [e["date"] for e in w["events"]] != sorted(held + ins):
            raise AssertionError(f"INVARIANT BROKEN: {tk}'s dates are not exactly held plus inserted, ascending and unique - nothing is written")
        by_date = {e["date"]: e for e in w["events"]}
        if any(by_date[e["date"]] != e for e in v["events"]):
            raise AssertionError(f"INVARIANT BROKEN: a print held for {tk} changed - nothing is written")
        new = [by_date[d] for d in ins]
        if any(set(e) != {"date", "accepted"} for e in new) or inserted_sha(new) != listed[tk]["inserted_sha256"]:
            raise AssertionError(f"INVARIANT BROKEN: {tk}'s inserted prints are not the recorded set - nothing is written")


def unadopt_predecessors(feed, tk, doc):
    """Reverse the LATEST recorded adoption for tk: remove exactly the dates that record lists, and only if those events still hash to
    what was inserted. doc is the parsed corrections record. -> the entry (kind "predecessor_reversed"). Raises ValueError otherwise."""
    recs = [r for r in doc.get("corrections", []) if r.get("ticker") == tk and r.get("kind") in ("predecessor", "predecessor_reversed")]
    if not recs or recs[-1]["kind"] != "predecessor":
        raise ValueError(f"{tk}: there is no adoption on record to reverse (or its latest record is already a reversal)")
    rec = recs[-1]
    v = feed.get(tk)
    if v is None:
        raise ValueError(f"{tk} is not in the feed")
    dates = set(rec["inserted_dates"])
    gone = [e for e in v["events"] if e["date"] in dates]
    if len(gone) != len(dates) or inserted_sha(gone) != rec["inserted_sha256"]:
        raise ValueError(f"{tk}: the prints the adoption inserted are not all present and unchanged any more - refusing to guess")
    v["events"] = [e for e in v["events"] if e["date"] not in dates]
    return {"kind": "predecessor_reversed", "ticker": tk, "removed": len(gone), "removed_dates": sorted(dates),
            "removed_sha256": rec["inserted_sha256"], "reverses_record_at": rec.get("at"), "held_after": len(v["events"]),
            "evidence": f"removes exactly the {len(gone)} dates the adoption recorded at {rec.get('at')}"}


def assert_only_removed(before, after, rec):
    """A reversal removes exactly the recorded dates from one ticker and changes nothing else."""
    gone = set(rec["removed_dates"])
    if set(before) != set(after):
        raise AssertionError("INVARIANT BROKEN: the set of tickers changed during a reversal - nothing is written")
    for tk, v in before.items():
        w = after[tk]
        want = [e for e in v["events"] if e["date"] not in gone] if tk == rec["ticker"] else v["events"]
        if w["cik"] != v["cik"] or w["events"] != want:
            raise AssertionError(f"INVARIANT BROKEN: {tk} changed beyond the recorded dates during a reversal - nothing is written")


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
def writer_running(path):
    """True when another process holds the book's lock (the nightly job mid-run). Probes WITHOUT keeping it: opens the lock file if one exists, tries a
    non-blocking exclusive flock and lets go at once. A missing lock file means nothing has ever written here, so nothing is running."""
    lock = os.path.abspath(path) + ".lock"
    if not os.path.exists(lock):
        return False
    fd = os.open(lock, os.O_RDWR)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return True
    else:
        fcntl.flock(fd, fcntl.LOCK_UN)
        return False
    finally:
        os.close(fd)


def stats(feed):
    dates = [e["date"] for v in feed.values() for e in v["events"]]
    return len(dates), max(dates) if dates else ""


def main(argv):
    ap = argparse.ArgumentParser(description="Incremental EDGAR 8-K Item 2.02 feed (EARN-004).")
    ap.add_argument("--selftest", action="store_true", help="offline checks, writes nothing")
    ap.add_argument("--correct-stamps", metavar="TICKER:DATE[,TICKER:DATE]",
                    help="one-time, disclosed correction of held ET-as-UTC stamps (needs --note)")
    ap.add_argument("--adopt-predecessors", metavar="TICKER[,TICKER]",
                    help="one-time, disclosed insertion of the NAMED tickers' predecessor registrants' prints, as listed and pinned in "
                         "cik_predecessors.json (needs --note)")
    ap.add_argument("--unadopt-predecessors", metavar="TICKER", help="reverse the latest recorded adoption for one ticker (needs --note)")
    ap.add_argument("--predecessor-label", action="store_true",
                    help="read-only: print the EARN-009 line (which tickers' counts include a predecessor registrant's prints)")
    ap.add_argument("--check", action="store_true",
                    help="EARN-011 dry run: the whole pass against live SEC with the same output and exit code, taking no lock and writing "
                         "nothing (no feed, no run stamp, no corrections record)")
    ap.add_argument("--note", default="", help="why: written to earnings_8k_corrections.json with the correction")
    args = ap.parse_args(argv)
    if args.selftest:
        return 0 if selftest() else 1
    if args.predecessor_label:
        try:
            lfeed = json.load(open(FEED))
            ldoc = json.load(open(CORR))               # a MISSING record is an error, never `none`: the feed may hold predecessor prints it would have named
            line = predecessor_label(lfeed, ldoc)
        except (OSError, ValueError, AttributeError, KeyError, TypeError) as e:
            print(f"the EARN-009 line cannot be computed: {type(e).__name__}: {e}", file=sys.stderr)
            return 1
        print(line)
        return 0
    if args.check and (args.correct_stamps or args.adopt_predecessors is not None or args.unadopt_predecessors):
        print("REFUSED: --check is a read-only dry run and cannot be combined with --correct-stamps, --adopt-predecessors or --unadopt-predecessors")
        return 1
    if (args.correct_stamps or args.adopt_predecessors or args.unadopt_predecessors) and not args.note.strip():
        print("REFUSED: a correction must carry --note \"why\": it is written to earnings_8k_corrections.json and is never silent")
        return 1
    specs = []
    if args.correct_stamps:
        try:
            specs = [tuple(s.strip().split(":")) for s in args.correct_stamps.split(",") if s.strip()]
            assert specs and all(len(s) == 2 for s in specs)
        except AssertionError:
            print("REFUSED: --correct-stamps wants TICKER:DATE[,TICKER:DATE]")
            return 1
    adopt = [t.strip() for t in (args.adopt_predecessors or "").split(",") if t.strip()]
    if args.adopt_predecessors is not None and not adopt:
        print("REFUSED: --adopt-predecessors wants TICKER[,TICKER]; there is no 'all'")
        return 1
    if not os.path.exists(CIK_MAP):
        print(f"REFUSED: {CIK_MAP} is missing - nothing to fetch for; nothing written")
        return 1
    if args.check:
        if writer_running(FEED):
            print("REFUSED: --check: the feed's lock is held by a running writer (the nightly job?) - a dry run now would double the request rate "
                  "against SEC. Nothing was fetched or written; try again when it has finished.")
            return 1
        print("earnings_8k --check: DRY RUN against live SEC - no lock is held and nothing is written (no feed, no run stamp, no corrections record)")
    else:
        atomicio.hold_book(FEED)                       # BOOK-001: the lock FIRST, then the read (a dry run only reads, and the feed is replaced whole)
    cik_map = json.load(open(CIK_MAP))
    feed = json.load(open(FEED)) if os.path.exists(FEED) else {}
    n0, newest0 = stats(feed)                          # the feed as this run FOUND it, before any explicit stage: the printed delta is the whole change
    explicit = []
    try:
        if specs:
            asked = copy.deepcopy(feed)
            explicit += correct_stamps(feed, specs, get, get_text)
            assert_only_stamps_changed(asked, feed, specs)
        if adopt:
            asked = copy.deepcopy(feed)
            got = adopt_predecessors(feed, load_predecessors(cik_map), adopt, get, get_text)
            assert_adopted(asked, feed, got)
            explicit += got
            if not got:
                print(f"  --adopt-predecessors {','.join(adopt)}: every predecessor print is already held, so nothing is inserted and nothing is recorded")
        if args.unadopt_predecessors:
            asked = copy.deepcopy(feed)
            rec = unadopt_predecessors(feed, args.unadopt_predecessors.strip(), json.load(open(CORR)) if os.path.exists(CORR) else {})
            assert_only_removed(asked, feed, rec)
            explicit.append(rec)
    except (ValueError, AssertionError) as e:
        print(f"REFUSED: {e}. Nothing written.")
        return 1
    except Refused as e:
        print(f"REFUSED: {e}. Nothing written.")
        return 1
    before = copy.deepcopy(feed)                       # AFTER an explicit stage: the daily invariant guards only the pass that follows
    try:
        # the header sample is drawn from a seed that is the calendar date: still a different sample every day, but the job's retries (3 attempts,
        # 10 minutes apart) re-read the SAME prints, so a refuted sample print cannot clear itself on attempt 2 by not being drawn again
        feed, rep = update(feed, cik_map, get, get_text, random.Random(dt.date.today().isoformat()))
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
    if not args.check and (n_new or rep["backfilled"] or explicit):
        atomicio.atomic_write_text(FEED, json.dumps(feed))   # the format the feed always had: json.dump defaults, no newline
    n1, newest1 = stats(feed)
    sha = hashlib.sha256(open(FEED, "rb").read()).hexdigest() if os.path.exists(FEED) else ""
    at = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    ledger = [dict(e, at=at, note=args.note.strip(), feed_sha256_after=sha) for e in explicit]
    ledger += [{"kind": "stamp_at_write", "ticker": f["ticker"], "date": f["date"], "accession": f["accession"],
                "was": f["json_stamp"], "now": f["stored"], "evidence": f["detail"], "at": at,
                "note": ("normalised at write time: the print's JSON stamp was the filing header's UTC read as New York time and converted to UTC "
                         "again (SEC's double conversion, EARN-011)" if f.get("how") == "double_converted" else
                         "normalised at write time: the new print's JSON stamp was the filing header's New York wall-clock"),
                "feed_sha256_after": sha}
               for f in rep["stamp_corrected"]]
    ledger_failed = None
    if not args.check:
        try:
            append_corrections(ledger)                 # AFTER the feed write (Brain section 2): a record never claims what was not written
        except Exception as e:                         # noqa: BLE001 - the feed is already written: say so LOUD, never swallow
            ledger_failed = f"{type(e).__name__}: {e}"
    n_dbl, tk_dbl = len(rep["doubled"]), len({x["ticker"] for x in rep["doubled"]})
    run = {"finished_at": at, "attempted": rep["attempted"], "answered": rep["answered"], "failed": rep["failed"],
           "sec_newest_filing": rep["sec_newest_filing"], "new_prints": n_new, "tickers_with_new": len(rep["new"]),
           "backfilled": rep["backfilled"], "vanished": rep["vanished"], "changed": rep["changed"],
           "cik_moved": rep["cik_moved"], "deferred": rep["deferred"], "stamp_corrected": rep["stamp_corrected"],
           "stamps_checked": rep["checked"],
           "double_converted": n_dbl, "double_converted_tickers": tk_dbl,
           "double_sample": [[s["ticker"], s["date"], s["verdict"], s["detail"]] for s in rep["double_sample"]],
           "corrections_this_run": explicit, "corrections_on_file": corrections_on_file(),
           "prints_before": n0, "prints_total": n1, "newest_print": newest1, "feed_sha256": sha}
    if not args.check:
        atomicio.atomic_write_text(RUN, json.dumps(run, indent=1) + "\n")
    print(f"earnings_8k: SEC answered {rep['answered']}/{rep['attempted']} tickers (its index shows filings through "
          f"{rep['sec_newest_filing']}); {n_new} new print(s) in {len(rep['new'])} ticker(s); "
          f"{n0} -> {n1} prints, newest {newest0} -> {newest1}"
          + ("" if (n_new or explicit) else " · nothing new: the feed is unchanged and was not rewritten")
          + (" · DRY RUN: nothing was written" if args.check else ""))
    k_s = len(rep["double_sample"])
    sample_ok = sum(1 for s in rep["double_sample"] if s["verdict"] == "ok")
    print(f"  {n_dbl} held prints SEC serves double-converted (+4h EDT / +5h EST) in {tk_dbl} ticker(s); "
          + ("no header sample needed" if not n_dbl else "NO header sample was read (ATTENTION below)" if not k_s else
             f"a sample of {k_s} header-verified: {sample_ok} equal the held stamp"
             + ((f" (all {n_dbl} are right)" if k_s == n_dbl else f" (those {k_s} are right; the other {n_dbl - k_s} are counted on that sample, not verified)")
                if sample_ok == k_s else f", {k_s - sample_ok} not confirmed (ATTENTION below)")))
    for s in sorted(rep["double_sample"], key=lambda s: (s["ticker"], s["date"])):
        print(f"  sample {s['ticker']} {s['date']}{' (mixed registrant)' if s['mixed'] else ''}: {s['verdict']} - {s['detail']}")
    for tk, ds in sorted(rep["new"].items()):
        print(f"  new  {tk}: {', '.join(ds)}")
    for tk, d, verdict, detail in rep["checked"]:
        print(f"  stamp {tk} {d}: {verdict} - {detail}")
    attention = 0
    if n_dbl and not k_s:                              # a dead sampler must not look clean (Brain section 3)
        attention += 1
        print(f"ATTENTION SAMPLE: {n_dbl} held prints are counted as double-converted but no filing header was read for any of them - the rule is UNCHECKED.")
    for e in explicit:
        if e["kind"] == "predecessor":
            print(f"  ADOPTED (explicit, noted) {e['ticker']}: {e['inserted']} print(s) ({e['inserted_2011_or_later']} dated 2011 or later) from "
                  f"{', '.join(str(n) for n in e['predecessor_names'])} (CIK {', '.join(str(int(c)) for c in e['predecessor_ciks'])}), "
                  f"{e['first']}..{e['last']}; {e['held_before']} -> {e['held_after']} held; "
                  f"{len(e['stamps_normalised'])} stamp(s) normalised to the header's UTC; set sha256 {e['inserted_sha256']}")
        elif e["kind"] == "predecessor_reversed":
            print(f"  REVERSED (explicit, noted) {e['ticker']}: removed {e['removed']} print(s); {e['held_after']} held; {e['evidence']}")
        else:
            print(f"  CORRECTED (explicit, noted) {e['ticker']} {e['date']}: {e['was']} -> {e['now']}  [{e['evidence']}]")
    for f in rep["stamp_corrected"]:
        print(f"  NOTE STAMP NORMALISED {f['ticker']} {f['date']}: {f['detail']}; stored {f['stored']} (recorded in earnings_8k_corrections.json)")
    for tk in rep["backfilled"]:
        print(f"  backfilled a ticker not previously held: {tk}")
    for tk, d, a in rep["vanished"]:
        attention += 1
        print(f"ATTENTION VANISHED {tk} {d} (accepted {a}): held in the feed but absent from SEC's current filing list "
              f"for that window - KEPT, not deleted. Look at it.")
    refuted = {(s["ticker"], s["date"]): s for s in rep["double_sample"] if s["verdict"] == "mismatch"}
    for tk, d, a in rep["changed"]:
        attention += 1
        if (tk, d) in refuted:                         # a header-sample print: SEC serves its double conversion, the filing header disagrees with the held stamp
            s = refuted[(tk, d)]
            print(f"ATTENTION CHANGED {tk} {d}: the feed holds accepted {a} and SEC serves {s['json']} (the held stamp double-converted), but "
                  f"{s['detail']} - KEPT as held. The other {n_dbl - 1} double-converted prints are counted on the strength of this sample and are NOT proven.")
            continue
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
    global PRED, FEED, CORR, RUN, CIK_MAP, get, get_text, DOUBLE_SAMPLE, update
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
    R = lambda d, f="8-K", i="2.02,9.01", t="20:17:37", acc=None, s=None: (d, f, i, s or f"{d}T{t}") + ((acc,) if acc else ())
    hdr = lambda digits: f"<SEC-HEADER>x\n<ACCEPTANCE-DATETIME>{digits}\n<ACCESSION-NUMBER>y\n"
    hdr_of = lambda utc: hdr(re.sub(r"\D", "", to_et_wall(utc)))                  # the filing header that goes with a true UTC stamp
    dbl = to_double_converted                                                       # what SEC serves for a switched registrant
    # 1. an incremental pass appends only what is newer, filters to 8-K + 2.02, and never touches a held print
    held = [E("2026-03-05"), E("2026-05-28")]
    rec = block([R("2026-09-24"), R("2026-09-25", i="5.02"), R("2026-09-26", f="8-K/A"), R("2026-05-28"), R("2026-03-05"),
                 R("2026-01-15", i="7.01"), R("2025-01-02")])
    new, vanished, changed, doubled = merge_incremental(held, rec)
    check([r["date"] for r in new] == ["2026-09-24"] and not vanished and not changed and not doubled, "new 2.02 print appended; non-2.02 and 8-K/A ignored")
    check(clean(new[0]) == {"date": "2026-09-24", "accepted": "2026-09-24T20:17:37"} and "_acc" not in clean(new[0]),
          "the stored print carries the schema's date/accepted only, accepted cut to 19 chars, never the accession")
    # 2. a held print SEC no longer lists inside its window is VANISHED, and an older one outside the window is not judged
    held2 = [E("2024-06-01"), E("2026-03-05"), E("2026-05-28")]
    rec2 = block([R("2026-05-28"), R("2025-10-01", i="9.01")])            # window starts 2025-10-01; 2026-03-05 missing
    n2, v2, c2, d2 = merge_incremental(held2, rec2)
    check([e["date"] for e in v2] == ["2026-03-05"], "a held print missing from SEC's window is VANISHED")
    check("2024-06-01" not in [e["date"] for e in v2 + c2], "a held print older than SEC's window is not judged")
    # 3. the oldest day of the window may be partial: a print dated ON it is not called vanished
    n3, v3, c3, d3 = merge_incremental([E("2025-10-01")], block([R("2026-05-28"), R("2025-10-01", i="9.01")]))
    check(not v3, "a held print on the window's oldest day is not called vanished")
    # 4. CHANGED: same date, other acceptance stamp; a second filing the same day is not a change
    n4, v4, c4, d4 = merge_incremental([E("2026-05-28", "20:17:37")], block([R("2026-05-28", t="21:00:00"), R("2026-05-27")]))
    check([e["date"] for e in c4] == ["2026-05-28"], "a held date SEC lists with another stamp is CHANGED")
    n5, v5, c5, d5 = merge_incremental([E("2026-05-28", "20:17:37")], block([R("2026-05-28", t="20:17:37"), R("2026-05-28", t="21:00:00"), R("2026-05-27")]))
    check(not c5 and not n5, "two filings on one date with the held stamp among them: not changed, nothing new")
    # 5. same-date dedupe is the original build's: the last row SEC lists wins
    check([clean(x) for x in dedupe([{"date": "d1", "accepted": "a"}, {"date": "d1", "accepted": "b"}, {"date": "d0", "accepted": "c"}])]
          == [{"date": "d0", "accepted": "c"}, {"date": "d1", "accepted": "b"}], "dedupe: ascending, last row per date wins")
    # 5b. EARN-011, the rule: SEC serves a switched registrant's stamp as the true UTC digits read as New York time and converted again (+4h EDT, +5h EST)
    check(dbl("2015-10-27T20:30:36") == "2015-10-28T00:30:36" and dbl("2022-10-27T20:30:22") == "2022-10-28T00:30:22",
          "the measured AAPL examples: 20:30:36 UTC (header 16:30:36 ET) is served as 2015-10-28T00:30:36")
    check(dbl("2026-01-05T21:02:22") == "2026-01-06T02:02:22" and dbl("2026-07-14T10:28:21") == "2026-07-14T14:28:21",
          "+5h in standard time, +4h in daylight time, across midnight UTC or not")
    check(dbl("2026-03-06T21:00:00") == "2026-03-07T02:00:00" and dbl("2026-03-09T21:00:00") == "2026-03-10T01:00:00"
          and dbl("2026-10-30T20:00:00") == "2026-10-31T00:00:00" and dbl("2026-11-02T21:00:00") == "2026-11-03T02:00:00", "either side of both 2026 changeovers")
    check(dbl("garbage") is None and dbl(None) is None and dbl("") is None, "a stamp that does not parse has no double conversion")
    for stamp in ("2026-07-14T10:28:21", "2026-01-14T11:28:36", "2026-03-09T21:00:00", "2026-11-02T21:00:00", "2026-05-01T04:00:00", "2026-03-06T21:00:00"):
        u = dt.datetime.strptime(stamp, FMT).replace(tzinfo=UTC)
        check(dbl(stamp) == (u - u.astimezone(ET).utcoffset()).strftime(FMT), f"{stamp}: 'UTC read as New York time' equals 'UTC plus the New York offset'")
    # 5c. EARN-011, the classification: the held stamp, its evening form and its double conversion are one print; anything else is CHANGED
    held_c = [E("2026-05-28"), E("2026-06-04"), E("2026-06-11"), E("2026-06-18")]
    rec_c = block([R("2026-05-01", i="9.01"), R("2026-05-28", acc="X-1"), R("2026-06-04", t="16:17:37", acc="X-2"),
                   R("2026-06-11", s=dbl("2026-06-11T20:17:37"), acc="X-3"), R("2026-06-18", t="21:00:00", acc="X-4")])
    n_c, v_c, c_c, d_c = merge_incremental(held_c, rec_c)
    check([e["date"] for e in c_c] == ["2026-06-18"] and not v_c and not n_c, "a stamp that is neither the held one, its evening form nor its double conversion is CHANGED")
    check(len(d_c) == 1 and d_c[0]["date"] == "2026-06-11" and d_c[0]["accepted"] == "2026-06-11T20:17:37" and d_c[0]["json"] == "2026-06-12T00:17:37"
          and d_c[0]["_acc"] == "X-3" and d_c[0]["mixed"] is True,
          "the double conversion is `doubled` (not changed), carries what SEC serves and the accession of that filing, and a registrant SEC also serves unshifted is MIXED")
    n_d, v_d, c_d, d_d = merge_incremental([E("2026-06-04"), E("2026-06-11"), E("2026-08-20", "10:59:50")],
                                           block([R("2026-05-01", i="9.01"), R("2026-06-04", s=dbl("2026-06-04T20:17:37"), acc="Y-1"),
                                                  R("2026-06-11", s=dbl("2026-06-11T20:17:37"), acc="Y-2"), R("2026-08-20", s=dbl("2026-08-20T10:59:50"), acc="Y-3")]))
    check([x["date"] for x in d_d] == ["2026-06-04", "2026-06-11", "2026-08-20"] and not c_d and not v_d and all(x["mixed"] is False for x in d_d),
          "a registrant SEC serves double-converted throughout: every print is doubled, none changed, none mixed")
    n_e, v_e, c_e, d_e = merge_incremental([E("2026-06-04"), E("2026-06-11", "16:17:37")],
                                           block([R("2026-05-01", i="9.01"), R("2026-06-04", acc="Z-1"), R("2026-06-11", acc="Z-2")]))
    check([x["date"] for x in d_e] == ["2026-06-11"] and d_e[0]["mixed"] is True and not c_e,
          "a held New York-digits stamp (EARN-004's defect) against a JSON that serves the TRUE stamp has the double-conversion look, and is MIXED so it is sampled first")
    n_f, v_f, c_f, d_f = merge_incremental([E("2026-06-11", "16:17:37")], block([R("2026-05-01", i="9.01"), R("2026-06-11", s=dbl("2026-06-11T20:17:37"), acc="W-1")]))
    check([e["date"] for e in c_f] == ["2026-06-11"] and not d_f, "the same wrong held stamp inside a registrant SEC has switched is 2 offsets off (+8h): CHANGED, as before")
    n_g, v_g, c_g, d_g = merge_incremental([E("2026-06-11")], block([R("2026-05-01", i="9.01"), R("2026-06-11", s=dbl("2026-06-11T20:17:37"), acc="V-1"),
                                                                     R("2026-06-11", s="2026-06-11T21:00:00", acc="V-2")]))
    check(len(d_g) == 1 and d_g[0]["_acc"] == "V-1" and not c_g, "two filings on one date: the doubled one is matched by its stamp and its own accession is carried")
    n_h, v_h, c_h, d_h = merge_incremental([E("2026-06-11", "garbage")], block([R("2026-05-01", i="9.01"), R("2026-06-11", acc="U-1")]))
    check([e["date"] for e in c_h] == ["2026-06-11"] and not d_h, "a held stamp that does not parse cannot be explained by the rule: CHANGED")
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
    # 7b. EARN-011: a JSON stamp that is the header's UTC double-converted is stored as the header's UTC (the 4th form SEC serves a print in)
    P2 = lambda stamp: {"date": "2026-09-30", "accepted": stamp, "_acc": "0000723125-26-000018"}
    v, s, det = check_stamp("0000723125", P2(dbl("2026-09-30T20:02:22")), ftext)
    check(v == "doubled" and s == "2026-09-30T20:02:22" and "double" in det and "2026-10-01T00:02:22" in det, "JSON stamp equal to the header's UTC double-converted is stored as the header's UTC")
    check(check_stamp("0000723125", P2("2026-10-01T04:02:22"), ftext)[0] == "mismatch", "a stamp twice as far off (+8h) is a mismatch, not a double conversion")
    check(check_stamp("0000723125", P2("2026-09-30T20:02:22"), ftext)[0] == "ok" and check_stamp("0000723125", P2("2026-09-30T16:02:22"), ftext)[0] == "corrected",
          "the existing ok and New York-digits verdicts are unchanged")
    # 7c. check_double: the held print's header decides whether SEC's shift or the held stamp is the odd one out
    H = lambda held, j, acc="0000723125-26-000018": {"date": "2026-09-30", "accepted": held, "json": j, "_acc": acc}
    v, det = check_double("0000723125", H("2026-09-30T20:02:22", "2026-10-01T00:02:22"), ftext)
    check(v == "ok" and "held 2026-09-30T20:02:22 = header 2026-09-30T16:02:22 ET" in det, "the header's UTC is the held stamp: ok (the feed is right, SEC's JSON is shifted)")
    v, det = check_double("0000723125", H("2026-09-30T18:00:00", "2026-09-30T22:00:00"), ftext)
    check(v == "mismatch" and "not the held 2026-09-30T18:00:00" in det and "--correct-stamps" not in det, "any other held stamp is a mismatch")
    v, det = check_double("0000723125", H("2026-09-30T16:02:22", "2026-09-30T20:02:22"), ftext)
    check(v == "mismatch" and "New York wall-clock" in det and "--correct-stamps" in det, "a held stamp that is the New York digits (JSON true) is a mismatch and says how to correct it")
    check(check_double("0000723125", dict(H("2026-09-30T20:02:22", "2026-10-01T00:02:22"), _acc=None), ftext)[0] == "unverifiable" and
          check_double("0000723125", H("2026-09-30T20:02:22", "2026-10-01T00:02:22"), dead)[0] == "unverifiable", "no accession, or a header that cannot be read: unverifiable")
    try:
        def blocked(url):
            raise Refused("throttled")
        check_double("0000723125", H("2026-09-30T20:02:22", "2026-10-01T00:02:22"), blocked); check(False, "a refusal by SEC must propagate, not be swallowed as unverifiable")
    except Refused:
        pass
    # 7d. pick_sample: DOUBLE_SAMPLE at random, mixed registrants first, all of them when there are fewer
    check(3 <= DOUBLE_SAMPLE <= 5, "the header sample is 3 to 5 prints")
    pool = [{"ticker": f"T{i}", "date": "2026-05-28", "mixed": False} for i in range(12)]
    picks = [pick_sample(pool, DOUBLE_SAMPLE, random.Random(sd)) for sd in range(20)]
    check(all(len(x) == DOUBLE_SAMPLE and len({y["ticker"] for y in x}) == DOUBLE_SAMPLE for x in picks) and len({tuple(y["ticker"] for y in x) for x in picks}) > 5,
          "a sample is DOUBLE_SAMPLE distinct prints and varies from run to run")
    check(len(pick_sample(pool[:2], DOUBLE_SAMPLE, random.Random(0))) == 2 and pick_sample([], DOUBLE_SAMPLE, random.Random(0)) == [], "fewer doubled prints than the sample: all of them; none: none")
    day = lambda d: [y["ticker"] for y in pick_sample(pool, DOUBLE_SAMPLE, random.Random(d))]
    check(day("2026-10-03") == day("2026-10-03") and len({tuple(day(f"2026-10-{n:02d}")) for n in range(1, 29)}) > 10,
          "seeded with a calendar date the sample is the same all day (the job's retries re-read the same prints) and differs from day to day")
    mixed_pool = pool + [{"ticker": "M1", "date": "2026-05-28", "mixed": True}, {"ticker": "M2", "date": "2026-05-28", "mixed": True}]
    check(all({"M1", "M2"} <= {y["ticker"] for y in pick_sample(mixed_pool, DOUBLE_SAMPLE, random.Random(sd))} for sd in range(20)), "the prints of a mixed registrant are always in the sample")
    many = [{"ticker": f"M{i}", "date": "2026-05-28", "mixed": True} for i in range(9)] + pool
    got_many = [pick_sample(many, DOUBLE_SAMPLE, random.Random(sd)) for sd in range(20)]
    check(all(len(x) == 9 + DOUBLE_SAMPLE and sum(1 for y in x if y["mixed"]) == 9 for x in got_many),
          "EVERY print of a mixed registrant is read however many there are, plus DOUBLE_SAMPLE others")
    huge = [{"ticker": f"X{i:03d}", "date": "2026-05-28", "mixed": True} for i in range(MIXED_CAP + 50)] + pool
    got_huge = pick_sample(huge, DOUBLE_SAMPLE, random.Random(1))
    check(len(got_huge) == MIXED_CAP + DOUBLE_SAMPLE and sum(1 for y in got_huge if y["mixed"]) == MIXED_CAP, "the mixed prints read are capped at MIXED_CAP")
    # 8. verify_new: a deferred print holds back every later one (the feed only takes prints newer than its newest)
    seq = [{"date": "2026-09-28", "accepted": "2026-09-28T20:00:00", "_acc": "A-1"}, {"date": "2026-09-29", "accepted": "2026-09-29T20:00:00", "_acc": "A-2"},
           {"date": "2026-09-30", "accepted": "2026-09-30T20:00:00", "_acc": "A-3"}]
    heads = {"A-1": hdr("20260928160000"), "A-3": hdr("20260930160000")}          # A-2's header is missing

    def ft(url):
        for k, v in heads.items():
            if url.endswith(f"/{k}.hdr.sgml"):
                return v
        raise KeyError(url)
    store, fixes, deferred, seen = verify_new("0000000001", seq, ft)
    check([s["date"] for s in store] == ["2026-09-28"] and [d[0] for d in deferred] == ["2026-09-29", "2026-09-30"],
          "the first unverifiable print and every later one are deferred")
    mixed_forms = [{"date": "2026-09-28", "accepted": "2026-09-28T20:00:00", "_acc": "A-1"}, {"date": "2026-09-30", "accepted": "2026-09-30T16:00:00", "_acc": "A-3"},
                   {"date": "2026-10-01", "accepted": dbl("2026-10-01T20:00:00"), "_acc": "A-4"}]
    heads4 = dict(heads, **{"A-4": hdr("20261001160000")})
    st4, fx4, df4, sn4 = verify_new("0000000001", mixed_forms, lambda url: next(v for k, v in heads4.items() if url.endswith(f"/{k}.hdr.sgml")))
    check(st4 == [{"date": "2026-09-28", "accepted": "2026-09-28T20:00:00"}, {"date": "2026-09-30", "accepted": "2026-09-30T20:00:00"},
                  {"date": "2026-10-01", "accepted": "2026-10-01T20:00:00"}] and not df4 and [x[1] for x in sn4] == ["ok", "corrected", "doubled"]
          and [(f["date"], f["how"]) for f in fx4] == [("2026-09-30", "ny_wall_clock"), ("2026-10-01", "double_converted")] and fx4[1]["json_stamp"] == "2026-10-02T00:00:00" and fx4[1]["stored"] == "2026-10-01T20:00:00",
          "whatever form SEC served it in, the header's UTC is stored; the two normalised forms are listed with how, both stamps and the accession")
    # 9. update(): held ticker incremental, new ticker backfilled through its older pages, empty-held ticker incremental, failure isolated
    pages = {"https://data.sec.gov/submissions/CIK0000000001.json": {"filings": {"recent": block([R("2026-09-24", acc="A-24"), R("2026-05-28")]), "files": []}},
             "https://data.sec.gov/submissions/CIK0000000002.json": {"filings": {"recent": block([R("2026-08-01", acc="N-1")]), "files": [
                 {"name": "old-001.json", "filingTo": "2015-01-01"}, {"name": "ancient.json", "filingTo": "2009-12-31"}]}},
             "https://data.sec.gov/submissions/old-001.json": block([R("2014-06-01", acc="N-2"), R("2012-01-05", acc="N-3")]),
             "https://data.sec.gov/submissions/CIK0000000003.json": {"filings": {"recent": block([R("2026-09-10", acc="A-10")]), "files": []}}}
    calls, hdr_calls = [], []

    def fake(url):
        calls.append(url)
        if url.endswith("CIK0000000004.json"):
            raise ConnectionError("dead")
        return pages[url]

    hdr_utc = {"A-24": "2026-09-24T20:17:37", "A-10": "2026-09-10T20:17:37", "N-1": "2026-08-01T20:17:37", "N-2": "2014-06-01T20:17:37", "N-3": "2012-01-05T20:17:37"}

    def fake_text(url):
        hdr_calls.append(url)
        return hdr_of(hdr_utc[re.search(r"/([^/]+)\.hdr\.sgml$", url).group(1)])
    feed = {"AAA": {"cik": "0000000001", "events": [E("2026-05-28")]}, "EMPTY": {"cik": "0000000003", "events": []}}
    before = json.loads(json.dumps(feed))
    cmap = {"AAA": "0000000001", "NEW": "0000000002", "EMPTY": "0000000003", "DEAD": "0000000004"}
    out, rep = update(feed, cmap, fake, fake_text)
    assert_nothing_moved(before, out)
    check([e["date"] for e in out["AAA"]["events"]] == ["2026-05-28", "2026-09-24"], "held ticker: old print first, new appended")
    check(all(set(e) == {"date", "accepted"} for v in out.values() for e in v["events"]), "no private key ever reaches the feed")
    check([e["date"] for e in out["NEW"]["events"]] == ["2012-01-05", "2014-06-01", "2026-08-01"], "new ticker backfilled, pre-2010 page skipped")
    check([e["date"] for e in out["EMPTY"]["events"]] == ["2026-09-10"], "a ticker held with no events picks up a first print incrementally")
    check(not any("ancient" in u for u in calls) and sum(1 for u in calls if "CIK0000000001" in u) == 1, "a held ticker costs one request; pre-2010 pages are not fetched")
    check(len(hdr_calls) == 5, "headers fetched for the two incremental prints AND the three backfilled ones (2026, 2014 and 2012): every print that enters the feed, whatever its age")
    check(rep["answered"] == 3 and rep["attempted"] == 4 and rep["failed"] == ["DEAD (ConnectionError)"], "a failing ticker is recorded, not fatal")
    check(rep["sec_newest_filing"] == "2026-09-24" and not rep["stamp_corrected"] and not rep["deferred"], "newest filing date recorded; nothing corrected or deferred")
    check(sorted((c[0], c[1], c[2]) for c in rep["checked"]) == [("AAA", "2026-09-24", "ok"), ("EMPTY", "2026-09-10", "ok"), ("NEW", "2012-01-05", "ok"),
                                                                 ("NEW", "2014-06-01", "ok"), ("NEW", "2026-08-01", "ok")]
          and all("= header" in c[3] for c in rep["checked"]), "every checked print is logged with what the JSON served against the header, even when they agree")
    check(rep["doubled"] == [] and rep["double_sample"] == [], "no registrant SEC serves double-converted: nothing counted, no sample read")
    # 10. THE SAME-EVENING PATH: SEC's JSON serves the New York digits with a Z for MU's print; the header says otherwise
    mu_hdr = lambda url: hdr("20260930160222") if "26-000018" in url else hdr("20260624160201")
    evening = {"https://data.sec.gov/submissions/CIK0000723125.json": {"filings": {"recent": block([
        R("2026-09-30", t="16:02:22", acc="0000723125-26-000018"), R("2026-06-24", t="20:02:01", acc="0000723125-26-000013")]), "files": []}}}
    mu_feed = {"MU": {"cik": "0000723125", "events": [E("2026-06-24", "20:02:01")]}}
    o10, r10 = update(mu_feed, {"MU": "0000723125"}, lambda u: evening[u], mu_hdr)
    check(o10["MU"]["events"][-1] == {"date": "2026-09-30", "accepted": "2026-09-30T20:02:22"}, "the evening print is stored with the UTC stamp, not the New York digits")
    check(len(r10["stamp_corrected"]) == 1 and r10["stamp_corrected"][0]["json_stamp"] == "2026-09-30T16:02:22"
          and r10["stamp_corrected"][0]["stored"] == "2026-09-30T20:02:22" and r10["stamp_corrected"][0]["accession"] == "0000723125-26-000018",
          "the normalisation is recorded with both values and the accession, never silent")
    # ... a SECOND run the same evening (a retry, a kickstart): the JSON still serves the New York digits; the held UTC print is the same print
    o10b, r10b = update(copy.deepcopy(o10), {"MU": "0000723125"}, lambda u: evening[u], mu_hdr)
    check(not r10b["changed"] and not r10b["new"], "same evening, second run: the correctly stored print is not CHANGED")
    # ... the next night SEC's JSON is normal and matches exactly
    nextday = {"https://data.sec.gov/submissions/CIK0000723125.json": {"filings": {"recent": block([
        R("2026-09-30", t="20:02:22", acc="0000723125-26-000018"), R("2026-06-24", t="20:02:01", acc="0000723125-26-000013")]), "files": []}}}
    o10c, r10c = update(copy.deepcopy(o10), {"MU": "0000723125"}, lambda u: nextday[u], mu_hdr)
    check(not r10c["changed"] and not r10c["new"], "next night, normal JSON: unchanged")
    # ... and the DEFECT itself still shows. EARN-011 NARROWED how: a held New York-digits stamp against a JSON that serves the TRUE stamp is exactly
    # what SEC's double conversion looks like (JSON = held + 4h), so the CHANGED test can no longer see it; the header sample does, and a registrant that
    # also has correctly held prints is MIXED, so its doubled prints are sampled first (here the only doubled print, so it is always read)
    wrong = {"MU": {"cik": "0000723125", "events": [E("2026-06-24", "20:02:01"), {"date": "2026-09-30", "accepted": "2026-09-30T16:02:22"}]}}
    nextday_w = {"https://data.sec.gov/submissions/CIK0000723125.json": {"filings": {"recent": block([R("2026-05-01", i="9.01"),
        R("2026-09-30", t="20:02:22", acc="0000723125-26-000018"), R("2026-06-24", t="20:02:01", acc="0000723125-26-000013")]), "files": []}}}
    o10d, r10d = update(wrong, {"MU": "0000723125"}, lambda u: nextday_w[u], mu_hdr, random.Random(1))
    check([x["date"] for x in r10d["doubled"]] == ["2026-09-30"] and r10d["doubled"][0]["mixed"] is True and len(r10d["double_sample"]) == 1
          and r10d["double_sample"][0]["verdict"] == "mismatch" and "--correct-stamps" in r10d["double_sample"][0]["detail"]
          and [c[1] for c in r10d["changed"]] == ["2026-09-30"] and o10d["MU"]["events"][-1]["accepted"] == "2026-09-30T16:02:22",
          "the held wrong stamp is found by the header sample, flagged CHANGED and KEPT (the daily pass never rewrites)")
    # ... inside a registrant SEC has switched, the same wrong stamp is 2 offsets off, which no rule explains: CHANGED without any header
    switched = {"https://data.sec.gov/submissions/CIK0000723125.json": {"filings": {"recent": block([R("2026-05-01", i="9.01"),
        R("2026-09-30", s=dbl("2026-09-30T20:02:22"), acc="0000723125-26-000018"), R("2026-06-24", s=dbl("2026-06-24T20:02:01"), acc="0000723125-26-000013")]), "files": []}}}
    o10e, r10e = update(copy.deepcopy(wrong), {"MU": "0000723125"}, lambda u: switched[u], mu_hdr, random.Random(1))
    check([x["date"] for x in r10e["doubled"]] == ["2026-06-24"] and [c[1] for c in r10e["changed"]] == ["2026-09-30"], "a wrong held stamp inside a switched registrant is CHANGED; its correct print is doubled")
    # 11. an unreadable header defers the print: not written, newest not advanced, SEC's answer still counted
    o11, r11 = update({"MU": {"cik": "0000723125", "events": [E("2026-06-24", "20:02:01")]}}, {"MU": "0000723125"}, lambda u: evening[u], dead)
    check(len(o11["MU"]["events"]) == 1 and [d[1] for d in r11["deferred"]] == ["2026-09-30"] and r11["answered"] == 1, "unverifiable print is deferred, not written")
    # 12. EARN-011: a backfill header-checks EVERY print, whatever its age (the 14-day cut-off let SEC's stamp in unchecked), and holds the ticker back whole
    # if one cannot be checked. The prints here are 30 days, 7 months and 11 years old when the run is 2026-10-01.
    bf_utc = {"B-1": "2026-09-01T20:17:37", "B-2": "2026-03-01T20:17:37", "B-3": "2015-05-05T20:17:37"}
    bf_url, bf_old = "https://data.sec.gov/submissions/CIK0000000009.json", "https://data.sec.gov/submissions/bf-old.json"
    bf_files = [{"name": "bf-old.json", "filingTo": "2016-01-01"}]
    bf = {bf_url: {"filings": {"recent": block([R("2026-09-01", acc="B-1"), R("2026-03-01", acc="B-2")]), "files": bf_files}},
          bf_old: block([R("2015-05-05", acc="B-3")])}
    bf_calls = []

    def bf_text(url):
        bf_calls.append(url)
        return hdr_of(bf_utc[re.search(r"/([^/]+)\.hdr\.sgml$", url).group(1)])
    o12, r12 = update({}, {"BF": "0000000009"}, lambda u: bf[u], bf_text)
    check([e["date"] for e in o12["BF"]["events"]] == ["2015-05-05", "2026-03-01", "2026-09-01"] and len(bf_calls) == 3
          and sorted(c[1] for c in r12["checked"]) == ["2015-05-05", "2026-03-01", "2026-09-01"],
          "a backfill header-checks the 30-day-old, 7-month-old AND 11-year-old print: one header request each")
    # ... SEC serves a switched registrant's old pages double-converted too: each is stored as the header's UTC and recorded, never taken as served
    bfd = {bf_url: {"filings": {"recent": block([R("2026-09-01", s=dbl("2026-09-01T20:17:37"), acc="B-1"), R("2026-03-01", s=dbl("2026-03-01T20:17:37"), acc="B-2")]), "files": bf_files}},
           bf_old: block([R("2015-05-05", s=dbl("2015-05-05T20:17:37"), acc="B-3")])}
    o12d, r12d = update({}, {"BF": "0000000009"}, lambda u: bfd[u], bf_text)
    check(o12d == o12 and len(r12d["stamp_corrected"]) == 3 and all(f["how"] == "double_converted" and f["json_stamp"] != f["stored"] for f in r12d["stamp_corrected"])
          and [f["stored"] for f in r12d["stamp_corrected"]] == ["2015-05-05T20:17:37", "2026-03-01T20:17:37", "2026-09-01T20:17:37"],
          "a double-converted backfill is stored exactly as the true one, every normalisation listed with both stamps")
    o12b, r12b = update({}, {"BF": "0000000009"}, lambda u: bf[u], dead)
    check("BF" not in o12b and r12b["answered"] == 0 and r12b["failed"] and "held back" in r12b["failed"][0], "a backfill with an unverifiable print is held back whole")
    bf_only_old_dead = lambda url: bf_text(url) if "B-3" not in url else dead(url)
    o12e, r12e = update({}, {"BF": "0000000009"}, lambda u: bf[u], bf_only_old_dead)
    check("BF" not in o12e and r12e["answered"] == 0 and "held back" in r12e["failed"][0] and "2015-05-05" in r12e["failed"][0],
          "the OLD print that cannot be read holds the whole ticker back (an age cut-off would have let it in unchecked)")
    o12f, r12f = update({}, {"BF": "0000000009"}, lambda u: bf[u], lambda u: hdr("20200101120000") if "B-3" in u else bf_text(u))
    check("BF" not in o12f and "held back" in r12f["failed"][0] and "mismatch" in r12f["failed"][0], "an old print whose header disagrees with every form of the JSON's stamp is a mismatch: the ticker is held back whole")
    # 12b. EARN-011: a registrant SEC serves double-converted (a bank: pre-market prints, EST then EDT). The held prints are the same prints: counted, a
    # random few have their header read, nothing is flagged and nothing is rewritten; the sample is what would catch the rule being wrong.
    sw = [("2025-10-14", "10:28:31"), ("2025-11-14", "11:28:31"), ("2025-12-12", "11:28:15"), ("2026-01-14", "11:28:36"), ("2026-02-12", "11:28:19"),
          ("2026-03-12", "10:28:07"), ("2026-04-14", "10:28:12"), ("2026-05-14", "10:28:40"), ("2026-06-11", "10:28:33"), ("2026-07-14", "10:28:21"),
          ("2026-08-13", "10:28:02"), ("2026-09-14", "10:28:44")]
    sw_url = "https://data.sec.gov/submissions/CIK0000000021.json"

    def sw_world(n, header_utc=None):
        """n held prints of one registrant SEC serves double-converted. header_utc: {accession: the header's true UTC, or None for an unreadable header}"""
        sub = sw[:n]
        feed_ = {"SW": {"cik": "0000000021", "events": [E(d, t) for d, t in sub]}}
        url_ = {sw_url: {"filings": {"recent": block([R("2025-09-01", i="9.01")] + [R(d, s=dbl(f"{d}T{t}"), acc=f"S-{i}") for i, (d, t) in enumerate(sub)]), "files": []}}}
        utc_ = {f"S-{i}": f"{d}T{t}" for i, (d, t) in enumerate(sub)}
        utc_.update(header_utc or {})
        calls_ = []

        def text_(url):
            calls_.append(url)
            u = utc_[re.search(r"/([^/]+)\.hdr\.sgml$", url).group(1)]
            if u is None:
                raise ConnectionError("no header")
            return hdr_of(u)
        return feed_, url_, text_, calls_
    f12s, u12s, t12s, c12s = sw_world(12)
    b12s = copy.deepcopy(f12s)
    o12s, r12s = update(f12s, {"SW": "0000000021"}, lambda u: u12s[u], t12s, random.Random(5))
    assert_nothing_moved(b12s, o12s)
    check(o12s == b12s and r12s["answered"] == 1 and not (r12s["changed"] or r12s["failed"] or r12s["deferred"] or r12s["vanished"] or r12s["new"]),
          "12 held prints SEC serves double-converted: nothing changed, nothing flagged, no print rewritten")
    check(len(r12s["doubled"]) == 12 and len(r12s["double_sample"]) == DOUBLE_SAMPLE and len(c12s) == DOUBLE_SAMPLE
          and all(x["verdict"] == "ok" for x in r12s["double_sample"]) and all(x["json"] == dbl(x["held"]) for x in r12s["double_sample"])
          and len({x["date"] for x in r12s["double_sample"]}) == DOUBLE_SAMPLE,
          "all 12 are counted, only DOUBLE_SAMPLE distinct headers are read, and each agrees with the held stamp")
    f3s, u3s, t3s, c3s = sw_world(3, {"S-1": "2025-11-14T11:45:00"})                 # one print's header says a time that is not the held stamp
    b3s = copy.deepcopy(f3s)
    o3s, r3s = update(f3s, {"SW": "0000000021"}, lambda u: u3s[u], t3s, random.Random(5))
    check(o3s == b3s and r3s["changed"] == [("SW", "2025-11-14", "2025-11-14T11:28:31")] and sorted(x["verdict"] for x in r3s["double_sample"]) == ["mismatch", "ok", "ok"]
          and "11:45:00" in [x for x in r3s["double_sample"] if x["verdict"] == "mismatch"][0]["detail"],
          "a sample print whose header is not the held stamp is CHANGED (and kept); the others still agree")
    f3u, u3u, t3u, c3u = sw_world(3, {"S-2": None})
    o3u, r3u = update(f3u, {"SW": "0000000021"}, lambda u: u3u[u], t3u, random.Random(5))
    check(not r3u["changed"] and len(r3u["failed"]) == 1 and "SW (header sample for 2025-12-12 unreadable" in r3u["failed"][0], "a sample header that cannot be read is FAILED, never taken as agreement")
    f0s, u0s, t0s, c0s = sw_world(0)
    o0s, r0s = update(f0s, {"SW": "0000000021"}, lambda u: u0s[u], t0s, random.Random(5))
    check(r0s["doubled"] == [] and r0s["double_sample"] == [] and c0s == [], "no doubled print: no sample, no header request")
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
    # 15. succession adoption (class (d), reviewed): explicit tickers only, the reviewed set pinned by sha256, insert-only, reversible
    succ_pages = {"https://data.sec.gov/submissions/CIK0000000034.json": {"name": "OLD CO", "filings": {"recent": block([
                      R("2026-05-01", acc="P-1"), R("2026-02-02", acc="P-2"), R("2026-07-31", t="05:00:00", acc="P-3")]), "files": [
                      {"name": "old-pred.json", "filingTo": "2015-01-01"}, {"name": "ancient-pred.json", "filingTo": "2009-12-31"}]}},
                  "https://data.sec.gov/submissions/old-pred.json": block([R("2012-01-05", acc="P-4"), R("2011-04-01", acc="P-5")]),
                  "https://data.sec.gov/submissions/CIK0000000099.json": {"filings": {"recent": block([R("2026-07-31", t="10:31:39", acc="S-1")]), "files": []}}}
    exp_ins = [E("2011-04-01"), E("2012-01-05"), E("2026-02-02"), E("2026-05-01")]      # the reviewed set; 2026-07-31 is held by the successor
    preds = {"XOM": {"successor": "0000000099", "predecessors": ["0000000034"], "pinned_sha256": inserted_sha(exp_ins), "reason": "why"}}
    sf = {"XOM": {"cik": "0000000099", "events": [E("2026-07-31", "10:31:39")]}, "OTHER": {"cik": "0000000077", "events": [E("2026-01-01")]}}
    sbefore = copy.deepcopy(sf)
    spage = lambda u: succ_pages[u]
    pstamp = {"P-1": "2026-05-01T20:17:37", "P-2": "2026-02-02T20:17:37", "P-4": "2012-01-05T20:17:37", "P-5": "2011-04-01T20:17:37", "P-3": "2026-07-31T05:00:00"}

    def phdr(url):                                      # the filing's own header for a predecessor accession: New York digits of its true UTC stamp
        for acc, utc in pstamp.items():
            if url.endswith(f"/{acc}.hdr.sgml"):
                return hdr(re.sub(r"\D", "", to_et_wall(utc)))
        raise KeyError(url)
    sent = adopt_predecessors(sf, preds, ["XOM"], spage, phdr)
    assert_adopted(sbefore, sf, sent)
    check([e["date"] for e in sf["XOM"]["events"]] == ["2011-04-01", "2012-01-05", "2026-02-02", "2026-05-01", "2026-07-31"], "predecessor prints inserted in date order")
    check(sf["XOM"]["events"][-1] == E("2026-07-31", "10:31:39"), "a date the successor already holds keeps the HELD print")
    check(len(sent) == 1 and sent[0]["kind"] == "predecessor" and sent[0]["inserted"] == 4 and sent[0]["inserted_dates"] == [e["date"] for e in exp_ins]
          and sent[0]["inserted_sha256"] == inserted_sha(exp_ins) and sent[0]["held_before"] == 1 and sent[0]["held_after"] == 5 and sent[0]["evidence"] == "why"
          and sent[0]["predecessor_names"] == ["OLD CO"], "the insertion is described for the corrections record, every date listed, with the set's sha256")
    check(sf["OTHER"] == sbefore["OTHER"], "no other ticker moves")
    check(sent[0]["stamps_normalised"] == [], "a registrant whose JSON stamps agree with the headers normalises nothing")
    check(adopt_predecessors(sf, preds, ["XOM"], spage, phdr) == [], "adopting twice inserts nothing and records nothing")
    sg = copy.deepcopy(sbefore)
    for name, bad_preds, tks, feed_x in (("the pin differs", {"XOM": dict(preds["XOM"], pinned_sha256="0" * 64)}, ["XOM"], sg),
                                        ("the ticker is not listed", preds, ["GOOG"], sg),
                                        ("the feed's cik is not the reviewed successor", {"XOM": dict(preds["XOM"], successor="0000000055")}, ["XOM"], sg),
                                        ("the ticker is not in the feed", preds, ["XOM"], {})):
        try:
            adopt_predecessors(feed_x, bad_preds, tks, spage, phdr); check(False, f"adoption must refuse when {name}")
        except ValueError:
            pass
    check(sg == sbefore, "a refused adoption leaves the feed exactly as it was")
    old_only = {"https://data.sec.gov/submissions/CIK0000000034.json": {"filings": {"recent": block([R("2012-03-01", acc="P-8")]), "files": []}}}
    try:
        adopt_predecessors({"XOM": {"cik": "0000000099", "events": []}}, preds, ["XOM"], lambda u: old_only[u], dead)
        check(False, "an OLD predecessor print that cannot be verified must refuse the adoption too (nothing is exempt)")
    except ValueError:
        pass
    # ... the permanent-quirk case: the JSON serves the New York digits with a Z for EVERY old print; the header's UTC is stored and listed
    dorm = {"https://data.sec.gov/submissions/CIK0000000034.json": {"name": "QUIRK CO", "filings": {"recent": block([
                R("2012-01-05", t="15:17:37", acc="P-4"), R("2011-04-01", t="16:17:37", acc="P-5")]), "files": []}},
            "https://data.sec.gov/submissions/CIK0000000098.json": {"filings": {"recent": block([R("2018-06-07", acc="S-9")]), "files": []}}}
    dexp = [E("2011-04-01"), E("2012-01-05")]                                           # what a correct (UTC) feed would hold
    dpred = {"AVG": {"successor": "0000000098", "predecessors": ["0000000034"], "pinned_sha256": inserted_sha(dexp), "reason": "why"}}
    df = {"AVG": {"cik": "0000000098", "events": [E("2018-06-07")]}}
    dbefore = copy.deepcopy(df)
    dent = adopt_predecessors(df, dpred, ["AVG"], lambda u: dorm[u], phdr)
    assert_adopted(dbefore, df, dent)
    check([e for e in df["AVG"]["events"][:2]] == dexp and [n["date"] for n in dent[0]["stamps_normalised"]] == ["2011-04-01", "2012-01-05"]
          and dent[0]["stamps_normalised"][0] == {"date": "2011-04-01", "accession": "P-5", "json_stamp": "2011-04-01T16:17:37", "stored": "2011-04-01T20:17:37"},
          "a registrant whose JSON serves New-York-digits stamps has them stored as the header's UTC and every one listed")
    # ... EARN-011: a predecessor whose JSON SEC serves double-converted: stored as the header's UTC (the pin is over that set), every one listed
    ddbl = {"https://data.sec.gov/submissions/CIK0000000034.json": {"name": "SWITCHED CO", "filings": {"recent": block([
                R("2012-01-05", s=dbl("2012-01-05T20:17:37"), acc="P-4"), R("2011-04-01", s=dbl("2011-04-01T20:17:37"), acc="P-5")]), "files": []}},
            "https://data.sec.gov/submissions/CIK0000000098.json": {"filings": {"recent": block([R("2018-06-07", s=dbl("2018-06-07T20:17:37"), acc="S-9")]), "files": []}}}
    df2 = copy.deepcopy(dbefore)
    dent2 = adopt_predecessors(df2, dpred, ["AVG"], lambda u: ddbl[u], phdr)
    assert_adopted(dbefore, df2, dent2)
    check(df2["AVG"]["events"][:2] == dexp and [n["date"] for n in dent2[0]["stamps_normalised"]] == ["2011-04-01", "2012-01-05"]
          and dent2[0]["stamps_normalised"][0] == {"date": "2011-04-01", "accession": "P-5", "json_stamp": "2011-04-02T00:17:37", "stored": "2011-04-01T20:17:37"},
          "a predecessor SEC serves double-converted is stored as the header's UTC and every normalisation listed")
    dwin = dict(ddbl, **{"https://data.sec.gov/submissions/CIK0000000098.json": {"filings": {"recent": block([
        R("2012-01-01", i="9.01"), R("2012-01-05", s=dbl("2012-01-05T20:17:37"), acc="S-8"), R("2018-06-07", s=dbl("2018-06-07T20:17:37"), acc="S-9")]), "files": []}}})
    check(adopt_predecessors(copy.deepcopy(dbefore), dpred, ["AVG"], lambda u: dwin[u], phdr)[0]["inserted"] == 2,
          "an adopted date the successor lists double-converted is the same print for the daily pass: not VANISHED or CHANGED, so not refused")
    # ... the refusal-only guard: a predecessor print inside the successor's own SEC window that the successor does not list would be VANISHED every night
    win = dict(dorm, **{"https://data.sec.gov/submissions/CIK0000000098.json": {"filings": {"recent": block([R("2018-06-07", acc="S-9"), R("2012-01-01", i="9.01")]), "files": []}}})
    gf = copy.deepcopy(dbefore)
    try:
        adopt_predecessors(gf, dpred, ["AVG"], lambda u: win[u], phdr); check(False, "a predecessor print inside the successor's window that it does not list must refuse the adoption")
    except ValueError as e:
        check("VANISHED" in str(e) and "2012-01-05" in str(e) and gf == dbefore, "refused with the dates named, and the feed is exactly as it was")
    chg = dict(dorm, **{"https://data.sec.gov/submissions/CIK0000000098.json": {"filings": {"recent": block([R("2012-01-05", t="09:00:00", acc="S-8"), R("2012-01-01", i="9.01")]), "files": []}}})
    try:
        adopt_predecessors(copy.deepcopy(dbefore), dpred, ["AVG"], lambda u: chg[u], phdr); check(False, "a predecessor date the successor lists with another stamp must refuse the adoption")
    except ValueError as e:
        check("VANISHED" in str(e) or "CHANGED" in str(e), "refused: the successor lists that date with another stamp")
    unrel = dict(dorm, **{"https://data.sec.gov/submissions/CIK0000000098.json": {"filings": {"recent": block([R("2018-06-07", t="09:00:00", acc="S-9"), R("2018-01-01", i="9.01")]), "files": []}}})
    check(adopt_predecessors(copy.deepcopy(dbefore), dpred, ["AVG"], lambda u: unrel[u], phdr)[0]["inserted"] == 2,
          "the guard judges only ADOPTED dates: an unrelated held print the successor lists with another stamp does not block the adoption")
    try:
        adopt_predecessors(copy.deepcopy(dbefore), {"AVG": dict(dpred["AVG"], pinned_sha256=inserted_sha([E("2011-04-01", "16:17:37"), E("2012-01-05", "15:17:37")]))},
                           ["AVG"], lambda u: dorm[u], phdr)
        check(False, "a pin taken over the un-normalised JSON stamps must refuse: the normalised set is what is reviewed")
    except ValueError:
        pass
    # ... the adoption invariant catches every way an insertion can go wrong
    for name, mutate in (("a held print rewritten", lambda f: f["XOM"]["events"][-1].update(accepted="x")), ("a held print dropped", lambda f: f["XOM"]["events"].pop()),
                         ("another ticker touched", lambda f: f["OTHER"]["events"].pop()), ("dates out of order", lambda f: f["XOM"]["events"].reverse()),
                         ("an inserted print tampered with", lambda f: f["XOM"]["events"][0].update(accepted="2011-04-01T00:00:00")),
                         ("an extra key on an inserted print", lambda f: f["XOM"]["events"][0].update(_acc="P-5")),
                         ("an unlisted print inserted", lambda f: f["XOM"]["events"].insert(1, E("2011-05-05"))), ("a ticker removed", lambda f: f.pop("OTHER")),
                         ("the cik changed", lambda f: f["XOM"].update(cik="0000000034"))):
        f4 = copy.deepcopy(sf); mutate(f4)
        try:
            assert_adopted(sbefore, f4, sent); check(False, f"the adoption invariant missed {name}")
        except AssertionError:
            pass
    # ... reversal: exactly the recorded dates, only if unchanged, and only once
    doc = {"corrections": [dict(sent[0], at="2026-10-01T00:30:00-07:00")]}
    sf_rev = copy.deepcopy(sf)
    rrec = unadopt_predecessors(sf_rev, "XOM", doc)
    assert_only_removed(sf, sf_rev, rrec)
    check(sf_rev == sbefore and rrec["kind"] == "predecessor_reversed" and rrec["removed"] == 4 and rrec["reverses_record_at"] == "2026-10-01T00:30:00-07:00",
          "the reversal restores the pre-adoption feed exactly and says which record it reverses")
    altered = copy.deepcopy(sf); altered["XOM"]["events"][0]["accepted"] = "x"
    for name, f_x, d_x in (("an inserted print changed since", altered, doc), ("there is no record", copy.deepcopy(sf), {"corrections": []}),
                           ("the latest record is already a reversal", copy.deepcopy(sf_rev), {"corrections": doc["corrections"] + [dict(rrec, at="2026-10-01T00:40:00-07:00")]})):
        try:
            unadopt_predecessors(f_x, "XOM", d_x); check(False, f"the reversal must refuse when {name}")
        except ValueError:
            pass
    for name, mutate in (("one extra print removed", lambda f: f["XOM"]["events"].pop()), ("another ticker touched", lambda f: f["OTHER"]["events"].clear()),
                         ("a recorded date left in", lambda f: f["XOM"]["events"].insert(0, E("2011-04-01")))):
        f5 = copy.deepcopy(sf_rev); mutate(f5)
        try:
            assert_only_removed(sf, f5, rrec); check(False, f"the reversal invariant missed {name}")
        except AssertionError:
            pass
    # ... the loader: notes are skipped, a stale or malformed entry is refused
    import tempfile
    real_pred, tmpd = PRED, tempfile.mkdtemp()
    try:
        PRED = os.path.join(tmpd, "cik_predecessors.json")
        good = {"XOM": {"successor": "0000000099", "predecessors": ["0000000034"], "pinned_sha256": "a" * 64, "reason": "why"}, "_verified_not_adopted": {"GOOG": {}}}
        open(PRED, "w").write(json.dumps(good))
        check(list(load_predecessors({"XOM": "0000000099"})) == ["XOM"], "the loader returns adopted tickers and skips _notes")
        for name, mut, cmap in (("the successor is no longer cik_map's", lambda g: None, {"XOM": "0000000055"}),
                                ("a predecessor equals the successor", lambda g: g["XOM"].update(predecessors=["0000000099"]), {"XOM": "0000000099"}),
                                ("a predecessor is not 10 digits", lambda g: g["XOM"].update(predecessors=["34"]), {"XOM": "0000000099"}),
                                ("the pin is not a sha256", lambda g: g["XOM"].update(pinned_sha256="abc"), {"XOM": "0000000099"}),
                                ("no reason", lambda g: g["XOM"].update(reason=" "), {"XOM": "0000000099"}),
                                ("the ticker is not in cik_map", lambda g: None, {})):
            g = copy.deepcopy(good); mut(g); open(PRED, "w").write(json.dumps(g))
            try:
                load_predecessors(cmap); check(False, f"the loader must refuse when {name}")
            except ValueError:
                pass
        os.remove(PRED)
        check(load_predecessors({}) == {}, "no cik_predecessors.json means nothing adopted")
    finally:
        PRED = real_pred
    # 15b. the EARN-009 label: replays the record against the feed as it stands
    lf = {"XOM": {"cik": "0000000099", "events": [E("2011-04-01"), E("2012-01-05"), E("2026-07-31")]},
          "GOOG": {"cik": "0000000098", "events": [E("2010-01-01"), E("2026-02-02")]}, "NONE": {"cik": "0000000097", "events": []}}
    rx = {"kind": "predecessor", "ticker": "XOM", "inserted_dates": ["2011-04-01", "2012-01-05"], "predecessor_names": ["EXXON MOBIL CORP"]}
    rg = {"kind": "predecessor", "ticker": "GOOG", "inserted_dates": ["2010-01-01"], "predecessor_names": ["GOOGLE INC. (old)", "Other Co"]}
    check(predecessor_label(lf, {"corrections": []}) == LABEL_MARK + " none", "no adoption on record: the line says none")
    check(predecessor_label(lf, {"corrections": [rg, rx]}) == LABEL_MARK + " GOOG 1 of 2 (GOOGLE INC. old; Other Co), XOM 2 of 3 (EXXON MOBIL CORP)",
          "tickers sorted, k of n counted from the feed as it stands, registrant names listed, parentheses stripped from names")
    check(predecessor_label(lf, {"corrections": [rx, {"kind": "predecessor_reversed", "ticker": "XOM", "removed_dates": rx["inserted_dates"]}]}) == LABEL_MARK + " none",
          "a reversed adoption is not listed")
    check(predecessor_label(lf, {"corrections": [rx, {"kind": "predecessor_reversed", "ticker": "XOM"}, rx]}) == LABEL_MARK + " XOM 2 of 3 (EXXON MOBIL CORP)",
          "adopted, reversed, adopted again: listed once")
    lf2 = copy.deepcopy(lf); lf2["XOM"]["events"] = [E("2026-07-31")]
    check(predecessor_label(lf2, {"corrections": [rx]}) == LABEL_MARK + " none", "dates the record lists that the feed no longer holds are not counted (k == 0 is not listed)")
    check(predecessor_label({}, {"corrections": [rx]}) == LABEL_MARK + " none" and "EDGAR" not in LABEL_MARK,
          "a ticker absent from the feed is not listed, and the marker never contains the word EDGAR")
    check(predecessor_label(lf, {"corrections": [{"kind": "stamp", "ticker": "XOM"}, {"kind": "stamp_at_write", "ticker": "XOM"}]}) == LABEL_MARK + " none",
          "stamp corrections are not adoptions")
    # ... the command: prints the whole line and exits 0; a missing or unreadable record or feed is an ERROR (exit 1, nothing on stdout), never `none`
    import contextlib, io, tempfile as _tf
    real_paths, ld = (FEED, CORR), _tf.mkdtemp()
    try:
        FEED, CORR = os.path.join(ld, "feed.json"), os.path.join(ld, "corr.json")
        json.dump(lf, open(FEED, "w"))
        json.dump({"corrections": [rx]}, open(CORR, "w"))

        def label_cli():
            o, e = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(o), contextlib.redirect_stderr(e):
                rc = main(["--predecessor-label"])
            return rc, o.getvalue(), e.getvalue()
        rc, o, e = label_cli()
        check(rc == 0 and o == LABEL_MARK + " XOM 2 of 3 (EXXON MOBIL CORP)\n" and not e, "--predecessor-label prints the whole line and exits 0")
        os.remove(CORR)
        rc, o, e = label_cli()
        check(rc == 1 and not o and "cannot be computed" in e, "a MISSING record is an error (exit 1, nothing on stdout), never `none`")
        open(CORR, "w").write("[1]")
        check(label_cli()[0] == 1, "a record that is not an object is an error")
        open(CORR, "w").write("{not json")
        check(label_cli()[0] == 1, "an unreadable record is an error")
        json.dump({"corrections": [rx]}, open(CORR, "w")); os.remove(FEED)
        check(label_cli()[0] == 1, "a missing feed is an error")
    finally:
        FEED, CORR = real_paths
    # 15d. EARN-011, END TO END: main() against a scratch tree and a faked SEC. Two registrants SEC serves double-converted (AAA, BBB), one it serves true (CCC).
    import shutil, tempfile as _tf2                      # contextlib and io are imported above (15b)
    e_cik = {"AAA": "0000000001", "BBB": "0000000002", "CCC": "0000000003"}
    e_url = lambda n: f"https://data.sec.gov/submissions/CIK000000000{n}.json"
    e_utc = {"H-1": "2026-05-28T20:17:37", "H-2": "2026-08-20T20:17:37", "H-3": "2026-05-14T10:59:50", "H-4": "2026-06-01T20:17:37"}
    e_old = R("2026-04-01", i="9.01")                       # an older filing, so every held print is INSIDE SEC's window (the oldest day is never judged)

    def e_pages(**over):
        pg = {e_url(1): {"filings": {"recent": block([e_old, R("2026-05-28", s=dbl("2026-05-28T20:17:37"), acc="H-1"), R("2026-08-20", s=dbl("2026-08-20T20:17:37"), acc="H-2")]), "files": []}},
              e_url(2): {"filings": {"recent": block([e_old, R("2026-05-14", s=dbl("2026-05-14T10:59:50"), acc="H-3")]), "files": []}},
              e_url(3): {"filings": {"recent": block([e_old, R("2026-06-01", acc="H-4")]), "files": []}}}
        for n, rows in over.items():
            pg[e_url(int(n[1:]))] = {"filings": {"recent": block([e_old] + rows), "files": []}}
        return pg
    e_feed = {"AAA": {"cik": "0000000001", "events": [E("2026-05-28"), E("2026-08-20")]}, "BBB": {"cik": "0000000002", "events": [E("2026-05-14", "10:59:50")]},
              "CCC": {"cik": "0000000003", "events": [E("2026-06-01")]}}
    e_text = lambda utc_map: (lambda url: hdr_of(utc_map[re.search(r"/([^/]+)\.hdr\.sgml$", url).group(1)]))

    def e2e(argv, feed_obj, pages_obj, text_fn, corr_obj=None, cmap=None, lock=None):
        """one main() in a scratch directory with FEED/RUN/CORR/CIK_MAP and the two SEC fetchers replaced. lock: None, "idle" (a lock file nobody holds)
        or "held" (the test holds it, as the nightly job would). -> (rc, stdout, facts)"""
        global FEED, RUN, CORR, CIK_MAP, PRED, get, get_text
        saved = (FEED, RUN, CORR, CIK_MAP, PRED, get, get_text)
        d = _tf2.mkdtemp()
        FEED, RUN, CORR, CIK_MAP, PRED = (os.path.join(d, n) for n in ("feed.json", "run.json", "corr.json", "cik_map.json", "pred.json"))
        try:
            json.dump(cmap or e_cik, open(CIK_MAP, "w"))
            open(FEED, "w").write(json.dumps(feed_obj))
            os.utime(FEED, (1000000000, 1000000000))                     # a rewrite would move this
            held_fd = None
            if lock:
                held_fd = os.open(FEED + ".lock", os.O_CREAT | os.O_RDWR, 0o644)
                if lock == "held":
                    fcntl.flock(held_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                else:
                    os.close(held_fd); held_fd = None
            if corr_obj is not None:
                json.dump(corr_obj, open(CORR, "w"))
            get, get_text = (lambda u: pages_obj[u]), text_fn
            o = io.StringIO()
            with contextlib.redirect_stdout(o), contextlib.redirect_stderr(io.StringIO()):
                rc = main(argv)
            facts = {"feed": open(FEED, "rb").read(), "mtime": os.stat(FEED).st_mtime, "run": json.load(open(RUN)) if os.path.exists(RUN) else None,
                     "corr": json.load(open(CORR)) if os.path.exists(CORR) else None, "lock": os.path.exists(FEED + ".lock")}
            if lock == "idle":                                           # was the lock left free? (a probe must let go at once)
                probe = os.open(FEED + ".lock", os.O_RDWR)
                try:
                    fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB); facts["lock_free_after"] = True
                except BlockingIOError:
                    facts["lock_free_after"] = False
                finally:
                    os.close(probe)
            return rc, o.getvalue(), facts
        finally:
            if held_fd is not None:
                os.close(held_fd)
            FEED, RUN, CORR, CIK_MAP, PRED, get, get_text = saved
            shutil.rmtree(d, ignore_errors=True)
    feed_bytes = json.dumps(e_feed).encode()
    # (a) the 10-02 situation: SEC serves 3 held prints double-converted. Exit 0, ONE summary line, no ATTENTION, the feed byte-identical and not rewritten, no record.
    rc, out, fx = e2e([], e_feed, e_pages(), e_text(e_utc))
    check(rc == 0 and "ATTENTION" not in out, "(a) double-converted held prints alone: exit 0 and no ATTENTION line")
    check("  3 held prints SEC serves double-converted (+4h EDT / +5h EST) in 2 ticker(s); a sample of 3 header-verified: 3 equal the held stamp (all 3 are right)\n" in out
          and out.count("held prints SEC serves double-converted") == 1, "(a) counted in ONE summary line, never per print")
    check(fx["feed"] == feed_bytes and fx["mtime"] == 1000000000 and fx["corr"] is None, "(a) the feed's bytes are identical and it was not rewritten; no corrections record")
    check(fx["run"] and fx["run"]["changed"] == [] and fx["run"]["failed"] == [] and fx["run"]["double_converted"] == 3 and fx["run"]["double_converted_tickers"] == 2
          and len(fx["run"]["double_sample"]) == 3 and fx["run"]["feed_sha256"] == hashlib.sha256(feed_bytes).hexdigest(), "(a) the run stamp carries the count and the sample, and flags nothing the resolver reads")
    # (b) a REAL change still alarms: AAA's 2026-08-20 print is listed with a stamp that is none of the held one, its evening form or its double conversion
    rc, out, fx = e2e([], e_feed, e_pages(A1=[R("2026-05-28", s=dbl("2026-05-28T20:17:37"), acc="H-1"), R("2026-08-20", t="21:00:00", acc="H-2")]), e_text(e_utc))
    check(rc == 2 and "ATTENTION CHANGED AAA 2026-08-20" in out and "ATTENTION CHANGED AAA 2026-05-28" not in out and "  2 held prints SEC serves double-converted" in out,
          "(b) a real change still exits 2 with its own ATTENTION CHANGED line, beside a count of the others")
    check(fx["feed"] == feed_bytes and fx["run"]["changed"] == [["AAA", "2026-08-20", "2026-08-20T20:17:37"]], "(b) it is KEPT as held, and the run stamp lists it for the resolver")
    # (c) a SAMPLE MISMATCH alarms: BBB's filing header says 11:30:00 UTC, not the held 10:59:50, though SEC's JSON is the held stamp double-converted
    rc, out, fx = e2e([], e_feed, e_pages(), e_text(dict(e_utc, **{"H-3": "2026-05-14T11:30:00"})))
    check(rc == 2 and "ATTENTION CHANGED BBB 2026-05-14" in out and "NOT proven" in out and "11:30:00" in out and "1 not confirmed (ATTENTION below)" in out,
          "(c) a header-sample print that disagrees with the held stamp exits 2, says so, and says the others rest on the sample")
    check(fx["feed"] == feed_bytes and fx["run"]["changed"] == [["BBB", "2026-05-14", "2026-05-14T10:59:50"]], "(c) the held stamp is KEPT and the run stamp lists the print")
    # (c2) an unreadable sample header alarms too (never counted as agreement)
    rc, out, fx = e2e([], e_feed, e_pages(), lambda url: (_ for _ in ()).throw(ConnectionError("dead")) if "H-3" in url else e_text(e_utc)(url))
    check(rc == 2 and "ATTENTION FAILED BBB (header sample for 2026-05-14 unreadable" in out and fx["feed"] == feed_bytes
          and "a sample of 3 header-verified: 2 equal the held stamp, 1 not confirmed (ATTENTION below)" in out, "(c2) a sample header that cannot be read exits 2, and the summary line does not count it as agreement")
    # (d) --check: the whole pass against (faked) live SEC, a genuinely new print for CCC, and NOTHING written, no lock, no run stamp, no record
    new_ccc = {"C3": [R("2026-06-01", acc="H-4"), R("2026-09-30", acc="H-5")]}                      # e_pages(C3=...) replaces CCC's rows
    e_utc5 = dict(e_utc, **{"H-5": "2026-09-30T20:17:37"})
    rc, out, fx = e2e(["--check"], e_feed, e_pages(**new_ccc), e_text(e_utc5))
    check(rc == 0 and "DRY RUN" in out and "1 new print(s) in 1 ticker(s)" in out and "new  CCC: 2026-09-30" in out, "(d) --check reports what a run would do, with the same exit code")
    check(fx["feed"] == feed_bytes and fx["mtime"] == 1000000000 and fx["run"] is None and fx["corr"] is None and not fx["lock"], "(d) --check writes no feed, no run stamp, no record and takes no lock")
    rc, out, fx = e2e([], e_feed, e_pages(**new_ccc), e_text(e_utc5))
    check(rc == 0 and fx["lock"] and fx["run"] and json.loads(fx["feed"])["CCC"]["events"][-1] == {"date": "2026-09-30", "accepted": "2026-09-30T20:17:37"}
          and {k: v for k, v in json.loads(fx["feed"]).items() if k != "CCC"} == {k: v for k, v in e_feed.items() if k != "CCC"}, "(d) the same run without --check writes the new print and nothing else")
    rc, out, fx = e2e(["--check", "--correct-stamps", "AAA:2026-05-28", "--note", "x"], e_feed, e_pages(), e_text(e_utc))
    check(rc == 1 and "REFUSED" in out and "--check" in out and fx["feed"] == feed_bytes, "(d) --check cannot be combined with an explicit correction")
    # (e) a NEW print from a switched registrant: header-checked, stored as the header's UTC (not the shifted JSON stamp), recorded; held prints stay byte-identical
    new_aaa = {"A1": [R("2026-05-28", s=dbl("2026-05-28T20:17:37"), acc="H-1"), R("2026-08-20", s=dbl("2026-08-20T20:17:37"), acc="H-2"),
                      R("2026-10-02", s=dbl("2026-10-02T20:15:15"), acc="H-6")]}                  # e_pages(A1=...) replaces AAA's rows
    rc, out, fx = e2e([], e_feed, e_pages(**new_aaa), e_text(dict(e_utc, **{"H-6": "2026-10-02T20:15:15"})))
    nf = json.loads(fx["feed"])
    check(rc == 0 and "ATTENTION" not in out and nf["AAA"]["events"][:2] == e_feed["AAA"]["events"] and nf["AAA"]["events"][2] == {"date": "2026-10-02", "accepted": "2026-10-02T20:15:15"}
          and {k: v for k, v in nf.items() if k != "AAA"} == {k: v for k, v in e_feed.items() if k != "AAA"} and "doubled -" in out,
          "(e) a new print from a switched registrant is stored as the header's UTC, not as served; the held prints are untouched")
    rec_e = (fx["corr"] or {}).get("corrections", [])
    check(len(rec_e) == 1 and rec_e[0]["kind"] == "stamp_at_write" and rec_e[0]["was"] == "2026-10-03T00:15:15" and rec_e[0]["now"] == "2026-10-02T20:15:15"
          and "double conversion" in rec_e[0]["note"] and rec_e[0]["accession"] == "H-6", "(e) it is recorded in the corrections ledger as a stamp_at_write entry that names the double conversion")
    # (f) the same print when its header cannot be read: DEFERRED, not written (exit 2), as before
    rc, out, fx = e2e([], e_feed, e_pages(**new_aaa), lambda url: (_ for _ in ()).throw(ConnectionError("dead")) if "H-6" in url else e_text(e_utc)(url))
    check(rc == 2 and "ATTENTION DEFERRED AAA 2026-10-02" in out and json.loads(fx["feed"])["AAA"] == e_feed["AAA"], "(f) a new print whose header cannot be read is still DEFERRED")
    # (a2) more doubled prints than the sample: the summary line says what was proved and what was counted on the sample
    f12e, u12e, t12e, c12e = sw_world(12)
    rc, out, fx = e2e([], f12e, u12e, t12e, cmap={"SW": "0000000021"})
    check(rc == 0 and "  12 held prints SEC serves double-converted (+4h EDT / +5h EST) in 1 ticker(s); a sample of 4 header-verified: 4 equal the held stamp "
          "(those 4 are right; the other 8 are counted on that sample, not verified)\n" in out and fx["feed"] == json.dumps(f12e).encode() and fx["mtime"] == 1000000000,
          "(a2) 12 doubled prints, 4 read: the line says the other 8 are counted on the sample, not verified; nothing written")
    # (d2) --check with a print that HAS to be normalised: a non-empty ledger would expose a --check that appends
    rc, out, fx = e2e(["--check"], e_feed, e_pages(**new_aaa), e_text(dict(e_utc, **{"H-6": "2026-10-02T20:15:15"})))
    check(rc == 0 and "doubled -" in out and fx["feed"] == feed_bytes and fx["run"] is None and fx["corr"] is None and not fx["lock"],
          "(d2) --check with a print that needs normalising writes no feed, run stamp or corrections record")
    # (d3) --check refuses while a writer holds the feed's lock, and a lock nobody holds is let go at once
    rc, out, fx = e2e(["--check"], e_feed, e_pages(), e_text(e_utc), lock="held")
    check(rc == 1 and "REFUSED" in out and "lock is held" in out and "ATTENTION" not in out and "double-converted" not in out and fx["feed"] == feed_bytes and fx["run"] is None,
          "(d3) --check refuses to start while the nightly writer holds the feed's lock, fetching and writing nothing")
    rc, out, fx = e2e(["--check"], e_feed, e_pages(), e_text(e_utc), lock="idle")
    check(rc == 0 and fx["lock_free_after"] is True and fx["run"] is None and fx["feed"] == feed_bytes, "(d3) an idle lock does not stop --check and the probe leaves it free")
    # (g) main() seeds the sample with the calendar date; update() draws from the rng it is given
    seen_seed, real_R = [], random.Random
    random.Random = lambda *a: (seen_seed.append(a), real_R(*a))[1]
    try:
        e2e([], e_feed, e_pages(), e_text(e_utc))
    finally:
        random.Random = real_R
    check(seen_seed == [(dt.date.today().isoformat(),)], "(g) main() seeds the header sample with the calendar date, once")
    sm = []
    for seed_ in ("2026-10-03", "2026-10-03", "2026-10-04"):
        f_, u_, t_, c_ = sw_world(12)
        _, r_ = update(f_, {"SW": "0000000021"}, lambda u, u_=u_: u_[u], t_, random.Random(seed_))
        sm.append([x["date"] for x in r_["double_sample"]])
    check(sm[0] == sm[1] and sm[0] != sm[2], "(g) update() draws from the rng it is given: same seed same prints, another day other prints")
    # (g2) the job's retry: a print that joins the population, or a registrant that turns mixed, between attempts never swaps a sampled print out
    pop_ = [{"ticker": f"T{i:02d}", "date": "2026-05-28", "mixed": False} for i in range(60)]
    s1_ = {(y["ticker"], y["date"]) for y in pick_sample(pop_, DOUBLE_SAMPLE, random.Random("2026-10-03"))}
    ok_g2 = True
    for i in range(0, 61, 3):
        p2 = pop_[:i] + [{"ticker": "T%02dx" % i, "date": "2026-10-03", "mixed": False}] + pop_[i:]
        ok_g2 &= len(s1_ - {(y["ticker"], y["date"]) for y in pick_sample(p2, DOUBLE_SAMPLE, random.Random("2026-10-03"))}) <= 1
    for t_ in sorted({t for t, d in s1_}):
        p3 = [dict(y, mixed=True) if y["ticker"] == t_ else y for y in pop_]
        ok_g2 &= s1_ <= {(y["ticker"], y["date"]) for y in pick_sample(p3, DOUBLE_SAMPLE, random.Random("2026-10-03"))}
    check(ok_g2, "(g2) a print that joins the population, or a registrant that turns mixed, between attempts never swaps a sampled print out")
    # (h) a dead sampler must not look clean: doubled prints counted and no sample read is ATTENTION
    real_ds, DOUBLE_SAMPLE = DOUBLE_SAMPLE, 0
    try:
        rc, out, fx = e2e([], e_feed, e_pages(), e_text(e_utc))
    finally:
        DOUBLE_SAMPLE = real_ds
    check(rc == 2 and "NO header sample was read (ATTENTION below)" in out and "ATTENTION SAMPLE: 3 held prints" in out and fx["feed"] == feed_bytes,
          "(h) doubled prints counted with no header read at all exits 2: a dead sampler is not a clean run")
    # (j) main() still refuses to write when the pass moved a held print (the invariant is CALLED, not just defined: Brain section 2)
    real_update = update
    update = lambda feed_, *a, **k: (feed_["AAA"]["events"][0].update(accepted="2026-05-28T00:00:00"), real_update(feed_, *a, **k))[1]
    try:
        rc, out, fx = e2e([], e_feed, e_pages(), e_text(e_utc))
    finally:
        update = real_update
    check(rc == 1 and "INVARIANT BROKEN" in out and fx["feed"] == feed_bytes and fx["run"] is None, "(j) a pass that moved a held print is REFUSED by main() and writes nothing")
    # 16. the throttle keeps under SEC's 10 requests a second; the feed's format is json.dumps defaults
    check(MIN_GAP_S >= 0.1, "request spacing is at least 0.1s (<= 10/s)")
    check(json.dumps({"a": [1]}) == '{"a": [1]}', "json.dumps default format is the feed's format")
    print("fetch_earnings_8k selftest: " + ("PASS" if not bad else "FAIL"))
    for b in bad:
        print("  FAIL:", b)
    return not bad


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
