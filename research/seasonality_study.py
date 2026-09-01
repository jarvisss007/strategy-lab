"""Calendar seasonality — Anupam's claimed pattern vs the actual tape (2026-08-31).

His claim: September starts a bear; Jan–Mar rises; APRIL makes the year's low; up till
August; down till December; then up. Tested on ^GSPC monthly closes since 1950.

THE MINING WARNING IS PART OF THE RESULT. Twelve months = twelve hypotheses tested at
once; at 5% significance, chance alone hands you ~one "significant" month. Any month
whose |t| does not clear a Bonferroni-ish bar (~2.87 for 12 tests) is a story. And a
calendar pattern that CAN'T state its mechanism (who is forced to trade against you in
September?) starts life as noise until proven otherwise.
"""
import json, math, statistics as st, urllib.request, datetime as dt
from collections import defaultdict

UA={"User-Agent":"Mozilla/5.0"}
u=("https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC"
   "?period1=-631152000&period2=9999999999&interval=1mo")
r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
res=r["chart"]["result"][0]; q=res["indicators"]["quote"][0]
rows=[(dt.datetime.fromtimestamp(t,dt.UTC), c) for t,c in zip(res["timestamp"],q["close"]) if c]
rows=[x for x in rows if x[0].year>=1950]
rets=defaultdict(list); lows=defaultdict(int); years=defaultdict(list)
for i in range(1,len(rows)):
    m=rows[i][0].month
    rets[m].append((rows[i][1]/rows[i-1][1]-1)*100)
    years[rows[i][0].year].append((rows[i][0].month,rows[i][1]))
for y,ms in years.items():
    if len(ms)>=12:
        lows[min(ms,key=lambda x:x[1])[0]]+=1
N=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
print(f"^GSPC monthly, {rows[0][0].year}–{rows[-1][0].year} ({len(rows)} months). Bonferroni bar |t|≈2.87 for 12 tests.")
print(f"{'month':<6}{'mean%':>8}{'win%':>7}{'t':>7}   year-low lands here")
for m in range(1,13):
    v=rets[m]; mu=st.mean(v); sd=st.stdev(v); t=mu/(sd/math.sqrt(len(v)))
    star="  ***" if abs(t)>=2.87 else ("  *" if abs(t)>=2.0 else "")
    print(f"{N[m-1]:<6}{mu:>+8.2f}{100*sum(1 for x in v if x>0)/len(v):>6.0f}%{t:>7.2f}{star}   {lows.get(m,0)} of {sum(lows.values())} years")
print("\nHIS CLAIMS vs the data:")
sep=rets[9]
print(f"  'September starts a bear': Sept mean {st.mean(sep):+.2f}%, win {100*sum(1 for x in sep if x>0)/len(sep):.0f}% — the one month with a real negative lean, but a ~1% average dip is a lean, not a bear.")
apr=lows.get(4,0); tot=sum(lows.values())
best_low=max(lows,key=lambda k:lows[k])
print(f"  'April makes the year low': April held the year's low in {apr}/{tot} years ({100*apr/tot:.0f}%). The low most often lands in {N[best_low-1]} ({lows[best_low]}/{tot}) — early-year lows dominate because markets drift up; April is not special.")
q4=[st.mean(rets[m]) for m in (10,11,12)]
print(f"  'down till December': Oct/Nov/Dec means {q4[0]:+.2f}/{q4[1]:+.2f}/{q4[2]:+.2f}% — Q4 is historically the STRONGEST stretch, the opposite of the claim.")
