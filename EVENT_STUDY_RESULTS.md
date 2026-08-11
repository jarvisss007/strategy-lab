# RESULTS — sector-event follow-through

*Run 2026-08-10 against `EVENT_STUDY_PREREG.md`, written before any number was computed.
15y, 3,776 sessions, 146 priced names, 7 sectors with ≥5 names.*

## The pre-registered test FAILED

**1,019 sector-events over 565 distinct event days** — a large sample, well past the
30-day floor. Entry at the event close, equal-weight sector basket, benchmarked against
SPY over the identical window.

| horizon | mean excess vs SPY | median | >0 | day-clustered t |
|---|---|---|---|---|
| 1d | +0.09pp | +0.01pp | 50% | 1.23 |
| **5d** | **+0.21pp** | +0.03pp | 51% | **1.84** |
| 21d | +2.17pp | +0.83pp | 55% | 4.88 |

The falsifier fixed in advance was: dead if the 5-day day-clustered t < 2.0.
**t = 1.84. The hypothesis as stated is dead.**

## The control is what actually settles it

Compared against the same measurement on **every third day with no event filter**
(8,281 sector-days):

| horizon | event days | ALL days (control) | what the event adds |
|---|---|---|---|
| 1d | +0.09pp | +0.03pp | +0.06pp |
| **5d** | **+0.22pp** | **+0.22pp** | **0.00pp** |
| 21d | +2.17pp | +1.01pp | +1.16pp |

At five days the event adds **exactly nothing**. The entire "edge" is the universe: a
basket of names that are worth watching in 2026 beats SPY on any random day of the last
fifteen years, because we picked them knowing they survived.

That survivorship is measurable, and it is large:

| sector | 21d excess vs SPY on ALL days |
|---|---|
| EMERGING TECH | **+2.32pp** |
| CHIPS/SEMICONDUCTORS | +1.52pp |
| TECHNOLOGY | +1.13pp |
| ENERGY | +0.63pp |
| FINANCIALS | +0.61pp |
| INDUSTRIALS | +0.54pp |
| HEALTHCARE | +0.38pp |

Emerging tech earns +2.32pp per 21 days *for existing in today's watchlist*. Any study on
this universe that does not subtract that is measuring hindsight.

## What survives — exploratory, NOT pre-registered

Measured **above each sector's own baseline**, so survivorship is removed:

> **21-day effect: +1.16pp, day-clustered t = 2.28, over 565 distinct event days.**

That is a real residual and it is honestly reported — but the 21-day horizon was **not**
the pre-registered test. Promoting it now is the multiple-testing sin the desk keeps
convicting itself of. It is a hypothesis for a NEW pre-registration, and it must clear the
deflation gate before the word "edge" is used. Not a finding. A candidate for a finding.

Note also the shape: nothing at 1 day, nothing at 5, something at 21. That is not what a
tradeable event reaction looks like — a real catalyst effect shows up fast and decays.
Something that only appears at three weeks is more likely slow-moving sector drift that
happens to follow a strong day.

## The limitation that matters most

**The universe has no cybersecurity sector.** PANW, CRWD, ZS, S, FTNT, NET and OKTA are
all tagged TECHNOLOGY (28 names). So today's actual move — the reason this study exists —
is invisible to it. A 7-name complex ripping +3–6% cannot trigger a "≥60% of 28 names"
test. Whatever TECHNOLOGY does says nothing about cyber.

Fixing that is a data change, not an analysis change: sub-industry tags on the watchlist.
Until it exists, this desk cannot detect the kind of event Anupam actually observed.

## Verdict

Sector-event follow-through is **not tradeable at 1–5 days** — the horizon a person would
actually trade. The 21-day residual is worth one properly registered test, and the
sub-industry tagging is worth doing regardless, because without it the desk is blind to
exactly the events that prompted the question.
