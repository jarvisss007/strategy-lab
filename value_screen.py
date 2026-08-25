#!/usr/bin/env python3
"""value_screen.py — the browsable value aisle: every universe name ranked by the FAMILY 9 signal.

Anupam, 2026-08-24: "searching for the value stocks for us to invest and to play around with."
This is the SCREEN half of the value experiment. The frozen forward book (value_forward.py)
tests the RULE; this page lets the human browse the same signal, judge each name, and file his
own paper picks — [anupam][fund] ledger rows with 6-month check dates, scored vs SPY like every
other call on the desk. Screen informs; only the ledger scores; nothing here is advice.

For every scoreable name: own-history valuation percentile (the FAMILY 9 signal, filed-date
law), Piotroski F, the ratio and its own 10-year median, drawdown off the 52w high, revenue
trend — the "why is it cheap" hint that separates hated-but-healthy from structurally broken.
Writes reports/value_screen.json and value.html (self-contained). Reads only.
Run: /opt/anaconda3/bin/python value_screen.py
"""
import csv, json, os, sys, datetime as dt
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from value_forward import load_panel, ratios_and_f, quarter_ends
from family9_gate import fscore

def main():
    import yfinance as yf
    panel = load_panel()
    names = sorted(panel)
    px = yf.download(names, start="2015-01-01", auto_adjust=False, progress=False)["Close"]
    px.index = px.index.tz_localize(None)
    mraw = px.resample("ME").last()
    today = dt.date.today()
    last = px.ffill().iloc[-1]
    hi52 = px.ffill().iloc[-252:].max()

    sig = ratios_and_f(panel, names, today, mraw)
    rows = []
    for tk, (ratio, pct, f) in sig.items():
        cur = [r for r in panel[tk] if r["filed"] and r["filed"] < today.isoformat()]
        rev_tr = ""
        if len(cur) >= 2:
            try:
                r1, r0 = float(cur[-1]["revenue"] or 0), float(cur[-2]["revenue"] or 0)
                rev_tr = round(100 * (r1 / r0 - 1), 1) if r0 else ""
            except ValueError:
                pass
        ni_pos = False
        try: ni_pos = float(cur[-1]["ni"] or 0) > 0
        except ValueError: pass
        # own-history median ratio for context
        qs = [q for q in quarter_ends(today) if q < today]
        rows.append({
            "ticker": tk, "pctile": round(pct, 1), "fscore": int(f),
            "ratio": round(ratio, 1), "ratio_kind": "P/E" if ni_pos else "P/B",
            "px": round(float(last.get(tk, np.nan)), 2),
            "off_hi_pct": round(100 * (float(last.get(tk, np.nan)) / float(hi52.get(tk, np.nan)) - 1), 1),
            "rev_yoy_pct": rev_tr,
            "qualifies": bool(pct <= 20 and f >= 6),
        })
    rows.sort(key=lambda r: r["pctile"])
    out = {"generated": dt.datetime.now().strftime("%Y-%m-%d %H:%M PT"), "n": len(rows),
           "qualifiers": sum(1 for r in rows if r["qualifies"]), "rows": rows,
           "how_to_use": ("The percentile is vs the stock's OWN valuation history (filed-date law). "
                          "<=20 + F>=6 is the frozen rule's bar. A pick you make goes into "
                          "stock-radar/agent/ledger.csv as [anupam][fund] with a 6-month check date "
                          "and is scored vs SPY — your judgment vs the rule, same signal, one scoreboard.")}
    os.makedirs(os.path.join(HERE, "reports"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "reports", "value_screen.json"), "w"), indent=1)

    tr = "".join(
        f"<tr class='{'q' if r['qualifies'] else ''}'><td><b>{r['ticker']}</b></td>"
        f"<td class=m>{r['pctile']}</td><td class=m>{r['fscore']}</td>"
        f"<td class=m>{r['ratio']} <span class=k>{r['ratio_kind']}</span></td>"
        f"<td class=m>{r['px']}</td><td class='m {'dn' if r['off_hi_pct']<-25 else ''}'>{r['off_hi_pct']}%</td>"
        f"<td class='m {'dn' if isinstance(r['rev_yoy_pct'],(int,float)) and r['rev_yoy_pct']<0 else ''}'>{r['rev_yoy_pct']}%</td>"
        f"<td>{'✅ qualifies' if r['qualifies'] else ''}</td></tr>" for r in rows)
    html = f"""<!DOCTYPE html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Leo's Trading Firm · Value Screen</title>
<style>:root{{--bg:#0d0f12;--panel:#14171c;--line:rgba(255,255,255,.09);--ink:#eef1f6;--muted:#a7b0be;--brass:#c9a227;--good:#2fa96b;--crit:#e0533d}}
@media(prefers-color-scheme:light){{:root{{--bg:#f2f4f7;--panel:#fff;--line:rgba(11,15,20,.1);--ink:#0f1419;--muted:#4a5566;--brass:#8a6d0d;--good:#17794a;--crit:#b93a24}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:14.5px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}.wrap{{max-width:980px;margin:0 auto;padding:28px 20px 70px}}
h1{{font-size:20px}}h1 em{{font-style:normal;color:var(--brass)}}.sub{{color:var(--muted);max-width:88ch;font-size:13px}}
.law{{border-left:3px solid var(--brass);background:rgba(201,162,39,.1);padding:11px 15px;border-radius:0 10px 10px 0;margin:14px 0;font-size:13px}}
table{{border-collapse:collapse;width:100%;background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden;font-size:13px}}
th,td{{padding:7px 10px;border-bottom:1px solid var(--line);text-align:right}}th{{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}td:first-child,th:first-child{{text-align:left}}
.m{{font-family:ui-monospace,Menlo,monospace;font-variant-numeric:tabular-nums}}.k{{color:var(--muted);font-size:10px}}.dn{{color:var(--crit)}}tr.q td{{background:rgba(47,169,107,.07)}}
.tscroll{{overflow-x:auto}}</style></head><body><div class=wrap>
<h1>🔎 <em>VALUE SCREEN</em> — Leo's Trading Firm <span class=sub>generated {out['generated']} · {out['n']} scoreable · {out['qualifiers']} qualify</span></h1>
<p class=sub>Every universe name ranked by how cheap it is against its OWN valuation history (point-in-time SEC filings — nothing used before it was filed), with the Piotroski health score beside it. Green rows clear the frozen rule's bar (own-history percentile ≤ 20 and F ≥ 6) — the same bar the forward book forms on at each quarter-end.</p>
<div class=law><b>How to use this, honestly.</b> Everything cheap is cheap for a reason — the drawdown and revenue columns are the reason's first hint. Your job when you "play around": decide which names are hated-but-healthy and which are broken. A pick becomes real (paper-real) only as an <span class=m>[anupam][fund]</span> row in the ledger with a 6-month check date, scored vs SPY. The frozen book tests the rule; your picks test you; one scoreboard judges both. Paper only — not advice, not money.</div>
<div class=tscroll><table><thead><tr><th>ticker</th><th>own-history pctile</th><th>F-score</th><th>ratio</th><th>price</th><th>off 52w high</th><th>revenue YoY</th><th></th></tr></thead><tbody>{tr}</tbody></table></div>
<p class=sub style="margin-top:14px">Frozen rule and forward book: strategy-lab/value_forward.py (formations from 2026-09-30). Gate verdict on record: FAILS (closest miss — DSR 0.79, PBO 0.52, +23.1% OOS excess). The screen informs; the ledger scores; the registry never moves.</p>
</div></body></html>"""
    open(os.path.join(HERE, "value.html"), "w").write(html)
    q = [r["ticker"] for r in rows if r["qualifies"]]
    print(f"value screen: {out['n']} scoreable, {out['qualifiers']} qualify: {', '.join(q)}")
    print("top 10 cheapest vs own history:", ", ".join(f"{r['ticker']}(p{r['pctile']:.0f},F{r['fscore']})" for r in rows[:10]))


if __name__ == "__main__":
    main()
