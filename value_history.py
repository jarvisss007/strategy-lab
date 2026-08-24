#!/usr/bin/env python3
"""value_history.py — point-in-time annual fundamentals for FAMILY 9 (own-history value).

Registered 2026-08-24 in REGISTRY.md before this file existed; the desk's forecast (p=0.20)
is already on file. This builds the one missing input: for every universe name, an ANNUAL
panel from SEC companyfacts where every number carries the date it was FILED — the
earnings_lab law. Nothing here uses a fact before the market could have read it.

Per name and fiscal year (10-K facts): net income, stockholders' equity, CFO, total and
current assets, current liabilities, long-term debt, revenue, gross profit (or cost of
revenue), diluted shares — plus the FILED date of that 10-K. From these the gate computes,
at any decision date t: trailing P/E and P/B via MARKET CAP (filed shares × raw price, both
in the same era's basis, so corporate splits cannot fabricate a ratio — the GRML lesson,
applied in advance) and the Piotroski signals year-over-year.

Writes data/value_panel.csv (tracked — it is derived-but-slow, the firm keeps the ingot).
Run: /opt/anaconda3/bin/python value_history.py [--limit N]
"""
import csv, json, os, sys, time, urllib.request, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
WATCH = os.path.expanduser("~/stock-radar/watchlist.csv")
OUT = os.path.join(HERE, "data", "value_panel.csv")
UA = {"User-Agent": "Anupam Patil anupam.p.patil@gmail.com"}
CONCEPTS = {
    "ni": ["NetIncomeLoss"],
    "equity": ["StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"],
    "cfo": ["NetCashProvidedByUsedInOperatingActivities"],
    "assets": ["Assets"],
    "assets_cur": ["AssetsCurrent"],
    "liab_cur": ["LiabilitiesCurrent"],
    "ltd": ["LongTermDebtNoncurrent", "LongTermDebt"],
    "revenue": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"],
    "gross": ["GrossProfit"],
    "shares": ["WeightedAverageNumberOfDilutedSharesOutstanding", "CommonStockSharesOutstanding"],
}


def jget(url):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read())


def annual_series(facts, names):
    """{fy: (value, filed)} from 10-K facts, preferring the earliest filing of each FY."""
    out = {}
    for name in names:
        node = facts.get("us-gaap", {}).get(name) or facts.get("dei", {}).get(name)
        if not node:
            continue
        for unit, rows in node.get("units", {}).items():
            for r in rows:
                if r.get("form") not in ("10-K", "10-K/A") or r.get("fp") != "FY":
                    continue
                fy, val, filed = r.get("fy"), r.get("val"), r.get("filed")
                # a fiscal year's number must cover ~a year, not a quarter restated under FY
                s, e = r.get("start"), r.get("end")
                if s and e:
                    try:
                        if (dt.date.fromisoformat(e) - dt.date.fromisoformat(s)).days < 300:
                            continue
                    except ValueError:
                        pass
                if fy is None or val is None or filed is None:
                    continue
                if fy not in out or filed < out[fy][1]:
                    out[fy] = (float(val), filed)
        if out:
            return out
    return out


def instant_series(facts, names):
    """Balance-sheet (instant) concepts: {fy: (value, filed)} off FY rows."""
    out = {}
    for name in names:
        node = facts.get("us-gaap", {}).get(name)
        if not node:
            continue
        for unit, rows in node.get("units", {}).items():
            for r in rows:
                if r.get("form") not in ("10-K", "10-K/A") or r.get("fp") != "FY":
                    continue
                fy, val, filed = r.get("fy"), r.get("val"), r.get("filed")
                if fy is None or val is None or filed is None:
                    continue
                if fy not in out or filed < out[fy][1]:
                    out[fy] = (float(val), filed)
        if out:
            return out
    return out


def main():
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 999
    tickers = [r["ticker"].strip() for r in csv.DictReader(open(WATCH))
               if r["ticker"].strip() and "=" not in r["ticker"] and "-" not in r["ticker"]][:limit]
    ct = jget("https://www.sec.gov/files/company_tickers.json")
    cik = {v["ticker"]: str(v["cik_str"]).zfill(10) for v in ct.values()}
    rows, missed = [], []
    for i, tk in enumerate(tickers):
        c = cik.get(tk)
        if not c:
            missed.append((tk, "no CIK")); continue
        try:
            facts = jget(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{c}.json").get("facts", {})
        except Exception as e:
            missed.append((tk, type(e).__name__)); continue
        series = {}
        for key, names in CONCEPTS.items():
            fn = annual_series if key in ("ni", "cfo", "revenue", "gross", "shares") else instant_series
            series[key] = fn(facts, names)
        fys = sorted(set().union(*[set(s) for s in series.values() if s]) if any(series.values()) else [])
        for fy in fys:
            row = {"ticker": tk, "fy": fy}
            filed_dates = []
            for key in CONCEPTS:
                v = series[key].get(fy)
                row[key] = v[0] if v else ""
                if v:
                    filed_dates.append(v[1])
            if not filed_dates or row.get("ni") == "" or row.get("shares") in ("", 0):
                continue
            row["filed"] = max(filed_dates)          # usable only once EVERYTHING is filed
            rows.append(row)
        time.sleep(0.15)
        if (i + 1) % 25 == 0:
            print(f"  {i+1}/{len(tickers)} fetched, {len(rows)} FY rows")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cols = ["ticker", "fy", "filed"] + list(CONCEPTS)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for r in sorted(rows, key=lambda x: (x["ticker"], x["fy"])):
            w.writerow(r)
    names_ok = len({r['ticker'] for r in rows})
    print(f"value_panel.csv: {len(rows)} FY rows across {names_ok} names "
          f"({len(missed)} skipped: {', '.join(t for t,_ in missed[:8])}{'…' if len(missed)>8 else ''})")


if __name__ == "__main__":
    main()
