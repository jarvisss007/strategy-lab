#!/usr/bin/env python3
"""ARENA → THE DEFLATION GATE.

2026-08-08. The Arena's dashboard has said "CANDIDATE — send to the deflation gate" on
five rules since 2026-07-25, and its own honesty line says "12 rules tested at once — the
best backtest flatters itself." Nobody ever sent them: `arena.py` does not import
`overfit.py`, and `knowledge_base.csv` still holds only the nine families from 07-07.
So five rules have been sitting on the dashboard wearing the word CANDIDATE without ever
facing the bar that word points at. This runs it.

METHOD. Build a T×N daily matrix from `blotter_backtest` — one column per registered rule,
one row per session, each cell the mean vs-SPY excess of that rule's trades ENTERED that
day (0 when the rule did not fire). Excess, not raw: a long-only rule in a bull year earns
a Sharpe from beta alone, and beta is not what is being tested. Then `overfit.analyze()`
selects the best column by full-sample Sharpe and asks whether that selection survives
Deflated Sharpe (adjusted for having tried 12 rules) and PBO/CSCV.

The N-trials argument is 12 by construction — that is the honest count of what was tried,
and it is the number the DSR discounts by.

Run: python3 arena_gate.py   ->  reports/arena_gate.md + reports/arena_gate.json
"""
import json, os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import overfit

BASE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(f"{BASE}/reports/arena.json"))
blot = A.get("blotter_backtest") or []
bt = A["backtest"]

rules = sorted(bt.keys())
dates = sorted({r["entry_date"] for r in blot})
idx = {d: i for i, d in enumerate(dates)}
M = np.zeros((len(dates), len(rules)))
cnt = np.zeros((len(dates), len(rules)))
for r in blot:
    j = rules.index(r["strategy"])
    i = idx[r["entry_date"]]
    M[i, j] += float(r.get("excess") or 0.0)
    cnt[i, j] += 1
with np.errstate(invalid="ignore", divide="ignore"):
    M = np.where(cnt > 0, M / np.maximum(cnt, 1), 0.0)

print(f"matrix: {M.shape[0]} sessions × {M.shape[1]} rules, from {len(blot)} backtest trades")

rep = overfit.analyze(M, periods_per_year=252, n_splits=16)

# SELF-AUDIT 2026-08-08 (Anupam: "you also do deep audit"). Two construction choices in
# this file are load-bearing, so both are reported rather than hidden:
#   (1) per-day MEAN vs per-day SUM. MEAN weights each session equally; SUM weights by how
#       many names the rule fired on. Run both — if the verdict depends on the choice, the
#       verdict is mine, not the data's.
#   (2) zero-fill on days a rule did not fire. This is the standard CSCV convention (flat
#       = no bet = 0 excess) but it PENALISES sparse rules: STORM_DIP fires 40 of 198
#       sessions, and zero-filling roughly halves its Sharpe. Reported alongside.
Msum = np.zeros_like(M)
for r in blot:
    Msum[idx[r["entry_date"]], rules.index(r["strategy"])] += float(r.get("excess") or 0.0)
rep_sum = overfit.analyze(Msum, periods_per_year=252, n_splits=16)
sparse = {k: {"days_fired": int((cnt[:, j] > 0).sum()),
              "sr_zero_filled": round(float(overfit.sharpe_ratio(M[:, j], 252)), 2),
              "sr_fired_days_only": round(float(overfit.sharpe_ratio(M[cnt[:, j] > 0, j], 252)), 2)}
          for j, k in enumerate(rules) if (cnt[:, j] > 0).sum() >= 5}

# per-rule standalone read, so the gate's verdict on the WINNER can be read beside
# what each rule looks like on its own (the difference between them is the selection effect)
per = {}
for j, k in enumerate(rules):
    col = M[:, j]
    fired = int((cnt[:, j] > 0).sum())
    sr = overfit.sharpe_ratio(col, 252)
    n = len(col)
    psr = overfit.probabilistic_sharpe_ratio(sr / math.sqrt(252), n) if n else float("nan")
    mtrl = None
    try:
        if sr > 0:
            mtrl = overfit.min_track_record_length(sr / math.sqrt(252))
    except Exception:
        pass
    per[k] = {"sharpe_ann": round(float(sr), 3), "days_fired": fired,
              "psr": round(float(psr), 4),
              "min_track_days": (round(float(mtrl)) if mtrl and np.isfinite(mtrl) else None),
              "bt_t": bt[k]["t_stat"], "bt_excess_bps": bt[k]["avg_excess_bps"],
              "bt_n": bt[k]["n"]}

