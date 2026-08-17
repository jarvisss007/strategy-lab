# Intraday Systematic Paper Desk — design (build only after sign-off)

Queued 2026-08-06 as a post-freeze Sunday design item; designed 2026-08-17 at the
lift. This is a DESIGN, not a build — its two open choices are Anupam's.

## Mandate (from the queue, unchanged)

Re-test intraday rule families **already convicted** by `intraday_discover` —
OR-breakout and VWAP-revert, both DEAD on replay — under Arena-style *forward*
discipline. Not new hope: the question is whether forward paper agrees with the
replay conviction, which validates the replay method itself. A conviction the
forward book confirms is worth more than either alone.

## Shape (mirrors the Arena so nothing new needs inventing)

- Frozen registered rules in REGISTRY.md before first trade: `OR_BREAK_30m`
  (long break of 30-min opening range high, stop at range low, flat by close)
  and `VWAP_REVERT` (fade >1.5% stretch from VWAP after 11:00 ET, flat by
  close). Exact params frozen at registration; the grid is NOT searched — these
  are the already-convicted configs, re-tested as-is.
- Entries/exits only at the two snapshots the desk already records (open+30m,
  close) — no continuous presence, no discretion, per the queue's own note that
  discretion is what the shop exists to measure away.
- Journals, day-clustered stats, roundtable paragraph, deflation gate at the
  same thresholds. One book file, one log file, both covered by a resolver
  check on day one (the ratchet requires it).

## Cost model — the decision that matters

Intraday round trips at 2×COST=20bps eat ~any daily-bar edge; at the 5-minute
holding scale the honest cost is nearer 4–8bps spread+slippage for the liquid
universe. **Choice A:** which cost number, fixed before first trade. A desk that
picks the cost after seeing results has pre-convicted itself.

## Data — the constraint that gates the build

The desk records open/close snapshots and the 0DTE chain recorder's sessions;
it does NOT store intraday bars for the equity universe. Options: (a) restrict
to SPY/QQQ + the ~10 names the intraday cache already covers, (b) extend the
recorder to pull 30-min bars for the 147 (new collector, new failure surface),
(c) don't build until the data exists for 60 sessions. **Choice B: a, b, or c.**

## Teacher's recommendation

(a) + the honest cost number, because it starts producing forward evidence this
month with zero new collection risk; extend to the full universe only if the
narrow book survives its own deflation gate. And the prediction, pre-registered
per house rule: both families confirm their replay conviction (p≈0.7) — the
build's value is validating the *method*, not resurrecting the rules.

*No code exists for this desk yet. It starts existing when Anupam picks A and B.*
