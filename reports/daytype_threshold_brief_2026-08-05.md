# Day-type TRADEABLE_PATH_PCT bar — design sensitivity brief (2026-08-05)

**Analysis only. No live threshold, label, or strategy file was changed.** Question for
Sunday review: the 12% absolute bar (`day_type.TRADEABLE_PATH_PCT`, consumed by
`universe_daytype.py`) was calibrated on SNDK (hand-sheet legend "Total Path >= $80
tradeable" when SNDK traded ~$500). Under it ~45% of the universe shows
`tradeable_pct = 0.0` and 80/108 label QUIET. The 2026-08-05 audit (commit 8f83d5e)
confirmed the *measurement* is real; this brief tests the *bar design*.

## Method

Same data path as the live builder: `day_type.intraday()` (Yahoo 15m), fetched fresh
2026-08-05 at `range=60d` per name. Last 21 sessions = evaluation window (matches the
builder's ~1mo); the ~39 sessions before them = each name's own trailing baseline
(median daily zigzag path%). Partial session 2026-08-05 dropped. Sanity: fresh numbers
reproduce the stored CSV (SNDK avg path 16.2 vs 16.6 stored, tradeable 66.7 both;
HOOD 6.8/0.0 both).

**Coverage, honestly:** 101 of 121 watchlist names profiled. 12 are the builder's usual
intraday failures. **7 more (MSFT, META, BABA, AAPL, NOC, HII, TXT) dropped because they
have too many sessions with *zero* 1.5% zigzag swings** to meet my 30-session minimum —
i.e. they are the quietest names, and every one would sit at 0.0 under any absolute bar
below. Zero-counts here are therefore a slight *undercount* vs the full universe.
CBRS: Yahoo HTTP 422, not filled.

## Sensitivity table — distribution of tradeable_pct across 101 names

| Design | Names at 0.0 | Median | Mean | p25 | p75 | Max | Names >= 25% | SNDK |
|---|---|---|---|---|---|---|---|---|
| Absolute 8% | 14 | 19.0 | 28.4 | 4.8 | 47.6 | 95.2 | 45 | 95.2 |
| Absolute 10% | 29 | 9.5 | 19.0 | 0.0 | 33.3 | 85.7 | 30 | 81.0 |
| **Absolute 12% (current)** | **43** | **4.8** | **11.1** | **0.0** | **14.3** | **81.0** | **15** | **66.7** |
| Absolute 15% | 61 | 0.0 | 6.0 | 0.0 | 9.5 | 61.9 | 6 | 57.1 |
| Relative 1.5x own median | 12 | 19.0 | 21.9 | 9.5 | 38.1 | 57.1 | 39 | 42.9 |
| Relative 2.0x own median | 25 | 4.8 | 9.6 | 4.8 | 14.3 | 38.1 | 8 | 23.8 |
| Relative 2.5x own median | 55 | 0.0 | 4.0 | 0.0 | 4.8 | 23.8 | 0 | 9.5 |

## Labels

The QUIET/TRENDY/CHOPPY/BALANCED label does **not** derive from the tradeable bar. It
derives from a separate absolute floor in `universe_daytype.py` (QUIET if avg path < 8%,
else efficiency splits). So changing TRADEABLE_PATH_PCT alone changes **zero** labels:
fresh label counts are QUIET 73 / BALANCED 24 / CHOPPY 3 / TRENDY 1 at every absolute
bar (stored full-universe equivalent: 80/24/3/1). Two scenarios if the floor moved too:

| Scenario | QUIET | BALANCED | CHOPPY | TRENDY |
|---|---|---|---|---|
| Floor scales with bar: 8% bar (floor 5.3%) | 47 | 36 | 3 | 15 |
| 10% bar (floor 6.7%) | 59 | 31 | 3 | 8 |
| 12% bar (floor 8.0%, current) | 73 | 24 | 3 | 1 |
| 15% bar (floor 10%) | 90 | 8 | 3 | 0 |
| Relative floor (QUIET if avg path < 1x own median) | 37 | 20 | 3 | **41** |

The last row is a warning, not an option: 41 "TRENDY" names appear because low-vol names
register few zigzag swings, so their efficiency is inflated — exactly the sparse-swing
artifact the 8% floor exists to suppress (per the comment in `universe_daytype.py`).
A fully relative label rule resurrects that artifact.

## Honest tradeoffs

**What a relative bar gains.** Each name is judged against its own character. The
absolute 12% bar makes `tradeable_pct` a volatility ranking wearing a different name —
43 names pinned at 0.0 carry no information about *which of their days* differ. At
K=1.5x own median, only 12 names sit at 0.0 and the column starts answering "is today
unusual *for this name*," which is the question a day-type framework is supposed to ask.
Note also the ceiling: even SNDK clears 2.0x its own median only 23.8% of days —
"unusual" is rare for everyone by construction, which is the point.

**What it costs.** A relative-"tradeable" day on a low-vol name may not clear round-trip
costs. The three lowest-vol names profiled (trailing median daily path): NFLX 1.8%,
EBAY 2.3%, NVDA 2.3%. A K=2.0 "tradeable" day on NFLX is a 3.6% *total zigzag path* —
on a $10,000 position the entire path is $360, and an optimistic 25% capture across
several round trips is ~$90 gross **for the whole day**, before spread, slippage, and
sizing reality on an 8GB-account-scale book. The same 25% capture on a 12%-path day is
~$300. To be precise about provenance: the code docstring justifies 12% as
"enough opportunity" (SNDK-calibrated, made scale-free vs *price*, not vs *volatility*);
the cost-floor argument is the implicit economics, not an explicit code comment.

## Recommendation *(recommendation only — decision is Anupam's)*

**Add, don't replace: keep one absolute opportunity floor and add a relative column.**
Concretely: (1) keep an absolute bar as the cost/opportunity floor but consider 8-10%
rather than the SNDK-calibrated 12% (at 8% the floor still reflects real dollar
opportunity while cutting dead-zero names from 43 to 14); (2) add a second column,
`unusual_pct` at K=1.5x own trailing 60d median, so the dashboard separates "moves a lot"
from "moving more than usual today"; (3) leave the QUIET label floor absolute — the
relative-label scenario above shows it would manufacture 41 fake TRENDY names out of the
sparse-swing artifact. A day worth trading should arguably clear **both** bars; that
hybrid wasn't tabulated per-day here and should be computed before any live change.

---
*Raw sensitivity data: scratchpad run of 2026-08-05 (fetch script + JSON, not committed).
Live files read but untouched: `day_type.py`, `universe_daytype.py`,
`reports/universe_daytype.{csv,json}`.*
