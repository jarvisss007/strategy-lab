# PRE-REGISTRATION — sector-event follow-through study

**Written 2026-08-10, BEFORE any result was computed.** Anupam's hypothesis, from watching
cybersecurity names move together today (PANW +5.8%, CRWD +5.0%, ZS +4.7%, S +3.9%,
NET +3.4%, FTNT +2.9%): *an event hits a sector, every name in it moves, and that
follow-through is tradeable — across all sectors, not just cyber.*

This file exists so the thesis cannot be edited after seeing the answer. Rule 1 of the
desk: pre-register or it didn't happen.

## The question
After a **coordinated sector move**, does the sector basket keep going, relative to SPY?

## Definitions, fixed now

- **Universe:** the 147-name watchlist, sector tags from `stock-radar/watchlist.csv`,
  adjusted closes from `strategy-lab/data/prices.csv` (15y). Sectors with **≥5 priced
  names** only.
- **EVENT DAY:** a (sector, date) where **≥60% of that sector's priced names close up
  ≥2%** on the same day. That is the machine version of "an event hit this sector."
- **Response:** equal-weight sector basket return over **+1d, +5d, +21d** from the event
  close (entry at the event close — no lookahead; the event is known by then).
- **Benchmark:** SPY over the **identical window**, via `bench.py`'s rule. Never raw return.
- **Effective n:** **distinct event days**, never event-rows. Two sectors firing on the
  same date is ONE market observation and is reported as such.

## Stated falsifier — decided now, not after

The idea is **dead as a standalone signal** if, at the 5-day horizon:
- mean excess vs SPY ≤ 0, **or**
- the day-clustered t-stat < 2.0, **or**
- fewer than 30 distinct event days exist to test on.

Any of those three and the honest verdict is "no edge," and it goes in the ledger as such.

## Priors, written down before running

The desk's own record says to expect nothing. Every momentum/drift family tested here has
died after costs (strategy-lab's 8-family survey, the Arena's 12 rules at DSR 0.233, r17,
DC-ML). Post-event drift is among the most-documented anomalies in the literature *and*
among the most decayed post-publication. A positive result here should be treated as
suspect until it survives a deflation gate, not as a discovery.

## Known limitation, stated up front

**The universe has no CYBERSECURITY sector.** PANW, CRWD, ZS, S, FTNT, NET, OKTA are
tagged TECHNOLOGY (30 names). So today's actual move — the thing that prompted this — is
NOT detectable as a sector event by this test's own definition. Whatever the study finds
about TECHNOLOGY says little about a 7-name cyber complex inside it. Fixing that means
tagging sub-industries, which is a data change and is not being made mid-study.
