#!/usr/bin/env python
"""earnings_postgap_study.py — does the [earnings] desk's ACTUAL traded window survive
the same 6,442-print EDGAR test that killed the unconditional post-print drift?

Written 2026-09-20 by the earnings-week agent, answering the council directive of
2026-09-18: "the earnings run-up study already convicted your window ... state which of
your 9 rows sit inside the window that study killed."

WHY A SECOND SCRIPT AND NOT A CITATION. preprint_runup_study.py measures `post5` as
close[T+1] -> close[T+5] on EVERY print, unconditionally. The earnings desk does not
trade that. Its plans, as check_plans.py executes them, are:

    trigger : |open[T] / close[T-1] - 1| >= 4%   (T = first tradeable session)
    entry   : open[T]                            (the gap-day open, not a later close)
    exit    : close[T+5]                         (check_date = trigger + 7 calendar days)

Two differences, both material: the desk's window (a) starts one full session EARLIER,
so it contains the whole gap-day open->close that `post5` discards, and (b) fires only on
a >=4% gap, which `post5` never conditions on. Firm Brain §6 — measure in the rule's OWN
units — forbids reading the desk's verdict off a window the desk does not trade.

Same event set (data/edgar/earnings_8k.json, 8-K Item 2.02), same price panel, same
SPY-excess, same announcement-week clustering, same drop-the-best-week reading.

PRIOR, WRITTEN BEFORE THE RUN. The unconditional post-print number is -0.04%/week at
t=-0.31 — no drift to inherit. The desk's 9 live rows read +3.27% mean, 7/9, on a sample
far too small to argue with. Claude expects the conditional legs to land near zero too,
with the gap-day open->close contributing most of whatever is left, and expects the
DOWN-gap leg (the desk's favourite, 5 of its 9 rows) to be the weaker of the two once
measured against SPY rather than against zero.

CORRECTION 2026-09-30 (EARN-006). print_session() read the clock off SEC's acceptance stamp as if it were New York time. The
stamp is UTC, so a print accepted between 16:00 UTC and the bell (12:00-16:00 ET in summer, 11:00-16:00 ET in winter) was filed as
after-close and landed one session late. On the 2026-09-30 feed 84 such mid-session prints since 2011 move one session earlier
(82 of them join this study and the run-up study, and 18 of those change leg). It now converts the stamp to America/New_York
(zoneinfo, DST-correct) before comparing. The corrected run is reports/earnings_postgap_study_2026-09-30.json;
reports/earnings_postgap_study.json (2026-09-20) is kept unchanged. On today's panel (open/close through 2026-09-25),
uncorrected -> corrected, excess vs SPY per announcement week (week-clustered t): up-gap +0.452 (1.40) -> +0.464 (1.45), down-gap
+0.221 (0.38) -> +0.175 (0.30), all prints -0.014 (-0.09) -> -0.023 (-0.14), on 6,466 -> 6,467 prints; the 09-20 file read up-gap
+0.451 (1.40) and down-gap +0.221 (0.38) on 6,469. Two figures quoted above came from the run-up study on the 2026-09-17 panel and
no longer reproduce: "the 6,442-print set" is 6,390 prints on today's panel (the 15-year panel's start rolled forward), and
"-0.04%/week at t=-0.31" reads -0.03 (t -0.21) under the old stamp rule and -0.01 (t -0.12) under the corrected one. Not changed:
(1) 4 prints in 15 years accepted on an early-close day after the 13:00 ET bell, which the old rule filed right by accident and the
flat 16:00 test now files one session early (named in the report's provenance; keeping them after-close moves no leg by more than
0.002); (2) the 196 prints accepted 09:30-16:00 ET (194 in this join) keep their own session, so this study's open[T] entry
precedes them; dropping them entirely gives up-gap +0.431 (t 1.32) and down-gap +0.204 (t 0.35).

CAVEAT to the correction above, found the same night: the stamp is UTC for every print the collector fetched days after its filing,
but the one print it fetched on its filing evening (MU, 2026-09-30) is held as 16:02:22, an ET wall-clock value, while SEC now lists
it at 20:02:22Z. Such a stamp is filed mid-session here (the old rule filed it after-close by luck). It is in neither study's join
yet; the feed never rewrites a held print, so the fix belongs to the collector (fetch_earnings_8k.py), not to these studies.
CORRECTED 2026-10-01 (EARN-008, strategy-lab 31302de): the feed now holds MU 2026-09-30 at 20:02:22 UTC, and every new print is checked against its filing header, so the caveat above is obsolete.
"""
import csv, datetime as dt, hashlib, json, math, os, statistics as st
from bisect import bisect_left
from zoneinfo import ZoneInfo

