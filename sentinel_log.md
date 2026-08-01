# Research Sentinel Log

date · registry-clean? · drift? · zdte n/60 · crypto days/skill · insider events

2026-07-25 · clean (6/6 families match REGISTRY.md) · no drift (all verdicts match 2026-07-11 frozen table; discoveries.csv row identical to 2026-07-18 run) · zdte 7/60 (first log, no prior baseline) · crypto 21 days, skill -0.031, edge_found=false (first log, no prior baseline) · insider 392 events (first log, no prior baseline)

2026-07-26 · clean (6/6 families match REGISTRY.md) · no drift (all 6 verdicts identical to the 2026-07-11 frozen table; 0 survivors, best DSR still t5 = 1.0 / PBO 0.01) · zdte 7/60 (+0) · crypto 22 days, skill -0.031, edge_found=false (+1 day) · insider 392 events (+0)

2026-08-01 · clean (6/6 families match REGISTRY.md) · **DRIFT: Price-action value-area fade real-but-loses → DEAD** (best net 0.08 → −0.04, PBO 0.05 → 0.43); Options-expiry best config flipped pre-opex → post-opex, PBO 0.54 → 0.69 · **PIPELINE FIX: open/close/volume.csv were frozen at 2026-07-07** — fetch_ohlc.py + fetch_volume.py are absent from refresh_all.sh (its Monday branch runs only fetch_data.py, which writes prices.csv, a different file). Every "no drift" since 2026-07-11 was arithmetic on a static panel, not evidence. Panels refreshed manually this run → 2026-07-31; discoveries.csv therefore holds TWO 2026-08-01 blocks (first = stale panel, second = refreshed; use the second). Rolling 15y window means the refresh added ~17 days and dropped ~16 off the front — not purely additive · zdte 12/60 (+5) · crypto 28 CSV days (+6), skill −0.031, edge_found=false (learned_weights.json itself stale, last built from data through 2026-07-25) · insider 400 events (+8)
