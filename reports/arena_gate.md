# ARENA → DEFLATION GATE

_198 sessions × 12 rules · 8961 backtest trades · columns are vs-SPY excess, not raw return._

The Arena dashboard has said *CANDIDATE — send to the deflation gate* since
2026-07-25. Nobody sent them: `arena.py` never imported `overfit.py`. This is that run.

## The gate's verdict on the selected best rule

```
  ============================================================
  Backtest overfitting report — 12 strategies, 198 obs
  ------------------------------------------------------------
  Best strategy (#3) Sharpe (ann.):   1.36
  Probabilistic Sharpe (vs 0):                0.887
  Deflated Sharpe (vs best-of-N benchmark):   0.233   (benchmark 2.18 ann.)
  Prob. of Backtest Overfitting (PBO):        0.474   (>0.5 is bad)
  Prob. OOS loss when selecting IS-best:      0.624
  IS→OOS performance degradation (slope):     -0.568   (negative ⇒ overfitting)
  Min backtest length for this many trials:   1.5 years
  ------------------------------------------------------------
  VERDICT: suspect: fails one of {deflated significance, low PBO} — treat as unproven
  ============================================================
```

## Each rule standing alone

| rule | backtest n | backtest vs-SPY | backtest t | days fired | ann. Sharpe (excess) | PSR | min track (days) |
|---|---|---|---|---|---|---|---|
| FRESH_HIGH | 574 | +104 bps | +2.92 | 153 | +1.36 | 0.885 | 369 |
| STORM_DIP | 602 | +136 bps | +6.16 | 40 | +0.77 | 0.751 | 1161 |
| DOUBLE_DIP | 1221 | +55 bps | +3.75 | 172 | +0.44 | 0.651 | 3516 |
| PANIC_LITE | 2780 | +36 bps | +4.37 | 196 | -0.07 | 0.475 | — |
| PANIC_BOUNCE | 1433 | +36 bps | +2.73 | 171 | -0.07 | 0.474 | — |
| PULLBACK_50 | 243 | +43 bps | +1.45 | 48 | -0.13 | 0.454 | — |
| SHORT_EXT | 258 | -57 bps | -0.68 | 98 | -0.69 | 0.271 | — |
| DEEP_DIP | 143 | -8 bps | +0.88 | 82 | -0.99 | 0.191 | — |
| TREND_RIDER | 100 | -190 bps | -0.66 | 41 | -1.51 | 0.092 | — |
| BOLL_SNAP | 745 | +52 bps | +4.27 | 160 | -1.82 | 0.055 | — |
| REVERSAL_3 | 252 | -45 bps | -1.13 | 45 | -2.55 | 0.013 | — |
| RSI2_DIP | 610 | -103 bps | -3.14 | 50 | -2.87 | 0.006 | — |

**Reading it.** PSR is the probability the rule's excess Sharpe is truly above zero
given its own skew/kurtosis and length — *before* any adjustment for the fact that 12
rules were tried. The gate's verdict above is what remains *after* that adjustment.
The distance between the two is the selection effect, and it is the whole reason this
file exists.

**Caveats that do not go away with a better number:** one year of history on a
119-name universe that is today's survivors; long-only rules in a bull tape; and the
15-year survey already convicted the short-term-reversal family (OOS −0.74). A rule
passing here has cleared one bar, not earned a trade.