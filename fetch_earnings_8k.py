#!/usr/bin/env python
"""fetch_earnings_8k.py — every earnings announcement date the universe ever filed, from EDGAR.

The estate's event study dates earnings by their FOOTPRINT (a gap+volume day), which is only
knowable after the fact. A pre-announcement study needs the date known IN ADVANCE: the 8-K
carrying Item 2.02 is the results announcement itself, and its acceptanceDateTime says whether
the market saw it before or after the close. Writes data/edgar/earnings_8k.json.
SEC etiquette: the desk's UA (stock-radar/fundamentals.py), <= 8 requests a second.
"""
import json, time, urllib.request, os, sys
BASE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Anupam Patil research apati077@ucr.edu"}
cik = json.load(open(f"{BASE}/data/edgar/cik_map.json"))
out_p = f"{BASE}/data/edgar/earnings_8k.json"
out = json.load(open(out_p)) if os.path.exists(out_p) else {}

def get(url):
    time.sleep(0.13)
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))

def pull(rec):
    rows = []
    for i, form in enumerate(rec["form"]):
        if form == "8-K" and "2.02" in (rec["items"][i] or ""):
            rows.append({"date": rec["filingDate"][i], "accepted": rec["acceptanceDateTime"][i][:19]})
    return rows

failed = []
for n, (tk, c) in enumerate(sorted(cik.items())):
    if tk in out and out[tk].get("events"):
        continue
    try:
        d = get(f"https://data.sec.gov/submissions/CIK{c}.json")
        rows = pull(d["filings"]["recent"])
        for f in d["filings"].get("files", []):
            if f["filingTo"] >= "2010-01-01":
                rows += pull(get(f"https://data.sec.gov/submissions/{f['name']}"))
        rows = sorted({r["date"]: r for r in rows}.values(), key=lambda r: r["date"])
        out[tk] = {"cik": c, "events": rows}
    except Exception as e:
        failed.append(f"{tk} ({type(e).__name__})")
    if n % 20 == 0:
        json.dump(out, open(out_p, "w"))
json.dump(out, open(out_p, "w"))
n_ev = sum(len(v["events"]) for v in out.values())
print(f"earnings_8k: {len(out)} names, {n_ev} announcement dates, earliest {min(e['date'] for v in out.values() for e in v['events'])}"
      + (f" · failed: {', '.join(failed)}" if failed else ""))
