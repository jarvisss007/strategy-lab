#!/usr/bin/env python3
"""Strategy battery. Each family is a generator of parameter configs; each config
produces a daily, net-of-cost portfolio return series aligned to the price index.
A family therefore yields a (T x N_configs) matrix that feeds the overfitting gate,
where N_configs is exactly the number of trials the Deflated Sharpe must discount.

Conventions
-----------
- prices: pandas DataFrame, DatetimeIndex, columns = tickers, adjusted close.
- We form a weight matrix W (dates x names), then trade it with a 1-day lag:
  a signal computed from the close of day t is held over day t+1's return.
- Net return_t = sum(W_{t-1} * ret_t) - turnover_t * COST, turnover = sum|W_t - W_{t-1}|.
- COST is per unit of traded notional (round-trip is two units of turnover).
"""
import numpy as np
import pandas as pd

COST = 0.0005  # 5 bps per unit turnover (~1 round trip on a full position = 10 bps)


def _returns(prices):
    return prices.pct_change()


def backtest(W, rets, cost=COST):
    """Trade weight matrix W against returns; return a net daily return Series."""
    W = W.reindex(rets.index).fillna(0.0)
    Wl = W.shift(1).fillna(0.0)
    gross = (Wl * rets).sum(axis=1)
    turnover = (W - Wl).abs().sum(axis=1)
    return (gross - turnover * cost).astype(float)


def _norm_long(sig):
    """Equal-weight the active longs so gross exposure = 1 each day."""
    n = sig.abs().sum(axis=1).replace(0, np.nan)
    return sig.div(n, axis=0).fillna(0.0)


