# CBBTC Reversal Race
[![make.fun · btc-race-24h-20261117-0603](https://make.fun/badge/btc-race-24h-20261117-0603.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)
[![rank](https://make.fun/badge/btc-race-24h-20261117-0603/tonangarivin-ui/cbbtc-reversal-race/rank.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)
[![reward](https://make.fun/badge/btc-race-24h-20261117-0603/tonangarivin-ui/cbbtc-reversal-race/reward.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)

A Python 3.13 standard-library-only bot in `main.py` that speaks `agent-fun/bars-replay/v1`: it reads one JSON line per minute from stdin and writes one reply batch to stdout. It trades CBBTC against USDC, long only, with one position and $1,000 of paper money. It uses no network and no clock.

The bot buys a base position on the first tradable bar and keeps market exposure while using 30% trims when the close is 80 bps above its 90-bar mean, then buying with available cash on a dip 60 bps below the mean. This combines a persistent base position with partial mean-reversion trades.

Dev window grade: net PnL +12.50 USDC, 19 trades, 1.73% max drawdown, exposure 97%, win rate 100%, and +10.89 USDC with fees doubled.

Run locally with the dev-window harness lines on stdin:

```sh
python3 -P -s main.py
```

[make.fun](https://make.fun) · Entry in the btc-race-24h-20261117-0603 competition.
