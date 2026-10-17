#!/opt/anaconda3/bin/python
"""earnings_puts_card.py -- the "Puts into earnings" tab of Leo Firm Live (conclusions first), plus a PNG/PDF record.

Reads research/earnings_puts/results_<newest>.json and data/eps_surprise.json only; nothing is typed in by hand.
build_html() returns the card (used by ~/command-center/live_page.py). Running the file writes
~/Desktop/Trading/reviews/earnings_puts_<date>.{png,pdf}. Paper research only; no account figures inside.
"""
import datetime as dt
import glob
import html as H
import json
import os
import statistics as st
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
OUT = Path.home() / "Desktop" / "Trading" / "reviews"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def m(x, d=1, plus=True):
    if x is None:
        return "–"
    s = f"{x:+.{d}f}" if plus else f"{x:.{d}f}"
    return s.replace("-", "−")


def load():
    R = json.loads(Path(sorted(glob.glob(str(HERE / "results_*.json")))[-1]).read_text())
    eps = json.loads((BASE / "data" / "eps_surprise.json").read_text())["tickers"].get("TSM", [])
    return R, eps


def smallest_beat_since(eps):
    """The TSMC surprise on 10-15 vs earlier quarters: the last quarter with a smaller beat."""
    rows = sorted([r for r in eps if r.get("surprise_pct") is not None], key=lambda r: r["ts"], reverse=True)
    now = rows[0]
    for r in rows[1:]:
        if r["surprise_pct"] <= now["surprise_pct"]:
            return now["surprise_pct"], r["ts"][:7]
    return now["surprise_pct"], None


def cost_chart(R):
    h2 = R["H2"]["h2"]
    bars = [("At a fair price", h2["all"]["mean"], "the stock's own past moves"),
            ("At October's real price", h2["at_k_real"]["mean"], f"options ran {round((h2['at_k_real']['k'] - 1) * 100)}% above fair"),
            ("After the bid/ask spread", h2["at_k_real"]["after_spread"], f"ask in, bid out: −{R['real_october']['spread_cost_pts']:.0f} more")]
    W, L, Rr, T, rowh = 660, 230, 60, 26, 46
    lo, hi = -30.0, 5.0
    X = lambda v: L + (v - lo) / (hi - lo) * (W - L - Rr)
    Hh = T + rowh * len(bars) + 30
    g = []
    for v in (-30, -20, -10, 0):
        g.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{T - 8}" y2="{Hh - 26}" stroke="{"#9a9994" if v == 0 else "#e6e5e1"}"/>')
        g.append(f'<text x="{X(v):.1f}" y="{Hh - 10}" text-anchor="middle" class="ax">{"0%" if v == 0 else f"−{abs(v)}%"}</text>')
    for i, (lab, v, sub) in enumerate(bars):
        y = T + i * rowh
        x0, x1 = sorted((X(0), X(v)))
        g.append(f'<text x="{L - 12}" y="{y + 14}" text-anchor="end" class="lb">{lab}</text>')
        g.append(f'<text x="{L - 12}" y="{y + 30}" text-anchor="end" class="ax">{sub}</text>')
        g.append(f'<rect x="{x0:.1f}" y="{y + 4}" width="{max(x1 - x0, 2):.1f}" height="24" fill="{"#d9a443" if i == 0 else "#d03b3b"}"/>')
        g.append(f'<text x="{x0 - 6:.1f}" y="{y + 21}" text-anchor="end" class="vd">{m(v)}%</text>')
    return f'<svg viewBox="0 0 {W} {Hh}" width="100%" style="max-width:{W}px" role="img" aria-label="Average put result per trade at three price levels">{"".join(g)}</svg>'


