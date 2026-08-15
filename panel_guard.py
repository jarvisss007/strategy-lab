#!/usr/bin/env python3
"""panel_guard.py — refuse to record a session the market has not finished trading.

Found 2026-08-15 by the research sentinel, and it is the third variant of the same
bug: the weekly re-validation ran on a panel that had gained no new equity data.

WHY IT HAPPENED. refresh_all.sh fires its Monday branch at ~06:23 PT — about five
minutes BEFORE the 06:30 PT cash open. At that instant Yahoo already carries a bar
for the current day for anything trading overnight, and nothing for the equities.
The fetchers build their date axis as the UNION of every ticker's dates, so that
one futures-only timestamp became a full row: on 2026-08-10, close.csv gained a
2026-08-10 row in which exactly two of 144 columns (ES=F, NQ=F) had a value and the
other 142 were blank.

WHY IT MATTERS more than a blank row looks like it should. The equity panel
therefore still ended 2026-08-07 — precisely where the previous week left it — so
discover.py re-ran on the same data and reported "no drift". That verdict was
arithmetic, not evidence. A sentinel whose quiet weeks are indistinguishable from
its broken weeks is not measuring anything, which is the actual failure here.

WHAT THIS DOES. Trims trailing dates whose coverage across the fetched universe is
below MIN_COVERAGE. Tail only: interior sparse dates are real history (listings,
delistings, holidays that differ by venue) and are left exactly alone. Nothing is
lost by trimming — the next fetch picks the session up in full once it has closed.

Threshold and posture deliberately match fetch_data.py's existing 0.8 abort guard:
a fetch that is missing most of the universe is a timing or network artefact, not
new data.
"""
from __future__ import annotations

MIN_COVERAGE = 0.8


def trim_incomplete_tail(dates, panel, tickers, min_coverage=MIN_COVERAGE):
    """Drop trailing dates that most of `tickers` has not traded yet.

    dates    -- sorted list of date strings (the union axis)
    panel    -- {ticker: {date: value}}
    tickers  -- the tickers actually written as columns

    Returns (kept_dates, dropped) where `dropped` is a list of
    (date, n_present, n_tickers) for logging. Only the tail is examined.
    """
    if not dates or not tickers:
        return dates, []
    n = len(tickers)
    kept = list(dates)
    dropped = []
    while kept:
        day = kept[-1]
        present = sum(1 for s in tickers if panel.get(s, {}).get(day) is not None)
        if present >= min_coverage * n:
            break
        dropped.append((day, present, n))
        kept.pop()
    dropped.reverse()
    return kept, dropped


def report(dropped, min_coverage=MIN_COVERAGE):
    """One log line per trimmed bar, so a silent trim never happens."""
    for day, present, n in dropped:
        print(f"  INCOMPLETE BAR dropped: {day} — only {present}/{n} tickers traded "
              f"(< {min_coverage:.0%}); session not finished at fetch time")