# --------------------------------------------------------------- families
def ts_momentum(prices, rets):
    """Time-series momentum: hold names whose trailing L-day return has the given
    sign, rebalanced every H days. Long-only and long/short variants."""
    out = {}
    for L in (21, 63, 126, 252):
        past = prices.pct_change(L)
        for H in (5, 21, 63):
            reb = (np.arange(len(prices)) // H)
            for mode in ("long", "ls"):
                sig = (past > 0).astype(float) if mode == "long" else np.sign(past)
                sig = pd.DataFrame(sig, index=prices.index, columns=prices.columns)
                sig = sig.groupby(reb).transform("first")  # hold within rebalance block
                W = _norm_long(sig) if mode == "long" else sig.div(
                    sig.abs().sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
                out[f"TSMOM L{L} H{H} {mode}"] = backtest(W, rets)
    return out


def xs_momentum(prices, rets):
    """Cross-sectional momentum: each rebalance, rank names by trailing L-day return
    (skipping the most recent S days), go long the top quantile / short the bottom,
    dollar-neutral. The classic academic anomaly."""
    out = {}
    for L in (63, 126, 252):
        for S in (0, 5):
            score = prices.shift(S).pct_change(L)
            for q in (0.1, 0.2, 0.3):
                for H in (5, 21):
                    reb = np.arange(len(prices)) // H
                    def rank_row(r):
                        v = r.dropna()
                        if len(v) < 10:
                            return pd.Series(0.0, index=r.index)
                        k = max(1, int(len(v) * q))
                        w = pd.Series(0.0, index=r.index)
                        top = v.nlargest(k).index
                        bot = v.nsmallest(k).index
                        w[top] = 0.5 / k
                        w[bot] = -0.5 / k
                        return w
                    W = score.apply(rank_row, axis=1)
                    W = W.groupby(reb).transform("first")
                    out[f"XSMOM L{L} skip{S} q{q} H{H}"] = backtest(W, rets)
    return out


def short_reversal(prices, rets):
    """Short-horizon mean reversion: long recent losers, short recent winners over
    an L-day window, held H days, dollar-neutral. Strong in-sample, cost-sensitive."""
    out = {}
    for L in (1, 3, 5):
        score = -prices.pct_change(L)  # negative: losers score high
        for q in (0.1, 0.2):
            for H in (1, 3, 5):
                reb = np.arange(len(prices)) // H
                def rank_row(r):
                    v = r.dropna()
                    if len(v) < 10:
                        return pd.Series(0.0, index=r.index)
                    k = max(1, int(len(v) * q))
                    w = pd.Series(0.0, index=r.index)
                    w[v.nlargest(k).index] = 0.5 / k
                    w[v.nsmallest(k).index] = -0.5 / k
                    return w
                W = score.apply(rank_row, axis=1)
                W = W.groupby(reb).transform("first")
                out[f"STR L{L} q{q} H{H}"] = backtest(W, rets)
    return out


def fifty_two_week(prices, rets):
    """Trade on position within the 52-week high/low range — the anomaly the original
    Stock Master Sheet was built around ("% off high"). Tests BOTH directions honestly:
      - near-high momentum (George & Hwang 2004): long names nearest their 52w high,
        short those furthest — dollar-neutral.
      - dip-buy reversion (the sheet's implicit thesis): the exact opposite — long the
        names most off their high, short those near it.
    Plus long-only screens: hold names near the high, and hold names deep off the high."""
    out = {}
    hi = prices.rolling(252, min_periods=200).max()
    rhi = prices / hi                       # 1.0 = sitting at 52w high, lower = further off
    for q in (0.1, 0.2, 0.3):
        for H in (5, 21):
            reb = np.arange(len(prices)) // H
            def rank_row(r):
                v = r.dropna()
                if len(v) < 10:
                    return pd.Series(0.0, index=r.index)
                k = max(1, int(len(v) * q))
                w = pd.Series(0.0, index=r.index)
                w[v.nlargest(k).index] = 0.5 / k    # nearest the high
                w[v.nsmallest(k).index] = -0.5 / k  # furthest off the high
                return w
            W = rhi.apply(rank_row, axis=1).groupby(reb).transform("first")
            out[f"52wHigh-mom q{q} H{H}"] = backtest(W, rets)      # long near-high
            out[f"52wHigh-revert q{q} H{H}"] = backtest(-W, rets)  # long most-off-high (the sheet)
    # long-only screens
    for thr in (0.90, 0.95):
        out[f"NearHigh-long within{int((1-thr)*100)}pct"] = backtest(
            _norm_long((rhi >= thr).astype(float)), rets)
    for thr in (0.80, 0.70, 0.60):
        out[f"DeepDip-long off{int((1-thr)*100)}pct"] = backtest(
            _norm_long((rhi <= thr).astype(float)), rets)
    return out


def ma_trend(prices, rets):
    """Moving-average trend on the equal-weight basket and on SPY: long when close is
    above its n-day SMA, else flat."""
    out = {}
    for n in (50, 100, 150, 200):
        above = (prices > prices.rolling(n).mean()).astype(float)
        # basket
        W = _norm_long(above)
        out[f"MAtrend basket n{n}"] = backtest(W, rets)
        # SPY alone
        if "SPY" in prices.columns:
            Ws = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
            Ws["SPY"] = above["SPY"]
            out[f"MAtrend SPY n{n}"] = backtest(Ws, rets)
    return out


def donchian(prices, rets):
    """Donchian breakout: long when close makes a new n-day high, exit on m-day low."""
    out = {}
    for n in (50, 100, 200):
        for m in (20, 50):
            hi = prices.rolling(n).max()
            lo = prices.rolling(m).min()
            pos = pd.DataFrame(np.nan, index=prices.index, columns=prices.columns)
            pos[prices >= hi] = 1.0
            pos[prices <= lo] = 0.0
            pos = pos.ffill().fillna(0.0)
            out[f"Donchian hi{n} lo{m}"] = backtest(_norm_long(pos), rets)
    return out


def vol_managed(prices, rets):
    """Volatility-managed SPY: scale exposure to hit a target annual vol."""
    out = {}
    if "SPY" not in prices.columns:
        return out
    spy = rets["SPY"]
    for tgt in (0.10, 0.15, 0.20):
        for lb in (21, 63):
            rv = spy.rolling(lb).std() * np.sqrt(252)
            lev = (tgt / rv).clip(upper=2.0)
            W = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
            W["SPY"] = lev
            out[f"VolMgd SPY tgt{int(tgt*100)} lb{lb}"] = backtest(W, rets)
    return out


def turn_of_month(prices, rets):
    """Calendar: hold the basket only around the turn of the month (last t + first t
    trading days). A known seasonal — included to test it honestly."""
    out = {}
    idx = prices.index
    dom = pd.Series(idx.day, index=idx)
    month = pd.Series(idx.to_period("M"), index=idx)
    is_last = month != month.shift(-1)
    is_first = month != month.shift(1)
    for t in (1, 3, 5):
        # last t days of month OR first t days
        near = pd.Series(False, index=idx)
        for k in range(t):
            near = near | is_last.shift(-k, fill_value=False) | is_first.shift(k, fill_value=False)
        base = _norm_long((prices > 0).astype(float))  # equal weight all names
        W = base.mul(near.astype(float), axis=0)
        out[f"TurnOfMonth t{t}"] = backtest(W, rets)
    return out


def day_of_week(prices, rets):
    """Calendar control: long SPY only on a single weekday. Almost certainly noise —
    included as a canary the honest gate SHOULD reject."""
    out = {}
    if "SPY" not in prices.columns:
        return out
    dow = pd.Series(prices.index.dayofweek, index=prices.index)
    for d, name in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri"]):
        W = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
        W.loc[dow == d, "SPY"] = 1.0
        out[f"DayOfWeek {name}"] = backtest(W, rets)
    return out


FAMILIES = {
    "Time-series momentum": ts_momentum,
    "Cross-sectional momentum": xs_momentum,
    "Short-term reversal": short_reversal,
    "52-week high/low": fifty_two_week,
    "Moving-average trend": ma_trend,
    "Donchian breakout": donchian,
    "Volatility-managed SPY": vol_managed,
    "Turn-of-month seasonality": turn_of_month,
    "Day-of-week (control)": day_of_week,
}