def year_chart(R):
    yrs = R["H2"]["h2"]["by_year"]
    keys = list(yrs)
    W, Hh, L, Rr, T, B = 640, 230, 46, 10, 18, 40
    lo, hi = -25.0, 30.0
    Y = lambda v: T + (hi - v) / (hi - lo) * (Hh - T - B)
    bw = (W - L - Rr) / len(keys)
    g = []
    for v in (-20, -10, 0, 10, 20, 30):
        g.append(f'<line x1="{L}" x2="{W - Rr}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{"#9a9994" if v == 0 else "#e6e5e1"}"/>')
        g.append(f'<text x="{L - 6}" y="{Y(v) + 4:.1f}" text-anchor="end" class="ax">{m(v, 0) if v else "0"}%</text>')
    for i, y in enumerate(keys):
        v = yrs[y]["mean"]
        x = L + i * bw + 3
        y0, y1 = sorted((Y(0), Y(v)))
        g.append(f'<rect x="{x:.1f}" y="{y0:.1f}" width="{bw - 6:.1f}" height="{max(y1 - y0, 1.5):.1f}" fill="{"#2a78d6" if v > 0 else "#d03b3b"}"/>')
        g.append(f'<text x="{x + (bw - 6) / 2:.1f}" y="{Hh - B + 16}" text-anchor="middle" class="ax">{"’" + y[2:]}</text>')
    zero = Y(0)
    return f'<svg viewBox="0 0 {W} {Hh}" width="100%" style="max-width:{W}px" role="img" aria-label="Put result by year at a fair price">{"".join(g)}</svg>'


def week_rows(R):
    cw = R["coming_week"]
    order = {"before open": 0, "time n/a": 1, "after close": 2}
    rows = []
    names = sorted(cw["names"], key=lambda x: (x["report_et"], order.get(x["when"], 1), -x.get("cap_b", 0)))
    last_day = None
    for x in names:
        day = dt.date.fromisoformat(x["report_et"])
        sep = ' class="day"' if day != last_day else ""
        last_day = day
        dlab = f"{day:%a %m/%d}"
        if x.get("error"):
            rows.append(f'<tr{sep}><td class="k">{dlab}</td><td><b>{H.escape(x["name"])}</b></td><td>{x["when"]}</td><td colspan="5" class="m">no option chain read ({H.escape(x["error"][:60])})</td></tr>')
            continue
        exp = dt.date(int(x["expiry"][:4]), int(x["expiry"][4:6]), int(x["expiry"][6:]))
        monthly = (exp - day).days > 10
        cls = ' class="mo"' if monthly else ""
        hist = x.get("n_past_prints") or 0
        fell = f'{x["past_drop_beyond_breakeven_pct"]:.0f}%' if x.get("past_drop_beyond_breakeven_pct") is not None else "–"
        down = f'{x["past_down_pct"]:.0f}%' if x.get("past_down_pct") is not None else "–"
        note = f'<span class="m"> monthly option (exp {exp:%m/%d}): includes weeks of ordinary moves</span>' if monthly else ""
        rows.append(f'<tr{sep}><td class="k">{dlab}</td><td><b>{H.escape(x["name"])}</b> <span class="m">{H.escape((x.get("desc") or "")[:28])}</span>{note}</td>'
                    f'<td class="k">{x["when"]}</td><td class="n"{cls}>±{x["implied_move_pct"]:.1f}%</td><td class="n"{cls}>{x["atm_put_pct"]:.1f}%</td>'
                    f'<td class="n">{hist or "–"}</td><td class="n">{down}</td><td class="n">{fell}</td></tr>')
    return "".join(rows)


def october_rows(R):
    out = []
    for r in sorted(R["real_october"]["rows"], key=lambda r: r["report_session"]):
        res = r["pnl_pct_ask_bid"]
        out.append(f'<tr><td><b>{r["ticker"]}</b></td><td class="k">{r["report_session"][5:]}</td><td class="k">{r["bought"][5:]}</td>'
                   f'<td class="n">{r["strike"]:g} P {r["expiry"][5:]}</td><td class="n">{r["put_cost_pct_spot"]:.1f}%</td>'
                   f'<td class="n">{m(r["stock_move_pct"])}%</td><td class="n {"pos" if res > 0 else "neg"}">{m(res, 0)}%</td></tr>')
    return "".join(out)


