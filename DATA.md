# Development-window evidence

These measurements describe the shipped 24-hour cbBTC development sample.
It contains 1,440 bars at one-minute intervals.

## Prices and liquidity

The first bar closed at 64,461.03527 USDC.
The last bar closed at 64,775.95230 USDC.
The change across the day was +48.8 bps.

Pool depth measured at bar opens had a median of roughly 880,000 USDC.
The observed range was approximately 709,000 to 1,064,000 USDC.

## Minute returns

The mean one-minute return was +0.036 bps.
Its standard deviation was 6.44 bps.
The smallest return was -34 bps and the largest was +45 bps.

Return autocorrelation varied with the lag:

| Lag in minutes | Autocorrelation |
| --- | --- |
| 1 | +0.153 |
| 2 | +0.049 |
| 3 | -0.023 |
| 10 | +0.039 |
| 30 | -0.004 |
| 60 | -0.020 |

## Reversal across longer windows

Sorting observations by their trailing 120-bar return reveals a strong multi-hour reversal.
The bottom fifth gained an average of +17.7 bps during the next 60 bars.
The top fifth returned -32.3 bps over the same forward horizon.

A return's sign rarely persisted into the next window of equal length:

| Window length in bars | Fraction retaining the same sign |
| --- | --- |
| 30 | 0.46 |
| 60 | 0.39 |
| 120 | 0.39 |

These frequencies indicate that momentum does not persist.

## Strategy results after costs

Trend-following lost money at every tested lookback between 15 and 480 bars.
Losses ranged from 22 to 249 USDC, or PnL of -22 to -249 USDC.
Each round trip cost more than the trend captured.

Pure mean reversion with a take-profit produced +2.55 USDC in a 12-trade development run.
Doubling fees changed that result to -2.32 USDC.
That leaves too little margin over trading costs.

The base-position strategy with a reversal overlay used a 180-bar mean.
It sold at +60 bps above the mean and bought back 40 bps below it
(the +40 bps buy-back parameter).
Its development results were:

- Net profit: +18.28 USDC.
- Trade count: 8.
- Maximum drawdown: 1.3%.
- Net profit with doubled fees: +15.04 USDC.

The continued profit under doubled fees shows that this strategy's result does not depend
on the lower-cost model.