BASE = os.path.dirname(os.path.abspath(__file__))
# EARN-006 (2026-09-30): each run writes a DATED file beside the old one, created exclusively (a re-run never overwrites).
# reports/earnings_postgap_study.json (the 2026-09-20 run, whose print_session read SEC's UTC stamp as New York time) is
# kept byte-for-byte as the record of what that rule produced (BENCH-002).
OUT = f"{BASE}/reports/earnings_postgap_study_{dt.date.today().isoformat()}.json"
START = "2011-01-01"
THRESH = 0.04
HOLD = 5
NY = ZoneInfo("America/New_York")    # EARN-006: calendar-correct EST/EDT, never a fixed UTC offset
UTC = dt.timezone.utc
PRINT_SESSION_RULE = ("SEC acceptance stamp (UTC) converted to America/New_York (zoneinfo, DST-correct), then: before 16:00 ET -> "
                      "that session, else the next session (EARN-006, 2026-09-30)")
# EARN-006 residual, disclosed and NOT corrected: prints accepted on an early-close day AFTER the 13:00 ET bell but before 16:00 ET.
# The old UTC rule filed them right by accident; the flat 16:00 ET test files them one session early (no historical early-close
# table exists in the estate; sessions.EARLY_CLOSES holds 2026-27 only).
EARLY_CLOSE_PRINTS = (("ABBV", "2024-07-03T18:07:48"), ("ABBV", "2025-07-03T17:07:55"),
                      ("NKE", "2018-07-03T18:31:40"), ("TSLA", "2017-07-03T19:21:19"))