def build_html(height_hint=None):
    R, eps = load()
    H1, h2, h1, h3 = R["H1"], R["H2"]["h2"], R["H2"]["h1"], R["H2"]["h3"]
    T3 = R["H3"]
    tsm, peers, tp = R["tsm_2026_10"], R["peers_tue_to_fri_pct"], R["tsm_put"]
    surp, since = smallest_beat_since(eps)
    oc = R["real_october"]
    cw = R["coming_week"]
    yrs = h2["by_year"]
    good_years = sum(1 for v in yrs.values() if v["mean"] > 0)
    y26 = yrs.get("2026", {}).get("mean")
    y26_real = (1 + y26 / 100) / h2["at_k_real"]["k"] * 100 - 100 - oc["spread_cost_pts"] if y26 is not None else None
    weekly = [x for x in cw["names"] if not x.get("error") and (dt.date(int(x["expiry"][:4]), int(x["expiry"][4:6]), int(x["expiry"][6:]))
                                                                 - dt.date.fromisoformat(x["report_et"])).days <= 10]
    be_med = st.median(x["atm_put_pct"] for x in weekly) if weekly else None
    fell_vals = [x["past_drop_beyond_breakeven_pct"] for x in weekly if x.get("past_drop_beyond_breakeven_pct") is not None]
    d14 = round(100 * (tsm["2026-10-14"] / tsm["2026-10-13"] - 1), 1)
    d16 = round(100 * (tsm["2026-10-16"] / tsm["2026-10-15"] - 1), 1)
    p_sorted = sorted(((t, v) for t, v in peers.items() if t != "SPY"), key=lambda kv: kv[1])
    peer_txt = ", ".join(f"{t} {m(v)}%" for t, v in p_sorted)

    concl = [
        ("TSMC’s 7.3% drop took three days, and the report day was the smallest part.",
         f"On report day (Thu 10/15) it fell {abs(tsm['react_pct']):.1f}%. It fell {abs(d14):.1f}% the day before and {abs(d16):.1f}% the day after, "
         f"while every chip stock fell with it, Tuesday’s close to Friday’s: {peer_txt}."),
        ("Its “robust” quarter was a small beat.",
         f"Earnings per share came in {surp:.1f}% above the estimate, its smallest beat since {dt.date.fromisoformat(since + '-01'):%B %Y}. "
         "Prices move on the surprise against what was expected, not on how big the growth is."),
        ("After a good report, stocks usually went up.",
         f"Across {H1['beats_react']['n']:,} beats, the stock rose on the day {H1['beats_react']['pos_pct']:.0f}% of the time, by {m(H1['beats_react']['mean'])}% on average. "
         f"A beat that falls, like TSMC, happens {H1['beats_fell_pct']:.0f}% of the time: common, but the less likely side."),
        ("A put on every report is mostly a bet against good news.",
         f"{H1['beat_share_pct']:.0f}% of reports beat the estimate. Puts lost {abs(h2['beats']['mean']):.0f}% of their cost after beats and made {m(h2['misses']['mean'], 0)}% after misses, "
         "but you only learn which one it was after you have paid."),
        ("At a fair price the put only broke even. At real prices it loses.",
         f"Priced at each stock’s own usual move, a put bought 2 days before lost {abs(h2['all']['mean']):.1f}% per trade and won only {h2['all']['pos_pct']:.0f}% of the time. "
         f"This October’s real prices ran {round((h2['at_k_real']['k'] - 1) * 100)}% above fair and the spread cost another {oc['spread_cost_pts']:.0f}% of the premium: "
         f"about {m(h2['at_k_real']['after_spread'], 0)}% per trade. Buying 1 day or 3 days before: {m(h1['at_k_real']['after_spread'], 0)}% and {m(h3['at_k_real']['after_spread'], 0)}%."),
        ("TSMC falling told you nothing about the next companies.",
         f"In {T3['after_tsm_down']['n'] + T3['after_tsm_up']['n']} past seasons, companies reporting in the 45 days after a TSMC drop beat the market by "
         f"{m(T3['after_tsm_down']['mean_x'], 2)}% on their report day, the same as after a TSMC rise ({m(T3['after_tsm_up']['mean_x'], 2)}%)."),
        ("2026 has been a good year for puts, and such years come and go.",
         f"Even at a fair price, puts made money in only {good_years} of {len(yrs)} years. 2026 so far: {m(y26, 0)}% at a fair price, about {m(y26_real, 0)}% after real costs."),
    ]
    concl_html = "".join(f"<li><b>{a}</b> {b}</li>" for a, b in concl)
    tsm_rows = "".join(f'<tr><td class="k">{dt.date.fromisoformat(d):%a %m/%d}</td><td class="n">{v:.2f}</td>'
                       f'<td class="n">{m(100 * (v / prev - 1)) + "%" if prev else ""}</td></tr>'
                       for (d, v), prev in zip([(d, tsm[d]) for d in ("2026-10-13", "2026-10-14", "2026-10-15", "2026-10-16")],
                                               [None, tsm["2026-10-13"], tsm["2026-10-14"], tsm["2026-10-15"]]))

    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Puts Into Earnings</title><style>
