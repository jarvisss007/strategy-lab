#!/opt/anaconda3/bin/python
"""fetch_week_implied.py - every US reporter >= $40B for the coming week, with the options-implied earnings move.

Same feed and same chain reader as Desktop/Trading/tradingview/week_ahead.py (Hanuman, COURT-004); only the cap floor
and name count differ. Read-only TradingView market data. Writes research/earnings_puts/week_implied_<monday>.json.
"""
import datetime as dt, json, os, sys
sys.path.insert(0, os.path.expanduser('~/Desktop/Trading/tradingview'))
sys.path.insert(0, os.path.expanduser('~/bin/tv'))
import week_ahead as W
import tv_feeds as F

MIN_CAP, MAX_NAMES = 40e9, 60
HERE = os.path.dirname(os.path.abspath(__file__))
now = dt.datetime.now(W.PT)
days, _ = W.week_sessions(now)
earn = F.earnings(days[0].isoformat(), days[-1].isoformat(), MIN_CAP)
rows, n = [], 1
for r in sorted(earn, key=lambda x: -(x.get('market_cap_basic') or 0))[:MAX_NAMES]:
    ts = r.get('earnings_release_next_date')
    if not ts:
        continue
    rep = dt.datetime.fromtimestamp(ts, W.UTC).astimezone(W.ET)
    when = {1: 'after close', -1: 'before open'}.get(r.get('earnings_release_next_time'), 'time n/a')
    row = {'name': r['name'], 'desc': r.get('description'), 'symbol': r['symbol'], 'cap_b': round((r.get('market_cap_basic') or 0) / 1e9),
           'report_et': rep.strftime('%Y-%m-%d'), 'when': when, 'close': r.get('close')}
    try:
        exps = [int(x['expiration']) for x in F.expirations(r['symbol'], r['name'])]; n += 1
        rd = rep.date()
        e = next(x for x in exps if (W._exp_date(x) >= rd if when == 'before open' else W._exp_date(x) > rd))
        row.update(W.read_chain(F.options(r['symbol'], r['name'], e), e)); n += 1
    except Exception as ex:
        row['error'] = f'{type(ex).__name__}: {str(ex)[:120]}'
    rows.append(row)
    print(row['name'], row.get('report_et'), row.get('move_pct'), row.get('error', ''), flush=True)
out = {'fetched_pt': now.strftime('%Y-%m-%d %H:%M'), 'week': [d.isoformat() for d in days], 'min_cap': MIN_CAP,
       'n_reporters_in_feed': len(earn), 'earnings': rows, 'requests': n}
p = os.path.join(HERE, f'week_implied_{days[0].isoformat()}.json')
json.dump(out, open(p + '.tmp', 'w'), indent=1, default=str); os.replace(p + '.tmp', p)
print('wrote', p, len(rows), 'names', n, 'requests')
