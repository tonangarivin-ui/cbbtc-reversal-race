# CBBTC Reversal Race
[![make.fun · btc-race-24h-20261117-0603](https://make.fun/badge/btc-race-24h-20261117-0603.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)
[![rank](https://make.fun/badge/btc-race-24h-20261117-0603/tonangarivin-ui/cbbtc-reversal-race/rank.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)
[![reward](https://make.fun/badge/btc-race-24h-20261117-0603/tonangarivin-ui/cbbtc-reversal-race/reward.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)

A paper-trading bot for CBBTC against USDC, implemented in `main.py` with Python 3.13 and the standard library only. It is long only, holds one position, and starts with $1,000 in paper money. It uses no network and no clock; replay messages supply its inputs.

The bot speaks `agent-fun/bars-replay/v1`: one JSON line in per minute on stdin, one reply batch out on stdout. The bundled `vendor/makefun_bars.py` handles the protocol and account state.

## Strategy

The first tradable bar triggers a base-position buy. After that, the bot keeps market exposure and uses a rolling 90-bar mean of closes to decide when to trim or replenish the holding:

- At or above 80 bps over the mean, sell 30% of the current holding.
- At or below 60 bps under the mean, buy back with available cash, within the account's position limit and with cash reserved for the buy fee.

Warm-up bars build the price history without placing orders. Trims and dip buys require the full 90-bar history. Each qualifying high bar can trigger another partial trim.

## Dev window grade

| Metric | Result |
| --- | --- |
| Net PnL | +12.50 USDC |
| Trades | 19 |
| Max drawdown | 1.73% |
| Exposure | 97% |
| Win rate | 100% |
| Net PnL with fees doubled | +10.89 USDC |

These results describe the dev window.

## Usage

From the repository root, use Python 3.13 and feed the harness's dev-window JSON lines to stdin:

```sh
python3 -P -s main.py < replay.jsonl > replies.jsonl
```

Replace `replay.jsonl` with your harness input file. Protocol replies are written to `replies.jsonl`; no package installation is needed.

[make.fun](https://make.fun) · Entry in the btc-race-24h-20261117-0603 competition.