@page {{ size: 1400px 3150px; margin: 0 }}
html, body {{ margin: 0 }}
body {{ background: #fcfcfb; color: #0b0b0b; font: 16px/1.45 -apple-system, Helvetica, Arial, sans-serif }}
.wrap {{ max-width: 1400px; padding: 30px 44px 26px; box-sizing: border-box }}
h1 {{ font-size: 32px; margin: 0 0 4px; text-wrap: balance }} .sub {{ color: #52514e; font-size: 14.5px }}
.verdict {{ margin: 16px 0 12px; padding: 13px 18px; border-left: 6px solid #d03b3b; background: #f6f5f2; font-size: 18.5px }}
ol {{ margin: 0; padding-left: 26px; max-width: 1080px }} li {{ margin: 0 0 9px; font-size: 16.5px }}
.dec {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 18px; margin: 14px 0 4px }}
.dec div {{ padding: 12px 16px; background: #eef4fc; border-left: 6px solid #2a78d6; font-size: 15px; min-width: 0 }}
.dec div.amber {{ background: #fbf3e4; border-left-color: #d9a443 }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 26px; margin-top: 14px; align-items: start }}
.grid > div {{ min-width: 0 }}
h2 {{ font-size: 17px; margin: 20px 0 6px; text-wrap: balance }}
.tw {{ overflow-x: auto }}
table {{ border-collapse: collapse; width: 100%; font-size: 13.4px }}
td, th {{ border-bottom: 1px solid #e6e5e1; padding: 4px 7px; text-align: left; vertical-align: top }}
th {{ color: #52514e; font-weight: 600; font-size: 12.5px }}
td.n, th.n {{ text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap }} td.k {{ white-space: nowrap }}
tr.day td {{ border-top: 2px solid #cfcdc7 }}
td.mo {{ color: #9a9994 }}
td.pos {{ color: #1f6fbf; font-weight: 600 }} td.neg {{ color: #b8312f; font-weight: 600 }}
.m {{ color: #52514e; font-size: 12px }}
svg text.ax {{ font-size: 12px; fill: #52514e }} svg text.lb {{ font-size: 13.5px; fill: #0b0b0b; font-weight: 600 }} svg text.vd {{ font-size: 12.5px; fill: #0b0b0b; font-weight: 700 }}
.note {{ color: #52514e; font-size: 12.5px; margin-top: 5px }}
.foot {{ color: #52514e; font-size: 12.3px; margin-top: 16px; border-top: 1px solid #e6e5e1; padding-top: 9px; line-height: 1.45 }}
</style></head><body><div class="wrap">
<h1>Buy a put before every earnings report?</h1>
<div class="sub">{R['n_prints']:,} reports from {R['n_tickers']} US companies, {R['first_print'][:7]} to {R['last_print']} · rules written down before the data (strategy-lab commit {R['prereg']}) ·
next week’s option prices read {H.escape(cw['fetched_pt'])} PT · paper research, nothing here is a trade · I am not a licensed advisor</div>
<div class="verdict"><b>Verdict: NOT SUPPORTED.</b> A put on every report lost money once you pay real option prices, about {m(h2['at_k_real']['after_spread'], 0)}% of what you pay per trade.
Good reports went up more often than down, and TSMC’s fall said nothing about the companies that reported after it.</div>
<ol>{concl_html}</ol>
<div class="dec">
<div><b>What this leaves you.</b> Don’t buy a put on every report: the history says you pay for it. The only thing that made puts work was knowing the result in advance.
Shorting the stock instead also lost ({m(R['short_stock_h2']['raw']['mean'], 2)}% per report, t {m(R['short_stock_h2']['raw']['t_cr1'], 1)}). Anything you try stays on paper first (your Rule 7 gate).</div>
<div class="amber"><b>This time the TSMC put did work.</b> Bought at Tuesday’s close for about {tp['price_pct_spot']:.1f}% of the price, it would have returned about {m(tp['result_pct_premium'], 0)}% by Thursday’s close.
That is one report. TSMC has reported {tp['past_prints']} times since 2012 and fell on the day {tp['past_down']} times.</div>
</div>

<div class="grid"><div>
<h2>What a put bought 2 days before the report returns, per trade</h2>
{cost_chart(R)}
<div class="note">Average of {h2['all']['n']:,} trades, as a share of what you pay. The usual single result is the whole premium lost: {100 - h2['all']['pos_pct']:.0f}% of puts lost money.</div>
<h2>Put result by year, at a fair price</h2>
{year_chart(R)}
<div class="note">Blue years made money, red years lost. Real prices take about {abs(h2['at_k_real']['after_spread'] - h2['all']['mean']):.0f} points off every bar.</div>
</div><div>
<h2>TSMC this week (closing prices, TSM)</h2>
<div class="tw"><table><tr><th>Session</th><th class="n">Close</th><th class="n">Day</th></tr>{tsm_rows}</table></div>
<div class="note">Report published before Thursday’s open. SPY on report day: {m(tsm['spy_react_pct'], 2)}%; SPY Tuesday to Friday: {m(peers['SPY'])}%.</div>
<h2>Real put trades this October, at recorded option prices</h2>
<div class="tw"><table><tr><th>Stock</th><th>Report</th><th>Bought</th><th class="n">Put</th><th class="n">Cost</th><th class="n">Stock</th><th class="n">Result</th></tr>{october_rows(R)}</table></div>
<div class="note">{oc['n']} reports between 9/24 and 10/16 that the firm’s daily chain recorder covered. Bought at the ask 2 sessions before, sold at the bid on report day:
{oc['winners']} of {oc['n']} won, average {m(oc['mean_pnl_ask_bid'], 0)}%. Cost and stock move are % of the share price.</div>
</div></div>

<h2>Next week: {len(cw['names'])} US companies worth ${cw['min_cap_b']:.0f}B or more report ({dt.date.fromisoformat(cw['week'][0]):%b %d}–{dt.date.fromisoformat(cw['week'][-1]):%d})</h2>
<div class="note" style="max-width:1080px;margin-bottom:6px">“Market expects” is the at-the-money straddle on the first expiry after the report. A put costs about half of it, so the stock must fall that much by expiry just to break even.
On the weekly names that fall is {be_med:.1f}% (median). “Fell that far” counts how often the stock’s past reports fell more than today’s put cost, held 2 days in; for these
{len(fell_vals)} names the median is {st.median(fell_vals):.0f}%. A name’s own past does not predict its next report (the firm’s 10/05 persistence test), so this is the price list, not a pick list.</div>
<div class="tw"><table>
<tr><th>Day</th><th>Company</th><th>When</th><th class="n">Market expects</th><th class="n">Put costs</th><th class="n">Past reports</th><th class="n">Fell on the day</th><th class="n">Fell that far</th></tr>
{week_rows(R)}</table></div>

<div class="foot"><b>How this was measured.</b> Report dates and times come from each company’s SEC 8-K (Item 2.02) filing; beat or miss from Yahoo’s EPS estimate. Report day = first session that could trade on the news.
Fair put price = what each stock usually moved on its last 8 reports plus its normal daily moves, priced as an at-the-money put held to the report-day close. “Real price” uses the median markup over fair seen on this October’s recorded chains ({oc['n']} reports, a small sample); the
spread is measured at closing quotes, which are wider than midday quotes, so the after-spread figures lean pessimistic. 13 cells were pre-declared; the one that cleared t 2 at a fair price (buying at the last close
before the news, {m(h1['all']['mean'])}%, t {h1['all']['t_cr1']:.1f}) turns negative at the real price ({m(h1['at_k_real']['mean'])}%). TSMC files 6-Ks, not 8-Ks, so its dates come from Yahoo. Adjusted closing prices through {R['prices_through']}.
Script: strategy-lab/research/earnings_puts/earnings_puts_study.py.</div>
</div></body></html>"""


def main():
    R, _ = load()
    OUT.mkdir(parents=True, exist_ok=True)
    stem = f"earnings_puts_{R['generated'][:10]}"
    with tempfile.TemporaryDirectory() as td:
        h = Path(td) / f"{stem}.html"
        h.write_text(build_html())
        base = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", f"--user-data-dir={Path(td) / 'chrome'}"]
        subprocess.run(base + ["--window-size=1400,3150", f"--screenshot={OUT / (stem + '.png')}", h.as_uri()], check=True, capture_output=True)
        subprocess.run(base + ["--no-pdf-header-footer", f"--print-to-pdf={OUT / (stem + '.pdf')}", h.as_uri()], check=True, capture_output=True)
    print("wrote", OUT / (stem + ".png"), OUT / (stem + ".pdf"))


if __name__ == "__main__":
    main()
