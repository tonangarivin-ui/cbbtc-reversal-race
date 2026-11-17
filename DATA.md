# Measurements of the shipped 24-hour dev window (1,440 one-minute cbBTC bars)

Taken from `dataset/bars/CBBTC.ndjson.gz` in the kit, re-derived by hand.

## Price level and depth

- close: 64,461.03527 USDC at the first bar, 64,775.95230 at the last (+48.8 bps over 24 hours)
- pool depth at bar opens: median 880,211 USDC raw units x 10^6, min ~709k, max ~1,064k
- an order worth 1,000 USDC meets a price impact of a/D ~ 1,000/880,211 = 11 bps... measured
  exactly by the grader: a 1,000 USDC buy-and-hold round trip paid 800,588 micro-USDC of fees on
  1,000,000,000, i.e. about 8 bps each way including the 4 bps fee and 2 bps slippage.

## Return statistics

- 1-minute returns: mean +0.036 bps, sd 6.44 bps, min -34, max +45
- autocorrelation of 1-minute returns: lag 1 **+0.153**, lag 2 +0.049, lag 3 -0.023,
  lag 10 +0.039, lag 30 -0.004, lag 60 -0.020
- forward return by trailing-return quintile (look 120 bars, forward 60 bars):
  the lowest trailing quintile (-89 bps) returned **+17.7 bps** forward and the highest (+88 bps)
  returned **-32.3 bps** forward. The reversal is strongest at 60-120 bar horizons.
- sign persistence of 30/60/120-bar returns into the next same-length window: 0.46/0.39/0.39,
  i.e. **below** 0.5, so momentum does not persist.

## What was tested and what happened (all with the full cost model)

- Trend-following (buy above an N-bar mean, sell below): **loses** at every lookback from 15 to 480
  bars, -$22 to -$249, because each round trip costs more than the trend it catches.
- Pure mean reversion (all-in when stretched below, exit at the mean or at a take-profit), 180-bar
  mean, -40 bps entry, +80 bps take-profit: dev +$2.55 with 12 trades, but **-$2.32 when fees are
  doubled** - too thin a margin.
- Base position plus reversion overlay (buy the base on the first bar, sell when stretched above the
  mean, buy back when stretched below), 180-bar mean, +60 bps sell, +40 bps buy-back:
  dev **+$18.28**, 8 trades, max drawdown 1.3%, and **+$15.04 with fees doubled**. This is the
  design that survived: its profit does not depend on the cost model being the low one.

## Noise to expect

The dev window is one day. The whole point of the overlay design is that it keeps a base exposure
and only trades the extreme stretch, so it does not need a lucky single trade to be profitable.
