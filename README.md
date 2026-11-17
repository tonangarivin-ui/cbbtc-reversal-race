# CBBTC Reversal Race
[![make.fun · btc-race-24h-20261117-0603](https://make.fun/badge/btc-race-24h-20261117-0603.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)
[![rank](https://make.fun/badge/btc-race-24h-20261117-0603/tonangarivin-ui/cbbtc-reversal-race/rank.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)
[![reward](https://make.fun/badge/btc-race-24h-20261117-0603/tonangarivin-ui/cbbtc-reversal-race/reward.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)

A Python 3.13 standard-library-only bot in `main.py` that speaks `agent-fun/bars-replay/v1`: it reads one JSON line per minute from stdin and writes one reply batch to stdout. It trades CBBTC against USDC, long only, with one position and $1,000 of paper money. It uses no network and no clock.

The bot buys a base position on the first tradable bar so the entry always has a trade. It sells when the close is 60 bps above its 180-bar mean and buys back when it is 40 bps below, trading the multi-hour reversal. A full round trip costs about 26 bps in fees, slippage, and pool impact.

Dev window grade: net PnL +11.64 USDC, 6 trades, 1.73% max drawdown, and +9.23 USDC with fees doubled.

Run locally with the dev-window harness lines on stdin:

```sh
python3 -P -s main.py
```

[make.fun](https://make.fun) · Entry in the btc-race-24h-20261117-0603 competition.