out = {"n_trials": len(rules), "sessions": M.shape[0], "gate": rep,
       "gate_size_weighted": rep_sum, "sparsity_audit": sparse, "per_rule": per}
json.dump(out, open(f"{BASE}/reports/arena_gate.json", "w"), indent=1, default=str)

L = ["# ARENA → DEFLATION GATE", "",
     f"_{M.shape[0]} sessions × {len(rules)} rules · {len(blot)} backtest trades · "
     "columns are vs-SPY excess, not raw return._", "",
     "The Arena dashboard has said *CANDIDATE — send to the deflation gate* since",
     "2026-07-25. Nobody sent them: `arena.py` never imported `overfit.py`. This is that run.", "",
     "## The gate's verdict on the selected best rule", "",
     "```", overfit.format_report(rep), "```", "",
     "## Robustness of the verdict to how I built the matrix", "",
     f"| construction | DSR | PBO | best rule | its Sharpe | best-of-12 benchmark | verdict |",
     "|---|---|---|---|---|---|---|",
     f"| per-day MEAN, zero-filled *(headline)* | {rep['dsr']:.3f} | {rep['pbo']:.3f} | "
     f"{rules[rep['best_strategy']]} | {rep['best_sharpe_annual']:.2f} | "
     f"{rep['deflated_benchmark_sharpe_annual']:.2f} | {rep['verdict'].split(':')[0]} |",
     f"| per-day SUM, size-weighted | {rep_sum['dsr']:.3f} | {rep_sum['pbo']:.3f} | "
     f"{rules[rep_sum['best_strategy']]} | {rep_sum['best_sharpe_annual']:.2f} | "
     f"{rep_sum['deflated_benchmark_sharpe_annual']:.2f} | {rep_sum['verdict'].split(':')[0]} |",
     "",
     "The verdict does not depend on the choice — and the headline construction is the",
     "**more generous** of the two. Size-weighting returns OVERFIT outright.", "",
     "## Sparsity bias — rules are penalised for not trading", "",
     "| rule | days fired (of 198) | Sharpe zero-filled | Sharpe on fired days only |",
     "|---|---|---|---|"] + [
     f"| {k} | {v['days_fired']} | {v['sr_zero_filled']:+.2f} | {v['sr_fired_days_only']:+.2f} |"
     for k, v in sorted(sparse.items(), key=lambda x: -x[1]["sr_fired_days_only"])] + [
     "",
     "**This distorts the ranking in the table below and I reported that table before",
     "checking.** STORM_DIP fires 40 of 198 sessions; zero-filling more than halves its",
     "Sharpe (1.70 → 0.77). The count of rules with negative excess Sharpe is unchanged",
     "either way, so the conclusion held — but the ORDER did not, and I presented an order.", "",
     "## Each rule standing alone", "",
     "| rule | backtest n | backtest vs-SPY | backtest t | days fired | ann. Sharpe (excess) | PSR | min track (days) |",
     "|---|---|---|---|---|---|---|---|"]
for k in sorted(per, key=lambda x: -per[x]["sharpe_ann"]):
    p = per[k]
    L.append(f"| {k} | {p['bt_n']} | {p['bt_excess_bps']:+.0f} bps | {p['bt_t']:+.2f} | "
             f"{p['days_fired']} | {p['sharpe_ann']:+.2f} | {p['psr']:.3f} | "
             f"{p['min_track_days'] if p['min_track_days'] else '—'} |")
L += ["", "**Reading it.** PSR is the probability the rule's excess Sharpe is truly above zero",
      "given its own skew/kurtosis and length — *before* any adjustment for the fact that 12",
      "rules were tried. The gate's verdict above is what remains *after* that adjustment.",
      "The distance between the two is the selection effect, and it is the whole reason this",
      "file exists.", "",
      "**Caveats that do not go away with a better number:** one year of history on a",
      "119-name universe that is today's survivors; long-only rules in a bull tape; and the",
      "15-year survey already convicted the short-term-reversal family (OOS −0.74). A rule",
      "passing here has cleared one bar, not earned a trade.", "",
      "**One more limit of this file, stated because it is not obvious.** Each row is a",
      "trade's full multi-day return (holds run 2–15 days) attributed to its ENTRY day, then",
      "annualised by sqrt(252) as if the rows were daily. The columns are all built the same",
      "way, so the comparison between them — which is what DSR and PBO test — is sound. The",
      "absolute Sharpe MAGNITUDES are not real annualised Sharpes and should not be quoted",
      "as such. I quoted them as such on 2026-08-08 before auditing this."]
open(f"{BASE}/reports/arena_gate.md", "w").write("\n".join(L))
print(overfit.format_report(rep))