def sha256_of(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest() if os.path.exists(path) else None


def provenance(corrects, panel_files, panel_dates):
    """What this run read and what it supersedes, so the vintage it was measured on can be pinned (EARN-006)."""
    return {"feed_sha256": sha256_of(f"{BASE}/data/edgar/earnings_8k.json"),
            "panel_files": panel_files, "panel_first_date": panel_dates[0], "panel_last_date": panel_dates[-1],
            "corrects": corrects, "corrects_sha256": sha256_of(f"{BASE}/{corrects}"),
            "early_close_prints_filed_one_session_early": [{"ticker": t, "accepted_utc": a} for t, a in EARLY_CLOSE_PRINTS]}


def load(fn):
    rows = list(csv.DictReader(open(f"{BASE}/data/{fn}")))
    dates = [r["date"] for r in rows]
    px = {t: [] for t in rows[0] if t != "date"}
    for r in rows:
        for t in px:
            v = r.get(t)
            px[t].append(float(v) if v not in (None, "") else None)
    return dates, px


def print_session(accepted, dates):
    """First session index on which the announcement could be traded (same rule as the
    run-up study, so the two are joinable event-for-event). `accepted` is SEC's acceptance stamp
    and it is UTC: it is converted to New York time before the date or the clock is read (EARN-006)."""
    et = dt.datetime.fromisoformat(accepted[:19]).replace(tzinfo=UTC).astimezone(NY)   # EARN-006: UTC stamp -> New York clock and date
    d, hhmm = et.strftime("%Y-%m-%d"), et.strftime("%H:%M")
    i = bisect_left(dates, d)
    if i >= len(dates):
        return None
    if dates[i] == d and hhmm < "16:00":
        return i
    return i + 1 if (dates[i] == d) else i


def t_of(v):
    if len(v) < 3:
        return None
    s = st.pstdev(v) * math.sqrt(len(v) / (len(v) - 1))
    return round(st.mean(v) / (s / math.sqrt(len(v))), 2) if s else None


def summarise(ev):
    """ev: list of (week, excess_pct). Week-clustered, per the study it replicates."""
    if not ev:
        return {"n": 0}
    byw = {}
    for w, x in ev:
        byw.setdefault(w, []).append(x)
    wk = {w: st.mean(v) for w, v in byw.items()}
    vals = list(wk.values())
    out = {"n": len(ev), "weeks": len(vals),
           "mean_per_week": round(st.mean(vals), 3),
           "t_week": t_of(vals),
           "median_event": round(st.median([x for _, x in ev]), 3),
           "hit": round(100 * sum(1 for _, x in ev if x > 0) / len(ev), 1)}
    if len(vals) > 3:
        best = max(wk, key=lambda w: wk[w])
        rest = [v for w, v in wk.items() if w != best]
        out["drop_best_week"] = round(st.mean(rest), 3)
        out["t_drop_best"] = t_of(rest)
    return out


def main():
    dates, op = load("open.csv")
    d2, cl = load("close.csv")
    assert dates == d2, "open.csv and close.csv are not on the same date index"
    events = json.load(open(f"{BASE}/data/edgar/earnings_8k.json"))
    events = [dict(e, ticker=t) for t, v in events.items() for e in v["events"]]

    legs = {k: [] for k in ("up", "down", "all_gaps", "no_gap", "unconditional")}
    gapday = {"up": [], "down": []}
    eras = {"2011-15": {}, "2016-20": {}, "2021-26": {}}
    for e in eras:
        eras[e] = {k: [] for k in ("up", "down")}
    seen = 0
    for ev in events:
        t = ev.get("ticker")
        acc = ev.get("accepted") or ev.get("acceptedTime") or ev.get("acceptance")
        if not t or not acc or t not in op or t not in cl:
            continue
        if acc[:10] < START:
            continue
        i = print_session(acc, dates)
        if i is None or i < 1 or i + HOLD >= len(dates):
            continue
        o, pc = op[t][i], cl[t][i - 1]
        xo, xc = cl[t][i + HOLD], op["SPY"][i]
        sc = cl["SPY"][i + HOLD]
        if None in (o, pc, xo, xc, sc) or 0 in (o, pc, xc):
            continue
        seen += 1
        gap = o / pc - 1
        stock = (xo / o - 1) * 100
        spy = (sc / xc - 1) * 100
        exc = stock - spy
        wk = dt.date.fromisoformat(dates[i]).isocalendar()[:2]
        wk = f"{wk[0]}-W{wk[1]:02d}"
        legs["unconditional"].append((wk, exc))
        era = "2011-15" if dates[i] < "2016-01-01" else ("2016-20" if dates[i] < "2021-01-01" else "2021-26")
        if abs(gap) >= THRESH:
            legs["all_gaps"].append((wk, exc))
            side = "up" if gap > 0 else "down"
            legs[side].append((wk, exc))
            eras[era][side].append((wk, exc))
            gd = cl[t][i]
            if gd:
                gapday[side].append((wk, (gd / o - 1) * 100 - (cl["SPY"][i] / xc - 1) * 100))
        else:
            legs["no_gap"].append((wk, exc))

    rep = {"generated": dt.datetime.now().isoformat(timespec="seconds"),
           "events_joined": seen, "prices_through": dates[-1],
           "print_session_rule": PRINT_SESSION_RULE,
           "provenance": provenance("reports/earnings_postgap_study.json", ["data/open.csv", "data/close.csv"], dates),
           "window": "open[T] -> close[T+5], excess vs SPY over identical dates",
           "trigger": f"|open[T]/close[T-1]-1| >= {THRESH:.0%}",
           "legs": {k: summarise(v) for k, v in legs.items()},
           "gap_day_only": {k: summarise(v) for k, v in gapday.items()},
           "eras": {e: {s: summarise(v) for s, v in d.items()} for e, d in eras.items()}}
    os.makedirs(f"{BASE}/reports", exist_ok=True)
    with open(OUT, "x") as fh:          # EARN-006: exclusive create - never overwrites an existing output (BENCH-002)
        json.dump(rep, fh, indent=1)
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
